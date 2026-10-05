"""
ARIF-Net — Phase 1 Climate — Langkah 2a: unduh batas administrasi GADM 4.1 (Indonesia, level 2).

Sumber   : https://gadm.org (versi 4.1), file resmi
           https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_IDN_2.json.zip
Lisensi  : GADM — bebas untuk penggunaan akademik/non-komersial; redistribusi tidak diizinkan.
           → file TIDAK di-commit (lihat .gitignore); provenance (URL + sha256) dicatat.

Output   : data/external/boundaries/gadm41_IDN_2.json(.zip)
           reports/boundaries_check.json

Pemakaian: conda run -n arif-net python scripts\\fetch_boundaries.py
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import BOUNDARIES, REPORTS, now_utc, rel, save_json, sha256_file  # noqa: E402

URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_IDN_2.json.zip"
ZIP_PATH = BOUNDARIES / "gadm41_IDN_2.json.zip"
JSON_NAME = "gadm41_IDN_2.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="Unduh GADM 4.1 IDN level 2 (Langkah 2a).")
    ap.add_argument("--redownload", action="store_true", help="Unduh ulang walau zip sudah ada.")
    args = ap.parse_args()

    print("=" * 72); print("ARIF-Net | Phase 1 Climate | Langkah 2a — Batas administrasi GADM 4.1"); print("=" * 72)
    BOUNDARIES.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists() and not args.redownload:
        print(f"[INFO] zip sudah ada, tidak diunduh ulang: {rel(ZIP_PATH)}")
        http_status, downloaded_at = None, None
    else:
        print(f"[INFO] mengunduh {URL}")
        r = requests.get(URL, timeout=180)
        http_status, downloaded_at = r.status_code, now_utc()
        if r.status_code != 200 or not r.content.startswith(b"PK"):
            print(f"[FAIL] HTTP {r.status_code}; konten bukan zip ({len(r.content)} bytes)")
            return 1
        tmp = ZIP_PATH.with_suffix(".part")
        tmp.write_bytes(r.content)
        tmp.replace(ZIP_PATH)

    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = zf.namelist()
        if JSON_NAME not in names:
            print(f"[FAIL] {JSON_NAME} tidak ada di zip. Isi: {names}")
            return 1
        zf.extract(JSON_NAME, BOUNDARIES)
    json_path = BOUNDARIES / JSON_NAME

    check = {
        "step": "Langkah 2a — batas administrasi", "verdict": "PASS",
        "source": "GADM 4.1, Indonesia, level 2 (kabupaten/kota)", "source_url": URL,
        "license": "GADM: academic & non-commercial use; redistribution not allowed (gadm.org/license.html)",
        "zip_file": rel(ZIP_PATH), "zip_sha256": sha256_file(ZIP_PATH), "zip_bytes": ZIP_PATH.stat().st_size,
        "json_file": rel(json_path), "json_sha256": sha256_file(json_path), "json_bytes": json_path.stat().st_size,
        "http_status": http_status, "downloaded_at_utc": downloaded_at, "checked_at_utc": now_utc(),
    }
    save_json(REPORTS / "boundaries_check.json", check)
    print(f"[PASS] {rel(json_path)} | {check['json_bytes']:,} bytes | sha256 {check['json_sha256'][:16]}…")
    print("HASIL: PASS | laporan: reports/boundaries_check.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
