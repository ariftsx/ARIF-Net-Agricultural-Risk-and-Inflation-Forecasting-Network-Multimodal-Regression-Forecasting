"""
ARIF-Net — Phase 1 PIBC — Langkah 1: verifikasi setup (offline).

Nilai yang dikunci keputusan/analisis ditulis eksplisit di sini → config yang menyimpang = FAIL.

Pemakaian (dari folder PIBC):
    conda run -n arif-net python scripts\\verify_setup.py
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PIHPS_LONG, ROOT, WIN_MAX_PATH, load_configs, load_state, longest_pipeline_path, now_utc, save_json  # noqa: E402

LOCKED_FIELDS = ["cjr_kpl", "cjr_slyp", "setra", "saigon", "muncul1", "muncul2", "muncul3",
                 "ir641", "ir642", "ir643", "ir42", "kp_biasa", "kp_paris", "ktn_htm"]
LOCKED_SETTINGS = {
    "data_url": "https://pibc.foodstation.co.id/rice-price-detail",
    "columns": ["tgl", *LOCKED_FIELDS],
    "start_date": "2019-01-01",          # P1-DG-16 (sejajar PIHPS)
    "end_date": "2025-06-16",            # data terakhir sumber (probe 2026-10-03)
    "chunk": "yearly", "imputation_at_collection": False,
}
REQUIRED_DIRS = ["config", "scripts", "tests", "docs", "logs", "reports", "data/raw/pibc/smoke", "data/processed/pibc"]
REQUIRED_FILES = ["README.md", "environment.yml", "requirements.txt", "config/varieties.json",
                  "config/request_settings.json", "docs/PHASE1_COLLECTION_PIBC.md"]


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
    print("=" * 72); print("ARIF-Net | Phase 1 PIBC | Langkah 1 — Verifikasi setup"); print("=" * 72)
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

    var, st = load_configs()
    fields = [v["field"] for v in var["varieties"]]
    rep.add("14 kolom varietas sesuai header halaman PIBC", fields == LOCKED_FIELDS, f"{len(fields)}")
    for key, val in LOCKED_SETTINGS.items():
        rep.add(f"setting {key} = {val!r}" if key != "columns" else "setting columns (15 field DataTables)",
                st.get(key) == val, "" if key == "columns" else f"terdeteksi {st.get(key)!r}")
    rep.add("page_length ≥ 366 (1 tahun per request)", int(st.get("page_length", 0)) >= 366, str(st.get("page_length")))
    rep.add("delay ≥ 1 detik", float(st.get("delay_seconds", 0)) >= 1.0, str(st.get("delay_seconds")))
    m = var.get("medium_i_mapping")
    rep.add("pemetaan Beras Medium I diputuskan peneliti (P1-DG-05; dibutuhkan Langkah 5)",
            m is not None and all(x in fields for x in (m if isinstance(m, list) else [m])),
            f"medium_i_mapping = {m!r}", level="WARN")
    rep.add("CSV PIHPS tersedia (untuk bukti pemetaan)", PIHPS_LONG.is_file(), str(PIHPS_LONG.name), level="WARN")
    longest = longest_pipeline_path()
    rep.add(f"path terpanjang pipeline ≤ {WIN_MAX_PATH} karakter", len(str(longest)) <= WIN_MAX_PATH,
            f"{len(str(longest))} karakter: {longest.relative_to(ROOT)}")
    rep.add("smoke test PASS", load_state().get("smoke", {}).get("verdict") == "PASS", level="WARN")

    verdict = "PASS" if rep.count("FAIL") == 0 else "FAIL"
    save_json(ROOT / "reports" / "setup_check.json", {
        "step": "Langkah 1 — setup PIBC", "verdict": verdict, "failed": rep.count("FAIL"), "warnings": rep.count("WARN"),
        "python": sys.version.split()[0], "sys_prefix": sys.prefix, "checked_at_utc": now_utc(), "items": rep.items})
    print("=" * 72)
    print(f"HASIL: {verdict} | FAIL={rep.count('FAIL')} WARN={rep.count('WARN')} | laporan: reports/setup_check.json")
    print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
