"""
Content Scheduler for Neon Frequency
=====================================
RoboDJ-style scheduling system for automated content generation.
Supports hourly, smart, and marker-based scheduling modes.
"""

import os
import json
import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Callable
from enum import Enum
import threading

logger = logging.getLogger("AEN.ContentScheduler")


class ScheduleMode(Enum):
    MANUAL = "Manual"
    AUTO = "Auto"


class ScheduleInterval(Enum):
    EVERY_HOUR = "Every hour"
    EVERY_30_MIN = "Every 30 minutes"
    EVERY_15_MIN = "Every 15 minutes"
    HOURLY_AT = "Hourly at specific minute"
    SMART = "Smart (playlist-aware)"
    CUSTOM = "Custom"


@dataclass
class Schedule:
    """
    A content generation schedule.
    
    Inspired by RoboDJ's Active Schedules feature.
    """
    id: str
    name: str
    interval: ScheduleInterval = ScheduleInterval.EVERY_HOUR
    minute_offset: int = 57  # e.g., "Every hour at :57"
    mode: ScheduleMode = ScheduleMode.AUTO
    
    # Which prompts to run
    prompt_ids: List[str] = field(default_factory=list)
    
    # Status
    enabled: bool = True
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def calculate_next_run(self) -> datetime:
        """Calculate the next run time based on interval."""
        now = datetime.now()
        
        if self.interval == ScheduleInterval.EVERY_HOUR:
            # Next hour at the specified minute
            next_run = now.replace(minute=self.minute_offset, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(hours=1)
            return next_run
        
        elif self.interval == ScheduleInterval.EVERY_30_MIN:
            # Next 30-minute mark
            if now.minute < 30:
                next_run = now.replace(minute=30, second=0, microsecond=0)
            else:
                next_run = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            return next_run
        
        elif self.interval == ScheduleInterval.EVERY_15_MIN:
            # Next 15-minute mark
            next_minute = ((now.minute // 15) + 1) * 15
            if next_minute >= 60:
                next_run = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            else:
                next_run = now.replace(minute=next_minute, second=0, microsecond=0)
            return next_run
        
        else:
            # Default: 1 hour from now
            return now + timedelta(hours=1)
    
    def get_time_remaining(self) -> Optional[str]:
        """Get human-readable time until next run."""
        if not self.next_run:
            return None
        
        try:
            next_dt = datetime.fromisoformat(self.next_run)
            delta = next_dt - datetime.now()
            
            if delta.total_seconds() < 0:
                return "Now"
            
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes = remainder // 60
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            return f"{minutes}m"
        except Exception:
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "interval": self.interval.value,
            "minute_offset": self.minute_offset,
            "mode": self.mode.value,
            "prompt_ids": self.prompt_ids,
            "enabled": self.enabled,
            "last_run": self.last_run,
            "next_run": self.next_run,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Schedule":
        return cls(
            id=data["id"],
            name=data["name"],
            interval=ScheduleInterval(data.get("interval", "Every hour")),
            minute_offset=data.get("minute_offset", 57),
            mode=ScheduleMode(data.get("mode", "Auto")),
            prompt_ids=data.get("prompt_ids", []),
            enabled=data.get("enabled", True),
            last_run=data.get("last_run"),
            next_run=data.get("next_run"),
            created_at=data.get("created_at", datetime.now().isoformat())
        )


class ContentScheduler:
    """
    Manages content generation schedules.
    
    Runs schedules in the background and generates scripts automatically.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), "data", "schedules.json"
        )
        self.schedules: Dict[str, Schedule] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._callbacks: List[Callable[[Schedule], None]] = []
        self._load()
    
    def _load(self) -> None:
        """Load schedules from storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for schedule_data in data.get("schedules", []):
                        schedule = Schedule.from_dict(schedule_data)
                        self.schedules[schedule.id] = schedule
                logger.info(f"Loaded {len(self.schedules)} schedules")
            except Exception as e:
                logger.error(f"Failed to load schedules: {e}")
        else:
            logger.info("No existing schedules file, creating defaults")
            self._create_defaults()
    
    def _save(self) -> None:
        """Persist schedules to storage."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "schedules": [s.to_dict() for s in self.schedules.values()],
            "updated_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def _create_defaults(self) -> None:
        """Create default schedules."""
        defaults = [
            Schedule(
                id="shoutout",
                name="ShoutOut",
                interval=ScheduleInterval.EVERY_HOUR,
                minute_offset=57,
                mode=ScheduleMode.MANUAL,
                prompt_ids=[]
            ),
            Schedule(
                id="smart_hourly",
                name="Smart Hourly",
                interval=ScheduleInterval.EVERY_HOUR,
                minute_offset=2,
                mode=ScheduleMode.AUTO,
                prompt_ids=["toh_time_artist"]
            ),
        ]
        
        for schedule in defaults:
            schedule.next_run = schedule.calculate_next_run().isoformat()
            self.schedules[schedule.id] = schedule
        self._save()
    
    def get(self, schedule_id: str) -> Optional[Schedule]:
        """Get a schedule by ID."""
        return self.schedules.get(schedule_id)
    
    def get_all(self) -> List[Schedule]:
        """Get all schedules."""
        return list(self.schedules.values())
    
    def get_active(self) -> List[Schedule]:
        """Get all enabled schedules."""
        return [s for s in self.schedules.values() if s.enabled]
    
    def create(self, schedule: Schedule) -> Schedule:
        """Create a new schedule."""
        schedule.next_run = schedule.calculate_next_run().isoformat()
        self.schedules[schedule.id] = schedule
        self._save()
        logger.info(f"Created schedule: {schedule.name}")
        return schedule
    
    def update(self, schedule_id: str, updates: Dict[str, Any]) -> Optional[Schedule]:
        """Update a schedule."""
        if schedule_id not in self.schedules:
            return None
        
        schedule = self.schedules[schedule_id]
        schedule_dict = schedule.to_dict()
        schedule_dict.update(updates)
        
        self.schedules[schedule_id] = Schedule.from_dict(schedule_dict)
        self.schedules[schedule_id].next_run = self.schedules[schedule_id].calculate_next_run().isoformat()
        self._save()
        return self.schedules[schedule_id]
    
    def delete(self, schedule_id: str) -> bool:
        """Delete a schedule."""
        if schedule_id in self.schedules:
            del self.schedules[schedule_id]
            self._save()
            return True
        return False
    
    def toggle(self, schedule_id: str) -> Optional[Schedule]:
        """Toggle schedule enabled state."""
        if schedule_id not in self.schedules:
            return None
        
        schedule = self.schedules[schedule_id]
        schedule.enabled = not schedule.enabled
        if schedule.enabled:
            schedule.next_run = schedule.calculate_next_run().isoformat()
        self._save()
        return schedule
    
    def on_schedule_trigger(self, callback: Callable[[Schedule], None]) -> None:
        """Register a callback for when a schedule triggers."""
        self._callbacks.append(callback)
    
    async def _run_loop(self) -> None:
        """Background loop to check and trigger schedules."""
        logger.info("Content scheduler started")
        
        while self._running:
            now = datetime.now()
            
            for schedule in self.get_active():
                if not schedule.next_run:
                    continue
                
                try:
                    next_run = datetime.fromisoformat(schedule.next_run)
                    
                    if now >= next_run:
                        logger.info(f"Triggering schedule: {schedule.name}")
                        
                        # Notify callbacks
                        for callback in self._callbacks:
                            try:
                                callback(schedule)
                            except Exception as e:
                                logger.error(f"Callback error: {e}")
                        
                        # Update schedule
                        schedule.last_run = now.isoformat()
                        schedule.next_run = schedule.calculate_next_run().isoformat()
                        self._save()
                
                except Exception as e:
                    logger.error(f"Schedule check error: {e}")
            
            # Check every 30 seconds
            await asyncio.sleep(30)
        
        logger.info("Content scheduler stopped")
    
    def start(self) -> None:
        """Start the scheduler background loop."""
        if self._running:
            return
        
        self._running = True
        
        # Start in a new thread with its own event loop
        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._run_loop())
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
        logger.info("Scheduler thread started")
    
    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False


# Convenience function
def get_content_scheduler() -> ContentScheduler:
    """Get the default content scheduler instance."""
    return ContentScheduler()
