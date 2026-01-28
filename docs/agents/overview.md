# Agent Overview

This document summarizes the broadcast agents, their responsibilities, and how they connect to documented skills.

## Skills Mapping Reference

Skills are defined in `skills.md`. Each agent is mapped to the closest listed capability (or noted as **None** when no direct match exists).

## Agents

### Scheduler
- **Inputs:** show clock, upcoming segments, timing constraints, priority overrides.
- **Outputs:** ordered run-of-show timeline, handoff timestamps.
- **Required tools:** timeline planner, segment queue manager.
- **Data sources:** show templates, schedule metadata, live clock.
- **Skills mapping:** **None** (no explicit scheduler skill in `skills.md`).
- **Failure modes + fallback:**
  - Drift or missing segment metadata can cause dead air → fall back to safe-mode playback (pre-approved filler bed) and trigger a replan.
  - If timeline planning fails, keep the last known schedule and hold the current segment until safe fallback audio is ready.

### Interview Producer
- **Inputs:** guest briefs, topic prompts, live transcript, segment duration.
- **Outputs:** question queue, follow-up prompts, segment wrap cues.
- **Required tools:** prompt generator, transcript monitor.
- **Data sources:** guest notes, prior episode archives, topic research notes.
- **Skills mapping:** **None** (no interview skill in `skills.md`).
- **Failure modes + fallback:**
  - If prompts stall or transcript lags → insert a neutral wrap-up prompt and hand control back to Scheduler for dead air prevention.
  - If guest data is missing → default to evergreen questions and shorten the segment.

### Voice Director
- **Inputs:** voice track, music bed levels, segment transitions.
- **Outputs:** level-adjusted voice mix, transition timing notes.
- **Required tools:** live mixer, volume automation.
- **Data sources:** mix presets, voice chain settings.
- **Skills mapping:** **Ducking** (manages voice/music balance).【F:skills.md†L4-L4】
- **Failure modes + fallback:**
  - If automation fails → apply conservative -15dB ducking preset and fade to safe-mode playback to avoid dead air.
  - If voice chain drops → mute mic, keep bed playing, alert Scheduler.

### Content Safety
- **Inputs:** live transcript, guest audio, approved/blocked term lists.
- **Outputs:** safety flags, redaction cues, allow/deny verdicts.
- **Required tools:** safety classifier, keyword monitor.
- **Data sources:** policy list, prior safety incidents.
- **Skills mapping:** **None** (no explicit safety skill in `skills.md`).
- **Failure modes + fallback:**
  - If safety model is unavailable → default to safe-mode playback and block live content until review.
  - If false positives surge → use manual override with Compliance Logger to document the decision.

### Showrunner
- **Inputs:** program goals, audience signals, segment performance.
- **Outputs:** segment priorities, host guidance, escalation decisions.
- **Required tools:** analytics dashboard, decision log.
- **Data sources:** audience metrics, engagement history.
- **Skills mapping:** **None** (no showrunner skill in `skills.md`).
- **Failure modes + fallback:**
  - If priorities are unclear → defer to Scheduler defaults and keep a short filler segment queued.
  - If live decisions fail → switch to safe-mode playback and pause dynamic changes.

### Librarian
- **Inputs:** content requests, mood tags, transition requirements.
- **Outputs:** candidate tracks, fallback playlists, metadata notes.
- **Required tools:** vector search, catalog browser.
- **Data sources:** music catalog, metadata embeddings.
- **Skills mapping:** **Crate Digging** (vector search for music).【F:skills.md†L3-L3】
- **Failure modes + fallback:**
  - If search results are empty → return approved fallback playlist to prevent dead air.
  - If catalog lookup fails → replay last known safe-mode playlist.

### Segue Engine
- **Inputs:** outgoing track metadata, incoming track metadata, transition rules.
- **Outputs:** crossfade plan, cue points, transition notes.
- **Required tools:** cue detector, crossfade controller.
- **Data sources:** track metadata, mix rules.
- **Skills mapping:** **None** (no explicit segue skill in `skills.md`).
- **Failure modes + fallback:**
  - If cue detection fails → use fixed-length fade and safe-mode playback until next track is ready.
  - If transition rules are missing → apply default crossfade profile.

### Compliance Logger
- **Inputs:** safety decisions, overrides, system alerts.
- **Outputs:** audit trail, compliance reports, incident summaries.
- **Required tools:** logging pipeline, immutable storage.
- **Data sources:** safety policy list, decision logs.
- **Skills mapping:** **None** (no compliance skill in `skills.md`).
- **Failure modes + fallback:**
  - If logging fails → write to local buffer and notify Showrunner; switch to safe-mode playback if logging is required for compliance.
  - If storage is unavailable → mirror logs to secondary store and tag as provisional.

## Commands Mapping

`skills.md` also documents runtime commands (`!skip`, `!request`, `!greg`). These are typically routed through Scheduler and Showrunner to coordinate operational responses to live requests.【F:skills.md†L7-L10】
