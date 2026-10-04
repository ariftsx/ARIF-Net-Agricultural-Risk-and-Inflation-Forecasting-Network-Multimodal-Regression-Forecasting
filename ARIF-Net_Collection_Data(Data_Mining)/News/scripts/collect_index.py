"""
ARIF-Net — Phase 1 News — Tahap 1: koleksi halaman indeks per (media, tanggal).

Untuk setiap media (P1-DG-25), tanggal (P1-DG-26), dan indeks (config/sources.json):
halaman 1, 2, 3 … diambil sampai halaman kosong ATAU tidak ada artikel baru (stop rule).
Raw = bytes respons ter-gzip (lossless) + sha256 bytes asli di manifest; tidak pernah ditimpa.
Resume: hari berstatus OK di manifest_index_days.csv di-skip. Satu thread per media, jeda per media.

Contoh (dari folder Historical… → News):
  conda run -n arif-net python scripts\\collect_index.py --dates 2019-01-02,2026-09-15          (smoke)
  conda run -n arif-net python scripts\\collect_index.py --source kompas --max-minutes 110      (full, bertahap)
"""
from __future__ import annotations

import argparse
import csv
import logging
import sys
import threading
import time
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    LOGS, MANIFEST_DAYS, MANIFEST_PAGES, article_id, build_index_url, daterange, load_configs, now_utc,
    raw_index_path, rel, rel_raw, save_raw_gz, sha256_bytes, stamp,
)
from parsers import INDEX_PARSERS  # noqa: E402

PAGE_FIELDS = ["run_id", "source", "index", "date", "page", "url", "http_status", "n_items", "n_new_items", "raw_file", "raw_sha256",
               "raw_bytes", "collected_at_utc"]
DAY_FIELDS = ["run_id", "source", "index", "date", "pages_fetched", "n_items_unique", "stop_reason", "status", "error", "finished_at_utc"]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
LOCK = threading.Lock()


def append(path: Path, fields: list[str], row: dict) -> None:
    with LOCK:
        new = not path.exists()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            if new:
                w.writeheader()
            w.writerow({k: row.get(k, "") for k in fields})


def done_days() -> set[tuple[str, str, str]]:
    """Status TERBARU per (source, index, date) = OK → di-skip saat resume."""
    if not MANIFEST_DAYS.exists():
        return set()
    latest: dict[tuple, str] = {}
    with MANIFEST_DAYS.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            latest[(r["source"], r["index"], r["date"])] = r["status"]
    return {k for k, v in latest.items() if v == "OK"}


def fetch(s: requests.Session, url: str, cfg: dict, log: logging.Logger) -> requests.Response | None:
    for attempt in range(1, cfg["retries"] + 1):
        try:
            r = s.get(url, timeout=cfg["timeout_seconds"])
        except requests.RequestException as exc:
            log.warning("koneksi gagal (%s/%s) %s: %s", attempt, cfg["retries"], url, exc)
            time.sleep(10 * attempt); continue
        time.sleep(cfg["delay_seconds"])
        if r.status_code == 429 or r.status_code >= 500:
            log.warning("HTTP %s (%s/%s) → tunggu %ss", r.status_code, attempt, cfg["retries"], 30 * attempt)
            time.sleep(30 * attempt); continue
        return r
    return None


def collect_day(s, cfg, source, scfg, idx, d, log, run_id) -> dict:
    parse = INDEX_PARSERS[source]
    seen: set[str] = set()
    page, pages, stop, no_new_streak = 1, 0, "", 0
    while True:
        if page > cfg["max_pages_per_day"]:
            stop = "MAX_PAGES"; break
        url = build_index_url(idx["url"], d, page, scfg["per_page"])
        r = fetch(s, url, cfg, log)
        if r is None:
            return {"pages_fetched": pages, "n_items_unique": len(seen), "stop_reason": "network", "status": "FAIL", "error": "retries habis"}
        f = save_raw_gz(raw_index_path(scfg["code"], idx["name"], d, page), r.content)
        pages += 1
        items = parse(r.content) if r.status_code == 200 else []
        new = [i for i in items if article_id(i["url"]) not in seen]
        append(MANIFEST_PAGES, PAGE_FIELDS, {"run_id": run_id, "source": source, "index": idx["name"], "date": d.isoformat(), "page": page, "url": r.url,
                                             "http_status": r.status_code, "n_items": len(items), "n_new_items": len(new), "raw_file": rel_raw(f),
                                             "raw_sha256": sha256_bytes(r.content), "raw_bytes": len(r.content), "collected_at_utc": now_utc()})
        if r.status_code != 200:
            if page == 1:
                return {"pages_fetched": pages, "n_items_unique": 0, "stop_reason": f"HTTP {r.status_code}", "status": "FAIL", "error": f"HTTP {r.status_code}"}
            stop = f"HTTP {r.status_code} (setelah halaman terakhir)"; break
        if not items:
            stop = "halaman kosong"; break
        # Stop rule (smoke-1): 2 halaman BERTURUT-TURUT tanpa artikel baru (satu halaman duplikat tidak menghentikan).
        no_new_streak = 0 if new else no_new_streak + 1
        if no_new_streak >= 2:
            stop = "2 halaman berturut-turut tanpa artikel baru"; break
        seen.update(article_id(i["url"]) for i in new)
        page += 1
    return {"pages_fetched": pages, "n_items_unique": len(seen), "stop_reason": stop,
            "status": "OK" if stop != "MAX_PAGES" else "FLAG", "error": "" if stop != "MAX_PAGES" else "batas halaman tercapai"}


