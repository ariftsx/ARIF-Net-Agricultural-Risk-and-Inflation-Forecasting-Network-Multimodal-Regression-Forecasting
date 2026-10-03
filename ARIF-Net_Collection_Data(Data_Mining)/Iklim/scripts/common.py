"""Utilitas bersama — ARIF-Net Phase 1 · koleksi iklim Open-Meteo.

Satu-satunya tempat URL/parameter request dibangun (build_params). Script lain
tidak boleh menyusun parameter sendiri.

Otoritas: Plan v2.0.0 §0.5, §10.2a · Contract v2.1.0 §0B, §5.6.
"""
from __future__ import annotations

import csv
import hashlib
import json
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"
RAW = ROOT / "data" / "raw" / "openmeteo"
SMOKE = RAW / "smoke"
MANIFEST = RAW / "collection_manifest.csv"
PROCESSED = ROOT / "data" / "processed" / "openmeteo"
BOUNDARIES = ROOT / "data" / "external" / "boundaries"
STATE = CONFIG / "state.json"
LEDGER = LOGS / "api_ledger.csv"

SETS = ("core", "reserve")
WIN_MAX_PATH = 259  # MAX_PATH 260 termasuk NUL

# Unit yang DIKUNCI P1-DG-15 → smoke test FAIL bila berbeda.
LOCKED_UNITS = {"°C", "mm", "m/s"}


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
def load_configs() -> tuple[dict, dict, dict]:
    return (
        load_json(CONFIG / "locations.json"),
        load_json(CONFIG / "variables.json"),
        load_json(CONFIG / "request_settings.json"),
    )


def load_state() -> dict:
    return load_json(STATE) if STATE.exists() else {"smoke": {}, "model_in_use": None}


def save_state(state: dict) -> None:
    state["updated_at_utc"] = now_utc()
    save_json(STATE, state)


def variables_for(varcfg: dict, which: str) -> list[str]:
    return [v["api_param"] for v in varcfg[which]]


def allowed_models(settings: dict) -> tuple[str, str]:
    return settings["model_primary"], settings["model_fallback"]


def build_params(loc: dict, variables: list[str], start: date | str, end: date | str,
                 settings: dict, model: str) -> dict:
    """Parameter query string Historical Weather API (GET /v1/archive).

    Tidak mengirim: hourly, elevation (default DEM 90 m), apikey, format.
    """
    if model not in allowed_models(settings):
        raise ValueError(f"model '{model}' tidak diizinkan (P1-DG-10): hanya {allowed_models(settings)}")
    if loc.get("latitude") is None or loc.get("longitude") is None:
        raise ValueError(f"koordinat '{loc.get('location_id')}' belum diisi (Langkah 2)")
    return {
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
        "start_date": str(start),
        "end_date": str(end),
        "daily": ",".join(variables),
        "models": model,
        "temperature_unit": settings["temperature_unit"],
        "wind_speed_unit": settings["wind_speed_unit"],
        "precipitation_unit": settings["precipitation_unit"],
        "timeformat": settings["timeformat"],
        "timezone": settings["timezone"],
        "cell_selection": settings["cell_selection"],
    }


# ---------------------------------------------------------------- response
def _lookup(block: dict, var: str):
    """Ambil kunci var; toleran terhadap suffix nama model (mis. var_era5_seamless)."""
    if var in block:
        return block[var]
    for key, val in block.items():
        if key.startswith(var + "_") and key[len(var) + 1:].startswith("era5"):
            return val
    return None


def daily_series(payload: dict, var: str) -> list | None:
    return _lookup(payload.get("daily") or {}, var)


def daily_unit(payload: dict, var: str) -> str | None:
    return _lookup(payload.get("daily_units") or {}, var)


# ---------------------------------------------------------------- periode
def year_chunks(start: date, end: date) -> list[tuple[date, date]]:
    return [(max(start, date(y, 1, 1)), min(end, date(y, 12, 31))) for y in range(start.year, end.year + 1)]


def raw_path(which: str, location_id: str, year: int) -> Path:
    return RAW / which / location_id / f"{year}.json"


