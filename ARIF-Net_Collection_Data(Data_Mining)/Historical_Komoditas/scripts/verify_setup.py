"""
ARIF-Net — Phase 1 PIHPS — Langkah 1: verifikasi setup (offline).

Memeriksa env, struktur folder, panjang path Windows, dan kesesuaian config dengan
keputusan P1-DG-01…06, 13, 16 (Plan v2.0.0 §0.5; Contract v2.1.0 §3.1, §5.6).
Nilai yang dikunci keputusan ditulis eksplisit di sini → config yang menyimpang = FAIL.

Pemakaian (dari folder Historical_Komoditas):
    conda run -n arif-net python scripts\\verify_setup.py
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WIN_MAX_PATH, load_configs, load_state, longest_pipeline_path, now_utc, save_json  # noqa: E402

LOCKED_COMMODITIES = {  # P1-DG-04/05; bawang putih dikeluarkan (P1-DG-13)
    "Cabai Merah Keriting": "com_14",
    "Bawang Merah Ukuran Sedang": "com_11",
    "Beras Kualitas Medium I": "com_3",
}
LOCKED_SETTINGS = {
    "data_url": "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas",
    "price_type_id": 1, "province_id": 13, "regency_id": 34, "tipe_laporan": 1,
    "show_kota": "true", "show_pasar": "true",
    "market_name": "Pasar Kramatjati", "market_level": 3,          # P1-DG-02/03
    "start_date": "2019-01-01", "end_date": "2026-09-30",          # P1-DG-16 + keputusan peneliti
    "chunk": "monthly", "imputation_at_collection": False,
}
REQUIRED_PACKAGES = ["requests", "pandas", "numpy"]
REQUIRED_DIRS = ["config", "scripts", "tests", "docs", "logs", "reports", "data/raw/pihps/reference",
                 "data/raw/pihps/smoke", "data/processed/pihps", "archive/run_2022"]
REQUIRED_FILES = ["README.md", "environment.yml", "requirements.txt", "config/commodities.json",
                  "config/request_settings.json", "docs/PHASE1_COLLECTION_PIHPS.md"]


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
    print("=" * 72); print("ARIF-Net | Phase 1 PIHPS | Langkah 1 — Verifikasi setup"); print("=" * 72)
    rep = Report()
    rep.add("Python 3.13.x", sys.version_info[:2] == (3, 13), sys.version.split()[0])
    rep.add("Conda env 'arif-net'", Path(sys.prefix).name.lower() == "arif-net", f"sys.prefix = {sys.prefix}", level="WARN")
    for pkg in REQUIRED_PACKAGES:
        try:
            rep.add(f"import {pkg}", True, getattr(importlib.import_module(pkg), "__version__", "?"))
        except Exception as exc:  # noqa: BLE001
            rep.add(f"import {pkg}", False, f"{type(exc).__name__}: {exc}")
    for d in REQUIRED_DIRS:
        rep.add(f"folder {d}/", (ROOT / d).is_dir())
    for f in REQUIRED_FILES:
        rep.add(f"file {f}", (ROOT / f).is_file())

    comm, settings = load_configs()
    got = {c["pihps_name"]: c["comcat_id"] for c in comm["commodities"]}
    rep.add("komoditas = 3 primary P1-DG-04/05", got == LOCKED_COMMODITIES, str(got))
    rep.add("bawang putih tidak ada (P1-DG-13)", not any("putih" in n.lower() for n in got))
    for key, val in LOCKED_SETTINGS.items():
        rep.add(f"setting {key} = {val!r}", settings.get(key) == val, f"terdeteksi {settings.get(key)!r}")
    rep.add("delay ≥ 1 detik (sopan terhadap server BI)", float(settings.get("delay_seconds", 0)) >= 1.0,
            str(settings.get("delay_seconds")))

    longest = longest_pipeline_path(list(got.values()))
    rep.add(f"path terpanjang pipeline ≤ {WIN_MAX_PATH} karakter", len(str(longest)) <= WIN_MAX_PATH,
            f"{len(str(longest))} karakter: {longest.relative_to(ROOT)}")
    rep.add("arsip run 2022 tersedia (pembanding audit)",
            (ROOT / "archive/run_2022/data_raw_pihps/pihps_price_kramatjati_long.csv").is_file(), level="WARN")
    sm = load_state().get("smoke", {})
    rep.add("smoke test PASS (Langkah 2)", sm.get("verdict") == "PASS", sm.get("at", "belum dijalankan"), level="WARN")

    verdict = "PASS" if rep.count("FAIL") == 0 else "FAIL"
    save_json(ROOT / "reports" / "setup_check.json", {
        "step": "Langkah 1 — setup", "verdict": verdict, "failed": rep.count("FAIL"), "warnings": rep.count("WARN"),
        "python": sys.version.split()[0], "sys_prefix": sys.prefix, "checked_at_utc": now_utc(), "items": rep.items})
    print("=" * 72)
    print(f"HASIL: {verdict} | FAIL={rep.count('FAIL')} WARN={rep.count('WARN')} | laporan: reports/setup_check.json")
    print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
