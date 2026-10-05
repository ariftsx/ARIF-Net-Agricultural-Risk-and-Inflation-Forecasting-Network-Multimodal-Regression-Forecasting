"""
ARIF-Net — Phase 1 IPJ — Langkah 1: verifikasi setup (offline).

Nilai yang dikunci keputusan/analisis ditulis eksplisit di sini → config yang menyimpang = FAIL.

Pemakaian (dari folder Historical_Komoditas\\IPJ):
    conda run -n arif-net python scripts\\verify_setup.py
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PIHPS_LONG, ROOT, WIN_MAX_PATH, load_configs, load_state, longest_pipeline_path, now_utc, save_json  # noqa: E402

LOCKED_MAPPING = {  # keputusan peneliti 2026-10-03 (P1-DG-04/05/06)
    "com_14": (8, "Cabe Merah Keriting"),
    "com_11": (12, "Bawang Merah"),
    "com_3": (4, "Beras Muncul I"),
}
LOCKED_SETTINGS = {
    "base_url": "https://infopangan.jakarta.go.id/api2", "report_path": "/v1/public/report",
    "filter_by": "market", "market_id": 12, "market_name": "Pasar Kramat Jati",
    "start_month": "2019-01", "end_month": "2026-09", "imputation_at_collection": False,
}
REQUIRED_DIRS = ["config", "scripts", "tests", "docs", "logs", "reports", "data/raw/ipj/smoke",
                 "data/raw/ipj/reference", "data/processed/ipj"]
# environment.yml & requirements.txt dipakai bersama di Historical_Komoditas/ (satu tingkat di atas paket)
REQUIRED_FILES = ["README.md", "../environment.yml", "../requirements.txt", "config/commodities.json",
                  "config/request_settings.json", "docs/PHASE1_COLLECTION_IPJ.md"]


class Report:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, check: str, ok: bool, detail: str = "", level: str = "FAIL") -> None:
        status = "PASS" if ok else level
        self.items.append({"check": check, "status": status, "detail": detail})
        print(f"[{status}] {check}" + (f" — {detail}" if detail else ""))

    def count(self, status: str) -> int:
        return sum(1 for i in self.items if i["status"] == status)


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 IPJ | Langkah 1 — Verifikasi setup"); print("=" * 72)
    rep = Report()
    rep.add("Python 3.13.x", sys.version_info[:2] == (3, 13), sys.version.split()[0])
    rep.add("Conda env 'arif-net'", Path(sys.prefix).name.lower() == "arif-net", f"sys.prefix = {sys.prefix}", level="WARN")
    for pkg in ("requests", "pandas", "numpy"):
        try:
            rep.add(f"import {pkg}", True, getattr(importlib.import_module(pkg), "__version__", "?"))
        except Exception as exc:  # noqa: BLE001
            rep.add(f"import {pkg}", False, f"{type(exc).__name__}: {exc}")
    for d in REQUIRED_DIRS:
        rep.add(f"folder {d}/", (ROOT / d).is_dir())
    for f in REQUIRED_FILES:
        rep.add(f"file {f}", (ROOT / f).is_file())

    comm, st = load_configs()
    got = {c["comcat_id"]: (c["ipj_commodity_id"], c["ipj_commodity_name"]) for c in comm["commodities"]}
    rep.add("pemetaan IPJ → 3 komoditas primary (keputusan peneliti)", got == LOCKED_MAPPING, str(got))
    for key, val in LOCKED_SETTINGS.items():
        rep.add(f"setting {key} = {val!r}", st.get(key) == val, f"terdeteksi {st.get(key)!r}")
    rep.add("market_id bukan 1 (Pasar Induk / PIKJ, P1-DG-02)", st.get("market_id") != 1)
    rep.add("delay ≥ 1 detik", float(st.get("delay_seconds", 0)) >= 1.0, str(st.get("delay_seconds")))
    rep.add("CSV PIHPS tersedia (untuk audit perbandingan)", PIHPS_LONG.is_file(), PIHPS_LONG.name, level="WARN")
    longest = longest_pipeline_path()
    rep.add(f"path terpanjang pipeline ≤ {WIN_MAX_PATH} karakter", len(str(longest)) <= WIN_MAX_PATH,
            f"{len(str(longest))} karakter: {longest.relative_to(ROOT)}")
    rep.add("smoke test PASS", load_state().get("smoke", {}).get("verdict") == "PASS", level="WARN")

    verdict = "PASS" if rep.count("FAIL") == 0 else "FAIL"
    save_json(ROOT / "reports" / "setup_check.json", {
        "step": "Langkah 1 — setup IPJ", "verdict": verdict, "failed": rep.count("FAIL"), "warnings": rep.count("WARN"),
        "python": sys.version.split()[0], "sys_prefix": sys.prefix, "checked_at_utc": now_utc(), "items": rep.items})
    print("=" * 72)
    print(f"HASIL: {verdict} | FAIL={rep.count('FAIL')} WARN={rep.count('WARN')} | laporan: reports/setup_check.json")
    print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
