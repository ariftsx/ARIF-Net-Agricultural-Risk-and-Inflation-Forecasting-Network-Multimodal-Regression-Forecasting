"""Utilitas bersama — ARIF-Net Phase 1 · koleksi News (6 media, P1-DG-25…30).

Satu-satunya tempat URL indeks dibangun (build_index_url), raw disimpan (save_raw_gz),
waktu dinormalisasi ke WIB, dan kata kunci dicocokkan (KeywordMatcher).
Otoritas: Plan v2.0.0 §10.4 · Contract v2.1.0 §5.3, §19 · AGENT.md §17.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"
RAW = ROOT / "data" / "raw" / "news"   # manifest (di-commit) & bukti probe


def _raw_store() -> Path:
    """Lokasi raw HTML (±11–12 GB). config/sources.json → 'raw_store' (path absolut, mis. di luar OneDrive); default di dalam paket."""
    try:
        v = json.loads((ROOT / "config" / "sources.json").read_text(encoding="utf-8")).get("raw_store")
    except (OSError, ValueError):
        v = None
    return Path(v) if v else RAW


RAW_STORE = _raw_store()
RAW_INDEX = RAW_STORE / "ix"      # lokal, tidak di-commit (ukuran & hak cipta)
RAW_ARTICLE = RAW_STORE / "art"   # lokal, tidak di-commit
RAWSTORE_PREFIX = "RAWSTORE:"
MANIFEST_PAGES = RAW / "manifest_index_pages.csv"
MANIFEST_DAYS = RAW / "manifest_index_days.csv"
MANIFEST_ARTICLES = RAW / "manifest_articles.csv"
PROCESSED = ROOT / "data" / "processed" / "news"
STATE = CONFIG / "state.json"
WIB = timezone(timedelta(hours=7))
WIN_MAX_PATH = 259
MONTHS_ID = {"jan": 1, "januari": 1, "feb": 2, "februari": 2, "mar": 3, "maret": 3, "apr": 4, "april": 4, "mei": 5,
             "jun": 6, "juni": 6, "jul": 7, "juli": 7, "agu": 8, "ags": 8, "agustus": 8, "agt": 8, "sep": 9, "september": 9,
             "okt": 10, "oktober": 10, "nov": 11, "november": 11, "des": 12, "desember": 12}


# ---------------------------------------------------------------- io
def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def rel_raw(path: Path) -> str:
    """Path raw untuk manifest: relatif ROOT bila di dalam paket, selain itu 'RAWSTORE:<relatif raw_store>'."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return RAWSTORE_PREFIX + path.relative_to(RAW_STORE).as_posix()


def resolve_raw(raw_file: str) -> Path:
    return RAW_STORE / raw_file[len(RAWSTORE_PREFIX):] if raw_file.startswith(RAWSTORE_PREFIX) else ROOT / raw_file


