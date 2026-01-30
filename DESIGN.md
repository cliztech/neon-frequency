# Neon Frequency: Design & UI/UX Verification

## 1. Competitive Analysis
We are positioning **Neon Frequency** against both utilitarian dashboards and vibe-based players.

| Competitor | Aesthetic | Strengths | Weaknesses | Our Edge |
| :--- | :--- | :--- | :--- | :--- |
| **AzuraCast (Public)** | Bootstrap/Clean | Functional, fast, responsive. | Boring, "Admin Panel" feel, no personality. | **Personality**: Our UI will feel *alive* with agent avatars. |
| **Poolside FM** | Retro Mac OS (1986) | Incredible vibe, distinct identity. | Niche aesthetic, clunky window management. | **Modernity**: We use sleek Glassmorphism vs. Retro pixel art. |
| **Lofi Girl** | Anime Loop | Cozy, distracting-free. | Passive experience, no interaction. | **Interactivity**: Users can chat/request with AEN & GREG. |
| **Monstercat** | Dark Mode/Sleek | Professional, focus on cover art. | sterile, feels like Spotify. | **Visuals**: WebGL React-based visualizers driven by real-time OSC. |

## 2. Visual Identity ("The Vibe")
**Theme:** *Cyberpunk Noir / Biopunk*
- **Primary Colors:** Neon Pink (`#FF00FF`), Cyan (`#00FFFF`), Deep Void Black (`#0b0b0b`).
- **Texture:** Glassmorphism (frosted blurs), Scanlines (CRT effects on GREG), Glitch artifacts.
- **Typography:**
    - Headers: `Orbitron` or `Rajdhani` (Tech/Futuristic).
    - Body: `Inter` or `Space Mono` (Readable/Terminal-like).

## 3. The "Look & Feel"
### The Player (Public Facing)
- **Hero Section:** Full-screen WebGL visualizer. It pulses to the `Energy` and `BPM` of the current track.
- **Agent Presence:**
    - **AEN:** A holographic waveform that speaks (text-to-speech visualization).
    - **GREG:** A glitchy, pixelated overlay that interrupts visually when he speaks.
- **Now Playing:** Large, bold typography. Cover art is secondary to the *motion*.
- **Chat:** A terminal-style chat box to "Communicate with the Station" (Triggering `!request`, `!greg`).

### The Control Room (Admin/Live Assist)
- **Layout:** "Spaceship Cockpit" vibe. High information density but grouped logically.
- **Crate:** Grid view of album art with "Energy" heatmaps.
- **Segues:** Visual representation of the crossfade (like DJ software wave-forms).

## 4. Technical Strategy (Frontend)
- **Framework:** Next.js 14 (App Router) + React.
- **Styling:** Tailwind CSS + Framer Motion (for buttery smooth transitions).
- **Visuals:** Three.js / React-Three-Fiber (R3F) for the background scenes.
- **State:** `Zustand` for local player state, `Socket.io` for real-time station updates.
