"""
Script Queue for Neon Frequency
================================
RoboDJ-style script generation queue with status tracking,
voice generation, and batch processing.
"""

import os
import json
import logging
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pathlib import Path

logger = logging.getLogger("AEN.ScriptQueue")


class ScriptStatus(Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class GeneratedScript:
    """
    A generated script with status tracking and voice track info.
    """
    id: str
    name: str
    prompt_id: str
    content: str
    status: ScriptStatus = ScriptStatus.PENDING
    
    # Voice track info
    voice_track_path: Optional[str] = None
    voice_generated_at: Optional[str] = None
    
    # Context used for generation
    input_song: Optional[str] = None
    input_artist: Optional[str] = None
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def has_voice_track(self) -> bool:
        """Check if voice track has been generated."""
        return self.voice_track_path is not None and os.path.exists(self.voice_track_path)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "prompt_id": self.prompt_id,
            "content": self.content,
            "status": self.status.value,
            "voice_track_path": self.voice_track_path,
            "voice_generated_at": self.voice_generated_at,
            "input_song": self.input_song,
            "input_artist": self.input_artist,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GeneratedScript":
        return cls(
            id=data["id"],
            name=data["name"],
            prompt_id=data["prompt_id"],
            content=data["content"],
            status=ScriptStatus(data.get("status", "pending")),
            voice_track_path=data.get("voice_track_path"),
            voice_generated_at=data.get("voice_generated_at"),
            input_song=data.get("input_song"),
            input_artist=data.get("input_artist"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat())
        )


class ScriptQueue:
    """
    Manages a queue of generated scripts with persistence.
    
    Inspired by RoboDJ's Script/VO Generation feature.
    """
    
    def __init__(self, storage_path: Optional[str] = None, output_dir: Optional[str] = None):
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), "data", "scripts.json"
        )
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(__file__), "data", "voice_tracks"
        )
        self.scripts: Dict[str, GeneratedScript] = {}
        self._load()
    
    def _load(self) -> None:
        """Load scripts from storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for script_data in data.get("scripts", []):
                        script = GeneratedScript.from_dict(script_data)
                        self.scripts[script.id] = script
                logger.info(f"Loaded {len(self.scripts)} scripts from {self.storage_path}")
            except Exception as e:
                logger.error(f"Failed to load scripts: {e}")
        else:
            logger.info("No existing scripts file, starting fresh")
    
    def _save(self) -> None:
        """Persist scripts to storage."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "scripts": [s.to_dict() for s in self.scripts.values()],
            "updated_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(self.scripts)} scripts")
    
    def _generate_id(self, name: str, timestamp: str) -> str:
        """Generate a unique ID for a script."""
        hash_input = f"{name}:{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    def get(self, script_id: str) -> Optional[GeneratedScript]:
        """Get a script by ID."""
        return self.scripts.get(script_id)
    
    def get_all(self) -> List[GeneratedScript]:
        """Get all scripts, sorted by created_at descending."""
        return sorted(
            self.scripts.values(),
            key=lambda s: s.created_at,
            reverse=True
        )
    
    def get_by_status(self, status: ScriptStatus) -> List[GeneratedScript]:
        """Get scripts by status."""
        return [s for s in self.scripts.values() if s.status == status]
    
    def get_pending_review(self) -> List[GeneratedScript]:
        """Get scripts awaiting review."""
        return self.get_by_status(ScriptStatus.UNDER_REVIEW)
    
    def get_complete(self) -> List[GeneratedScript]:
        """Get completed scripts."""
        return self.get_by_status(ScriptStatus.COMPLETE)
    
    def add(
        self,
        name: str,
        prompt_id: str,
        content: str,
        input_song: Optional[str] = None,
        input_artist: Optional[str] = None
    ) -> GeneratedScript:
        """Add a new script to the queue."""
        timestamp = datetime.now().isoformat()
        script_id = self._generate_id(name, timestamp)
        
        script = GeneratedScript(
            id=script_id,
            name=name,
            prompt_id=prompt_id,
            content=content,
            status=ScriptStatus.UNDER_REVIEW,
            input_song=input_song,
            input_artist=input_artist,
            created_at=timestamp,
            updated_at=timestamp
        )
        
        self.scripts[script_id] = script
        self._save()
        logger.info(f"Added script to queue: {name}")
        return script
    
    def update_content(self, script_id: str, new_content: str) -> Optional[GeneratedScript]:
        """Update script content (for manual edits)."""
        if script_id not in self.scripts:
            return None
        
        script = self.scripts[script_id]
        script.content = new_content
        script.updated_at = datetime.now().isoformat()
        self._save()
        logger.info(f"Updated script content: {script_id}")
        return script
    
    def set_status(self, script_id: str, status: ScriptStatus) -> Optional[GeneratedScript]:
        """Update script status."""
        if script_id not in self.scripts:
            return None
        
        script = self.scripts[script_id]
        script.status = status
        script.updated_at = datetime.now().isoformat()
        self._save()
        logger.info(f"Updated script status: {script_id} -> {status.value}")
        return script
    
    def approve(self, script_id: str) -> Optional[GeneratedScript]:
        """Approve a script."""
        return self.set_status(script_id, ScriptStatus.APPROVED)
    
    def mark_complete(self, script_id: str, voice_track_path: str) -> Optional[GeneratedScript]:
        """Mark script as complete with voice track."""
        if script_id not in self.scripts:
            return None
        
        script = self.scripts[script_id]
        script.status = ScriptStatus.COMPLETE
        script.voice_track_path = voice_track_path
        script.voice_generated_at = datetime.now().isoformat()
        script.updated_at = datetime.now().isoformat()
        self._save()
        logger.info(f"Script complete with voice track: {script_id}")
        return script
    
    def delete(self, script_id: str) -> bool:
        """Delete a script and its voice track."""
        if script_id not in self.scripts:
            return False
        
        script = self.scripts[script_id]
        
        # Delete voice track file if exists
        if script.voice_track_path and os.path.exists(script.voice_track_path):
            try:
                os.remove(script.voice_track_path)
                logger.info(f"Deleted voice track: {script.voice_track_path}")
            except Exception as e:
                logger.warning(f"Failed to delete voice track: {e}")
        
        del self.scripts[script_id]
        self._save()
        logger.info(f"Deleted script: {script_id}")
        return True
    
    def delete_all(self) -> int:
        """Delete all scripts. Returns count of deleted."""
        count = len(self.scripts)
        
        # Delete all voice track files
        for script in self.scripts.values():
            if script.voice_track_path and os.path.exists(script.voice_track_path):
                try:
                    os.remove(script.voice_track_path)
                except Exception as e:
                    logger.warning(f"Failed to delete voice track: {e}")
        
        self.scripts.clear()
        self._save()
        logger.info(f"Deleted all {count} scripts")
        return count
    
    def get_stats(self) -> Dict[str, int]:
        """Get queue statistics."""
        stats = {
            "total": len(self.scripts),
            "pending": 0,
            "under_review": 0,
            "approved": 0,
            "complete": 0,
            "failed": 0
        }
        for script in self.scripts.values():
            stats[script.status.value] = stats.get(script.status.value, 0) + 1
        return stats


