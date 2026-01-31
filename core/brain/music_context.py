"""
Music Context Provider for Neon Frequency
==========================================
Enriches track information with artist facts, song trivia,
and contextual data for AI-powered commentary.

Inspired by RadioGPT's music log awareness feature.
"""

import os
import logging
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import random

logger = logging.getLogger("AEN.MusicContext")


@dataclass
class ChartInfo:
    """Chart/ranking information for a song."""
    peak_position: int
    chart_name: str
    weeks_on_chart: int
    current_position: Optional[int] = None
    entry_date: Optional[datetime] = None


@dataclass
class MusicContext:
    """
    Rich context about current/upcoming music.
    
    Provides AI-friendly information for generating engaging commentary.
    """
    title: str
    artist: str
    album: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    
    # Enriched data
    artist_facts: List[str] = field(default_factory=list)
    song_trivia: List[str] = field(default_factory=list)
    similar_artists: List[str] = field(default_factory=list)
    chart_history: Optional[ChartInfo] = None
    
    # Station-specific
    last_played: Optional[datetime] = None
    play_count: int = 0
    listener_favorites: bool = False
    
    def get_random_artist_fact(self) -> str:
        """Get a random artist fact or default message."""
        if self.artist_facts:
            return random.choice(self.artist_facts)
        return f"{self.artist} is an amazing artist"
    
    def get_random_song_trivia(self) -> str:
        """Get a random song trivia or default message."""
        if self.song_trivia:
            return random.choice(self.song_trivia)
        return f"Here's '{self.title}'"
    
    def get_last_played_humanized(self) -> str:
        """Get human-readable time since last played."""
        if not self.last_played:
            return "first time playing this one"
        
        delta = datetime.now() - self.last_played
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hours ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "just a moment ago"
    
    def get_similar_artists_text(self) -> str:
        """Get formatted similar artists string."""
        if not self.similar_artists:
            return ""
        if len(self.similar_artists) == 1:
            return self.similar_artists[0]
        return ", ".join(self.similar_artists[:-1]) + f" and {self.similar_artists[-1]}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "year": self.year,
            "genre": self.genre,
            "artist_facts": self.artist_facts,
            "song_trivia": self.song_trivia,
            "similar_artists": self.similar_artists,
            "chart_history": {
                "peak_position": self.chart_history.peak_position,
                "chart_name": self.chart_history.chart_name,
                "weeks_on_chart": self.chart_history.weeks_on_chart,
            } if self.chart_history else None,
            "last_played": self.last_played.isoformat() if self.last_played else None,
            "play_count": self.play_count,
            "listener_favorites": self.listener_favorites,
        }


