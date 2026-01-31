# Competitor feature matrix

> **Source**: Feature list derived from the NextKast Internet Radio Automation User Manual v1.1. See `docs/competitors/nextkast.md` for links.

| Feature name | Source product (NextKast/RoboDJ) | Notes/constraints | Neon Frequency status (missing/partial/existing) | Target subsystem (Scheduler/Playout/Library/Voice/Analytics/UI) |
| --- | --- | --- | --- | --- |
| Category + rotation based scheduling | NextKast | Categories and rotations drive playlist generation. | Existing | Scheduler/Library |
| Automated playlist generation + playback | NextKast | Builds playlists from rotations and plays them in automation. | Existing | Scheduler/Playout |
| Track metadata + intro/outro markers | NextKast | Manual includes markers for sweepers + intro/outro/next-start. | Partial (intro/outro durations exist; no explicit next-start marker) | Library/Playout |
| Sweeper overlay + ID insertion | NextKast | Manual references sweepers and overlays. | Partial (sweepers modeled; overlay behavior not explicit) | Playout/Scheduler |
| Manual / Live Assist / Automated modes | NextKast | Explicit modes for operator control. | Existing | Playout/UI |
| Sound FX / hot buttons | NextKast | Hot buttons for instant carts. | Existing | Live Assist/UI |
| Voice tracking workflow | NextKast | Voice track recording + insertion. | Existing | Voice/Scheduler |
| Simulcast another stream | NextKast | Relay another stream inside playout. | Missing | Playout |
| Mic + line input | NextKast | Live input sources for talk breaks. | Partial (live mic mixing documented, no explicit line input handling) | Playout |
| External DSP (Stereo Tool/Breakaway) | NextKast | Winamp DSP support for processing chain. | Missing | Playout/Engineering |
| Remote voice tracking management | NextKast | Remote contribution workflow. | Missing | Voice/Workflow |
| Skype/VOIP call handling | NextKast | Live call integration. | Missing | Live Assist/Playout |
| Shortcut keys (main + voice tracking) | NextKast | Keyboard shortcuts for ops. | Partial (UI shortcuts defined, voice tracking shortcuts not specified) | UI |
| Backup + restore utility | NextKast | Built-in backup/restore. | Missing | Ops/Infrastructure |

## Enhancement backlog (from gaps)
- Playout: simulcast relay input, external DSP chain configuration, and explicit sweeper overlay rules.
- Voice: remote voice-tracking review/approval workflows and voice-tracking keyboard shortcuts.
- Live Assist: VOIP call intake and line-input routing support.
- Ops: backup/restore tooling for schedules, library, and configuration snapshots.
