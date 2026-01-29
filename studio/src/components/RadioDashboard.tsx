import type { ReactNode } from 'react';

const agents = [
    {
        name: 'Nova Vale',
        role: 'Primary Host',
        voice: 'Warm Alto / Velvet',
        persona: 'Curious, precise, cinematic',
        status: 'Live',
        accent: 'cyan',
    },
    {
        name: 'Axel Rift',
        role: 'Interview Agent',
        voice: 'Midrange / Crisp',
        persona: 'Playful, fearless, fast',
        status: 'Standby',
        accent: 'emerald',
    },
    {
        name: 'Echo Grey',
        role: 'News & Culture',
        voice: 'Neutral / Clear',
        persona: 'Measured, insightful',
        status: 'Queued',
        accent: 'violet',
    },
    {
        name: 'Lyra Flux',
        role: 'After Hours',
        voice: 'Husky / Noir',
        persona: 'Unhinged, poetic',
        status: 'Ready',
        accent: 'fuchsia',
    },
];

const interviewQueue = [
    {
        time: '19:45',
        topic: 'Synthwave renaissance & underground labels',
        mode: 'Professional',
        host: 'Nova Vale',
        guests: ['Label Founder', 'Touring Artist'],
    },
    {
        time: '20:30',
        topic: 'AI vocals: ethics, craft, and future radio',
        mode: 'Fun',
        host: 'Axel Rift',
        guests: ['Vocal Engineer', 'Community Curator'],
    },
    {
        time: '22:00',
        topic: 'Midnight confessions: listener call-ins',
        mode: 'Adult',
        host: 'Lyra Flux',
        guests: ['Live Callers'],
    },
];

const automationRules = [
    {
        label: 'Auto-Interview Generator',
        detail: 'Slots fill with trending topics + guest synth models.',
        status: 'Active',
    },
    {
        label: 'Content Safety Mesh',
        detail: 'Realtime tone analysis, profanity routing, compliance logging.',
        status: 'Active',
    },
    {
        label: 'Smart Segue Engine',
        detail: 'BPM + sentiment-matched transitions, ad-lib intros.',
        status: 'Learning',
    },
];

const contentModes = [
    { name: 'Professional', detail: 'Journalistic, crisp delivery.' },
    { name: 'Fun', detail: 'Playful, energetic banter.' },
    { name: 'Adult', detail: 'Late-night intimacy filters.' },
    { name: 'Unhinged', detail: 'Chaotic, experimental sparks.' },
];

const voicePresets = [
    {
        name: 'Glasswave',
        tone: 'Bright, airy',
        personality: 'Dreamy strategist',
    },
    {
        name: 'Velvet Noir',
        tone: 'Low, intimate',
        personality: 'Storyteller',
    },
    {
        name: 'Pulse Crisp',
        tone: 'Tight, punchy',
        personality: 'Hype conductor',
    },
];

const multiVoiceSelections = [
    {
        slot: 'Voice A',
        name: 'Nova Vale',
        role: 'Primary Host',
        tone: 'Warm Alto / Velvet',
        accent: 'cyan',
    },
    {
        slot: 'Voice B',
        name: 'Axel Rift',
        role: 'Interview Agent',
        tone: 'Midrange / Crisp',
        accent: 'emerald',
    },
];

const scriptModes = [
    {
        name: 'Banter',
        detail: 'Rapid-fire setup, punchlines, and playful callouts.',
        status: 'Pinned',
    },
    {
        name: 'Interview',
        detail: 'Guided Q&A with structured voice handoffs.',
        status: 'Ready',
    },
    {
        name: 'Dual-Announce',
        detail: 'Co-hosted announcements and synchronized reads.',
        status: 'Draft',
    },
];

const timelinePreview = [
    {
        time: '00:00',
        segment: 'Cold open + audience tease',
        speaker: 'Nova Vale',
        length: '00:45',
        accent: 'cyan',
    },
    {
        time: '00:45',
        segment: 'Topic primer + hype cues',
        speaker: 'Axel Rift',
        length: '01:10',
        accent: 'emerald',
    },
    {
        time: '01:55',
        segment: 'Dual-announce sponsor tag',
        speaker: 'Nova + Axel',
        length: '00:30',
        accent: 'violet',
    },
    {
        time: '02:25',
        segment: 'Listener voicemail + follow-up',
        speaker: 'Nova Vale',
        length: '01:05',
        accent: 'cyan',
    },
];

