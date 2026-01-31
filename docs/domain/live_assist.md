# Live Assist controls

## Purpose
Live Assist is the human override layer that lets a DJ or operator take control of automation when needed. It supports quick cart firing, manual overrides, and emergency handling while still emitting events for logging and downstream automation.

## Override levels
- **FULL_AUTO**: Automation runs end-to-end; live assist inputs are ignored unless explicitly requested.
- **ASSISTED**: AI suggests transitions and carts, but a human must approve them.
- **MANUAL**: Human drives the show while automation provides recommendations.
- **EMERGENCY**: Emergency playout mode that prioritizes alert carts and dead-air recovery.

## Instant cart grid
Live Assist ships with a 12-slot cart grid (4x3) that can be bound to hotkeys.

**Default cart types**
- **Station IDs**: Main and short IDs for legal/top-of-hour compliance.
- **Jingles**: Quick branding stingers.
- **Sweepers**: Short transitions between songs or segments.
- **SFX**: Effects like airhorns or applause for moment-to-moment flavor.
- **Voice tracks**: Pre-recorded host breaks or timed promos for assisted shows.
- **Emergency**: Prebuilt alert or backup loop for outages.

**Cart behaviors**
- Each cart can enable ducking so that it lowers bed audio while the cart plays.
- Carts can be color-coded for quick scanning in a live UI.

## Live session workflow
1. **Start a session** with a host name and desired override level.
2. **Set override level** during the show as the operator’s role changes.
3. **Fire carts** for IDs, sweepers, or emergency alerts.
4. **End the session** to return automation to FULL_AUTO and log duration.

## Emergency behavior
- Silence detection is monitored over a configurable threshold (default: 10 seconds).
- On dead air, Live Assist escalates to **EMERGENCY** and fires the emergency cart.
- Operators can deactivate emergency mode to resume automation.

## Event hooks
Live Assist emits events for integration with logging and analytics pipelines:
- `override_changed`
- `session_started`
- `session_ended`
- `cart_fired`

Use these events to populate playout logs, proof-of-play records, and compliance audits.
