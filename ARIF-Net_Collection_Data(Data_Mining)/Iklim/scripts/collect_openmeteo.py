"""
ARIF-Net — Phase 1 Climate — Langkah 3/4 (smoke) & 5 (full): collector Open-Meteo Historical Weather API.

Mode:
  smoke  1 lokasi × 1 bulan per set (core/reserve). Memverifikasi nama parameter, model, unit,
         timezone, dan ketersediaan variabel. Hasil PASS dicatat di config/state.json.
  full   18 lokasi × chunk tahunan × set core lalu reserve. Hanya berjalan bila koordinat
         terisi dan smoke kedua set PASS dengan model yang sama. Dapat di-resume.

Aturan (Plan v2.0.0 §10.2a; Contract v2.1.0 §5.6; AGENT.md §8):
  * Raw = evidence: bytes response disimpan apa adanya + sha256 di manifest; tidak pernah ditimpa.
  * Tanpa imputasi, agregasi, lag, atau feature engineering. Tanggal disimpan apa adanya (WIB).
  * Core & reserve: request dan folder terpisah (P1-DG-14).
  * Model: era5_seamless; fallback era5 HANYA lewat smoke --model era5 (P1-DG-10). Best Match dilarang.
  * Kuota: rate limiter berbobot (common.ApiBudget) mengikuti aturan hitung Open-Meteo.

Contoh (dari folder Iklim):
  conda run -n arif-net python scripts\\collect_openmeteo.py smoke --set core
  conda run -n arif-net python scripts\\collect_openmeteo.py smoke --set reserve
  conda run -n arif-net python scripts\\collect_openmeteo.py full
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    LOCKED_UNITS, LOGS, MANIFEST, RAW, REPORTS, ROOT, SETS, SMOKE, ApiBudget, BudgetExhausted, build_params,
    daily_series, daily_unit, load_configs, load_state, n_days, now_utc, raw_path, rel, request_weight,
    save_json, save_state, sha256_bytes, sha256_file, stamp, variables_for, write_new, year_chunks,
)

MANIFEST_FIELDS = [
    "set", "location_id", "year", "start_date", "end_date", "model", "request_url", "http_status",
    "raw_file", "raw_sha256", "raw_bytes", "grid_latitude", "grid_longitude", "grid_elevation",
    "utc_offset_seconds", "timezone", "n_days", "n_null_values", "api_weight", "check", "error", "collected_at_utc",
]
EXIT_PAUSED = 3


def setup_logging(tag: str) -> None:
    LOGS.mkdir(exist_ok=True)
    logfile = LOGS / f"collect_{tag}_{stamp()}.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(logfile, encoding="utf-8")])
    logging.info("Log: %s", rel(logfile))


def fetch(session: requests.Session, settings: dict, params: dict, budget: ApiBudget,
          weight: float, kind: str, label: str) -> requests.Response:
    """GET dengan rate limit berbobot + retry (429 / 5xx / koneksi). HTTP 400 dikembalikan apa adanya."""
    last: requests.Response | Exception | None = None
    for attempt in range(1, settings["retries"] + 1):
        budget.acquire(weight)
        try:
            r = session.get(settings["endpoint"], params=params, timeout=settings["timeout_seconds"])
        except requests.RequestException as exc:
            budget.record(weight, kind, label, "EXC")
            last = exc
            logging.warning("%s: koneksi gagal (percobaan %s/%s): %s", label, attempt, settings["retries"], exc)
            time.sleep(10 * attempt)
            continue
        budget.record(weight, kind, label, r.status_code)
        time.sleep(settings["min_delay_seconds"])
        if r.status_code == 429 or r.status_code >= 500:
            wait = 60 * attempt if r.status_code == 429 else 10 * attempt
            logging.warning("%s: HTTP %s (percobaan %s/%s) → tunggu %ss", label, r.status_code, attempt, settings["retries"], wait)
            last = r
            time.sleep(wait)
            continue
        return r
    if isinstance(last, requests.Response):
        return last
    raise last if last else RuntimeError("fetch gagal tanpa respons")


def error_reason(r: requests.Response) -> str:
    try:
        return str(r.json().get("reason", r.text[:300]))
    except ValueError:
        return r.text[:300]


def summarize(payload: dict, variables: list[str]) -> dict:
    times = (payload.get("daily") or {}).get("time") or []
    per_var = {}
    for v in variables:
        s = daily_series(payload, v)
        per_var[v] = {"present": s is not None, "n_values": len(s) if s is not None else None,
                      "n_null": sum(1 for x in s if x is None) if s is not None else None,
                      "unit": daily_unit(payload, v), "first_values": s[:3] if s is not None else None}
    return {"times": times, "per_var": per_var}


def chunk_check(payload: dict, summ: dict, start: date, end: date, settings: dict, variables: list[str]) -> list[str]:
    """Validasi struktural respons (tanpa mengubah data). Kosong = OK."""
    issues = []
    if payload.get("utc_offset_seconds") != settings["expected_utc_offset_seconds"]:
        issues.append(f"utc_offset={payload.get('utc_offset_seconds')}")
    if payload.get("timezone") != settings["timezone"]:
        issues.append(f"timezone={payload.get('timezone')}")
    t = summ["times"]
    if len(t) != n_days(start, end):
        issues.append(f"n_days={len(t)}≠{n_days(start, end)}")
    if t and (t[0] != str(start) or t[-1] != str(end)):
        issues.append(f"rentang={t[0]}→{t[-1]}")
    for v in variables:
        info = summ["per_var"][v]
        if not info["present"]:
            issues.append(f"{v} tidak ada")
        elif info["n_values"] != len(t):
            issues.append(f"{v} panjang {info['n_values']}≠{len(t)}")
    return issues


# ---------------------------------------------------------------- manifest
def append_manifest(row: dict) -> None:
    new = not MANIFEST.exists()
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in MANIFEST_FIELDS})


def done_chunks() -> set[tuple[str, str, str]]:
    """(set, location_id, year) yang sukses: HTTP 200, check OK, file ada, sha256 cocok."""
    out: set[tuple[str, str, str]] = set()
    if not MANIFEST.exists():
        return out
    with MANIFEST.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            p = ROOT / r["raw_file"] if r["raw_file"] else None
            if r["http_status"] == "200" and r["check"] == "OK" and p and p.exists() and sha256_file(p) == r["raw_sha256"]:
                out.add((r["set"], r["location_id"], r["year"]))
    return out


# ---------------------------------------------------------------- smoke
def cmd_smoke(args) -> int:
    setup_logging(f"smoke_{args.set}")
    locs, varcfg, settings = load_configs()
    state = load_state()
    model = args.model or settings["model_primary"]
    if args.set == "reserve":
        core = state.get("smoke", {}).get("core", {})
        if core.get("verdict") != "PASS":
            logging.error("Smoke CORE belum PASS. Jalankan Langkah 3 dulu."); return 1
        if model != core["model"]:
            logging.error("Reserve WAJIB memakai model yang sama dengan core ('%s'). Ulangi dengan --model %s.",
                          core["model"], core["model"]); return 1
    loc = next((l for l in locs["locations"] if l["location_id"] == args.location), None)
    if loc is None:
        logging.error("location_id '%s' tidak ada.", args.location); return 1
    if loc["latitude"] is None:
        logging.error("Koordinat '%s' belum diisi. Selesaikan Langkah 2.", args.location); return 1

    variables = variables_for(varcfg, args.set)
    params = build_params(loc, variables, args.start, args.end, settings, model)
    weight = request_weight(len(variables), n_days(args.start, args.end))
    budget = ApiBudget(settings["rate_limit"], log=logging.info)
    label = f"smoke:{args.set}:{loc['location_id']}:{model}"
    r = fetch(requests.Session(), settings, params, budget, weight, "smoke", label)
    raw_file = write_new(SMOKE / f"{args.set}_{model}_{loc['location_id']}.json", r.content)

    checks: list[dict] = []

    def chk(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
        logging.info("[%s] %s%s", "PASS" if ok else "FAIL", name, f" — {detail}" if detail else "")

    report = {"step": f"Langkah {'3' if args.set == 'core' else '4'} — smoke {args.set}", "set": args.set, "model": model,
              "location_id": loc["location_id"], "requested_point": [loc["latitude"], loc["longitude"]],
              "period": [str(args.start), str(args.end)], "request_url": r.url, "http_status": r.status_code,
              "api_weight": round(weight, 3), "raw_file": rel(raw_file), "raw_sha256": sha256_bytes(r.content),
              "checked_at_utc": now_utc()}
    chk("HTTP 200", r.status_code == 200, f"status={r.status_code}" + (f" reason={error_reason(r)}" if r.status_code != 200 else ""))
    failure_kind = "http" if r.status_code != 200 else None
    if r.status_code == 200:
        payload = r.json()
        summ = summarize(payload, variables)
        expected = n_days(args.start, args.end)
        chk("utc_offset_seconds = 25200 (WIB)", payload.get("utc_offset_seconds") == settings["expected_utc_offset_seconds"],
            str(payload.get("utc_offset_seconds")))
        chk("timezone = Asia/Jakarta", payload.get("timezone") == settings["timezone"], str(payload.get("timezone")))
        chk("daily_units.time = iso8601", (payload.get("daily_units") or {}).get("time") == "iso8601",
            str((payload.get("daily_units") or {}).get("time")))
        chk(f"jumlah hari = {expected}", len(summ["times"]) == expected, str(len(summ["times"])))
        chk("hari pertama/terakhir sesuai", bool(summ["times"]) and summ["times"][0] == str(args.start)
            and summ["times"][-1] == str(args.end), f"{summ['times'][:1]}…{summ['times'][-1:]}")
        doc_units = {v["api_param"]: v["doc_unit"] for v in varcfg[args.set]}
        for v, info in summ["per_var"].items():
            ok = info["present"] and info["n_null"] is not None and info["n_null"] < len(summ["times"])
            if not ok:
                failure_kind = failure_kind or "variable"
            chk(f"variabel {v} ada & tidak seluruhnya null", ok,
                f"unit={info['unit']} null={info['n_null']}/{len(summ['times'])} contoh={info['first_values']}")
            if info["present"] and doc_units[v] in LOCKED_UNITS:
                chk(f"unit {v} = {doc_units[v]} (P1-DG-15)", info["unit"] == doc_units[v], str(info["unit"]))
        unit_mismatch = {v: {"doc": doc_units[v], "response": i["unit"]} for v, i in summ["per_var"].items()
                         if i["present"] and i["unit"] != doc_units[v] and doc_units[v] not in LOCKED_UNITS}
        report.update({
            "response_meta": {k: payload.get(k) for k in ("latitude", "longitude", "elevation", "utc_offset_seconds",
                                                          "timezone", "timezone_abbreviation", "generationtime_ms")},
            "daily_units": payload.get("daily_units"), "per_variable": summ["per_var"],
            "unit_notes_non_locked": unit_mismatch,
        })
    verdict = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    report.update({"verdict": verdict, "checks": checks})
    save_json(REPORTS / f"smoke_{args.set}.json", report)

    hist = state.setdefault("smoke_history", [])
    hist.append({"set": args.set, "model": model, "verdict": verdict, "at": report["checked_at_utc"], "raw_file": report["raw_file"]})
    if verdict == "PASS":
        state.setdefault("smoke", {})[args.set] = {"verdict": "PASS", "model": model, "at": report["checked_at_utc"],
                                                   "raw_file": report["raw_file"], "report": f"reports/smoke_{args.set}.json"}
        if args.set == "core":
            state["model_in_use"] = model
            state.get("smoke", {}).pop("reserve", None)  # reserve harus diulang bila core diulang
            if model != settings["model_primary"]:
                state["model_fallback_reason"] = (f"smoke core '{settings['model_primary']}' FAIL; PASS dengan fallback "
                                                  f"'{model}' (P1-DG-10) pada {report['checked_at_utc']}")
            else:
                state.pop("model_fallback_reason", None)
    save_state(state)

    logging.info("=" * 60)
    logging.info("HASIL SMOKE %s: %s | model=%s | laporan: reports/smoke_%s.json", args.set.upper(), verdict, model, args.set)
    if verdict == "FAIL":
        if failure_kind == "variable" and model == settings["model_primary"] and args.set == "core":
            logging.info("Variabel kosong/hilang → fallback P1-DG-10: ulangi dengan --model %s (dicatat).", settings["model_fallback"])
        elif failure_kind == "variable":
            logging.info("Variabel reserve tidak tersedia pada model core → BERHENTI, laporkan (decision gate).")
        elif failure_kind == "http":
            logging.info("HTTP error → baca 'reason'; cocokkan api_param dengan open-meteo.com/en/docs/historical-weather-api.")
    return 0 if verdict == "PASS" else 1


# ---------------------------------------------------------------- full
def cmd_full(args) -> int:
    setup_logging("full")
    locs, varcfg, settings = load_configs()
    state = load_state()
    problems = []
    missing = [l["location_id"] for l in locs["locations"] if l["latitude"] is None or l["longitude"] is None]
    if missing:
        problems.append(f"koordinat belum terisi: {missing} (Langkah 2)")
    sm = state.get("smoke", {})
    for s in SETS:
        if sm.get(s, {}).get("verdict") != "PASS":
            problems.append(f"smoke {s} belum PASS (Langkah {'3' if s == 'core' else '4'})")
    model = state.get("model_in_use")
    if not model or {sm.get(s, {}).get("model") for s in SETS} != {model}:
        problems.append(f"model smoke tidak konsisten: model_in_use={model}, smoke={ {s: sm.get(s, {}).get('model') for s in SETS} }")
    if args.refetch and not args.location:
        problems.append("--refetch hanya boleh bersama --location (ambil ulang terbatas, atas izin peneliti)")
    if problems:
        for p in problems:
            logging.error("Gate gagal: %s", p)
        return 1

    start, end = date.fromisoformat(settings["start_date"]), date.fromisoformat(settings["end_date"])
    chunks = year_chunks(start, end)
    sets = [args.set] if args.set else list(SETS)
    targets = [l for l in locs["locations"] if not args.location or l["location_id"] == args.location]
    done = set() if args.refetch else done_chunks()
    todo = [(w, l, s, e) for w in sets for l in targets for s, e in chunks if (w, l["location_id"], str(s.year)) not in done]
    est = sum(request_weight(len(variables_for(varcfg, w)), n_days(s, e)) for w, _, s, e in todo)
    budget = ApiBudget(settings["rate_limit"], log=logging.info)
    logging.info("Model=%s | set=%s | lokasi=%s | chunk/lokasi=%s | sudah selesai=%s | sisa request=%s | estimasi bobot=%.0f "
                 "| terpakai 24 jam=%.0f/%s", model, sets, len(targets), len(chunks), len(done), len(todo), est,
                 budget.used(86400), settings["rate_limit"]["per_day"])

    session = requests.Session()
    n_ok = n_err = 0
    paused = None
    for which, loc, s, e in todo:
        variables = variables_for(varcfg, which)
        weight = request_weight(len(variables), n_days(s, e))
        label = f"{which}:{loc['location_id']}:{s.year}"
        params = build_params(loc, variables, s, e, settings, model)
        try:
            r = fetch(session, settings, params, budget, weight, "full", label)
        except BudgetExhausted as exc:
            paused = exc.resume_at_utc
            logging.warning("Jatah harian habis → berhenti rapi. Jalankan ulang perintah yang sama setelah %s UTC.", paused)
            break
        except requests.RequestException as exc:
            n_err += 1
            append_manifest({"set": which, "location_id": loc["location_id"], "year": s.year, "start_date": s, "end_date": e,
                             "model": model, "http_status": "EXC", "api_weight": round(weight, 3), "error": str(exc)[:300],
                             "collected_at_utc": now_utc()})
            logging.error("%s | koneksi gagal: %s", label, exc)
            continue
        row = {"set": which, "location_id": loc["location_id"], "year": s.year, "start_date": s, "end_date": e,
               "model": model, "request_url": r.url, "http_status": r.status_code, "api_weight": round(weight, 3),
               "collected_at_utc": now_utc()}
        if r.status_code != 200:
            f = write_new(raw_path(which, loc["location_id"], s.year).with_suffix(".err.json"), r.content)
            row.update({"raw_file": rel(f), "raw_sha256": sha256_bytes(r.content), "raw_bytes": len(r.content),
                        "check": "HTTP_ERROR", "error": error_reason(r)})
            append_manifest(row)
            n_err += 1
            logging.error("%s | HTTP %s | %s", label, r.status_code, row["error"])
            continue
        f = write_new(raw_path(which, loc["location_id"], s.year), r.content)  # evidence: byte-identik
        payload = json.loads(r.content)
        summ = summarize(payload, variables)
        issues = chunk_check(payload, summ, s, e, settings, variables)
        row.update({
            "raw_file": rel(f), "raw_sha256": sha256_bytes(r.content), "raw_bytes": len(r.content),
            "grid_latitude": payload.get("latitude"), "grid_longitude": payload.get("longitude"),
            "grid_elevation": payload.get("elevation"), "utc_offset_seconds": payload.get("utc_offset_seconds"),
            "timezone": payload.get("timezone"), "n_days": len(summ["times"]),
            "n_null_values": sum(v["n_null"] or 0 for v in summ["per_var"].values()),
            "check": "OK" if not issues else "STRUCTURE: " + "; ".join(issues),
        })
        append_manifest(row)
        if issues:
            n_err += 1
            logging.error("%s | respons tidak sesuai struktur: %s", label, issues)
        else:
            n_ok += 1
            logging.info("%-26s OK | grid=(%s, %s) elev=%s | null=%s | bobot=%.1f", label, row["grid_latitude"],
                         row["grid_longitude"], row["grid_elevation"], row["n_null_values"], weight)

    done_after = done_chunks()
    expected = {(w, l["location_id"], str(s.year)) for w in SETS for l in locs["locations"] for s, _ in chunks}
    per_set = {w: sum(1 for k in done_after if k[0] == w) for w in SETS}
    complete = expected <= done_after
    summary = {
        "step": "Langkah 5 — full collection", "model": model, "start_date": str(start), "end_date": str(end),
        "n_locations": len(locs["locations"]), "n_chunks_per_location": len(chunks), "expected_chunks": len(expected),
        "completed_chunks_total": len(expected & done_after), "completed_chunks_per_set": per_set,
        "this_run": {"requests_ok": n_ok, "requests_error": n_err, "paused_until_utc": paused},
        "api_weight_used_last_24h": round(budget.used(86400), 1),
        "verdict": "PASS" if complete else ("PAUSED_BUDGET" if paused else "INCOMPLETE"),
        "manifest": rel(MANIFEST), "finished_at_utc": now_utc(),
        "note": "Tanpa imputasi. Null di hari-hari terakhir wajar (jeda ERA5 ±5 hari) — dilaporkan di audit.",
    }
    save_json(RAW / "collection_summary.json", summary)
    logging.info("=" * 60)
    logging.info("HASIL FULL: %s | selesai %s/%s chunk (core=%s, reserve=%s) | run ini OK=%s ERROR=%s",
                 summary["verdict"], summary["completed_chunks_total"], len(expected), per_set["core"], per_set["reserve"], n_ok, n_err)
    if paused:
        logging.info("Lanjutkan setelah %s UTC dengan perintah yang sama (resume otomatis).", paused)
        return EXIT_PAUSED
    if n_err:
        logging.info("Ada error. Jalankan ulang perintah yang sama: chunk sukses di-skip.")
    return 0 if complete else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Collector Open-Meteo ARIF-Net (Langkah 3–5).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sm = sub.add_parser("smoke", help="Langkah 3/4: smoke test")
    sm.add_argument("--set", choices=SETS, required=True)
    sm.add_argument("--model", choices=["era5_seamless", "era5"], default=None,
                    help="Default: model_primary. 'era5' = fallback P1-DG-10.")
    sm.add_argument("--location", default="brebes")
    sm.add_argument("--start", type=date.fromisoformat, default=date(2018, 1, 1))
    sm.add_argument("--end", type=date.fromisoformat, default=date(2018, 1, 31))
    fu = sub.add_parser("full", help="Langkah 5: full collection (resume otomatis)")
    fu.add_argument("--set", choices=SETS, default=None, help="Default: core lalu reserve")
    fu.add_argument("--location", default=None, help="Batasi ke satu lokasi")
    fu.add_argument("--refetch", action="store_true",
                    help="Ambil ulang chunk lokasi tsb (file lama TIDAK ditimpa; versi baru .rN). Wajib --location.")
    args = ap.parse_args()
    return cmd_smoke(args) if args.cmd == "smoke" else cmd_full(args)


if __name__ == "__main__":
    sys.exit(main())
