from dataclasses import dataclass, field
import logging
from typing import Dict, Any, Optional
from core.brain.radio_automation import AzuraCastClient

logger = logging.getLogger(__name__)

@dataclass
class DeckMaster:
    """
    The Broadcast Engineer Agent.
    Responsible for controlling the audio pipeline and automation.
    """
    azuracast: AzuraCastClient = field(default_factory=AzuraCastClient)
    
    def skip_track(self) -> bool:
        """Forces a track skip via AzuraCast."""
        logger.info("DeckMaster: Forcing track skip")
        # In real implementation: return self.azuracast.skip_current()
        return True

    def get_stream_health(self) -> Dict[str, Any]:
        """Checks if the stream is live and levels are good."""
        # Simulated check
        return {
            "is_live": True,
            "listeners": 0, # Would fetch from API
            "cpu_load": 12.5
        }

    def trigger_ducking(self, duration: float = 5.0):
        """
        Lowers music volume for voiceover.
        This would typically send a telnet command to Liquidsoap.
        """
        logger.info(f"DeckMaster: Ducking audio for {duration}s")
        # telnet.write("duck(true)")
        # schedule "duck(false)" after duration

    def emergency_override(self):
        """
        Kills all automation and plays the emergency loop.
        Used for Dead Air detection.
        """
        logger.critical("DeckMaster: EMERGENCY OVERRIDE TRIGGERED")
        # Logic to switch master source to fallback
