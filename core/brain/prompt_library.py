"""
Prompt Library for Neon Frequency
==================================
RoboDJ-style prompt management with dynamic variables, categories,
voice profiles, and scheduling triggers.
"""

import os
import json
import re
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pathlib import Path

logger = logging.getLogger("AEN.PromptLibrary")


class PromptStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DRAFT = "draft"


class PromptCategory(Enum):
    GENERAL = "General"
    PROMOS = "Promos"
    WEATHER = "Weather"
    NEWS = "News"
    SONG_INTRO = "Song Intro"
    SONG_OUTRO = "Song Outro"
    STATION_ID = "Station ID"
    AD_BREAK = "Ad Break"
    SHOUTOUTS = "ShoutOuts"
    CUSTOM = "Custom"


class VTMarkerPosition(Enum):
    BEFORE_MARKER = "Before Marker"
    AFTER_MARKER = "After Marker"
    BOTH = "Both"


class TTSProvider(Enum):
    ELEVENLABS = "ElevenLabs"
    GEMINI = "Gemini"
    OPENAI = "OpenAI"


# Built-in dynamic variables
DYNAMIC_VARIABLES = {
    "{{GREETING}}": lambda: _get_greeting(),
    "{{DAY}}": lambda: datetime.now().strftime("%A"),
    "{{DATE}}": lambda: datetime.now().strftime("%B %d, %Y"),
    "{{CASUAL_TIME}}": lambda: _get_casual_time(),
    "{{TIME}}": lambda: datetime.now().strftime("%I:%M %p"),
    "{{STATION_NAME}}": lambda: os.getenv("STATION_NAME", "Neon Frequency"),
    "{{STATION_TAGLINE}}": lambda: os.getenv("STATION_TAGLINE", "The Future of Sound"),
    "{{DJ_NAME}}": lambda: os.getenv("DJ_PERSONALITY", "AEN"),
}


