"""
ARIF-Net — Phase 1 IPJ — Langkah 5: audit deskriptif (TIDAK mengubah data).

  1. Ketersediaan per bulan (OK vs OK_EMPTY) → bulan pertama/terakhir berisi data.
  2. Per komoditas: hari tercakup vs hari kalender sejak tanggal pertama, nilai kosong/0, min/median/max,
     share hari tanpa perubahan, run berulang terpanjang, lompatan harian terbesar.
  3. Perbandingan dengan PIHPS (eceran, PASAR SAMA) pada tanggal sama: n pasangan, % identik,
     median & p90 |selisih %|. Deskriptif — bukan kalibrasi (kalibrasi = P1-DG-06, training-only).
  4. Cakupan null PIHPS: tanggal '-' PIHPS yang punya nilai IPJ di tanggal sama.

Output: reports/audit_ipj_summary.json, reports/audit_ipj_months.csv
Pemakaian: conda run -n arif-net python scripts\\audit_ipj.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANIFEST, PIHPS_LONG, PROCESSED, REPORTS, load_configs, now_utc, save_json  # noqa: E402


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 IPJ | Langkah 5 — Audit"); print("=" * 72)
    comm, st = load_configs()
    path = PROCESSED / "ipj_kramatjati_long.csv"
    if not path.exists():
        print("[FAIL] jalankan normalize_ipj.py dulu"); return 1
    man = pd.read_csv(MANIFEST, dtype=str, keep_default_na=False)
    man = man[man["check"].isin(["OK", "OK_EMPTY"])].sort_values("collected_at_utc").drop_duplicates("chunk", keep="last").sort_values("chunk")
    man[["chunk", "check", "recaps_per_target"]].to_csv(REPORTS / "audit_ipj_months.csv", index=False)
    data_months = man.loc[man["check"] == "OK", "chunk"].tolist()
    gaps = sorted(set(man["chunk"]) - set(data_months))
    gaps_inside = [m for m in gaps if data_months and data_months[0] < m < data_months[-1]]
    print(f"[INFO] bulan berisi data={len(data_months)} ({data_months[0] if data_months else '-'} → {data_months[-1] if data_months else '-'}) "
          f"| bulan kosong={len(gaps)} | kosong DI ANTARA bulan berisi data={gaps_inside or 'tidak ada'}")

    df = pd.read_csv(path, parse_dates=["date"])
    ph = pd.read_csv(PIHPS_LONG, parse_dates=["date"]) if PIHPS_LONG.exists() else None
    fails, per = [], {}
    for m in comm["commodities"]:
        cid = m["comcat_id"]
        g = df[df["comcat_id"] == cid].sort_values("date").set_index("date")
        if g.empty:
            fails.append(f"{cid}: tidak ada data"); continue
        exp = pd.date_range(g.index.min(), g.index.max(), freq="D")
        rep = g.loc[g["is_reported"], "price_rp"].astype(float)
        chg = rep.pct_change().dropna()
        run = best = 0; prev = None
        for v in rep:
            run = run + 1 if v == prev else 1; prev = v; best = max(best, run)
        top = chg.abs().sort_values(ascending=False).head(5)
        f = {"ipj_commodity": m["ipj_commodity_name"], "first_date": g.index.min().date().isoformat(),
             "last_date": g.index.max().date().isoformat(), "days": int(len(g)), "calendar_days_in_span": int(len(exp)),
             "missing_days_in_span": int(len(exp.difference(g.index))), "not_reported": int((~g["is_reported"]).sum()),
             "price_min": float(rep.min()), "price_median": float(rep.median()), "price_max": float(rep.max()),
             "share_days_no_change_pct": round(100 * float((chg == 0).mean()), 2), "longest_repeat_run_days": best,
             "largest_abs_daily_change": [{"date": d.date().isoformat(), "pct": round(100 * float(chg[d]), 2)} for d in top.index]}
        if ph is not None:
            p = ph[ph["comcat_id"] == cid].set_index("date")
            both = pd.concat([rep.rename("ipj"), p.loc[p["is_reported"], "price_rp_per_kg"].astype(float).rename("pihps")], axis=1, join="inner")
            d = (both["ipj"] / both["pihps"] - 1).abs() * 100
            nulls = p.index[~p["is_reported"]]
            f["vs_pihps_same_market"] = {"n_pairs": int(len(both)), "identical_pct": round(100 * float((both["ipj"] == both["pihps"]).mean()), 2) if len(both) else None,
                                         "median_abs_diff_pct": round(float(d.median()), 3) if len(both) else None,
                                         "p90_abs_diff_pct": round(float(d.quantile(0.9)), 3) if len(both) else None,
                                         "mean_ratio_ipj_over_pihps": round(float((both["ipj"] / both["pihps"]).mean()), 4) if len(both) else None}
            f["pihps_null_dates"] = int(len(nulls))
            f["pihps_null_with_ipj_value"] = int(len(nulls.intersection(rep.index)))
        per[cid] = f
        v = f.get("vs_pihps_same_market", {})
        print(f"[INFO] {cid:6s} {m['ipj_commodity_name']:20s} {f['first_date']}→{f['last_date']} hari={f['days']}/{f['calendar_days_in_span']} "
              f"kosong={f['not_reported']} | Rp {f['price_min']:,.0f}–{f['price_max']:,.0f} | vs PIHPS: n={v.get('n_pairs')} identik={v.get('identical_pct')}% "
              f"median|Δ|={v.get('median_abs_diff_pct')}% | null PIHPS tercakup={f.get('pihps_null_with_ipj_value')}/{f.get('pihps_null_dates')}")
        if f["missing_days_in_span"]:
            print(f"[WARN] {cid}: {f['missing_days_in_span']} hari tidak dikembalikan dalam rentang data")
    dup = int(df.duplicated(["date", "comcat_id"]).sum())
    if dup:
        fails.append(f"{dup} duplikat")
    verdict = "PASS" if not fails else "FAIL"
    save_json(REPORTS / "audit_ipj_summary.json", {
        "step": "Langkah 5 — audit IPJ", "verdict": verdict, "fails": fails, "market": f"{st['market_name']} (id {st['market_id']}, eceran)",
        "months_with_data": len(data_months), "first_month_with_data": data_months[0] if data_months else None,
        "last_month_with_data": data_months[-1] if data_months else None, "empty_months": len(gaps),
        "empty_months_inside_data_span": gaps_inside, "per_commodity": per,
        "note": "Deskriptif; tidak ada data diubah. Perbandingan PIHPS bukan kalibrasi (P1-DG-06: kalibrasi training-only).",
        "checked_at_utc": now_utc()})
    print("HASIL:", verdict, "| laporan: reports/audit_ipj_summary.json")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
