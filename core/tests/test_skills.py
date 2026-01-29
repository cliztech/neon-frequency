import unittest
from core.brain.skills import TrendWatcher

class TestTrendWatcher(unittest.IsolatedAsyncioTestCase):
    async def test_get_current_trends_returns_string(self):
        watcher = TrendWatcher()
        trend = await watcher.get_current_trends()
        self.assertIsInstance(trend, str)
        self.assertIn(trend, watcher.trends)

if __name__ == "__main__":
    unittest.main()
