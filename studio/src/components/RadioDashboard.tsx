import type { ReactNode } from 'react';

import PronunciationSafetyPanel from './PronunciationSafetyPanel';

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

const v2FeatureHighlights = [
    {
        title: 'Dual Marker Mode',
        detail: 'Back-announce and front-announce songs in a single automated pass.',
    },
    {
        title: 'Music Beds',
        detail: 'Layer news, weather, or custom beds under every voice track.',
    },
    {
        title: 'Multi-Voice Scripts',
        detail: 'Generate morning-show style banter with two distinct AI voices.',
    },
    {
        title: 'Smart Scheduler',
        detail: 'Scan playlists for markers and auto-build breaks in seconds.',
    },
    {
        title: 'Banned Phrase + Pronunciation',
        detail: 'Teach the system exactly how to say names and what to avoid.',
    },
    {
        title: 'Dynamic Prompt Variables',
        detail: 'Insert time of day, custom tags, and live station text on the fly.',
    },
    {
        title: 'Prompt & Promo Library',
        detail: 'Organized scripting, promos, and custom templates in one hub.',
    },
    {
        title: 'Custom Scripts',
        detail: 'Write it your way while RoboDJ handles delivery and pacing.',
    },
    {
        title: 'Expanded AI Voices',
        detail: 'Mix up to 16 voices across ElevenLabs and Gemini.',
    },
];

const coreCapabilities = [
    {
        title: 'Playlist-Aware Voice Tracks',
        detail: 'Generate contextual breaks based on the songs you are playing now.',
    },
    {
        title: 'Automated Scripts + Segments',
        detail: 'Prompt-powered trivia, song stories, promos, and weather in 30+ languages.',
    },
    {
        title: 'Hands-Free Scheduling',
        detail: 'Let the system build breaks automatically or jump in to edit instantly.',
    },
    {
        title: 'Broadcast-Ready Processing',
        detail: 'Built-in processing delivers loud, clear voice tracks without engineering.',
    },
    {
        title: 'Realtime Weather Reports',
        detail: 'Instant local forecasts via National Weather Service or Weather API.',
    },
];

const benefitPillars = [
    {
        title: 'Content that Connects',
        items: [
            'AI voice tracks that match your playlist',
            'Artist trivia, song stories, and station promos',
            'Dual marker announcing for real DJ flow',
            'Music beds built in for every segment',
        ],
    },
    {
        title: 'Control without Chaos',
        items: [
            'Smart scheduler builds breaks automatically',
            'Hands-on edits or full automation on demand',
            'Silence remover for natural pacing',
            'Organized file saving with custom naming',
        ],
    },
    {
        title: 'Customization that Matters',
        items: [
            'Up to 20 voices across multiple AI providers',
            'Banned phrase + pronunciation guardrails',
            'Dynamic prompt variables for time and tags',
            'Fully custom scripts written by your team',
        ],
    },
];

const integrationOptions = [
    'RadioDJ',
    'StationPlaylist',
    'SAM Broadcaster',
    'mAirList',
    'PlayIt Live',
    'Radio Boss',
    'NextKast',
    'Raduga',
    'Playlist files (.pls, .alb, .m3u)',
];

const accentStyles: Record<string, string> = {
    cyan: 'from-cyan-400/20 to-cyan-500/5 border-cyan-400/30',
    emerald: 'from-emerald-400/20 to-emerald-500/5 border-emerald-400/30',
    violet: 'from-violet-400/20 to-violet-500/5 border-violet-400/30',
    fuchsia: 'from-fuchsia-400/20 to-fuchsia-500/5 border-fuchsia-400/30',
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
                    <h1 className="text-xl font-semibold tracking-tight">RoboDJ V2 Automation Suite</h1>
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
                    <Panel title="RoboDJ V2 Feature Pack" subtitle="Everything new in the Deluxe automation stack.">
                        <div className="grid grid-cols-2 gap-4">
                            {v2FeatureHighlights.map((feature) => (
                                <div
                                    key={feature.title}
                                    className="rounded-xl border border-white/10 p-4 bg-gradient-to-br from-white/10 to-transparent"
                                >
                                    <h3 className="text-sm font-semibold text-white">{feature.title}</h3>
                                    <p className="text-xs text-zinc-400 mt-2 leading-relaxed">{feature.detail}</p>
                                </div>
                            ))}
                        </div>
                    </Panel>

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

                    <Panel title="AI Voice Track Engine" subtitle="Your playlist, now with personality.">
                        <div className="grid grid-cols-2 gap-4">
                            {coreCapabilities.map((capability) => (
                                <div key={capability.title} className="rounded-xl border border-white/10 p-4 bg-white/5">
                                    <p className="text-xs uppercase tracking-[0.3em] text-zinc-400">{capability.title}</p>
                                    <p className="text-sm text-white mt-2 leading-relaxed">{capability.detail}</p>
                                </div>
                            ))}
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

                    <Panel title="Benefits Dashboard" subtitle="Why broadcasters use RoboDJ instead of generic scripts.">
                        <div className="grid grid-cols-3 gap-4">
                            {benefitPillars.map((pillar) => (
                                <div key={pillar.title} className="rounded-xl border border-white/10 p-4 bg-white/5">
                                    <h3 className="text-sm font-semibold text-white">{pillar.title}</h3>
                                    <ul className="mt-3 space-y-2 text-xs text-zinc-300">
                                        {pillar.items.map((item) => (
                                            <li key={item} className="flex items-start gap-2">
                                                <span className="mt-1 h-1.5 w-1.5 rounded-full bg-cyan-400" />
                                                <span>{item}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            ))}
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

                    <PronunciationSafetyPanel />

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

                    <Panel title="Playout Integrations" subtitle="Built for small stations and major markets alike.">
                        <div className="flex flex-wrap gap-2">
                            {integrationOptions.map((integration) => (
                                <span
                                    key={integration}
                                    className="text-xs px-3 py-2 rounded-full border border-white/10 bg-white/5 text-zinc-200"
                                >
                                    {integration}
                                </span>
                            ))}
                        </div>
                        <p className="text-xs text-zinc-500 mt-4 leading-relaxed">
                            Playlist file support keeps RoboDJ compatible with custom automation stacks and legacy
                            workflows.
                        </p>
                    </Panel>
                </aside>
            </div>
        </div>
    );
};

export default RadioDashboard;
