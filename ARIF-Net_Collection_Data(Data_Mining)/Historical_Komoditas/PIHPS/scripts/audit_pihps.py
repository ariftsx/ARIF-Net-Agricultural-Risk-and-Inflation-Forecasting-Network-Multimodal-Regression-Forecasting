"""
ARIF-Net — Phase 1 PIHPS — Langkah 5: audit deskriptif harga (TIDAK mengubah data).

  1. Coverage: hari kerja (Sen–Jum) yang dikembalikan sumber vs yang diharapkan; tanggal akhir pekan.
  2. Tidak dilaporkan: tanggal yang dikembalikan tetapi bernilai '-' (sering = hari libur);
     tanggal '-' yang sama di semua komoditas ditandai.
  3. Statistik: min / median / max harga per komoditas.
  4. Dinamika (deskriptif): lompatan harian terbesar antar-hari-dilaporkan; share hari tanpa perubahan;
     run terpanjang nilai berulang (P1-DG-06: nilai berulang = observasi valid, bukan missing).
  5. Konsistensi dengan arsip run 2022 (archive/run_2022) pada tanggal overlap: identik / berbeda.

Output: reports/audit_pihps_summary.json, audit_pihps_not_reported.csv, audit_pihps_missing_weekdays.csv,
        audit_pihps_vs_archive2022.csv
Pemakaian: conda run -n arif-net python scripts\\audit_pihps.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ARCHIVE_2022, PROCESSED, REPORTS, load_configs, now_utc, save_json  # noqa: E402


def longest_run(values: pd.Series) -> tuple[int, str | None]:
    best, cur, best_end, prev = 0, 0, None, object()
    for d, v in values.items():
        cur = cur + 1 if v == prev else 1
        prev = v
        if cur > best:
            best, best_end = cur, d
    return best, best_end


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 PIHPS | Langkah 5 — Audit"); print("=" * 72)
    comm, st = load_configs()
    path = PROCESSED / "pihps_kramatjati_long.csv"
    if not path.exists():
        print("[FAIL] CSV processed tidak ada (Langkah 4)."); return 1
    df = pd.read_csv(path, parse_dates=["date"])
    start, end = pd.Timestamp(st["start_date"]), pd.Timestamp(st["end_date"])
    exp_wd = pd.bdate_range(start, end)
    fails, findings = [], {"per_commodity": {}}
    not_rep_rows, missing_rows = [], []

    dash_sets = {}
    for c in comm["commodities"]:
        cid = c["comcat_id"]
        g = df[df["comcat_id"] == cid].sort_values("date").set_index("date")
        weekend = int((g.index.dayofweek >= 5).sum())
        missing = exp_wd.difference(g.index)
        dash = g.index[~g["is_reported"]]
        dash_sets[cid] = set(dash)
        rep = g.loc[g["is_reported"], "price_rp_per_kg"].astype(float)
        chg = rep.pct_change().dropna()
        top = chg.abs().sort_values(ascending=False).head(5)
        run_len, run_end = longest_run(rep)
        findings["per_commodity"][cid] = {
            "commodity": c["pihps_name"], "dates_returned": int(len(g)), "expected_weekdays": int(len(exp_wd)),
            "weekday_coverage_pct": round(100 * len(exp_wd.intersection(g.index)) / len(exp_wd), 2),
            "weekday_not_returned": int(len(missing)), "weekend_dates_returned": weekend,
            "first_date": g.index.min().date().isoformat(), "last_date": g.index.max().date().isoformat(),
            "reported": int(len(rep)), "not_reported_dash": int(len(dash)),
            "price_min": float(rep.min()), "price_median": float(rep.median()), "price_max": float(rep.max()),
            "share_days_no_change_pct": round(100 * float((chg == 0).mean()), 2),
            "longest_repeat_run_days": run_len, "longest_repeat_run_end": run_end.date().isoformat() if run_end is not None else None,
            "largest_abs_daily_change": [{"date": d.date().isoformat(), "pct": round(100 * float(chg[d]), 2),
                                          "price": float(rep[d]), "prev_price": float(rep.shift(1)[d])} for d in top.index],
        }
        if weekend:
            fails.append(f"{cid}: {weekend} tanggal akhir pekan")
        not_rep_rows += [{"comcat_id": cid, "date": d.date().isoformat(), "weekday": d.day_name()} for d in dash]
        missing_rows += [{"comcat_id": cid, "date": d.date().isoformat(), "weekday": d.day_name()} for d in missing]
        f = findings["per_commodity"][cid]
        print(f"[INFO] {cid:6s} {c['pihps_name']:28s} tanggal={f['dates_returned']} / hari kerja {f['expected_weekdays']} "
              f"({f['weekday_coverage_pct']}%) | dilaporkan={f['reported']} '-'={f['not_reported_dash']} | "
              f"Rp {f['price_min']:,.0f}–{f['price_max']:,.0f} | tanpa perubahan {f['share_days_no_change_pct']}%")

    common_dash = sorted(set.intersection(*dash_sets.values())) if dash_sets else []
    findings["dash_dates_common_all_commodities"] = len(common_dash)
    nr = pd.DataFrame(not_rep_rows, columns=["comcat_id", "date", "weekday"])
    nr["common_all_commodities"] = pd.to_datetime(nr["date"]).isin(common_dash)
    nr.to_csv(REPORTS / "audit_pihps_not_reported.csv", index=False)
    pd.DataFrame(missing_rows, columns=["comcat_id", "date", "weekday"]).to_csv(REPORTS / "audit_pihps_missing_weekdays.csv", index=False)
    print(f"[INFO] tanggal '-' yang sama di ketiga komoditas = {len(common_dash)} (indikasi hari libur / tidak ada survei)")

    dup = int(df.duplicated(["date", "comcat_id"]).sum())
    if dup:
        fails.append(f"{dup} duplikat (date, comcat_id)")

    # 5. konsistensi dengan arsip 2022
    arch_path = ARCHIVE_2022 / "pihps_price_kramatjati_long.csv"
    if arch_path.exists():
        a = pd.read_csv(arch_path, parse_dates=["date"])[["date", "comcat_id", "price_rp_per_kg"]].rename(columns={"price_rp_per_kg": "archive_price"})
        m = df[["date", "comcat_id", "price_rp_per_kg"]].merge(a, on=["date", "comcat_id"], how="inner")
        both = m["price_rp_per_kg"].notna() & m["archive_price"].notna()
        same = both & (m["price_rp_per_kg"].astype(float) == m["archive_price"].astype(float))
        null_mismatch = m["price_rp_per_kg"].isna() != m["archive_price"].isna()
        diff = m[(both & ~same) | null_mismatch]
        diff.to_csv(REPORTS / "audit_pihps_vs_archive2022.csv", index=False)
        findings["archive_2022_overlap"] = {"overlap_rows": int(len(m)), "identical": int(same.sum() + (m["price_rp_per_kg"].isna() & m["archive_price"].isna()).sum()),
                                            "value_differs": int((both & ~same).sum()), "null_status_differs": int(null_mismatch.sum()),
                                            "file": "reports/audit_pihps_vs_archive2022.csv"}
        print(f"[{'PASS' if len(diff) == 0 else 'WARN'}] overlap dengan arsip 2022: {findings['archive_2022_overlap']}")
    else:
        findings["archive_2022_overlap"] = "arsip tidak ditemukan"

    verdict = "PASS" if not fails else "FAIL"
    save_json(REPORTS / "audit_pihps_summary.json", {
        "step": "Langkah 5 — audit PIHPS", "verdict": verdict, "fails": fails, "period": [st["start_date"], st["end_date"]],
        "market": f"{st['market_name']} (level {st['market_level']}, harga eceran)", "findings": findings,
        "note": "Audit deskriptif; tidak ada data diubah. '-' dan tanggal tidak dikembalikan TIDAK diimputasi.",
        "checked_at_utc": now_utc()})
    print("=" * 72); print(f"HASIL: {verdict} | laporan: reports/audit_pihps_summary.json"); print("=" * 72)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
