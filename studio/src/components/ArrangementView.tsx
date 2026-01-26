export default function ArrangementView() {
    const tracks = ["KICK", "SNARE", "BASS", "LEAD"];
    const clips = [
        { track: 0, start: 0, length: 4, name: "Kick Loop 1", color: "bg-red-500" },
        { track: 1, start: 4, length: 4, name: "Snare Build", color: "bg-yellow-500" },
        { track: 2, start: 0, length: 8, name: "Reese Bass", color: "bg-blue-500" },
        { track: 3, start: 8, length: 8, name: "Arp Lead", color: "bg-purple-500" },
    ];

    return (
        <div className="h-full bg-zinc-900 overflow-y-auto flex flex-col">
            {/* Timeline Header */}
            <div className="h-8 bg-zinc-950 border-b border-zinc-800 flex relative overflow-hidden">
                <div className="w-24 border-r border-zinc-800 bg-zinc-950 flex-shrink-0" />
                <div className="flex-1 bg-zinc-900/50 relative">
                    {/* Time Ruler (Mock) */}
                    <div className="absolute top-0 bottom-0 left-0 w-[1px] bg-red-500/50 z-10" />
                    {Array.from({ length: 32 }).map((_, i) => (
                        <div key={i} className="absolute top-4 h-2 w-[1px] bg-zinc-700 text-[9px] text-zinc-500 font-mono pl-1" style={{ left: `${i * 40}px` }}>
                            {i % 4 === 0 ? i / 4 + 1 : ''}
                        </div>
                    ))}
                </div>
            </div>

            {/* Tracks */}
            <div className="flex-1 bg-zinc-900 relative">
                {tracks.map((track, i) => (
                    <div key={i} className="h-16 flex border-b border-zinc-800 relative group">
                        {/* Header */}
                        <div className="w-24 border-r border-zinc-800 bg-zinc-950 flex items-center justify-center text-xs font-bold text-zinc-400 group-hover:text-white transition-colors">
                            {track}
                        </div>
                        {/* Lane */}
                        <div className="flex-1 relative bg-zinc-900/30 group-hover:bg-zinc-800/30 transition-colors">
                            {/* Grid Lines */}
                            <div className="absolute inset-0"
                                style={{ backgroundImage: 'linear-gradient(to right, #27272a 1px, transparent 1px)', backgroundSize: '40px 100%' }}
                            />
                        </div>
                    </div>
                ))}

                {/* Clips Overlay */}
                {clips.map((clip, i) => (
                    <div
                        key={i}
                        className={`absolute h-14 top-1 rounded border border-white/10 ${clip.color} opacity-80 hover:opacity-100 cursor-move flex items-center px-2 shadow-lg`}
                        style={{
                            left: `${clip.start * 40 + 96}px`, // 96px offset for header
                            top: `${clip.track * 64 + 1}px`, // 64px row height
                            width: `${clip.length * 40}px`
                        }}
                    >
                        <span className="text-[10px] font-bold text-white shadow-black drop-shadow-md truncate">{clip.name}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