def _get_greeting() -> str:
    """Get appropriate greeting based on time of day."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"


def _get_casual_time() -> str:
    """Get casual time description."""
    hour = datetime.now().hour
    minute = datetime.now().minute
    
    if minute < 10:
        minute_str = f"just after {hour % 12 or 12}"
    elif minute < 20:
        minute_str = f"about quarter past {hour % 12 or 12}"
    elif minute < 40:
        minute_str = f"around half past {hour % 12 or 12}"
    elif minute < 50:
        minute_str = f"about quarter to {(hour + 1) % 12 or 12}"
    else:
        minute_str = f"almost {(hour + 1) % 12 or 12}"
    
    return minute_str


@dataclass
class VoiceSettings:
    """Voice configuration for TTS."""
    provider: TTSProvider = TTSProvider.ELEVENLABS
    voice_profile: str = "Default"
    model_override: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider.value,
            "voice_profile": self.voice_profile,
            "model_override": self.model_override
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VoiceSettings":
        return cls(
            provider=TTSProvider(data.get("provider", "ElevenLabs")),
            voice_profile=data.get("voice_profile", "Default"),
            model_override=data.get("model_override")
        )


@dataclass
class TriggerRules:
    """Trigger rules for when to use this prompt."""
    vt_marker_name: Optional[str] = None
    position: VTMarkerPosition = VTMarkerPosition.AFTER_MARKER
    custom_filename: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "vt_marker_name": self.vt_marker_name,
            "position": self.position.value,
            "custom_filename": self.custom_filename
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerRules":
        return cls(
            vt_marker_name=data.get("vt_marker_name"),
            position=VTMarkerPosition(data.get("position", "After Marker")),
            custom_filename=data.get("custom_filename")
        )


@dataclass
class AISettings:
    """AI model settings for script generation."""
    model_name: Optional[str] = None  # None = use global default
    temperature: float = 0.8
    max_tokens: int = 200
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AISettings":
        return cls(
            model_name=data.get("model_name"),
            temperature=data.get("temperature", 0.8),
            max_tokens=data.get("max_tokens", 200)
        )


@dataclass
class Prompt:
    """
    A prompt template for AI script generation.
    
    Supports dynamic variables like {{GREETING}}, {{DAY}}, {{STATION_NAME}}
    and input variables like INPUT_SONG, INPUT_ARTIST.
    """
    id: str
    name: str
    content: str
    category: PromptCategory = PromptCategory.GENERAL
    status: PromptStatus = PromptStatus.ACTIVE
    is_custom_script: bool = False  # If true, skip AI generation
    
    # Settings
    voice_settings: VoiceSettings = field(default_factory=VoiceSettings)
    trigger_rules: TriggerRules = field(default_factory=TriggerRules)
    ai_settings: AISettings = field(default_factory=AISettings)
    
    # Output
    output_folder: Optional[str] = None
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def substitute_variables(
        self,
        input_song: Optional[str] = None,
        input_artist: Optional[str] = None,
        custom_vars: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Replace all dynamic variables in the prompt content.
        
        Args:
            input_song: Current/next song title
            input_artist: Current/next artist name
            custom_vars: Additional custom variables
            
        Returns:
            Prompt content with all variables substituted
        """
        result = self.content
        
        # Replace built-in dynamic variables
        for var, getter in DYNAMIC_VARIABLES.items():
            if var in result:
                result = result.replace(var, getter())
        
        # Replace input variables
        if input_song:
            result = result.replace("INPUT_SONG", input_song)
            result = result.replace("{{INPUT_SONG}}", input_song)
        if input_artist:
            result = result.replace("INPUT_ARTIST", input_artist)
            result = result.replace("{{INPUT_ARTIST}}", input_artist)
        
        # Replace custom variables
        if custom_vars:
            for key, value in custom_vars.items():
                result = result.replace(f"{{{{{key}}}}}", value)
                result = result.replace(key, value)
        
        return result
    
    def get_available_variables(self) -> List[str]:
        """Extract all variables used in this prompt."""
        pattern = r'\{\{([A-Z_]+)\}\}|INPUT_[A-Z]+'
        matches = re.findall(pattern, self.content)
        return list(set(matches))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "category": self.category.value,
            "status": self.status.value,
            "is_custom_script": self.is_custom_script,
            "voice_settings": self.voice_settings.to_dict(),
            "trigger_rules": self.trigger_rules.to_dict(),
            "ai_settings": self.ai_settings.to_dict(),
            "output_folder": self.output_folder,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prompt":
        """Create Prompt from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            content=data["content"],
            category=PromptCategory(data.get("category", "General")),
            status=PromptStatus(data.get("status", "active")),
            is_custom_script=data.get("is_custom_script", False),
            voice_settings=VoiceSettings.from_dict(data.get("voice_settings", {})),
            trigger_rules=TriggerRules.from_dict(data.get("trigger_rules", {})),
            ai_settings=AISettings.from_dict(data.get("ai_settings", {})),
            output_folder=data.get("output_folder"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat())
        )


class PromptLibrary:
    """
    Manages a collection of prompts with persistence.
    
    Inspired by RoboDJ's Prompt Library feature.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), "data", "prompts.json"
        )
        self.prompts: Dict[str, Prompt] = {}
        self._load()
    
    def _load(self) -> None:
        """Load prompts from storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for prompt_data in data.get("prompts", []):
                        prompt = Prompt.from_dict(prompt_data)
                        self.prompts[prompt.id] = prompt
                logger.info(f"Loaded {len(self.prompts)} prompts from {self.storage_path}")
            except Exception as e:
                logger.error(f"Failed to load prompts: {e}")
        else:
            logger.info("No existing prompts file, starting fresh")
            self._create_default_prompts()
    
    def _save(self) -> None:
        """Persist prompts to storage."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "prompts": [p.to_dict() for p in self.prompts.values()],
            "updated_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(self.prompts)} prompts")
    
    def _create_default_prompts(self) -> None:
        """Create default prompt templates."""
        defaults = [
            Prompt(
                id="toh_time_artist",
                name="TOH-Time_Artist",
                category=PromptCategory.PROMOS,
                content="""You are an experienced radio DJ known for making even routine announcements sound fresh and engaging. Complete this 16-second radio script. It MUST start with this exact opening:

{{GREETING}} everyone! It's {{DAY}}, {{CASUAL_TIME}} on {{STATION_NAME}}

THEN mention my name, and how I'm playing another hour of music and mention artist name: INPUT_ARTIST

#Requirements:
-Maximum 48 words / 17 seconds when spoken
-Must end with station ID
-No quotation marks in output, although questions written as sentences are allowed.
-No system text or other messages, just the script.
-Focus on creating genuine enthusiasm without sounding sales-y"""
            ),
            Prompt(
                id="song_intro",
                name="Song Intro",
                category=PromptCategory.SONG_INTRO,
                content="""Generate a short, energetic intro for the next song.

Now playing: INPUT_SONG by INPUT_ARTIST
Weather: {{WEATHER}}
Time: {{CASUAL_TIME}}

Write 1-2 sentences only. Be engaging and natural."""
            ),
            Prompt(
                id="weather_update",
                name="Weather Update",
                category=PromptCategory.WEATHER,
                content="""Quick weather update for {{STATION_NAME}} listeners.

Current conditions: {{WEATHER}}
Location: {{LOCATION}}

Keep it under 2 sentences. Make it fit the DJ persona."""
            ),
            Prompt(
                id="station_id",
                name="Station ID",
                category=PromptCategory.STATION_ID,
                content="""Generate a short station ID for {{STATION_NAME}}.

Keep it under 10 words. Make it memorable and punchy.
Tagline: {{STATION_TAGLINE}}"""
            ),
        ]
        
        for prompt in defaults:
            self.prompts[prompt.id] = prompt
        self._save()
    
    def get(self, prompt_id: str) -> Optional[Prompt]:
        """Get a prompt by ID."""
        return self.prompts.get(prompt_id)
    
    def get_all(self) -> List[Prompt]:
        """Get all prompts."""
        return list(self.prompts.values())
    
    def get_by_category(self, category: PromptCategory) -> List[Prompt]:
        """Get prompts by category."""
        return [p for p in self.prompts.values() if p.category == category]
    
    def get_active(self) -> List[Prompt]:
        """Get all active prompts."""
        return [p for p in self.prompts.values() if p.status == PromptStatus.ACTIVE]
    
    def create(self, prompt: Prompt) -> Prompt:
        """Create a new prompt."""
        if prompt.id in self.prompts:
            raise ValueError(f"Prompt with ID {prompt.id} already exists")
        self.prompts[prompt.id] = prompt
        self._save()
        logger.info(f"Created prompt: {prompt.name}")
        return prompt
    
    def update(self, prompt_id: str, updates: Dict[str, Any]) -> Optional[Prompt]:
        """Update an existing prompt."""
        if prompt_id not in self.prompts:
            return None
        
        prompt = self.prompts[prompt_id]
        prompt_dict = prompt.to_dict()
        prompt_dict.update(updates)
        prompt_dict["updated_at"] = datetime.now().isoformat()
        
        self.prompts[prompt_id] = Prompt.from_dict(prompt_dict)
        self._save()
        logger.info(f"Updated prompt: {prompt_id}")
        return self.prompts[prompt_id]
    
    def delete(self, prompt_id: str) -> bool:
        """Delete a prompt."""
        if prompt_id in self.prompts:
            del self.prompts[prompt_id]
            self._save()
            logger.info(f"Deleted prompt: {prompt_id}")
            return True
        return False
    
    def search(self, query: str) -> List[Prompt]:
        """Search prompts by name or content."""
        query_lower = query.lower()
        return [
            p for p in self.prompts.values()
            if query_lower in p.name.lower() or query_lower in p.content.lower()
        ]


# Convenience function
def get_prompt_library() -> PromptLibrary:
    """Get the default prompt library instance."""
    return PromptLibrary()
