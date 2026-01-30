"""
Rotation Engine
===============
Handles advanced music scheduling logic, including artist separation,
track separation, and dayparting rules.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import random

from core.brain.music_library import TrackMetadata, MusicLibrary

logger = logging.getLogger("AEN.Rotation")

@dataclass
class RotationRules:
    """Rules for track selection."""
    artist_separation_minutes: int = 60
    track_separation_minutes: int = 240  # 4 hours
    same_title_separation_minutes: int = 120 # Prevent different versions of same song

    # DMCA/Performance rights rules (webcasting)
    dmca_artist_limit_3hours: int = 3 # Max 3 songs by same artist in 3 hours
    dmca_album_limit_3hours: int = 2  # Max 2 songs from same album in 3 hours


@dataclass
class PlayHistoryItem:
    """Record of a played track."""
    track: TrackMetadata
    played_at: datetime


class RotationEngine:
    """
    Engine for selecting tracks based on rotation rules.
    """

    def __init__(self, rules: RotationRules = None):
        self.rules = rules or RotationRules()
        self.history: List[PlayHistoryItem] = []

    def add_to_history(self, track: TrackMetadata, played_at: datetime):
        """Add a track to the play history."""
        self.history.append(PlayHistoryItem(track, played_at))
        # Prune history older than max separation rule (keep 24h for safety)
        cutoff = datetime.now() - timedelta(hours=24)
        self.history = [h for h in self.history if h.played_at > cutoff]

    def check_separation(self, track: TrackMetadata, simulated_time: datetime) -> bool:
        """
        Check if a track violates any separation rules.
        Returns True if allowed, False if violated.
        """
        # 1. Track Separation
        track_cutoff = simulated_time - timedelta(minutes=self.rules.track_separation_minutes)
        for item in reversed(self.history):
            if item.played_at < track_cutoff:
                break # History is sorted, so we can stop

            # Check Identity (File hash or path)
            # Ensure we don't match on None == None
            hash_match = (item.track.file_hash is not None and
                          track.file_hash is not None and
                          item.track.file_hash == track.file_hash)

            path_match = item.track.file_path == track.file_path

            if hash_match or path_match:
                logger.debug(f"Track Separation Violated: {track.title} (played at {item.played_at})")
                return False

            # Check Title (e.g., Live version vs Studio)
            if item.track.title.lower() == track.title.lower():
                 title_cutoff = simulated_time - timedelta(minutes=self.rules.same_title_separation_minutes)
                 if item.played_at > title_cutoff:
                     logger.debug(f"Title Separation Violated: {track.title}")
                     return False

        # 2. Artist Separation
        artist_cutoff = simulated_time - timedelta(minutes=self.rules.artist_separation_minutes)
        for item in reversed(self.history):
            if item.played_at < artist_cutoff:
                break

            if item.track.artist.lower() == track.artist.lower():
                logger.debug(f"Artist Separation Violated: {track.artist} (played at {item.played_at})")
                return False

        return True

    def check_dmca(self, track: TrackMetadata, simulated_time: datetime) -> bool:
        """
        Check if track violates DMCA webcasting rules.
        """
        window_start = simulated_time - timedelta(hours=3)

        artist_count = 0
        album_count = 0

        for item in reversed(self.history):
            if item.played_at < window_start:
                break

            if item.track.artist.lower() == track.artist.lower():
                artist_count += 1

            if track.album and item.track.album and item.track.album.lower() == track.album.lower():
                album_count += 1

        if artist_count >= self.rules.dmca_artist_limit_3hours:
            return False

        if album_count >= self.rules.dmca_album_limit_3hours:
            return False

        return True

    def select_track(
        self,
        candidates: List[TrackMetadata],
        simulated_time: datetime,
        enforce_dmca: bool = True
    ) -> Optional[TrackMetadata]:
        """
        Select the best track from candidates that respects rules.
        """
        # Shuffle to ensure variety among valid tracks
        pool = list(candidates)
        random.shuffle(pool)

        best_candidate = None

        for track in pool:
            # Check Hard Rules (Separation)
            if not self.check_separation(track, simulated_time):
                continue

            # Check DMCA (if enabled)
            if enforce_dmca and not self.check_dmca(track, simulated_time):
                continue

            # If passed, return immediately (since we shuffled)
            return track

        # Fallback: If strict rules block everything, try relaxing artist separation
        # This prevents "dead air" in small libraries
        logger.warning("Strict rotation rules blocked all tracks. Relaxing rules...")

        for track in pool:
            # Only check track separation (prevent immediate repeat), ignore artist
            track_cutoff = simulated_time - timedelta(minutes=self.rules.track_separation_minutes)
            last_play = next((h for h in reversed(self.history)
                            if h.track.file_path == track.file_path and h.played_at > track_cutoff), None)

            if not last_play:
                return track

        return None