def save_raw_gz(path: Path, data: bytes) -> Path:
    """Simpan bytes respons ter-gzip (lossless) ke file BARU; tidak pernah menimpa (→ .r2.gz, …)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    target, n = path, 1
    while target.exists():
        n += 1
        target = path.with_name(f"{path.name[:-3]}.r{n}.gz")
    with target.open("xb") as fh:
        fh.write(gzip.compress(data, mtime=0))
    return target


def read_raw_gz(path: Path) -> bytes:
    return gzip.decompress(path.read_bytes())


# ---------------------------------------------------------------- config
def load_configs() -> tuple[dict, dict]:
    return load_json(CONFIG / "sources.json"), load_json(CONFIG / "news_scope_DRAFT.json")


def load_state() -> dict:
    return load_json(STATE) if STATE.exists() else {}


def save_state(state: dict) -> None:
    state["updated_at_utc"] = now_utc()
    save_json(STATE, state)


def daterange(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def build_index_url(template: str, d: date, page: int, per_page: int) -> str:
    """URL indeks satu tanggal & halaman. Detik: tanggal WAJIB ter-encode (%2F), dibangun sebagai string utuh."""
    tokens = {"date_iso": d.isoformat(), "date_next_iso": (d + timedelta(days=1)).isoformat(),
              "date_mdy_enc": f"{d:%m}%2F{d:%d}%2F{d:%Y}", "date_ymd_slash": f"{d:%Y/%m/%d}",
              "yyyy": f"{d:%Y}", "mm": f"{d:%m}", "dd": f"{d:%d}", "d": str(d.day),
              "page": str(page), "offset": str((page - 1) * per_page)}
    return template.format(**tokens)


def raw_index_path(code: str, index_name: str, d: date, page: int) -> Path:
    return RAW_INDEX / code / f"{d:%Y}" / f"{d:%m%d}_{index_name}_{page:02d}.gz"


def raw_article_path(code: str, article_id: str) -> Path:
    return RAW_ARTICLE / code / f"{article_id[:16]}.gz"


# ---------------------------------------------------------------- url & waktu
def canonical_url(url: str) -> str:
    parts = urlsplit(url.strip())
    return urlunsplit(("https", parts.netloc.lower(), parts.path.rstrip("/"), "", ""))


def article_id(url: str) -> str:
    return hashlib.sha1(canonical_url(url).encode("utf-8")).hexdigest()


def to_wib_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=WIB)
    return dt.astimezone(WIB).strftime("%Y-%m-%dT%H:%M:%S+07:00")


def parse_iso_any(text: str) -> datetime | None:
    """ISO 8601 dengan zona (+00:00, +07:00, Z). Tanpa zona → None (ambigu)."""
    t = (text or "").strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(t)
    except ValueError:
        return None
    return dt if dt.tzinfo else None


def parse_id_datetime(text: str) -> datetime | None:
    """'Rabu, 02 Jan 2019 22:00 WIB' / '02 Januari 2019 | 21:10 WIB' → datetime WIB."""
    m = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})(?:\D+(\d{1,2})[:.](\d{2}))?", text or "")
    if not m or m.group(2).lower() not in MONTHS_ID:
        return None
    hh, mi = (int(m.group(4)), int(m.group(5))) if m.group(4) else (0, 0)
    return datetime(int(m.group(3)), MONTHS_ID[m.group(2).lower()], int(m.group(1)), hh, mi, tzinfo=WIB)


def kompas_url_time(url: str) -> datetime | None:
    """/read/YYYY/MM/DD/HHMMSSxxx/ → WIB (terverifikasi cocok dengan meta & JSON-LD, docs §3b)."""
    m = re.search(r"/read/(\d{4})/(\d{2})/(\d{2})/(\d{2})(\d{2})(\d{2})\d*", url)
    if not m:
        return None
    y, mo, d, hh, mi, ss = map(int, m.groups())
    if hh > 23 or mi > 59 or ss > 59:
        return None
    return datetime(y, mo, d, hh, mi, ss, tzinfo=WIB)


# ---------------------------------------------------------------- relevansi (P1-DG-30)
class KeywordMatcher:
    """Kata kunci P1-DG-27 dicocokkan pada JUDUL, case-insensitive, batas kata (inflasi ≠ deflasi)."""

    def __init__(self, topics: dict[str, list[str]]):
        self.rules = [(t, kw, re.compile(r"(?<![0-9a-z])" + re.escape(kw.lower()) + r"(?![0-9a-z])"))
                      for t, kws in topics.items() for kw in kws]

    def match(self, title: str) -> tuple[list[str], list[str]]:
        low = (title or "").lower()
        hits = [(t, kw) for t, kw, rx in self.rules if rx.search(low)]
        return sorted({t for t, _ in hits}), sorted({kw for _, kw in hits})


class RegionMatcher:
    """Kolom wilayah_pemasok (keputusan peneliti 2026-10-03): judul menyebut salah satu 18 kabupaten pemasok
    (Iklim/config/locations.json, P1-DG-11). Nama terpanjang dicocokkan lebih dulu ('bandung barat' sebelum 'bandung').
    Catatan: judul tidak membedakan Kabupaten vs Kota (mis. Kota Bandung, Kota Cirebon) dan 'Bima' bisa nama orang —
    dicatat sebagai keterbatasan; penyaringan lanjut di Phase 3."""

    def __init__(self, locations: list[dict]):
        names = sorted(((l["kabupaten"].replace("Kabupaten ", "").lower(), l["location_id"]) for l in locations), key=lambda x: -len(x[0]))
        self.rules = [(lid, re.compile(r"(?<![0-9a-z])" + re.escape(n) + r"(?![0-9a-z])")) for n, lid in names]

    def match(self, title: str) -> list[str]:
        low, hits = (title or "").lower(), []
        for lid, rx in self.rules:
            if rx.search(low):
                hits.append(lid)
                low = rx.sub(" ", low)   # cegah 'bandung' ikut cocok dari 'bandung barat'
        return sorted(hits)


def load_supplier_locations() -> list[dict]:
    return load_json(ROOT.parent / "Iklim" / "config" / "locations.json")["locations"]


def longest_pipeline_path(codes: list[str]) -> Path:
    c = max(codes, key=len)
    cands = [RAW_INDEX / c / "2026" / "0930_news_80.r9.gz", RAW_ARTICLE / c / "0123456789abcdef.r9.gz",
             PROCESSED / "articles_relevant.csv", MANIFEST_PAGES, LOGS / f"collect_index_{c}_{stamp()}.log"]
    return max(cands, key=lambda p: len(str(p)))
