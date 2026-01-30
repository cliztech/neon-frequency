"""
Rowville Weather Client
=======================
Fetches real-time weather for the station.
"""

import os
import logging
import random
import httpx
from typing import Optional

logger = logging.getLogger("AEN.Weather")

class WeatherClient:
    """
    Client for OpenWeatherMap.
    Auto-detects API key or switches to Mock Mode.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENWEATHERMAP_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        if not self.api_key:
            logger.warning("WeatherClient: No API Key found. Switching to MOCK mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self.client = httpx.Client(timeout=5.0)

    def get_weather(self, location: str = "Rowville") -> str:
        """
        Get current weather description.
        Returns string like "24°C, Sunny"
        """
        if self.mock_mode:
            return self._mock_weather(location)
            
        try:
            response = self.client.get(
                self.base_url,
                params={"q": location, "appid": self.api_key, "units": "metric"}
            )
            response.raise_for_status()
            data = response.json()
            
            temp = int(data["main"]["temp"])
            description = data["weather"][0]["description"].capitalize()
            
            return f"{temp}°C, {description}"
            
        except Exception as e:
            logger.error(f"Weather fetch failed: {e}")
            return self._mock_weather(location)

    def _mock_weather(self, location: str) -> str:
        """Generate plausible fake weather."""
        temp = random.randint(15, 35)
        conditions = [
            "Sunny", 
            "Partly Cloudy", 
            "Neon Rain", 
            "Electric Fog", 
            "Clear Night",
            "Data Storm"
        ]
        return f"{temp}°C, {random.choice(conditions)}"
