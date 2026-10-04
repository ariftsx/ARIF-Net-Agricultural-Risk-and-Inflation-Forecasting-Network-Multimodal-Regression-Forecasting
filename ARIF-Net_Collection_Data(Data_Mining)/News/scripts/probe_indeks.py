"""
ARIF-Net — Phase 1 News — Langkah 0d: probe halaman indeks/arsip per tanggal (read-only, 1 request per portal).

Mengecek apakah halaman indeks berita untuk tanggal 2019-01-02 dapat diakses dan memuat tautan artikel
tanggal tersebut — bukti bahwa arsip historis tersedia tanpa memakai halaman search (yang di-Disallow
beberapa robots.txt). Pola URL indeks adalah pola publik portal; WAJIB dikonfirmasi peneliti via DevTools
sebelum dipakai untuk koleksi. Tidak mengambil isi artikel.

Pemakaian (dari folder News):
    conda run -n arif-net python scripts\\probe_indeks.py
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
RAW = ROOT / "data" / "raw" / "news" / "probe" / "indeks"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
# (sumber, url indeks 2019-01-02, pola tautan artikel bertanggal 2019-01-02)
TARGETS = [
    ("kompas", "https://indeks.kompas.com/?site=all&date=2019-01-02", r"[a-z]+\.kompas\.com/read/2019/01/02/\d+"),
    ("detik", "https://news.detik.com/indeks?date=01/02/2019", r"detik\.com/[^\"']*?/d-\d+"),
    ("cnnindonesia", "https://www.cnnindonesia.com/indeks?date=2019/01/02", r"cnnindonesia\.com/[a-z\-]+/20190102\d+"),
    ("cnbcindonesia", "https://www.cnbcindonesia.com/indeks?date=2019/01/02", r"cnbcindonesia\.com/[a-z\-]+/20190102\d+"),
    ("antaranews", "https://www.antaranews.com/indeks/terkini/2019-01-02", r"antaranews\.com/berita/\d+/"),
    ("kontan", "https://www.kontan.co.id/search/indeks?kanal=&tanggal=2&bulan=01&tahun=2019", r"kontan\.co\.id/news/[a-z0-9\-]+"),
]


def main() -> int:
    s = requests.Session(); s.headers["User-Agent"] = UA
    out = []
    for key, url, pat in TARGETS:
        try:
            r = s.get(url, timeout=40, allow_redirects=True)
            status, content, final = r.status_code, r.content, r.url
        except requests.RequestException as exc:
            status, content, final = "EXC", str(exc).encode(), url
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / f"{key}_2019-01-02.html").write_bytes(content)
        text = content.decode("utf-8", "replace")
        links = sorted(set(re.findall(pat, text)))
        entry = {"source": key, "url": url, "final_url": final, "http_status": status, "bytes": len(content),
                 "sha256": hashlib.sha256(content).hexdigest(), "article_links_found": len(links), "link_sample": links[:3]}
        out.append(entry)
        print(f"[{status}] {key:14s} tautan artikel={len(links):3d} final={final[:80]} contoh={links[:1]}")
        time.sleep(3)
    rep = {"step": "Langkah 0d — probe indeks arsip per tanggal (2019-01-02)",
           "probed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "results": out,
           "note": "Hanya halaman indeks; pola URL wajib dikonfirmasi peneliti via DevTools sebelum koleksi."}
    (ROOT / "reports" / "probe_indeks.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("laporan: reports/probe_indeks.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
