# Voice Domain

## Voice Profile Schema

Define voice profiles as structured documents that can be validated by JSON Schema or typed configs.

```yaml
voice_profile:
  id: voice_profile_id
  persona:
    name: "Ava"
    description: "Confident, warm, concise product guide"
    target_audience: ["new users", "power users"]
    banned_traits: ["condescending", "overly verbose"]
  voice_model:
    provider: "acme-tts"
    model: "aurora-v2"
    locale: "en-US"
    gender_presentation: "neutral" # optional
    prosody:
      pitch: "medium"
      rate: "medium"
      energy: "moderate"
  tone_constraints:
    speaking_style:
      - "clear"
      - "empathetic"
      - "direct"
    forbidden:
      - "sarcasm"
      - "mocking"
    compliance:
      max_sentence_length: 24
      hedging_allowed: false
```

**Schema expectations**
- **persona** captures the brand-facing identity and boundaries for the voice.
- **voice_model** defines the TTS provider, model, and acoustic characteristics.
- **tone_constraints** captures allowed stylistic language and explicit disallow lists.

## Mode Switching

Mode switching is a runtime overlay on the base voice profile. Each mode should be a well-defined delta that affects tone and safety behavior without changing the core persona identity.

| Mode | Intent | Tone Adjustments | Hard Limits |
| --- | --- | --- | --- |
| professional | Efficient, factual, reliable | Short sentences, low affect, precise wording | No jokes, no slang, no speculation |
| fun | Friendly, energetic, playful | Light humor, warmer wording, more expressive interjections | Avoid sarcasm, avoid ridicule |
| adult | Mature, candid, still respectful | Direct, minimal euphemisms, measured warmth | No explicit sexual content, no coercive language |
| unhinged | Hyper-energetic, chaotic flavor | Fast cadence, unusual metaphors, playful unpredictability | Never violates safety boundaries, no threats, no harassment |

Implementation notes:
- Modes should be mapped to a deterministic set of tone changes (e.g., prompt snippets or prosody overrides).
- Do not allow mode switching to bypass persona or safety constraints.
- Log mode changes for observability, including the previous and next mode.

## Safety Policy Boundaries

Safety boundaries are enforced by capability toggles that configure both generation and playback rules.

**Common toggles**
- `allow_profanity`: Enables mild profanity in generated text and spoken output.
- `allow_slang`: Allows informal slang and regional idioms.
- `allow_sensitive_topics`: Allows discussion of sensitive topics with neutral phrasing.
- `allow_age_restricted`: Allows adult themes without explicit sexual content.
- `allow_violent_language`: Allows non-graphic references to violence.

**Boundary rules**
- Even when toggles are enabled, disallowed content remains disallowed (e.g., hate speech, threats, explicit sexual content, self-harm instructions).
- When toggles are disabled, sanitize output and rephrase into safe, neutral language.
- Emit a moderation reason code when content is filtered or rewritten to keep auditability.

## TTS Provider Integration & Caching

**Integration points**
1. **Text normalization**: Expand acronyms, clean markup, and inject SSML tags if supported.
2. **Voice selection**: Match `voice_profile.voice_model` to the provider's voice catalog.
3. **Synthesis request**: Include mode overlays and tone constraints in metadata.
4. **Post-processing**: Apply loudness normalization and trim silences if needed.

**Caching strategy**
- Cache on a deterministic hash of `(normalized_text + voice_profile_id + mode + locale + provider_model_version)`.
- Store metadata alongside audio (timestamps, model version, safety toggles applied).
- Invalidate cache entries when:
  - The voice model version changes.
  - The voice profile constraints change.
  - Safety policy toggles change.
- Use tiered caching: in-memory for hot phrases, object storage for long-lived audio.
- Deduplicate identical requests across sessions to reduce provider costs.
