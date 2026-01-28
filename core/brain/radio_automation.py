"""
Radio Automation Skills for Neon Frequency
===========================================
AI-powered radio automation integrating with AzuraCast, ElevenLabs, and other tools.
"""

import os
import logging
import httpx
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache

logger = logging.getLogger("AEN.Radio")


@dataclass
class Track:
    """Represents a track in the radio system."""
    title: str
    artist: str
    duration: int  # seconds
    path: Optional[str] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    bpm: Optional[int] = None
    energy: Optional[float] = None  # 0.0-1.0


@dataclass
class NowPlaying:
    """Current playback state."""
    track: Track
    position: int  # seconds into track
    listeners: int
    is_live: bool
    started_at: datetime


class AzuraCastClient:
    """
    AzuraCast API Client for radio automation.
    
    Provides full control over:
    - Now playing information
    - Playlist management
    - Song requests
    - Station control
    """
    
    def __init__(self, base_url: str = None, api_key: str = None, station_id: int = 1):
        self.base_url = base_url or os.getenv("AZURACAST_URL", "http://localhost")
        self.api_key = api_key or os.getenv("AZURACAST_API_KEY", "")
        self.station_id = station_id
        self.client = httpx.Client(
            base_url=f"{self.base_url}/api",
            headers={"X-API-Key": self.api_key} if self.api_key else {},
            timeout=30.0
        )
        logger.info(f"AzuraCast client initialized for {self.base_url}")
    
    def get_now_playing(self) -> Optional[NowPlaying]:
        """Get current now playing information."""
        try:
            response = self.client.get(f"/nowplaying/{self.station_id}")
            response.raise_for_status()
            data = response.json()
            
            now_playing = data.get("now_playing", {})
            song = now_playing.get("song", {})
            
            return NowPlaying(
                track=Track(
                    title=song.get("title", "Unknown"),
                    artist=song.get("artist", "Unknown"),
                    duration=now_playing.get("duration", 0),
                    album=song.get("album", "")
                ),
                position=now_playing.get("elapsed", 0),
                listeners=data.get("listeners", {}).get("current", 0),
                is_live=data.get("live", {}).get("is_live", False),
                started_at=datetime.fromtimestamp(now_playing.get("played_at", 0))
            )
        except Exception as e:
            logger.error(f"Failed to get now playing: {e}")
            return None
    
    def get_queue(self) -> List[Track]:
        """Get upcoming tracks in queue."""
        try:
            response = self.client.get(f"/station/{self.station_id}/queue")
            response.raise_for_status()
            
            tracks = []
            for item in response.json():
                song = item.get("song", {})
                tracks.append(Track(
                    title=song.get("title", "Unknown"),
                    artist=song.get("artist", "Unknown"),
                    duration=item.get("duration", 0)
                ))
            return tracks
        except Exception as e:
            logger.error(f"Failed to get queue: {e}")
            return []
    
    def add_to_queue(self, media_id: int) -> bool:
        """Add a track to the queue by media ID."""
        try:
            response = self.client.post(
                f"/station/{self.station_id}/queue",
                json={"media_id": media_id}
            )
            response.raise_for_status()
            logger.info(f"Added media {media_id} to queue")
            return True
        except Exception as e:
            logger.error(f"Failed to add to queue: {e}")
            return False
    
    def skip_current(self) -> bool:
        """Skip the currently playing track."""
        try:
            response = self.client.post(f"/station/{self.station_id}/backend/skip")
            response.raise_for_status()
            logger.info("Skipped current track")
            return True
        except Exception as e:
            logger.error(f"Failed to skip: {e}")
            return False
    
    def get_playlists(self) -> List[Dict[str, Any]]:
        """Get all playlists for the station."""
        try:
            response = self.client.get(f"/station/{self.station_id}/playlists")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get playlists: {e}")
            return []
    
    def search_media(self, query: str) -> List[Dict[str, Any]]:
        """Search for media in the library."""
        try:
            response = self.client.get(
                f"/station/{self.station_id}/files",
                params={"searchPhrase": query}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to search media: {e}")
            return []
    
    def get_listeners(self) -> Dict[str, Any]:
        """Get listener statistics."""
        try:
            response = self.client.get(f"/station/{self.station_id}/listeners")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get listeners: {e}")
            return {}


class RadioDJClient:
    """
    RadioDJ Telnet API Client for Windows automation.
    
    Provides backup automation via RadioDJ's telnet interface.
    """
    
    def __init__(self, host: str = "localhost", port: int = 9091):
        self.host = host
        self.port = port
        logger.info(f"RadioDJ client initialized for {host}:{port}")
    
    async def send_command(self, command: str) -> str:
        """Send a command to RadioDJ via telnet."""
        import telnetlib3
        
        try:
            reader, writer = await telnetlib3.open_connection(self.host, self.port)
            writer.write(command + "\r\n")
            await writer.drain()
            response = await reader.read(1024)
            writer.close()
            return response.decode()
        except Exception as e:
            logger.error(f"RadioDJ command failed: {e}")
            return ""
    
    async def now_playing(self) -> Dict[str, str]:
        """Get current track info."""
        response = await self.send_command("NOWPLAYING")
        # Parse response: "Artist - Title"
        if " - " in response:
            artist, title = response.split(" - ", 1)
            return {"artist": artist.strip(), "title": title.strip()}
        return {"artist": "Unknown", "title": response.strip()}
    
    async def skip(self) -> bool:
        """Skip to next track."""
        response = await self.send_command("NEXT")
        return "OK" in response
    
    async def queue_track(self, track_id: int) -> bool:
        """Queue a track by ID."""
        response = await self.send_command(f"LOAD {track_id}")
        return "OK" in response


class VoiceGenerator:
    """
    AI Voice Generation using ElevenLabs.
    
    Generates DJ voiceovers, station IDs, weather reports, etc.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
        self.base_url = "https://api.elevenlabs.io/v1"
        self.default_voice = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Rachel
        
        self.client = httpx.Client(
            base_url=self.base_url,
            headers={"xi-api-key": self.api_key},
            timeout=60.0
        )
        logger.info("ElevenLabs voice generator initialized")
    
    @lru_cache(maxsize=64)
    def list_voices(self) -> List[Dict[str, str]]:
        """Get available voices."""
        try:
            response = self.client.get("/voices")
            response.raise_for_status()
            return [
                {"id": v["voice_id"], "name": v["name"]}
                for v in response.json().get("voices", [])
            ]
        except Exception as e:
            logger.error(f"Failed to list voices: {e}")
            return []
    
    def generate_audio(
        self,
        text: str,
        voice_id: str = None,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        output_path: str = None
    ) -> Optional[bytes]:
        """
        Generate speech audio from text.
        
        Args:
            text: The text to convert to speech
            voice_id: ElevenLabs voice ID (uses default if not specified)
            stability: Voice stability (0.0-1.0)
            similarity_boost: Voice clarity/similarity (0.0-1.0)
            output_path: Optional path to save the audio file
            
        Returns:
            Audio bytes in MP3 format, or None on failure
        """
        voice = voice_id or self.default_voice
        
        try:
            response = self.client.post(
                f"/text-to-speech/{voice}",
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": stability,
                        "similarity_boost": similarity_boost
                    }
                },
                headers={"Accept": "audio/mpeg"}
            )
            response.raise_for_status()
            audio_data = response.content
            
            if output_path:
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                logger.info(f"Audio saved to {output_path}")
            
            return audio_data
            
        except Exception as e:
            logger.error(f"Voice generation failed: {e}")
            return None
    
    def generate_station_id(self, station_name: str = "Neon Frequency") -> Optional[bytes]:
        """Generate a station ID voice track."""
        scripts = [
            f"You're listening to {station_name}. The future of sound.",
            f"This is {station_name}. Where the vibe never stops.",
            f"{station_name}. Your gateway to sonic dimensions.",
        ]
        import random
        return self.generate_audio(random.choice(scripts))
    
    def generate_weather_report(self, weather_data: str, location: str = "Rowville") -> Optional[bytes]:
        """Generate a weather report voice track."""
        script = f"It's currently {weather_data} in {location}. Stay cool, and keep vibing."
        return self.generate_audio(script)
    
    def generate_song_intro(self, track: Track) -> Optional[bytes]:
        """Generate an intro for an upcoming track."""
        script = f"Coming up next, {track.title} by {track.artist}. Let's go!"
        return self.generate_audio(script)


class PlaylistOptimizer:
    """
    AI-powered playlist optimization.
    
    Inspired by Super Hi-Fi's MagicStitch and NextKast's Audience Pleaser.
    """
    
    def __init__(self):
        self.energy_history: List[float] = []
        self.bpm_history: List[int] = []
        logger.info("Playlist optimizer initialized")
    
    def calculate_transition_score(self, current: Track, next_track: Track) -> float:
        """
        Calculate how well two tracks transition together.
        
        Returns a score from 0.0 (terrible) to 1.0 (perfect).
        """
        score = 0.5  # Base score
        
        # BPM matching (±10 BPM is ideal)
        if current.bpm and next_track.bpm:
            bpm_diff = abs(current.bpm - next_track.bpm)
            if bpm_diff <= 5:
                score += 0.25
            elif bpm_diff <= 10:
                score += 0.15
            elif bpm_diff > 30:
                score -= 0.2
        
        # Energy matching (smooth transitions)
        if current.energy and next_track.energy:
            energy_diff = abs(current.energy - next_track.energy)
            if energy_diff <= 0.1:
                score += 0.2
            elif energy_diff <= 0.2:
                score += 0.1
            elif energy_diff > 0.5:
                score -= 0.15
        
        # Genre matching
        if current.genre and next_track.genre:
            if current.genre == next_track.genre:
                score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def suggest_crossfade_duration(self, current: Track, next_track: Track) -> int:
        """Suggest optimal crossfade duration in milliseconds."""
        base_duration = 3000  # 3 seconds default
        
        # Adjust based on BPM
        if current.bpm and next_track.bpm:
            avg_bpm = (current.bpm + next_track.bpm) / 2
            if avg_bpm > 140:  # Fast tracks = shorter crossfade
                base_duration = 2000
            elif avg_bpm < 90:  # Slow tracks = longer crossfade
                base_duration = 5000
        
        return base_duration
    
    def optimize_queue(self, tracks: List[Track]) -> List[Track]:
        """
        Reorder tracks for optimal flow.
        
        Uses a greedy algorithm to maximize transition scores.
        """
        if len(tracks) <= 2:
            return tracks
        
        optimized = [tracks[0]]
        remaining = tracks[1:]
        
        while remaining:
            current = optimized[-1]
            # Find best next track
            scores = [
                (t, self.calculate_transition_score(current, t))
                for t in remaining
            ]
            scores.sort(key=lambda x: x[1], reverse=True)
            best_track = scores[0][0]
            
            optimized.append(best_track)
            remaining.remove(best_track)
        
        return optimized


class ShowRunner:
    """
    Showrunner agent for managing broadcast segments.
    
    Handles segment pacing, ad breaks, and tempo transitions.
    """
    
    def __init__(self, azuracast: AzuraCastClient, voice: VoiceGenerator):
        self.azuracast = azuracast
        self.voice = voice
        self.segment_duration = 15 * 60  # 15 minute segments
        self.ad_interval = 30 * 60  # 30 minutes between ad breaks
        logger.info("ShowRunner initialized")
    
    def build_hour_clock(self) -> List[Dict[str, Any]]:
        """
        Build a station clock for the current hour.
        
        Returns a list of scheduled events for the hour.
        """
        clock = []
        
        # Top of hour - Station ID
        clock.append({
            "time": 0,
            "type": "station_id",
            "duration": 10
        })
        
        # Music blocks with voice links
        for i in range(4):
            minute = i * 15
            clock.append({
                "time": minute + 1,
                "type": "music_block",
                "duration": 12 * 60,  # 12 minutes of music
                "tracks": 3
            })
            clock.append({
                "time": minute + 13,
                "type": "voice_link",
                "duration": 30
            })
        
        # Ad break at :30
        clock.append({
            "time": 30,
            "type": "ad_break",
            "duration": 3 * 60
        })
        
        return clock
    
    async def generate_voice_link(self, now_playing: NowPlaying) -> Optional[bytes]:
        """Generate a contextual voice link based on current playback."""
        scripts = [
            f"That was {now_playing.track.title} by {now_playing.track.artist}. You're locked in to Neon Frequency.",
            f"{now_playing.track.artist}, keeping the vibe alive. More heat coming up.",
            f"The future sounds good, doesn't it? {now_playing.track.title} on Neon Frequency."
        ]
        import random
        return self.voice.generate_audio(random.choice(scripts))


# Convenience function to get all clients
def get_radio_clients() -> Dict[str, Any]:
    """Initialize and return all radio automation clients."""
    return {
        "azuracast": AzuraCastClient(),
        "voice": VoiceGenerator(),
        "optimizer": PlaylistOptimizer()
    }
