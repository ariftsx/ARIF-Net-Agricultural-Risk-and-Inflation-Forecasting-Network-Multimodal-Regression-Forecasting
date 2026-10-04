"""
ARIF-Net — Phase 1 News — audit deskriptif (TIDAK mengubah data). Contract §19 checklist News.

  1. Cakupan hari per media/indeks: OK / FLAG (batas halaman) / FAIL / belum diambil; hari tanpa artikel.
  2. Halaman per hari (min/median/max) — basis estimasi beban.
  3. Timestamp: artikel relevan tanpa waktu terbit (tidak boleh dipakai Phase 3); presisi waktu (detik/menit/tanggal);
     tanggal terbit ≠ tanggal indeks; waktu terbit di luar periode.
  4. Relevansi: artikel relevan per topik per tahun per media.

Output: reports/audit_news_summary.json, reports/audit_news_days.csv
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANIFEST_DAYS, PROCESSED, REPORTS, daterange, load_configs, now_utc, save_json  # noqa: E402


def main() -> int:
    print("=" * 72); print("ARIF-Net | Phase 1 News | Audit"); print("=" * 72)
    cfg, _ = load_configs()
    p0, p1 = date.fromisoformat(cfg["period"]["start"]), date.fromisoformat(cfg["period"]["end"])
    n_days = len(daterange(p0, p1))
    days = pd.read_csv(MANIFEST_DAYS, dtype=str).sort_values("finished_at_utc").drop_duplicates(["source", "index", "date"], keep="last")
    days.to_csv(REPORTS / "audit_news_days.csv", index=False)
    rel_path = PROCESSED / "articles_relevant.csv"
    rel_df = pd.read_csv(rel_path, dtype=str, keep_default_na=False) if rel_path.exists() else pd.DataFrame()
    summary, fails = {}, []
    for s, scfg in cfg["sources"].items():
        info = {}
        for idx in scfg["indexes"]:
            d = days[(days["source"] == s) & (days["index"] == idx["name"])]
            pages = pd.to_numeric(d.loc[d["status"].isin(["OK", "FLAG"]), "pages_fetched"], errors="coerce")
            items = pd.to_numeric(d.loc[d["status"].isin(["OK", "FLAG"]), "n_items_unique"], errors="coerce")
            info[idx["name"]] = {"days_expected": n_days, "ok": int((d["status"] == "OK").sum()), "flag_max_pages": int((d["status"] == "FLAG").sum()),
                                 "fail": int((d["status"] == "FAIL").sum()), "not_collected": n_days - int(d["status"].isin(["OK", "FLAG", "FAIL"]).sum()),
                                 "days_zero_articles": int((items == 0).sum()),
                                 "pages_per_day": {"min": float(pages.min()) if len(pages) else None, "median": float(pages.median()) if len(pages) else None,
                                                   "max": float(pages.max()) if len(pages) else None}}
        r = rel_df[rel_df["source"] == s] if len(rel_df) else rel_df
        if len(r):
            pub = pd.to_datetime(r["published_at_wib"].str[:19], errors="coerce")
            idx_d = pd.to_datetime(r["index_date"], errors="coerce")
            info["relevant"] = {"n": int(len(r)), "without_time": int((r["published_at_wib"] == "").sum()),
                                "precision": r["time_precision"].replace("", "none").value_counts().to_dict(),
                                "pub_date_ne_index_date": int(((pub.dt.normalize() != idx_d) & pub.notna()).sum()),
                                "outside_period": int(((pub < pd.Timestamp(p0)) | (pub > pd.Timestamp(p1) + pd.Timedelta(days=1))).sum()),
                                "per_year": r["index_date"].str[:4].value_counts().sort_index().to_dict(),
                                "per_topic": pd.Series([t for x in r["topics_matched"] for t in x.split("|") if t]).value_counts().to_dict()}
        summary[s] = info
        for k, v in info.items():
            if k != "relevant" and v["fail"]:
                fails.append(f"{s}/{k}: {v['fail']} hari FAIL")
        rv = info.get("relevant", {})
        print(f"[INFO] {s:14s} " + " ".join(f"{k}: ok={v['ok']}/{n_days} fail={v['fail']} hal/hari med={v['pages_per_day']['median']}"
                                           for k, v in info.items() if k != "relevant")
              + f" | relevan={rv.get('n')} tanpa_waktu={rv.get('without_time')}")
    verdict = "PASS" if not fails else "WARN"
    save_json(REPORTS / "audit_news_summary.json", {"step": "Audit News", "verdict": verdict, "period": [str(p0), str(p1)],
              "per_source": summary, "issues": fails,
              "note": "Deskriptif (Contract §19). Artikel tanpa waktu terbit tidak boleh dipakai Phase 3. Tidak ada data diubah.",
              "checked_at_utc": now_utc()})
    print("HASIL:", verdict, "| laporan: reports/audit_news_summary.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
