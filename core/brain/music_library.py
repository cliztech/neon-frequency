"""
Music Library Manager for Neon Frequency
==========================================
Handles music catalog, metadata, BPM analysis, and smart playlist generation.
"""

import os
import logging
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger("AEN.MusicLibrary")


class Genre(Enum):
    """Music genre categories."""
    ELECTRONIC = "electronic"
    SYNTHWAVE = "synthwave"
    TRANCE = "trance"
    HOUSE = "house"
    TECHNO = "techno"
    DRUM_AND_BASS = "drum_and_bass"
    HAPPY_HARDCORE = "happy_hardcore"
    AMBIENT = "ambient"
    LOFI = "lofi"
    HIP_HOP = "hip_hop"
    POP = "pop"
    ROCK = "rock"
    OTHER = "other"


class Energy(Enum):
    """Track energy levels."""
    LOW = 1
    MEDIUM_LOW = 2
    MEDIUM = 3
    MEDIUM_HIGH = 4
    HIGH = 5


@dataclass
class TrackMetadata:
    """Complete metadata for a music track."""
    file_path: str
    title: str
    artist: str
    album: Optional[str] = None
    genre: Genre = Genre.OTHER
    bpm: Optional[int] = None
    key: Optional[str] = None  # e.g., "Am", "C#m"
    duration_seconds: int = 0
    energy: Energy = Energy.MEDIUM
    year: Optional[int] = None
    
    # Audio properties
    sample_rate: int = 44100
    bitrate: int = 320
    loudness_lufs: Optional[float] = None  # Integrated loudness
    
    # Scheduling metadata
    last_played: Optional[datetime] = None
    play_count: int = 0
    rotation_category: str = "normal"  # hot, normal, recurrent, gold
    
    # Smart features
    intro_seconds: float = 0.0  # Time before vocals/main
    outro_seconds: float = 0.0  # Fade out duration
    hook_start: Optional[float] = None  # Best part for promos
    
    # Tags
    tags: List[str] = field(default_factory=list)
    mood: List[str] = field(default_factory=list)  # e.g., ["uplifting", "dark"]

    # AI Generation Metadata
    is_generated: bool = False
    generation_source: Optional[str] = None  # e.g., "lyria-2", "suno", "elevenlabs"
    generation_prompt: Optional[str] = None
    
    # File hash for deduplication
    file_hash: Optional[str] = None
    
    def matches_search(self, query: str) -> bool:
        """Check if track matches a search query."""
        query = query.lower()
        searchable = f"{self.title} {self.artist} {self.album or ''} {' '.join(self.tags)}".lower()
        if self.is_generated:
            searchable += f" {self.generation_prompt or ''} generated"
        return query in searchable


@dataclass
class Playlist:
    """A collection of tracks."""
    name: str
    tracks: List[TrackMetadata] = field(default_factory=list)
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    is_smart: bool = False
    smart_rules: Dict[str, Any] = field(default_factory=dict)
    
    def add_track(self, track: TrackMetadata):
        """Add a track to the playlist."""
        self.tracks.append(track)
    
    @property
    def total_duration(self) -> int:
        """Total duration in seconds."""
        return sum(t.duration_seconds for t in self.tracks)
    
    @property
    def track_count(self) -> int:
        return len(self.tracks)