const accentStyles: Record<string, string> = {
    cyan: 'from-cyan-400/20 to-cyan-500/5 border-cyan-400/30',
    emerald: 'from-emerald-400/20 to-emerald-500/5 border-emerald-400/30',
    violet: 'from-violet-400/20 to-violet-500/5 border-violet-400/30',
    fuchsia: 'from-fuchsia-400/20 to-fuchsia-500/5 border-fuchsia-400/30',
};

const accentDots: Record<string, string> = {
    cyan: 'bg-cyan-400',
    emerald: 'bg-emerald-400',
    violet: 'bg-violet-400',
    fuchsia: 'bg-fuchsia-400',
};

const StatusBadge = ({ label }: { label: string }) => {
    const palette = {
        Live: 'bg-emerald-500/20 text-emerald-200 border-emerald-400/40',
        Standby: 'bg-cyan-500/20 text-cyan-200 border-cyan-400/40',
        Queued: 'bg-violet-500/20 text-violet-200 border-violet-400/40',
        Ready: 'bg-fuchsia-500/20 text-fuchsia-200 border-fuchsia-400/40',
    };

    return (
        <span
            className={`px-2 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] border rounded-full ${
                palette[label as keyof typeof palette] ?? 'bg-white/10 text-white/60 border-white/10'
            }`}
        >
            {label}
        </span>
    );
};

const Panel = ({ title, subtitle, children }: { title: string; subtitle?: string; children: ReactNode }) => (
    <section className="rounded-2xl border border-white/10 bg-zinc-950/70 backdrop-blur-xl p-6 shadow-[0_0_30px_rgba(0,0,0,0.35)]">
        <div className="flex items-start justify-between gap-4 mb-4">
            <div>
                <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
                {subtitle && <p className="text-xs text-zinc-400 mt-1">{subtitle}</p>}
            </div>
        </div>
        {children}
    </section>
);

