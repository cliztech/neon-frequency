# Full-Stack Architecture

## Backend services
- **Scheduler**: Builds hourly and daily clocks, applies rules (rotation, spacing, compliance), and emits a finalized playlist with timings.
- **Playout orchestration**: Owns the real-time playout timeline, crossfades, and failover; consumes the scheduler output and runtime triggers.
- **Agent runtime**: Hosts LLM-driven or rules-based agents that generate spoken segments, promos, or dynamic content.
- **Logging & compliance**: Captures immutable playout logs, operator actions, and compliance records for audits and reporting.
- **Metadata ingestion**: Normalizes track/asset metadata from labels, catalogs, or internal producers and enriches it for discovery.

## APIs & event bus
- **REST**: CRUD for playlists, assets, schedules, and admin settings.
- **GraphQL**: Aggregated reads for studio UI and dashboards (e.g., “show me the current hour + metadata + usage rights”).
- **WebSocket**: Low-latency updates for “now playing,” live logs, and playout state changes.
- **Event bus (NATS or Kafka)**: Streams playout events, ingestion updates, scheduler outputs, and agent runtime results to decouple services.

## Storage
- **Postgres**: Source of truth for schedules, logs, compliance data, and operational metadata.
- **Object storage (S3-compatible)**: Audio masters, stems, waveforms, and generated voice segments.
- **Vector database**: Content discovery, similarity search, and semantic tagging for programming assistance.

## Observability
- **Structured logs**: JSON logs with correlation IDs (show, hour, asset, and playout event IDs).
- **Metrics**: Service KPIs (latency, queue depth, delivery time) and playout health.
- **Tracing**: Distributed traces across scheduler → orchestration → agent runtime → playout.

## Frontend
- **Studio UI**: React + Tailwind for operator workflows, with Three.js for realtime visualizers.
- **Design system**: Tokens for color/typography, reusable components (buttons, panels, data tables, timeline), and accessibility baselines.

## External integrations
- **Icecast/Liquidsoap**: Streaming and playout control.
- **Voice TTS providers**: Multilingual voices for intros, outros, and dynamic segments.
- **Ad servers**: Ad decisioning, insertion, and reporting.

## Core “hour of broadcast” flow
1. **Scheduler** produces the hour clock and emits a playlist with timings.
2. **Playout orchestration** pulls audio from object storage and validates metadata/compliance.
3. **Agent runtime** generates dynamic segments (voice, promos, bumpers) and stores outputs.
4. **Orchestration** sequences audio, handles crossfades, and triggers Icecast/Liquidsoap.
5. **Event bus** broadcasts now-playing, transitions, and errors to APIs and WebSocket clients.
6. **Logging/compliance** writes immutable logs to Postgres and long-term archives.
7. **Studio UI** receives live updates and displays the current hour timeline.
