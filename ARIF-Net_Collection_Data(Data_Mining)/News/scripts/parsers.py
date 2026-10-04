"""Parser halaman indeks & artikel per media (BeautifulSoup + lxml). Tidak mengubah raw.

Setiap parser indeks mengembalikan list item:
  {url, title, channel, time_wib (datetime|None), time_source, time_precision, index_time_text}
Struktur HTML diturunkan dari halaman probe yang tersimpan (data/raw/news/probe/, docs §3b).
"""
from __future__ import annotations

import json
import re
from datetime import datetime

from bs4 import BeautifulSoup

from common import kompas_url_time, parse_id_datetime, parse_iso_any


def _txt(node) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip() if node else ""


def _item(url, title, channel="", time_wib=None, source="", precision="", raw_time=""):
    return {"url": url.strip(), "title": title.strip(), "channel": channel.strip(), "time_wib": time_wib,
            "time_source": source if time_wib else "", "time_precision": precision if time_wib else "",
            "index_time_text": raw_time.strip()}


def parse_kompas(html: bytes) -> list[dict]:
    s = BeautifulSoup(html, "lxml")
    out = []
    for it in s.select("div.articleItem"):
        a = it.select_one("a.article-link[href]")
        if not a or "/read/" not in a["href"]:
            continue
        out.append(_item(a["href"], _txt(it.select_one(".articleTitle")), _txt(it.select_one(".articlePost-subtitle")),
                         kompas_url_time(a["href"]), "url", "second", _txt(it.select_one(".articlePost-date"))))
    return out


def parse_detik(html: bytes) -> list[dict]:
    s = BeautifulSoup(html, "lxml")
    out = []
    for it in s.select("article.list-content__item"):
        a = it.select_one("a.media__link[href]") or it.select_one("a[href*='/d-']")
        if not a:
            continue
        t = it.select_one("[title*='WIB']")
        raw = t.get("title", "") if t else ""
        title = _txt(it.select_one(".media__title")) or (it.find("img") or {}).get("alt", "")
        out.append(_item(a["href"], title, a["href"].split("/")[3] if a["href"].count("/") > 3 else "",
                         parse_id_datetime(raw), "index", "minute", raw))
    return out


def _parse_tailwind_articles(html: bytes, url_rx: str) -> list[dict]:
    """CNN Indonesia & CNBC Indonesia: <article><a href=…><h2>judul</h2> … kanal …"""
    s = BeautifulSoup(html, "lxml")
    out = []
    for it in s.find_all("article"):
        a = it.find("a", href=re.compile(url_rx))
        h2 = it.find("h2")
        if not a or not h2:
            continue
        chan = a["href"].split("/")[3]
        out.append(_item(a["href"], _txt(h2), chan))
    return out


def parse_cnnindonesia(html: bytes) -> list[dict]:
    return _parse_tailwind_articles(html, r"^https://www\.cnnindonesia\.com/[a-z\-]+/\d{14}-\d+-\d+/")


def parse_cnbcindonesia(html: bytes) -> list[dict]:
    return _parse_tailwind_articles(html, r"^https://www\.cnbcindonesia\.com/[a-z\-]+/\d{14}-\d+-\d+/")


def parse_kontan(html: bytes) -> list[dict]:
    s = BeautifulSoup(html, "lxml")
    out = []
    for li in s.find_all("li", attrs={"data-offset": True}):  # hanya daftar indeks utama (bukan sidebar)
        h = li.select_one("h1 a[href*='kontan.co.id/news/']")
        if not h:
            continue
        raw = _txt(li.select_one(".font-gray")).lstrip("| ").strip()
        out.append(_item(h["href"], _txt(h), _txt(li.select_one(".linkto-orange")), parse_id_datetime(raw), "index",
                         "minute" if re.search(r"\d{1,2}[:.]\d{2}", raw) else "date", raw))
    return out


def parse_liputan6(html: bytes) -> list[dict]:
    s = BeautifulSoup(html, "lxml")
    out = []
    for it in s.select("article.articles--rows--item"):
        a = it.select_one("a[data-template-var=url][href]") or it.find("a", href=re.compile(r"/read/\d+/"))
        if not a:
            continue
        tm = it.find("time", attrs={"datetime": True})
        raw = tm["datetime"] if tm else ""
        title = a.get("title") or _txt(it.select_one("[data-template-var=title]")) or _txt(a)
        out.append(_item(a["href"], title, it.get("data-channel-slug", ""), parse_iso_any(raw), "index", "second", raw))
    return out


INDEX_PARSERS = {"kompas": parse_kompas, "detik": parse_detik, "cnnindonesia": parse_cnnindonesia,
                 "cnbcindonesia": parse_cnbcindonesia, "kontan": parse_kontan, "liputan6": parse_liputan6}


def parse_article_time(html: bytes) -> tuple[datetime | None, str]:
    """Waktu terbit dari halaman artikel: JSON-LD datePublished → meta article:published_time. Hanya nilai ber-zona."""
    text = html.decode("utf-8", "replace")
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', text, flags=re.S):
        try:
            data = json.loads(block)
        except ValueError:
            m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', block)
            data = {"datePublished": m.group(1)} if m else {}
        for d in (data if isinstance(data, list) else [data]):
            dt = parse_iso_any(str(d.get("datePublished", ""))) if isinstance(d, dict) else None
            if dt:
                return dt, "jsonld"
    m = re.search(r'<meta[^>]+article:published_time[^>]+content="([^"]+)"', text)
    if m and parse_iso_any(m.group(1)):
        return parse_iso_any(m.group(1)), "meta"
    return None, ""
