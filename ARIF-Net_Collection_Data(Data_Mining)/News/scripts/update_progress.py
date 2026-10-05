"""
ARIF-Net — Phase 1 News — tulis progres 93 fase ke AGENT.md (§17, blok bertanda) dan docs §3d.

Sumber kebenaran: data/raw/news/manifest_index_days.csv (status TERBARU per media/indeks/tanggal).
Fase (bulan) = SELESAI bila semua indeks terdaftar berstatus OK/FLAG untuk setiap hari di bulan itu.
Dipanggil otomatis di akhir run_phase.py dan oleh agen saat scraping dihentikan (interupsi pengguna).

Pemakaian: conda run -n arif-net python scripts/update_progress.py [--note "teks"]
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import MANIFEST_DAYS, REPORTS, ROOT, daterange, load_configs, now_utc, save_json  # noqa: E402

AGENT = ROOT.parent / "AGENT.md"
DOCS = ROOT / "docs" / "PHASE1_COLLECTION_NEWS.md"
START, END = "<!-- NEWS_PROGRESS:START -->", "<!-- NEWS_PROGRESS:END -->"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--note", default="", help="catatan (mis. 'dihentikan atas interupsi pengguna')")
    args = ap.parse_args()
    cfg, _ = load_configs()
    p0, p1 = date.fromisoformat(cfg["period"]["start"]), date.fromisoformat(cfg["period"]["end"])
    keys = [(s, i["name"]) for s, v in cfg["sources"].items() for i in v["indexes"]]
    latest: dict[tuple, dict] = {}
    if MANIFEST_DAYS.exists():
        with MANIFEST_DAYS.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                latest[(r["source"], r["index"], r["date"])] = r
    done = {k for k, r in latest.items() if r["status"] in ("OK", "FLAG")}
    months: dict[str, list[date]] = defaultdict(list)
    for d in daterange(p0, p1):
        months[f"{d:%Y-%m}"].append(d)
    status = {}
    for m, ds in months.items():
        per = {f"{s}/{i}": sum((s, i, d.isoformat()) in done for d in ds) for s, i in keys}
        status[m] = {"days": len(ds), "per_source_days_done": per, "complete": all(v == len(ds) for v in per.values()),
                     "started": any(v > 0 for v in per.values())}
    complete = [m for m, v in status.items() if v["complete"]]
    partial = [m for m, v in status.items() if v["started"] and not v["complete"]]
    nxt = next((m for m in months if not status[m]["complete"]), None)
    fails = sum(1 for r in latest.values() if r["status"] == "FAIL")
    articles = defaultdict(int)
    for (s, i, _), r in latest.items():
        if (s, i) in keys and r["status"] in ("OK", "FLAG"):
            articles[f"{s}/{i}"] += int(r["n_items_unique"] or 0)
    per_year = defaultdict(lambda: [0, 0])
    for m, v in status.items():
        per_year[m[:4]][1] += 1
        per_year[m[:4]][0] += v["complete"]
    wib = (datetime.now(timezone.utc) + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M WIB")
    prog = {"updated_at_utc": now_utc(), "phases_total": len(months), "phases_complete": len(complete),
            "last_complete_phase": complete[-1] if complete else None, "next_phase": nxt, "partial_phases": partial,
            "partial_detail": {m: status[m]["per_source_days_done"] for m in partial}, "fail_days_latest": fails,
            "articles_collected": dict(articles), "per_year": {y: f"{a}/{b}" for y, (a, b) in sorted(per_year.items())}, "note": args.note}
    save_json(REPORTS / "progress_news.json", prog)

    lines = [START, f"**Progres scraping News — diperbarui otomatis {wib}** (`News/reports/progress_news.json`)", "",
             "| Item | Nilai |", "|---|---|",
             f"| Fase selesai | **{len(complete)}/{len(months)}** |",
             f"| Fase terakhir selesai | {complete[-1] if complete else '—'} |",
             f"| Fase berikutnya | {nxt or 'SELESAI SEMUA'} |",
             f"| Fase berjalan sebagian | {', '.join(partial) if partial else '—'} |",
             f"| Hari FAIL (status terbaru) | {fails} |",
             f"| Judul terkumpul | {sum(articles.values()):,} ({', '.join(f'{k} {v:,}' for k, v in articles.items())}) |",
             f"| Per tahun (bulan selesai) | {' · '.join(f'{y}: {a}/{b}' for y, (a, b) in sorted(per_year.items()))} |"]
    if partial:
        for m in partial:
            lines.append(f"| Detail {m} (hari selesai per media) | " + ", ".join(f"{k} {v}/{status[m]['days']}" for k, v in status[m]["per_source_days_done"].items()) + " |")
    if args.note:
        lines.append(f"| Catatan | {args.note} |")
    lines.append(END)
    block = "\n".join(lines)

    t = AGENT.read_text(encoding="utf-8")
    if START in t:
        t = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, t, flags=re.S)
    else:
        anchor = "### 17.5 Hal yang sering salah (hindari)"
        t = t.replace(anchor, "### 17.4b Progres eksekusi (otomatis)\n" + block + "\n\n" + anchor, 1) if anchor in t else t + "\n" + block + "\n"
    AGENT.write_text(t, encoding="utf-8")

    d = DOCS.read_text(encoding="utf-8")
    for y, (a, b) in per_year.items():
        d = re.sub(rf"(\| {y} \| [0-9–]+ \| )\d+/\d+( \|)", lambda m: f"{m.group(1)}{a}/{b}{m.group(2)}", d)
    DOCS.write_text(d, encoding="utf-8")
    print(f"Progres: {len(complete)}/{len(months)} fase selesai | berikutnya: {nxt} | sebagian: {partial} | FAIL: {fails}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
