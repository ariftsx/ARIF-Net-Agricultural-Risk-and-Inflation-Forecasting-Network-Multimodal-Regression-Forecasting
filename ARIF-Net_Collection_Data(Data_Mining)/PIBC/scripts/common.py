"""Utilitas bersama — ARIF-Net Phase 1 · koleksi harga beras PIBC (Pasar Induk Beras Cipinang).

Satu-satunya tempat parameter request dibangun (build_params) dan nilai di-parse
(parse_tgl, parse_price). Script lain tidak boleh menyusun parameter sendiri.

Semantik tanggal endpoint (terverifikasi probe 2026-10-03): start_date EKSKLUSIF,
end_date INKLUSIF → untuk rentang [S, E] dikirim start_date = S − 1 hari.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"
RAW = ROOT / "data" / "raw" / "pibc"
SMOKE = RAW / "smoke"
MANIFEST = RAW / "collection_manifest.csv"
PROCESSED = ROOT / "data" / "processed" / "pibc"
PIHPS_LONG = ROOT.parent / "Historical_Komoditas" / "data" / "processed" / "pihps" / "pihps_kramatjati_long.csv"
STATE = CONFIG / "state.json"
WIN_MAX_PATH = 259
TGL_RE = re.compile(r"^\d{4} \d{2} \d{2}$")


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
    return load_json(CONFIG / "varieties.json"), load_json(CONFIG / "request_settings.json")


def load_state() -> dict:
    return load_json(STATE) if STATE.exists() else {}


def save_state(state: dict) -> None:
    state["updated_at_utc"] = now_utc()
    save_json(STATE, state)


def build_params(settings: dict, start: date, end: date, offset: int, cache_buster: int) -> dict:
    """Parameter DataTables /rice-price-detail untuk rentang INKLUSIF [start, end]."""
    p: dict[str, Any] = {
        "start_date": (start - timedelta(days=1)).isoformat(),  # server: start_date eksklusif
        "end_date": end.isoformat(),
        "draw": 1,
    }
    for i, col in enumerate(settings["columns"]):
        p.update({f"columns[{i}][data]": col, f"columns[{i}][name]": "", f"columns[{i}][searchable]": "true",
                  f"columns[{i}][orderable]": "true", f"columns[{i}][search][value]": "",
                  f"columns[{i}][search][regex]": "false"})
    p.update({"order[0][column]": 0, "order[0][dir]": "asc", "start": offset, "length": settings["page_length"],
              "search[value]": "", "search[regex]": "false", "_": str(cache_buster)})
    return p


# ---------------------------------------------------------------- periode & parsing
def year_chunks(start: date, end: date) -> list[tuple[date, date]]:
    return [(max(start, date(y, 1, 1)), min(end, date(y, 12, 31))) for y in range(start.year, end.year + 1)]


def n_days(start: date, end: date) -> int:
    return (end - start).days + 1


def raw_path(chunk_start: date) -> Path:
    return RAW / f"{chunk_start.year}.json"


def parse_tgl(value: str) -> date:
    if not TGL_RE.match(str(value)):
        raise ValueError(f"format tgl tidak dikenal: {value!r}")
    return datetime.strptime(value, "%Y %m %d").date()


def parse_price(value: Any) -> float | None:
    """'13,325' → 13325.0 ; '' / '-' / None → None. Koma = pemisah ribuan."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if text.lower() in {"", "-", "null", "none"}:
        return None
    if not re.fullmatch(r"\d{1,3}(,\d{3})*(\.\d+)?|\d+(\.\d+)?", text):
        raise ValueError(f"format harga tidak dikenal: {text!r}")
    return float(text.replace(",", ""))


def longest_pipeline_path() -> Path:
    candidates = [RAW / "2025.r9.json", SMOKE / "2019-01.r9.json", PROCESSED / "pibc_medium_i_long.csv",
                  LOGS / f"collect_smoke_{stamp()}.log", REPORTS / "mapping_evidence.json"]
    return max(candidates, key=lambda p: len(str(p)))
