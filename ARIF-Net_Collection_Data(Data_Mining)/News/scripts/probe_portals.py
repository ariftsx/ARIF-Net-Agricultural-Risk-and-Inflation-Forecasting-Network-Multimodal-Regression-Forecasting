"""
ARIF-Net — Phase 1 News — Langkah 0b: probe kelayakan portal berita Indonesia (read-only).

Untuk setiap kandidat sumber: ambil robots.txt (1 request) → catat aturan untuk User-agent '*',
Crawl-delay, dan daftar Sitemap. Sitemap berbasis tanggal = jalur arsip historis yang paling bersih.
Tidak mengambil artikel apa pun. Respons robots.txt disimpan byte-identik sebagai bukti.

Pemakaian (dari folder News):
    conda run -n arif-net python scripts\\probe_portals.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "news" / "probe" / "robots"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
CANDIDATES = [
    ("antaranews", "https://www.antaranews.com"), ("kompas", "https://www.kompas.com"),
    ("detik", "https://www.detik.com"), ("cnnindonesia", "https://www.cnnindonesia.com"),
    ("cnbcindonesia", "https://www.cnbcindonesia.com"), ("kontan", "https://www.kontan.co.id"),
    ("bisnis", "https://www.bisnis.com"), ("tempo", "https://www.tempo.co"),
    ("liputan6", "https://www.liputan6.com"), ("republika", "https://www.republika.co.id"),
    ("katadata", "https://katadata.co.id"), ("okezone", "https://www.okezone.com"),
    ("beritajakarta", "https://www.beritajakarta.id"), ("bapanas", "https://badanpangan.go.id"),
]


def parse_robots(text: str) -> dict:
    groups, cur, sitemaps = {}, None, []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = (x.strip() for x in line.split(":", 1))
        k = k.lower()
        if k == "user-agent":
            cur = v.lower(); groups.setdefault(cur, {"disallow": [], "allow": [], "crawl_delay": None})
        elif k == "sitemap":
            sitemaps.append(v)
        elif cur is not None and k in ("disallow", "allow"):
            groups[cur][k].append(v)
        elif cur is not None and k == "crawl-delay":
            groups[cur]["crawl_delay"] = v
    star = groups.get("*", {"disallow": [], "allow": [], "crawl_delay": None})
    return {"star_disallow": star["disallow"], "star_allow": star["allow"][:10], "crawl_delay": star["crawl_delay"],
            "blocks_all_for_star": "/" in star["disallow"], "sitemaps": sitemaps[:15], "n_sitemaps": len(sitemaps),
            "user_agents": sorted(groups)[:20]}


def main() -> int:
    s = requests.Session(); s.headers["User-Agent"] = UA
    out = []
    for key, base in CANDIDATES:
        try:
            r = s.get(base + "/robots.txt", timeout=30, allow_redirects=True)
            status, content, final = r.status_code, r.content, r.url
        except requests.RequestException as exc:
            status, content, final = "EXC", str(exc).encode(), base
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / f"{key}_robots.txt").write_bytes(content)
        text = content.decode("utf-8", "replace")
        info = parse_robots(text) if status == 200 and "<html" not in text[:200].lower() else {"note": "robots.txt tidak tersedia/HTML"}
        entry = {"source": key, "base": base, "final_url": final, "http_status": status,
                 "sha256": hashlib.sha256(content).hexdigest(), **info}
        out.append(entry)
        print(f"[{status}] {key:14s} disallow*={str(info.get('star_disallow', ''))[:90]:90s} sitemaps={info.get('n_sitemaps')}")
        time.sleep(3)
    rep = {"step": "Langkah 0b — probe robots.txt portal", "probed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "results": out, "note": "Hanya robots.txt; tidak ada artikel diambil. ToS tiap media tetap harus dibaca peneliti."}
    (ROOT / "reports" / "probe_portals.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("laporan: reports/probe_portals.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
