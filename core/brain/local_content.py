"""
Local Content Engine for Neon Frequency
========================================
Real-time local market awareness - fetches and processes local news,
events, trending topics, and social mentions for AI commentary.

Inspired by RadioGPT's real-time local content features.
"""

import os
import logging
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum
import json

logger = logging.getLogger("AEN.LocalContent")


class ContentType(str, Enum):
    """Types of local content."""
    NEWS = "news"
    EVENT = "event"
    TRENDING = "trending"
    SOCIAL = "social"
    WEATHER = "weather"
    TRAFFIC = "traffic"


@dataclass
class NewsItem:
    """A news article or headline."""
    title: str
    summary: str
    source: str
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    category: str = "general"
    sentiment: Optional[str] = None  # positive, negative, neutral
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "summary": self.summary,
            "source": self.source,
            "url": self.url,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "category": self.category,
            "sentiment": self.sentiment,
        }


@dataclass
class LocalEvent:
    """A local event (concert, festival, etc.)."""
    name: str
    venue: str
    date: datetime
    description: str = ""
    category: str = "general"
    ticket_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "venue": self.venue,
            "date": self.date.isoformat(),
            "description": self.description,
            "category": self.category,
            "ticket_url": self.ticket_url,
        }


@dataclass
class TrendingTopic:
    """A trending topic or hashtag."""
    topic: str
    volume: int  # Number of mentions
    trend_direction: str = "up"  # up, down, stable
    related_terms: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "volume": self.volume,
            "trend_direction": self.trend_direction,
            "related_terms": self.related_terms,
        }


@dataclass
class SocialMention:
    """A social media mention of the station."""
    platform: str  # twitter, instagram, etc.
    author: str
    content: str
    timestamp: datetime
    sentiment: str = "neutral"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform": self.platform,
            "author": self.author,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "sentiment": self.sentiment,
        }


