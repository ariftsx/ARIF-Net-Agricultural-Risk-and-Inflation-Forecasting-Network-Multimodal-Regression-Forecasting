"""
ARIF-Net — Phase 1 News — verifikasi pola URL indeks dari tangkapan peneliti (read-only).

Untuk tiap media (pola dari tangkapan peneliti 2026-10-03, tanggal uji 2019-01-02):
  p1 = indeks satu tanggal · p2 = halaman ke-2 · ch = indeks kanal ekonomi · art = 1 artikel dari p1/ch
Dicek: HTTP status (akses dari script, bukan browser), jumlah tautan artikel, overlap p1∩p2,
dan sumber waktu terbit artikel (meta article:published_time, JSON-LD datePublished, field lain).
Respons disimpan byte-identik di data/raw/news/probe/media/<media>/. Tidak ada koleksi.

Pemakaian (dari folder News):
    conda run -n arif-net python scripts\\verify_media.py
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "news" / "probe" / "media"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
D = "2019-01-02"
MEDIA = {
    "detik": {"p1": "https://news.detik.com/indeks?date=01/02/2019", "p2": "https://news.detik.com/indeks?page=2&date=01/02/2019",
              "ch": "https://finance.detik.com/indeks?date=01/02/2019", "link": r"https://[a-z]+\.detik\.com/[a-z0-9\-/]+/d-\d+/[a-z0-9\-]+"},
    "cnbcindonesia": {"p1": "https://www.cnbcindonesia.com/indeks?date=2019/01/02&tipe=", "p2": "https://www.cnbcindonesia.com/indeks?date=2019/01/02&page=2",
                      "ch": "https://www.cnbcindonesia.com/mymoney/indeks/71?date=2019/01/02&tipe=", "link": r"https://www\.cnbcindonesia\.com/[a-z\-]+/\d{14}-\d+-\d+/[a-z0-9\-]+"},
    "cnnindonesia": {"p1": "https://www.cnnindonesia.com/indeks/?date=2019/01/02", "p2": "https://www.cnnindonesia.com/indeks/2?date=2019/01/02&page=2",
                     "ch": "https://www.cnnindonesia.com/ekonomi/indeks/5?date=2019/01/02", "link": r"https://www\.cnnindonesia\.com/[a-z\-]+/\d{14}-\d+-\d+/[a-z0-9\-]+"},
    "kontan": {"p1": "https://www.kontan.co.id/search/indeks?kanal=&tanggal=2&bulan=01&tahun=2019", "p2": "https://www.kontan.co.id/search/indeks?kanal=&tanggal=2&bulan=01&tahun=2019&per_page=20",
               "ch": None, "link": r"https://[a-z]+\.kontan\.co\.id/news/[a-z0-9\-]+"},
    "liputan6": {"p1": "https://www.liputan6.com/indeks/2019/01/02?start=2019-01-02&end=2019-01-03", "p2": "https://www.liputan6.com/indeks/2019/01/02?end=2019-01-03&start=2019-01-02&page=2",
                 "ch": "https://www.liputan6.com/bisnis/indeks/2019/01/02", "link": r"https://www\.liputan6\.com/[a-z\-]+/read/\d+/[a-z0-9\-]+"},
    "tempo": {"p1": "https://www.tempo.co/indeks?page=1&start_date=2019-01-02&end_date=2019-01-02", "p2": "https://www.tempo.co/indeks?page=2&start_date=2019-01-02&end_date=2019-01-02",
              "ch": "https://www.tempo.co/indeks?page=1&rubric_slug=ekonomi&start_date=2019-01-02&end_date=2019-01-02", "link": r"https://www\.tempo\.co/[a-z\-]+/[a-z0-9\-]+-\d{5,}"},
    "bisnis": {"p1": "https://www.bisnis.com/index?categoryId=0&type=indeks&date=2019-01-02", "p2": None,
               "ch": "https://www.bisnis.com/index?categoryId=43&date=2019-01-02&type=indeks", "link": r"https://[a-z]+\.bisnis\.com/read/\d{8}/\d+/\d+/[a-z0-9\-]+"},
    "katadata": {"p1": "https://katadata.co.id/indeks/search/-/02-01-2019/02-01-2019", "p2": None,
                 "ch": "https://katadata.co.id/indeks/search/4/02-01-2019/02-01-2019", "link": r"https://katadata\.co\.id/[a-z\-]+/[a-z\-]+/[0-9a-f]{13}/[a-z0-9\-]+"},
}
TIME_PATTERNS = {"meta_published_time": r'<meta[^>]+article:published_time[^>]+content="([^"]*)"',
                 "jsonld_datePublished": r'"datePublished"\s*:\s*"([^"]*)"',
                 "content_published_date": r'"content_published_date"\s*:\s*"([^"]*)"',
                 "meta_pubdate": r'<meta[^>]+name="(?:pubdate|publishdate)"[^>]+content="([^"]*)"'}


def fetch(s, media, name, url):
    try:
        r = s.get(url, timeout=40); status, content, final = r.status_code, r.content, r.url
    except requests.RequestException as exc:
        status, content, final = "EXC", str(exc).encode(), url
    p = RAW / media; p.mkdir(parents=True, exist_ok=True)
    (p / f"{name}.html").write_bytes(content)
    time.sleep(3)
    return status, content.decode("utf-8", "replace"), final


def main() -> int:
    s = requests.Session(); s.headers["User-Agent"] = UA
    out = {}
    for media, cfg in MEDIA.items():
        res, links = {}, {}
        for part in ("p1", "p2", "ch"):
            if not cfg.get(part):
                res[part] = None; continue
            status, html, final = fetch(s, media, part, cfg[part])
            found = sorted(set(re.findall(cfg["link"], html)))
            links[part] = set(found)
            res[part] = {"url": cfg[part], "final_url": final, "http_status": status, "article_links": len(found), "sample": found[:2]}
        res["overlap_p1_p2"] = len(links.get("p1", set()) & links.get("p2", set())) if cfg.get("p2") else None
        cand = sorted(links.get("ch") or links.get("p1") or [])
        if cand:
            status, html, final = fetch(s, media, "article", cand[0])
            res["article"] = {"url": cand[0], "http_status": status,
                              **{k: re.findall(v, html)[:2] for k, v in TIME_PATTERNS.items()}}
        out[media] = res
        a = res.get("article") or {}
        times = {k: v for k, v in a.items() if k in TIME_PATTERNS and v}
        print(f"{media:14s} p1={_s(res['p1'])} p2={_s(res['p2'])} overlap={res['overlap_p1_p2']} ch={_s(res['ch'])} | waktu={times}")
    (ROOT / "reports" / "verify_media.json").write_text(json.dumps(
        {"step": "Verifikasi pola URL tangkapan peneliti", "test_date": D,
         "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "results": out},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("laporan: reports/verify_media.json")
    return 0


def _s(r):
    return "-" if r is None else f"{r['http_status']}/{r['article_links']}"


if __name__ == "__main__":
    sys.exit(main())
