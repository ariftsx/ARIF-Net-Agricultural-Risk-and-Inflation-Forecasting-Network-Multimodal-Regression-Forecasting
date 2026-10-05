"""
ARIF-Net — Phase 1 News — normalisasi: raw indeks (+ waktu artikel) → tabel artikel.

  1. Item dari raw indeks (sha256 diverifikasi; index_items.iter_items).
  2. Dedup per article_id (sha1 URL kanonik); kemunculan pertama (tanggal & halaman terawal) dipakai.
  3. published_at_wib: dari indeks (Detik/Liputan6/Kontan), URL (Kompas), atau JSON-LD artikel (CNN/CNBC, Tahap 2).
  4. Relevansi = kata kunci P1-DG-27 pada judul (P1-DG-30) → topics_matched, keywords_matched.
  5. wilayah_pemasok = location_id 18 kabupaten pemasok (P1-DG-11) yang disebut di judul (keputusan peneliti 2026-10-03).

Output:
  data/processed/news/articles_relevant.csv   (di-commit, LFS) — hanya artikel relevan
  data/processed/news/daily_counts.csv        (di-commit) — total & relevan per media per hari (penyebut volume)
  data/processed/news/articles_all.csv.gz     (LOKAL) — semua judul
Tanpa teks penuh (P1-DG-29), tanpa skor sentimen/agregasi fitur (Phase 3).
"""
from __future__ import annotations

import csv
import gzip
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (MANIFEST_ARTICLES, PROCESSED, REPORTS, KeywordMatcher, RegionMatcher, load_configs, load_supplier_locations,
                    now_utc, rel, save_json, to_wib_iso)  # noqa: E402
from index_items import iter_items  # noqa: E402

COLS = ["article_id", "source", "index", "channel", "url", "title", "published_at_wib", "time_source", "time_precision",
        "index_date", "index_page", "topics_matched", "keywords_matched", "wilayah_pemasok", "is_relevant", "raw_index_sha256", "raw_article_sha256"]


def article_times() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if MANIFEST_ARTICLES.exists():
        with MANIFEST_ARTICLES.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["check"] == "OK":
                    out[r["article_id"]] = r
    return out


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 News | Normalisasi"); print("=" * 72)
    cfg, scope = load_configs()
    matcher = KeywordMatcher(scope["topics"])
    regions = RegionMatcher(load_supplier_locations())   # kolom wilayah_pemasok (keputusan peneliti 2026-10-03)
    times = article_times()
    problems: list[str] = []
    rows: dict[str, dict] = {}
    dup = defaultdict(int)
    for it in iter_items(problems):
        aid = it["article_id"]
        if aid in rows:
            dup[it["source"]] += 1; continue
        topics, kws = matcher.match(it["title"])
        pub, src, prec, art_sha = "", it["time_source"], it["time_precision"], ""
        if it["time_wib"] is not None:
            pub = to_wib_iso(it["time_wib"])
        elif aid in times:
            pub, src, prec, art_sha = times[aid]["published_at_wib"], times[aid]["time_source"], "second", times[aid]["raw_sha256"]
        rows[aid] = {"article_id": aid, "source": it["source"], "index": it["index"], "channel": it["channel"], "url": it["url"],
                     "title": it["title"], "published_at_wib": pub, "time_source": src if pub else "", "time_precision": prec if pub else "",
                     "index_date": it["index_date"], "index_page": it["page"], "topics_matched": "|".join(topics),
                     "keywords_matched": "|".join(kws), "wilayah_pemasok": "|".join(regions.match(it["title"])),
                     "is_relevant": str(bool(topics)).lower(),
                     "raw_index_sha256": it["raw_index_sha256"], "raw_article_sha256": art_sha}
    PROCESSED.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows.values(), key=lambda r: (r["source"], r["index_date"], r["index"], r["index_page"]))
    with gzip.open(PROCESSED / "articles_all.csv.gz", "wt", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(ordered)
    rel_rows = [r for r in ordered if r["is_relevant"] == "true"]
    with (PROCESSED / "articles_relevant.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS); w.writeheader(); w.writerows(rel_rows)
    counts = defaultdict(lambda: [0, 0, 0])
    for r in ordered:
        c = counts[(r["source"], r["index_date"])]
        c[0] += 1
        if r["is_relevant"] == "true":
            c[1] += 1; c[2] += bool(r["published_at_wib"])
    with (PROCESSED / "daily_counts.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["source", "index_date", "n_articles", "n_relevant", "n_relevant_with_time"])
        for (s, d), c in sorted(counts.items()):
            w.writerow([s, d, *c])
    per = {}
    for s in cfg["sources"]:
        sr = [r for r in ordered if r["source"] == s]
        rr = [r for r in sr if r["is_relevant"] == "true"]
        per[s] = {"articles": len(sr), "relevant": len(rr), "relevant_with_time": sum(1 for r in rr if r["published_at_wib"]),
                  "relevant_time_precision": {p: sum(1 for r in rr if r["time_precision"] == p) for p in ("second", "minute", "date", "")},
                  "relevant_with_wilayah_pemasok": sum(1 for r in rr if r["wilayah_pemasok"]),
                  "duplicates_across_pages_days": dup[s]}
        print(f"[INFO] {s:14s} artikel={per[s]['articles']:>8,} relevan={per[s]['relevant']:>6,} relevan+waktu={per[s]['relevant_with_time']:>6,} duplikat={dup[s]}")
    verdict = "PASS" if not problems else "FAIL"
    save_json(REPORTS / "normalize_check.json", {"step": "Normalisasi News", "verdict": verdict, "per_source": per,
              "files": {"relevant": rel(PROCESSED / "articles_relevant.csv"), "daily_counts": rel(PROCESSED / "daily_counts.csv"),
                        "all_local": rel(PROCESSED / "articles_all.csv.gz")}, "problems": problems[:200], "checked_at_utc": now_utc()})
    for p in problems[:20]:
        print(f"[FAIL] {p}")
    print("HASIL:", verdict, "| laporan: reports/normalize_check.json")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
