#!/usr/bin/env python3
"""
ARIF-Net — PIHPS Price Data Collector

Collects historical PIHPS market-price data for the requested 12 commodities
at Pasar Kramatjati, using the PIHPS backend JSON endpoint discovered from
browser DevTools.

Research period (default): 2022-01-01 .. 2026-09-29

The collector:
1. Warms up a requests.Session on the PIHPS page.
2. Discovers commodity IDs using PIHPS's reference endpoint when possible.
3. Requests data in bounded date chunks (monthly by default).
4. Saves every raw JSON response (immutable raw evidence).
5. Extracts only the level=3 row named "Pasar Kramatjati".
6. Converts PIHPS wide date columns into long rows.
7. Writes normalized CSV + collection manifest + coverage/missingness reports.

IMPORTANT:
- No cookie, XSRF token, or hard-coded session token is embedded.
- If the public endpoint requires session state, the warm-up request is used
  to obtain fresh cookies in-memory.
- Commodity IDs are NOT guessed. If auto-discovery fails, the script stops
  and writes the reference response for manual verification.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable

import requests


BASE = "https://www.bi.go.id/hargapangan"
PAGE_URL = f"{BASE}/TabelHarga/PasarTradisionalKomoditas"
DATA_URL = f"{BASE}/WebSite/TabelHarga/GetGridDataKomoditas"
REFERENCE_URL = f"{BASE}/WebSite/TabelHarga/GetRefCommodityAndCategory"

DEFAULT_START = date(2022, 1, 1)
DEFAULT_END = date(2026, 9, 29)
DEFAULT_CHUNK_MONTHS = 1
DEFAULT_DELAY = 0.50
DEFAULT_TIMEOUT = 45
DEFAULT_RETRIES = 4

PRICE_TYPE_ID = 1
PROVINCE_ID = 13
REGENCY_ID = 34
SHOW_KOTA = "true"
SHOW_PASAR = "true"
TIPE_LAPORAN = 1
MARKET_NAME = "Pasar Kramatjati"
MARKET_LEVEL = 3

REQUESTED_COMMODITIES = [
    "Beras Kualitas Bawah I",
    "Beras Kualitas Bawah II",
    "Beras Kualitas Medium I",
    "Beras Kualitas Medium II",
    "Beras Kualitas Super I",
    "Beras Kualitas Super II",
    "Bawang Merah Ukuran Sedang",
    "Bawang Putih Ukuran Sedang",
    "Cabai Merah Besar",
    "Cabai Merah Keriting",
    "Cabai Rawit Hijau",
    "Cabai Rawit Merah",
]

# IDs directly verified from the user's browser capture.
# Other IDs are intentionally discovered at runtime rather than guessed.
KNOWN_COMMODITY_IDS = {
    "Cabai Merah Keriting": "com_14",
    "Bawang Merah Ukuran Sedang": "com_11",
}

DATE_FIELD_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")


@dataclass
class CommodityConfig:
    name: str
    comcat_id: str


@dataclass
class CollectionRecord:
    commodity: str
    comcat_id: str
    source: str
    source_url: str
    collection_method: str
    price_type_id: int
    province_id: int
    regency_id: int
    market: str
    market_level: int
    start_date: str
    end_date: str
    raw_file: str
    raw_sha256: str
    http_status: int
    observed_rows: int
    collected_at_utc: str


class PIHPSCollectorError(RuntimeError):
    pass


def setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Tanggal harus YYYY-MM-DD, diterima: {value}"
        ) from exc


def month_end(d: date) -> date:
    next_month = date(d.year + (d.month == 12), 1 if d.month == 12 else d.month + 1, 1)
    return next_month - timedelta(days=1)


def add_months(first: date, months: int) -> date:
    zero = first.year * 12 + first.month - 1 + months
    year = zero // 12
    month = zero % 12 + 1
    return date(year, month, 1)


def iter_chunks(start: date, end: date, chunk_months: int) -> Iterable[tuple[date, date]]:
    cursor = start
    while cursor <= end:
        chunk_start = cursor
        candidate = add_months(chunk_start, chunk_months)
        chunk_end = min(end, candidate - timedelta(days=1))
        yield chunk_start, chunk_end
        cursor = chunk_end + timedelta(days=1)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def normalized_text(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("-", " ")
    value = re.sub(r"\s+", " ", value)
    return value


def parse_price(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if text in {"", "-", "null", "None"}:
        return None

    # PIHPS values observed in the captured response use comma thousands
    # separators, e.g. "50,000". We remove non-digits rather than applying
    # locale-dependent float parsing.
    digits = re.sub(r"[^0-9]", "", text)
    if not digits:
        return None
    return float(digits)


def extract_json_rows(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        raise PIHPSCollectorError("Response JSON bukan object/dict.")
    rows = payload.get("data")
    if not isinstance(rows, list):
        raise PIHPSCollectorError(
            f"Response tidak memiliki field data[] yang valid. Keys={list(payload.keys())[:20]}"
        )
    return [row for row in rows if isinstance(row, dict)]


def find_market_row(rows: list[dict[str, Any]], market_name: str) -> dict[str, Any]:
    target = normalized_text(market_name)
    matches = [
        row
        for row in rows
        if int(row.get("level", -1)) == MARKET_LEVEL
        and normalized_text(str(row.get("name", ""))) == target
    ]

    if not matches:
        available = [
            {"level": row.get("level"), "name": row.get("name")}
            for row in rows
            if str(row.get("name", "")).strip()
        ]
        sample = available[:30]
        raise PIHPSCollectorError(
            f"Market '{market_name}' level={MARKET_LEVEL} tidak ditemukan. Sample rows: {sample}"
        )

    if len(matches) > 1:
        raise PIHPSCollectorError(
            f"Market '{market_name}' ditemukan lebih dari satu row: {len(matches)}."
        )
    return matches[0]


def iter_date_values(row: dict[str, Any]) -> Iterable[tuple[str, float | None]]:
    for key, value in row.items():
        if not DATE_FIELD_RE.match(str(key)):
            continue
        yield str(key), parse_price(value)


def parse_pihps_row(
    row: dict[str, Any],
    commodity: CommodityConfig,
    chunk_start: date,
    chunk_end: date,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for date_text, price in iter_date_values(row):
        dt = datetime.strptime(date_text, "%d/%m/%Y").date()
        if not (chunk_start <= dt <= chunk_end):
            continue
        out.append(
            {
                "date": dt.isoformat(),
                "commodity": commodity.name,
                "comcat_id": commodity.comcat_id,
                "market": row.get("name"),
                "market_level": row.get("level"),
                "price_rp_per_kg": price,
                "source": "PIHPS Bank Indonesia",
                "source_url": DATA_URL,
                "collection_method": "PIHPS backend JSON GET",
                "price_type_id": PRICE_TYPE_ID,
                "province_id": PROVINCE_ID,
                "regency_id": REGENCY_ID,
                "tipe_laporan": TIPE_LAPORAN,
            }
        )
    return out


def request_json(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
) -> tuple[dict[str, Any], int]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, params=params, timeout=timeout)
            logging.debug("GET %s -> %s", response.url, response.status_code)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise PIHPSCollectorError("JSON response bukan object.")
            return payload, response.status_code
        except (requests.RequestException, ValueError, PIHPSCollectorError) as exc:
            last_error = exc
            if attempt == retries:
                break
            sleep_for = min(2 ** (attempt - 1), 8)
            logging.warning(
                "Request gagal (attempt %s/%s): %s | retry %ss",
                attempt,
                retries,
                exc,
                sleep_for,
            )
            time.sleep(sleep_for)

    raise PIHPSCollectorError(f"Request gagal setelah {retries} percobaan: {last_error}")


def warmup_session(session: requests.Session) -> None:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": BASE,
    }
    session.headers.update(headers)
    logging.info("Warm-up PIHPS page: %s", PAGE_URL)
    response = session.get(PAGE_URL, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    logging.info("Warm-up OK | cookies=%s", list(session.cookies.keys()))

    # Optional anti-forgery token header. Do not hard-code or persist it.
    xsrf = session.cookies.get("XSRF-TOKEN")
    if xsrf:
        session.headers["XSRF-TOKEN"] = xsrf

    session.headers.update(
        {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": PAGE_URL,
        }
    )


def collect_reference_payload(session: requests.Session) -> dict[str, Any]:
    attempts = [
        ({"_": str(int(time.time() * 1000))}),
        ({"price_type_id": PRICE_TYPE_ID, "_": str(int(time.time() * 1000))}),
        ({},),
    ]

    last_error: Exception | None = None
    for packed in attempts:
        params = packed[0] if isinstance(packed, tuple) else packed
        try:
            payload, _ = request_json(session, REFERENCE_URL, params=params)
            return payload
        except Exception as exc:  # noqa: BLE001 - discovery fallback chain
            last_error = exc
            logging.debug("Reference discovery attempt gagal: %s", exc)

    raise PIHPSCollectorError(f"Tidak dapat mengambil commodity reference: {last_error}")


def candidate_id_fields(d: dict[str, Any]) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    for key, value in d.items():
        if not isinstance(value, (str, int)):
            continue
        s = str(value).strip()
        k = str(key).lower()
        if not s:
            continue
        if "id" in k and ("com" in k or k in {"id", "value", "code"}):
            candidates.append((str(key), s))
    return candidates


def discover_ids_recursive(payload: Any, target_names: set[str]) -> dict[str, str]:
    """Best-effort flexible discovery across likely PIHPS reference shapes."""
    found: dict[str, str] = {}

    def walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return

        text_fields = []
        for key, value in node.items():
            if isinstance(value, str):
                norm = normalized_text(value)
                if norm in target_names:
                    text_fields.append(norm)

        ids = candidate_id_fields(node)
        if text_fields and ids:
            # Prefer the most commodity-looking ID field.
            chosen = sorted(ids, key=lambda kv: ("com" not in kv[0].lower(), len(kv[0])))[0][1]
            for name in text_fields:
                found.setdefault(name, chosen)

        # Handle simple map shape like {"com_14": "Cabai Merah Keriting"}
        for key, value in node.items():
            if isinstance(key, str) and isinstance(value, str):
                if normalized_text(value) in target_names and ("com" in key.lower() or key.lower().startswith("cat")):
                    found.setdefault(normalized_text(value), key)

        for value in node.values():
            walk(value)

    walk(payload)
    return found


def load_manual_commodity_mapping(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PIHPSCollectorError(f"Commodity mapping JSON tidak valid: {path} | {exc}") from exc
    if not isinstance(payload, dict):
        raise PIHPSCollectorError(f"Commodity mapping harus object/dict: {path}")
    result: dict[str, str] = {}
    for name, cid in payload.items():
        if cid is None or str(cid).strip() == "":
            continue
        result[normalized_text(str(name))] = str(cid).strip()
    return result


def resolve_commodity_configs(
    session: requests.Session,
    requested_names: list[str],
    out_dir: Path,
) -> list[CommodityConfig]:
    target_norm = {normalized_text(x) for x in requested_names}
    payload: dict[str, Any] | None = None

    try:
        payload = collect_reference_payload(session)
        debug_path = out_dir / "reference_commodity_response.json"
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        debug_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        logging.info("Commodity reference disimpan: %s", debug_path)
    except Exception as exc:  # noqa: BLE001
        logging.warning("Auto-discovery reference gagal: %s", exc)

    discovered = discover_ids_recursive(payload, target_norm) if payload else {}

    configs: list[CommodityConfig] = []
    unresolved: list[str] = []
    for name in requested_names:
        norm = normalized_text(name)
        cid = discovered.get(norm)
        if cid is None:
            # Exact verified IDs from the user's browser capture; these are safe fallbacks.
            if name == "Cabai Merah Keriting":
                cid = KNOWN_COMMODITY_IDS["Cabai Merah Keriting"]
            elif name == "Bawang Merah Ukuran Sedang":
                cid = KNOWN_COMMODITY_IDS["Bawang Merah Ukuran Sedang"]
            else:
                unresolved.append(name)
                continue
        configs.append(CommodityConfig(name=name, comcat_id=cid))

    if unresolved:
        mapping_path = out_dir / "commodity_id_mapping_REQUIRED.json"
        payload = {
            "requested": requested_names,
            "resolved": {cfg.name: cfg.comcat_id for cfg in configs},
            "unresolved": unresolved,
            "instruction": (
                "Isi comcat_id yang terverifikasi dari PIHPS DevTools/response reference. "
                "Jangan menebak ID."
            ),
        }
        mapping_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        raise PIHPSCollectorError(
            "Sebagian comcat_id belum berhasil didiscover. "
            f"Daftar: {unresolved}. File diagnostik: {mapping_path}"
        )

    configs.sort(key=lambda x: requested_names.index(x.name))
    resolved_path = out_dir / "commodity_id_mapping.json"
    resolved_path.write_text(
        json.dumps({cfg.name: cfg.comcat_id for cfg in configs}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logging.info("Commodity ID map disimpan: %s", resolved_path)
    return configs


def build_data_params(commodity: CommodityConfig, start: date, end: date) -> dict[str, Any]:
    return {
        "price_type_id": PRICE_TYPE_ID,
        "comcat_id": commodity.comcat_id,
        "province_id": PROVINCE_ID,
        "regency_id": REGENCY_ID,
        "showKota": SHOW_KOTA,
        "showPasar": SHOW_PASAR,
        "tipe_laporan": TIPE_LAPORAN,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "_": str(int(time.time() * 1000)),
    }


def append_csv_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "date",
        "commodity",
        "comcat_id",
        "market",
        "market_level",
        "price_rp_per_kg",
        "source",
        "source_url",
        "collection_method",
        "price_type_id",
        "province_id",
        "regency_id",
        "tipe_laporan",
    ]
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def append_manifest(path: Path, record: CollectionRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    fieldnames = list(asdict(record).keys())
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(asdict(record))


def deduplicate_csv(source: Path, destination: Path) -> int:
    seen: set[tuple[str, str, str]] = set()
    rows: list[dict[str, Any]] = []
    with source.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        for row in reader:
            key = (row["date"], row["commodity"], row["market"])
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)

    rows.sort(key=lambda r: (r["commodity"], r["date"]))
    with destination.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def generate_coverage_report(
    normalized_csv: Path,
    out_path: Path,
    start: date,
    end: date,
) -> None:
    by_commodity: dict[str, set[date]] = {}
    values: dict[str, list[float]] = {}
    with normalized_csv.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            c = row["commodity"]
            dt = datetime.strptime(row["date"], "%Y-%m-%d").date()
            by_commodity.setdefault(c, set()).add(dt)
            if row["price_rp_per_kg"] not in {"", "None", "null"}:
                try:
                    values.setdefault(c, []).append(float(row["price_rp_per_kg"]))
                except ValueError:
                    pass

    expected_weekdays: list[date] = []
    cursor = start
    while cursor <= end:
        if cursor.weekday() < 5:
            expected_weekdays.append(cursor)
        cursor += timedelta(days=1)

    fieldnames = [
        "commodity",
        "start_date",
        "end_date",
        "observed_dates",
        "expected_weekdays",
        "weekday_coverage_pct",
        "missing_weekdays",
        "first_observed",
        "last_observed",
        "non_missing_price_count",
        "min_price_rp_per_kg",
        "max_price_rp_per_kg",
        "median_not_calculated",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for commodity in sorted(by_commodity):
            observed = by_commodity[commodity]
            missing = [d for d in expected_weekdays if d not in observed]
            numeric = sorted(values.get(commodity, []))
            writer.writerow(
                {
                    "commodity": commodity,
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat(),
                    "observed_dates": len(observed),
                    "expected_weekdays": len(expected_weekdays),
                    "weekday_coverage_pct": round(
                        100 * len(observed.intersection(expected_weekdays)) / len(expected_weekdays), 2
                    )
                    if expected_weekdays
                    else 0.0,
                    "missing_weekdays": len(missing),
                    "first_observed": min(observed).isoformat() if observed else "",
                    "last_observed": max(observed).isoformat() if observed else "",
                    "non_missing_price_count": len(numeric),
                    "min_price_rp_per_kg": min(numeric) if numeric else "",
                    "max_price_rp_per_kg": max(numeric) if numeric else "",
                    "median_not_calculated": "see Phase 1 audit",
                }
            )


def generate_missing_dates(
    normalized_csv: Path,
    out_path: Path,
    start: date,
    end: date,
) -> None:
    by_commodity: dict[str, set[date]] = {}
    with normalized_csv.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            c = row["commodity"]
            dt = datetime.strptime(row["date"], "%Y-%m-%d").date()
            by_commodity.setdefault(c, set()).add(dt)

    fieldnames = ["commodity", "missing_weekday", "reason"]
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for commodity in sorted(by_commodity):
            observed = by_commodity[commodity]
            cursor = start
            while cursor <= end:
                if cursor.weekday() < 5 and cursor not in observed:
                    writer.writerow(
                        {
                            "commodity": commodity,
                            "missing_weekday": cursor.isoformat(),
                            "reason": "not returned by PIHPS for selected market/time window; do not auto-impute",
                        }
                    )
                cursor += timedelta(days=1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect PIHPS historical price data for ARIF-Net commodities at Pasar Kramatjati."
    )
    parser.add_argument("--start-date", type=parse_date, default=DEFAULT_START)
    parser.add_argument("--end-date", type=parse_date, default=DEFAULT_END)
    parser.add_argument("--chunk-months", type=int, default=DEFAULT_CHUNK_MONTHS)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument("--out-dir", type=Path, default=Path("data/raw/pihps"))
    parser.add_argument("--limit-commodities", type=int, default=None)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--skip-reference-discovery", action="store_true")
    parser.add_argument("--commodity-map", type=Path, default=Path("config/commodity_ids.json"))
    args = parser.parse_args()

    setup_logging(args.verbose)

    if args.start_date > args.end_date:
        parser.error("--start-date tidak boleh lebih besar dari --end-date")
    if args.chunk_months < 1 or args.chunk_months > 12:
        parser.error("--chunk-months harus 1..12")
    if args.delay < 0:
        parser.error("--delay tidak boleh negatif")

    out_dir: Path = args.out_dir
    raw_dir = out_dir / "raw_json"
    normalized_tmp = out_dir / "price_long_unsorted.csv"
    normalized_final = out_dir / "pihps_price_kramatjati_long.csv"
    manifest_path = out_dir / "collection_manifest.csv"
    coverage_path = out_dir / "coverage_report.csv"
    missing_path = out_dir / "missing_weekdays.csv"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    requested = REQUESTED_COMMODITIES[: args.limit_commodities] if args.limit_commodities else REQUESTED_COMMODITIES

    session = requests.Session()
    try:
        warmup_session(session)
    except requests.RequestException as exc:
        logging.error("Warm-up PIHPS gagal: %s", exc)
        return 2

    try:
        if args.skip_reference_discovery:
            manual_map = load_manual_commodity_mapping(args.commodity_map)
            configs = []
            unresolved: list[str] = []
            for name in requested:
                cid = manual_map.get(normalized_text(name))
                if cid is None:
                    cid = KNOWN_COMMODITY_IDS.get(name)
                if cid is None:
                    unresolved.append(name)
                    continue
                configs.append(CommodityConfig(name, cid))
            if unresolved:
                raise PIHPSCollectorError(
                    f"--skip-reference-discovery: comcat_id belum tersedia untuk {unresolved}. "
                    f"Isi {args.commodity_map} dari hasil DevTools PIHPS."
                )
        else:
            configs = resolve_commodity_configs(session, requested, out_dir)
    except PIHPSCollectorError as exc:
        logging.error("Commodity ID resolution gagal: %s", exc)
        return 3

    logging.info("Commodity yang akan dikoleksi: %s", [c.name for c in configs])
    logging.info(
        "Range: %s → %s | chunk=%s bulan | market=%s",
        args.start_date,
        args.end_date,
        args.chunk_months,
        MARKET_NAME,
    )

    # Start clean for a reproducible collection run.
    for path in (normalized_tmp, normalized_final, manifest_path, coverage_path, missing_path):
        if path.exists():
            path.unlink()

    total_rows = 0
    total_requests = 0

    for commodity in configs:
        commodity_dir = raw_dir / re.sub(r"[^a-z0-9]+", "_", commodity.name.lower()).strip("_")
        commodity_dir.mkdir(parents=True, exist_ok=True)

        for chunk_start, chunk_end in iter_chunks(args.start_date, args.end_date, args.chunk_months):
            total_requests += 1
            params = build_data_params(commodity, chunk_start, chunk_end)
            logging.info(
                "Collect %s | %s → %s | comcat=%s",
                commodity.name,
                chunk_start,
                chunk_end,
                commodity.comcat_id,
            )

            try:
                payload, status_code = request_json(
                    session,
                    DATA_URL,
                    params=params,
                    timeout=args.timeout,
                    retries=args.retries,
                )
                rows = extract_json_rows(payload)
                market_row = find_market_row(rows, MARKET_NAME)
                parsed_rows = parse_pihps_row(market_row, commodity, chunk_start, chunk_end)

                raw_name = f"{chunk_start.isoformat()}_{chunk_end.isoformat()}.json"
                raw_path = commodity_dir / raw_name
                raw_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
                raw_hash = sha256_file(raw_path)

                append_csv_rows(normalized_tmp, parsed_rows)
                total_rows += len(parsed_rows)

                append_manifest(
                    manifest_path,
                    CollectionRecord(
                        commodity=commodity.name,
                        comcat_id=commodity.comcat_id,
                        source="PIHPS Bank Indonesia",
                        source_url=DATA_URL,
                        collection_method="PIHPS backend JSON GET",
                        price_type_id=PRICE_TYPE_ID,
                        province_id=PROVINCE_ID,
                        regency_id=REGENCY_ID,
                        market=MARKET_NAME,
                        market_level=MARKET_LEVEL,
                        start_date=chunk_start.isoformat(),
                        end_date=chunk_end.isoformat(),
                        raw_file=str(raw_path.as_posix()),
                        raw_sha256=raw_hash,
                        http_status=status_code,
                        observed_rows=len(parsed_rows),
                        collected_at_utc=datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                    ),
                )
                logging.info("  -> %s observations | raw=%s", len(parsed_rows), raw_path)

            except PIHPSCollectorError as exc:
                error_dir = out_dir / "errors"
                error_dir.mkdir(parents=True, exist_ok=True)
                error_path = error_dir / (
                    f"{re.sub(r'[^a-z0-9]+','_',commodity.name.lower()).strip('_')}"
                    f"_{chunk_start.isoformat()}_{chunk_end.isoformat()}.txt"
                )
                error_path.write_text(str(exc), encoding="utf-8")
                logging.error("Chunk gagal: %s", exc)

            time.sleep(args.delay)

    if not normalized_tmp.exists():
        logging.error("Tidak ada row hasil collection yang tersimpan.")
        return 4

    unique_count = deduplicate_csv(normalized_tmp, normalized_final)
    generate_coverage_report(normalized_final, coverage_path, args.start_date, args.end_date)
    generate_missing_dates(normalized_final, missing_path, args.start_date, args.end_date)

    summary = {
        "project": "ARIF-Net",
        "source": "PIHPS Bank Indonesia",
        "collection_method": "backend JSON GET",
        "market": MARKET_NAME,
        "market_level": MARKET_LEVEL,
        "price_type_id": PRICE_TYPE_ID,
        "province_id": PROVINCE_ID,
        "regency_id": REGENCY_ID,
        "start_date": args.start_date.isoformat(),
        "end_date": args.end_date.isoformat(),
        "commodities": [asdict(c) for c in configs],
        "requests_attempted": total_requests,
        "raw_observations_before_dedup": total_rows,
        "normalized_unique_rows": unique_count,
        "files": {
            "normalized": str(normalized_final.as_posix()),
            "manifest": str(manifest_path.as_posix()),
            "coverage": str(coverage_path.as_posix()),
            "missing_weekdays": str(missing_path.as_posix()),
        },
        "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "note": "Missing dates are reported, not imputed. Review them in Phase 1 temporal audit.",
    }
    summary_path = out_dir / "collection_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # Keep unsorted intermediate only as optional audit artifact; users can remove it after review.
    logging.info("Selesai.")
    logging.info("Requests attempted : %s", total_requests)
    logging.info("Raw observations   : %s", total_rows)
    logging.info("Unique rows         : %s", unique_count)
    logging.info("Normalized CSV      : %s", normalized_final)
    logging.info("Coverage report     : %s", coverage_path)
    logging.info("Missing report      : %s", missing_path)
    logging.info("Summary             : %s", summary_path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nDihentikan oleh pengguna.", file=sys.stderr)
        raise SystemExit(130)
