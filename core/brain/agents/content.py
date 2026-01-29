from dataclasses import dataclass, field
import logging
from typing import Optional, List, Dict, Any
from core.brain.scheduler import BroadcastScheduler, DayPart, HourClock
from core.brain.content_engine import ContentEngine, DJPersonality
from core.brain.radio_automation import VoiceGenerator
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class ShowRunner:
    """
    The Executive Producer Agent.
    Responsible for managing the broadcast clock, shows, and timing.
    """
    scheduler: BroadcastScheduler = field(default_factory=BroadcastScheduler)
    
    def get_current_daypart(self) -> DayPart:
        """Determines the current daypart based on time."""
        # Simple mapping for now
        hour = datetime.now().hour
        if 5 <= hour < 10: return DayPart.MORNING_DRIVE
        if 10 <= hour < 15: return DayPart.MIDDAY
        if 15 <= hour < 19: return DayPart.AFTERNOON_DRIVE
        if 19 <= hour < 24: return DayPart.EVENING
        return DayPart.OVERNIGHT

    def get_next_clock_event(self) -> Optional[Dict[str, Any]]:
        """
        Determines what should happen next based on the hour clock.
        e.g., Playing a song, an ad, or a station ID.
        """
        # In a real implementation, this would track state within the hour
        # For now, return a dummy event
        return {"type": "music", "duration": 180}

    def emergency_cart_trigger(self) -> str:
        """Returns the path to the emergency backup loop."""
        return "/music/station/emergency_loop_01.mp3"

@dataclass
class TalentParams:
    """
    The Voice Director Agent.
    Responsible for managing DJ personas and voice synthesis.
    """
    engine: ContentEngine = field(default_factory=ContentEngine)
    voice: VoiceGenerator = field(default_factory=VoiceGenerator)
    
    current_persona: str = "AEN"
    
    def set_persona(self, persona_name: str):
        """Switches the active DJ persona."""
        self.current_persona = persona_name
        # logic to swap voice settings would go here

    def generate_break(self, context: Dict[str, Any]) -> str:
        """
        Generates a voice break script and synthesis.
        Context includes: current_track, next_track, weather, etc.
        """
        # 1. Generate Script
        script = self.engine.generate_dj_script(
            personality=self.current_persona,
            context=context.get("weather", "unknown weather"), # Simplified
            song_name=context.get("current_track", {}).get("title", "Unknown Track"),
            artist_name=context.get("current_track", {}).get("artist", "Unknown Artist")
        )
        
        # 2. Synthesize (if API key present)
        # audio_path = self.voice.generate_voice_clip(script, ...)
        
        return script
    
    def check_safety(self, text: str) -> bool:
        """Simple profanity filter."""
        banned = ["dead air", "silence", "radio is broken"]
        for word in banned:
            if word in text.lower():
                return False
        return True
