"""
ARIF-Net — Phase 1 News — verifikasi setup (offline). Nilai terkunci P1-DG-25…30 → config menyimpang = FAIL.

Pemakaian (dari folder News):
    conda run -n arif-net python scripts\\verify_setup.py
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WIN_MAX_PATH, load_configs, longest_pipeline_path, now_utc, save_json  # noqa: E402

LOCKED_SOURCES = ["kompas", "detik", "cnnindonesia", "cnbcindonesia", "kontan", "liputan6"]          # P1-DG-25
LOCKED_PERIOD = {"start": "2019-01-01", "end": "2026-09-30"}                                       # P1-DG-26
LOCKED_TOPIC_GROUPS = ["komoditas_cmk", "komoditas_bawang_merah", "komoditas_beras", "pasar_pasokan",
                       "harga_inflasi_kebijakan", "cuaca_iklim", "bbm_logistik"]                     # P1-DG-27
EXCLUDED = ["katadata", "bisnis", "tempo", "antaranews", "gdelt"]


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
    print("=" * 72); print("ARIF-Net | Phase 1 News | Verifikasi setup"); print("=" * 72)
    rep = Report()
    rep.add("Python 3.13.x", sys.version_info[:2] == (3, 13), sys.version.split()[0])
    rep.add("Conda env 'arif-net'", Path(sys.prefix).name.lower() == "arif-net", sys.prefix, level="WARN")
    for pkg in ("requests", "pandas", "bs4", "lxml"):
        try:
            mod = importlib.import_module(pkg)
            rep.add(f"import {pkg}", True, str(getattr(mod, "__version__", "")))
        except Exception as exc:  # noqa: BLE001
            rep.add(f"import {pkg}", False, f"{type(exc).__name__}: {exc}")
    for d in ("config", "scripts", "tests", "docs", "reports", "logs", "data/raw/news", "data/processed/news"):
        rep.add(f"folder {d}/", (ROOT / d).is_dir())
    cfg, scope = load_configs()
    rep.add("sumber = 6 media P1-DG-25", list(cfg["sources"]) == LOCKED_SOURCES, str(list(cfg["sources"])))
    rep.add("tidak ada sumber yang dikeluarkan", not set(cfg["sources"]) & set(EXCLUDED))
    rep.add("periode = P1-DG-26", cfg["period"] == LOCKED_PERIOD, str(cfg["period"]))
    rep.add("keputusan P1-DG-25…30 tercatat DECIDED", all(f"P1-DG-{n}" in scope.get("decisions", {}) for n in range(25, 31)))
    rep.add("7 kelompok topik P1-DG-27", list(scope["topics"]) == LOCKED_TOPIC_GROUPS, str(list(scope["topics"])))
    rep.add("Detik: tanggal indeks ter-encode (%2F)", all("{date_mdy_enc}" in i["url"] for i in cfg["sources"]["detik"]["indexes"]))
    rep.add("jeda ≥ 1 detik", float(cfg["delay_seconds"]) >= 1.0, str(cfg["delay_seconds"]))
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
    rep.add("raw HTML & artikel tidak di-commit (.gitignore)", "data/raw/news/ix/" in gi and "data/raw/news/art/" in gi)
    from common import RAW_STORE
    rep.add("lokasi raw HTML di luar OneDrive (±11–12 GB)", "onedrive" not in str(RAW_STORE).lower(), str(RAW_STORE), level="WARN")
    try:
        RAW_STORE.mkdir(parents=True, exist_ok=True); (RAW_STORE / ".write_test").write_text("ok"); (RAW_STORE / ".write_test").unlink()
        rep.add("lokasi raw dapat ditulis", True, str(RAW_STORE))
    except OSError as exc:
        rep.add("lokasi raw dapat ditulis", False, str(exc))
    rep.add("18 kabupaten pemasok terbaca dari Iklim/config/locations.json", len(__import__("common").load_supplier_locations()) == 18)
    longest = longest_pipeline_path([v["code"] for v in cfg["sources"].values()])
    rep.add(f"path terpanjang ≤ {WIN_MAX_PATH}", len(str(longest)) <= WIN_MAX_PATH, f"{len(str(longest))}: {longest}")
    verdict = "PASS" if rep.count("FAIL") == 0 else "FAIL"
    save_json(ROOT / "reports" / "setup_check.json", {"step": "Setup News", "verdict": verdict, "failed": rep.count("FAIL"),
              "warnings": rep.count("WARN"), "checked_at_utc": now_utc(), "items": rep.items})
    print("=" * 72); print(f"HASIL: {verdict} | FAIL={rep.count('FAIL')} WARN={rep.count('WARN')}"); print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
