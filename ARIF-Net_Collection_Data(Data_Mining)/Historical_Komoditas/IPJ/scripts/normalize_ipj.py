"""
ARIF-Net — Phase 1 IPJ — Langkah 4: normalisasi HANYA 3 komoditas terpetakan → CSV long.

Untuk setiap bulan (entri manifest OK/OK_EMPTY terbaru) sha256 raw diverifikasi, lalu recaps harian
komoditas terpetakan ditulis:

  data/processed/ipj/ipj_kramatjati_long.csv
  kolom: date, commodity_target, comcat_id, ipj_commodity_id, ipj_commodity_name, market_id, market_name,
         price_rp, raw_value, is_reported, price_level, source, raw_file

Nilai 0/kosong → price kosong + is_reported=false. Hanya tanggal yang dikembalikan sumber yang ditulis.
Duplikat tanggal bernilai IDENTIK (entri ganda sumber) → disimpan 1 baris & dicatat (keputusan peneliti 2026-10-03).
Tanpa imputasi/ffill/kalibrasi (pengisian null target = tahap P1-DG-06).

Pemakaian: conda run -n arif-net python scripts\\normalize_ipj.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANIFEST, PROCESSED, REPORTS, ROOT, load_configs, now_utc, parse_value, rel, report_rows, save_json, sha256_file  # noqa: E402

COLUMNS = ["date", "commodity_target", "comcat_id", "ipj_commodity_id", "ipj_commodity_name", "market_id", "market_name",
           "price_rp", "raw_value", "is_reported", "price_level", "source", "raw_file"]
SOURCE = "Info Pangan Jakarta (IPJ), Pemprov DKI Jakarta"


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 IPJ | Langkah 4 — Normalisasi"); print("=" * 72)
    comm, st = load_configs()
    man = pd.read_csv(MANIFEST, dtype=str, keep_default_na=False)
    ok = man[(man["http_status"] == "200") & man["check"].isin(["OK", "OK_EMPTY"])].sort_values("collected_at_utc") \
        .drop_duplicates("chunk", keep="last").sort_values("chunk")
    problems: list[str] = []
    dup_dropped: list[str] = []
    PROCESSED.mkdir(parents=True, exist_ok=True)
    out = PROCESSED / "ipj_kramatjati_long.csv"
    n = n_rep = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        for _, r in ok.iterrows():
            p = ROOT / r["raw_file"]
            if not p.exists() or sha256_file(p) != r["raw_sha256"]:
                problems.append(f"raw hilang/berubah: {r['raw_file']}"); continue
            rows = {x["commodity_id"]: x for x in report_rows(json.loads(p.read_bytes()))}
            for m in comm["commodities"]:
                seen: dict[str, object] = {}
                for rc in sorted(rows[m["ipj_commodity_id"]].get("recaps") or [], key=lambda x: x["time"]):
                    price = parse_value(rc.get("value"))
                    if rc["time"] in seen:  # duplikat identik (diterima di collector) → simpan 1 baris
                        if seen[rc["time"]] != price:
                            problems.append(f"{m['comcat_id']} {rc['time']}: duplikat nilai berbeda di {r['raw_file']}")
                        dup_dropped.append(f"{m['comcat_id']}:{rc['time']}")
                        continue
                    seen[rc["time"]] = price
                    w.writerow([rc["time"], m["target"], m["comcat_id"], m["ipj_commodity_id"], rows[m["ipj_commodity_id"]]["commodity_name"],
                                st["market_id"], st["market_name"], "" if price is None else int(price) if price.is_integer() else price,
                                rc.get("value"), str(price is not None).lower(), "eceran", SOURCE, r["raw_file"]])
                    n += 1; n_rep += price is not None
    df = pd.read_csv(out, usecols=["date", "comcat_id"])
    dup = int(df.duplicated().sum())
    if dup:
        problems.append(f"{dup} duplikat (date, comcat_id)")
    per = df.groupby("comcat_id")["date"].agg(["count", "min", "max"]).to_dict("index") if n else {}
    verdict = "PASS" if not problems else "FAIL"
    save_json(REPORTS / "normalize_check.json", {
        "step": "Langkah 4 — normalisasi IPJ", "verdict": verdict, "file": rel(out), "rows": n, "reported": n_rep,
        "not_reported": n - n_rep, "months": int(len(ok)), "duplicates": dup,
        "identical_duplicates_dropped": dup_dropped, "per_commodity": per,
        "problems": problems, "checked_at_utc": now_utc()})
    for cid, v in per.items():
        print(f"[INFO] {cid:6s} baris={v['count']:,} rentang={v['min']}→{v['max']}")
    print(f"[{verdict}] total baris={n:,} dilaporkan={n_rep:,} kosong/0={n - n_rep} duplikat={dup}")
    for pr in problems:
        print(f"[FAIL] {pr}")
    print("HASIL:", verdict, "| laporan: reports/normalize_check.json")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
