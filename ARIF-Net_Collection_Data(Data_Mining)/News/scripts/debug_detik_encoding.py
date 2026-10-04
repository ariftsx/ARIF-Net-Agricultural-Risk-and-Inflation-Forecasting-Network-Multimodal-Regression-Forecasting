"""
ARIF-Net — Phase 1 News — debug detikNews pagination: header Accept-Encoding (read-only, 6 request, jeda 3 detik).
Hipotesis smoke-2: CDN Detik melayani varian ter-kompresi (gzip/br) halaman 1 untuk semua `page`,
sedangkan permintaan tanpa kompresi (seperti curl) mendapat halaman yang benar.
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
URL = "https://news.detik.com/indeks?date=01%2F02%2F2019&page={p}"


def main() -> int:
    res, sets = {}, {}
    for enc in ("default", "identity"):
        for p in (1, 2, 3):
            h = {"User-Agent": UA}
            if enc == "identity":
                h["Accept-Encoding"] = "identity"
            r = requests.get(URL.format(p=p), headers=h, timeout=40)
            sets[(enc, p)] = {i["url"] for i in parse_detik(r.content)}
            res[f"{enc}_p{p}"] = {"status": r.status_code, "n": len(sets[(enc, p)]), "content_encoding": r.headers.get("Content-Encoding"),
                                  "cache": r.headers.get("X-Cache") or r.headers.get("CF-Cache-Status") or r.headers.get("Age")}
            print(enc, p, res[f"{enc}_p{p}"])
            time.sleep(3)
        for a, b in ((1, 2), (2, 3), (1, 3)):
            res[f"{enc}_overlap_p{a}_p{b}"] = len(sets[(enc, a)] & sets[(enc, b)])
            print(f"{enc}: overlap p{a}&p{b} = {res[f'{enc}_overlap_p{a}_p{b}']}")
    (ROOT / "reports" / "debug_detik_encoding.json").write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
