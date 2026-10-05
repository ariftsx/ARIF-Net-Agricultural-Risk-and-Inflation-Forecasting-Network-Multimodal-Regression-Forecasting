"""
ARIF-Net — Phase 1 Climate — Langkah 6: normalisasi raw JSON → CSV long.

Untuk setiap (set, lokasi, tahun) diambil entri manifest SUKSES terbaru (HTTP 200, check OK),
sha256 file raw diverifikasi, lalu nilai harian ditulis ke format long:

  data/processed/openmeteo/climate_core_long.csv
  data/processed/openmeteo/climate_reserve_long.csv
  kolom: date, location_id, variable, value, unit, set, model,
         grid_latitude, grid_longitude, grid_elevation, raw_file

Tidak ada imputasi, agregasi, lag, atau pembulatan. Null tetap kosong.
Jika sha256 tidak cocok → raw berubah → FAIL (jangan "perbaiki" raw).

Pemakaian: conda run -n arif-net python scripts\\normalize_openmeteo.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    MANIFEST, PROCESSED, REPORTS, ROOT, SETS, daily_series, daily_unit, load_configs, load_state, now_utc, rel,
    save_json, sha256_file, variables_for,
)

COLUMNS = ["date", "location_id", "variable", "value", "unit", "set", "model",
           "grid_latitude", "grid_longitude", "grid_elevation", "raw_file"]


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 Climate | Langkah 6 — Normalisasi"); print("=" * 72)
    if not MANIFEST.exists():
        print("[FAIL] collection_manifest.csv tidak ada. Jalankan Langkah 5 dulu."); return 1
    locs, varcfg, _ = load_configs()
    model_in_use = load_state().get("model_in_use")
    man = pd.read_csv(MANIFEST, dtype=str, keep_default_na=False)
    ok = man[(man["http_status"] == "200") & (man["check"] == "OK")]
    ok = ok.sort_values("collected_at_utc").drop_duplicates(["set", "location_id", "year"], keep="last")
    loc_order = {l["location_id"]: i for i, l in enumerate(locs["locations"])}
    ok = ok.assign(_o=ok["location_id"].map(loc_order), _y=ok["year"].astype(int)).sort_values(["set", "_o", "_y"])

    problems: list[str] = []
    models = sorted(ok["model"].unique())
    if models != [model_in_use]:
        problems.append(f"model di manifest {models} ≠ model_in_use '{model_in_use}'")
    summary = {}
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for which in SETS:
        sub = ok[ok["set"] == which]
        variables = variables_for(varcfg, which)
        out = PROCESSED / f"climate_{which}_long.csv"
        n_rows = n_null = 0
        with out.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(COLUMNS)
            for _, r in sub.iterrows():
                path = ROOT / r["raw_file"]
                if not path.exists():
                    problems.append(f"file hilang: {r['raw_file']}"); continue
                if sha256_file(path) != r["raw_sha256"]:
                    problems.append(f"sha256 tidak cocok (raw berubah?): {r['raw_file']}"); continue
                payload = json.loads(path.read_bytes())
                times = payload["daily"]["time"]
                grid = (payload.get("latitude"), payload.get("longitude"), payload.get("elevation"))
                for v in variables:
                    series = daily_series(payload, v)
                    if series is None:
                        problems.append(f"variabel {v} tidak ada di {r['raw_file']}"); continue
                    unit = daily_unit(payload, v)
                    for t, val in zip(times, series):
                        w.writerow([t, r["location_id"], v, "" if val is None else val, unit, which, r["model"], *grid, r["raw_file"]])
                        n_rows += 1
                        n_null += val is None
        df = pd.read_csv(out, usecols=["date", "location_id", "variable"])
        dup = int(df.duplicated().sum())
        if dup:
            problems.append(f"{which}: {dup} baris duplikat (date, location_id, variable)")
        summary[which] = {"file": rel(out), "rows": n_rows, "null_values": n_null, "chunks": int(len(sub)),
                          "locations": int(sub["location_id"].nunique()), "variables": len(variables),
                          "date_min": str(df["date"].min()) if n_rows else None, "date_max": str(df["date"].max()) if n_rows else None,
                          "duplicates": dup}
        print(f"[{'PASS' if not dup else 'FAIL'}] {which:8s} rows={n_rows:,} null={n_null:,} chunks={len(sub)} "
              f"lokasi={sub['location_id'].nunique()} duplikat={dup}")

    verdict = "PASS" if not problems else "FAIL"
    save_json(REPORTS / "normalize_check.json", {"step": "Langkah 6 — normalisasi", "verdict": verdict, "model": model_in_use,
                                                  "sets": summary, "problems": problems, "checked_at_utc": now_utc()})
    for p in problems:
        print(f"[FAIL] {p}")
    print("=" * 72); print(f"HASIL: {verdict} | laporan: reports/normalize_check.json"); print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
