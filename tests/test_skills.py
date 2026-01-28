import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the repo root to sys.path so we can import core
sys.path.append(os.getcwd())

from core.brain.skills import TrendWatcher

class TestTrendWatcher(unittest.TestCase):

    def test_fallback_no_keys(self):
        """Tests that TrendWatcher falls back to simulated trends when API keys are not set."""
        # Use patch.dict to ensure the environment is clean of the API keys for this test.
        with patch.dict(os.environ, {}, clear=True):
            watcher = TrendWatcher()
            self.assertIsNone(watcher.search_tool)
            trend = watcher.get_current_trends()
            self.assertIn(trend, watcher.trends)

    @patch("core.brain.skills.GoogleSearchAPIWrapper")
    @patch("core.brain.skills.GoogleSearchRun")
    def test_search_with_keys(self, mock_run, mock_wrapper):
        # Mock keys
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake", "GOOGLE_CSE_ID": "fake"}):
            # Setup mock
            mock_tool_instance = MagicMock()
            mock_tool_instance.run.return_value = "AI is taking over the world"
            mock_run.return_value = mock_tool_instance

            watcher = TrendWatcher()
            self.assertIsNotNone(watcher.search_tool)

            trend = watcher.get_current_trends()
            self.assertEqual(trend, "AI is taking over the world")
            print(f"Mocked search trend: {trend}")

    def test_search_failure_fallback(self):
         with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake", "GOOGLE_CSE_ID": "fake"}):
             # We need to mock the imports so they don't fail, but we want the run() to fail
             with patch("core.brain.skills.GoogleSearchAPIWrapper") as mock_wrapper, \
                  patch("core.brain.skills.GoogleSearchRun") as mock_run:

                mock_tool_instance = MagicMock()
                mock_tool_instance.run.side_effect = Exception("API quota exceeded")
                mock_run.return_value = mock_tool_instance

                watcher = TrendWatcher()
                trend = watcher.get_current_trends()

                # Should fall back
                self.assertIn(trend, watcher.trends)
                print(f"Fallback after failure: {trend}")

if __name__ == "__main__":
    unittest.main()
