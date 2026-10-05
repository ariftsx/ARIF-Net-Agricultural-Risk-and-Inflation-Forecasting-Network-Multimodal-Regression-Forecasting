"""
ARIF-Net — Phase 1 News — Langkah 0c: probe sitemap indeks portal (read-only, 1 request per portal).

Mengecek apakah sitemap indeks memuat arsip berbasis tanggal yang menjangkau 2019 (jalur historis
yang sah bila halaman search di-Disallow robots.txt). Halaman indeks Antara/Tempo dicek karena
robots.txt mereka tidak mencantumkan sitemap. Tidak mengambil artikel.

Pemakaian (dari folder News):
    conda run -n arif-net python scripts\\probe_sitemaps.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "news" / "probe" / "sitemaps"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
TARGETS = [
    ("kompas", "https://www.kompas.com/sitemap.xml"), ("detik", "https://www.detik.com/sitemap.xml"),
    ("cnnindonesia", "https://www.cnnindonesia.com/sitemap.xml"), ("cnbcindonesia", "https://www.cnbcindonesia.com/sitemap.xml"),
    ("kontan", "https://www.kontan.co.id/sitemap.xml"), ("bisnis", "https://www.bisnis.com/sitemap.xml"),
    ("liputan6", "https://www.liputan6.com/sitemap.xml"), ("republika", "https://republika.co.id/files/xml/sitemap.xml"),
    ("katadata", "https://www.katadata.co.id/sitemap-index.xml"), ("okezone", "https://www.okezone.com/sitemap.xml"),
    ("antaranews_indeks", "https://www.antaranews.com/indeks/2019-01-02"), ("tempo_indeks", "https://www.tempo.co/indeks/2019-01-02"),
]


def main() -> int:
    s = requests.Session(); s.headers["User-Agent"] = UA
    out = []
    for key, url in TARGETS:
        try:
            r = s.get(url, timeout=40, allow_redirects=True)
            status, content, final = r.status_code, r.content, r.url
        except requests.RequestException as exc:
            status, content, final = "EXC", str(exc).encode(), url
        RAW.mkdir(parents=True, exist_ok=True)
        ext = "xml" if url.endswith(".xml") else "html"
        (RAW / f"{key}.{ext}").write_bytes(content)
        text = content.decode("utf-8", "replace")
        locs = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", text)
        years = sorted({int(y) for y in re.findall(r"(20[0-2]\d)", " ".join(locs) if locs else text) if 2010 <= int(y) <= 2026})
        article_links_2019 = len(re.findall(r"2019", text)) if ext == "html" else None
        entry = {"source": key, "url": url, "final_url": final, "http_status": status, "bytes": len(content),
                 "sha256": hashlib.sha256(content).hexdigest(), "n_loc": len(locs), "loc_sample": locs[:6],
                 "years_mentioned": years, "mentions_2019_in_html": article_links_2019}
        out.append(entry)
        print(f"[{status}] {key:18s} loc={len(locs):5d} tahun={years[:3]}…{years[-3:] if years else ''} contoh={locs[:2]}")
        time.sleep(3)
    rep = {"step": "Langkah 0c — probe sitemap/indeks portal", "probed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "results": out, "note": "Hanya indeks; tidak ada artikel diambil."}
    (ROOT / "reports" / "probe_sitemaps.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("laporan: reports/probe_sitemaps.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