class LocalContentEngine:
    """
    Fetches real-time local content for AI commentary.
    
    Sources:
    - News APIs (NewsAPI, RSS feeds)
    - Event APIs (Eventbrite, local sources)
    - Social trending (Twitter/X trends)
    - Station social mentions
    """
    
    def __init__(
        self,
        region: str = None,
        news_api_key: str = None,
        cache_ttl_minutes: int = 15
    ):
        self.region = region or os.getenv("LOCAL_REGION", "Melbourne, Australia")
        self.news_api_key = news_api_key or os.getenv("NEWS_API_KEY")
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        
        # In-memory cache
        self._cache: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"LocalContentEngine initialized for region: {self.region}")
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached data if not expired."""
        if key in self._cache:
            cached = self._cache[key]
            if datetime.now() - cached["timestamp"] < self.cache_ttl:
                return cached["data"]
        return None
    
    def _set_cached(self, key: str, data: Any):
        """Cache data with timestamp."""
        self._cache[key] = {
            "data": data,
            "timestamp": datetime.now()
        }
    
    async def get_local_news(
        self,
        category: str = "general",
        limit: int = 5
    ) -> List[NewsItem]:
        """
        Fetch local news headlines.
        
        Args:
            category: News category (general, entertainment, sports, tech)
            limit: Maximum number of items to return
        
        Returns:
            List of NewsItem objects
        """
        cache_key = f"news_{category}_{self.region}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached[:limit]
        
        news_items = []
        
        # Try NewsAPI if key available
        if self.news_api_key:
            try:
                news_items = await self._fetch_from_newsapi(category, limit)
            except Exception as e:
                logger.warning(f"NewsAPI fetch failed: {e}")
        
        # Fallback to mock data for demo/testing
        if not news_items:
            news_items = self._get_mock_news(category, limit)
        
        self._set_cached(cache_key, news_items)
        return news_items[:limit]
    
    async def _fetch_from_newsapi(
        self,
        category: str,
        limit: int
    ) -> List[NewsItem]:
        """Fetch news from NewsAPI.org."""
        try:
            import httpx
        except ImportError:
            logger.warning("httpx not installed, using mock data")
            return []
        
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": self.news_api_key,
            "country": "au",  # Australia
            "category": category,
            "pageSize": limit
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        items = []
        for article in data.get("articles", []):
            items.append(NewsItem(
                title=article.get("title", ""),
                summary=article.get("description", ""),
                source=article.get("source", {}).get("name", "Unknown"),
                url=article.get("url"),
                published_at=datetime.fromisoformat(
                    article.get("publishedAt", "").replace("Z", "+00:00")
                ) if article.get("publishedAt") else None,
                category=category
            ))
        
        return items
    
    def _get_mock_news(self, category: str, limit: int) -> List[NewsItem]:
        """Return mock news for demo/testing."""
        mock_data = [
            NewsItem(
                title="Local Music Festival Announces Lineup",
                summary="The annual Neon Nights festival reveals this year's headliners.",
                source="Melbourne Herald",
                category="entertainment",
                published_at=datetime.now() - timedelta(hours=2)
            ),
            NewsItem(
                title="Tech Startup Raises $10M in Funding",
                summary="Melbourne-based AI company secures Series A funding.",
                source="Tech Daily",
                category="tech",
                published_at=datetime.now() - timedelta(hours=4)
            ),
            NewsItem(
                title="Weekend Weather: Sunshine Expected",
                summary="Clear skies and warm temperatures forecast for the weekend.",
                source="Weather Bureau",
                category="general",
                published_at=datetime.now() - timedelta(hours=1)
            ),
            NewsItem(
                title="Local Band Hits Charts",
                summary="Rising stars from Rowville debut at #5 on national charts.",
                source="Music News",
                category="entertainment",
                published_at=datetime.now() - timedelta(hours=6)
            ),
            NewsItem(
                title="Community Event This Saturday",
                summary="Free outdoor concert at Knox Park this weekend.",
                source="Local Gazette",
                category="general",
                published_at=datetime.now() - timedelta(hours=3)
            ),
        ]
        
        # Filter by category if not general
        if category != "general":
            mock_data = [n for n in mock_data if n.category == category]
        
        return mock_data[:limit]
    
    async def get_trending_topics(self, limit: int = 10) -> List[TrendingTopic]:
        """
        Get trending topics for the region.
        
        Returns:
            List of TrendingTopic objects
        """
        cache_key = f"trending_{self.region}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached[:limit]
        
        # Mock trending topics for now
        topics = [
            TrendingTopic(
                topic="#MelbourneMusic",
                volume=15000,
                trend_direction="up",
                related_terms=["local artists", "live music", "festivals"]
            ),
            TrendingTopic(
                topic="#WeekendVibes",
                volume=12000,
                trend_direction="stable",
                related_terms=["relaxation", "music", "chill"]
            ),
            TrendingTopic(
                topic="#NeonFrequency",
                volume=500,
                trend_direction="up",
                related_terms=["radio", "music", "AI DJ"]
            ),
            TrendingTopic(
                topic="#SummerHits",
                volume=8000,
                trend_direction="up",
                related_terms=["summer", "music", "beach"]
            ),
        ]
        
        self._set_cached(cache_key, topics)
        return topics[:limit]
    
    async def get_local_events(
        self,
        date: datetime = None,
        category: str = "all",
        limit: int = 5
    ) -> List[LocalEvent]:
        """
        Get upcoming local events.
        
        Args:
            date: Filter by date (default: today and upcoming)
            category: Event category filter
            limit: Maximum number of events
        
        Returns:
            List of LocalEvent objects
        """
        if date is None:
            date = datetime.now()
        
        cache_key = f"events_{self.region}_{date.date()}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached[:limit]
        
        # Mock events for now
        events = [
            LocalEvent(
                name="Friday Night Live",
                venue="The Corner Hotel",
                date=datetime.now() + timedelta(days=1),
                description="Live music featuring local bands",
                category="music"
            ),
            LocalEvent(
                name="Summer Festival",
                venue="Knox Park",
                date=datetime.now() + timedelta(days=3),
                description="Free outdoor music festival",
                category="music"
            ),
            LocalEvent(
                name="DJ Workshop",
                venue="Music Academy Melbourne",
                date=datetime.now() + timedelta(days=2),
                description="Learn to mix and produce electronic music",
                category="workshop"
            ),
        ]
        
        self._set_cached(cache_key, events)
        return events[:limit]
    
    async def get_social_mentions(
        self,
        station_name: str = None,
        limit: int = 10
    ) -> List[SocialMention]:
        """
        Get social media mentions of the station.
        
        Args:
            station_name: Station name to search for
            limit: Maximum number of mentions
        
        Returns:
            List of SocialMention objects
        """
        if station_name is None:
            station_name = os.getenv("STATION_NAME", "Neon Frequency")
        
        cache_key = f"social_{station_name}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached[:limit]
        
        # Mock social mentions
        mentions = [
            SocialMention(
                platform="twitter",
                author="@musiclover",
                content=f"Loving the vibes on {station_name} right now! 🎶",
                timestamp=datetime.now() - timedelta(minutes=30),
                sentiment="positive"
            ),
            SocialMention(
                platform="instagram",
                author="@djfan",
                content=f"Best radio station in Melbourne! #{station_name.replace(' ', '')}",
                timestamp=datetime.now() - timedelta(hours=1),
                sentiment="positive"
            ),
        ]
        
        self._set_cached(cache_key, mentions)
        return mentions[:limit]
    
    def get_content_for_prompt(self) -> Dict[str, str]:
        """
        Get formatted content for prompt variable substitution.
        
        Returns:
            Dictionary of variable names to values
        """
        import asyncio
        
        # Run async fetches
        loop = asyncio.new_event_loop()
        try:
            news = loop.run_until_complete(self.get_local_news(limit=3))
            trending = loop.run_until_complete(self.get_trending_topics(limit=3))
            events = loop.run_until_complete(self.get_local_events(limit=2))
        finally:
            loop.close()
        
        # Format for prompts
        news_text = "; ".join([n.title for n in news]) if news else "No news available"
        trending_text = ", ".join([t.topic for t in trending]) if trending else "No trends"
        events_text = "; ".join([f"{e.name} at {e.venue}" for e in events]) if events else "No events"
        
        return {
            "{{LOCAL_NEWS}}": news_text,
            "{{TRENDING_TOPICS}}": trending_text,
            "{{LOCAL_EVENTS}}": events_text,
            "{{REGION}}": self.region,
        }
    
    def clear_cache(self):
        """Clear all cached data."""
        self._cache = {}
        logger.info("Local content cache cleared")


# Singleton instance
_local_content_engine: Optional[LocalContentEngine] = None


def get_local_content_engine() -> LocalContentEngine:
    """Get the default local content engine instance."""
    global _local_content_engine
    if _local_content_engine is None:
        _local_content_engine = LocalContentEngine()
    return _local_content_engine