class MusicLibrary:
    """
    Central music library manager.
    
    Features:
    - Track catalog with full metadata
    - BPM and key analysis integration
    - Smart playlist generation
    - Rotation scheduling
    - Duplicate detection
    """
    
    def __init__(self, music_dir: str = None):
        self.music_dir = music_dir or os.getenv("MUSIC_DIR", "/music")
        self.tracks: Dict[str, TrackMetadata] = {}  # hash -> metadata
        self.playlists: Dict[str, Playlist] = {}
        logger.info(f"Music library initialized: {self.music_dir}")
    
    def scan_directory(self, path: str = None) -> int:
        """Scan a directory for music files."""
        scan_path = Path(path or self.music_dir)
        extensions = {'.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac'}
        found = 0
        
        if not scan_path.exists():
            logger.warning(f"Music directory not found: {scan_path}")
            return 0
        
        for file_path in scan_path.rglob('*'):
            if file_path.suffix.lower() in extensions:
                try:
                    track = self._create_track_from_file(str(file_path))
                    self.add_track(track)
                    found += 1
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {e}")
        
        logger.info(f"Scanned {found} tracks from {scan_path}")
        return found
    
    def _create_track_from_file(self, file_path: str) -> TrackMetadata:
        """Create track metadata from a file."""
        path = Path(file_path)
        
        # Calculate file hash for deduplication
        file_hash = self._hash_file(file_path)
        
        # Basic metadata from filename (artist - title.ext pattern)
        filename = path.stem
        if " - " in filename:
            artist, title = filename.split(" - ", 1)
        else:
            artist = "Unknown Artist"
            title = filename
        
        # TODO: Use mutagen or similar for real metadata extraction
        return TrackMetadata(
            file_path=file_path,
            title=title.strip(),
            artist=artist.strip(),
            file_hash=file_hash,
            genre=self._guess_genre_from_path(file_path)
        )
    
    def _hash_file(self, file_path: str) -> str:
        """Generate a hash for file deduplication."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            # Only hash first 1MB for speed
            hasher.update(f.read(1024 * 1024))
        return hasher.hexdigest()
    
    def _guess_genre_from_path(self, path: str) -> Genre:
        """Guess genre from folder structure."""
        path_lower = path.lower()
        
        genre_map = {
            'synthwave': Genre.SYNTHWAVE,
            'trance': Genre.TRANCE,
            'house': Genre.HOUSE,
            'techno': Genre.TECHNO,
            'dnb': Genre.DRUM_AND_BASS,
            'drum': Genre.DRUM_AND_BASS,
            'hardcore': Genre.HAPPY_HARDCORE,
            'ambient': Genre.AMBIENT,
            'lofi': Genre.LOFI,
            'lo-fi': Genre.LOFI,
            'hip-hop': Genre.HIP_HOP,
            'hiphop': Genre.HIP_HOP,
            'electronic': Genre.ELECTRONIC
        }
        
        for keyword, genre in genre_map.items():
            if keyword in path_lower:
                return genre
        
        return Genre.OTHER
    
    def add_track(self, track: TrackMetadata):
        """Add a track to the library."""
        if track.file_hash and track.file_hash in self.tracks:
            logger.debug(f"Duplicate track skipped: {track.title}")
            return
        
        key = track.file_hash or track.file_path
        self.tracks[key] = track
    
    def search(self, query: str, limit: int = 50) -> List[TrackMetadata]:
        """Search tracks by query."""
        results = [t for t in self.tracks.values() if t.matches_search(query)]
        return results[:limit]
    
    def get_by_genre(self, genre: Genre, limit: int = 50) -> List[TrackMetadata]:
        """Get tracks by genre."""
        results = [t for t in self.tracks.values() if t.genre == genre]
        return results[:limit]
    
    def get_by_bpm_range(self, min_bpm: int, max_bpm: int) -> List[TrackMetadata]:
        """Get tracks within a BPM range."""
        return [
            t for t in self.tracks.values()
            if t.bpm and min_bpm <= t.bpm <= max_bpm
        ]
    
    def get_by_energy(self, energy: Energy) -> List[TrackMetadata]:
        """Get tracks by energy level."""
        return [t for t in self.tracks.values() if t.energy == energy]
    
    def find_similar_tracks(self, track: TrackMetadata, limit: int = 10) -> List[TrackMetadata]:
        """Find tracks similar to the given track."""
        candidates = []
        
        for t in self.tracks.values():
            if t.file_hash == track.file_hash:
                continue
            
            score = 0
            
            # Same genre = +3
            if t.genre == track.genre:
                score += 3
            
            # Similar BPM (±10) = +2
            if t.bpm and track.bpm and abs(t.bpm - track.bpm) <= 10:
                score += 2
            
            # Same energy = +2
            if t.energy == track.energy:
                score += 2
            
            # Same key = +1 (harmonic mixing)
            if t.key and track.key and t.key == track.key:
                score += 1
            
            if score > 0:
                candidates.append((score, t))
        
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [t for _, t in candidates[:limit]]
    
    def create_smart_playlist(
        self,
        name: str,
        duration_minutes: int = 60,
        genre: Genre = None,
        energy: Energy = None,
        bpm_range: tuple = None
    ) -> Playlist:
        """Create a smart playlist based on criteria."""
        playlist = Playlist(
            name=name,
            is_smart=True,
            smart_rules={
                "genre": genre.value if genre else None,
                "energy": energy.value if energy else None,
                "bpm_range": bpm_range
            }
        )
        
        candidates = list(self.tracks.values())
        
        # Apply filters
        if genre:
            candidates = [t for t in candidates if t.genre == genre]
        if energy:
            candidates = [t for t in candidates if t.energy == energy]
        if bpm_range:
            candidates = [t for t in candidates if t.bpm and bpm_range[0] <= t.bpm <= bpm_range[1]]
        
        # Fill playlist to target duration
        import random
        random.shuffle(candidates)
        
        target_seconds = duration_minutes * 60
        current_duration = 0
        
        for track in candidates:
            if current_duration >= target_seconds:
                break
            playlist.add_track(track)
            current_duration += track.duration_seconds
        
        logger.info(f"Created smart playlist '{name}' with {playlist.track_count} tracks")
        return playlist
    
    def get_rotation_picks(self, category: str = "hot", count: int = 10) -> List[TrackMetadata]:
        """Get tracks from a rotation category."""
        candidates = [t for t in self.tracks.values() if t.rotation_category == category]
        import random
        return random.sample(candidates, min(count, len(candidates)))
    
    def update_play_count(self, track_hash: str):
        """Update play count and last played time."""
        if track_hash in self.tracks:
            self.tracks[track_hash].play_count += 1
            self.tracks[track_hash].last_played = datetime.now()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get library statistics."""
        genres = {}
        for t in self.tracks.values():
            genres[t.genre.value] = genres.get(t.genre.value, 0) + 1
        
        return {
            "total_tracks": len(self.tracks),
            "total_playlists": len(self.playlists),
            "genres": genres,
            "total_duration_hours": sum(t.duration_seconds for t in self.tracks.values()) / 3600
        }


# Convenience function
def get_library(music_dir: str = None) -> MusicLibrary:
    """Get a configured music library instance."""
    return MusicLibrary(music_dir)
