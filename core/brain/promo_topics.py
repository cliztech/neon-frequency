"""
Promo Topics for Neon Frequency
================================
RoboDJ-style promo topics management with shoutouts,
subject rotation, and usage tracking.
"""

import os
import json
import csv
import random
import logging
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from enum import Enum
from io import StringIO

logger = logging.getLogger("AEN.PromoTopics")


class TopicCategory(Enum):
    SHOUTOUTS = "ShoutOuts"
    REQUESTS = "Requests"
    CONTESTS = "Contests"
    EVENTS = "Events"
    SPONSORS = "Sponsors"
    GENERAL = "General"
    UNCATEGORIZED = "Uncategorized"


class TopicMode(Enum):
    SINGLE_TEXT = "Single Text"
    LIST_MODE = "List Mode"


@dataclass
class TopicSubject:
    """A single subject/entry within a topic."""
    id: int
    text: str
    used_count: int = 0
    last_used: Optional[str] = None
    active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "used_count": self.used_count,
            "last_used": self.last_used,
            "active": self.active
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TopicSubject":
        return cls(
            id=data["id"],
            text=data["text"],
            used_count=data.get("used_count", 0),
            last_used=data.get("last_used"),
            active=data.get("active", True)
        )


@dataclass
class PromoTopic:
    """
    A promo topic with subjects list.
    
    Inspired by RoboDJ's Promo Topics feature.
    """
    id: str
    name: str
    category: TopicCategory = TopicCategory.GENERAL
    mode: TopicMode = TopicMode.LIST_MODE
    status: str = "Active"
    
    # Subjects list
    subjects: List[TopicSubject] = field(default_factory=list)
    
    # Scheduling
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    # Metadata
    last_used: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def get_next_subject(self) -> Optional[TopicSubject]:
        """Get the next subject to use (least recently used)."""
        active_subjects = [s for s in self.subjects if s.active]
        
        if not active_subjects:
            return None
        
        # Sort by used_count, then by last_used
        active_subjects.sort(
            key=lambda s: (s.used_count, s.last_used or "")
        )
        
        return active_subjects[0]
    
    def get_random_subject(self) -> Optional[TopicSubject]:
        """Get a random active subject."""
        active_subjects = [s for s in self.subjects if s.active]
        if not active_subjects:
            return None
        return random.choice(active_subjects)
    
    def use_subject(self, subject_id: int) -> Optional[TopicSubject]:
        """Mark a subject as used."""
        for subject in self.subjects:
            if subject.id == subject_id:
                subject.used_count += 1
                subject.last_used = datetime.now().isoformat()
                self.last_used = subject.last_used
                return subject
        return None
    
    def add_subject(self, text: str) -> TopicSubject:
        """Add a new subject."""
        next_id = max([s.id for s in self.subjects], default=0) + 1
        subject = TopicSubject(id=next_id, text=text)
        self.subjects.append(subject)
        return subject
    
    def remove_subject(self, subject_id: int) -> bool:
        """Remove a subject by ID."""
        for i, subject in enumerate(self.subjects):
            if subject.id == subject_id:
                self.subjects.pop(i)
                return True
        return False
    
    def is_active_for_date(self, check_date: Optional[date] = None) -> bool:
        """Check if topic is active for a given date."""
        if self.status != "Active":
            return False
        
        check_date = check_date or date.today()
        
        if self.start_date:
            start = date.fromisoformat(self.start_date)
            if check_date < start:
                return False
        
        if self.end_date:
            end = date.fromisoformat(self.end_date)
            if check_date > end:
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "mode": self.mode.value,
            "status": self.status,
            "subjects": [s.to_dict() for s in self.subjects],
            "start_date": self.start_date,
            "end_date": self.end_date,
            "last_used": self.last_used,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromoTopic":
        return cls(
            id=data["id"],
            name=data["name"],
            category=TopicCategory(data.get("category", "General")),
            mode=TopicMode(data.get("mode", "List Mode")),
            status=data.get("status", "Active"),
            subjects=[TopicSubject.from_dict(s) for s in data.get("subjects", [])],
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            last_used=data.get("last_used"),
            created_at=data.get("created_at", datetime.now().isoformat())
        )