const RadioDashboard = () => {
    return (
        <div className="flex flex-col h-full pointer-events-auto">
            <header className="h-16 flex items-center justify-between px-6 border-b border-white/10 bg-zinc-950/80 backdrop-blur-md">
                <div>
                    <p className="text-xs uppercase tracking-[0.4em] text-cyan-400">Neon Frequency</p>
                    <h1 className="text-xl font-semibold tracking-tight">AI Radio DJ Control Room</h1>
                </div>
                <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5">
                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                        <span className="text-xs text-zinc-300">On Air · 128 BPM</span>
                    </div>
                    <button className="px-4 py-2 rounded-full bg-white text-black text-xs font-semibold tracking-[0.2em] uppercase">
                        Go Live
                    </button>
                </div>
            </header>

            <div className="flex-1 grid grid-cols-[260px_minmax(0,1fr)_360px] gap-6 p-6 overflow-hidden">
                <aside className="flex flex-col gap-6 overflow-y-auto pr-1">
                    <Panel title="Automation Core" subtitle="Fully autonomous orchestration stack.">
                        <div className="space-y-4">
                            {automationRules.map((rule) => (
                                <div key={rule.label} className="border border-white/10 rounded-xl p-3 bg-white/5">
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm font-semibold">{rule.label}</p>
                                        <span className="text-[11px] text-emerald-200 bg-emerald-500/20 px-2 py-1 rounded-full border border-emerald-400/30">
                                            {rule.status}
                                        </span>
                                    </div>
                                    <p className="text-xs text-zinc-400 mt-2 leading-relaxed">{rule.detail}</p>
                                </div>
                            ))}
                        </div>
                    </Panel>

                    <Panel title="Tone Modes" subtitle="Set the broadcast personality instantly.">
                        <div className="space-y-3">
                            {contentModes.map((mode) => (
                                <div key={mode.name} className="flex items-start gap-3 border border-white/10 rounded-xl p-3">
                                    <div className="h-2 w-2 rounded-full bg-cyan-400 mt-2" />
                                    <div>
                                        <p className="text-sm font-semibold">{mode.name}</p>
                                        <p className="text-xs text-zinc-400">{mode.detail}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </Panel>
                </aside>

                <main className="flex flex-col gap-6 overflow-y-auto pr-1">
                    <Panel title="Live Flow" subtitle="Music, interviews, and ad-libs stitched into one timeline.">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="rounded-xl border border-white/10 p-4 bg-gradient-to-br from-white/10 to-transparent">
                                <p className="text-xs uppercase tracking-[0.3em] text-zinc-400">Now Playing</p>
                                <h3 className="text-xl font-semibold mt-2">Neon Drift · Arcadia</h3>
                                <p className="text-xs text-zinc-400 mt-2">Energy: 92 · Mood: Euphoric</p>
                                <div className="mt-4 flex items-center gap-2">
                                    <span className="text-[11px] px-2 py-1 rounded-full border border-white/10 text-zinc-300">
                                        Auto-Segue: Enabled
                                    </span>
                                    <span className="text-[11px] px-2 py-1 rounded-full border border-white/10 text-zinc-300">
                                        03:12 remaining
                                    </span>
                                </div>
                            </div>
                            <div className="rounded-xl border border-white/10 p-4 bg-gradient-to-br from-cyan-500/10 to-transparent">
                                <p className="text-xs uppercase tracking-[0.3em] text-zinc-400">Up Next</p>
                                <ul className="mt-3 space-y-2 text-sm">
                                    <li className="flex items-center justify-between text-zinc-200">
                                        <span>Echo Avenue · Lumen</span>
                                        <span className="text-xs text-zinc-400">04:28</span>
                                    </li>
                                    <li className="flex items-center justify-between text-zinc-200">
                                        <span>Interview: Synthwave Renaissance</span>
                                        <span className="text-xs text-zinc-400">06:00</span>
                                    </li>
                                    <li className="flex items-center justify-between text-zinc-200">
                                        <span>Solar Bloom · Neon Tide</span>
                                        <span className="text-xs text-zinc-400">03:40</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </Panel>

                    <Panel title="Interview Scheduler" subtitle="Assign hosts, topics, and tones or let agents auto-fill.">
                        <div className="space-y-4">
                            {interviewQueue.map((slot) => (
                                <div
                                    key={`${slot.time}-${slot.topic}`}
                                    className="flex items-start justify-between gap-4 border border-white/10 rounded-xl p-4 bg-white/5"
                                >
                                    <div>
                                        <p className="text-xs uppercase tracking-[0.3em] text-zinc-400">{slot.time}</p>
                                        <h3 className="text-base font-semibold mt-1">{slot.topic}</h3>
                                        <p className="text-xs text-zinc-400 mt-2">
                                            Host: {slot.host} · Guests: {slot.guests.join(', ')}
                                        </p>
                                    </div>
                                    <StatusBadge label={slot.mode} />
                                </div>
                            ))}
                        </div>
                        <div className="mt-5 flex flex-wrap gap-3 text-xs text-zinc-400">
                            <span className="px-3 py-2 border border-white/10 rounded-full">Auto-fill open slots</span>
                            <span className="px-3 py-2 border border-white/10 rounded-full">Lock host personas</span>
                            <span className="px-3 py-2 border border-white/10 rounded-full">Adaptive topic radar</span>
                        </div>
                    </Panel>

                    <Panel
                        title="Multi-Voice Scripts"
                        subtitle="Select two voices, set a script mode, and preview the handoff timeline."
                    >
                        <div className="grid gap-4 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,0.9fr)]">
                            <div className="space-y-4">
                                <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                                    <p className="text-xs uppercase tracking-[0.3em] text-zinc-400">Voice pairing</p>
                                    <div className="mt-3 grid gap-3 sm:grid-cols-2">
                                        {multiVoiceSelections.map((voice) => (
                                            <div
                                                key={voice.slot}
                                                className={`rounded-xl border bg-gradient-to-br p-3 ${accentStyles[voice.accent]}`}
                                            >
                                                <p className="text-[11px] uppercase tracking-[0.3em] text-zinc-300">
                                                    {voice.slot}
                                                </p>
                                                <p className="text-sm font-semibold mt-2">{voice.name}</p>
                                                <p className="text-xs text-zinc-300">{voice.role}</p>
                                                <p className="text-xs text-zinc-400 mt-2">{voice.tone}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                                    <p className="text-xs uppercase tracking-[0.3em] text-zinc-400">Script mode</p>
                                    <div className="mt-3 space-y-3">
                                        {scriptModes.map((mode) => (
                                            <div
                                                key={mode.name}
                                                className="flex items-start justify-between gap-4 rounded-xl border border-white/10 bg-zinc-950/70 p-3"
                                            >
                                                <div>
                                                    <p className="text-sm font-semibold">{mode.name}</p>
                                                    <p className="text-xs text-zinc-400 mt-1">{mode.detail}</p>
                                                </div>
                                                <span className="text-[11px] uppercase tracking-[0.3em] text-cyan-200 border border-cyan-400/40 px-2 py-1 rounded-full">
                                                    {mode.status}
                                                </span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                                <div className="flex items-center justify-between">
                                    <p className="text-xs uppercase tracking-[0.3em] text-zinc-400">Timeline preview</p>
                                    <span className="text-[11px] uppercase tracking-[0.3em] text-zinc-300">
                                        3:30 total
                                    </span>
                                </div>
                                <div className="mt-4 space-y-3">
                                    {timelinePreview.map((entry) => (
                                        <div
                                            key={`${entry.time}-${entry.segment}`}
                                            className="flex items-start gap-3 rounded-xl border border-white/10 bg-zinc-950/70 p-3"
                                        >
                                            <div className="mt-1 flex flex-col items-center">
                                                <span
                                                    className={`h-2.5 w-2.5 rounded-full ${
                                                        accentDots[entry.accent] ?? 'bg-white/50'
                                                    }`}
                                                />
                                                <span className="mt-2 text-[11px] text-zinc-400">{entry.time}</span>
                                            </div>
                                            <div className="flex-1">
                                                <p className="text-sm font-semibold">{entry.segment}</p>
                                                <p className="text-xs text-zinc-400 mt-1">
                                                    {entry.speaker} · {entry.length}
                                                </p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                                <div className="mt-4 flex flex-wrap gap-2 text-[11px] text-zinc-400">
                                    <span className="px-3 py-2 border border-white/10 rounded-full">
                                        Generate alt takes
                                    </span>
                                    <span className="px-3 py-2 border border-white/10 rounded-full">
                                        Sync with cues
                                    </span>
                                    <span className="px-3 py-2 border border-white/10 rounded-full">
                                        Export rundown
                                    </span>
                                </div>
                            </div>
                        </div>
                    </Panel>
                </main>

                <aside className="flex flex-col gap-6 overflow-y-auto pr-1">
                    <Panel title="Agent Voices" subtitle="Consistent personalities across every show.">
                        <div className="space-y-4">
                            {agents.map((agent) => (
                                <div
                                    key={agent.name}
                                    className={`rounded-xl border bg-gradient-to-br p-4 ${accentStyles[agent.accent]}`}
                                >
                                    <div className="flex items-start justify-between">
                                        <div>
                                            <h3 className="text-base font-semibold">{agent.name}</h3>
                                            <p className="text-xs text-zinc-300">{agent.role}</p>
                                        </div>
                                        <StatusBadge label={agent.status} />
                                    </div>
                                    <p className="text-xs text-zinc-200 mt-3">
                                        Voice: <span className="text-white">{agent.voice}</span>
                                    </p>
                                    <p className="text-xs text-zinc-400 mt-1">{agent.persona}</p>
                                </div>
                            ))}
                        </div>
                    </Panel>

                    <Panel title="Voice Design Lab" subtitle="Preset library for every station and mood.">
                        <div className="space-y-3">
                            {voicePresets.map((preset) => (
                                <div key={preset.name} className="border border-white/10 rounded-xl p-3 bg-white/5">
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm font-semibold">{preset.name}</p>
                                        <span className="text-[11px] uppercase tracking-[0.3em] text-cyan-300">Preset</span>
                                    </div>
                                    <p className="text-xs text-zinc-400 mt-2">
                                        Tone: {preset.tone} · Persona: {preset.personality}
                                    </p>
                                </div>
                            ))}
                        </div>
                        <button className="w-full mt-4 px-4 py-2 rounded-full border border-cyan-400/40 text-cyan-200 text-xs uppercase tracking-[0.3em]">
                            Create New Voice
                        </button>
                    </Panel>
                </aside>
            </div>
        </div>
    );
};

export default RadioDashboard;
