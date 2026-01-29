"""
News Agent
==========
Fetches latest headlines for the station.
"""

import logging
import random
import os
import httpx
from typing import List

logger = logging.getLogger("AEN.News")

class NewsAgent:
    """
    Fetches news from RSS or APIs.
    Mock Mode: Generates fake cyberpunk/tech news.
    """
    
    def __init__(self):
        self.rss_urls = [
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.theverge.com/rss/index.xml"
        ]
        self.mock_mode = os.getenv("NEWS_API_MOCK", "true").lower() == "true"
        
    def get_top_stories(self, limit: int = 5) -> List[str]:
        """Get list of headline strings."""
        if self.mock_mode:
            return self._mock_headlines(limit)
            
        # Real implementation would parse RSS here
        # For now, we default to mock to keep it simple unless we add feedparser dependency
        return self._mock_headlines(limit)

    def _mock_headlines(self, limit: int) -> List[str]:
        """Generate fake headlines."""
        templates = [
            "AI Model writes symphony in 3 seconds",
            "Mars Colony 4 reports oxygen surplus",
            "Neural Link beta testing enters phase 3",
            "Old internet archive discovered in underwater server",
            "Hacker group 'Ghost Shell' releases open source toaster",
            "Local cat becomes mayor of digital town",
            "Flying cars delayed again due to gravity bug",
            "Python 5.0 released: It just reads your mind",
            "Coffee prices drop as synthetic caffeine takes over",
            "New color discovered by quantum computer"
        ]
        return random.sample(templates, min(limit, len(templates)))
