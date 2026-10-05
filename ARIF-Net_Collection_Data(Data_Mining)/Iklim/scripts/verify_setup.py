"""
ARIF-Net — Phase 1 Climate — Langkah 1: verifikasi setup (offline).

Memeriksa environment, struktur folder, panjang path Windows, dan kesesuaian config
dengan keputusan P1-DG-09…17 (Plan v2.0.0 §0.5; Contract v2.1.0 §0B, §4.6, §5.6).
Nilai yang dikunci keputusan ditulis di sini secara eksplisit sehingga perubahan
config yang menyimpang terdeteksi.

Tidak melakukan request internet; hanya menulis reports/setup_check.json.

Pemakaian (dari folder Iklim):
    conda run -n arif-net python scripts\\verify_setup.py
"""
from __future__ import annotations

import importlib
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    ROOT, SETS, WIN_MAX_PATH, load_configs, load_state, longest_pipeline_path, now_utc, save_json, year_chunks,
)

LOCKED_CORE = [
    "precipitation_sum", "precipitation_hours", "temperature_2m_mean", "temperature_2m_max",
    "temperature_2m_min", "relative_humidity_2m_mean", "sunshine_duration",
    "et0_fao_evapotranspiration", "soil_moisture_7_to_28cm_mean",
]
LOCKED_RESERVE = [
    "relative_humidity_2m_max", "relative_humidity_2m_min", "vapour_pressure_deficit_max",
    "shortwave_radiation_sum", "cloud_cover_mean", "wind_speed_10m_max", "wind_speed_10m_mean",
    "soil_moisture_0_to_7cm_mean", "soil_moisture_28_to_100cm_mean", "soil_temperature_0_to_7cm_mean", "rain_sum",
]
LOCKED_LOCATIONS = [
    "garut", "cianjur", "bandung_barat", "bandung", "sumedang", "magelang", "brebes", "cirebon", "indramayu",
    "karawang", "subang", "demak", "temanggung", "nganjuk", "bima", "sragen", "cilacap", "sukoharjo",
]
COMMODITIES = {"cabai_merah_keriting", "bawang_merah_ukuran_sedang", "beras_kualitas_medium_i"}
LOCKED_SETTINGS = {
    "endpoint": "https://archive-api.open-meteo.com/v1/archive",
    "model_primary": "era5_seamless", "model_fallback": "era5",
    "temperature_unit": "celsius", "wind_speed_unit": "ms", "precipitation_unit": "mm",
    "timeformat": "iso8601", "timezone": "Asia/Jakarta", "expected_utc_offset_seconds": 25200,
    "cell_selection": "land", "start_date": "2018-01-01", "end_date": "2026-09-30",
    "release_lag_days_for_features": 5, "imputation_at_collection": False,
}
REQUIRED_PACKAGES = ["requests", "pandas", "numpy", "geopandas", "shapely", "pyproj", "pyogrio"]
REQUIRED_DIRS = [
    "config", "scripts", "docs", "logs", "reports", "tests",
    "data/raw/openmeteo/core", "data/raw/openmeteo/reserve", "data/raw/openmeteo/smoke",
    "data/processed/openmeteo", "data/external/boundaries",
]
REQUIRED_FILES = [
    "README.md", "environment.yml", "requirements.txt",
    "config/locations.json", "config/variables.json", "config/request_settings.json",
    "docs/PHASE1_COLLECTION_OPENMETEO.md",
]


class Report:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, check: str, ok: bool, detail: str = "", level: str = "FAIL") -> None:
        status = "PASS" if ok else level
        self.items.append({"check": check, "status": status, "detail": detail})
        print(f"[{status}] {check}" + (f" — {detail}" if detail else ""))

    def count(self, status: str) -> int:
        return sum(1 for i in self.items if i["status"] == status)


def long_paths_enabled() -> bool | None:
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\FileSystem") as k:
            return bool(winreg.QueryValueEx(k, "LongPathsEnabled")[0])
    except Exception:
        return None


