"""Test offline (tanpa internet) untuk pipeline iklim ARIF-Net.

Pemakaian (dari folder Iklim):
    conda run -n arif-net python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import common  # noqa: E402
from collect_openmeteo import chunk_check, summarize  # noqa: E402
from verify_setup import LOCKED_CORE, LOCKED_LOCATIONS, LOCKED_RESERVE, LOCKED_SETTINGS  # noqa: E402

LOCS, VARS, SETTINGS = common.load_configs()
LOC = {"location_id": "brebes", "latitude": -7.0, "longitude": 108.9}


def payload(start: str, n: int, variables: list[str], suffix: str = "") -> dict:
    days = [str(date.fromisoformat(start).fromordinal(date.fromisoformat(start).toordinal() + i)) for i in range(n)]
    return {"latitude": -7.0, "longitude": 109.0, "elevation": 20.0, "utc_offset_seconds": 25200,
            "timezone": "Asia/Jakarta", "daily_units": {"time": "iso8601", **{v + suffix: "mm" for v in variables}},
            "daily": {"time": days, **{v + suffix: [1.0] * (n - 1) + [None] for v in variables}}}


class TestConfig(unittest.TestCase):
    def test_config_matches_decisions(self):
        self.assertEqual(common.variables_for(VARS, "core"), LOCKED_CORE)
        self.assertEqual(common.variables_for(VARS, "reserve"), LOCKED_RESERVE)
        self.assertEqual([l["location_id"] for l in LOCS["locations"]], LOCKED_LOCATIONS)
        for k, v in LOCKED_SETTINGS.items():
            self.assertEqual(SETTINGS[k], v, k)


class TestBuildParams(unittest.TestCase):
    def test_params_exact(self):
        p = common.build_params(LOC, ["precipitation_sum", "rain_sum"], date(2018, 1, 1), date(2018, 1, 31), SETTINGS, "era5_seamless")
        self.assertEqual(p["daily"], "precipitation_sum,rain_sum")
        self.assertEqual((p["wind_speed_unit"], p["timezone"], p["timeformat"], p["models"]),
                         ("ms", "Asia/Jakarta", "iso8601", "era5_seamless"))
        for banned in ("hourly", "elevation", "apikey", "format"):
            self.assertNotIn(banned, p)

    def test_best_match_rejected(self):
        for m in ("best_match", "era5_land", ""):
            with self.assertRaises(ValueError):
                common.build_params(LOC, ["rain_sum"], "2018-01-01", "2018-01-31", SETTINGS, m)

    def test_missing_coordinates_rejected(self):
        with self.assertRaises(ValueError):
            common.build_params({"location_id": "x", "latitude": None, "longitude": None}, ["rain_sum"],
                                "2018-01-01", "2018-01-31", SETTINGS, "era5")


class TestParsing(unittest.TestCase):
    def test_suffix_tolerant(self):
        pl = payload("2018-01-01", 3, ["temperature_2m_mean"], suffix="_era5_seamless")
        self.assertEqual(common.daily_series(pl, "temperature_2m_mean"), [1.0, 1.0, None])
        self.assertEqual(common.daily_unit(pl, "temperature_2m_mean"), "mm")

    def test_prefix_not_confused(self):
        pl = {"daily": {"temperature_2m_mean_anomaly": [9]}, "daily_units": {}}
        self.assertIsNone(common.daily_series(pl, "temperature_2m_mean"))

    def test_chunk_check(self):
        v = ["precipitation_sum"]
        pl = payload("2026-01-01", 273, v)
        s = summarize(pl, v)
        self.assertEqual(chunk_check(pl, s, date(2026, 1, 1), date(2026, 9, 30), SETTINGS, v), [])
        self.assertEqual(s["per_var"]["precipitation_sum"]["n_null"], 1)
        pl["utc_offset_seconds"] = 0
        self.assertTrue(chunk_check(pl, s, date(2026, 1, 1), date(2026, 9, 30), SETTINGS, v))


class TestPeriods(unittest.TestCase):
    def test_year_chunks(self):
        ch = common.year_chunks(date(2018, 1, 1), date(2026, 9, 30))
        self.assertEqual(len(ch), 9)
        self.assertEqual(ch[-1], (date(2026, 1, 1), date(2026, 9, 30)))
        self.assertEqual(sum(common.n_days(s, e) for s, e in ch), 3195)

    def test_path_length_under_max_path(self):
        years = [s.year for s, _ in common.year_chunks(date(2018, 1, 1), date(2026, 9, 30))]
        p = common.longest_pipeline_path(LOCKED_LOCATIONS, years)
        self.assertLessEqual(len(str(p)), common.WIN_MAX_PATH, str(p))


class TestWriteNew(unittest.TestCase):
    def test_never_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            a = common.write_new(Path(d) / "2018.json", b"A")
            b = common.write_new(Path(d) / "2018.json", b"B")
            self.assertEqual((a.name, b.name), ("2018.json", "2018.r2.json"))
            self.assertEqual(a.read_bytes(), b"A")


class TestBudget(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.t = [1_000_000.0]
        self.slept: list[float] = []

    def tearDown(self):
        self.tmp.cleanup()

    def budget(self, limits):
        def sleep(s):
            self.slept.append(s); self.t[0] += s
        return common.ApiBudget(limits, ledger=Path(self.tmp.name) / "ledger.csv",
                                clock=lambda: self.t[0], sleep=sleep, log=lambda m: None)

    def test_weights(self):
        self.assertAlmostEqual(common.request_weight(15, 14), 1.5)
        self.assertAlmostEqual(common.request_weight(9, 14), 1.0)
        self.assertAlmostEqual(common.request_weight(9, 365), 365 / 14)
        self.assertAlmostEqual(common.request_weight(11, 365), 1.1 * 365 / 14)

    def test_minute_window_waits(self):
        b = self.budget({"per_minute": 60, "per_hour": 1000, "per_day": 5000})
        for _ in range(2):
            b.acquire(26.1); b.record(26.1, "t", "x", 200)
        b.acquire(26.1)  # 78.3 > 60 → harus menunggu jendela menit
        self.assertTrue(self.slept and self.slept[0] > 0)
        self.assertLessEqual(b.used(60) + 26.1, 60 + 1e-9)

    def test_daily_exhaustion_raises(self):
        b = self.budget({"per_minute": 600, "per_hour": 5000, "per_day": 50})
        b.acquire(30); b.record(30, "t", "x", 200)
        with self.assertRaises(common.BudgetExhausted):
            b.acquire(30)

    def test_ledger_persists(self):
        b = self.budget({"per_minute": 600, "per_hour": 5000, "per_day": 100})
        b.record(40, "t", "x", 200)
        b2 = self.budget({"per_minute": 600, "per_hour": 5000, "per_day": 100})
        self.assertAlmostEqual(b2.used(86400), 40)


if __name__ == "__main__":
    unittest.main()
