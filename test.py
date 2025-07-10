import unittest
from index import parse
from datetime import datetime

# July 10th, 2025 at 21:20:42
fixed_date = datetime(2025, 7, 10, 21, 20, 42)


class TestParse(unittest.TestCase):
    def test_parse_add_days(self):
        result = parse("now()+2d", now=fixed_date)
        assert result == datetime(2025, 7, 12, 21, 20, 42)

    def test_parse_remove_days(self):
        result = parse("now()-2d", now=fixed_date)
        assert result == datetime(2025, 7, 8, 21, 20, 42)


if __name__ == "__main__":
    unittest.main()
