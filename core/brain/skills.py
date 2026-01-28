import logging
import random
import os
from typing import List, Dict

try:
    from langchain_community.utilities import GoogleSearchAPIWrapper
    from langchain_community.tools import GoogleSearchRun
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

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
        self.search_tool = None
        if HAS_LANGCHAIN and os.environ.get("GOOGLE_API_KEY") and os.environ.get("GOOGLE_CSE_ID"):
            try:
                wrapper = GoogleSearchAPIWrapper()
                self.search_tool = GoogleSearchRun(api_wrapper=wrapper)
            except Exception as e:
                logger.error(f"Failed to initialize Google Search: {e}")

    def get_current_trends(self) -> str:
        """Simulates fetching real-time trends."""
        if self.search_tool:
            try:
                result = self.search_tool.run("top pop culture trends today")
                logger.info(f"Real trend detected via Google: {result[:100]}...")
                return result
            except Exception as e:
                logger.error(f"Search failed: {e}")

        # Fallback to simulated trends
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
    def get_weather(location: str = "Rowville") -> str:
        # TODO: Connect to OpenWeatherMap
        temp = random.randint(30, 42)
        conditions = ["Sunny", "Heatwave", "Stormy", "Neon Rain"]
        return f"{temp}°C, {random.choice(conditions)}"