class ScriptGenerator:
    """
    Generates scripts from prompts using AI.
    
    Integrates with the ContentEngine for LLM-powered generation.
    """
    
    def __init__(self, queue: Optional[ScriptQueue] = None):
        self.queue = queue or ScriptQueue()
        self._content_engine = None
    
    @property
    def content_engine(self):
        """Lazy load content engine."""
        if self._content_engine is None:
            from content_engine import ContentEngine
            self._content_engine = ContentEngine()
        return self._content_engine
    
    def generate_from_prompt(
        self,
        prompt,  # Prompt object from prompt_library
        input_song: Optional[str] = None,
        input_artist: Optional[str] = None,
        custom_vars: Optional[Dict[str, str]] = None
    ) -> GeneratedScript:
        """
        Generate a script from a prompt template.
        
        Args:
            prompt: Prompt object with template
            input_song: Current/next song for substitution
            input_artist: Current/next artist for substitution
            custom_vars: Additional custom variables
            
        Returns:
            GeneratedScript added to queue
        """
        # Substitute variables in prompt
        processed_content = prompt.substitute_variables(
            input_song=input_song,
            input_artist=input_artist,
            custom_vars=custom_vars
        )
        
        # If custom script, use content as-is
        if prompt.is_custom_script:
            script_content = processed_content
        else:
            # Generate with AI
            script_content = self.content_engine._generate_with_llm(
                processed_content,
                system_prompt=f"You are {os.getenv('DJ_PERSONALITY', 'AEN')}, a radio DJ."
            )
            
            if not script_content:
                # Fallback to processed content
                script_content = processed_content
        
        # Build script name
        name_parts = [prompt.name]
        if input_artist:
            name_parts.append(input_artist)
        if input_song:
            name_parts.append(input_song)
        script_name = ": ".join(name_parts)
        
        # Add to queue
        return self.queue.add(
            name=script_name,
            prompt_id=prompt.id,
            content=script_content,
            input_song=input_song,
            input_artist=input_artist
        )
    
    def regenerate(self, script_id: str) -> Optional[GeneratedScript]:
        """Regenerate a script using same prompt and inputs."""
        script = self.queue.get(script_id)
        if not script:
            return None
        
        from prompt_library import get_prompt_library
        library = get_prompt_library()
        prompt = library.get(script.prompt_id)
        
        if not prompt:
            logger.error(f"Prompt not found: {script.prompt_id}")
            return None
        
        # Generate new content
        new_script = self.generate_from_prompt(
            prompt,
            input_song=script.input_song,
            input_artist=script.input_artist
        )
        
        # Delete old script
        self.queue.delete(script_id)
        
        return new_script


# Convenience functions
def get_script_queue() -> ScriptQueue:
    """Get the default script queue instance."""
    return ScriptQueue()


def get_script_generator() -> ScriptGenerator:
    """Get the default script generator instance."""
    return ScriptGenerator()
