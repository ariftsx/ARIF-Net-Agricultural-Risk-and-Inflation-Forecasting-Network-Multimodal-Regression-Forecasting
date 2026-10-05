"""Test offline (tanpa internet) untuk collector IPJ ARIF-Net.

Fixture meniru respons /api2/v1/public/report dari tangkapan DevTools peneliti (2026-10-03):
{"status":200,"message":"Success","data":{"data":[{"commodity_id":1,"commodity_name":"Beras IR. I (IR 64)",
  "avg_value":15000,...,"recaps":[{"value":15000,"time":"2024-01-01"}, ...]}]}}

Pemakaian (dari folder Historical_Komoditas\\IPJ):
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
from collect_ipj import check_month  # noqa: E402
from verify_setup import LOCKED_MAPPING, LOCKED_SETTINGS  # noqa: E402

COMM, ST = common.load_configs()
MAP = COMM["commodities"]
NAMES = {1: "Beras IR. I (IR 64)", 4: "Beras Muncul I", 8: "Cabe Merah Keriting", 12: "Bawang Merah", 13: "Bawang Putih"}


def fixture(ym: str, empty: bool = False, rename: dict | None = None, extra_day: bool = False, dup: bool = False,
            dup_diff: bool = False) -> bytes:
    start, end = common.month_bounds(ym)
    days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
    rows = []
    for cid, name in NAMES.items():
        recaps = [] if empty else [{"value": 15000, "time": d.isoformat()} for d in days]
        if extra_day and not empty:
            recaps.append({"value": 15000, "time": (end + timedelta(days=1)).isoformat()})
        if dup and not empty:
            recaps.append(dict(recaps[11]))  # entri ganda bernilai identik (pola sumber 2026-09-12)
        if dup_diff and not empty:
            recaps.append({"value": 99999, "time": recaps[11]["time"]})
        rows.append({"commodity_id": cid, "commodity_name": (rename or {}).get(cid, name), "avg_value": 15000,
                     "max_value": 15000, "min_value": 15000, "recaps": recaps})
    return json.dumps({"status": 200, "message": "Success", "data": {"data": rows}}).encode()


class TestConfig(unittest.TestCase):
    def test_locked(self):
        self.assertEqual({c["comcat_id"]: (c["ipj_commodity_id"], c["ipj_commodity_name"]) for c in MAP}, LOCKED_MAPPING)
        for k, v in LOCKED_SETTINGS.items():
            self.assertEqual(ST[k], v, k)
        self.assertNotEqual(ST["market_id"], 1)  # Pasar Induk (PIKJ) tidak dipakai

    def test_params(self):
        self.assertEqual(common.build_report_params(ST, "2024-01"), {"filterBy": "market", "Id": 12, "yearMonth": "2024-01"})


class TestPeriods(unittest.TestCase):
    def test_months(self):
        ms = common.months("2019-01", "2026-09")
        self.assertEqual((len(ms), ms[0], ms[-1]), (93, "2019-01", "2026-09"))
        self.assertEqual(common.month_bounds("2024-02"), (date(2024, 2, 1), date(2024, 2, 29)))

    def test_path_length(self):
        self.assertLessEqual(len(str(common.longest_pipeline_path())), common.WIN_MAX_PATH)


class TestParsing(unittest.TestCase):
    def test_value(self):
        self.assertEqual(common.parse_value(15000), 15000.0)
        self.assertEqual(common.parse_value("15,000"), 15000.0)
        for empty in (None, "", 0):
            self.assertIsNone(common.parse_value(empty))
        with self.assertRaises(ValueError):
            common.parse_value("abc")


class TestCheckMonth(unittest.TestCase):
    def test_ok(self):
        status, issues, st = check_month(fixture("2024-01"), MAP, "2024-01")
        self.assertEqual((status, issues), ("OK", []))
        self.assertEqual(st["recaps_per_target"], {"com_14": 31, "com_11": 31, "com_3": 31})

    def test_empty_month_is_ok_empty(self):
        status, issues, _ = check_month(fixture("2019-01", empty=True), MAP, "2019-01")
        self.assertEqual((status, issues), ("OK_EMPTY", []))

    def test_renamed_commodity_fails(self):
        status, issues, _ = check_month(fixture("2024-01", rename={4: "Beras Medium"}), MAP, "2024-01")
        self.assertEqual(status, "FAIL")

    def test_date_outside_month_fails(self):
        self.assertEqual(check_month(fixture("2024-01", extra_day=True), MAP, "2024-01")[0], "FAIL")

    def test_identical_duplicate_accepted(self):  # keputusan peneliti 2026-10-03
        status, issues, st = check_month(fixture("2024-01", dup=True), MAP, "2024-01")
        self.assertEqual((status, issues), ("OK", []))
        self.assertEqual(len(st["duplicate_identical"]), 3)
        self.assertEqual(st["recaps_per_target"]["com_3"], 31)  # dihitung per tanggal unik

    def test_conflicting_duplicate_fails(self):
        self.assertEqual(check_month(fixture("2024-01", dup_diff=True), MAP, "2024-01")[0], "FAIL")

    def test_bad_status_fails(self):
        self.assertEqual(check_month(json.dumps({"status": 500, "data": None}).encode(), MAP, "2024-01")[0], "FAIL")


class TestWriteNew(unittest.TestCase):
    def test_never_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            a = common.write_new(Path(d) / "2024-01.json", b"A"); b = common.write_new(Path(d) / "2024-01.json", b"B")
            self.assertEqual((a.name, b.name, a.read_bytes()), ("2024-01.json", "2024-01.r2.json", b"A"))


if __name__ == "__main__":
    unittest.main()
