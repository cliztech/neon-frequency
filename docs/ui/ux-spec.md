# UX Specification

## Screen list
- **Dashboard**: Executive overview of live status, KPIs, and alerts.
- **Scheduler**: Timeline and queue management for campaigns, shifts, and outbound tasks.
- **Agent Studio**: Configure agents, intents, prompts, tools, and testing sandboxes.
- **Voice Lab**: Audio assets, voice tuning, call scripts, and pronunciation controls.
- **Compliance Logs**: Audit trails, consent records, retention controls, and export tools.
- **Library**: Shared assets (scripts, FAQs, prompt snippets, templates, media).
- **Live Assist**: Real-time supervisor console for active calls and escalation handling.

## Core user flows
1. **Monitor operations**
   - Land on Dashboard.
   - Review status cards, alerts, and performance trends.
   - Drill into Scheduler or Live Assist when anomalies appear.
2. **Plan a campaign**
   - Open Scheduler and create a new schedule.
   - Select agent configuration from Agent Studio.
   - Attach scripts and assets from Library and Voice Lab.
   - Save and publish the schedule.
3. **Design or update an agent**
   - Enter Agent Studio and create/edit an agent profile.
   - Define intents, prompts, and tool permissions.
   - Run test conversations and validate outputs.
   - Publish updates to make them available in Scheduler.
4. **Tune voice experience**
   - Open Voice Lab to adjust voice model, tone, and pronunciations.
   - Preview audio with sample scripts.
   - Save versions and share with Library.
5. **Audit and compliance review**
   - Go to Compliance Logs to filter calls or conversations.
   - Review consent, scripts, and escalation events.
   - Export required records or flag issues.
6. **Live escalation**
   - Use Live Assist to monitor active calls.
   - Intervene with whisper, barge, or takeover actions.
   - Log resolutions back to Compliance Logs.

## Key components and states
### Global components
- **Primary navigation**: Persistent sidebar with screen icons, badges, and quick search.
- **Header bar**: Environment selector, alerts, profile menu, and help.
- **Action panel**: Contextual drawer for create/edit flows.

### Dashboard
- **Status cards**: Active calls, queued tasks, success rate, alerts.
- **Trend charts**: Daily/weekly performance, anomalies, and comparisons.
- **Alert feed**: Priority notifications and suggested actions.

### Scheduler
- **Timeline view**: Drag-and-drop scheduling with zoom controls.
- **Queue table**: Sortable list of upcoming tasks.
- **Publish workflow**: Draft vs. live indicators.

### Agent Studio
- **Agent list**: Search, filter, and version indicators.
- **Prompt builder**: Editable prompt sections with validation.
- **Test harness**: Simulated conversations and response review.

### Voice Lab
- **Voice selector**: Model list with preview.
- **Pronunciation editor**: Phonetic editor and glossary.
- **Audio preview**: Playback controls and waveform.

### Compliance Logs
- **Audit table**: Filterable logs with export actions.
- **Consent viewer**: Transcript and consent metadata.
- **Retention controls**: Policy and expiration settings.

### Library
- **Asset grid**: Card-based assets with tags.
- **Version history**: Change log and revert actions.
- **Share controls**: Permissions and usage tracking.

### Live Assist
- **Active session list**: Real-time call list with priority badges.
- **Intervention controls**: Whisper, barge, takeover, and note taking.
- **Transcript stream**: Live updates with highlight markers.

### States
- **Empty state**: Clear messaging, quick-start action, and sample data link.
- **Live state**: Real-time indicators, auto-refresh, and latency labels.
- **Failure state**: Error summary, retry actions, and support links.

## Accessibility and keyboard shortcuts
### Accessibility
- **Color contrast**: Meet WCAG AA for text and key UI elements.
- **Focus management**: Visible focus rings and logical tab order.
- **ARIA labeling**: Descriptive labels for controls and dynamic content.
- **Keyboard parity**: All actions available without a mouse.
- **Motion control**: Reduced motion option for animated components.
- **Screen reader support**: Announce status changes and alerts.

### Keyboard shortcuts
- **Global**
  - `?` = Open shortcuts/help modal.
  - `g d` = Go to Dashboard.
  - `g s` = Go to Scheduler.
  - `g a` = Go to Agent Studio.
  - `g v` = Go to Voice Lab.
  - `g c` = Go to Compliance Logs.
  - `g l` = Go to Library.
  - `g i` = Go to Live Assist.
  - `cmd/ctrl + k` = Open global search.
- **Scheduler**
  - `n` = New schedule item.
  - `p` = Publish schedule.
  - `[` / `]` = Zoom out/in timeline.
- **Agent Studio**
  - `n` = New agent.
  - `t` = Run test conversation.
- **Live Assist**
  - `w` = Whisper.
  - `b` = Barge.
  - `x` = Takeover.
