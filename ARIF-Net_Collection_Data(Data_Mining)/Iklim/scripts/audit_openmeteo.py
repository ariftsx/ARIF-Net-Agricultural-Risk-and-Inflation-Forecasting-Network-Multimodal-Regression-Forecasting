"""
ARIF-Net — Phase 1 Climate — Langkah 7: audit deskriptif data iklim (TIDAK mengubah data).

  1. Kelengkapan tanggal per lokasi × variabel (start → end, harian).
  2. Null: jumlah, null di ekor periode (wajar: jeda ERA5 ±5 hari) vs null di tengah periode.
  3. Range fisik: hujan/ET0 ≥ 0, RH & awan 0–100, soil moisture 0–1, sunshine 0–86400 s,
     precipitation_hours 0–24, suhu −5…45 °C; konsistensi Tmin ≤ Tmean ≤ Tmax.
  4. Grid collision: lokasi berbeda yang jatuh di grid cell identik (keterbatasan, bukan untuk diperbaiki).
  5. Elevasi grid & jarak titik diminta ↔ pusat grid.
  6. QC reserve: rain_sum vs precipitation_sum.
  7. Konsistensi metadata manifest: model tunggal, utc_offset 25200, timezone Asia/Jakarta.

Output: reports/audit_climate_summary.json + reports/audit_<set>_completeness.csv + reports/audit_grid.csv

Pemakaian: conda run -n arif-net python scripts\\audit_openmeteo.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANIFEST, PROCESSED, REPORTS, SETS, load_configs, load_state, now_utc, save_json  # noqa: E402

RANGES = {
    "precipitation_sum": (0, None), "rain_sum": (0, None), "et0_fao_evapotranspiration": (0, None),
    "precipitation_hours": (0, 24), "sunshine_duration": (0, 86400),
    "relative_humidity_2m_mean": (0, 100), "relative_humidity_2m_max": (0, 100), "relative_humidity_2m_min": (0, 100),
    "cloud_cover_mean": (0, 100), "soil_moisture_7_to_28cm_mean": (0, 1), "soil_moisture_0_to_7cm_mean": (0, 1),
    "soil_moisture_28_to_100cm_mean": (0, 1), "wind_speed_10m_max": (0, None), "wind_speed_10m_mean": (0, None),
    "shortwave_radiation_sum": (0, None), "vapour_pressure_deficit_max": (0, None),
    "temperature_2m_mean": (-5, 45), "temperature_2m_max": (-5, 45), "temperature_2m_min": (-5, 45),
    "soil_temperature_0_to_7cm_mean": (-5, 60),
}


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(a))


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 Climate | Langkah 7 — Audit"); print("=" * 72)
    locs, _, settings = load_configs()
    state = load_state()
    expected_days = pd.date_range(settings["start_date"], settings["end_date"], freq="D")
    fails, findings = [], {}
    frames = {}

    for which in SETS:
        path = PROCESSED / f"climate_{which}_long.csv"
        if not path.exists():
            fails.append(f"{path.name} tidak ada (Langkah 6)"); continue
        df = pd.read_csv(path, parse_dates=["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        frames[which] = df

        # 1 + 2 kelengkapan & null
        rows = []
        for (lid, var), g in df.sort_values("date").groupby(["location_id", "variable"], sort=False):
            vals = g["value"].tolist()
            tail = 0
            for x in reversed(vals):
                if pd.isna(x): tail += 1
                else: break
            n_null = int(g["value"].isna().sum())
            nulls = g.loc[g["value"].isna(), "date"]
            rows.append({"set": which, "location_id": lid, "variable": var, "n_days": len(g),
                         "missing_dates": len(expected_days.difference(pd.DatetimeIndex(g["date"]))),
                         "duplicate_dates": int(g["date"].duplicated().sum()),
                         "n_null": n_null, "tail_nulls": tail, "non_tail_nulls": n_null - tail,
                         "first_null": nulls.min().date().isoformat() if n_null else None,
                         "min": g["value"].min(), "max": g["value"].max(), "mean": round(g["value"].mean(), 4)})
        comp = pd.DataFrame(rows)
        comp.to_csv(REPORTS / f"audit_{which}_completeness.csv", index=False)
        n_missing, n_dup = int(comp["missing_dates"].sum()), int(comp["duplicate_dates"].sum())
        n_mid, max_tail = int(comp["non_tail_nulls"].sum()), int(comp["tail_nulls"].max())
        n_series = len(comp)
        exp_series = len(locs["locations"]) * df["variable"].nunique()
        if n_missing or n_dup or n_series != exp_series:
            fails.append(f"{which}: tanggal hilang={n_missing}, duplikat={n_dup}, seri={n_series}/{exp_series}")
        print(f"[{'PASS' if not (n_missing or n_dup) else 'FAIL'}] {which}: kelengkapan tanggal (hilang={n_missing}, duplikat={n_dup}, seri={n_series}/{exp_series})")
        print(f"[{'PASS' if not n_mid else 'WARN'}] {which}: null di tengah periode={n_mid} | null di ekor maks={max_tail} hari")
        findings[which] = {"series": n_series, "missing_dates": n_missing, "duplicate_dates": n_dup,
                           "non_tail_nulls": n_mid, "max_tail_nulls_days": max_tail,
                           "series_with_mid_nulls": comp.loc[comp["non_tail_nulls"] > 0, ["location_id", "variable", "non_tail_nulls", "first_null"]]
                           .astype(str).values.tolist(),
                           "completeness_file": f"reports/audit_{which}_completeness.csv"}

        # 3 range fisik
        viol = []
        for var, (lo, hi) in RANGES.items():
            s = df[(df["variable"] == var) & df["value"].notna()]
            bad = s[(s["value"] < lo) | ((s["value"] > hi) if hi is not None else False)]
            if len(bad):
                viol.append({"variable": var, "n": int(len(bad)),
                             "examples": bad.head(3)[["date", "location_id", "value"]].astype(str).values.tolist()})
        if which == "core":
            wide = df.pivot_table(index=["date", "location_id"], columns="variable", values="value")
            bad_t = wide[(wide["temperature_2m_min"] > wide["temperature_2m_mean"] + 1e-6)
                         | (wide["temperature_2m_mean"] > wide["temperature_2m_max"] + 1e-6)]
            if len(bad_t):
                viol.append({"variable": "Tmin<=Tmean<=Tmax", "n": int(len(bad_t)),
                             "examples": [list(map(str, i)) for i in bad_t.index[:3]]})
        findings[which]["range_violations"] = viol
        print(f"[{'PASS' if not viol else 'WARN'}] {which}: pelanggaran range fisik = {sum(v['n'] for v in viol)}")

    # 4 + 5 grid (dari core; reserve memakai titik & model yang sama)
    if "core" in frames:
        grid = frames["core"].groupby("location_id")[["grid_latitude", "grid_longitude", "grid_elevation"]].agg(["first", "nunique"])
        g = pd.DataFrame({"location_id": grid.index,
                          "grid_latitude": grid[("grid_latitude", "first")].values,
                          "grid_longitude": grid[("grid_longitude", "first")].values,
                          "grid_elevation": grid[("grid_elevation", "first")].values,
                          "grid_variants": grid[[("grid_latitude", "nunique"), ("grid_longitude", "nunique")]].max(axis=1).values})
        pts = {l["location_id"]: (l["latitude"], l["longitude"]) for l in locs["locations"]}
        g["requested_lat"] = g["location_id"].map(lambda i: pts[i][0])
        g["requested_lon"] = g["location_id"].map(lambda i: pts[i][1])
        g["offset_km"] = [round(haversine_km(a, b, c, d), 2) for a, b, c, d in
                          zip(g["requested_lat"], g["requested_lon"], g["grid_latitude"], g["grid_longitude"])]
        g.to_csv(REPORTS / "audit_grid.csv", index=False)
        coll = g[g.duplicated(["grid_latitude", "grid_longitude"], keep=False)]
        groups = coll.groupby(["grid_latitude", "grid_longitude"])["location_id"].apply(list).tolist()
        findings["grid"] = {"file": "reports/audit_grid.csv", "collisions": groups,
                            "locations_with_multiple_grid_cells": g.loc[g["grid_variants"] > 1, "location_id"].tolist(),
                            "max_offset_km": float(g["offset_km"].max())}
        print(f"[{'PASS' if not groups else 'WARN'}] grid collision = {groups or 'tidak ada'} | offset maks titik→grid = {g['offset_km'].max()} km")

    # 6 QC rain vs precipitation
    if {"core", "reserve"} <= set(frames):
        p = frames["core"].query("variable == 'precipitation_sum'")[["date", "location_id", "value"]].rename(columns={"value": "p"})
        r = frames["reserve"].query("variable == 'rain_sum'")[["date", "location_id", "value"]].rename(columns={"value": "r"})
        m = p.merge(r, on=["date", "location_id"])
        d = (m["p"] - m["r"]).abs()
        findings["qc_rain_vs_precip"] = {"n_pairs": int(len(m)), "max_abs_diff_mm": float(d.max()),
                                         "share_diff_gt_0_1mm": round(float((d > 0.1).mean()), 6)}
        print(f"[INFO] QC rain_sum vs precipitation_sum: {findings['qc_rain_vs_precip']}")

    # 7 metadata manifest
    if MANIFEST.exists():
        man = pd.read_csv(MANIFEST, dtype=str, keep_default_na=False)
        ok = man[(man["http_status"] == "200") & (man["check"] == "OK")]
        meta = {"models": sorted(ok["model"].unique()), "utc_offsets": sorted(ok["utc_offset_seconds"].unique()),
                "timezones": sorted(ok["timezone"].unique()), "model_in_use": state.get("model_in_use"),
                "model_fallback_reason": state.get("model_fallback_reason")}
        meta_ok = meta["models"] == [state.get("model_in_use")] and meta["utc_offsets"] == ["25200"] and meta["timezones"] == ["Asia/Jakarta"]
        if not meta_ok:
            fails.append(f"metadata manifest tidak konsisten: {meta}")
        findings["manifest_meta"] = meta
        print(f"[{'PASS' if meta_ok else 'FAIL'}] metadata: model={meta['models']} utc_offset={meta['utc_offsets']} tz={meta['timezones']}")

    verdict = "PASS" if not fails else "FAIL"
    save_json(REPORTS / "audit_climate_summary.json", {
        "step": "Langkah 7 — audit", "verdict": verdict, "fails": fails, "findings": findings,
        "period": [settings["start_date"], settings["end_date"]], "data_nature": "reanalysis (Open-Meteo), bukan observasi stasiun",
        "note": "Audit deskriptif. Tidak ada data yang diubah. WARN dilaporkan ke peneliti, bukan diperbaiki otomatis.",
        "checked_at_utc": now_utc()})
    print("=" * 72); print(f"HASIL: {verdict} | laporan: reports/audit_climate_summary.json"); print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
