"""
Radio Scheduler
===============
AI-driven scheduler that generates daily playlists with voice tracking,
weather, news, and music.
"""

import os
import logging
import random
from datetime import datetime, timedelta
from typing import List, Optional
from pathlib import Path

# Imports
from core.brain.content_engine import ContentEngine, ShowProducer, ContentContext, DJPersonality
from core.brain.voice_generator import ElevenLabsClient
from core.brain.weather_client import WeatherClient
from core.brain.agents.news_agent import NewsAgent
from core.brain.music_library import MusicLibrary, TrackMetadata, Genre
from core.brain.playlist_manager import PlaylistManager
from core.brain.voice_mixer import get_voice_mixer

logger = logging.getLogger("AEN.Scheduler")

class RadioScheduler:
    """
    The Master Scheduler.
    Generates ready-to-play M3U playlists with interleaved AI voice tracks.
    """
    
    def __init__(self, library_path: str = None, audio_output_dir: str = None):
        self.library = MusicLibrary(library_path)
        self.voice = ElevenLabsClient()
        self.weather = WeatherClient()
        self.news = NewsAgent()
        
        # Audio output for generated voice tracks
        self.audio_dir = Path(audio_output_dir or os.getenv("AUDIO_OUTPUT_DIR", "./generated_audio"))
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Content Engines for different dayparts
        self.engine_morning = ContentEngine() # Default AEN
        self.producer = ShowProducer(self.engine_morning)
        
    def _generate_audio_file(self, text: str, prefix: str = "voice") -> Optional[str]:
        """
        Generate audio from text and save to disk.
        Returns the absolute path to the file.
        """
        if not text:
            return None

        # Create a filename based on hash of text to avoid re-generating same lines
        import hashlib
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        filename = f"{prefix}_{text_hash}.mp3"
        filepath = self.audio_dir / filename
        
        # If exists, return cached
        if filepath.exists():
            return str(filepath.absolute())

        # Generate
        audio_data = self.voice.generate(text)
        if audio_data:
            with open(filepath, "wb") as f:
                f.write(audio_data)
            return str(filepath.absolute())

        return None

    def _create_voice_track(self, text: str, title: str = "Voice Track") -> Optional[TrackMetadata]:
        """Create a TrackMetadata object for a voice track."""
        filepath = self._generate_audio_file(text)
        if not filepath:
            return None

        # Get duration (mocking or reading file)
        # TODO: Use mutagen or similar to read exact duration from the generated MP3 file
        # For simplicity, we estimate duration based on word count (avg 150 wpm)
        word_count = len(text.split())
        duration = max(2, int((word_count / 150) * 60))

        return TrackMetadata(
            file_path=filepath,
            title=title,
            artist="AI DJ",
            duration_seconds=duration,
            genre=Genre.OTHER,
            is_generated=True,
            generation_prompt=text
        )

    def generate_hour_block(self, hour: int, output_dir: str) -> str:
        """
        Generate a 1-hour playlist M3U file.
        Returns the path to the generated playlist.
        """
        logger.info(f"Generating schedule for Hour {hour:02d}...")
        
        # 1. Context
        weather_data = self.weather.get_weather()
        headlines = self.news.get_top_stories(1)
        
        # Determine Mood/Time
        time_of_day = "night"
        if 5 <= hour < 12: time_of_day = "morning"
        elif 12 <= hour < 17: time_of_day = "afternoon"
        elif 17 <= hour < 21: time_of_day = "evening"
        
        context = ContentContext(
            weather=weather_data,
            trending_topics=headlines,
            time_of_day=time_of_day,
            mood="energetic" if 8 <= hour <= 20 else "chill"
        )
        
        # 2. Get Content Script Package
        package = self.producer.generate_hourly_package(context)
        
        # 3. Assemble Playlist Tracks
        playlist_tracks: List[TrackMetadata] = []
        
        # -- Top of Hour ID --
        track = self._create_voice_track(package["top_of_hour_id"], "Station ID")
        if track: playlist_tracks.append(track)
        
        # -- Weather Update --
        track = self._create_voice_track(package["weather_update"], "Weather Update")
        if track: playlist_tracks.append(track)
        
        # -- Music Block 1 --
        # Try to get real music, otherwise mock
        music_tracks = self.library.get_rotation_picks(count=15) # Grab enough for the hour
        if not music_tracks:
            # Create dummy music tracks for demo
            music_tracks = [
                TrackMetadata(f"/music/demo_track_{i}.mp3", f"Demo Track {i}", "Unknown Artist", duration_seconds=180)
                for i in range(1, 15)
            ]
        
        music_idx = 0
        
        # Loop to fill the hour
        # Structure: Music -> Music -> Music -> Voice Intro -> Music
        
        script_intros = package["song_intros"]

        # Block 1 (3 songs)
        for _ in range(3):
            if music_idx < len(music_tracks):
                playlist_tracks.append(music_tracks[music_idx])
                music_idx += 1

        # -- News Brief --
        track = self._create_voice_track(package["news_brief"], "News Update")
        if track: playlist_tracks.append(track)

        # -- Block 2 (Music with intros) --
        for i in range(3):
            if music_idx < len(music_tracks):
                song = music_tracks[music_idx]

                # Insert Intro if available
                if i < len(script_intros):
                    # RAMP AWARENESS LOGIC
                    ramp_seconds = song.intro_seconds

                    # Simulate ramp for demo purposes if not set (or 0)
                    if ramp_seconds == 0 and "Demo Track" in song.title:
                        ramp_seconds = random.uniform(5.0, 15.0)

                    mixed_success = False

                    # Attempt "Voice Over Intro" mixing if we have enough ramp
                    if ramp_seconds > 5.0:
                        try:
                            # 1. Generate Constrained Script
                            intro_text = self.engine_morning.generate_constrained_intro(
                                ContentContext(weather=weather_data, next_track=song.title, time_of_day=time_of_day),
                                max_seconds=ramp_seconds - 1.0  # Leave 1s buffer
                            )

                            # 2. Generate Voice Audio
                            voice_track = self._create_voice_track(intro_text, f"Intro: {song.title}")

                            if voice_track:
                                # 3. Mix
                                mixer = get_voice_mixer()
                                # Synchronous call
                                mixed_path = mixer.mix_over_intro(
                                    voice_track.file_path,
                                    song.file_path,
                                    ramp_seconds
                                )

                                if mixed_path:
                                    # Create metadata for the mixed track
                                    mixed_song = TrackMetadata(
                                        file_path=mixed_path,
                                        title=song.title,
                                        artist=song.artist,
                                        duration_seconds=song.duration_seconds,
                                        intro_seconds=0, # Ramp used
                                        is_generated=True,
                                        generation_prompt="Voice Over Ramp Mix"
                                    )
                                    playlist_tracks.append(mixed_song)
                                    mixed_success = True
                        except Exception as e:
                            logger.error(f"Ramp mixing failed: {e}")

                    if not mixed_success:
                        # Fallback: Stop Set (Voice then Song)
                        # We need to regenerate intro specifically for THIS song to be accurate
                        intro_text = self.engine_morning.generate_song_intro(
                            ContentContext(weather=weather_data, next_track=song.title, time_of_day=time_of_day)
                        )
                        intro = self._create_voice_track(intro_text, f"Intro: {song.title}")
                        if intro: playlist_tracks.append(intro)
                        playlist_tracks.append(song)

                else:
                    playlist_tracks.append(song)

                music_idx += 1

        # -- Ad Break --
        track = self._create_voice_track(package["ad_lead_in"], "Ad Break Lead-in")
        if track: playlist_tracks.append(track)

        # (Insert Ad Placeholder)
        playlist_tracks.append(TrackMetadata("/ads/dummy_ad.mp3", "Sponsor Message", "Sponsor", duration_seconds=30))

        track = self._create_voice_track(package["ad_lead_out"], "Ad Break Lead-out")
        if track: playlist_tracks.append(track)

        # -- Remaining Music --
        while music_idx < len(music_tracks) and music_idx < 12: # Limit to ~12 songs/hr
            playlist_tracks.append(music_tracks[music_idx])
            music_idx += 1

        # 4. Export
        filename = f"hour_{hour:02d}.m3u"
        output_path = os.path.join(output_dir, filename)
        PlaylistManager.export_m3u(playlist_tracks, output_path)

        return output_path

    def generate_daily_schedule(self, output_dir: str):
        """Generate 24 playlists for the day."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        generated_files = []
        for hour in range(24):
            path = self.generate_hour_block(hour, output_dir)
            generated_files.append(path)

        logger.info(f"Daily schedule generated in {output_dir}")
        return generated_files
