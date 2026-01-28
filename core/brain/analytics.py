"""
Analytics & Logging for Neon Frequency
========================================
Playout logging, listener stats, and compliance reporting.
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum

logger = logging.getLogger("AEN.Analytics")


class LogType(Enum):
    """Types of log entries."""
    TRACK_PLAY = "track_play"
    AD_PLAY = "ad_play"
    VOICE_PLAY = "voice_play"
    STATION_ID = "station_id"
    LISTENER_UPDATE = "listener_update"
    ERROR = "error"
    AUTOMATION_EVENT = "automation_event"


@dataclass
class PlayoutLogEntry:
    """A single playout log entry for compliance and analytics."""
    timestamp: datetime
    log_type: LogType
    title: str
    artist: Optional[str] = None
    duration_seconds: int = 0
    source: str = "automation"  # automation, live, request
    
    # Ad-specific
    advertiser: Optional[str] = None
    campaign_id: Optional[str] = None
    
    # Audio properties
    loudness_lufs: Optional[float] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['log_type'] = self.log_type.value
        return data


@dataclass
class ListenerSnapshot:
    """Snapshot of listener statistics."""
    timestamp: datetime
    current_listeners: int
    peak_listeners: int
    unique_sessions: int
    average_listen_duration: int  # seconds
    geographical: Dict[str, int] = field(default_factory=dict)  # country -> count


class PlayoutLogger:
    """
    Playout logging for compliance and royalty reporting.
    
    Features:
    - Real-time logging of all played content
    - ASCAP/BMI/SESAC reporting format
    - Ad proof for advertisers
    - Export to various formats
    """
    
    def __init__(self, log_dir: str = None):
        self.log_dir = Path(log_dir or os.getenv("LOG_DIR", "./logs"))
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.entries: List[PlayoutLogEntry] = []
        self.current_hour_file: Optional[Path] = None
        logger.info(f"Playout logger initialized: {self.log_dir}")
    
    def log_track(
        self,
        title: str,
        artist: str,
        duration: int,
        source: str = "automation",
        **metadata
    ):
        """Log a track play."""
        entry = PlayoutLogEntry(
            timestamp=datetime.now(),
            log_type=LogType.TRACK_PLAY,
            title=title,
            artist=artist,
            duration_seconds=duration,
            source=source,
            metadata=metadata
        )
        self._add_entry(entry)
        logger.info(f"Logged: {artist} - {title}")
    
    def log_ad(
        self,
        title: str,
        advertiser: str,
        duration: int,
        campaign_id: str = None
    ):
        """Log an ad play."""
        entry = PlayoutLogEntry(
            timestamp=datetime.now(),
            log_type=LogType.AD_PLAY,
            title=title,
            advertiser=advertiser,
            duration_seconds=duration,
            campaign_id=campaign_id
        )
        self._add_entry(entry)
        logger.info(f"Ad logged: {title} ({advertiser})")
    
    def log_voice(self, title: str, duration: int, dj_name: str = "AEN"):
        """Log a voice break."""
        entry = PlayoutLogEntry(
            timestamp=datetime.now(),
            log_type=LogType.VOICE_PLAY,
            title=title,
            artist=dj_name,
            duration_seconds=duration
        )
        self._add_entry(entry)
    
    def log_event(self, event_name: str, details: Dict[str, Any] = None):
        """Log an automation event."""
        entry = PlayoutLogEntry(
            timestamp=datetime.now(),
            log_type=LogType.AUTOMATION_EVENT,
            title=event_name,
            metadata=details or {}
        )
        self._add_entry(entry)
    
    def _add_entry(self, entry: PlayoutLogEntry):
        """Add entry and persist to file."""
        self.entries.append(entry)
        self._write_to_file(entry)
    
    def _write_to_file(self, entry: PlayoutLogEntry):
        """Write entry to hourly log file."""
        hour_str = entry.timestamp.strftime("%Y-%m-%d_%H")
        log_file = self.log_dir / f"playout_{hour_str}.jsonl"
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(entry.to_dict()) + '\n')
    
    def get_last_hour(self) -> List[PlayoutLogEntry]:
        """Get log entries from the last hour."""
        cutoff = datetime.now() - timedelta(hours=1)
        return [e for e in self.entries if e.timestamp >= cutoff]
    
    def get_track_plays(self, hours: int = 24) -> List[PlayoutLogEntry]:
        """Get track plays from the last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            e for e in self.entries
            if e.timestamp >= cutoff and e.log_type == LogType.TRACK_PLAY
        ]
    
    def export_ascap_report(self, date: datetime = None) -> str:
        """Export ASCAP/BMI format report."""
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        
        # Get entries for the date
        entries = [
            e for e in self.entries
            if e.timestamp.date() == date.date() and e.log_type == LogType.TRACK_PLAY
        ]
        
        lines = [
            f"ASCAP Music Report - {date_str}",
            f"Station: Neon Frequency",
            f"Generated: {datetime.now().isoformat()}",
            "-" * 60,
            "Time | Artist | Title | Duration",
            "-" * 60
        ]
        
        for entry in entries:
            time_str = entry.timestamp.strftime("%H:%M:%S")
            lines.append(
                f"{time_str} | {entry.artist} | {entry.title} | {entry.duration_seconds}s"
            )
        
        lines.append("-" * 60)
        lines.append(f"Total Tracks: {len(entries)}")
        
        report = '\n'.join(lines)
        
        # Save to file
        report_file = self.log_dir / f"ascap_report_{date_str}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        return str(report_file)
    
    def export_ad_proof(self, advertiser: str, start_date: datetime, end_date: datetime) -> Dict:
        """Generate ad proof report for an advertiser."""
        entries = [
            e for e in self.entries
            if (e.log_type == LogType.AD_PLAY and
                e.advertiser == advertiser and
                start_date <= e.timestamp <= end_date)
        ]
        
        return {
            "advertiser": advertiser,
            "period": f"{start_date.date()} to {end_date.date()}",
            "total_plays": len(entries),
            "total_time_seconds": sum(e.duration_seconds for e in entries),
            "plays": [e.to_dict() for e in entries]
        }


