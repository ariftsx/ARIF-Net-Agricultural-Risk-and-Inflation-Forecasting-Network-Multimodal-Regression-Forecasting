"""
ARIF-Net — Phase 1 News — satu FASE = SATU BULAN data (keputusan peneliti 2026-10-03, revisi ke pilihan A:
fase kecil ±40–60 menit supaya laptop tidak berjalan berjam-jam; 93 fase 2019-01 … 2026-09).
Opsi --year (fase besar) tetap tersedia.

Urutan per fase:
  1. verify_setup.py                                    (berhenti bila FAIL)
  2. collect_index.py --start … --end … [--max-minutes N]   ← 6 media paralel, resume otomatis
  3. collect_articles.py --start … --end …              ← waktu terbit artikel relevan CNN/CNBC (hanya bulan fase)
  4. normalize_news.py + audit_news.py                   ← kumulatif; HANYA di fase Desember, fase terakhir (2026-09), atau --normalize
  5. reports/phase_<YYYY-MM>.json + update_progress.py  ← ringkasan fase & blok progres di AGENT.md/docs

Aman dihentikan kapan saja (Ctrl+C / laptop mati): jalankan ulang perintah yang sama → lanjut dari hari terakhir.

Pemakaian (Windows CMD, dari folder News):
    conda run -n arif-net --no-capture-output python scripts/run_phase.py --month 2019-01
    conda run -n arif-net --no-capture-output python scripts/run_phase.py --month 2019-01 --max-minutes 60
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANIFEST_DAYS, REPORTS, daterange, load_configs, now_utc, save_json  # noqa: E402

HERE = Path(__file__).resolve().parent


def step(name: str, *args: str) -> int:
    print("\n" + "=" * 72 + f"\n>>> {name} {' '.join(args)}\n" + "=" * 72, flush=True)
    return subprocess.run([sys.executable, str(HERE / name), *args]).returncode


def phase_range(args, p0: date, p1: date) -> tuple[date, date, str]:
    if args.month:
        y, m = map(int, args.month.split("-"))
        nxt = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
        return max(p0, date(y, m, 1)), min(p1, date.fromordinal(nxt.toordinal() - 1)), f"{y}-{m:02d}"
    return max(p0, date(args.year, 1, 1)), min(p1, date(args.year, 12, 31)), str(args.year)


def main() -> int:
    ap = argparse.ArgumentParser(description="Jalankan satu fase koleksi News (disarankan: 1 bulan).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--month", help="YYYY-MM (1 fase = 1 bulan, ±40–60 menit)")
    g.add_argument("--year", type=int, choices=range(2019, 2027), help="1 tahun (fase besar, ±5–9 jam)")
    ap.add_argument("--normalize", action="store_true", help="paksa normalisasi + audit kumulatif di fase ini")
    ap.add_argument("--max-minutes", type=float, default=None,
                    help="batas waktu pengaman: koleksi berhenti rapi setelah N menit; jalankan ulang untuk melanjutkan")
    args = ap.parse_args()
    cfg, _ = load_configs()
    p0, p1 = date.fromisoformat(cfg["period"]["start"]), date.fromisoformat(cfg["period"]["end"])
    start, end, label = phase_range(args, p0, p1)
    if start > end:
        print(f"[FAIL] fase {label} di luar periode P1-DG-26 {p0}→{p1}"); return 1
    started = now_utc()
    extra = ["--max-minutes", str(args.max_minutes)] if args.max_minutes else []

    if step("verify_setup.py") != 0:
        print("[STOP] verify_setup FAIL — perbaiki dulu (lihat reports/setup_check.json)."); return 1
    rc_index = step("collect_index.py", "--start", start.isoformat(), "--end", end.isoformat(), *extra)
    rc_art = step("collect_articles.py", "--start", start.isoformat(), "--end", end.isoformat(), *extra)
    do_norm = args.normalize or end.month == 12 or end == p1
    rc_norm = step("normalize_news.py") if do_norm else None
    rc_audit = step("audit_news.py") if do_norm else None

    latest: dict[tuple, dict] = {}
    with MANIFEST_DAYS.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if start.isoformat() <= r["date"] <= end.isoformat():
                latest[(r["source"], r["index"], r["date"])] = r
    n_days = len(daterange(start, end))
    per = {}
    for s, scfg in cfg["sources"].items():
        for idx in scfg["indexes"]:
            rows = [r for (a, b, _), r in latest.items() if a == s and b == idx["name"]]
            per[f"{s}/{idx['name']}"] = {"days_expected": n_days, "ok": sum(r["status"] == "OK" for r in rows),
                                         "flag": sum(r["status"] == "FLAG" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows),
                                         "articles": sum(int(r["n_items_unique"] or 0) for r in rows)}
    complete = all(v["ok"] + v["flag"] == n_days for v in per.values())
    rep = {"phase": label, "range": [start.isoformat(), end.isoformat()], "started_at_utc": started, "finished_at_utc": now_utc(),
           "verdict": "COMPLETE" if complete else "INCOMPLETE (jalankan ulang perintah yang sama untuk melanjutkan)",
           "per_source": per, "return_codes": {"collect_index": rc_index, "collect_articles": rc_art, "normalize": rc_norm, "audit": rc_audit}}
    save_json(REPORTS / f"phase_{label}.json", rep)
    step("update_progress.py")
    print("\n" + "=" * 72)
    for k, v in per.items():
        print(f"{k:22s} OK={v['ok']:>3}/{n_days} FLAG={v['flag']} FAIL={v['fail']} artikel={v['articles']:,}")
    print(f"FASE {label}: {rep['verdict']} | laporan: reports/phase_{label}.json")
    print("=" * 72)
    return 0 if complete else 1


if __name__ == "__main__":
    sys.exit(main())
