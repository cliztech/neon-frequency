# Master Plan: Project "Neon Frequency"

## Phase 0: Competitive Feature Audit (Radio Automation)
- [x] Document feature parity vs NextKast + RoboDJ (source links, screenshots, capability notes).
- [x] Research 20+ radio automation tools (see implementation_plan.md in brain folder).
- [x] Map station clock concepts (hours, dayparts, rotations, sweepers, IDs, ads) into Neon Frequency scheduling model.
- [ ] Define live-assist controls (manual override, hotkeys, instant cart, voice tracks, emergency override).
- [ ] Specify logging + compliance needs (playout logs, ad proof, metadata history, retention policy).
- [ ] Outline library management parity (metadata editor, duplicate detection, normalization, loudness).
- [x] Establish playout intelligence (auto-segue rules, crossfade profiles, energy ramps) - see `radio_automation.py`.
- [ ] Identify remote control + monitoring features (web dashboard, mobile, alerts, failover).
- [x] Define third-party integrations (AzuraCast, ElevenLabs, RadioDJ) - implemented in `radio_automation.py`.


## Phase 1: The Librarian (Asset Management)
- [x] Infrastructure (Docker/Icecast)
- [x] The Deck (Liquidsoap Configuration)
- [x] The Librarian (Lyria Client + Music Library)

## Phase 2: The Host (Ralph Wiggum)
- [x] Implement Ralph Agent ("I'm a unit test!")
- [x] Connect Real Weather API (Rowville)

## Phase 3: The Score (Lyria RealTime)
- [x] Python OSC Emitter
- [x] TouchDesigner / Three.js Receiver
- [x] Lyria RealTime Scorer
- [x] The Deck (Liquidsoap Configuration)
- [ ] The Librarian (Music Scanner)
- [ ] Implement metadata normalization + loudness analysis.
- [ ] Add library de-dupe + content quality checks.

## Phase 4: The Visuals (Hallucination)
- [ ] Python OSC Emitter
- [ ] TouchDesigner / Three.js Receiver
- [ ] Define OSC event schema (now playing, mood, intensity, alerts).
- [ ] Implement real-time overlays (now playing, headlines, alerts).

## Phase 4: Orchestration & Scheduling
- [ ] Implement station clock engine (hourly templates, rotations, sweepers).
- [ ] Build daypart profiles (morning, midday, drive, late).
- [ ] Add region/timezone aware scheduling (daypart rules per market).
- [ ] Add rules engine (artist separation, repeats, energy curves, tempo).
- [ ] Implement dynamic playlist generation (AI-aware segment insertion).
- [ ] Add failover handling for missing assets and empty queues.

## Phase 5: Content Pipelines (Music, Talk, News, Ads)
- [ ] Music ingest pipeline (tags, genre, mood, energy, explicit flags).
- [ ] Talk segment templates (monologues, interviews, promos).
- [ ] Guest persona library (voice, background, opinions, topics).
- [ ] News ingestion (RSS/APIs) with scheduling blocks.
- [ ] Ad inventory model (flights, geo/targeting, frequency caps).
- [ ] Locale-specific ad targeting and content filters.
- [ ] Multi-language persona/voice profiles with localized script templates.
- [ ] Proof-of-play logging for ads and promos.
- [ ] Exportable royalty reports (track plays, timestamps, territory).
- [ ] Integration hooks for rights organizations or CSV output templates.
- [ ] Validation for missing/incorrect metadata fields.

## Phase 6: Playout & Rendering
- [ ] TTS rendering pipeline (per-persona voices, caching, retries).
- [ ] Audio mastering chain (EQ, compression, loudness normalization).
- [ ] Bed music + SFX mixing for talk segments.
- [ ] Crossfade + auto-segue profiles per daypart.
- [ ] Live-assist overrides with hotkeys + safety ducking.

## Phase 7: Monitoring, QA, & Compliance
- [ ] Stream health checks (silence, clipping, disconnects).
- [ ] Content QA gate (profanity, banned phrases, length, topic blocks).
- [ ] Centralized secrets vault for API keys.
- [ ] Key rotation policy and automated renewal for third-party services.
- [ ] Audit logs for secret access.
- [ ] Audit logs + retention policy controls.
- [ ] DMCA/rights takedown workflow (intake, verification, removal, audit trail).
- [ ] Retention policy controls for audio logs + user data (configurable TTLs).
- [ ] Consent + privacy controls for user-submitted content (upload approvals, revocation).
- [ ] Alerting (Slack/Email/SMS) and incident runbooks.
- [ ] Analytics dashboard (listener minutes, tune-outs, top tracks).
- [ ] Experiment flags for segment templates, host styles, and rotation rules.
- [ ] Split audiences into cohorts and measure tune-out rates.
- [ ] Automated rollout/rollback based on KPIs.

## Phase 8: Admin & Studio UI
- [ ] Authentication + role-based access control.
- [ ] Library management UI (search, edit, duplicates, batch actions).
- [ ] Scheduling UI (clock builder, rotations, daypart rules).
- [ ] Playout dashboard (now playing, upcoming, logs).
- [ ] Host console (carts, hotkeys, voice tracking).
- [ ] Review queue for AI scripts/segments before playout.
- [ ] “Approve/Reject/Edit” workflow with version history.
- [ ] Emergency kill-switch for specific personas or content types.
