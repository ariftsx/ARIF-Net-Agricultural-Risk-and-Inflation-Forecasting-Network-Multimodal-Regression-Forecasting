"""Utilitas bersama — ARIF-Net Phase 1 · koleksi harga PIHPS Bank Indonesia.

Satu-satunya tempat parameter request dibangun (build_params) dan nilai harga di-parse
(parse_price). Script lain tidak boleh menyusun parameter sendiri.

Otoritas: Plan v2.0.0 §0.5, §10.1a · Contract v2.1.0 §3.1, §5.6.
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
RAW = ROOT / "data" / "raw" / "pihps"
REFERENCE = RAW / "reference"
SMOKE = RAW / "smoke"
MANIFEST = RAW / "collection_manifest.csv"
PROCESSED = ROOT / "data" / "processed" / "pihps"
ARCHIVE_2022 = ROOT / "archive" / "run_2022" / "data_raw_pihps"
STATE = CONFIG / "state.json"
WIN_MAX_PATH = 259

DATE_KEY_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
MISSING_TOKENS = {"", "-", "null", "none"}


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


def build_params(settings: dict, comcat_id: str, start: date, end: date, cache_buster: int) -> dict:
    """Parameter query GetGridDataKomoditas (sesuai tangkapan DevTools peneliti)."""
    return {
        "price_type_id": settings["price_type_id"],
        "comcat_id": comcat_id,
        "province_id": settings["province_id"],
        "regency_id": settings["regency_id"],
        "showKota": settings["show_kota"],
        "showPasar": settings["show_pasar"],
        "tipe_laporan": settings["tipe_laporan"],
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "_": str(cache_buster),
    }


# ---------------------------------------------------------------- periode
def month_chunks(start: date, end: date) -> list[tuple[date, date]]:
    out, cur = [], start
    while cur <= end:
        nxt = date(cur.year + (cur.month == 12), 1 if cur.month == 12 else cur.month + 1, 1)
        out.append((cur, min(end, nxt - timedelta(days=1))))
        cur = nxt
    return out


def weekdays(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1) if (start + timedelta(days=i)).weekday() < 5]


def raw_path(comcat_id: str, chunk_start: date) -> Path:
    return RAW / comcat_id / f"{chunk_start:%Y-%m}.json"


# ---------------------------------------------------------------- respons PIHPS
def norm_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower().replace("-", " "))


def parse_price(value: Any) -> float | None:
    """'50,000' → 50000.0 ; '-' / '' → None. Koma = pemisah ribuan (format respons PIHPS)."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if text.lower() in MISSING_TOKENS:
        return None
    if not re.fullmatch(r"\d{1,3}(,\d{3})*(\.\d+)?|\d+(\.\d+)?", text):
        raise ValueError(f"format harga tidak dikenal: {text!r}")
    return float(text.replace(",", ""))


def market_rows(payload: Any, market_name: str, level: int) -> list[dict]:
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise ValueError("respons bukan {'data': [...]} ")
    return [r for r in payload["data"] if isinstance(r, dict)
            and str(r.get("level")) == str(level) and norm_text(r.get("name")) == norm_text(market_name)]


def date_items(row: dict) -> list[tuple[date, str]]:
    """Kunci tanggal DD/MM/YYYY → (date, nilai mentah sebagai string)."""
    out = []
    for k, v in row.items():
        if DATE_KEY_RE.match(str(k)):
            out.append((datetime.strptime(k, "%d/%m/%Y").date(), "" if v is None else str(v)))
    return sorted(out)


def longest_pipeline_path(comcat_ids: list[str]) -> Path:
    cid = max(comcat_ids, key=len)
    candidates = [
        raw_path(cid, date(2026, 9, 1)).with_name("2026-09.r9.json"),
        SMOKE / f"{cid}_2019-01.r9.json",
        REFERENCE / "ref_commodity.r9.json",
        PROCESSED / "pihps_kramatjati_long.csv",
        LOGS / f"collect_smoke_{stamp()}.log",
    ]
    return max(candidates, key=lambda p: len(str(p)))
