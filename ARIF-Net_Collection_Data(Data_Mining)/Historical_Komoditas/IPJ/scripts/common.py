"""Utilitas bersama — ARIF-Net Phase 1 · koleksi harga IPJ (Info Pangan Jakarta).

Satu-satunya tempat parameter request dibangun (build_report_params) dan nilai di-parse.
Endpoint: GET {base}/v1/public/report?filterBy=market&Id=<market_id>&yearMonth=YYYY-MM
(tangkapan DevTools peneliti 2026-10-03). Satu request = 1 bulan × semua komoditas pasar.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"
RAW = ROOT / "data" / "raw" / "ipj"
SMOKE = RAW / "smoke"
REFERENCE = RAW / "reference"
MANIFEST = RAW / "collection_manifest.csv"
PROCESSED = ROOT / "data" / "processed" / "ipj"
PIHPS_LONG = ROOT.parent / "PIHPS" / "data" / "processed" / "pihps" / "pihps_kramatjati_long.csv"  # Historical_Komoditas/PIHPS
STATE = CONFIG / "state.json"
WIN_MAX_PATH = 259


# ---------------------------------------------------------------- io
def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_new(path: Path, data: bytes) -> Path:
    """Tulis bytes ke file BARU. Tidak pernah menimpa: bila nama dipakai → <stem>.r2<suffix>, r3, …"""
    path.parent.mkdir(parents=True, exist_ok=True)
    target, n = path, 1
    while target.exists():
        n += 1
        target = path.with_name(f"{path.stem}.r{n}{path.suffix}")
    with target.open("xb") as fh:
        fh.write(data)
    return target


# ---------------------------------------------------------------- config
def load_configs() -> tuple[dict, dict]:
    return load_json(CONFIG / "commodities.json"), load_json(CONFIG / "request_settings.json")


def load_state() -> dict:
    return load_json(STATE) if STATE.exists() else {}


def save_state(state: dict) -> None:
    state["updated_at_utc"] = now_utc()
    save_json(STATE, state)


def build_report_params(settings: dict, year_month: str) -> dict:
    return {"filterBy": settings["filter_by"], "Id": settings["market_id"], "yearMonth": year_month}


# ---------------------------------------------------------------- periode & parsing
def months(start: str, end: str) -> list[str]:
    y, m = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    out = []
    while (y, m) <= (ey, em):
        out.append(f"{y}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def month_bounds(year_month: str) -> tuple[date, date]:
    y, m = map(int, year_month.split("-"))
    start = date(y, m, 1)
    end = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
    return start, date.fromordinal(end.toordinal() - 1)


def raw_path(year_month: str) -> Path:
    return RAW / f"{year_month}.json"


def parse_value(value: Any) -> float | None:
    """Nilai harga IPJ berupa angka JSON. None/'' → None. 0 diperlakukan sebagai tidak dilaporkan (dicatat di audit)."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError(f"nilai boolean tidak valid: {value!r}")
    if isinstance(value, (int, float)):
        return None if value == 0 else float(value)
    text = str(value).strip().replace(",", "")
    try:
        v = float(text)
    except ValueError as exc:
        raise ValueError(f"format nilai tidak dikenal: {value!r}") from exc
    return None if v == 0 else v


def report_rows(payload: Any) -> list[dict]:
    if not isinstance(payload, dict) or payload.get("status") != 200:
        raise ValueError(f"status respons bukan 200: {payload.get('status') if isinstance(payload, dict) else type(payload)}")
    inner = payload.get("data")
    rows = inner.get("data") if isinstance(inner, dict) else None
    if not isinstance(rows, list):
        raise ValueError("respons tanpa data.data[]")
    return rows


def longest_pipeline_path() -> Path:
    candidates = [RAW / "2026-09.r9.json", SMOKE / "2024-01.r9.json", REFERENCE / "market_kramat.r9.json",
                  PROCESSED / "ipj_kramatjati_long.csv", LOGS / f"collect_smoke_{stamp()}.log"]
    return max(candidates, key=lambda p: len(str(p)))
