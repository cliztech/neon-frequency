import unittest
from unittest.mock import MagicMock, patch
from core.brain.skills import TrendWatcher, GoogleWorkspace

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

class TestGoogleWorkspace(unittest.TestCase):
    def setUp(self):
        self.workspace = GoogleWorkspace()

    def test_simulation_schedule(self):
        # Ensure we are in simulation mode (no creds)
        self.workspace.service_calendar = None
        schedule = self.workspace.get_schedule("2023-10-27")
        self.assertIn("Interview", schedule)
        self.assertIsInstance(schedule, str)

    def test_simulation_drive_search(self):
        self.workspace.service_drive = None
        results = self.workspace.search_drive("guest")
        self.assertTrue(len(results) > 0)
        self.assertIn("guest_list_guest.xlsx", results)

    def test_simulation_create_doc(self):
        self.workspace.service_docs = None
        self.workspace.service_drive = None
        result = self.workspace.create_doc("My Doc", "Content")
        self.assertIn("Created (Simulated)", result)

    @patch("core.brain.skills.build")
    @patch("core.brain.skills.service_account.Credentials.from_service_account_file")
    @patch("os.path.exists")
    @patch("os.getenv")
    def test_initialization_with_creds(self, mock_getenv, mock_exists, mock_creds, mock_build):
        # Simulate environment where creds exist
        mock_getenv.return_value = "/path/to/creds.json"
        mock_exists.return_value = True

        # Re-initialize
        ws = GoogleWorkspace()

        # Verify that build was called 3 times (drive, calendar, docs)
        self.assertEqual(mock_build.call_count, 3)
        self.assertIsNotNone(ws.service_drive)
        self.assertIsNotNone(ws.service_calendar)

if __name__ == "__main__":
    unittest.main()
