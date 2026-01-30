"""
Broadcast Scheduler for Neon Frequency
=======================================
Manages scheduling, station clocks, and automated programming.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("AEN.Scheduler")


class DayPart(Enum):
    """Radio industry dayparts."""
    OVERNIGHT = "overnight"      # 12am - 6am
    MORNING = "morning"          # 6am - 10am
    MIDDAY = "midday"           # 10am - 3pm
    AFTERNOON = "afternoon"      # 3pm - 7pm
    EVENING = "evening"         # 7pm - 12am


class SegmentType(Enum):
    """Types of broadcast segments."""
    MUSIC = "music"
    VOICE = "voice"
    STATION_ID = "station_id"
    WEATHER = "weather"
    NEWS = "news"
    AD_BREAK = "ad_break"
    JINGLE = "jingle"
    SWEEPER = "sweeper"
    SHOW_INTRO = "show_intro"
    SHOW_OUTRO = "show_outro"


@dataclass
class ScheduleSlot:
    """A single slot in the broadcast schedule."""
    segment_type: SegmentType
    duration_seconds: int
    minute_of_hour: int  # 0-59, when this slot should play
    content_id: Optional[str] = None  # Reference to specific content
    playlist_id: Optional[str] = None
    callback: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HourClock:
    """
    Station clock defining what plays each hour.
    
    Inspired by industry standard hot clocks from Myriad, NextKast, etc.
    """
    name: str
    daypart: DayPart
    slots: List[ScheduleSlot] = field(default_factory=list)
    
    def add_slot(self, slot: ScheduleSlot):
        """Add a slot to the clock."""
        self.slots.append(slot)
        self.slots.sort(key=lambda s: s.minute_of_hour)
    
    def get_current_slot(self) -> Optional[ScheduleSlot]:
        """Get the slot that should be playing now."""
        current_minute = datetime.now().minute
        
        # Find the most recent slot
        for slot in reversed(self.slots):
            if slot.minute_of_hour <= current_minute:
                return slot
        
        # Return last slot if we've wrapped
        return self.slots[-1] if self.slots else None
    
    def get_next_slot(self) -> Optional[ScheduleSlot]:
        """Get the next upcoming slot."""
        current_minute = datetime.now().minute
        
        for slot in self.slots:
            if slot.minute_of_hour > current_minute:
                return slot
        
        # Wrap to first slot of next hour
        return self.slots[0] if self.slots else None


class ClockBuilder:
    """Factory for creating common clock patterns."""
    
    @staticmethod
    def create_music_heavy_clock(name: str = "Music Heavy") -> HourClock:
        """Create a clock focused on music with minimal talk."""
        clock = HourClock(name=name, daypart=DayPart.OVERNIGHT)
        
        # Top of hour
        clock.add_slot(ScheduleSlot(SegmentType.STATION_ID, 10, 0))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 1))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 4))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 7))
        clock.add_slot(ScheduleSlot(SegmentType.VOICE, 30, 10))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 11))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 14))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 17))
        
        # Quarter hour
        clock.add_slot(ScheduleSlot(SegmentType.SWEEPER, 15, 20))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 21))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 24))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 27))
        
        # Half hour - ad break
        clock.add_slot(ScheduleSlot(SegmentType.AD_BREAK, 120, 30))
        clock.add_slot(ScheduleSlot(SegmentType.JINGLE, 10, 32))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 33))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 36))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 39))
        clock.add_slot(ScheduleSlot(SegmentType.VOICE, 30, 42))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 43))
        
        # Three quarter
        clock.add_slot(ScheduleSlot(SegmentType.WEATHER, 30, 45))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 46))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 49))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 52))
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 55))
        clock.add_slot(ScheduleSlot(SegmentType.SWEEPER, 15, 58))
        
        return clock
    
    @staticmethod
    def create_talk_radio_clock(name: str = "Talk Radio") -> HourClock:
        """Create a clock for talk-heavy programming."""
        clock = HourClock(name=name, daypart=DayPart.MORNING)
        
        clock.add_slot(ScheduleSlot(SegmentType.STATION_ID, 10, 0))
        clock.add_slot(ScheduleSlot(SegmentType.SHOW_INTRO, 60, 1))
        clock.add_slot(ScheduleSlot(SegmentType.VOICE, 480, 2))  # 8 min talk segment
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 10))
        clock.add_slot(ScheduleSlot(SegmentType.VOICE, 480, 13))
        clock.add_slot(ScheduleSlot(SegmentType.WEATHER, 60, 21))
        clock.add_slot(ScheduleSlot(SegmentType.VOICE, 420, 22))
        
        clock.add_slot(ScheduleSlot(SegmentType.AD_BREAK, 180, 30))
        clock.add_slot(ScheduleSlot(SegmentType.VOICE, 600, 33))  # 10 min talk
        clock.add_slot(ScheduleSlot(SegmentType.MUSIC, 180, 43))
        clock.add_slot(ScheduleSlot(SegmentType.NEWS, 120, 46))
        clock.add_slot(ScheduleSlot(SegmentType.VOICE, 420, 48))
        clock.add_slot(ScheduleSlot(SegmentType.SHOW_OUTRO, 60, 55))
        clock.add_slot(ScheduleSlot(SegmentType.SWEEPER, 15, 56))
        
        return clock


@dataclass
class Show:
    """A scheduled radio show."""
    name: str
    host: str
    start_time: datetime
    duration_hours: int
    clock: HourClock
    playlist_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def end_time(self) -> datetime:
        return self.start_time + timedelta(hours=self.duration_hours)
    
    def is_active(self) -> bool:
        now = datetime.now()
        return self.start_time <= now < self.end_time


class BroadcastScheduler:
    """
    Master scheduler for radio broadcasts.
    
    Manages:
    - Daily programming schedule
    - Station clocks per daypart
    - Show scheduling
    - Event triggers
    """
    
    def __init__(self):
        self.clocks: Dict[DayPart, HourClock] = {}
        self.shows: List[Show] = []
        self.default_clock = ClockBuilder.create_music_heavy_clock()
        self._init_default_clocks()
        logger.info("Broadcast scheduler initialized")
    
    def _init_default_clocks(self):
        """Initialize default clocks for each daypart."""
        self.clocks[DayPart.OVERNIGHT] = ClockBuilder.create_music_heavy_clock("Overnight")
        self.clocks[DayPart.MORNING] = ClockBuilder.create_talk_radio_clock("Morning Drive")
        self.clocks[DayPart.MIDDAY] = ClockBuilder.create_music_heavy_clock("Midday Mix")
        self.clocks[DayPart.AFTERNOON] = ClockBuilder.create_music_heavy_clock("Afternoon Drive")
        self.clocks[DayPart.EVENING] = ClockBuilder.create_music_heavy_clock("Evening Vibes")
    
    def get_current_daypart(self) -> DayPart:
        """Get the current daypart based on time."""
        hour = datetime.now().hour
        
        if 0 <= hour < 6:
            return DayPart.OVERNIGHT
        elif 6 <= hour < 10:
            return DayPart.MORNING
        elif 10 <= hour < 15:
            return DayPart.MIDDAY
        elif 15 <= hour < 19:
            return DayPart.AFTERNOON
        else:
            return DayPart.EVENING
    
    def get_active_clock(self) -> HourClock:
        """Get the currently active clock."""
        # Check for active show first
        for show in self.shows:
            if show.is_active():
                return show.clock
        
        # Fall back to daypart clock
        daypart = self.get_current_daypart()
        return self.clocks.get(daypart, self.default_clock)
    
    def schedule_show(self, show: Show):
        """Add a show to the schedule."""
        self.shows.append(show)
        self.shows.sort(key=lambda s: s.start_time)
        logger.info(f"Scheduled show: {show.name} at {show.start_time}")
    
    def get_upcoming_shows(self, hours: int = 24) -> List[Show]:
        """Get shows in the next N hours."""
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)
        return [s for s in self.shows if now <= s.start_time < cutoff]
    
    def get_current_slot(self) -> Optional[ScheduleSlot]:
        """Get what should be playing right now."""
        clock = self.get_active_clock()
        return clock.get_current_slot()
    
    def get_next_slot(self) -> Optional[ScheduleSlot]:
        """Get the next upcoming slot."""
        clock = self.get_active_clock()
        return clock.get_next_slot()
    
    def get_schedule_summary(self) -> Dict[str, Any]:
        """Get a summary of the current schedule."""
        clock = self.get_active_clock()
        current_slot = self.get_current_slot()
        next_slot = self.get_next_slot()
        
        return {
            "daypart": self.get_current_daypart().value,
            "active_clock": clock.name,
            "current_segment": current_slot.segment_type.value if current_slot else None,
            "next_segment": next_slot.segment_type.value if next_slot else None,
            "next_segment_at": next_slot.minute_of_hour if next_slot else None,
            "upcoming_shows": [
                {"name": s.name, "host": s.host, "start": s.start_time.isoformat()}
                for s in self.get_upcoming_shows(6)
            ]
        }


# Convenience function
def get_scheduler() -> BroadcastScheduler:
    """Get a configured broadcast scheduler."""
    return BroadcastScheduler()
