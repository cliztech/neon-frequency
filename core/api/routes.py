"""
API Routes for Neon Frequency Studio
=====================================
FastAPI endpoints for prompt library, script queue,
content scheduler, and promo topics.
"""

import os
import uuid
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from brain.prompt_library import (
    PromptLibrary, Prompt, PromptCategory, PromptStatus,
    VoiceSettings, TriggerRules, AISettings, TTSProvider, VTMarkerPosition
)
from brain.script_queue import (
    ScriptQueue, ScriptGenerator, GeneratedScript, ScriptStatus
)
from brain.content_scheduler import (
    ContentScheduler, Schedule, ScheduleInterval, ScheduleMode
)
from brain.promo_topics import (
    PromoTopicsManager, PromoTopic, TopicSubject, TopicCategory, TopicMode
)

logger = logging.getLogger("AEN.API")

# Initialize FastAPI app
app = FastAPI(
    title="Neon Frequency API",
    description="RoboDJ-style radio automation API",
    version="2.0.0"
)

# Enable CORS for the Studio frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
prompt_library = PromptLibrary()
script_queue = ScriptQueue()
script_generator = ScriptGenerator(script_queue)
content_scheduler = ContentScheduler()
promo_topics = PromoTopicsManager()


# ================== Pydantic Models ==================

class VoiceSettingsModel(BaseModel):
    provider: str = "ElevenLabs"
    voice_profile: str = "Default"
    model_override: Optional[str] = None


class TriggerRulesModel(BaseModel):
    vt_marker_name: Optional[str] = None
    position: str = "After Marker"
    custom_filename: Optional[str] = None


class AISettingsModel(BaseModel):
    model_name: Optional[str] = None
    temperature: float = 0.8
    max_tokens: int = 200


class PromptCreate(BaseModel):
    name: str
    content: str
    category: str = "General"
    status: str = "active"
    is_custom_script: bool = False
    voice_settings: Optional[VoiceSettingsModel] = None
    trigger_rules: Optional[TriggerRulesModel] = None
    ai_settings: Optional[AISettingsModel] = None
    output_folder: Optional[str] = None


class PromptUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    is_custom_script: Optional[bool] = None
    voice_settings: Optional[VoiceSettingsModel] = None
    trigger_rules: Optional[TriggerRulesModel] = None
    ai_settings: Optional[AISettingsModel] = None
    output_folder: Optional[str] = None


class GenerateScriptRequest(BaseModel):
    prompt_id: str
    input_song: Optional[str] = None
    input_artist: Optional[str] = None
    custom_vars: Optional[Dict[str, str]] = None


class ScriptUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[str] = None


class ScheduleCreate(BaseModel):
    name: str
    interval: str = "Every hour"
    minute_offset: int = 57
    mode: str = "Auto"
    prompt_ids: List[str] = []
    enabled: bool = True


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    interval: Optional[str] = None
    minute_offset: Optional[int] = None
    mode: Optional[str] = None
    prompt_ids: Optional[List[str]] = None
    enabled: Optional[bool] = None


class TopicCreate(BaseModel):
    name: str
    category: str = "General"
    mode: str = "List Mode"
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class TopicUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    mode: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class SubjectCreate(BaseModel):
    text: str


# ================== Prompts Endpoints ==================

