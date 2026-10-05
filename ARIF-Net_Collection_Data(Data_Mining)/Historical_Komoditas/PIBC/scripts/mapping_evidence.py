"""
ARIF-Net — Phase 1 PIBC — Langkah 4: bukti pendukung pemetaan Beras Kualitas Medium I → kolom PIBC.

TIDAK memilih pemetaan (keputusan peneliti, P1-DG-05). Hanya menyajikan statistik deskriptif
setiap varietas PIBC non-ketan terhadap PIHPS Pasar Kramatjati com_3 (Beras Kualitas Medium I).

Jendela evidence DIBATASI 2019-01-01 → 2020-12-31 (periode paling awal, pasti di dalam data training
kronologis) agar pemilihan taxonomy tidak memakai informasi periode validasi/test (anti-leakage;
semangat P1-DG-06(4)).

Metrik per kandidat (tanggal yang sama-sama dilaporkan PIHPS & PIBC, hari kerja):
  n_pairs, mean harga PIBC, mean PIHPS, rasio PIHPS/PIBC (mean, CV), korelasi level,
  korelasi perubahan antar-tanggal-berpasangan, share arah perubahan sama (perubahan ≠ 0).

Output: reports/mapping_evidence.json, reports/mapping_evidence.csv
Pemakaian: conda run -n arif-net python scripts\\mapping_evidence.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANIFEST, PIHPS_LONG, REPORTS, ROOT, load_configs, now_utc, parse_price, parse_tgl, save_json, sha256_file  # noqa: E402

WINDOW = ("2019-01-01", "2020-12-31")


def load_pibc_wide() -> pd.DataFrame:
    man = pd.read_csv(MANIFEST, dtype=str, keep_default_na=False)
    ok = man[(man["http_status"] == "200") & (man["check"] == "OK")].sort_values("collected_at_utc") \
        .drop_duplicates("chunk", keep="last").sort_values("chunk")
    recs = []
    for _, r in ok.iterrows():
        p = ROOT / r["raw_file"]
        if sha256_file(p) != r["raw_sha256"]:
            raise SystemExit(f"[FAIL] sha256 tidak cocok: {r['raw_file']}")
        for row in json.loads(p.read_bytes())["data"]:
            recs.append({"date": pd.Timestamp(parse_tgl(row["tgl"])), **{k: parse_price(v) for k, v in row.items() if k != "tgl"}})
    return pd.DataFrame(recs).set_index("date").sort_index()


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 PIBC | Langkah 4 — Bukti pemetaan Beras Medium I"); print("=" * 72)
    var, _ = load_configs()
    if not PIHPS_LONG.exists():
        print(f"[FAIL] CSV PIHPS tidak ditemukan: {PIHPS_LONG}"); return 1
    pibc = load_pibc_wide().loc[WINDOW[0]:WINDOW[1]]
    ph = pd.read_csv(PIHPS_LONG, parse_dates=["date"])
    ph = ph[(ph["comcat_id"] == "com_3") & ph["is_reported"]].set_index("date")["price_rp_per_kg"].astype(float).loc[WINDOW[0]:WINDOW[1]]

    rows = []
    for v in var["varieties"]:
        if v["group"] != "non-ketan":
            continue
        j = pd.concat([ph.rename("pihps"), pibc[v["field"]].rename("pibc")], axis=1, join="inner").dropna()
        ratio = j["pihps"] / j["pibc"]
        dp, db = j["pihps"].diff().dropna(), j["pibc"].diff().dropna()
        nz = (dp != 0) & (db != 0)
        rows.append({
            "field": v["field"], "label": v["label"], "n_pairs": int(len(j)),
            "pibc_mean": round(float(j["pibc"].mean()), 1), "pihps_mean": round(float(j["pihps"].mean()), 1),
            "ratio_pihps_over_pibc_mean": round(float(ratio.mean()), 4),
            "ratio_cv_pct": round(float(100 * ratio.std() / ratio.mean()), 2),
            "corr_level": round(float(np.corrcoef(j["pihps"], j["pibc"])[0, 1]), 4),
            "corr_change": round(float(np.corrcoef(dp, db)[0, 1]), 4) if dp.std() > 0 and db.std() > 0 else None,
            "same_direction_share_pct": round(float(100 * (np.sign(dp[nz]) == np.sign(db[nz])).mean()), 1) if nz.any() else None,
            "n_nonzero_change_pairs": int(nz.sum()),
        })
    df = pd.DataFrame(rows)
    df.to_csv(REPORTS / "mapping_evidence.csv", index=False)
    save_json(REPORTS / "mapping_evidence.json", {
        "step": "Langkah 4 — bukti pemetaan (P1-DG-05)", "target": "PIHPS Pasar Kramatjati com_3 Beras Kualitas Medium I (eceran)",
        "window": list(WINDOW), "window_reason": "Periode paling awal; pasti di dalam training kronologis (anti-leakage).",
        "candidates": rows, "decision": "BELUM — pemetaan dipilih peneliti; laporan ini tidak memilih.",
        "caveat": "PIBC = grosir pasar induk, PIHPS = eceran pasar tradisional; rasio > 1 mencerminkan margin eceran. "
                  "Korelasi tinggi tidak membuktikan kesetaraan grade.", "generated_at_utc": now_utc()})
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        print(df.to_string(index=False))
    print("=" * 72); print("Laporan: reports/mapping_evidence.json / .csv — KEPUTUSAN pemetaan oleh peneliti."); print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
