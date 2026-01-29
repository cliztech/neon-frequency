# Master Plan: Project "Neon Frequency"

## Phase 0: Competitive Feature Audit (Radio Automation)
- [ ] Document feature parity vs NextKast + RoboDJ (source links, screenshots, capability notes).
- [ ] Map station clock concepts (hours, dayparts, rotations, sweepers, IDs, ads) into Neon Frequency scheduling model.
- [ ] Define live-assist controls (manual override, hotkeys, instant cart, voice tracks, emergency override).
- [ ] Specify logging + compliance needs (playout logs, ad proof, metadata history, retention policy).
- [ ] Outline library management parity (metadata editor, duplicate detection, normalization, loudness).
- [ ] Establish playout intelligence (auto-segue rules, crossfade profiles, energy ramps).
- [ ] Identify remote control + monitoring features (web dashboard, mobile, alerts, failover).
- [ ] Define third-party integrations (streaming servers, encoder, reporting, social posting).
- [ ] Draft station identity guide (tone, audience, editorial rules, banned topics).
- [ ] Define show formats + daypart programming rules (music/talk/news/ad ratios).
- [ ] Capture rights/licensing requirements and content takedown workflow.

## Phase 1: The Pulse (Core Audio)
- [x] Infrastructure (Docker/Icecast)
- [x] The Deck (Liquidsoap Configuration)
- [ ] The Librarian (Music Scanner)
- [ ] Implement metadata normalization + loudness analysis.
- [ ] Add library de-dupe + content quality checks.

## Phase 2: The Personality (Agent)
- [ ] Implement ElevenLabs API for Voice
- [ ] Connect Real Weather API (Rowville)
- [ ] Implement "Greg" Agent (Parody Hip Hop)
- [ ] Build interview producer agent (schedule, topic discovery, guest briefs, tone selection).
- [ ] Build voice director agent (persona consistency, voice presets, compliance rules).
- [ ] Build content safety agent (profanity routing, age gating, policy tagging).
- [ ] Build showrunner agent (segment pacing, ad breaks, tempo transitions).
- [ ] Build continuity agent (station IDs, stingers, transitions).
- [ ] Build news editor agent (ingest, summarize, localize, fact-check).
- [ ] Build ad copy agent (inventory-aware, compliance-safe scripts).

## Phase 3: The Hallucination (Visuals)
- [ ] Python OSC Emitter
- [ ] TouchDesigner / Three.js Receiver
- [ ] Define OSC event schema (now playing, mood, intensity, alerts).
- [ ] Implement real-time overlays (now playing, headlines, alerts).

## Phase 4: Orchestration & Scheduling
- [ ] Implement station clock engine (hourly templates, rotations, sweepers).
- [ ] Build daypart profiles (morning, midday, drive, late).
- [ ] Add rules engine (artist separation, repeats, energy curves, tempo).
- [ ] Implement dynamic playlist generation (AI-aware segment insertion).
- [ ] Add failover handling for missing assets and empty queues.

## Phase 5: Content Pipelines (Music, Talk, News, Ads)
- [ ] Music ingest pipeline (tags, genre, mood, energy, explicit flags).
- [ ] Talk segment templates (monologues, interviews, promos).
- [ ] Guest persona library (voice, background, opinions, topics).
- [ ] News ingestion (RSS/APIs) with scheduling blocks.
- [ ] Ad inventory model (flights, geo/targeting, frequency caps).
- [ ] Proof-of-play logging for ads and promos.

## Phase 6: Playout & Rendering
- [ ] TTS rendering pipeline (per-persona voices, caching, retries).
- [ ] Audio mastering chain (EQ, compression, loudness normalization).
- [ ] Bed music + SFX mixing for talk segments.
- [ ] Crossfade + auto-segue profiles per daypart.
- [ ] Live-assist overrides with hotkeys + safety ducking.

## Phase 7: Monitoring, QA, & Compliance
- [ ] Stream health checks (silence, clipping, disconnects).
- [ ] Content QA gate (profanity, banned phrases, length, topic blocks).
- [ ] Audit logs + retention policy controls.
- [ ] DMCA/rights takedown workflow (intake, verification, removal, audit trail).
- [ ] Retention policy controls for audio logs and user data (configurable TTLs).
- [ ] Consent and privacy controls for any user-submitted content (upload approvals, revocation).
- [ ] Alerting (Slack/Email/SMS) and incident runbooks.
- [ ] Analytics dashboard (listener minutes, tune-outs, top tracks).

## Phase 8: Admin & Studio UI
- [ ] Authentication + role-based access control.
- [ ] Library management UI (search, edit, duplicates, batch actions).
- [ ] Scheduling UI (clock builder, rotations, daypart rules).
- [ ] Playout dashboard (now playing, upcoming, logs).
- [ ] Host console (carts, hotkeys, voice tracking).
