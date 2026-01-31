"""
Voice Mixer for Neon Frequency
==============================
Audio mixing for voice tracks with music beds.
Provides intro/outro music, background ducking, and smooth transitions.

Inspired by RadioGPT's Virtual Announcer with music bed features.
"""

import os
import logging
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pathlib import Path
import tempfile

logger = logging.getLogger("AEN.VoiceMixer")


@dataclass
class BedConfig:
    """Configuration for a music bed."""
    name: str
    file_path: str
    style: str  # energetic, chill, news, promo
    bpm: Optional[int] = None
    duration: Optional[float] = None


@dataclass
class MixSettings:
    """Settings for voice + bed mixing."""
    intro_duration: float = 2.0  # Seconds of intro before voice starts
    outro_duration: float = 2.0  # Seconds of outro after voice ends
    bed_volume: float = -12.0  # dB level for background bed
    voice_volume: float = 0.0  # dB level for voice
    crossfade_duration: float = 0.5  # Seconds for fade transitions
    ducking_attack: float = 0.1  # Seconds to duck bed when voice starts
    ducking_release: float = 0.3  # Seconds to restore bed after voice ends


class VoiceMixer:
    """
    Mixes TTS voiceovers with music beds.
    
    Features:
    - Intro music with crossfade to speech
    - Background music with automatic ducking
    - Outro music with fade-out
    - Multiple bed styles (energetic, chill, news, promo)
    """
    
    def __init__(self, beds_directory: str = None):
        self.beds_directory = beds_directory or os.getenv(
            "MUSIC_BEDS_DIR",
            os.path.join(os.path.dirname(__file__), "..", "..", "broadcast", "beds")
        )
        self.output_directory = os.getenv(
            "VOICE_OUTPUT_DIR",
            os.path.join(os.path.dirname(__file__), "..", "..", "broadcast", "output")
        )
        
        # Ensure output directory exists
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
        
        # Available bed styles
        self._beds: Dict[str, BedConfig] = {}
        self._load_beds()
        
        logger.info(f"VoiceMixer initialized with {len(self._beds)} beds")
    
    def _load_beds(self):
        """Load available music beds from directory."""
        if not os.path.exists(self.beds_directory):
            logger.warning(f"Beds directory not found: {self.beds_directory}")
            return
        
        for file in Path(self.beds_directory).glob("*.mp3"):
            # Extract style from filename (e.g., "energetic_bed_01.mp3")
            name = file.stem
            style = name.split("_")[0] if "_" in name else "default"
            
            self._beds[name] = BedConfig(
                name=name,
                file_path=str(file),
                style=style
            )
    
    def get_available_styles(self) -> List[str]:
        """Get list of available bed styles."""
        styles = set(bed.style for bed in self._beds.values())
        return list(styles) if styles else ["default"]
    
    def get_bed_by_style(self, style: str) -> Optional[BedConfig]:
        """Get a bed config by style."""
        for bed in self._beds.values():
            if bed.style == style:
                return bed
        return None
    
    async def mix_with_bed(
        self,
        voice_path: str,
        bed_path: str = None,
        bed_style: str = "default",
        settings: MixSettings = None,
        output_path: str = None
    ) -> str:
        """
        Mix a voice track with a music bed.
        
        Args:
            voice_path: Path to the voice audio file
            bed_path: Path to specific bed file (optional)
            bed_style: Style of bed to use if bed_path not specified
            settings: Mix settings (uses defaults if not specified)
            output_path: Output file path (auto-generated if not specified)
        
        Returns:
            Path to the mixed audio file
        """
        if settings is None:
            settings = MixSettings()
        
        # Get bed file
        if bed_path is None:
            bed_config = self.get_bed_by_style(bed_style)
            if bed_config:
                bed_path = bed_config.file_path
        
        # Generate output path
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(
                self.output_directory,
                f"mixed_{timestamp}.mp3"
            )
        
        # Check if pydub is available for mixing
        try:
            from pydub import AudioSegment
            return await self._mix_with_pydub(
                voice_path, bed_path, settings, output_path
            )
        except ImportError:
            logger.warning("pydub not installed, using fallback (voice only)")
            return await self._fallback_copy(voice_path, output_path)
    
    async def _mix_with_pydub(
        self,
        voice_path: str,
        bed_path: str,
        settings: MixSettings,
        output_path: str
    ) -> str:
        """Mix audio using pydub library."""
        from pydub import AudioSegment
        
        # Load audio files
        voice = AudioSegment.from_file(voice_path)
        
        if bed_path and os.path.exists(bed_path):
            bed = AudioSegment.from_file(bed_path)
        else:
            # No bed available, just process voice
            logger.info("No bed file available, outputting voice only")
            voice.export(output_path, format="mp3")
            return output_path
        
        # Calculate durations
        intro_ms = int(settings.intro_duration * 1000)
        outro_ms = int(settings.outro_duration * 1000)
        crossfade_ms = int(settings.crossfade_duration * 1000)
        
        # Adjust volumes
        voice = voice + settings.voice_volume
        bed = bed + settings.bed_volume
        
        # Calculate total duration needed
        total_duration = intro_ms + len(voice) + outro_ms
        
        # Loop bed if necessary
        if len(bed) < total_duration:
            loops_needed = (total_duration // len(bed)) + 1
            bed = bed * loops_needed
        
        # Trim bed to exact duration
        bed = bed[:total_duration]
        
        # Apply ducking to bed during voice
        # Create ducked version of bed
        duck_amount = settings.bed_volume - 6  # Additional 6dB duck during voice
        ducked_bed = bed + duck_amount
        
        # Create the mix
        # Part 1: Intro (full bed)
        intro = bed[:intro_ms]
        
        # Part 2: Voice section (ducked bed + voice)
        voice_section_bed = ducked_bed[intro_ms:intro_ms + len(voice)]
        voice_section = voice_section_bed.overlay(voice)
        
        # Part 3: Outro (full bed with fade)
        outro_start = intro_ms + len(voice)
        outro = bed[outro_start:outro_start + outro_ms]
        outro = outro.fade_out(outro_ms)
        
        # Combine all parts
        mixed = intro + voice_section + outro
        
        # Apply fade in at start
        mixed = mixed.fade_in(crossfade_ms)
        
        # Export
        mixed.export(output_path, format="mp3")
        logger.info(f"Mixed audio exported to: {output_path}")
        
        return output_path
    
    async def _fallback_copy(self, voice_path: str, output_path: str) -> str:
        """Fallback: just copy voice file if mixing not available."""
        import shutil
        shutil.copy(voice_path, output_path)
        return output_path
    
    async def create_station_id(
        self,
        text: str,
        bed_style: str = "energetic",
        voice_generator: Any = None
    ) -> str:
        """
        Create a station ID with voice and bed.
        
        Args:
            text: The station ID text
            bed_style: Style of music bed to use
            voice_generator: VoiceGenerator instance for TTS
        
        Returns:
            Path to the final station ID audio
        """
        # Generate voice
        if voice_generator is None:
            from core.brain.voice_generator import VoiceGenerator
            voice_generator = VoiceGenerator()
        
        # Create temp file for voice
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            voice_path = f.name
        
        # Generate TTS
        voice_path = voice_generator.generate_audio(
            text=text,
            output_path=voice_path
        )
        
        # Mix with bed
        settings = MixSettings(
            intro_duration=1.5,
            outro_duration=1.0,
            bed_volume=-10.0  # Slightly louder for station IDs
        )
        
        output_path = await self.mix_with_bed(
            voice_path=voice_path,
            bed_style=bed_style,
            settings=settings
        )
        
        # Clean up temp voice file
        try:
            os.remove(voice_path)
        except:
            pass
        
        return output_path
    
    async def create_promo(
        self,
        text: str,
        bed_style: str = "promo",
        voice_generator: Any = None
    ) -> str:
        """
        Create a promotional announcement with voice and bed.
        
        Args:
            text: The promo text
            bed_style: Style of music bed to use
            voice_generator: VoiceGenerator instance for TTS
        
        Returns:
            Path to the final promo audio
        """
        settings = MixSettings(
            intro_duration=2.0,
            outro_duration=2.5,
            bed_volume=-12.0
        )
        
        return await self.create_station_id(
            text=text,
            bed_style=bed_style,
            voice_generator=voice_generator
        )

    def mix_over_intro(
        self,
        voice_path: str,
        song_path: str,
        intro_duration: float,
        output_path: str = None
    ) -> Optional[str]:
        """
        Mix voice track over the intro (ramp) of a song.

        Args:
            voice_path: Path to voice file
            song_path: Path to song file
            intro_duration: Duration of intro in seconds (the 'post')
            output_path: Output file path

        Returns:
            Path to mixed file, or None if failed
        """
        if output_path is None:
            import hashlib
            # Create deterministic filename based on inputs so we cache mixes
            h = hashlib.md5(f"{voice_path}{song_path}{intro_duration}".encode()).hexdigest()
            output_path = os.path.join(self.output_directory, f"ramp_mix_{h}.mp3")

        # Check cache
        if os.path.exists(output_path):
            return output_path

        try:
            from pydub import AudioSegment

            # Load files
            if not os.path.exists(voice_path) or not os.path.exists(song_path):
                logger.error(f"Missing input files for mixing: {voice_path}, {song_path}")
                return None

            voice = AudioSegment.from_file(voice_path)
            song = AudioSegment.from_file(song_path)

            # Logic:
            # Voice starts at 0. Song starts at 0.
            # Voice should end before intro_duration.
            # Ideally, we align the END of the voice with the END of the intro (hitting the post).
            # But standard practice is usually start immediately and hope it fits (since we constrained generation).
            # Let's align START for now, as that's safer than voice starting late and clashing if we calculated wrong.
            # But let's add a small padding (0.5s) so it doesn't start INSTANTLY with the first drum kick.

            start_offset_ms = 500 # 0.5s

            # Adjust levels
            # Song dips slightly? Usually not for intro ramps, just voice sits on top.
            # Maybe duck song -2dB during voice.

            voice_len = len(voice)

            # Create a ducked version of song during the voice segment
            # We need to overlay voice onto song at start_offset_ms

            # Simple overlay
            # song.overlay(voice, position=start_offset_ms)
            # However, pydub overlay handles volume.
            # Let's boost voice slightly to cut through
            voice = voice + 2

            mixed = song.overlay(voice, position=start_offset_ms)

            mixed.export(output_path, format="mp3")
            logger.info(f"Ramp mix created: {output_path}")
            return output_path

        except ImportError:
            logger.error("pydub not installed, cannot mix ramp.")
            return None
        except Exception as e:
            logger.error(f"Failed to mix ramp: {e}")
            return None


# Singleton instance
_voice_mixer: Optional[VoiceMixer] = None


def get_voice_mixer() -> VoiceMixer:
    """Get the default voice mixer instance."""
    global _voice_mixer
    if _voice_mixer is None:
        _voice_mixer = VoiceMixer()
    return _voice_mixer
