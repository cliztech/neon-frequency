# Neon Frequency: The Virtuoso Protocol

## 1. Prime Directive
We are building a **Synthetic Broadcast Entity**. Code must be **biological**, **resilient**, and **state-aware**.
- **Resilience:** The radio runs 24/7. Exceptions must be caught. Dead air is death.
- **State:** Use `pydantic` models for all internal state and data transfers.
- **Performance:** Audio processing must remain latency-neutral (<200ms).

## 2. Tech Stack & Standards
- **Language:** Python 3.12+ (Type hints required)
- **Frameworks:** `langgraph` (Agents), `fastapi` (API), `pydantic` (Data)
- **Audio:** `liquidsoap` (Broadcast), `ffmpeg` (Processing)
- **Database:** `redis` (Hot State), `json` (Cold Storage - for now)
- **Style:** PEP 8. Use `black` formatting. Docstrings required for all agents.

## 3. Project Structure
- `core/brain/`: Cortex logic, Agents, and Content Engines.
- `core/brain/agents/`: Specialized Subagents (Music, Ops, Dev).
- `broadcast/`: Liquidsoap scripts and Docker configs.
- `assets/`: Audio jingles, beds, and voice samples.

## 4. Development Workflow
1. **Plan first:** Always update `task.md` before starting work.
2. **Modularize:** Keep agents small and focused (`AGENTS.md`).
3. **Verify:** Test generic logic with scripts before full integration.
4. **Document:** Update `walkthrough.md` after significant features.

## 5. Agent Commands (Chat)
- `!skip`: Force fade to next track.
- `!request <query>`: Search and queue a song.
- `!greg`: Trigger a specific interaction with the "Greg" persona.
- `!clock`: Visualize the current hour's programming clock.
- `!stats`: View listener numbers and stream health.
