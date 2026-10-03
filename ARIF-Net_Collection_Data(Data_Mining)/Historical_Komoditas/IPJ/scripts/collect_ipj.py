"""
ARIF-Net — Phase 1 IPJ — Langkah 2 (smoke) & 3 (full): collector harga Info Pangan Jakarta.

  smoke  (a) /v1/master-data/market?search_text=kramat → verifikasi market_id 12 = 'Pasar Kramat Jati';
         (b) /v1/public/report 2024-01 → 3 komoditas terpetakan ada, nama cocok, 31 hari, nilai numerik.
  full   semua bulan 2019-01 … 2026-09 (93 request). Status per bulan:
           OK        ada data untuk ≥1 komoditas terpetakan
           OK_EMPTY  respons valid tetapi recaps ketiga komoditas kosong (= tidak tersedia di sumber)
           FAIL      HTTP/JSON/struktur/nama komoditas/tanggal tidak sesuai → diulang saat resume

Raw = bytes response apa adanya + sha256 (tidak pernah ditimpa); memuat semua komoditas pasar.
Tanpa imputasi. Tidak ada cookie/token hard-coded.

Contoh (dari folder Historical_Komoditas\\IPJ):
  conda run -n arif-net python scripts\\collect_ipj.py smoke
  conda run -n arif-net python scripts\\collect_ipj.py full
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
    LOGS, MANIFEST, RAW, REFERENCE, REPORTS, ROOT, SMOKE, build_report_params, load_configs, load_state, month_bounds,
    months, now_utc, parse_value, raw_path, rel, report_rows, save_json, save_state, sha256_bytes, sha256_file, stamp,
    write_new,
)

MANIFEST_FIELDS = ["chunk", "request_url", "http_status", "raw_file", "raw_sha256", "raw_bytes", "n_commodities",
                   "recaps_per_target", "check", "error", "collected_at_utc"]
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/154.0.0.0 Safari/537.36")
DONE_STATES = {"OK", "OK_EMPTY"}


def setup_logging(tag: str) -> None:
    LOGS.mkdir(exist_ok=True)
    logfile = LOGS / f"collect_{tag}_{stamp()}.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(logfile, encoding="utf-8")])
    logging.info("Log: %s", rel(logfile))


class Client:
    def __init__(self, settings: dict):
        self.st, self.s = settings, requests.Session()
        self.s.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json, text/plain, */*",
                               "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8", "Referer": settings["page_url"]})

    def get(self, path: str, params: dict, label: str) -> requests.Response:
        last: Exception | requests.Response | None = None
        for attempt in range(1, self.st["retries"] + 1):
            try:
                r = self.s.get(self.st["base_url"] + path, params=params, timeout=self.st["timeout_seconds"])
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


def norm(text: object) -> str:
    return " ".join(str(text or "").lower().split())


def check_month(content: bytes, mapping: list[dict], year_month: str) -> tuple[str, list[str], dict]:
    """Return (status OK/OK_EMPTY/FAIL, issues, stats). Tidak mengubah data."""
    try:
        rows = report_rows(json.loads(content))
    except ValueError as exc:
        return "FAIL", [str(exc)], {}
    start, end = month_bounds(year_month)
    issues, counts, dup_identical = [], {}, []
    for m in mapping:
        hit = [r for r in rows if r.get("commodity_id") == m["ipj_commodity_id"]]
        if len(hit) != 1:
            issues.append(f"commodity_id {m['ipj_commodity_id']} muncul {len(hit)}x (harus 1)"); continue
        row = hit[0]
        if norm(row.get("commodity_name")) != norm(m["ipj_commodity_name"]):
            issues.append(f"nama commodity_id {m['ipj_commodity_id']} = {row.get('commodity_name')!r} ≠ {m['ipj_commodity_name']!r}")
        recaps = row.get("recaps") or []
        seen: dict[date, float | None] = {}
        for rc in recaps:
            try:
                d = date.fromisoformat(str(rc.get("time")))
                v = parse_value(rc.get("value"))
            except ValueError as exc:
                issues.append(f"{m['comcat_id']}: {exc}"); continue
            if not (start <= d <= end):
                issues.append(f"{m['comcat_id']}: tanggal {d} di luar {year_month}")
            if d in seen:
                # Keputusan peneliti 2026-10-03: duplikat bernilai IDENTIK = entri ganda sumber → diterima
                # (dinormalisasi jadi 1 baris, dicatat). Duplikat bernilai BERBEDA → FAIL (decision gate).
                if seen[d] == v:
                    dup_identical.append(f"{m['comcat_id']}:{d}")
                else:
                    issues.append(f"{m['comcat_id']}: tanggal {d} duplikat dengan nilai berbeda ({seen[d]} vs {v})")
            seen[d] = v
        counts[m["comcat_id"]] = len(seen)
    stats = {"n_commodities": len(rows), "recaps_per_target": counts, "days_in_month": (end - start).days + 1,
             "duplicate_identical": dup_identical}
    if issues:
        return "FAIL", issues, stats
    return ("OK" if any(counts.values()) else "OK_EMPTY"), [], stats


def append_manifest(row: dict) -> None:
    new = not MANIFEST.exists()
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in MANIFEST_FIELDS})


def done_chunks() -> dict[str, str]:
    out: dict[str, str] = {}
    if MANIFEST.exists():
        with MANIFEST.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                p = ROOT / r["raw_file"] if r["raw_file"] else None
                if r["http_status"] == "200" and r["check"] in DONE_STATES and p and p.exists() and sha256_file(p) == r["raw_sha256"]:
                    out[r["chunk"]] = r["check"]
    return out


def fmt_counts(counts: dict) -> str:
    return "|".join(f"{k}:{v}" for k, v in counts.items())


# ---------------------------------------------------------------- smoke
def cmd_smoke(args) -> int:
    setup_logging("smoke")
    comm, st = load_configs()
    client = Client(st)
    checks: list[dict] = []

    def chk(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
        logging.info("[%s] %s%s", "PASS" if ok else "FAIL", name, f" — {detail}" if detail else "")

    r = client.get(st["market_path"], {"search_text": st["market_search_text"]}, "market")
    ref = write_new(REFERENCE / "market_kramat.json", r.content)
    market = None
    try:
        payload = r.json()
        items = payload.get("data", payload)
        items = items.get("data", items) if isinstance(items, dict) else items
        market = next((m for m in items or [] if str(m.get("market_id")) == str(st["market_id"])), None)
    except ValueError:
        pass
    chk("market reference HTTP 200", r.status_code == 200, f"file={rel(ref)}")
    chk(f"market_id {st['market_id']} = '{st['market_name']}'", bool(market) and norm(market.get("market_name")) == norm(st["market_name"]),
        f"ditemukan: {market}")

    r = client.get(st["report_path"], build_report_params(st, args.month), f"smoke:{args.month}")
    f = write_new(SMOKE / f"{args.month}.json", r.content)
    status, issues, stats = check_month(r.content, comm["commodities"], args.month) if r.status_code == 200 else ("FAIL", [f"HTTP {r.status_code}"], {})
    chk(f"report {args.month} HTTP 200 & struktur", status != "FAIL", "; ".join(issues) or f"status={status} {stats}")
    full = stats.get("days_in_month")
    for cid, n in (stats.get("recaps_per_target") or {}).items():
        chk(f"{cid}: recaps = {full} hari", n == full, f"{n}")
    verdict = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    report = {"step": "Langkah 2 — smoke IPJ", "verdict": verdict, "market": market, "reference_file": rel(ref),
              "month": args.month, "request_url": r.url, "raw_file": rel(f), "raw_sha256": sha256_bytes(r.content),
              "stats": stats, "checks": checks, "checked_at_utc": now_utc()}
    save_json(REPORTS / "smoke_ipj.json", report)
    state = load_state()
    state.setdefault("smoke_history", []).append({"verdict": verdict, "at": report["checked_at_utc"]})
    if verdict == "PASS":
        state["smoke"] = {"verdict": "PASS", "at": report["checked_at_utc"], "market_verified": market, "report": "reports/smoke_ipj.json"}
    save_state(state)
    logging.info("HASIL SMOKE IPJ: %s | laporan: reports/smoke_ipj.json", verdict)
    return 0 if verdict == "PASS" else 1


# ---------------------------------------------------------------- full
def cmd_full(_args) -> int:
    setup_logging("full")
    comm, st = load_configs()
    if load_state().get("smoke", {}).get("verdict") != "PASS":
        logging.error("Gate gagal: smoke belum PASS."); return 1
    all_months = months(st["start_month"], st["end_month"])
    done = done_chunks()
    todo = [m for m in all_months if m not in done]
    logging.info("Bulan=%s | sudah selesai=%s | sisa=%s", len(all_months), len(done), len(todo))
    client = Client(st)
    n = {"OK": 0, "OK_EMPTY": 0, "FAIL": 0}
    for ym in todo:
        row = {"chunk": ym, "collected_at_utc": now_utc()}
        try:
            r = client.get(st["report_path"], build_report_params(st, ym), ym)
        except requests.RequestException as exc:
            row.update({"http_status": "EXC", "check": "FAIL", "error": str(exc)[:300]})
            append_manifest(row); n["FAIL"] += 1; continue
        f = write_new(raw_path(ym).with_suffix(".json" if r.status_code == 200 else ".err.json"), r.content)
        status, issues, stats = check_month(r.content, comm["commodities"], ym) if r.status_code == 200 else ("FAIL", [f"HTTP {r.status_code}"], {})
        row.update({"request_url": r.url, "http_status": r.status_code, "raw_file": rel(f), "raw_sha256": sha256_bytes(r.content),
                    "raw_bytes": len(r.content), "n_commodities": stats.get("n_commodities", ""),
                    "recaps_per_target": fmt_counts(stats.get("recaps_per_target", {})), "check": status,
                    "error": "; ".join(issues)[:500] if issues else
                    ("NOTE duplikat identik (diterima): " + ",".join(stats["duplicate_identical"]) if stats.get("duplicate_identical") else "")})
        append_manifest(row)
        n[status] += 1
        (logging.error if status == "FAIL" else logging.info)("%s %-8s | %s %s", ym, status, row["recaps_per_target"], row["error"])

    done_after = done_chunks()
    data_months = sorted(m for m, s in done_after.items() if s == "OK")
    summary = {"step": "Langkah 3 — full collection IPJ", "market_id": st["market_id"], "market_name": st["market_name"],
               "months_expected": len(all_months), "months_done": len(set(all_months) & set(done_after)),
               "months_with_data": len(data_months), "months_empty": sum(1 for s in done_after.values() if s == "OK_EMPTY"),
               "first_month_with_data": data_months[0] if data_months else None,
               "last_month_with_data": data_months[-1] if data_months else None,
               "this_run": n, "verdict": "PASS" if set(all_months) <= set(done_after) else "INCOMPLETE",
               "manifest": rel(MANIFEST), "finished_at_utc": now_utc(),
               "note": "OK_EMPTY = respons valid tanpa data untuk 3 komoditas terpetakan (tidak tersedia di sumber). Tanpa imputasi."}
    save_json(RAW / "collection_summary.json", summary)
    logging.info("HASIL FULL: %s | %s/%s bulan | berisi data=%s (%s → %s) | kosong=%s | run ini %s",
                 summary["verdict"], summary["months_done"], len(all_months), summary["months_with_data"],
                 summary["first_month_with_data"], summary["last_month_with_data"], summary["months_empty"], n)
    return 0 if summary["verdict"] == "PASS" else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Collector IPJ ARIF-Net (Langkah 2–3).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sm = sub.add_parser("smoke")
    sm.add_argument("--month", default="2024-01")
    sub.add_parser("full")
    args = ap.parse_args()
    return cmd_smoke(args) if args.cmd == "smoke" else cmd_full(args)


if __name__ == "__main__":
    sys.exit(main())
