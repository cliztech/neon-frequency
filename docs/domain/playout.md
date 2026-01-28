# Playout rules

## Crossfade profiles, energy ramps, and segue rules

### Crossfade profiles
- **Tight talkback**: 0.4s fade-out / 0.2s fade-in. Used for live talkback beds or DJ drops where speech remains intelligible.
- **Standard music mix**: 1.8s fade-out / 1.8s fade-in. Default for most music-to-music transitions.
- **Long blend**: 4.0s fade-out / 4.0s fade-in. Used for ambient blocks or long-form programming where overlap is acceptable.
- **Hard cut**: 0s fade-out / 0s fade-in with a -9 dB pre-cut trim. Reserved for stingers and ID sweepers to keep impact.

### Energy ramps
- **Energy up**: Pre-roll the incoming track at -6 dB, ramp to 0 dB over 6–8s, while outgoing track ramps to -8 dB over the same window.
- **Energy down**: Pre-roll the incoming track at -10 dB, ramp to -3 dB over 4–6s while outgoing track ramps to -3 dB over 4–6s.
- **Neutral**: Symmetric overlap at -6 dB mid-point, equal fade time for both sources.

### Segue rules
- Segues are determined by segment metadata: `segue_class` and `energy_index`.
- Allowed combinations:
  - `music -> music`: Standard or long blend depending on combined `energy_index` delta.
  - `speech -> music`: Tight talkback or standard music mix if `energy_index` ≥ 60.
  - `music -> speech`: Tight talkback with speech pre-roll at -8 dB.
  - `sweeper -> music`: Hard cut to preserve the sweep.
- If metadata is missing, fall back to **standard music mix**.

## Ducking policy and voice-over priority
- Voice-over (VO) always has highest priority; it enforces a music duck of -12 dB for the full VO duration plus a 250ms tail.
- Live mic is treated like VO but with a softer duck of -9 dB to retain ambience.
- Promos and sweepers duck music by -6 dB, unless a VO is already active (VO wins).
- Priority order: `voice_over > live_mic > promo_sweeper > music_bed`.
- If two overlays conflict, only the highest priority overlay is audible; lower-priority overlays are suppressed.

## Failover logic
- **Silence detection**: If output drops below -45 dBFS for more than 1.5s, trigger a failover sequence.
- **Fallback playlist**: Switch to the curated fallback playlist (`playlist_fallback`) and crossfade with the **standard music mix**.
- **Recovery**: Once primary audio returns and stays above -35 dBFS for 3s, resume the scheduled log at the next safe segue point.
- **Alerting**: Emit a `playout_failover` event with the silence duration and current segment metadata.

## Backtiming and live assist overrides
- **Backtiming**: Automation computes a target exit time for every segment. If current program is running long, apply a 1.2x speed trim (max 6%) on the outgoing track and use a **tight talkback** to realign.
- **Live assist**: DJs can override any crossfade profile. Manual overrides persist until the next log break.
- **Hard backtime**: If the system is >15s behind at a legal ID breakpoint, it will drop the next non-mandatory element (typically a music track) and roll into the required element.

## Mapping rules into Liquidsoap (or equivalent)

### Crossfades
```liquidsoap
# Crossfade profiles
music_standard = crossfade(start_next = 1.8, fade_in = 1.8, fade_out = 1.8)
music_long = crossfade(start_next = 4.0, fade_in = 4.0, fade_out = 4.0)
talkback = crossfade(start_next = 0.2, fade_in = 0.2, fade_out = 0.4)

# Switch based on metadata
radio = switch(
  [({metadata["segue_class"] == "long"}, music_long),
   ({metadata["segue_class"] == "talk"}, talkback)],
  default = music_standard
)
```

### Ducking and priority
```liquidsoap
# Priority: VO > live mic > promo > music
vo = input.harbor("vo")
mic = input.harbor("live_mic")
promo = input.harbor("promo")
music = playlist("main")

# Duck music when overlays are active
music_ducked = ducking(
  overlay = vo,
  ratio = 12.0,
  attack = 0.05,
  release = 0.25,
  target = music
)

music_ducked = ducking(
  overlay = mic,
  ratio = 9.0,
  attack = 0.05,
  release = 0.25,
  target = music_ducked
)

music_ducked = ducking(
  overlay = promo,
  ratio = 6.0,
  attack = 0.05,
  release = 0.25,
  target = music_ducked
)

# Final mix, VO wins via fallback priority
radio = fallback(track_sensitive = false, [vo, mic, promo, music_ducked])
```

### Failover
```liquidsoap
# Silence detection and failover
silence = on_silence(duration = 1.5, threshold = -45.)
primary = input.http("primary")
fallback = playlist("playlist_fallback")

safe = fallback(track_sensitive = false, [primary, fallback])
radio = silence(safe)
```

### Backtiming and overrides
```liquidsoap
# Example: apply time-stretch when behind schedule
music_backtimed = stretch(max_ratio = 1.06, sync = true, music)

# Manual override switch
manual_override = input.harbor("assist")
radio = switch(
  [({metadata["manual_override"] == "true"}, manual_override)],
  default = music_backtimed
)
```