def longest_pipeline_path(location_ids: list[str], years: list[int]) -> Path:
    loc = max(location_ids, key=len)
    candidates = [
        raw_path("reserve", loc, max(years)).with_name(f"{max(years)}.r9.json"),
        SMOKE / "reserve_era5_seamless_brebes.r9.json",
        PROCESSED / "climate_reserve_long.csv",
        LOGS / f"collect_smoke_reserve_{stamp()}.log",
        REPORTS / "audit_reserve_completeness.csv",
    ]
    return max(candidates, key=lambda p: len(str(p)))


# ---------------------------------------------------------------- kuota API
def request_weight(n_vars: int, n_days: int) -> float:
    """Bobot 'API call' Open-Meteo (open-meteo.com/en/pricing): >10 variabel atau >14 hari
    dihitung pecahan. Contoh resmi: 14 hari × 15 variabel = 1.5 call."""
    return max(1.0, n_vars / 10) * max(1.0, n_days / 14)


class BudgetExhausted(Exception):
    def __init__(self, resume_at_utc: str, used: float, limit: float):
        super().__init__(f"jatah harian habis ({used:.0f}/{limit:.0f}); lanjutkan setelah {resume_at_utc}")
        self.resume_at_utc = resume_at_utc


class ApiBudget:
    """Rate limiter berbobot dengan ledger persisten (logs/api_ledger.csv).

    Ledger mencatat setiap request (termasuk yang gagal) sehingga jatah menit/jam/hari
    tetap dihitung benar walau script dijalankan ulang.
    """
    FIELDS = ["epoch", "utc", "weight", "kind", "label", "http_status"]

    def __init__(self, limits: dict, ledger: Path = LEDGER,
                 clock: Callable[[], float] = time.time, sleep: Callable[[float], None] = time.sleep,
                 log: Callable[[str], None] = print):
        self.limits = {60: float(limits["per_minute"]), 3600: float(limits["per_hour"]), 86400: float(limits["per_day"])}
        self.ledger, self.clock, self.sleep, self.log = ledger, clock, sleep, log
        self.entries: list[tuple[float, float]] = []
        if ledger.exists():
            with ledger.open(encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    self.entries.append((float(r["epoch"]), float(r["weight"])))

    def used(self, window: int) -> float:
        t = self.clock()
        return sum(w for e, w in self.entries if t - e < window)

    def _free_at(self, window: int, weight: float) -> float:
        """Epoch paling awal ketika (pemakaian window + weight) ≤ limit."""
        t, limit = self.clock(), self.limits[window]
        inside = sorted((e, w) for e, w in self.entries if t - e < window)
        excess = sum(w for _, w in inside) + weight - limit
        free = t
        for e, w in inside:
            if excess <= 0:
                break
            excess -= w
            free = e + window
        return free

    def acquire(self, weight: float) -> None:
        if weight > self.limits[60]:
            raise ValueError(f"bobot request {weight:.1f} > batas per menit {self.limits[60]:.0f}")
        if self.used(86400) + weight > self.limits[86400]:
            resume = datetime.fromtimestamp(self._free_at(86400, weight), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            raise BudgetExhausted(resume, self.used(86400), self.limits[86400])
        for window in (3600, 60):
            if self.used(window) + weight > self.limits[window]:
                wait = max(0.0, self._free_at(window, weight) - self.clock()) + 1.0
                self.log(f"[kuota] batas per {'jam' if window == 3600 else 'menit'} "
                         f"({self.used(window):.0f}+{weight:.1f}>{self.limits[window]:.0f}) → tunggu {wait:.0f}s")
                self.sleep(wait)

    def record(self, weight: float, kind: str, label: str, http_status: int | str) -> None:
        t = self.clock()
        self.entries.append((t, weight))
        new = not self.ledger.exists()
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger.open("a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=self.FIELDS)
            if new:
                w.writeheader()
            w.writerow({"epoch": f"{t:.3f}", "utc": datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "weight": f"{weight:.3f}", "kind": kind, "label": label, "http_status": http_status})


def n_days(start: date, end: date) -> int:
    return (end - start).days + 1
