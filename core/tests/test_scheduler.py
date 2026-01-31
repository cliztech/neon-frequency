import unittest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from core.brain.playlist_manager import PlaylistManager
from core.brain.music_library import TrackMetadata
from core.brain.scheduler import RadioScheduler

class TestPlaylistManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tracks = [
            TrackMetadata(file_path="/music/song1.mp3", title="Song 1", artist="Artist 1", duration_seconds=180),
            TrackMetadata(file_path="/music/song2.mp3", title="Song 2", artist="Artist 2", duration_seconds=200),
        ]

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_export_and_parse_m3u(self):
        filepath = os.path.join(self.test_dir, "test.m3u")

        # Export
        result = PlaylistManager.export_m3u(self.tracks, filepath)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filepath))

        # Parse
        parsed = PlaylistManager.parse_m3u(filepath)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0].title, "Song 1")
        self.assertEqual(parsed[1].file_path, "/music/song2.mp3")

    def test_export_and_parse_pls(self):
        filepath = os.path.join(self.test_dir, "test.pls")

        # Export
        result = PlaylistManager.export_pls(self.tracks, filepath)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filepath))

        # Parse
        parsed = PlaylistManager.parse_pls(filepath)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0].title, "Song 1")
        self.assertEqual(parsed[1].duration_seconds, 200)

class TestRadioScheduler(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('core.brain.scheduler.MusicLibrary')
    @patch('core.brain.scheduler.ElevenLabsClient')
    @patch('core.brain.scheduler.WeatherClient')
    @patch('core.brain.scheduler.NewsAgent')
    def test_generate_hour_block(self, mock_news, mock_weather, mock_voice, mock_library):
        # Setup mocks
        mock_weather_instance = mock_weather.return_value
        mock_weather_instance.get_weather.return_value = "20C, Sunny"

        mock_news_instance = mock_news.return_value
        mock_news_instance.get_top_stories.return_value = ["AI takes over world"]

        mock_voice_instance = mock_voice.return_value
        # Mock generate to return dummy bytes
        mock_voice_instance.generate.return_value = b"fake audio data"

        # Mock Music Library
        mock_library_instance = mock_library.return_value
        mock_library_instance.get_rotation_picks.return_value = [
            TrackMetadata("/music/test1.mp3", "Test 1", "Artist 1", duration_seconds=180),
            TrackMetadata("/music/test2.mp3", "Test 2", "Artist 2", duration_seconds=180)
        ]

        scheduler = RadioScheduler(audio_output_dir=self.test_dir)

        # Generate
        output_path = scheduler.generate_hour_block(10, self.test_dir)

        # Verify
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith("hour_10.m3u"))

        # Check content
        tracks = PlaylistManager.parse_m3u(output_path)
        self.assertGreater(len(tracks), 0)

        # Should have generated audio files
        generated_audio = list(Path(self.test_dir).glob("*.mp3"))
        self.assertGreater(len(generated_audio), 0)

        # Check if we have both music and voice (Music has /music/ path, Voice has temp dir path)
        has_voice = any(str(self.test_dir) in t.file_path for t in tracks)
        has_music = any("/music/" in t.file_path for t in tracks)

        self.assertTrue(has_voice, "Playlist should contain voice tracks")
        self.assertTrue(has_music, "Playlist should contain music tracks")

if __name__ == '__main__':
    unittest.main()