class MusicContextProvider:
    """
    Enriches track information with AI-friendly context.
    
    Features:
    - Artist biography snippets
    - Song trivia and backstory
    - Similar artist recommendations
    - Chart history
    - Station play statistics
    """
    
    def __init__(self, music_facts_path: str = None):
        self.music_facts_path = music_facts_path
        self._facts_cache: Dict[str, List[str]] = {}
        self._play_history: Dict[str, Dict[str, Any]] = {}
        
        # Pre-loaded artist facts database (expandable)
        self._artist_facts_db = {
            "Default": [
                "This artist has been making waves in the music scene",
                "Known for their unique sound and style",
                "A fan favorite here at Neon Frequency",
            ],
        }
        
        # Pre-loaded song facts database
        self._song_trivia_db = {
            "Default": [
                "This track has been climbing the charts",
                "A perfect song for this time of day",
                "One of our most requested tracks",
            ],
        }
        
        logger.info("MusicContextProvider initialized")
    
    async def get_context(self, title: str, artist: str) -> MusicContext:
        """
        Get full context for a track.
        
        Args:
            title: Song title
            artist: Artist name
        
        Returns:
            MusicContext with enriched data
        """
        context = MusicContext(
            title=title,
            artist=artist
        )
        
        # Get artist facts
        context.artist_facts = await self._get_artist_facts(artist)
        
        # Get song trivia
        context.song_trivia = await self._get_song_trivia(title, artist)
        
        # Get similar artists
        context.similar_artists = await self._get_similar_artists(artist)
        
        # Get play history from station
        history = self._get_play_history(title, artist)
        context.last_played = history.get("last_played")
        context.play_count = history.get("play_count", 0)
        
        return context
    
    async def get_artist_bio(self, artist: str) -> str:
        """
        Get a brief artist biography.
        
        Args:
            artist: Artist name
        
        Returns:
            Biography string suitable for DJ commentary
        """
        # In a full implementation, this would query a music database
        # For now, generate a generic bio
        facts = await self._get_artist_facts(artist)
        if facts:
            return f"{artist} - {facts[0]}"
        return f"{artist} is a talented artist bringing great music to our airwaves."
    
    async def get_song_story(self, title: str, artist: str) -> str:
        """
        Get the story behind a song.
        
        Args:
            title: Song title
            artist: Artist name
        
        Returns:
            Story/trivia about the song
        """
        trivia = await self._get_song_trivia(title, artist)
        if trivia:
            return trivia[0]
        return f"'{title}' by {artist} - a track that always hits the right note."
    
    async def _get_artist_facts(self, artist: str) -> List[str]:
        """Get facts about an artist."""
        # Check cache
        if artist in self._facts_cache:
            return self._facts_cache[artist]
        
        # Check local database
        if artist in self._artist_facts_db:
            facts = self._artist_facts_db[artist]
        else:
            # Use default facts with artist name inserted
            facts = [
                f"{artist} has been creating incredible music",
                f"One of the most exciting artists in their genre",
                f"{artist}'s unique style has garnered a dedicated fanbase",
            ]
        
        self._facts_cache[artist] = facts
        return facts
    
    async def _get_song_trivia(self, title: str, artist: str) -> List[str]:
        """Get trivia about a song."""
        key = f"{artist}:{title}"
        
        if key in self._song_trivia_db:
            return self._song_trivia_db[key]
        
        # Generate contextual trivia
        return [
            f"'{title}' showcases {artist}'s signature sound",
            f"This track has become a staple in our rotation",
            f"'{title}' - the perfect track for this moment",
        ]
    
    async def _get_similar_artists(self, artist: str) -> List[str]:
        """Get similar artists for recommendations."""
        # In a full implementation, this would use a music recommendation API
        # For now, return empty list
        return []
    
    def _get_play_history(self, title: str, artist: str) -> Dict[str, Any]:
        """Get station play history for a track."""
        key = f"{artist}:{title}"
        return self._play_history.get(key, {})
    
    def record_play(self, title: str, artist: str):
        """Record that a track was played."""
        key = f"{artist}:{title}"
        if key not in self._play_history:
            self._play_history[key] = {"play_count": 0}
        
        self._play_history[key]["play_count"] += 1
        self._play_history[key]["last_played"] = datetime.now()
    
    def add_artist_facts(self, artist: str, facts: List[str]):
        """Add facts about an artist to the database."""
        if artist in self._artist_facts_db:
            self._artist_facts_db[artist].extend(facts)
        else:
            self._artist_facts_db[artist] = facts
        logger.info(f"Added {len(facts)} facts for artist: {artist}")
    
    def add_song_trivia(self, title: str, artist: str, trivia: List[str]):
        """Add trivia about a song to the database."""
        key = f"{artist}:{title}"
        if key in self._song_trivia_db:
            self._song_trivia_db[key].extend(trivia)
        else:
            self._song_trivia_db[key] = trivia
        logger.info(f"Added {len(trivia)} trivia items for: {title} by {artist}")


# Singleton instance
_music_context_provider: Optional[MusicContextProvider] = None


def get_music_context_provider() -> MusicContextProvider:
    """Get the default music context provider instance."""
    global _music_context_provider
    if _music_context_provider is None:
        _music_context_provider = MusicContextProvider()
    return _music_context_provider


# Convenience function for prompt variable substitution
def get_music_context_variables(title: str, artist: str) -> Dict[str, str]:
    """
    Get music context formatted for prompt variables.
    
    Args:
        title: Song title
        artist: Artist name
    
    Returns:
        Dictionary of variable names to values
    """
    provider = get_music_context_provider()
    
    # Run async
    loop = asyncio.new_event_loop()
    try:
        context = loop.run_until_complete(provider.get_context(title, artist))
    finally:
        loop.close()
    
    return {
        "{{ARTIST_FACT}}": context.get_random_artist_fact(),
        "{{SONG_TRIVIA}}": context.get_random_song_trivia(),
        "{{LAST_PLAYED}}": context.get_last_played_humanized(),
        "{{SIMILAR_ARTISTS}}": context.get_similar_artists_text(),
        "{{SONG_TITLE}}": title,
        "{{SONG_ARTIST}}": artist,
        "{{PLAY_COUNT}}": str(context.play_count),
    }
