"""Test offline (tanpa internet) collector News. Fixture = HTML probe tersimpan (data/raw/news/probe/).

Pemakaian (dari folder News):
    conda run -n arif-net python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import common  # noqa: E402
from parsers import INDEX_PARSERS, parse_article_time  # noqa: E402
from verify_setup import LOCKED_PERIOD, LOCKED_SOURCES  # noqa: E402

PROBE = common.RAW / "probe"
CFG, SCOPE = common.load_configs()
FIX = {"kompas": "kompas/all_p1.html", "detik": "media/detik/p2_encoded.html", "cnnindonesia": "media/cnnindonesia/p1.html",
       "cnbcindonesia": "media/cnbcindonesia/p1.html", "kontan": "media/kontan/p1.html", "liputan6": "media/liputan6/p1.html"}


class TestConfig(unittest.TestCase):
    def test_locked(self):
        self.assertEqual(list(CFG["sources"]), LOCKED_SOURCES)
        self.assertEqual(CFG["period"], LOCKED_PERIOD)


class TestUrls(unittest.TestCase):
    D = date(2019, 1, 2)

    def url(self, src, page=1, i=0):
        s = CFG["sources"][src]
        return common.build_index_url(s["indexes"][i]["url"], self.D, page, s["per_page"])

    def test_detik_encoded(self):  # tanpa %2F server mengabaikan page (docs §3b)
        # keputusan CP2: Detik = detikFinance saja (detikNews tidak stabil)
        self.assertEqual(self.url("detik", 2), "https://finance.detik.com/indeks?date=01%2F02%2F2019&page=2")
        self.assertEqual(len(CFG["sources"]["detik"]["indexes"]), 1)

    def test_others(self):
        self.assertEqual(self.url("kompas", 2), "https://indeks.kompas.com/?site=news&date=2019-01-02&page=2")  # revisi 2026-10-04
        self.assertEqual(self.url("kompas", 1, 1), "https://indeks.kompas.com/?site=money&date=2019-01-02&page=1")
        self.assertEqual(self.url("cnnindonesia", 2), "https://www.cnnindonesia.com/indeks/2?date=2019/01/02&page=2")
        self.assertEqual(self.url("cnnindonesia", 1), "https://www.cnnindonesia.com/indeks/2?date=2019/01/02&page=1")  # smoke-1: /indeks/1 → 404
        self.assertEqual(self.url("cnbcindonesia", 2), "https://www.cnbcindonesia.com/indeks?date=2019/01/02&page=2")
        self.assertTrue(self.url("kontan", 3).endswith("tanggal=2&bulan=01&tahun=2019&pos=indeks&per_page=40"))
        self.assertEqual(self.url("liputan6", 2), "https://www.liputan6.com/indeks/2019/01/02?start=2019-01-02&end=2019-01-03&page=2")


class TestParsers(unittest.TestCase):
    EXPECT = {"kompas": 20, "detik": 20, "cnnindonesia": 10, "cnbcindonesia": 10, "kontan": 20, "liputan6": 20}

    def test_counts_and_fields(self):
        for src, f in FIX.items():
            items = INDEX_PARSERS[src]((PROBE / f).read_bytes())
            self.assertEqual(len(items), self.EXPECT[src], src)
            self.assertTrue(all(i["url"].startswith("http") and i["title"] for i in items), src)
            self.assertEqual(len({common.article_id(i["url"]) for i in items}), len(items), src)

    def test_times(self):
        kmp = INDEX_PARSERS["kompas"]((PROBE / FIX["kompas"]).read_bytes())
        self.assertTrue(all(i["time_wib"] and i["time_wib"].date() == date(2019, 1, 2) for i in kmp))
        dtk = INDEX_PARSERS["detik"]((PROBE / FIX["detik"]).read_bytes())[0]
        self.assertEqual(dtk["time_wib"], datetime(2019, 1, 2, 22, 0, tzinfo=common.WIB))
        lp6 = INDEX_PARSERS["liputan6"]((PROBE / FIX["liputan6"]).read_bytes())[0]
        self.assertEqual(common.to_wib_iso(lp6["time_wib"]), "2019-01-02T23:02:15+07:00")
        ktn = INDEX_PARSERS["kontan"]((PROBE / FIX["kontan"]).read_bytes())
        self.assertTrue(all(i["time_precision"] == "date" for i in ktn))
        self.assertTrue(all(i["time_wib"] is None for i in INDEX_PARSERS["cnnindonesia"]((PROBE / FIX["cnnindonesia"]).read_bytes())))


class TestTime(unittest.TestCase):
    def test_kompas_url(self):  # contoh peneliti: meta 15:49:59Z = URL 224959 WIB
        dt = common.kompas_url_time("https://money.kompas.com/read/2026/10/01/224959226/x")
        self.assertEqual(common.to_wib_iso(dt), "2026-10-01T22:49:59+07:00")
        self.assertEqual(common.to_wib_iso(common.parse_iso_any("2026-10-01T15:49:59+00:00")), "2026-10-01T22:49:59+07:00")

    def test_parse_id(self):
        self.assertEqual(common.parse_id_datetime("Rabu, 02 Jan 2019 22:00 WIB"), datetime(2019, 1, 2, 22, 0, tzinfo=common.WIB))
        self.assertEqual(common.parse_id_datetime("02 Januari 2019 | 21:10 WIB"), datetime(2019, 1, 2, 21, 10, tzinfo=common.WIB))
        self.assertIsNone(common.parse_iso_any("2026-10-03 19:41:00"))  # tanpa zona = ambigu

    def test_article_jsonld(self):
        html = b'<script type="application/ld+json">{"@type":"WebPage","datePublished":"2019-01-01T23:15:10+07:00"}</script>'
        dt, src = parse_article_time(html)
        self.assertEqual((common.to_wib_iso(dt), src), ("2019-01-01T23:15:10+07:00", "jsonld"))


class TestKeywords(unittest.TestCase):
    M = common.KeywordMatcher(SCOPE["topics"])

    def test_match(self):
        t, k = self.M.match("Harga Cabai Merah Keriting Naik Jelang Lebaran")
        self.assertIn("komoditas_cmk", t)
        self.assertIn("cabai merah keriting", k)
        self.assertEqual(self.M.match("BI: Deflasi Terjadi di Bulan Ini")[0], [])  # 'inflasi' tidak cocok 'deflasi'
        self.assertIn("bbm_logistik", self.M.match("Pemerintah Umumkan Harga BBM Naik")[0])


class TestRegions(unittest.TestCase):
    R = common.RegionMatcher(common.load_supplier_locations())

    def test_regions(self):
        self.assertEqual(self.R.match("Banjir Rendam Sawah di Brebes, Panen Bawang Terancam"), ["brebes"])
        self.assertEqual(self.R.match("Petani Cabai di Bandung Barat Gagal Panen"), ["bandung_barat"])  # bukan 'bandung'
        self.assertEqual(self.R.match("Harga Beras di Karawang dan Subang Naik"), ["karawang", "subang"])
        self.assertEqual(self.R.match("Banjir dan Longsor Landa 3 Kabupaten di Aceh"), [])
        self.assertEqual(self.R.match("Brebesan"), [])  # batas kata


class TestRaw(unittest.TestCase):
    def test_gz_lossless_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            a = common.save_raw_gz(Path(d) / "0102_all_01.gz", b"<html>A</html>")
            b = common.save_raw_gz(Path(d) / "0102_all_01.gz", b"<html>B</html>")
            self.assertEqual((a.name, b.name), ("0102_all_01.gz", "0102_all_01.r2.gz"))
            self.assertEqual(common.read_raw_gz(a), b"<html>A</html>")

    def test_raw_path_roundtrip(self):
        p = common.ROOT / "data" / "raw" / "news" / "ix" / "kmp" / "2019" / "0102_all_01.gz"
        self.assertEqual(common.resolve_raw(common.rel_raw(p)), p)
        self.assertEqual(common.resolve_raw("RAWSTORE:ix/kmp/2019/0102_all_01.gz"), common.RAW_STORE / "ix/kmp/2019/0102_all_01.gz")

    def test_canonical(self):
        self.assertEqual(common.canonical_url("http://Www.X.com/a/b/?utm=1#c"), "https://www.x.com/a/b")


if __name__ == "__main__":
    unittest.main()
