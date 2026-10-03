"""Test offline (tanpa internet) untuk collector PIHPS ARIF-Net.

Fixture meniru bentuk respons asli GetGridDataKomoditas (raw run 2022 di git 0cfdf94):
6 row (L0 Semua Provinsi, L1 DKI Jakarta, L2 'Kota Jakarta Pusat', L3 tiga pasar),
kunci tanggal DD/MM/YYYY hanya hari kerja, nilai string '50,000' dan '-'.

Pemakaian (dari folder Historical_Komoditas):
    conda run -n arif-net python -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import common  # noqa: E402
from collect_pihps import check_chunk, find_commodity_ids  # noqa: E402
from verify_setup import LOCKED_COMMODITIES, LOCKED_SETTINGS  # noqa: E402

COMM, ST = common.load_configs()


def fixture(start: date, end: date, kramatjati_rows: int = 1, dash_on: set[date] = frozenset(), weekend: bool = False) -> bytes:
    days = [d for d in common.weekdays(start, end)] + ([date(2019, 1, 5)] if weekend else [])
    vals = {f"{d:%d/%m/%Y}": ("-" if d in dash_on else "50,000") for d in days}
    rows = [{"no": "I", "name": "Semua Provinsi", "level": 0, **vals},
            {"no": "II", "name": "DKI Jakarta", "level": 1, **vals},
            {"no": 1, "name": "Kota Jakarta Pusat", "level": 2, **vals},
            {"no": "a", "name": "Pasar Jatinegara", "level": 3, **vals}]
    rows += [{"no": "b", "name": "Pasar Kramatjati", "level": 3, **vals}] * kramatjati_rows
    rows += [{"no": "c", "name": "Pasar Minggu", "level": 3, **vals}]
    return json.dumps({"data": rows}).encode()


class TestConfig(unittest.TestCase):
    def test_locked(self):
        self.assertEqual({c["pihps_name"]: c["comcat_id"] for c in COMM["commodities"]}, LOCKED_COMMODITIES)
        for k, v in LOCKED_SETTINGS.items():
            self.assertEqual(ST[k], v, k)

    def test_params(self):
        p = common.build_params(ST, "com_3", date(2019, 1, 1), date(2019, 1, 31), 123)
        self.assertEqual((p["comcat_id"], p["province_id"], p["regency_id"], p["tipe_laporan"], p["start_date"], p["end_date"]),
                         ("com_3", 13, 34, 1, "2019-01-01", "2019-01-31"))


class TestParsing(unittest.TestCase):
    def test_parse_price(self):
        self.assertEqual(common.parse_price("50,000"), 50000.0)
        self.assertEqual(common.parse_price("1,250,500"), 1250500.0)
        self.assertEqual(common.parse_price("12500"), 12500.0)
        for m in ("-", "", None, " - "):
            self.assertIsNone(common.parse_price(m))
        with self.assertRaises(ValueError):
            common.parse_price("50.000,00")  # format lokal tak dikenal → harus gagal, bukan ditebak

    def test_market_row_and_dates(self):
        pl = json.loads(fixture(date(2019, 1, 1), date(2019, 1, 31)))
        rows = common.market_rows(pl, "Pasar Kramatjati", 3)
        self.assertEqual(len(rows), 1)
        items = common.date_items(rows[0])
        self.assertEqual(items[0], (date(2019, 1, 1), "50,000"))
        self.assertEqual(len(items), 23)  # hari kerja Januari 2019


class TestChunkCheck(unittest.TestCase):
    S, E = date(2019, 1, 1), date(2019, 1, 31)

    def test_ok_with_dash(self):
        issues, st = check_chunk(fixture(self.S, self.E, dash_on={date(2019, 1, 1)}), ST, self.S, self.E)
        self.assertEqual(issues, [])
        self.assertEqual((st["n_date_keys"], st["n_reported"], st["n_dash"], st["n_expected_weekdays"]), (23, 22, 1, 23))

    def test_duplicate_market_fails(self):
        issues, _ = check_chunk(fixture(self.S, self.E, kramatjati_rows=2), ST, self.S, self.E)
        self.assertTrue(issues)

    def test_weekend_flagged(self):
        issues, _ = check_chunk(fixture(self.S, self.E, weekend=True), ST, self.S, self.E)
        self.assertTrue(any("akhir pekan" in i for i in issues))

    def test_html_rejected(self):
        issues, _ = check_chunk(b"<html>login</html>", ST, self.S, self.E)
        self.assertTrue(issues)


class TestReference(unittest.TestCase):
    def test_list_shape(self):
        pl = {"data": [{"cat_id": "cat_1", "com_id": "com_3", "com_name": "Beras Kualitas Medium I"},
                       {"cat_id": "cat_4", "com_id": "com_14", "com_name": "Cabai Merah Keriting"}]}
        f = find_commodity_ids(pl, {"com_3": "x", "com_14": "y", "com_11": "z"})
        self.assertIn("Beras Kualitas Medium I", f["com_3"])
        self.assertIn("Cabai Merah Keriting", f["com_14"])
        self.assertEqual(f["com_11"], [])

    def test_map_shape(self):
        f = find_commodity_ids({"com_11": "Bawang Merah Ukuran Sedang"}, {"com_11": "x"})
        self.assertEqual(f["com_11"], ["Bawang Merah Ukuran Sedang"])


class TestPeriodsPaths(unittest.TestCase):
    def test_month_chunks(self):
        ch = common.month_chunks(date(2019, 1, 1), date(2026, 9, 30))
        self.assertEqual(len(ch), 93)
        self.assertEqual(ch[1], (date(2019, 2, 1), date(2019, 2, 28)))
        self.assertEqual(ch[-1], (date(2026, 9, 1), date(2026, 9, 30)))

    def test_path_length(self):
        p = common.longest_pipeline_path(list(LOCKED_COMMODITIES.values()))
        self.assertLessEqual(len(str(p)), common.WIN_MAX_PATH, str(p))

    def test_write_new_never_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            a = common.write_new(Path(d) / "2019-01.json", b"A")
            b = common.write_new(Path(d) / "2019-01.json", b"B")
            self.assertEqual((a.name, b.name, a.read_bytes()), ("2019-01.json", "2019-01.r2.json", b"A"))


if __name__ == "__main__":
    unittest.main()
