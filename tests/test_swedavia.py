import unittest
from date_validation import validate_date
from flight_display import swedish_time

class TestSwedavia(unittest.TestCase):

    def test_valid_date(self):
        self.assertTrue(validate_date("2026-10-26"))

    def test_invalid_date(self):
        self.assertFalse(validate_date("2026-99-99"))
        self.assertFalse(validate_date("2026-02-30"))

    def test_winter_time(self):
        self.assertEqual(
            swedish_time("2026-01-15T18:45:00Z"),
            "2026-01-15 19:45 CET"
        )

    def test_summer_time(self):
        self.assertEqual(
            swedish_time("2026-07-15T18:45:00Z"),
            "2026-07-15 20:45 CEST"
        )

    def test_missing_time(self):
        self.assertEqual(swedish_time(None), "N/A")

if __name__ == "__main__":
    unittest.main()