class ListenerAnalytics:
    """
    Listener statistics and analytics.
    
    Features:
    - Real-time listener counts
    - Peak tracking
    - Geographic breakdown
    - Session analytics
    """
    
    def __init__(self):
        self.snapshots: List[ListenerSnapshot] = []
        self.current_listeners: int = 0
        self.peak_listeners: int = 0
        self.peak_timestamp: Optional[datetime] = None
        logger.info("Listener analytics initialized")
    
    def update_count(self, count: int, geo_data: Dict[str, int] = None):
        """Update listener count."""
        self.current_listeners = count
        
        if count > self.peak_listeners:
            self.peak_listeners = count
            self.peak_timestamp = datetime.now()
        
        # Create snapshot every 5 minutes
        if not self.snapshots or (datetime.now() - self.snapshots[-1].timestamp).seconds >= 300:
            snapshot = ListenerSnapshot(
                timestamp=datetime.now(),
                current_listeners=count,
                peak_listeners=self.peak_listeners,
                unique_sessions=0,  # Would need session tracking
                average_listen_duration=0,
                geographical=geo_data or {}
            )
            self.snapshots.append(snapshot)
    
    def get_hourly_average(self, hours: int = 24) -> float:
        """Get average listeners over the last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        relevant = [s for s in self.snapshots if s.timestamp >= cutoff]
        
        if not relevant:
            return 0.0
        
        return sum(s.current_listeners for s in relevant) / len(relevant)
    
    def get_peak_time(self) -> Optional[datetime]:
        """Get the time of peak listenership."""
        return self.peak_timestamp
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return {
            "current_listeners": self.current_listeners,
            "peak_listeners": self.peak_listeners,
            "peak_time": self.peak_timestamp.isoformat() if self.peak_timestamp else None,
            "hourly_average": self.get_hourly_average(1),
            "daily_average": self.get_hourly_average(24)
        }


class AnalyticsDashboard:
    """Combined analytics dashboard."""
    
    def __init__(self, log_dir: str = None):
        self.playout = PlayoutLogger(log_dir)
        self.listeners = ListenerAnalytics()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get combined dashboard data."""
        last_hour = self.playout.get_last_hour()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "listeners": self.listeners.get_stats(),
            "playout": {
                "last_hour_tracks": len([e for e in last_hour if e.log_type == LogType.TRACK_PLAY]),
                "last_hour_ads": len([e for e in last_hour if e.log_type == LogType.AD_PLAY]),
                "recent_tracks": [
                    {"artist": e.artist, "title": e.title, "time": e.timestamp.isoformat()}
                    for e in last_hour[-5:] if e.log_type == LogType.TRACK_PLAY
                ]
            }
        }


# Convenience functions
def get_logger(log_dir: str = None) -> PlayoutLogger:
    """Get a playout logger instance."""
    return PlayoutLogger(log_dir)


def get_analytics() -> AnalyticsDashboard:
    """Get an analytics dashboard instance."""
    return AnalyticsDashboard()
