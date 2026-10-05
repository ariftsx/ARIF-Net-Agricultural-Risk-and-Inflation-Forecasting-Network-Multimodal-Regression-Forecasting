"""
ARIF-Net — Phase 1 PIBC — Langkah 5a: normalisasi HANYA kolom yang dipetakan ke Beras Kualitas Medium I.

Menolak berjalan bila config/varieties.json → medium_i_mapping masih null (keputusan peneliti, P1-DG-05).
Raw (14 varietas) tetap utuh sebagai evidence; output processed hanya kolom terpetakan.

Output: data/processed/pibc/pibc_medium_i_long.csv
  date, source, market, price_level, variety_field, variety_label, mapped_to, price_rp, raw_value,
  is_reported, unit_note, raw_file
Tanpa imputasi/ffill/kalibrasi. Kalibrasi & pengisian null target = tahap P1-DG-06 (terpisah, split-aware).

Pemakaian: conda run -n arif-net python scripts\\normalize_pibc.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANIFEST, PROCESSED, REPORTS, ROOT, load_configs, now_utc, parse_price, parse_tgl, rel, save_json, sha256_file  # noqa: E402

COLUMNS = ["date", "source", "market", "price_level", "variety_field", "variety_label", "mapped_to", "price_rp",
           "raw_value", "is_reported", "unit_note", "raw_file"]
MAPPED_TO = "Beras Kualitas Medium I (PIHPS com_3)"


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 PIBC | Langkah 5a — Normalisasi (kolom terpetakan)"); print("=" * 72)
    var, st = load_configs()
    mapping = var.get("medium_i_mapping")
    fields = mapping if isinstance(mapping, list) else ([mapping] if mapping else [])
    labels = {v["field"]: v["label"] for v in var["varieties"]}
    if not fields or any(f not in labels for f in fields):
        print(f"[FAIL] medium_i_mapping belum diputuskan/tidak valid: {mapping!r}. Isi setelah keputusan peneliti (P1-DG-05).")
        return 1
    man = pd.read_csv(MANIFEST, dtype=str, keep_default_na=False)
    ok = man[(man["http_status"] == "200") & (man["check"] == "OK")].sort_values("collected_at_utc") \
        .drop_duplicates("chunk", keep="last").sort_values("chunk")
    problems: list[str] = []
    PROCESSED.mkdir(parents=True, exist_ok=True)
    out = PROCESSED / "pibc_medium_i_long.csv"
    n = n_rep = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        for _, r in ok.iterrows():
            p = ROOT / r["raw_file"]
            if not p.exists() or sha256_file(p) != r["raw_sha256"]:
                problems.append(f"raw hilang/berubah: {r['raw_file']}"); continue
            for row in json.loads(p.read_bytes())["data"]:
                d = parse_tgl(row["tgl"])
                for f in fields:
                    price = parse_price(row[f])
                    w.writerow([d.isoformat(), "PIBC — PT Food Station Tjipinang Jaya", "Pasar Induk Beras Cipinang", "grosir",
                                f, labels[f], MAPPED_TO, "" if price is None else int(price) if price.is_integer() else price,
                                row[f], str(price is not None).lower(), st["_meta"]["unit_note"], r["raw_file"]])
                    n += 1; n_rep += price is not None
    df = pd.read_csv(out, usecols=["date", "variety_field"])
    dup = int(df.duplicated().sum())
    if dup:
        problems.append(f"{dup} duplikat (date, variety_field)")
    verdict = "PASS" if not problems else "FAIL"
    save_json(REPORTS / "normalize_check.json", {
        "step": "Langkah 5a — normalisasi PIBC", "verdict": verdict, "mapping": fields, "mapped_to": MAPPED_TO,
        "decided_at": var["_meta"].get("medium_i_mapping_decided_at"), "file": rel(out), "rows": n, "reported": n_rep,
        "empty": n - n_rep, "date_min": str(df["date"].min()), "date_max": str(df["date"].max()), "duplicates": dup,
        "problems": problems, "checked_at_utc": now_utc()})
    print(f"[{verdict}] kolom={fields} baris={n:,} dilaporkan={n_rep:,} kosong={n - n_rep} duplikat={dup} "
          f"rentang={df['date'].min()}→{df['date'].max()}")
    for pr in problems:
        print(f"[FAIL] {pr}")
    print("HASIL:", verdict, "| laporan: reports/normalize_check.json")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
