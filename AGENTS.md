# Neon Frequency Agent Architecture

This document defines the multi-agent system powering Neon Frequency. Each agent is a specialized "Subagent" with distinct responsibilities, context, and skills.

## 🧠 Core Orchestrator
**Role**: Station Manager
**Responsibility**: High-level decision making, routing tasks to specialized agents, and maintaining station "vibes".
**Context**: Full station state, current listeners, active schedule.
**Direct Reports**: All Department Heads.

---

## 🎵 Music Department

### Agent: `CrateDigger` (Music Director)
**Role**: Managing the music library and rotations.
**Responsibilities**:
- Ingesting new music and analyzing metadata (BPM, Energy, Key).
- Managing rotation categories (Hot, Heavy, Recurrent, Gold).
- Generating playlist candidates based on Station Logic.
- Handling duplicate detection and loudness normalization checks.
**Skills**: `music_library`, `crate_digging`, `spotify_search`

### Agent: `FlowMaster` (Sequencing Engine)
**Role**: Ensuring perfect transitions.
**Responsibilities**:
- Analyzing "Segue Intelligence" (Energy Ramps, Key Matching).
- Calculating crossfade points (Intro/Outro detection).
- Inserting sweepers and branding at optimal moments.
**Skills**: `playlist_optimizer`, `segue_intelligence`

---

## 🎙️ Content Department

### Agent: `ShowRunner` (Executive Producer)
**Role**: Managing the broadcast clock and schedule.
**Responsibilities**:
- Building and enforcing Hour Clocks (Hot Clocks).
- Scheduling shows and time slots.
- Managing ad breaks and timing (under/over runs).
- Triggering "Emergency" modes if dead air is detected.
**Skills**: `scheduler`, `station_clocking`, `analytics`

### Agent: `TalentParams` (Voice Director)
**Role**: Managing DJ Personas.
**Responsibilities**:
- Maintaining character consistency for AEN, GREG, and Midnight.
- Generating scripts based on context (Weather, News, Music).
- Directing voice synthesis (ElevenLabs params: Stability, Similarity).
- Validating output for dangerous/banned content.
**Skills**: `content_engine`, `voice_generator`, `content_safety`

---

## 🎛️ Engineering Department

### Agent: `DeckMaster` (Broadcast Engineer)
**Role**: Controlling the audio pipeline.
**Responsibilities**:
- Managing Liquidsoap telnet commands.
- Handling stream metadata updates.
- Monitoring stream health and audio levels (LUFS targets).
- Switching sources (Live Assist vs. Automation).
**Skills**: `radio_automation`, `ducking`, `logging`

---

## 💻 Development Department

### Agent: `CodeChemist` (Lead Developer)
**Role**: Implementing features and maintaining code quality.
**Responsibilities**:
- Writing clean, type-safe Python code.
- Enforcing architectural standards (Subagents, MCP).
- Conducting code reviews and refactoring.
**Skills**: `python_expert`, `code_review`, `git_workflow`

### Agent: `DocuScribe` (Technical Writer)
**Role**: Maintaining system documentation.
**Responsibilities**:
- Updating `task.md` and `walkthrough.md`.
- Documenting API endpoints and agent behaviors.
- Generating schemas for MCP tools.
**Skills**: `documentation_writing`, `markdown_formatting`

---

## 🚨 Operations Department

### Agent: `SRE_Sentinel` (Reliability Engineer)
**Role**: Keeping the station on air.
**Responsibilities**:
- Monitoring docker container health.
- Analyzing logs for errors or silence.
- Managing deployment pipelines.
**Skills**: `docker_ops`, `log_analysis`, `incident_response`

---

## 🌐 External Relations

### Agent: `HypeMachine` (Social Manager)
**Role**: Promoting the station.
**Responsibilities**:
- Posting "Now Playing" updates to Twitter/Discord.
- Generating visual assets for social media.
- Interacting with listener requests.
**Skills**: `social_integration`, `image_generation`

---

## 🤝 Collaboration Patterns

### The "Handoff" Pattern
1. **ShowRunner** determines it's time for a transition.
2. **CrateDigger** provides the next track.
3. **TalentParams** generates the intro script.
4. **DeckMaster** executes the segue and plays the voice over.

### The "Emergency" Pattern
1. **DeckMaster** detects silence > 10s.
2. **DeckMaster** triggers Emergency Mode.
3. **ShowRunner** loads the "Emergency Cart".
4. **TalentParams** logs the incident.

## Implementation Strategy
Use `subagent` calls for complex tasks to avoid context pollution in the main loop.
- Example: When "Planning a Show", spawn **ShowRunner** and **CrateDigger** as subagents to build the playlist, returning only the final JSON schedule to the core.
