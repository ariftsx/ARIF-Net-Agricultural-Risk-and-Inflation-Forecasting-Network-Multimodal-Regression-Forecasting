"""
ARIF-Net — Phase 1 News — debug detikNews: cache-buster (read-only, 9 request, jeda 3 detik).
Temuan: hasil page=N detikNews tidak konsisten antar-percobaan (cache CDN basi). Uji parameter
`_=<epoch ms>` (diabaikan server, memaksa CDN mengambil versi segar) pada 3 ulangan × 3 halaman.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT  # noqa: E402
from parsers import parse_detik  # noqa: E402

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"


def main() -> int:
    res, ok_rounds = {}, 0
    for rnd in range(3):
        sets = {}
        for p in (1, 2, 3):
            url = f"https://news.detik.com/indeks?date=01%2F02%2F2019&page={p}&_={int(time.time() * 1000)}"
            r = requests.get(url, headers={"User-Agent": UA}, timeout=40)
            sets[p] = {i["url"] for i in parse_detik(r.content)}
            time.sleep(3)
        ov = {"p1p2": len(sets[1] & sets[2]), "p2p3": len(sets[2] & sets[3]), "p1p3": len(sets[1] & sets[3]),
              "n": [len(sets[p]) for p in (1, 2, 3)]}
        distinct = ov["p1p2"] == ov["p2p3"] == ov["p1p3"] == 0 and min(ov["n"]) > 0
        ok_rounds += distinct
        res[f"round{rnd + 1}"] = {**ov, "all_distinct": distinct}
        print(f"ulangan {rnd + 1}: {ov} → halaman berbeda semua: {distinct}")
    res["rounds_all_distinct"] = f"{ok_rounds}/3"
    (ROOT / "reports" / "debug_detik_cachebust.json").write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
