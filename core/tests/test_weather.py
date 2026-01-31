import unittest
from unittest.mock import patch, MagicMock
import os
import requests  # Import requests to patch it
from core.brain.skills import WeatherStation

class TestWeatherStation(unittest.TestCase):

    @patch('requests.get')
    @patch('core.brain.skills.os.getenv')
    def test_get_weather_success(self, mock_getenv, mock_requests_get):
        # Mock API Key
        mock_getenv.return_value = "fake_api_key"

        # Mock API Response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 25.5},
            "weather": [{"description": "clear sky"}]
        }
        mock_requests_get.return_value = mock_response

        weather = WeatherStation.get_weather("TestCity")

        # Assertions
        mock_requests_get.assert_called_with(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": "TestCity", "appid": "fake_api_key", "units": "metric"},
            timeout=5
        )
        self.assertEqual(weather, "25.5°C, Clear sky")

    @patch('core.brain.skills.os.getenv')
    def test_get_weather_no_api_key(self, mock_getenv):
        # Mock missing API Key
        mock_getenv.return_value = None

        weather = WeatherStation.get_weather("Rowville")

        # Should return the random fallback format
        # e.g. "35°C, Sunny"
        self.assertIsInstance(weather, str)
        self.assertIn("°C, ", weather)

    @patch('requests.get')
    @patch('core.brain.skills.os.getenv')
    def test_get_weather_api_failure(self, mock_getenv, mock_requests_get):
        # Mock API Key
        mock_getenv.return_value = "fake_api_key"

        # Mock API Failure
        mock_requests_get.side_effect = Exception("API Error")

        weather = WeatherStation.get_weather("Rowville")

        # Should return the random fallback format
        self.assertIsInstance(weather, str)
        self.assertIn("°C, ", weather)

if __name__ == "__main__":
    unittest.main()
