"""
Live Assist Mode for Neon Frequency
=====================================
Manual override, hotkeys, instant carts, and emergency controls.
"""

import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("AEN.LiveAssist")


class OverrideLevel(Enum):
    """Levels of automation override."""
    FULL_AUTO = "full_auto"          # Complete automation
    ASSISTED = "assisted"            # AI suggests, human approves
    MANUAL = "manual"               # Human in control, AI assists
    EMERGENCY = "emergency"         # Emergency broadcast mode


class CartType(Enum):
    """Types of instant carts."""
    JINGLE = "jingle"
    SWEEPER = "sweeper"
    SOUND_EFFECT = "sound_effect"
    STATION_ID = "station_id"
    VOICE_TRACK = "voice_track"
    EMERGENCY = "emergency"


@dataclass
class InstantCart:
    """An instant playout cart/button."""
    id: str
    name: str
    cart_type: CartType
    audio_path: str
    hotkey: Optional[str] = None  # e.g., "F1", "Ctrl+1"
    color: str = "blue"  # UI color
    duration_seconds: int = 0
    ducking_enabled: bool = True  # Duck main audio while playing


@dataclass
class LiveSession:
    """A live broadcast session."""
    started_at: datetime
    host_name: str
    override_level: OverrideLevel
    ended_at: Optional[datetime] = None
    notes: str = ""
    
    @property
    def is_active(self) -> bool:
        return self.ended_at is None
    
    @property
    def duration_minutes(self) -> int:
        end = self.ended_at or datetime.now()
        return int((end - self.started_at).total_seconds() / 60)


