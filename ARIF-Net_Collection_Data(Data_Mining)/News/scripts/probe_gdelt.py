"""
ARIF-Net — Phase 1 News — Langkah 0: probe kelayakan GDELT DOC 2.0 API (read-only).

Tujuan: mengukur — sebelum decision gate sumber news — apakah GDELT menyediakan berita
Indonesia tentang komoditas target sejak 2019, berapa volumenya, dan media apa saja yang tercakup.
BUKAN koleksi final. Setiap respons disimpan byte-identik di data/raw/news/probe/ + sha256.

Endpoint: https://api.gdeltproject.org/api/v2/doc/doc (mode ArtList / TimelineVolRaw, format JSON)
Jeda 6 detik antar-request (sopan terhadap server publik GDELT).

Pemakaian (dari folder News):
    conda run -n arif-net python scripts\\probe_gdelt.py
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "news" / "probe"
REPORTS = ROOT / "reports"
API = "https://api.gdeltproject.org/api/v2/doc/doc"
UA = "ARIF-Net-research-probe/1.0 (capstone research; read-only)"
DELAY = 6.0

# (nama, query, mode, start, end)
PROBES = [
    ("cabai_2019-01", '"cabai" sourcecountry:indonesia', "ArtList", "20190101000000", "20190131235959"),
    ("cabai_2026-09", '"cabai" sourcecountry:indonesia', "ArtList", "20260901000000", "20260930235959"),
    ("bawang_merah_2019-06", '"bawang merah" sourcecountry:indonesia', "ArtList", "20190601000000", "20190630235959"),
    ("harga_beras_2019-06", '"harga beras" sourcecountry:indonesia', "ArtList", "20190601000000", "20190630235959"),
    ("kramat_jati_2024", '"kramat jati" sourcecountry:indonesia', "ArtList", "20240101000000", "20241231235959"),
    ("cabai_volraw_2019-2026", '"cabai" sourcecountry:indonesia', "TimelineVolRaw", "20190101000000", "20260930235959"),
]


def write_new(path: Path, data: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    target, n = path, 1
    while target.exists():
        n += 1
        target = path.with_name(f"{path.stem}.r{n}{path.suffix}")
    target.write_bytes(data)
    return target


def summarize(mode: str, payload: dict) -> dict:
    if mode == "ArtList":
        arts = payload.get("articles") or []
        dates = sorted(a.get("seendate", "") for a in arts if a.get("seendate"))
        return {"n_articles": len(arts), "capped_at_250": len(arts) >= 250,
                "first_seendate": dates[0] if dates else None, "last_seendate": dates[-1] if dates else None,
                "languages": dict(collections.Counter(a.get("language") for a in arts)),
                "top_domains": collections.Counter(a.get("domain") for a in arts).most_common(15),
                "sample_titles": [a.get("title") for a in arts[:5]], "fields": sorted(arts[0].keys()) if arts else []}
    series = (payload.get("timeline") or [{}])[0].get("data") or []
    vals = [(p.get("date"), p.get("value")) for p in series]
    nonzero = [d for d, v in vals if v]
    by_year = collections.defaultdict(int)
    for d, v in vals:
        if d and v:
            by_year[d[:4]] += int(v)
    return {"n_points": len(vals), "first_point": vals[0][0] if vals else None, "last_point": vals[-1][0] if vals else None,
            "points_with_articles": len(nonzero), "first_nonzero": nonzero[0] if nonzero else None,
            "articles_per_year": dict(sorted(by_year.items()))}


def main() -> int:
    s = requests.Session()
    s.headers["User-Agent"] = UA
    results = []
    for name, query, mode, start, end in PROBES:
        params = {"query": query, "mode": mode, "format": "json", "maxrecords": 250,
                  "startdatetime": start, "enddatetime": end, "sort": "DateAsc"}
        try:
            r = s.get(API, params=params, timeout=90)
            status, content, url = r.status_code, r.content, r.url
        except requests.RequestException as exc:
            status, content, url = "EXC", str(exc).encode(), API
        f = write_new(RAW / f"gdelt_{name}.json", content)
        entry = {"name": name, "query": query, "mode": mode, "start": start, "end": end, "http_status": status,
                 "request_url": url, "raw_file": f.relative_to(ROOT).as_posix(), "raw_sha256": hashlib.sha256(content).hexdigest(),
                 "bytes": len(content)}
        try:
            entry["summary"] = summarize(mode, json.loads(content))
        except ValueError:
            entry["summary"] = {"non_json_response": content[:300].decode("utf-8", "replace")}
        results.append(entry)
        print(f"[{status}] {name:24s} {json.dumps(entry['summary'], ensure_ascii=False)[:400]}")
        time.sleep(DELAY)
    out = {"step": "Langkah 0 — probe GDELT DOC 2.0 API", "api": API, "delay_seconds": DELAY,
           "probed_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "results": results,
           "note": "Probe kelayakan, bukan koleksi final. Keputusan sumber = decision gate peneliti."}
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "probe_gdelt.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("laporan: reports/probe_gdelt.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
