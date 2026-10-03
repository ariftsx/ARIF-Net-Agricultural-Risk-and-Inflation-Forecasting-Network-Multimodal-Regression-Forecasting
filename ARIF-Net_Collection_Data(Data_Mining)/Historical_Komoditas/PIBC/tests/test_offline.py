"""Test offline (tanpa internet) untuk collector PIBC ARIF-Net.

Fixture meniru respons /rice-price-detail dari tangkapan DevTools peneliti (2026-10-03):
{"draw", "recordsTotal", "recordsFiltered", "data": [{"tgl": "2019 01 01", "cjr_kpl": "13,325", ...}]}

Pemakaian (dari folder Historical_Komoditas\\PIBC):
    conda run -n arif-net python -m unittest discover -s tests -v
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import common  # noqa: E402
from collect_pibc import check_chunk  # noqa: E402
from verify_setup import LOCKED_FIELDS, LOCKED_SETTINGS  # noqa: E402

VAR, ST = common.load_configs()
COLS = ST["columns"]
ROW_2019_01_01 = {"tgl": "2019 01 01", "cjr_kpl": "13,325", "cjr_slyp": "12,050", "setra": "13,275", "saigon": "11,800",
                  "muncul1": "11,175", "muncul2": "10,300", "muncul3": "9,625", "ir641": "10,800", "ir642": "10,200",
                  "ir643": "8,500", "ir42": "12,075", "kp_biasa": "11,675", "kp_paris": "14,925", "ktn_htm": "17,925"}


def fixture(start: date, end: date, drop: date | None = None, dup: bool = False, rf_extra: int = 0) -> bytes:
    rows = []
    d = start
    while d <= end:
        if d != drop:
            rows.append({**ROW_2019_01_01, "tgl": f"{d:%Y %m %d}"})
        d += timedelta(days=1)
    if dup:
        rows.append(rows[-1])
    return json.dumps({"draw": 1, "recordsTotal": len(rows) + rf_extra, "recordsFiltered": len(rows) + rf_extra,
                       "data": rows, "disableOrdering": False}).encode()


class TestConfig(unittest.TestCase):
    def test_locked(self):
        self.assertEqual([v["field"] for v in VAR["varieties"]], LOCKED_FIELDS)
        for k, v in LOCKED_SETTINGS.items():
            self.assertEqual(ST[k], v, k)

    def test_mapping_not_preset(self):
        # pemetaan Medium I adalah keputusan peneliti — tidak boleh terisi diam-diam
        self.assertTrue(VAR["medium_i_mapping"] is None or VAR["_meta"]["medium_i_mapping_decided_at"])


class TestParams(unittest.TestCase):
    def test_start_date_exclusive_shift(self):
        p = common.build_params(ST, date(2019, 1, 1), date(2019, 12, 31), 0, 1)
        self.assertEqual((p["start_date"], p["end_date"]), ("2018-12-31", "2019-12-31"))
        self.assertEqual(p["columns[0][data]"], "tgl")
        self.assertEqual(p["columns[14][data]"], "ktn_htm")
        self.assertEqual(p["length"], ST["page_length"])


class TestParsing(unittest.TestCase):
    def test_tgl(self):
        self.assertEqual(common.parse_tgl("2019 01 01"), date(2019, 1, 1))
        for bad in ("2019-01-01", "01/01/2019", ""):
            with self.assertRaises(ValueError):
                common.parse_tgl(bad)

    def test_price(self):
        self.assertEqual(common.parse_price("13,325"), 13325.0)
        self.assertIsNone(common.parse_price(""))
        self.assertIsNone(common.parse_price(None))
        with self.assertRaises(ValueError):
            common.parse_price("13.325,00")


class TestChunk(unittest.TestCase):
    S, E = date(2019, 1, 1), date(2019, 1, 31)

    def test_ok(self):
        issues, st = check_chunk(fixture(self.S, self.E), COLS, self.S, self.E, 400)
        self.assertEqual(issues, [])
        self.assertEqual((st["n_rows"], st["first_tgl"], st["last_tgl"]), (31, "2019 01 01", "2019 01 31"))

    def test_missing_first_day_detected(self):  # gejala bila start_date tidak digeser −1
        issues, _ = check_chunk(fixture(self.S, self.E, drop=self.S), COLS, self.S, self.E, 400)
        self.assertTrue(issues)

    def test_duplicate_detected(self):
        issues, _ = check_chunk(fixture(self.S, self.E, dup=True), COLS, self.S, self.E, 400)
        self.assertTrue(issues)

    def test_pagination_needed_detected(self):
        issues, _ = check_chunk(fixture(self.S, self.E, rf_extra=500), COLS, self.S, self.E, 400)
        self.assertTrue(any("pagination" in i for i in issues))


class TestPeriodsPaths(unittest.TestCase):
    def test_chunks_and_days(self):
        ch = common.year_chunks(date(2019, 1, 1), date(2025, 6, 16))
        self.assertEqual(len(ch), 7)
        self.assertEqual(ch[-1], (date(2025, 1, 1), date(2025, 6, 16)))
        self.assertEqual(sum(common.n_days(s, e) for s, e in ch), 2359)

    def test_path_length(self):
        self.assertLessEqual(len(str(common.longest_pipeline_path())), common.WIN_MAX_PATH)

    def test_write_new(self):
        with tempfile.TemporaryDirectory() as d:
            a = common.write_new(Path(d) / "2019.json", b"A"); b = common.write_new(Path(d) / "2019.json", b"B")
            self.assertEqual((a.name, b.name, a.read_bytes()), ("2019.json", "2019.r2.json", b"A"))


if __name__ == "__main__":
    unittest.main()
