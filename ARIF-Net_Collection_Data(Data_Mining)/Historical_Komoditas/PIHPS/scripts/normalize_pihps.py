"""
ARIF-Net — Phase 1 PIHPS — Langkah 4: normalisasi raw JSON → CSV long.

Untuk setiap (comcat_id, bulan) diambil entri manifest SUKSES terbaru, sha256 raw
diverifikasi, lalu row Pasar Kramatjati L3 diubah dari kolom tanggal (wide) ke long:

  data/processed/pihps/pihps_kramatjati_long.csv
  kolom: date, commodity, comcat_id, market, market_level, price_rp_per_kg, raw_value,
         is_reported, source, price_type_id, province_id, regency_id, regency_label_source, raw_file

'-' dari sumber → price kosong + is_reported=false. Tidak ada imputasi/ffill (P1-DG-06).
Hanya tanggal yang dikembalikan sumber yang ditulis (tanggal yang tidak dikembalikan
dilaporkan di audit, bukan ditambahkan).

Pemakaian: conda run -n arif-net python scripts\\normalize_pihps.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    MANIFEST, PROCESSED, REPORTS, ROOT, date_items, load_configs, market_rows, now_utc, parse_price, rel,
    save_json, sha256_file,
)

COLUMNS = ["date", "commodity", "comcat_id", "market", "market_level", "price_rp_per_kg", "raw_value", "is_reported",
           "source", "price_type_id", "province_id", "regency_id", "regency_label_source", "raw_file"]
SOURCE = "PIHPS Bank Indonesia (harga eceran, pasar tradisional)"


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 PIHPS | Langkah 4 — Normalisasi"); print("=" * 72)
    if not MANIFEST.exists():
        print("[FAIL] collection_manifest.csv tidak ada. Jalankan Langkah 3."); return 1
    comm, st = load_configs()
    order = {c["comcat_id"]: i for i, c in enumerate(comm["commodities"])}
    man = pd.read_csv(MANIFEST, dtype=str, keep_default_na=False)
    ok = man[(man["http_status"] == "200") & (man["check"] == "OK")]
    ok = ok.sort_values("collected_at_utc").drop_duplicates(["comcat_id", "chunk"], keep="last")
    ok = ok.assign(_o=ok["comcat_id"].map(order)).sort_values(["_o", "chunk"])

    problems: list[str] = []
    PROCESSED.mkdir(parents=True, exist_ok=True)
    out = PROCESSED / "pihps_kramatjati_long.csv"
    n_rows = n_rep = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        for _, r in ok.iterrows():
            path = ROOT / r["raw_file"]
            if not path.exists():
                problems.append(f"file hilang: {r['raw_file']}"); continue
            if sha256_file(path) != r["raw_sha256"]:
                problems.append(f"sha256 tidak cocok (raw berubah?): {r['raw_file']}"); continue
            rows = market_rows(json.loads(path.read_bytes()), st["market_name"], st["market_level"])
            if len(rows) != 1:
                problems.append(f"row market ≠ 1 di {r['raw_file']}"); continue
            for d, raw in date_items(rows[0]):
                price = parse_price(raw)
                w.writerow([d.isoformat(), r["commodity"], r["comcat_id"], rows[0]["name"], rows[0]["level"],
                            "" if price is None else int(price) if price.is_integer() else price, raw,
                            str(price is not None).lower(), SOURCE, st["price_type_id"], st["province_id"],
                            st["regency_id"], st["regency_label_source"], r["raw_file"]])
                n_rows += 1
                n_rep += price is not None

    df = pd.read_csv(out, usecols=["date", "comcat_id"])
    dup = int(df.duplicated().sum())
    if dup:
        problems.append(f"{dup} baris duplikat (date, comcat_id)")
    per = df.groupby("comcat_id")["date"].agg(["count", "min", "max"]).to_dict("index")
    verdict = "PASS" if not problems else "FAIL"
    save_json(REPORTS / "normalize_check.json", {
        "step": "Langkah 4 — normalisasi PIHPS", "verdict": verdict, "file": rel(out), "rows": n_rows,
        "reported": n_rep, "not_reported_dash": n_rows - n_rep, "chunks": int(len(ok)), "duplicates": dup,
        "per_commodity": per, "problems": problems, "checked_at_utc": now_utc()})
    for cid, v in per.items():
        print(f"[INFO] {cid:6s} baris={v['count']:,} rentang={v['min']}→{v['max']}")
    print(f"[{'PASS' if not dup else 'FAIL'}] total baris={n_rows:,} dilaporkan={n_rep:,} '-'={n_rows - n_rep:,} duplikat={dup}")
    for p in problems:
        print(f"[FAIL] {p}")
    print("=" * 72); print(f"HASIL: {verdict} | laporan: reports/normalize_check.json"); print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
