import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import os
from core.brain.skills import WeatherStation

class TestWeatherStation(unittest.IsolatedAsyncioTestCase):

    @patch('core.brain.skills.httpx.AsyncClient')
    @patch('core.brain.skills.os.getenv')
    async def test_get_weather_success(self, mock_getenv, mock_client_cls):
        # Mock API Key
        mock_getenv.return_value = "fake_api_key"

        # Mock API Response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 25.5},
            "weather": [{"description": "clear sky"}]
        }
        mock_response.raise_for_status = MagicMock()

        # Mock Client
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_client_cls.return_value = mock_client

        weather = await WeatherStation.get_weather("TestCity")

        # Assertions
        mock_client.get.assert_called_with(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": "TestCity", "appid": "fake_api_key", "units": "metric"},
            timeout=5.0
        )
        self.assertEqual(weather, "25.5°C, Clear sky")

    @patch('core.brain.skills.os.getenv')
    async def test_get_weather_no_api_key(self, mock_getenv):
        # Mock missing API Key
        mock_getenv.return_value = None

        weather = await WeatherStation.get_weather("Rowville")

        # Should return the random fallback format
        # e.g. "35°C, Sunny"
        self.assertIsInstance(weather, str)
        self.assertIn("°C, ", weather)

    @patch('core.brain.skills.httpx.AsyncClient')
    @patch('core.brain.skills.os.getenv')
    async def test_get_weather_api_failure(self, mock_getenv, mock_client_cls):
        # Mock API Key
        mock_getenv.return_value = "fake_api_key"

        # Mock API Failure
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("API Error")
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_client_cls.return_value = mock_client

        weather = await WeatherStation.get_weather("Rowville")

        # Should return the random fallback format
        self.assertIsInstance(weather, str)
        self.assertIn("°C, ", weather)

if __name__ == "__main__":
    unittest.main()