@app.get("/api/prompts", tags=["Prompts"])
async def list_prompts(
    category: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """List all prompts, optionally filtered."""
    prompts = prompt_library.get_all()
    
    if category:
        prompts = [p for p in prompts if p.category.value == category]
    if status:
        prompts = [p for p in prompts if p.status.value == status]
    
    return [p.to_dict() for p in prompts]


@app.get("/api/prompts/{prompt_id}", tags=["Prompts"])
async def get_prompt(prompt_id: str) -> Dict[str, Any]:
    """Get a single prompt by ID."""
    prompt = prompt_library.get(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt.to_dict()


@app.post("/api/prompts", tags=["Prompts"])
async def create_prompt(data: PromptCreate) -> Dict[str, Any]:
    """Create a new prompt."""
    prompt_id = str(uuid.uuid4())[:8]
    
    prompt = Prompt(
        id=prompt_id,
        name=data.name,
        content=data.content,
        category=PromptCategory(data.category),
        status=PromptStatus(data.status),
        is_custom_script=data.is_custom_script,
        output_folder=data.output_folder
    )
    
    if data.voice_settings:
        prompt.voice_settings = VoiceSettings(
            provider=TTSProvider(data.voice_settings.provider),
            voice_profile=data.voice_settings.voice_profile,
            model_override=data.voice_settings.model_override
        )
    
    if data.trigger_rules:
        prompt.trigger_rules = TriggerRules(
            vt_marker_name=data.trigger_rules.vt_marker_name,
            position=VTMarkerPosition(data.trigger_rules.position),
            custom_filename=data.trigger_rules.custom_filename
        )
    
    if data.ai_settings:
        prompt.ai_settings = AISettings(
            model_name=data.ai_settings.model_name,
            temperature=data.ai_settings.temperature,
            max_tokens=data.ai_settings.max_tokens
        )
    
    created = prompt_library.create(prompt)
    return created.to_dict()


@app.put("/api/prompts/{prompt_id}", tags=["Prompts"])
async def update_prompt(prompt_id: str, data: PromptUpdate) -> Dict[str, Any]:
    """Update a prompt."""
    updates = {k: v for k, v in data.dict().items() if v is not None}
    
    # Convert nested objects
    if "voice_settings" in updates and updates["voice_settings"]:
        updates["voice_settings"] = dict(updates["voice_settings"])
    if "trigger_rules" in updates and updates["trigger_rules"]:
        updates["trigger_rules"] = dict(updates["trigger_rules"])
    if "ai_settings" in updates and updates["ai_settings"]:
        updates["ai_settings"] = dict(updates["ai_settings"])
    
    prompt = prompt_library.update(prompt_id, updates)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt.to_dict()


@app.delete("/api/prompts/{prompt_id}", tags=["Prompts"])
async def delete_prompt(prompt_id: str) -> Dict[str, str]:
    """Delete a prompt."""
    if not prompt_library.delete(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"status": "deleted"}


@app.get("/api/prompts/variables/list", tags=["Prompts"])
async def list_variables() -> List[Dict[str, str]]:
    """List available dynamic variables."""
    from brain.prompt_library import DYNAMIC_VARIABLES
    return [
        {"name": var.replace("{{", "").replace("}}", ""), "syntax": var}
        for var in DYNAMIC_VARIABLES.keys()
    ] + [
        {"name": "INPUT_SONG", "syntax": "INPUT_SONG"},
        {"name": "INPUT_ARTIST", "syntax": "INPUT_ARTIST"}
    ]


# ================== Scripts Endpoints ==================

@app.get("/api/scripts", tags=["Scripts"])
async def list_scripts(
    status: Optional[str] = None,
    limit: int = Query(50, le=100)
) -> List[Dict[str, Any]]:
    """List all scripts."""
    scripts = script_queue.get_all()[:limit]
    
    if status:
        scripts = [s for s in scripts if s.status.value == status]
    
    return [s.to_dict() for s in scripts]


@app.get("/api/scripts/stats", tags=["Scripts"])
async def get_script_stats() -> Dict[str, int]:
    """Get script queue statistics."""
    return script_queue.get_stats()


@app.get("/api/scripts/{script_id}", tags=["Scripts"])
async def get_script(script_id: str) -> Dict[str, Any]:
    """Get a single script."""
    script = script_queue.get(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return script.to_dict()


@app.post("/api/scripts/generate", tags=["Scripts"])
async def generate_script(data: GenerateScriptRequest) -> Dict[str, Any]:
    """Generate a new script from a prompt."""
    prompt = prompt_library.get(data.prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    script = script_generator.generate_from_prompt(
        prompt,
        input_song=data.input_song,
        input_artist=data.input_artist,
        custom_vars=data.custom_vars
    )
    
    return script.to_dict()


@app.put("/api/scripts/{script_id}", tags=["Scripts"])
async def update_script(script_id: str, data: ScriptUpdate) -> Dict[str, Any]:
    """Update script content or status."""
    script = script_queue.get(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    if data.content:
        script_queue.update_content(script_id, data.content)
    
    if data.status:
        script_queue.set_status(script_id, ScriptStatus(data.status))
    
    return script_queue.get(script_id).to_dict()


@app.post("/api/scripts/{script_id}/approve", tags=["Scripts"])
async def approve_script(script_id: str) -> Dict[str, Any]:
    """Approve a script."""
    script = script_queue.approve(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return script.to_dict()


@app.post("/api/scripts/{script_id}/regenerate", tags=["Scripts"])
async def regenerate_script(script_id: str) -> Dict[str, Any]:
    """Regenerate a script with same inputs."""
    script = script_generator.regenerate(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="Script not found or prompt missing")
    return script.to_dict()


@app.delete("/api/scripts/{script_id}", tags=["Scripts"])
async def delete_script(script_id: str) -> Dict[str, str]:
    """Delete a script."""
    if not script_queue.delete(script_id):
        raise HTTPException(status_code=404, detail="Script not found")
    return {"status": "deleted"}


@app.delete("/api/scripts", tags=["Scripts"])
async def delete_all_scripts() -> Dict[str, int]:
    """Delete all scripts."""
    count = script_queue.delete_all()
    return {"deleted": count}


# ================== Schedules Endpoints ==================

@app.get("/api/schedules", tags=["Schedules"])
async def list_schedules() -> List[Dict[str, Any]]:
    """List all schedules."""
    return [s.to_dict() for s in content_scheduler.get_all()]


@app.get("/api/schedules/{schedule_id}", tags=["Schedules"])
async def get_schedule(schedule_id: str) -> Dict[str, Any]:
    """Get a single schedule."""
    schedule = content_scheduler.get(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule.to_dict()


@app.post("/api/schedules", tags=["Schedules"])
async def create_schedule(data: ScheduleCreate) -> Dict[str, Any]:
    """Create a new schedule."""
    schedule_id = str(uuid.uuid4())[:8]
    
    schedule = Schedule(
        id=schedule_id,
        name=data.name,
        interval=ScheduleInterval(data.interval),
        minute_offset=data.minute_offset,
        mode=ScheduleMode(data.mode),
        prompt_ids=data.prompt_ids,
        enabled=data.enabled
    )
    
    created = content_scheduler.create(schedule)
    return created.to_dict()


@app.put("/api/schedules/{schedule_id}", tags=["Schedules"])
async def update_schedule(schedule_id: str, data: ScheduleUpdate) -> Dict[str, Any]:
    """Update a schedule."""
    updates = {k: v for k, v in data.dict().items() if v is not None}
    
    schedule = content_scheduler.update(schedule_id, updates)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule.to_dict()


@app.post("/api/schedules/{schedule_id}/toggle", tags=["Schedules"])
async def toggle_schedule(schedule_id: str) -> Dict[str, Any]:
    """Toggle schedule enabled/disabled."""
    schedule = content_scheduler.toggle(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule.to_dict()


@app.delete("/api/schedules/{schedule_id}", tags=["Schedules"])
async def delete_schedule(schedule_id: str) -> Dict[str, str]:
    """Delete a schedule."""
    if not content_scheduler.delete(schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"status": "deleted"}


# ================== Topics Endpoints ==================

@app.get("/api/topics", tags=["Topics"])
async def list_topics(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all promo topics."""
    topics = promo_topics.get_all()
    
    if category:
        topics = [t for t in topics if t.category.value == category]
    
    return [t.to_dict() for t in topics]


@app.get("/api/topics/{topic_id}", tags=["Topics"])
async def get_topic(topic_id: str) -> Dict[str, Any]:
    """Get a single topic."""
    topic = promo_topics.get(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic.to_dict()


@app.post("/api/topics", tags=["Topics"])
async def create_topic(data: TopicCreate) -> Dict[str, Any]:
    """Create a new topic."""
    topic_id = str(uuid.uuid4())[:8]
    
    topic = PromoTopic(
        id=topic_id,
        name=data.name,
        category=TopicCategory(data.category),
        mode=TopicMode(data.mode),
        start_date=data.start_date,
        end_date=data.end_date
    )
    
    created = promo_topics.create(topic)
    return created.to_dict()


@app.put("/api/topics/{topic_id}", tags=["Topics"])
async def update_topic(topic_id: str, data: TopicUpdate) -> Dict[str, Any]:
    """Update a topic."""
    updates = {k: v for k, v in data.dict().items() if v is not None}
    
    topic = promo_topics.update(topic_id, updates)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic.to_dict()


@app.delete("/api/topics/{topic_id}", tags=["Topics"])
async def delete_topic(topic_id: str) -> Dict[str, str]:
    """Delete a topic."""
    if not promo_topics.delete(topic_id):
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"status": "deleted"}


@app.post("/api/topics/{topic_id}/subjects", tags=["Topics"])
async def add_subject(topic_id: str, data: SubjectCreate) -> Dict[str, Any]:
    """Add a subject to a topic."""
    subject = promo_topics.add_subject(topic_id, data.text)
    if not subject:
        raise HTTPException(status_code=404, detail="Topic not found")
    return subject.to_dict()


@app.delete("/api/topics/{topic_id}/subjects/{subject_id}", tags=["Topics"])
async def remove_subject(topic_id: str, subject_id: int) -> Dict[str, str]:
    """Remove a subject from a topic."""
    if not promo_topics.remove_subject(topic_id, subject_id):
        raise HTTPException(status_code=404, detail="Topic or subject not found")
    return {"status": "deleted"}


@app.post("/api/topics/{topic_id}/subjects/{subject_id}/use", tags=["Topics"])
async def use_subject(topic_id: str, subject_id: int) -> Dict[str, Any]:
    """Mark a subject as used."""
    subject = promo_topics.use_subject(topic_id, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Topic or subject not found")
    return subject.to_dict()


@app.get("/api/topics/{topic_id}/export", tags=["Topics"])
async def export_topic_csv(topic_id: str) -> Dict[str, str]:
    """Export topic subjects as CSV."""
    csv_content = promo_topics.export_csv(topic_id)
    if csv_content is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"csv": csv_content}


@app.post("/api/topics/{topic_id}/import", tags=["Topics"])
async def import_topic_csv(topic_id: str, csv_content: str) -> Dict[str, int]:
    """Import subjects from CSV."""
    count = promo_topics.import_csv(topic_id, csv_content)
    return {"imported": count}


# ================== Dashboard Endpoints ==================

@app.get("/api/dashboard", tags=["Dashboard"])
async def get_dashboard() -> Dict[str, Any]:
    """Get dashboard summary data."""
    return {
        "schedules": {
            "active": len(content_scheduler.get_active()),
            "total": len(content_scheduler.get_all()),
            "next_runs": [
                {"name": s.name, "next_run": s.next_run, "time_remaining": s.get_time_remaining()}
                for s in content_scheduler.get_active()[:3]
            ]
        },
        "prompts": {
            "active": len(prompt_library.get_active()),
            "total": len(prompt_library.get_all())
        },
        "topics": {
            "active": len(promo_topics.get_active()),
            "total": len(promo_topics.get_all())
        },
        "scripts": script_queue.get_stats()
    }


# ================== Health Check ==================

@app.get("/health", tags=["System"])
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "version": "2.0.0"}


# Run with: uvicorn core.api.routes:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