def run_source(source: str, cfg: dict, dates: list[date], deadline: float | None, results: dict, run_id: str, redo: bool) -> None:
    scfg = cfg["sources"][source]
    log = logging.getLogger(source)
    s = requests.Session(); s.headers.update({"User-Agent": UA, "Accept-Language": "id-ID,id;q=0.9"})
    done = set() if redo else done_days()
    n = {"OK": 0, "FAIL": 0, "FLAG": 0, "skip": 0}
    for d in dates:
        for idx in scfg["indexes"]:
            if (source, idx["name"], d.isoformat()) in done:
                n["skip"] += 1; continue
            if deadline and time.time() > deadline:
                log.info("batas waktu run tercapai → berhenti rapi (resume di run berikutnya)")
                results[source] = n; return
            res = collect_day(s, cfg, source, scfg, idx, d, log, run_id)
            append(MANIFEST_DAYS, DAY_FIELDS, {"run_id": run_id, "source": source, "index": idx["name"], "date": d.isoformat(), **res, "finished_at_utc": now_utc()})
            n[res["status"]] += 1
            log.info("%s %-4s %s | halaman=%2s artikel=%3s | %s | %s", source, idx["name"], d, res["pages_fetched"],
                     res["n_items_unique"], res["status"], res["stop_reason"])
    results[source] = n


def main() -> int:
    ap = argparse.ArgumentParser(description="Tahap 1 — koleksi indeks News.")
    ap.add_argument("--source", default="all", help="nama media (koma) atau 'all'")
    ap.add_argument("--dates", default=None, help="daftar tanggal YYYY-MM-DD dipisah koma (smoke)")
    ap.add_argument("--start", default=None); ap.add_argument("--end", default=None)
    ap.add_argument("--max-minutes", type=float, default=None, help="berhenti rapi setelah N menit")
    ap.add_argument("--redo", action="store_true", help="ambil ulang hari yang sudah OK (run baru; raw lama tidak ditimpa)")
    args = ap.parse_args()

    cfg, _ = load_configs()
    sources = list(cfg["sources"]) if args.source == "all" else [x.strip() for x in args.source.split(",")]
    unknown = [x for x in sources if x not in cfg["sources"]]
    if unknown:
        print(f"[FAIL] media tidak dikenal (bukan P1-DG-25): {unknown}"); return 1
    if args.dates:
        dates = [date.fromisoformat(x.strip()) for x in args.dates.split(",")]
    else:
        dates = daterange(date.fromisoformat(args.start or cfg["period"]["start"]), date.fromisoformat(args.end or cfg["period"]["end"]))
    p0, p1 = date.fromisoformat(cfg["period"]["start"]), date.fromisoformat(cfg["period"]["end"])
    if any(not (p0 <= d <= p1) for d in dates):
        print(f"[FAIL] tanggal di luar periode P1-DG-26 {p0}→{p1}"); return 1

    LOGS.mkdir(exist_ok=True)
    logfile = LOGS / f"collect_index_{stamp()}.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)-13s | %(levelname)s | %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(logfile, encoding="utf-8")])
    logging.info("Log %s | media=%s | tanggal=%s (%s → %s)", rel(logfile), sources, len(dates), dates[0], dates[-1])
    deadline = time.time() + args.max_minutes * 60 if args.max_minutes else None
    results: dict = {}
    run_id = stamp()
    logging.info("run_id=%s redo=%s", run_id, args.redo)
    threads = [threading.Thread(target=run_source, args=(src, cfg, dates, deadline, results, run_id, args.redo), name=src) for src in sources]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    logging.info("SELESAI run: %s", results)
    return 0 if all(v.get("FAIL", 0) == 0 for v in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
