"""
ARIF-Net — Phase 1 News — Tahap 2: waktu terbit artikel RELEVAN yang indeksnya tidak memuat jam.

Hanya media ber-time_strategy 'article_jsonld' (CNN Indonesia, CNBC Indonesia; docs §3b: angka di URL ≠ waktu terbit).
Hanya artikel yang judulnya cocok kata kunci P1-DG-27 (P1-DG-30). Yang diambil HANYA waktu terbit
(JSON-LD datePublished / meta article:published_time); teks penuh tidak disimpan ke processed (P1-DG-29).
Raw halaman artikel disimpan gzip LOKAL (tidak di-commit) + sha256 di manifest. Resume via manifest.

Contoh: conda run -n arif-net python scripts\\collect_articles.py --max-minutes 110
"""
from __future__ import annotations

import argparse
import csv
import logging
import sys
import threading
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_index import UA, append, fetch  # noqa: E402
from common import (  # noqa: E402
    LOGS, MANIFEST_ARTICLES, KeywordMatcher, load_configs, now_utc, raw_article_path, rel, rel_raw, save_raw_gz, sha256_bytes,
    stamp, to_wib_iso,
)
from index_items import iter_items  # noqa: E402
from parsers import parse_article_time  # noqa: E402

FIELDS = ["article_id", "source", "url", "http_status", "raw_file", "raw_sha256", "published_at_wib", "time_source",
          "check", "collected_at_utc"]


def done_ids() -> set[str]:
    if not MANIFEST_ARTICLES.exists():
        return set()
    with MANIFEST_ARTICLES.open(encoding="utf-8") as fh:
        return {r["article_id"] for r in csv.DictReader(fh) if r["check"] == "OK"}


def run_source(source, todo, cfg, deadline, results):
    log = logging.getLogger(source)
    s = requests.Session(); s.headers.update({"User-Agent": UA, "Accept-Language": "id-ID,id;q=0.9"})
    n = {"OK": 0, "NO_TIME": 0, "FAIL": 0}
    for it in todo:
        if deadline and time.time() > deadline:
            log.info("batas waktu run tercapai → berhenti rapi"); break
        r = fetch(s, it["url"], cfg, log)
        row = {"article_id": it["article_id"], "source": source, "url": it["url"], "collected_at_utc": now_utc()}
        if r is None:
            row.update({"http_status": "EXC", "check": "FAIL"}); n["FAIL"] += 1
        else:
            f = save_raw_gz(raw_article_path(cfg["sources"][source]["code"], it["article_id"]), r.content)
            dt, src = parse_article_time(r.content) if r.status_code == 200 else (None, "")
            chk = "OK" if dt else ("NO_TIME" if r.status_code == 200 else "FAIL")
            row.update({"http_status": r.status_code, "raw_file": rel_raw(f), "raw_sha256": sha256_bytes(r.content),
                        "published_at_wib": to_wib_iso(dt) if dt else "", "time_source": src, "check": chk})
            n[chk] += 1
        append(MANIFEST_ARTICLES, FIELDS, row)
    results[source] = n
    log.info("%s selesai run: %s", source, n)


def main() -> int:
    ap = argparse.ArgumentParser(description="Tahap 2 — waktu terbit artikel relevan (CNN, CNBC).")
    ap.add_argument("--max-minutes", type=float, default=None)
    ap.add_argument("--limit", type=int, default=None, help="maks artikel per media (smoke)")
    ap.add_argument("--start", default=None, help="batasi ke tanggal indeks ≥ YYYY-MM-DD (fase)")
    ap.add_argument("--end", default=None, help="batasi ke tanggal indeks ≤ YYYY-MM-DD (fase)")
    args = ap.parse_args()
    cfg, scope = load_configs()
    targets = {k for k, v in cfg["sources"].items() if v["time_strategy"] == "article_jsonld"}
    matcher = KeywordMatcher(scope["topics"])
    LOGS.mkdir(exist_ok=True)
    logfile = LOGS / f"collect_articles_{stamp()}.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)-13s | %(levelname)s | %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(logfile, encoding="utf-8")])
    problems: list[str] = []
    done, todo, seen = done_ids(), {t: [] for t in targets}, set()
    for it in iter_items(problems, targets, args.start, args.end):
        if it["article_id"] in seen or it["article_id"] in done:
            continue
        seen.add(it["article_id"])
        if matcher.match(it["title"])[0]:
            todo[it["source"]].append(it)
    if args.limit:
        todo = {k: v[: args.limit] for k, v in todo.items()}
    for p in problems:
        logging.error("[INTEGRITAS] %s", p)
    logging.info("Log %s | artikel relevan yang perlu waktu terbit: %s", rel(logfile), {k: len(v) for k, v in todo.items()})
    deadline = time.time() + args.max_minutes * 60 if args.max_minutes else None
    results: dict = {}
    threads = [threading.Thread(target=run_source, args=(src, todo[src], cfg, deadline, results)) for src in targets]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    logging.info("SELESAI: %s", results)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
