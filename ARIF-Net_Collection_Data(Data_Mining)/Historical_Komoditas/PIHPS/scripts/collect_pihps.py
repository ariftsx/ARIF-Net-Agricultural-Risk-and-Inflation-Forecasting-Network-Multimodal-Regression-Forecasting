"""
ARIF-Net — Phase 1 PIHPS — Langkah 2 (smoke) & 3 (full): collector harga PIHPS Bank Indonesia.

Mode:
  smoke  (a) ambil reference komoditas PIHPS dan verifikasi bahwa setiap comcat_id di
         config/commodities.json memang bernama komoditas yang dimaksud (ID tidak ditebak);
         (b) 1 chunk (default Januari 2019) per komoditas → validasi row Pasar Kramatjati L3.
  full   3 komoditas × chunk bulanan 2019-01 … 2026-09. Hanya berjalan bila smoke PASS.
         Resume otomatis dari manifest.

Aturan (Plan v2.0.0 §10.1a; Contract v2.1.0 §5.6; P1-DG-01…06):
  * Raw = evidence: bytes response disimpan apa adanya + sha256; tidak pernah ditimpa.
  * Tanpa imputasi/ffill. '-' dari sumber dibiarkan (dilaporkan di normalisasi/audit).
  * Satu market: Pasar Kramatjati level 3 (harga eceran). Label regency = source quirk.

Contoh (dari folder Historical_Komoditas\\PIHPS):
  conda run -n arif-net python scripts\\collect_pihps.py smoke
  conda run -n arif-net python scripts\\collect_pihps.py full
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import sys
import time
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    LOGS, MANIFEST, RAW, REFERENCE, REPORTS, ROOT, SMOKE, build_params, date_items, load_configs, load_state,
    market_rows, month_chunks, norm_text, now_utc, parse_price, raw_path, rel, save_json, save_state, sha256_bytes,
    sha256_file, stamp, weekdays, write_new,
)

MANIFEST_FIELDS = [
    "comcat_id", "commodity", "chunk", "start_date", "end_date", "request_url", "http_status", "raw_file",
    "raw_sha256", "raw_bytes", "n_date_keys", "n_reported", "n_dash", "n_expected_weekdays", "check", "error",
    "collected_at_utc",
]
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/154.0.0.0 Safari/537.36")


def setup_logging(tag: str) -> None:
    LOGS.mkdir(exist_ok=True)
    logfile = LOGS / f"collect_{tag}_{stamp()}.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(logfile, encoding="utf-8")])
    logging.info("Log: %s", rel(logfile))


# ---------------------------------------------------------------- HTTP
class Client:
    """Satu session; warm-up halaman PIHPS untuk cookie (tanpa token hard-coded); jeda + backoff."""

    def __init__(self, settings: dict):
        self.s, self.settings = requests.Session(), settings
        self.warm_up()

    def warm_up(self) -> None:
        self.s.headers.clear()
        self.s.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
                               "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                               "Referer": self.settings["base_url"]})
        r = self.s.get(self.settings["page_url"], timeout=self.settings["timeout_seconds"])
        r.raise_for_status()
        xsrf = self.s.cookies.get("XSRF-TOKEN")
        if xsrf:
            self.s.headers["XSRF-TOKEN"] = xsrf
        self.s.headers.update({"Accept": "application/json, text/javascript, */*; q=0.01",
                               "X-Requested-With": "XMLHttpRequest", "Referer": self.settings["page_url"]})
        logging.info("Warm-up OK | HTTP %s | cookies=%s", r.status_code, sorted(self.s.cookies.keys()))

    def pause(self) -> None:
        time.sleep(self.settings["delay_seconds"] + random.uniform(0, self.settings["delay_jitter_seconds"]))

    def get(self, url: str, params: dict | None, label: str) -> requests.Response:
        st = self.settings
        last: Exception | requests.Response | None = None
        rewarmed = False
        for attempt in range(1, st["retries"] + 1):
            try:
                r = self.s.get(url, params=params, timeout=st["timeout_seconds"])
            except requests.RequestException as exc:
                last = exc
                logging.warning("%s: koneksi gagal (%s/%s): %s", label, attempt, st["retries"], exc)
                time.sleep(5 * attempt)
                continue
            self.pause()
            if r.status_code == 429 or r.status_code >= 500:
                last = r
                logging.warning("%s: HTTP %s (%s/%s) → tunggu %ss", label, r.status_code, attempt, st["retries"], 30 * attempt)
                time.sleep(30 * attempt)
                continue
            if r.status_code == 200 and not r.content.lstrip().startswith(b"{") and not rewarmed:
                logging.warning("%s: respons bukan JSON (sesi kedaluwarsa?) → warm-up ulang", label)
                rewarmed = True
                self.warm_up()
                continue
            return r
        if isinstance(last, requests.Response):
            return last
        raise last if last else RuntimeError("request gagal tanpa respons")


# ---------------------------------------------------------------- validasi
def check_chunk(content: bytes, settings: dict, start: date, end: date) -> tuple[list[str], dict]:
    """Validasi struktural chunk (tanpa mengubah data). Return (issues, stats)."""
    try:
        payload = json.loads(content)
    except ValueError as exc:
        return [f"bukan JSON: {exc}"], {}
    try:
        rows = market_rows(payload, settings["market_name"], settings["market_level"])
    except ValueError as exc:
        return [str(exc)], {}
    if len(rows) != 1:
        names = [(r.get("level"), r.get("name")) for r in payload.get("data", []) if isinstance(r, dict)]
        return [f"row '{settings['market_name']}' L{settings['market_level']} = {len(rows)} (harus 1); rows={names}"], {}
    items = date_items(rows[0])
    issues = []
    outside = [d for d, _ in items if not (start <= d <= end)]
    weekend = [d for d, _ in items if d.weekday() >= 5]
    if outside:
        issues.append(f"{len(outside)} tanggal di luar chunk")
    if weekend:
        issues.append(f"{len(weekend)} tanggal akhir pekan: {[d.isoformat() for d in weekend[:3]]}")
    n_dash = n_rep = 0
    for d, v in items:
        try:
            p = parse_price(v)
        except ValueError as exc:
            issues.append(f"{d}: {exc}")
            continue
        n_rep += p is not None
        n_dash += p is None
    stats = {"n_date_keys": len(items), "n_reported": n_rep, "n_dash": n_dash,
             "n_expected_weekdays": len(weekdays(start, end)),
             "first_values": [(d.isoformat(), v) for d, v in items[:3]]}
    return issues, stats


def find_commodity_ids(payload, names: dict[str, str]) -> dict[str, list[str]]:
    """Cari pasangan (comcat_id, nama) di respons reference. Return {comcat_id: [nama ditemukan]}."""
    want = set(names)
    found: dict[str, list[str]] = {cid: [] for cid in want}

    def walk(node) -> None:
        if isinstance(node, list):
            for x in node:
                walk(x)
        elif isinstance(node, dict):
            vals = [str(v).strip() for v in node.values() if isinstance(v, (str, int))]
            ids = [v for v in vals if v in want]
            texts = [v for v in vals if not v.startswith(("com_", "cat_"))]
            for cid in ids:
                found[cid].extend(t for t in texts if norm_text(t) != norm_text(cid))
            for k, v in node.items():  # bentuk peta {"com_3": "Beras ..."}
                if k in want and isinstance(v, str):
                    found[k].append(v)
            for v in node.values():
                walk(v)

    walk(payload)
    return found


# ---------------------------------------------------------------- manifest
def append_manifest(row: dict) -> None:
    new = not MANIFEST.exists()
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in MANIFEST_FIELDS})


def done_chunks() -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    if not MANIFEST.exists():
        return out
    with MANIFEST.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            p = ROOT / r["raw_file"] if r["raw_file"] else None
            if r["http_status"] == "200" and r["check"] == "OK" and p and p.exists() and sha256_file(p) == r["raw_sha256"]:
                out.add((r["comcat_id"], r["chunk"]))
    return out


# ---------------------------------------------------------------- smoke
def cmd_smoke(args) -> int:
    setup_logging("smoke")
    comm, settings = load_configs()
    names = {c["comcat_id"]: c["pihps_name"] for c in comm["commodities"]}
    client = Client(settings)
    checks: list[dict] = []

    def chk(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
        logging.info("[%s] %s%s", "PASS" if ok else "FAIL", name, f" — {detail}" if detail else "")

    # (a) reference → verifikasi ID
    r = client.get(settings["reference_url"], {"_": int(time.time() * 1000)}, "reference")
    ref_file = write_new(REFERENCE / "ref_commodity.json", r.content)
    chk("reference HTTP 200", r.status_code == 200, f"status={r.status_code} file={rel(ref_file)}")
    id_check = {}
    if r.status_code == 200:
        try:
            found = find_commodity_ids(json.loads(r.content), names)
        except ValueError as exc:
            found = {}
            chk("reference = JSON", False, str(exc))
        for cid, name in names.items():
            hits = sorted(set(found.get(cid, [])))
            ok = any(norm_text(h) == norm_text(name) for h in hits)
            id_check[cid] = {"expected": name, "found_names": hits[:5], "verified": ok}
            chk(f"comcat_id {cid} = '{name}' di reference", ok, f"ditemukan: {hits[:3]}")

    # (b) chunk uji per komoditas
    chunk_report = {}
    for cid, name in names.items():
        params = build_params(settings, cid, args.start, args.end, int(time.time() * 1000))
        r = client.get(settings["data_url"], params, f"smoke:{cid}")
        f = write_new(SMOKE / f"{cid}_{args.start:%Y-%m}.json", r.content)
        chk(f"{cid} HTTP 200", r.status_code == 200, f"status={r.status_code}")
        issues, stats = check_chunk(r.content, settings, args.start, args.end) if r.status_code == 200 else (["HTTP"], {})
        chk(f"{cid} struktur & row {settings['market_name']} L{settings['market_level']}", not issues, "; ".join(issues) or
            f"tanggal={stats['n_date_keys']} (hari kerja {stats['n_expected_weekdays']}) dilaporkan={stats['n_reported']} "
            f"'-'={stats['n_dash']} contoh={stats['first_values']}")
        chunk_report[cid] = {"commodity": name, "request_url": r.url, "http_status": r.status_code, "raw_file": rel(f),
                             "raw_sha256": sha256_bytes(r.content), "issues": issues, **stats}

    verdict = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    report = {"step": "Langkah 2 — smoke PIHPS", "verdict": verdict, "period": [str(args.start), str(args.end)],
              "reference_file": rel(ref_file), "id_verification": id_check, "chunks": chunk_report,
              "checks": checks, "checked_at_utc": now_utc()}
    save_json(REPORTS / "smoke_pihps.json", report)
    state = load_state()
    state.setdefault("smoke_history", []).append({"verdict": verdict, "at": report["checked_at_utc"]})
    if verdict == "PASS":
        state["smoke"] = {"verdict": "PASS", "at": report["checked_at_utc"], "ids_verified": sorted(names),
                          "reference_file": rel(ref_file), "report": "reports/smoke_pihps.json"}
    save_state(state)
    logging.info("=" * 60)
    logging.info("HASIL SMOKE PIHPS: %s | laporan: reports/smoke_pihps.json", verdict)
    if verdict == "FAIL":
        logging.info("Jangan lanjut ke full. Laporkan ke peneliti; comcat_id tidak boleh ditebak.")
    return 0 if verdict == "PASS" else 1


# ---------------------------------------------------------------- full
def cmd_full(args) -> int:
    setup_logging("full")
    comm, settings = load_configs()
    if load_state().get("smoke", {}).get("verdict") != "PASS":
        logging.error("Gate gagal: smoke belum PASS (Langkah 2)."); return 1
    start, end = date.fromisoformat(settings["start_date"]), date.fromisoformat(settings["end_date"])
    chunks = month_chunks(start, end)
    targets = [c for c in comm["commodities"] if not args.comcat or c["comcat_id"] == args.comcat]
    done = done_chunks()
    todo = [(c, s, e) for c in targets for s, e in chunks if (c["comcat_id"], f"{s:%Y-%m}") not in done]
    logging.info("Komoditas=%s | chunk/komoditas=%s | sudah selesai=%s | sisa=%s",
                 [c["comcat_id"] for c in targets], len(chunks), len(done), len(todo))
    client = Client(settings) if todo else None
    n_ok = n_err = 0
    for c, s, e in todo:
        cid, label = c["comcat_id"], f"{c['comcat_id']}:{s:%Y-%m}"
        row = {"comcat_id": cid, "commodity": c["pihps_name"], "chunk": f"{s:%Y-%m}", "start_date": s, "end_date": e,
               "collected_at_utc": now_utc()}
        try:
            r = client.get(settings["data_url"], build_params(settings, cid, s, e, int(time.time() * 1000)), label)
        except requests.RequestException as exc:
            row.update({"http_status": "EXC", "check": "EXCEPTION", "error": str(exc)[:300]})
            append_manifest(row); n_err += 1
            logging.error("%s | koneksi gagal: %s", label, exc); continue
        suffix = ".json" if r.status_code == 200 else ".err.json"
        f = write_new(raw_path(cid, s).with_suffix(suffix), r.content)  # evidence: byte-identik
        issues, stats = check_chunk(r.content, settings, s, e) if r.status_code == 200 else ([f"HTTP {r.status_code}"], {})
        row.update({"request_url": r.url, "http_status": r.status_code, "raw_file": rel(f), "raw_sha256": sha256_bytes(r.content),
                    "raw_bytes": len(r.content), **{k: stats.get(k, "") for k in ("n_date_keys", "n_reported", "n_dash", "n_expected_weekdays")},
                    "check": "OK" if not issues else "FAIL", "error": "; ".join(issues)[:500]})
        append_manifest(row)
        if issues:
            n_err += 1
            logging.error("%s | %s", label, row["error"])
        else:
            n_ok += 1
            logging.info("%-14s OK | tanggal=%2s/%2s hari kerja | dilaporkan=%2s | '-'=%s",
                         label, stats["n_date_keys"], stats["n_expected_weekdays"], stats["n_reported"], stats["n_dash"])

    done_after = done_chunks()
    expected = {(c["comcat_id"], f"{s:%Y-%m}") for c in comm["commodities"] for s, _ in chunks}
    per = {c["comcat_id"]: sum(1 for k in done_after if k[0] == c["comcat_id"]) for c in comm["commodities"]}
    complete = expected <= done_after
    summary = {"step": "Langkah 3 — full collection PIHPS", "market": settings["market_name"], "market_level": settings["market_level"],
               "start_date": str(start), "end_date": str(end), "chunk": "monthly", "expected_chunks": len(expected),
               "completed_chunks_total": len(expected & done_after), "completed_chunks_per_commodity": per,
               "this_run": {"requests_ok": n_ok, "requests_error": n_err}, "verdict": "PASS" if complete else "INCOMPLETE",
               "manifest": rel(MANIFEST), "finished_at_utc": now_utc(),
               "note": "Tanpa imputasi/ffill. Nilai '-' dari sumber dilaporkan di normalisasi & audit."}
    save_json(RAW / "collection_summary.json", summary)
    logging.info("=" * 60)
    logging.info("HASIL FULL: %s | selesai %s/%s chunk %s | run ini OK=%s ERROR=%s", summary["verdict"],
                 summary["completed_chunks_total"], len(expected), per, n_ok, n_err)
    if n_err:
        logging.info("Ada chunk gagal → jalankan ulang perintah yang sama (chunk sukses di-skip).")
    return 0 if complete else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Collector PIHPS ARIF-Net (Langkah 2–3).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sm = sub.add_parser("smoke", help="Langkah 2: reference + 1 chunk per komoditas")
    sm.add_argument("--start", type=date.fromisoformat, default=date(2019, 1, 1))
    sm.add_argument("--end", type=date.fromisoformat, default=date(2019, 1, 31))
    fu = sub.add_parser("full", help="Langkah 3: full collection (resume otomatis)")
    fu.add_argument("--comcat", default=None, help="Batasi ke satu comcat_id")
    args = ap.parse_args()
    return cmd_smoke(args) if args.cmd == "smoke" else cmd_full(args)


if __name__ == "__main__":
    sys.exit(main())
