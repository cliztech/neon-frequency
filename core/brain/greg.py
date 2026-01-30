import logging
import random
from typing import TypedDict, Dict

logger = logging.getLogger("AEN.Greg")

class GregPersona:
    """
    Greg is the rival agent.
    Vibe: 90s Hip Hop, pretentious, hates 'fast electronic noise'.
    Role: Interrupts the broadcast to roast AEN.
    """
    
    def __init__(self, weather_client=None, news_agent=None):
        self.name = "GREG"
        self.weather = weather_client
        self.news = news_agent
        
    def generate_interruption(self, current_track: str, host_last_words: str) -> str:
        """
        Generates a roast or interruption using real data if available.
        """
        logger.info(f"Greg is listening to {current_track}...")
        
        # Context gathering
        weather_roast = ""
        if self.weather:
            w = self.weather.get_weather()
            if "Rain" in w or "Storm" in w:
                weather_roast = " It's raining code out there."
        
        news_roast = ""
        if self.news:
            headlines = self.news.get_top_stories(1)
            if headlines:
                news_roast = f" Did you hear? {headlines[0]}. Boring."

        roasts = [
            f"Yo AEN, cut this noise. We need some real Boom Bap.{weather_roast}",
            f"Is this music or a modem dial-up tone? Greg is not impressed.{news_roast}",
            "Sector 7G deserves better beats. This is tinny.",
            "Stop trying to be cool, AEN. You're just python code.",
            f"I heard you say '{host_last_words}'... cringe."
        ]
        
        return random.choice(roasts)
