"""
ARIF-Net — Phase 1 PIBC — Langkah 5b: audit deskriptif seri PIBC terpetakan (TIDAK mengubah data).

  1. Kelengkapan harian (kalender penuh) start → end; tanggal duplikat.
  2. Nilai kosong; min / median / max; share hari tanpa perubahan; run berulang terpanjang;
     lompatan harian terbesar (dilaporkan, tidak dikoreksi).
  3. Cakupan terhadap null target: berapa tanggal PIHPS com_3 bernilai '-' yang memiliki nilai PIBC
     pada tanggal sama (DESKRIPTIF — pengisian hanya di tahap P1-DG-06 dengan value_source/is_filled).
  4. Batas sumber: data terakhir PIBC vs end_date target PIHPS.

Output: reports/audit_pibc_summary.json
Pemakaian: conda run -n arif-net python scripts\\audit_pibc.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PIHPS_LONG, PROCESSED, REPORTS, load_configs, now_utc, save_json  # noqa: E402


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 PIBC | Langkah 5b — Audit"); print("=" * 72)
    _, st = load_configs()
    path = PROCESSED / "pibc_medium_i_long.csv"
    if not path.exists():
        print("[FAIL] jalankan normalize_pibc.py dulu"); return 1
    df = pd.read_csv(path, parse_dates=["date"])
    exp = pd.date_range(st["start_date"], st["end_date"], freq="D")
    fails, per = [], {}
    for f, g in df.groupby("variety_field"):
        g = g.sort_values("date").set_index("date")
        rep = g.loc[g["is_reported"], "price_rp"].astype(float)
        chg = rep.pct_change().dropna()
        run = best = 0; prev = None
        for v in rep:
            run = run + 1 if v == prev else 1; prev = v; best = max(best, run)
        missing = exp.difference(g.index)
        dup = int(g.index.duplicated().sum())
        if len(missing) or dup:
            fails.append(f"{f}: tanggal hilang={len(missing)} duplikat={dup}")
        top = chg.abs().sort_values(ascending=False).head(5)
        per[f] = {"label": g["variety_label"].iloc[0], "days": int(len(g)), "expected_days": int(len(exp)),
                  "missing_dates": int(len(missing)), "duplicates": dup, "empty_values": int((~g["is_reported"]).sum()),
                  "first_date": g.index.min().date().isoformat(), "last_date": g.index.max().date().isoformat(),
                  "price_min": float(rep.min()), "price_median": float(rep.median()), "price_max": float(rep.max()),
                  "share_days_no_change_pct": round(100 * float((chg == 0).mean()), 2), "longest_repeat_run_days": best,
                  "largest_abs_daily_change": [{"date": d.date().isoformat(), "pct": round(100 * float(chg[d]), 2)} for d in top.index]}
        p = per[f]
        print(f"[{'PASS' if not (len(missing) or dup) else 'FAIL'}] {f} ({p['label']}): {p['days']}/{p['expected_days']} hari | "
              f"kosong={p['empty_values']} | Rp {p['price_min']:,.0f}–{p['price_max']:,.0f} | tanpa perubahan {p['share_days_no_change_pct']}% "
              f"| run terpanjang {best} hari")

    cover = None
    if PIHPS_LONG.exists():
        ph = pd.read_csv(PIHPS_LONG, parse_dates=["date"])
        nulls = ph[(ph["comcat_id"] == "com_3") & ~ph["is_reported"]]["date"]
        avail = set(df.loc[df["is_reported"], "date"])
        covered = nulls[nulls.isin(avail)]
        cover = {"pihps_com3_null_dates": int(len(nulls)), "with_pibc_value_same_date": int(len(covered)),
                 "pihps_null_after_pibc_end": int((nulls > pd.Timestamp(st["end_date"])).sum()),
                 "note": "Deskriptif saja. Pengisian = tahap P1-DG-06 (value_source + is_filled, validasi overlap, kalibrasi training-only)."}
        print(f"[INFO] null PIHPS com_3 = {cover['pihps_com3_null_dates']} | ada nilai PIBC di tanggal sama = "
              f"{cover['with_pibc_value_same_date']} | null setelah PIBC berakhir = {cover['pihps_null_after_pibc_end']}")
    verdict = "PASS" if not fails else "FAIL"
    save_json(REPORTS / "audit_pibc_summary.json", {
        "step": "Langkah 5b — audit PIBC", "verdict": verdict, "fails": fails, "per_variety": per,
        "coverage_of_pihps_nulls": cover, "source_end_date": st["end_date"],
        "source_end_note": "Situs PIBC tidak diperbarui setelah 2025-06-16; target PIHPS s.d. 2026-09-30.",
        "note": "Audit deskriptif; tidak ada data diubah.", "checked_at_utc": now_utc()})
    print("HASIL:", verdict, "| laporan: reports/audit_pibc_summary.json")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
