"""
ARIF-Net — Phase 1 PIBC — Langkah 2 (smoke) & 3 (full): collector harga beras PIBC.

Endpoint DataTables GET /rice-price-detail (tangkapan DevTools peneliti 2026-10-03).
  smoke  1 request Januari 2019 → cek 2019-01-01 ikut terambil (start_date eksklusif), 31 baris, 15 field.
  full   chunk tahunan 2019 … 2025 (2025 berakhir 2025-06-16 = data terakhir sumber). Resume via manifest.

Aturan: raw = bytes response apa adanya + sha256 (tidak pernah ditimpa). Respons memuat ke-14 varietas;
hanya kolom yang dipetakan ke Beras Medium I (keputusan peneliti, P1-DG-05) yang dinormalisasi nanti.
Tanpa imputasi/ffill. Cookie diambil lewat warm-up; tidak ada cookie/token hard-coded.

Contoh (dari folder PIBC):
  conda run -n arif-net python scripts\\collect_pibc.py smoke
  conda run -n arif-net python scripts\\collect_pibc.py full
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    LOGS, MANIFEST, RAW, REPORTS, ROOT, SMOKE, build_params, load_configs, load_state, n_days, now_utc,
    parse_price, parse_tgl, raw_path, rel, save_json, save_state, sha256_bytes, sha256_file, stamp, write_new,
    year_chunks,
)

MANIFEST_FIELDS = ["chunk", "start_date", "end_date", "request_url", "http_status", "raw_file", "raw_sha256", "raw_bytes",
                   "records_filtered", "n_rows", "n_expected_days", "first_tgl", "last_tgl", "n_empty_values", "check",
                   "error", "collected_at_utc"]
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/154.0.0.0 Safari/537.36")


def setup_logging(tag: str) -> None:
    LOGS.mkdir(exist_ok=True)
    logfile = LOGS / f"collect_{tag}_{stamp()}.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(logfile, encoding="utf-8")])
    logging.info("Log: %s", rel(logfile))


class Client:
    def __init__(self, settings: dict):
        self.s, self.st = requests.Session(), settings
        self.s.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8"})
        r = self.s.get(settings["page_url"], timeout=settings["timeout_seconds"])
        r.raise_for_status()
        self.s.headers.update({"Accept": "application/json, text/javascript, */*; q=0.01",
                               "X-Requested-With": "XMLHttpRequest", "Referer": settings["page_url"]})
        logging.info("Warm-up OK | HTTP %s | cookies=%s", r.status_code, sorted(self.s.cookies.keys()))

    def get(self, params: dict, label: str) -> requests.Response:
        last: Exception | requests.Response | None = None
        for attempt in range(1, self.st["retries"] + 1):
            try:
                r = self.s.get(self.st["data_url"], params=params, timeout=self.st["timeout_seconds"])
            except requests.RequestException as exc:
                last = exc
                logging.warning("%s: koneksi gagal (%s/%s): %s", label, attempt, self.st["retries"], exc)
                time.sleep(5 * attempt); continue
            time.sleep(self.st["delay_seconds"])
            if r.status_code == 429 or r.status_code >= 500:
                last = r
                logging.warning("%s: HTTP %s → tunggu %ss", label, r.status_code, 30 * attempt)
                time.sleep(30 * attempt); continue
            return r
        if isinstance(last, requests.Response):
            return last
        raise last if last else RuntimeError("request gagal")


def check_chunk(content: bytes, columns: list[str], start: date, end: date, page_length: int) -> tuple[list[str], dict]:
    """Validasi struktural (tanpa mengubah data). Data PIBC harian penuh → baris = jumlah hari."""
    try:
        pl = json.loads(content)
    except ValueError as exc:
        return [f"bukan JSON: {exc}"], {}
    rows = pl.get("data") if isinstance(pl, dict) else None
    if not isinstance(rows, list):
        return ["respons tanpa data[]"], {}
    issues, empty = [], 0
    rf = pl.get("recordsFiltered")
    if isinstance(rf, int) and rf > page_length:
        issues.append(f"recordsFiltered {rf} > page_length {page_length} (perlu pagination)")
    dates = []
    for i, r in enumerate(rows):
        missing = [c for c in columns if c not in r]
        if missing:
            issues.append(f"baris {i}: field hilang {missing}"); continue
        try:
            dates.append(parse_tgl(r["tgl"]))
            for c in columns[1:]:
                empty += parse_price(r[c]) is None
        except ValueError as exc:
            issues.append(f"baris {i}: {exc}")
    exp = n_days(start, end)
    if len(rows) != exp or rf != len(rows):
        issues.append(f"baris={len(rows)} recordsFiltered={rf} hari={exp}")
    if dates and (dates[0] != start or dates[-1] != end):
        issues.append(f"rentang {dates[0]}→{dates[-1]} ≠ {start}→{end}")
    if len(set(dates)) != len(dates):
        issues.append(f"{len(dates) - len(set(dates))} tanggal duplikat")
    stats = {"records_filtered": rf, "n_rows": len(rows), "n_expected_days": exp,
             "first_tgl": rows[0]["tgl"] if rows else "", "last_tgl": rows[-1]["tgl"] if rows else "", "n_empty_values": empty}
    return issues, stats


def append_manifest(row: dict) -> None:
    new = not MANIFEST.exists()
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in MANIFEST_FIELDS})


def done_chunks() -> set[str]:
    out: set[str] = set()
    if MANIFEST.exists():
        with MANIFEST.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                p = ROOT / r["raw_file"] if r["raw_file"] else None
                if r["http_status"] == "200" and r["check"] == "OK" and p and p.exists() and sha256_file(p) == r["raw_sha256"]:
                    out.add(r["chunk"])
    return out


def cmd_smoke(args) -> int:
    setup_logging("smoke")
    _, st = load_configs()
    client = Client(st)
    r = client.get(build_params(st, args.start, args.end, 0, int(time.time() * 1000)), "smoke")
    f = write_new(SMOKE / f"{args.start:%Y-%m}.json", r.content)
    issues, stats = check_chunk(r.content, st["columns"], args.start, args.end, st["page_length"]) if r.status_code == 200 \
        else ([f"HTTP {r.status_code}"], {})
    verdict = "PASS" if not issues else "FAIL"
    first = json.loads(r.content)["data"][:2] if r.status_code == 200 and not any("JSON" in i for i in issues) else None
    report = {"step": "Langkah 2 — smoke PIBC", "verdict": verdict, "period": [str(args.start), str(args.end)],
              "request_url": r.url, "http_status": r.status_code, "raw_file": rel(f), "raw_sha256": sha256_bytes(r.content),
              "issues": issues, **stats, "first_rows": first, "checked_at_utc": now_utc()}
    save_json(REPORTS / "smoke_pibc.json", report)
    for k in ("records_filtered", "n_rows", "n_expected_days", "first_tgl", "last_tgl", "n_empty_values"):
        logging.info("%-17s %s", k, stats.get(k))
    for i in issues:
        logging.error("[FAIL] %s", i)
    state = load_state()
    state.setdefault("smoke_history", []).append({"verdict": verdict, "at": report["checked_at_utc"]})
    if verdict == "PASS":
        state["smoke"] = {"verdict": "PASS", "at": report["checked_at_utc"], "report": "reports/smoke_pibc.json"}
    save_state(state)
    logging.info("HASIL SMOKE PIBC: %s | laporan: reports/smoke_pibc.json", verdict)
    return 0 if verdict == "PASS" else 1


def cmd_full(_args) -> int:
    setup_logging("full")
    _, st = load_configs()
    if load_state().get("smoke", {}).get("verdict") != "PASS":
        logging.error("Gate gagal: smoke belum PASS."); return 1
    start, end = date.fromisoformat(st["start_date"]), date.fromisoformat(st["end_date"])
    chunks = year_chunks(start, end)
    done = done_chunks()
    todo = [(s, e) for s, e in chunks if str(s.year) not in done]
    logging.info("Chunk tahunan=%s | sudah selesai=%s | sisa=%s", len(chunks), len(done), len(todo))
    client = Client(st) if todo else None
    n_ok = n_err = 0
    for s, e in todo:
        label = str(s.year)
        row = {"chunk": label, "start_date": s, "end_date": e, "collected_at_utc": now_utc()}
        try:
            r = client.get(build_params(st, s, e, 0, int(time.time() * 1000)), label)
        except requests.RequestException as exc:
            row.update({"http_status": "EXC", "check": "EXCEPTION", "error": str(exc)[:300]})
            append_manifest(row); n_err += 1; continue
        f = write_new(raw_path(s).with_suffix(".json" if r.status_code == 200 else ".err.json"), r.content)
        issues, stats = check_chunk(r.content, st["columns"], s, e, st["page_length"]) if r.status_code == 200 \
            else ([f"HTTP {r.status_code}"], {})
        row.update({"request_url": r.url, "http_status": r.status_code, "raw_file": rel(f),
                    "raw_sha256": sha256_bytes(r.content), "raw_bytes": len(r.content), **stats,
                    "check": "OK" if not issues else "FAIL", "error": "; ".join(issues)[:500]})
        append_manifest(row)
        if issues:
            n_err += 1; logging.error("%s | %s", label, row["error"])
        else:
            n_ok += 1
            logging.info("%s OK | baris=%s/%s hari | %s → %s | nilai kosong=%s", label, stats["n_rows"],
                         stats["n_expected_days"], stats["first_tgl"], stats["last_tgl"], stats["n_empty_values"])
    done_after = done_chunks()
    expected = {str(s.year) for s, _ in chunks}
    summary = {"step": "Langkah 3 — full collection PIBC", "start_date": str(start), "end_date": str(end), "chunk": "yearly",
               "expected_chunks": len(expected), "completed_chunks": len(expected & done_after),
               "expected_rows": n_days(start, end), "this_run": {"requests_ok": n_ok, "requests_error": n_err},
               "verdict": "PASS" if expected <= done_after else "INCOMPLETE", "manifest": rel(MANIFEST),
               "finished_at_utc": now_utc(), "note": "Raw memuat 14 varietas; tanpa imputasi."}
    save_json(RAW / "collection_summary.json", summary)
    logging.info("HASIL FULL: %s | %s/%s chunk | run ini OK=%s ERROR=%s", summary["verdict"],
                 summary["completed_chunks"], len(expected), n_ok, n_err)
    return 0 if summary["verdict"] == "PASS" else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Collector PIBC ARIF-Net (Langkah 2–3).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sm = sub.add_parser("smoke")
    sm.add_argument("--start", type=date.fromisoformat, default=date(2019, 1, 1))
    sm.add_argument("--end", type=date.fromisoformat, default=date(2019, 1, 31))
    sub.add_parser("full")
    args = ap.parse_args()
    return cmd_smoke(args) if args.cmd == "smoke" else cmd_full(args)


if __name__ == "__main__":
    sys.exit(main())