class LiveAssistController:
    """
    Live assist control panel for DJs.
    
    Features:
    - Manual override modes
    - Instant cart system (12-button grid)
    - Emergency broadcast controls
    - Hotkey bindings
    - Duck/fade controls
    """
    
    def __init__(self):
        self.override_level = OverrideLevel.FULL_AUTO
        self.carts: Dict[str, InstantCart] = {}
        self.current_session: Optional[LiveSession] = None
        self.event_handlers: Dict[str, List[Callable]] = {}
        self._init_default_carts()
        logger.info("Live assist controller initialized")
    
    def _init_default_carts(self):
        """Initialize default cart layout."""
        default_carts = [
            InstantCart("id1", "Station ID", CartType.STATION_ID, "/audio/ids/main_id.mp3", "F1", "purple"),
            InstantCart("id2", "Short ID", CartType.STATION_ID, "/audio/ids/short_id.mp3", "F2", "purple"),
            InstantCart("jingle1", "Jingle 1", CartType.JINGLE, "/audio/jingles/jingle1.mp3", "F3", "green"),
            InstantCart("jingle2", "Jingle 2", CartType.JINGLE, "/audio/jingles/jingle2.mp3", "F4", "green"),
            InstantCart("sweep1", "Sweeper", CartType.SWEEPER, "/audio/sweepers/sweep1.mp3", "F5", "blue"),
            InstantCart("sfx1", "Airhorn", CartType.SOUND_EFFECT, "/audio/sfx/airhorn.mp3", "F6", "yellow"),
            InstantCart("sfx2", "Applause", CartType.SOUND_EFFECT, "/audio/sfx/applause.mp3", "F7", "yellow"),
            InstantCart("sfx3", "Rewind", CartType.SOUND_EFFECT, "/audio/sfx/rewind.mp3", "F8", "yellow"),
            InstantCart("emer1", "Emergency", CartType.EMERGENCY, "/audio/emergency/alert.mp3", "F12", "red"),
        ]
        
        for cart in default_carts:
            self.carts[cart.id] = cart
    
    def set_override_level(self, level: OverrideLevel):
        """Set the automation override level."""
        old_level = self.override_level
        self.override_level = level
        logger.info(f"Override level changed: {old_level.value} -> {level.value}")
        self._trigger_event("override_changed", {"old": old_level, "new": level})
    
    def start_live_session(self, host_name: str, level: OverrideLevel = OverrideLevel.MANUAL) -> LiveSession:
        """Start a live broadcast session."""
        if self.current_session and self.current_session.is_active:
            self.end_live_session()
        
        self.current_session = LiveSession(
            started_at=datetime.now(),
            host_name=host_name,
            override_level=level
        )
        self.set_override_level(level)
        logger.info(f"Live session started: {host_name}")
        self._trigger_event("session_started", {"host": host_name})
        return self.current_session
    
    def end_live_session(self, notes: str = "") -> Optional[LiveSession]:
        """End the current live session."""
        if not self.current_session:
            return None
        
        self.current_session.ended_at = datetime.now()
        self.current_session.notes = notes
        session = self.current_session
        
        # Reset to full automation
        self.set_override_level(OverrideLevel.FULL_AUTO)
        
        logger.info(f"Live session ended: {session.host_name} ({session.duration_minutes} min)")
        self._trigger_event("session_ended", {"session": session})
        
        self.current_session = None
        return session
    
    def fire_cart(self, cart_id: str) -> bool:
        """Fire an instant cart."""
        if cart_id not in self.carts:
            logger.warning(f"Cart not found: {cart_id}")
            return False
        
        cart = self.carts[cart_id]
        logger.info(f"Cart fired: {cart.name}")
        self._trigger_event("cart_fired", {"cart": cart})
        return True
    
    def add_cart(self, cart: InstantCart):
        """Add a custom cart."""
        self.carts[cart.id] = cart
        logger.info(f"Cart added: {cart.name}")
    
    def get_cart_grid(self) -> List[List[InstantCart]]:
        """Get carts organized in a 4x3 grid."""
        carts = list(self.carts.values())
        grid = []
        for i in range(0, 12, 4):
            row = carts[i:i+4]
            # Pad row if needed
            while len(row) < 4:
                row.append(None)
            grid.append(row)
        return grid
    
    # Event system
    def on(self, event: str, handler: Callable):
        """Register an event handler."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
    
    def _trigger_event(self, event: str, data: Dict[str, Any]):
        """Trigger an event."""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(data)
                except Exception as e:
                    logger.error(f"Event handler error: {e}")


class EmergencyController:
    """
    Emergency broadcast controls.
    
    Features:
    - Emergency alert system
    - Silence detection failover
    - Dead air protection
    - Backup stream activation
    """
    
    def __init__(self, live_assist: LiveAssistController):
        self.live_assist = live_assist
        self.emergency_active = False
        self.silence_threshold_seconds = 10
        self.last_audio_time = datetime.now()
        logger.info("Emergency controller initialized")
    
    def activate_emergency(self, reason: str = "Manual activation"):
        """Activate emergency mode."""
        self.emergency_active = True
        self.live_assist.set_override_level(OverrideLevel.EMERGENCY)
        logger.critical(f"EMERGENCY ACTIVATED: {reason}")
        
        # Fire emergency cart
        self.live_assist.fire_cart("emer1")
    
    def deactivate_emergency(self):
        """Deactivate emergency mode."""
        self.emergency_active = False
        self.live_assist.set_override_level(OverrideLevel.FULL_AUTO)
        logger.info("Emergency mode deactivated")
    
    def check_silence(self, audio_level: float) -> bool:
        """Check for dead air / silence."""
        if audio_level > 0.01:  # Above silence threshold
            self.last_audio_time = datetime.now()
            return False
        
        silence_duration = (datetime.now() - self.last_audio_time).total_seconds()
        
        if silence_duration >= self.silence_threshold_seconds:
            logger.warning(f"Dead air detected: {silence_duration:.1f}s")
            if not self.emergency_active:
                self.activate_emergency("Dead air detected")
            return True
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get emergency system status."""
        return {
            "emergency_active": self.emergency_active,
            "silence_threshold": self.silence_threshold_seconds,
            "last_audio": self.last_audio_time.isoformat(),
            "override_level": self.live_assist.override_level.value
        }


# Convenience functions
def get_live_assist() -> LiveAssistController:
    """Get a live assist controller instance."""
    return LiveAssistController()


def get_emergency_controller(live_assist: LiveAssistController = None) -> EmergencyController:
    """Get an emergency controller instance."""
    return EmergencyController(live_assist or get_live_assist())
