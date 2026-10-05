"""
ARIF-Net — Phase 1 News — verifikasi pola URL Kompas (read-only, 4 request, jeda 3 detik).

Menggabungkan tangkapan peneliti (2026-10-03: pagination `indeks.kompas.com/?page=2`,
`article:published_time` dalam UTC) dengan probe 0d (`?site=all&date=YYYY-MM-DD`) untuk memastikan:
  1. indeks per tanggal halaman 1 & halaman 2 (date + page) mengembalikan artikel tanggal itu, dan berbeda;
  2. filter kanal Money (`site=money`) per tanggal;
  3. meta waktu terbit artikel 2019 (format & zona waktu).
Respons disimpan byte-identik di data/raw/news/probe/kompas/. Tidak ada koleksi.

Pemakaian (dari folder News):
    conda run -n arif-net python scripts\\verify_kompas.py
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
RAW = ROOT / "data" / "raw" / "news" / "probe" / "kompas"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
DATE = "2019-01-02"
LINK = re.compile(r"https?://([a-z]+)\.kompas\.com/read/2019/01/02/(\d+)/[a-z0-9\-]+")
PAGES = [("all_p1", f"https://indeks.kompas.com/?site=all&date={DATE}"),
         ("all_p2", f"https://indeks.kompas.com/?site=all&date={DATE}&page=2"),
         ("money_p1", f"https://indeks.kompas.com/?site=money&date={DATE}")]


def get(s: requests.Session, name: str, url: str) -> tuple[int | str, str]:
    try:
        r = s.get(url, timeout=40); status, content = r.status_code, r.content
    except requests.RequestException as exc:
        status, content = "EXC", str(exc).encode()
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / f"{name}.html").write_bytes(content)
    time.sleep(3)
    return status, content.decode("utf-8", "replace")


def main() -> int:
    s = requests.Session(); s.headers["User-Agent"] = UA
    out, links_by_page = {}, {}
    for name, url in PAGES:
        status, html = get(s, name, url)
        links = sorted({m.group(0) for m in LINK.finditer(html)})
        subs = sorted({m.group(1) for m in LINK.finditer(html)})
        pages = sorted({int(p) for p in re.findall(r"[?&]page=(\d+)", html)})
        links_by_page[name] = set(links)
        out[name] = {"url": url, "http_status": status, "article_links_2019_01_02": len(links), "subdomains": subs,
                     "pagination_numbers_seen": pages[:20], "max_page_seen": max(pages) if pages else None, "sample": links[:2]}
        print(f"[{status}] {name:9s} artikel={len(links):3d} kanal={subs} halaman={pages[:12]}")
    out["p1_p2_overlap"] = len(links_by_page["all_p1"] & links_by_page["all_p2"])
    money_ok = all("money" == l.split("//")[1].split(".")[0] for l in links_by_page["money_p1"]) if links_by_page["money_p1"] else None
    out["money_filter_only_money_links"] = money_ok
    print(f"overlap p1∩p2 = {out['p1_p2_overlap']} | filter money hanya money.kompas.com = {money_ok}")

    art = next(iter(sorted(links_by_page["money_p1"] or links_by_page["all_p1"])), None)
    if art:
        status, html = get(s, "article_2019", art)
        meta = re.findall(r'<meta[^>]+(?:article:published_time|datePublished|pubdate)[^>]*>', html)[:3]
        ld = re.findall(r'"datePublished"\s*:\s*"([^"]+)"', html)[:2]
        url_time = re.search(r"/read/(\d{4})/(\d{2})/(\d{2})/(\d{2})(\d{2})", art)
        out["article"] = {"url": art, "http_status": status, "meta_published": meta, "jsonld_datePublished": ld,
                          "url_date_time_wib": "-".join(url_time.groups()[:3]) + f" {url_time.group(4)}:{url_time.group(5)}" if url_time else None}
        print(f"[{status}] artikel {art}\n   meta={meta}\n   json-ld={ld}\n   waktu dari URL (WIB)={out['article']['url_date_time_wib']}")
    rep = {"step": "Verifikasi pola URL Kompas", "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "researcher_capture": {"pagination": "https://indeks.kompas.com/?page=2",
                                  "article_meta": '<meta property="article:published_time" content="2026-10-02T23:10:00+00:00" />',
                                  "article_url": "https://money.kompas.com/read/2026/10/03/061000026/..."},
           "results": out}
    (ROOT / "reports" / "verify_kompas.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("laporan: reports/verify_kompas.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