def main() -> int:
    print("=" * 72)
    print("ARIF-Net | Phase 1 Climate | Langkah 1 — Verifikasi setup")
    print("=" * 72)
    rep = Report()

    # --- environment
    rep.add("Python 3.13.x", sys.version_info[:2] == (3, 13), sys.version.split()[0])
    env = Path(sys.prefix).name
    rep.add("Conda env 'arif-net'", env.lower() == "arif-net", f"sys.prefix = {sys.prefix}", level="WARN")
    for pkg in REQUIRED_PACKAGES:
        try:
            mod = importlib.import_module(pkg)
            rep.add(f"import {pkg}", True, getattr(mod, "__version__", "?"))
        except Exception as exc:  # noqa: BLE001
            rep.add(f"import {pkg}", False, f"{type(exc).__name__}: {exc}")

    # --- struktur
    for d in REQUIRED_DIRS:
        rep.add(f"folder {d}/", (ROOT / d).is_dir())
    for f in REQUIRED_FILES:
        rep.add(f"file {f}", (ROOT / f).is_file())

    # --- config
    locs, varcfg, settings = load_configs()
    ids = [l["location_id"] for l in locs["locations"]]
    rep.add("lokasi = 18 lokasi Contract §4.6 (P1-DG-11)", ids == LOCKED_LOCATIONS, f"{len(ids)} lokasi")
    rep.add("semua lokasi = Kabupaten", all(l["kabupaten"].startswith("Kabupaten ") for l in locs["locations"]))
    tiers_ok = all(set(l["commodity_tiers"]) <= COMMODITIES and set(l["commodity_tiers"].values()) <= {1, 2}
                   for l in locs["locations"])
    rep.add("tier hanya 1/2 untuk 3 komoditas (P1-DG-04/11)", tiers_ok)
    for c in sorted(COMMODITIES):
        t1 = [l["location_id"] for l in locs["locations"] if l["commodity_tiers"].get(c) == 1]
        rep.add(f"{c}: ada lokasi Tier 1", bool(t1), ", ".join(t1))
    n_coord = sum(1 for l in locs["locations"] if l["latitude"] is not None and l["longitude"] is not None)
    rep.add("koordinat centroid terisi (Langkah 2)", n_coord == len(ids), f"{n_coord}/{len(ids)}", level="WARN")

    core, reserve = (
        [v["api_param"] for v in varcfg["core"]],
        [v["api_param"] for v in varcfg["reserve"]],
    )
    rep.add("variabel core = 9 variabel P1-DG-14", core == LOCKED_CORE, f"{len(core)}")
    rep.add("variabel reserve = 11 variabel P1-DG-14", reserve == LOCKED_RESERVE, f"{len(reserve)}")
    rep.add("core ∩ reserve kosong", not set(core) & set(reserve))
    rep.add("tidak ada hourly di config", "hourly" not in settings and "hourly" not in varcfg)

    for key, val in LOCKED_SETTINGS.items():
        rep.add(f"setting {key} = {val!r}", settings.get(key) == val, f"terdeteksi {settings.get(key)!r}")
    rep.add("model bukan best_match", "best_match" not in (settings["model_primary"], settings["model_fallback"]))
    rl = settings.get("rate_limit", {})
    rep.add("rate limit ≤ kuota free tier (600/m, 5000/j, 10000/h)",
            0 < rl.get("per_minute", 0) <= 600 and 0 < rl.get("per_hour", 0) <= 5000 and 0 < rl.get("per_day", 0) <= 10000,
            str({k: v for k, v in rl.items() if not k.startswith("_")}))

    # --- path Windows
    start, end = date.fromisoformat(settings["start_date"]), date.fromisoformat(settings["end_date"])
    years = [s.year for s, _ in year_chunks(start, end)]
    longest = longest_pipeline_path(ids, years)
    n = len(str(longest))
    lpe = long_paths_enabled()
    rep.add(f"path terpanjang pipeline ≤ {WIN_MAX_PATH} karakter (MAX_PATH Windows)", n <= WIN_MAX_PATH,
            f"{n} karakter: {longest.relative_to(ROOT)} | LongPathsEnabled={lpe}")

    # --- status smoke (informasi)
    state = load_state()
    for s in SETS:
        sm = state.get("smoke", {}).get(s, {})
        rep.add(f"smoke test {s} PASS (Langkah {'3' if s == 'core' else '4'})", sm.get("verdict") == "PASS",
                f"model={sm.get('model')}" if sm else "belum dijalankan", level="WARN")

    verdict = "PASS" if rep.count("FAIL") == 0 else "FAIL"
    save_json(ROOT / "reports" / "setup_check.json", {
        "step": "Langkah 1 — setup", "verdict": verdict, "failed": rep.count("FAIL"), "warnings": rep.count("WARN"),
        "python": sys.version.split()[0], "sys_prefix": sys.prefix, "checked_at_utc": now_utc(), "items": rep.items,
    })
    print("=" * 72)
    print(f"HASIL: {verdict} | FAIL={rep.count('FAIL')} WARN={rep.count('WARN')} | laporan: reports/setup_check.json")
    print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
