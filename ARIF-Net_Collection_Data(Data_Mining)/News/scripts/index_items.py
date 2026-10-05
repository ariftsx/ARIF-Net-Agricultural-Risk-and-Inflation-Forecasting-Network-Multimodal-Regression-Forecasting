"""Baca ulang raw indeks (verifikasi sha256) → item artikel ter-dedup, dipakai Tahap 2 & normalisasi."""
from __future__ import annotations

import csv
from collections.abc import Iterator

from common import MANIFEST_DAYS, MANIFEST_PAGES, article_id, load_configs, read_raw_gz, resolve_raw, sha256_bytes
from parsers import INDEX_PARSERS


def ok_days() -> dict[tuple[str, str, str], str]:
    """(source, index, date) → run_id dari status TERBARU bila OK/FLAG (run lama yang di-redo diabaikan)."""
    if not MANIFEST_DAYS.exists():
        return {}
    latest: dict[tuple, dict] = {}
    with MANIFEST_DAYS.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            latest[(r["source"], r["index"], r["date"])] = r
    return {k: r["run_id"] for k, r in latest.items() if r["status"] in ("OK", "FLAG")}


def iter_items(problems: list[str], sources: set[str] | None = None, start: str | None = None, end: str | None = None) -> Iterator[dict]:
    """Item dari halaman ber-HTTP 200 pada hari OK/FLAG; halaman terbaru per (source,index,date,page)."""
    days = ok_days()
    cfg, _ = load_configs()
    allowed = {(s, i["name"]) for s, v in cfg["sources"].items() for i in v["indexes"]}   # mis. detikNews dikeluarkan (CP2)
    latest: dict[tuple, dict] = {}
    with MANIFEST_PAGES.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["http_status"] != "200" or days.get((r["source"], r["index"], r["date"])) != r["run_id"]:
                continue
            if (r["source"], r["index"]) not in allowed or (sources and r["source"] not in sources):
                continue
            if (start and r["date"] < start) or (end and r["date"] > end):   # batasi ke rentang fase (efisiensi)
                continue
            latest[(r["source"], r["index"], r["date"], int(r["page"]))] = r
    for key in sorted(latest):
        r = latest[key]
        path = resolve_raw(r["raw_file"])
        if not path.exists():
            problems.append(f"raw hilang: {r['raw_file']}"); continue
        raw = read_raw_gz(path)
        if sha256_bytes(raw) != r["raw_sha256"]:
            problems.append(f"sha256 tidak cocok: {r['raw_file']}"); continue
        for it in INDEX_PARSERS[r["source"]](raw):
            yield {**it, "source": r["source"], "index": r["index"], "index_date": r["date"], "page": int(r["page"]),
                   "article_id": article_id(it["url"]), "raw_index_sha256": r["raw_sha256"]}
