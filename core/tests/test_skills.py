import unittest
from core.brain.skills import TrendWatcher

class TestTrendWatcher(unittest.TestCase):
    def setUp(self):
        # Clear cache before each test to ensure isolation
        TrendWatcher.get_current_trends.cache_clear()

    def test_get_current_trends_returns_string(self):
        watcher = TrendWatcher()
        trend = watcher.get_current_trends()
        self.assertIsInstance(trend, str)
        self.assertIn(trend, watcher.trends)

    def test_get_current_trends_caching(self):
        watcher = TrendWatcher()
        trend1 = watcher.get_current_trends()
        trend2 = watcher.get_current_trends()
        self.assertEqual(trend1, trend2)

        # Check cache hits
        info = watcher.get_current_trends.cache_info()
        self.assertGreater(info.hits, 0)

if __name__ == "__main__":
    unittest.main()
