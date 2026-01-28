import logging
import random
import os
import httpx
from typing import List, Dict

# In a real scenario, we would use:
# from langchain_community.tools import GoogleSearchRun

logger = logging.getLogger("AEN.Skills")

class TrendWatcher:
    """The eyes and ears of the station."""
    
    def __init__(self):
        self.trends = [
            "Hyper-Pop revival",
            "AI-generated Jazz",
            "Cyberpunk aesthetics in UI design",
            "The weather in Sector 7G",
            "Retro-gaming soundtracks"
        ]

    async def get_current_trends(self) -> str:
        """Simulates fetching real-time trends."""
        # TODO: Implement real Perplexity/Google Search here
        trend = random.choice(self.trends)
        logger.info(f"Trend detected: {trend}")
        return trend

    def search_music(self, query: str) -> List[str]:
        """Simulates finding music based on a query."""
        logger.info(f"Searching for: {query}")
        return [f"{query}_remix.mp3", f"{query}_speed_up.mp3"]

class WeatherStation:
    """Real-time weather data."""
    
    @staticmethod
    async def get_weather(location: str = "Rowville") -> str:
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")

        if api_key:
            try:
                # Use httpx for async request
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"https://api.openweathermap.org/data/2.5/weather",
                        params={"q": location, "appid": api_key, "units": "metric"},
                        timeout=5.0
                    )
                    response.raise_for_status()
                    data = response.json()

                temp = data["main"]["temp"]
                # Capitalize first letter of description for better readability
                description = data["weather"][0]["description"].capitalize()
                return f"{temp}°C, {description}"

            except Exception as e:
                logger.error(f"Failed to fetch weather data: {e}")
        else:
            logger.warning("OPENWEATHERMAP_API_KEY not found. Using random fallback data.")

        # Fallback to random data
        temp = random.randint(30, 42)
        conditions = ["Sunny", "Heatwave", "Stormy", "Neon Rain"]
        return f"{temp}°C, {random.choice(conditions)}"
