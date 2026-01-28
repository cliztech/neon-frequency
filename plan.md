# Master Plan: Project "Neon Frequency"

## Phase 0: Competitive Feature Audit (Radio Automation)
- [x] Document feature parity vs NextKast + RoboDJ (source links, screenshots, capability notes).
- [x] Research 20+ radio automation tools (see implementation_plan.md in brain folder).
- [ ] Map station clock concepts (hours, dayparts, rotations, sweepers, IDs, ads) into Neon Frequency scheduling model.
- [ ] Define live-assist controls (manual override, hotkeys, instant cart, voice tracks, emergency override).
- [ ] Specify logging + compliance needs (playout logs, ad proof, metadata history, retention policy).
- [ ] Outline library management parity (metadata editor, duplicate detection, normalization, loudness).
- [x] Establish playout intelligence (auto-segue rules, crossfade profiles, energy ramps) - see `radio_automation.py`.
- [ ] Identify remote control + monitoring features (web dashboard, mobile, alerts, failover).
- [x] Define third-party integrations (AzuraCast, ElevenLabs, RadioDJ) - implemented in `radio_automation.py`.


## Phase 1: The Pulse (Core Audio)
- [x] Infrastructure (Docker/Icecast)
- [x] The Deck (Liquidsoap Configuration)
- [ ] The Librarian (Music Scanner)

## Phase 2: The Personality (Agent)
- [ ] Implement ElevenLabs API for Voice
- [ ] Connect Real Weather API (Rowville)
- [ ] Implement "Greg" Agent (Parody Hip Hop)
- [ ] Build interview producer agent (schedule, topic discovery, guest briefs, tone selection).
- [ ] Build voice director agent (persona consistency, voice presets, compliance rules).
- [ ] Build content safety agent (profanity routing, age gating, policy tagging).
- [ ] Build showrunner agent (segment pacing, ad breaks, tempo transitions).

## Phase 3: The Hallucination (Visuals)
- [ ] Python OSC Emitter
- [ ] TouchDesigner / Three.js Receiver
