const bannedPhrases = [
    {
        phrase: 'Unfiltered call-in chaos',
        reason: 'Flags unsafe solicitation language',
        severity: 'High',
    },
    {
        phrase: 'All bets are off',
        reason: 'Suggests unmoderated content',
        severity: 'Medium',
    },
    {
        phrase: 'No rules tonight',
        reason: 'Conflicts with broadcast compliance',
        severity: 'Medium',
    },
];

const pronunciationOverrides = [
    {
        term: 'Neon Frequency',
        sayAs: 'Nee-on Free-kwen-see',
        phonetic: 'niːˌɒn ˈfriːkwənsi',
        locale: 'en-US',
    },
    {
        term: 'Axel Rift',
        sayAs: 'Ax-el Rift',
        phonetic: 'ˈæksəl rɪft',
        locale: 'en-GB',
    },
    {
        term: 'Synthwave',
        sayAs: 'Sinth-wayv',
        phonetic: 'ˈsɪnθweɪv',
        locale: 'en-US',
    },
];

const PronunciationSafetyPanel = () => {
    return (
        <section className="rounded-2xl border border-white/10 bg-zinc-950/70 backdrop-blur-xl p-6 shadow-[0_0_30px_rgba(0,0,0,0.35)]">
            <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                    <h2 className="text-lg font-semibold tracking-tight">Pronunciation &amp; Safety</h2>
                    <p className="text-xs text-zinc-400 mt-1">
                        Guardrails for on-air delivery and voice clarity.
                    </p>
                </div>
                <button className="px-3 py-2 rounded-full border border-cyan-400/40 text-cyan-200 text-[11px] uppercase tracking-[0.3em]">
                    Add Rule
                </button>
            </div>

            <div className="space-y-5">
                <div>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold">Banned Phrases</h3>
                        <span className="text-[11px] text-zinc-400">3 active</span>
                    </div>
                    <div className="space-y-3">
                        {bannedPhrases.map((item) => (
                            <div key={item.phrase} className="rounded-xl border border-white/10 bg-white/5 p-3">
                                <div className="flex items-start justify-between gap-3">
                                    <div>
                                        <p className="text-sm font-semibold">“{item.phrase}”</p>
                                        <p className="text-xs text-zinc-400 mt-1">{item.reason}</p>
                                    </div>
                                    <span className="text-[11px] px-2 py-1 rounded-full border border-rose-400/40 text-rose-200 bg-rose-500/20">
                                        {item.severity}
                                    </span>
                                </div>
                                <div className="mt-3 flex flex-wrap gap-2 text-[11px] text-zinc-300">
                                    <button className="px-2 py-1 rounded-full border border-white/10">Edit</button>
                                    <button className="px-2 py-1 rounded-full border border-white/10">Delete</button>
                                    <span className="px-2 py-1 rounded-full border border-white/10 text-zinc-400">
                                        Auto-mute on detection
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-sm font-semibold">Pronunciation Overrides</h3>
                        <span className="text-[11px] text-zinc-400">3 saved</span>
                    </div>
                    <div className="space-y-3">
                        {pronunciationOverrides.map((item) => (
                            <div key={item.term} className="rounded-xl border border-white/10 bg-white/5 p-3">
                                <div className="flex items-start justify-between gap-3">
                                    <div>
                                        <p className="text-sm font-semibold">{item.term}</p>
                                        <p className="text-xs text-zinc-400 mt-1">Say as: {item.sayAs}</p>
                                        <p className="text-[11px] text-zinc-500 mt-1">/{item.phonetic}/ · {item.locale}</p>
                                    </div>
                                    <div className="flex gap-2 text-[11px]">
                                        <button className="px-2 py-1 rounded-full border border-white/10">Edit</button>
                                        <button className="px-2 py-1 rounded-full border border-white/10">Delete</button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="rounded-xl border border-white/10 bg-black/40 p-4">
                    <p className="text-xs uppercase tracking-[0.3em] text-zinc-500">Sample usage</p>
                    <div className="mt-3 space-y-2 text-xs text-zinc-300">
                        <p>
                            “Tonight on <span className="text-white">Neon Frequency</span>, Axel Rift welcomes our Synthwave
                            curator.”
                        </p>
                        <p className="text-zinc-500">
                            Auto-replace unsafe phrases and enforce phonetic clarity before airing.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default PronunciationSafetyPanel;
