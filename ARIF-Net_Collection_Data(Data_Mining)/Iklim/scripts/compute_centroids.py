"""
ARIF-Net — Phase 1 Climate — Langkah 2b: centroid poligon kabupaten (P1-DG-12).

Metode:
  * Fitur dicocokkan berdasarkan nama kabupaten + provinsi; fitur bertipe Kota dikecualikan.
  * Geometri multipart digabung, centroid dihitung di CRS equal-area EPSG:6933,
    lalu dikonversi ke WGS84 (EPSG:4326), dibulatkan 5 desimal (~1 m).
  * Centroid di luar poligon → WARN + representative_point dilaporkan sebagai pembanding.
    Script TIDAK mengganti metode (perubahan = decision gate; keterbatasan ditulis di Limitations).

Output: config/locations.json (lat/lon + provenance; hanya bila PASS dan bukan --dry-run)
        reports/centroids_report.csv, reports/centroids_points.geojson, reports/centroids_check.json

Pemakaian:
    conda run -n arif-net python scripts\\compute_centroids.py --dry-run
    conda run -n arif-net python scripts\\compute_centroids.py
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import BOUNDARIES, CONFIG, REPORTS, load_json, now_utc, rel, save_json, sha256_file  # noqa: E402

EQUAL_AREA = "EPSG:6933"
WGS84 = "EPSG:4326"
DEFAULT_BOUNDARY = BOUNDARIES / "gadm41_IDN_2.json"
SOURCE_LABEL = "GADM 4.1 level 2"
# bbox kasar Jawa + NTB untuk sanity check
LAT_RANGE, LON_RANGE = (-9.5, -5.5), (105.0, 119.5)


def norm(text: object) -> str:
    s = str(text or "").lower().strip()
    s = re.sub(r"^(kabupaten|kab\.?)\s*", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def is_city(name: object, typ: object) -> bool:
    n, t = str(name or "").lower().strip(), str(typ or "").lower().strip()
    return n.startswith("kota") or t in {"kota", "city", "kotamadya", "municipality"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Centroid kabupaten → config/locations.json (P1-DG-12).")
    ap.add_argument("--boundary", type=Path, default=DEFAULT_BOUNDARY)
    ap.add_argument("--dry-run", action="store_true", help="Hitung & laporkan tanpa mengubah locations.json.")
    args = ap.parse_args()

    print("=" * 72); print("ARIF-Net | Phase 1 Climate | Langkah 2b — Centroid kabupaten (P1-DG-12)"); print("=" * 72)
    if not args.boundary.is_file():
        print(f"[FAIL] file batas tidak ada: {args.boundary} → jalankan scripts\\fetch_boundaries.py"); return 1

    gdf = gpd.read_file(args.boundary)
    if gdf.crs is None:
        print("[WARN] CRS tidak terdefinisi; diasumsikan WGS84."); gdf = gdf.set_crs(WGS84)
    for col in ("NAME_1", "NAME_2", "TYPE_2"):
        if col not in gdf.columns:
            print(f"[FAIL] kolom {col} tidak ada. Kolom: {list(gdf.columns)}"); return 1
    print(f"File batas : {args.boundary.name} | {len(gdf)} fitur | CRS {gdf.crs}")
    gdf["_n"], gdf["_p"] = gdf["NAME_2"].map(norm), gdf["NAME_1"].map(norm)
    gdf["_city"] = [is_city(n, t) for n, t in zip(gdf["NAME_2"], gdf["TYPE_2"])]

    loc_path = CONFIG / "locations.json"
    cfg = load_json(loc_path)
    rows, failures, outside, new = [], [], [], {}
    for loc in cfg["locations"]:
        lid = loc["location_id"]
        want_n, want_p = norm(loc["kabupaten"]), norm(loc["provinsi"])
        cand = gdf[(gdf["_n"] == want_n) & (gdf["_p"] == want_p) & (~gdf["_city"])]
        if len(cand) != 1:
            near = gdf[gdf["_n"].str.contains(want_n[:5], na=False)][["NAME_1", "NAME_2", "TYPE_2"]]
            failures.append(lid)
            print(f"[FAIL] {lid:14s} kecocokan = {len(cand)} (harus 1). Kandidat:\n{near.head(6).to_string(index=False)}")
            continue
        feat = cand.iloc[[0]]
        geom = feat.to_crs(EQUAL_AREA).geometry.union_all()
        c = gpd.GeoSeries([geom.centroid], crs=EQUAL_AREA).to_crs(WGS84).iloc[0]
        rp = gpd.GeoSeries([geom.representative_point()], crs=EQUAL_AREA).to_crs(WGS84).iloc[0]
        inside = bool(geom.contains(geom.centroid))
        lat, lon = round(float(c.y), 5), round(float(c.x), 5)
        in_bbox = LAT_RANGE[0] <= lat <= LAT_RANGE[1] and LON_RANGE[0] <= lon <= LON_RANGE[1]
        status = "FAIL" if not in_bbox else ("WARN" if not inside else "PASS")
        if status == "FAIL": failures.append(lid)
        if status == "WARN": outside.append(lid)
        area = round(geom.area / 1e6, 1)
        print(f"[{status}] {lid:14s} lat={lat:9.5f} lon={lon:10.5f} | {area:8.1f} km² | centroid di dalam poligon: {inside}")
        rows.append({
            "location_id": lid, "kabupaten": loc["kabupaten"], "provinsi": loc["provinsi"],
            "gadm_gid_2": feat["GID_2"].iloc[0] if "GID_2" in feat else None,
            "gadm_name_2": feat["NAME_2"].iloc[0], "gadm_name_1": feat["NAME_1"].iloc[0], "gadm_type_2": feat["TYPE_2"].iloc[0],
            "centroid_lat": lat, "centroid_lon": lon, "centroid_inside_polygon": inside,
            "representative_lat": round(float(rp.y), 5), "representative_lon": round(float(rp.x), 5),
            "area_km2": area, "status": status,
        })
        new[lid] = (lat, lon, f"{feat['NAME_2'].iloc[0]}, {feat['NAME_1'].iloc[0]} ({feat['TYPE_2'].iloc[0]}"
                              + (f", {feat['GID_2'].iloc[0]})" if "GID_2" in feat else ")"))

    REPORTS.mkdir(exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(REPORTS / "centroids_report.csv", index=False, encoding="utf-8")
    if rows:
        gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["centroid_lon"], df["centroid_lat"]), crs=WGS84) \
            .to_file(REPORTS / "centroids_points.geojson", driver="GeoJSON")

    bhash = sha256_file(args.boundary)
    verdict = "PASS" if not failures and len(rows) == len(cfg["locations"]) else "FAIL"
    check = {
        "step": "Langkah 2b — centroid", "verdict": verdict, "decision_ref": "P1-DG-12",
        "boundary_file": args.boundary.name, "boundary_source": SOURCE_LABEL, "boundary_sha256": bhash,
        "crs_centroid": EQUAL_AREA, "n_locations": len(cfg["locations"]), "n_matched": len(rows),
        "failed": failures, "centroid_outside_polygon": outside, "dry_run": args.dry_run, "checked_at_utc": now_utc(),
    }
    save_json(REPORTS / "centroids_check.json", check)

    if verdict == "PASS" and not args.dry_run:
        for loc in cfg["locations"]:
            lat, lon, feat_name = new[loc["location_id"]]
            loc["latitude"], loc["longitude"] = lat, lon
            loc["boundary_feature"] = feat_name
            loc["boundary_source"] = f"{SOURCE_LABEL} | {args.boundary.name} | sha256={bhash}"
        cfg["_meta"]["coordinates_filled_in"] = f"Langkah 2b — {check['checked_at_utc']}"
        save_json(loc_path, cfg)
        print(f"\n{rel(loc_path)} diperbarui.")

    print("=" * 72)
    print(f"HASIL: {verdict} | cocok {len(rows)}/{len(cfg['locations'])} | FAIL={len(failures)} | "
          f"centroid di luar poligon={len(outside)} | dry_run={args.dry_run}")
    if verdict == "FAIL":
        print("locations.json TIDAK diubah. Laporkan kandidat di atas ke peneliti — jangan memilih fitur manual.")
    print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
