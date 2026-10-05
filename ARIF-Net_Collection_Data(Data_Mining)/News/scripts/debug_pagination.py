"""
ARIF-Net — Phase 1 News — debug pagination detikNews & CNN Indonesia (read-only, ±9 request, jeda 3 detik).
Temuan smoke: detikNews p1==p2 dalam satu sesi; CNN `/indeks/1?…&page=1` → 404.
Raw disimpan di data/raw/news/probe/debug/. Hasil → reports/debug_pagination.json.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT  # noqa: E402
from parsers import parse_cnnindonesia, parse_detik  # noqa: E402

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"
OUT = ROOT / "data" / "raw" / "news" / "probe" / "debug"
TESTS = [
    ("detik_nosess_p1", "detik", "https://news.detik.com/indeks?page=1&date=01%2F02%2F2019"),
    ("detik_nosess_p2", "detik", "https://news.detik.com/indeks?page=2&date=01%2F02%2F2019"),
    ("detik_nosess_p3", "detik", "https://news.detik.com/indeks?page=3&date=01%2F02%2F2019"),
    ("detik_nopage", "detik", "https://news.detik.com/indeks?date=01%2F02%2F2019"),
    ("cnn_root_nopage", "cnn", "https://www.cnnindonesia.com/indeks/?date=2019/01/02"),
    ("cnn_2_p1", "cnn", "https://www.cnnindonesia.com/indeks/2?date=2019/01/02&page=1"),
    ("cnn_2_p2", "cnn", "https://www.cnnindonesia.com/indeks/2?date=2019/01/02&page=2"),
    ("cnn_2_p3", "cnn", "https://www.cnnindonesia.com/indeks/2?date=2019/01/02&page=3"),
    ("cnn_root_p3", "cnn", "https://www.cnnindonesia.com/indeks/?date=2019/01/02&page=3"),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    res, sets = {}, {}
    for name, kind, url in TESTS:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=40)   # TANPA sesi (cookie tidak dibawa)
        (OUT / f"{name}.html").write_bytes(r.content)
        items = (parse_detik if kind == "detik" else parse_cnnindonesia)(r.content) if r.status_code == 200 else []
        sets[name] = {i["url"] for i in items}
        res[name] = {"url": url, "final_url": r.url, "status": r.status_code, "n": len(items), "set_cookie": list(r.cookies.keys())}
        print(f"[{r.status_code}] {name:16s} n={len(items):2d} final={r.url[-55:]}")
        time.sleep(3)
    pairs = [("detik_nosess_p1", "detik_nosess_p2"), ("detik_nosess_p2", "detik_nosess_p3"), ("detik_nopage", "detik_nosess_p1"),
             ("cnn_root_nopage", "cnn_2_p1"), ("cnn_2_p1", "cnn_2_p2"), ("cnn_2_p2", "cnn_2_p3"), ("cnn_root_nopage", "cnn_root_p3")]
    for a, b in pairs:
        res[f"overlap {a}&{b}"] = len(sets[a] & sets[b])
        print(f"overlap {a:16s} & {b:16s} = {len(sets[a] & sets[b])}")
    (ROOT / "reports" / "debug_pagination.json").write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