class PromoTopicsManager:
    """
    Manages promo topics with persistence and CSV import/export.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), "data", "promo_topics.json"
        )
        self.topics: Dict[str, PromoTopic] = {}
        self._load()
    
    def _load(self) -> None:
        """Load topics from storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for topic_data in data.get("topics", []):
                        topic = PromoTopic.from_dict(topic_data)
                        self.topics[topic.id] = topic
                logger.info(f"Loaded {len(self.topics)} promo topics")
            except Exception as e:
                logger.error(f"Failed to load topics: {e}")
        else:
            logger.info("No existing topics file, creating defaults")
            self._create_defaults()
    
    def _save(self) -> None:
        """Persist topics to storage."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "topics": [t.to_dict() for t in self.topics.values()],
            "updated_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def _create_defaults(self) -> None:
        """Create default topics."""
        shoutouts = PromoTopic(
            id="listener_shoutouts",
            name="Listener Shouts-2",
            category=TopicCategory.SHOUTOUTS,
            subjects=[
                TopicSubject(1, "Megan from Malibu"),
                TopicSubject(2, "Jeff from West Hills"),
                TopicSubject(3, "John from Ventura"),
                TopicSubject(4, "Mike from Chino"),
                TopicSubject(5, "Harry from Honolulu"),
            ]
        )
        
        requests = PromoTopic(
            id="requests",
            name="Requests",
            category=TopicCategory.REQUESTS,
            subjects=[]
        )
        
        self.topics[shoutouts.id] = shoutouts
        self.topics[requests.id] = requests
        self._save()
    
    def get(self, topic_id: str) -> Optional[PromoTopic]:
        """Get a topic by ID."""
        return self.topics.get(topic_id)
    
    def get_all(self) -> List[PromoTopic]:
        """Get all topics."""
        return list(self.topics.values())
    
    def get_by_category(self, category: TopicCategory) -> List[PromoTopic]:
        """Get topics by category."""
        return [t for t in self.topics.values() if t.category == category]
    
    def get_active(self) -> List[PromoTopic]:
        """Get all currently active topics."""
        return [t for t in self.topics.values() if t.is_active_for_date()]
    
    def create(self, topic: PromoTopic) -> PromoTopic:
        """Create a new topic."""
        self.topics[topic.id] = topic
        self._save()
        logger.info(f"Created topic: {topic.name}")
        return topic
    
    def update(self, topic_id: str, updates: Dict[str, Any]) -> Optional[PromoTopic]:
        """Update a topic."""
        if topic_id not in self.topics:
            return None
        
        topic = self.topics[topic_id]
        topic_dict = topic.to_dict()
        
        # Handle nested updates
        if "subjects" not in updates:
            updates["subjects"] = topic_dict["subjects"]
        
        topic_dict.update(updates)
        self.topics[topic_id] = PromoTopic.from_dict(topic_dict)
        self._save()
        return self.topics[topic_id]
    
    def delete(self, topic_id: str) -> bool:
        """Delete a topic."""
        if topic_id in self.topics:
            del self.topics[topic_id]
            self._save()
            return True
        return False
    
    def add_subject(self, topic_id: str, text: str) -> Optional[TopicSubject]:
        """Add a subject to a topic."""
        topic = self.get(topic_id)
        if not topic:
            return None
        
        subject = topic.add_subject(text)
        self._save()
        return subject
    
    def remove_subject(self, topic_id: str, subject_id: int) -> bool:
        """Remove a subject from a topic."""
        topic = self.get(topic_id)
        if not topic:
            return False
        
        result = topic.remove_subject(subject_id)
        if result:
            self._save()
        return result
    
    def use_subject(self, topic_id: str, subject_id: int) -> Optional[TopicSubject]:
        """Mark a subject as used."""
        topic = self.get(topic_id)
        if not topic:
            return None
        
        subject = topic.use_subject(subject_id)
        if subject:
            self._save()
        return subject
    
    def export_csv(self, topic_id: str) -> Optional[str]:
        """Export topic subjects to CSV string."""
        topic = self.get(topic_id)
        if not topic:
            return None
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Subject", "Used Count", "Last Used", "Active"])
        
        for subject in topic.subjects:
            writer.writerow([
                subject.text,
                subject.used_count,
                subject.last_used or "",
                "Yes" if subject.active else "No"
            ])
        
        return output.getvalue()
    
    def import_csv(self, topic_id: str, csv_content: str) -> int:
        """Import subjects from CSV. Returns count of imported."""
        topic = self.get(topic_id)
        if not topic:
            return 0
        
        reader = csv.reader(StringIO(csv_content))
        count = 0
        
        # Skip header if present
        first_row = next(reader, None)
        if first_row and first_row[0].lower() not in ["subject", "text", "name"]:
            # First row is data, add it
            topic.add_subject(first_row[0])
            count += 1
        
        for row in reader:
            if row and row[0].strip():
                topic.add_subject(row[0].strip())
                count += 1
        
        self._save()
        logger.info(f"Imported {count} subjects to {topic.name}")
        return count


# Convenience function
def get_promo_topics_manager() -> PromoTopicsManager:
    """Get the default promo topics manager instance."""
    return PromoTopicsManager()
