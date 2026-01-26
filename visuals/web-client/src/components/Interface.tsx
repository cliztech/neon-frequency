import { Radio, Heart, MessageSquare, Disc } from 'lucide-react';

export default function Interface() {
    return (
        <div className="absolute inset-0 z-10 flex flex-col p-6 pointer-events-none">

            {/* HEADER */}
            <header className="flex justify-between items-center pointer-events-auto">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-neon-pink flex items-center justify-center shadow-[0_0_15px_#ff00ff]">
                        <Radio className="text-white w-6 h-6 animate-pulse" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-mono font-bold tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-neon-cyan to-neon-purple neon-text">
                            NEON FREQUENCY
                        </h1>
                        <p className="text-xs text-neon-cyan/80 font-mono tracking-[0.2em]">GENESIS PROTOCOL ACTIVE</p>
                    </div>
                </div>

                <div className="glass-panel px-4 py-2 rounded-full flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                    <span className="text-xs font-mono text-red-400">LIVE · 38°C · SECTOR 7G</span>
                </div>
            </header>

            {/* MAIN LAYOUT */}
            <main className="flex-1 flex items-end justify-between mt-10">

                {/* LEFT: NOW PLAYING */}
                <div className="glass-panel p-6 rounded-2xl w-80 pointer-events-auto backdrop-blur-xl border-neon-cyan/20 neon-border">
                    <div className="flex items-start gap-4 mb-4">
                        <div className="w-16 h-16 bg-black/50 rounded-lg flex items-center justify-center border border-white/10 shrink-0 overflow-hidden">
                            <Disc className="w-8 h-8 text-white/20 animate-spin-slow" />
                        </div>
                        <div>
                            <h2 className="text-lg font-bold leading-tight text-white">Happy Hardcore Anthem</h2>
                            <p className="text-sm text-neon-purple mt-1">Unknown Artist</p>
                        </div>
                    </div>

                    {/* Visualizer Bar (Simulated) */}
                    <div className="flex items-end gap-1 h-8 animate-pulse">
                        {[...Array(12)].map((_, i) => (
                            <div key={i} className="flex-1 bg-neon-cyan rounded-t-sm" style={{ height: `${Math.random() * 100}%`, opacity: 0.8 }} />
                        ))}
                    </div>
                </div>

                {/* RIGHT: CHAT LOG */}
                <div className="glass-panel p-4 rounded-xl w-72 h-80 flex flex-col pointer-events-auto border-neon-purple/20">
                    <div className="flex items-center gap-2 mb-3 border-b border-white/10 pb-2">
                        <MessageSquare className="w-4 h-4 text-neon-pink" />
                        <span className="text-xs font-bold font-mono tracking-wider">LIVE FEED</span>
                    </div>

                    <div className="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-thin">
                        <div className="text-sm">
                            <span className="text-neon-cyan font-bold text-xs">AEN:</span>
                            <span className="text-white/80 ml-2">Dropping the bass in 3... 2...</span>
                        </div>
                        <div className="text-sm opacity-60">
                            <span className="text-neon-purple font-bold text-xs">User123:</span>
                            <span className="text-white/80 ml-2">Yoooo lets go!</span>
                        </div>
                        <div className="text-sm opacity-60">
                            <span className="text-red-400 font-bold text-xs">GREG:</span>
                            <span className="text-white/80 ml-2">This beat is whack.</span>
                        </div>
                    </div>

                    <input
                        type="text"
                        placeholder="Send a signal..."
                        className="mt-3 bg-black/40 border border-white/10 rounded px-3 py-2 text-xs focus:outline-none focus:border-neon-cyan transition-colors"
                    />
                </div>

            </main>

            {/* FOOTER CONTROLS */}
            <footer className="mt-6 flex justify-center pointer-events-auto">
                <button className="glass-panel w-12 h-12 rounded-full flex items-center justify-center hover:bg-white/10 transition-colors group">
                    <Heart className="w-5 h-5 text-white group-hover:text-neon-pink group-hover:fill-neon-pink transition-all" />
                </button>
            </footer>

            <div className="scanline" />
        </div>
    );
}
