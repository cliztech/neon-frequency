import { useCallback } from 'react';
import { TrackChannel } from '../core/TrackChannel';
import { MicOff, Headphones } from 'lucide-react';
import MeterDisplay from './MeterDisplay';

interface ChannelStripProps {
    track: TrackChannel;
}

export default function ChannelStrip({ track }: ChannelStripProps) {
    // Simple state-less simulation for now, w/ direct mutations

    const handleToggleMute = useCallback(() => track.toggleMute(!track.isMuted()), [track]);
    const handleToggleSolo = useCallback(() => track.toggleSolo(!track.isSoloed()), [track]);

    return (
        <div className="w-24 h-96 bg-zinc-900 border-r border-zinc-800 flex flex-col p-2 gap-4">

            {/* Headers */}
            <div className="text-center font-mono text-xs font-bold text-zinc-400 truncate">
                {track.name}
            </div>

            {/* EQ/Pan Area Mockup */}
            <div className="flex-1 bg-zinc-950/50 rounded border border-zinc-800 flex items-center justify-center">
                <div className="text-[10px] text-zinc-600 -rotate-90">insert rack</div>
            </div>

            {/* Fader Area */}
            <div className="h-40 flex gap-2 justify-center bg-zinc-950 rounded p-1">
                {/* Meter */}
                <MeterDisplay track={track} />

                {/* Fader Track */}
                <div className="w-6 relative group">
                    {/* Fader Handle Mockup */}
                    <div className="absolute top-[20%] left-1/2 w-6 h-8 bg-gradient-to-b from-zinc-700 to-zinc-800 rounded -translate-x-1/2 shadow-lg border border-zinc-600 hover:border-neon-cyan cursor-grab flex items-center justify-center z-10">
                        <div className="w-4 h-[1px] bg-white/50" />
                    </div>
                    <div className="absolute left-1/2 top-0 bottom-0 w-[2px] bg-zinc-800 -translate-x-1/2" />
                </div>
            </div>

            {/* Controls */}
            <div className="flex gap-1 justify-center">
                <button
                    onClick={handleToggleMute}
                    className="w-6 h-6 rounded bg-zinc-800 text-zinc-400 hover:text-red-400 hover:bg-red-400/10 flex items-center justify-center transition-colors"
                >
                    <MicOff className="w-3 h-3" />
                </button>
                <button
                    onClick={handleToggleSolo}
                    className="w-6 h-6 rounded bg-zinc-800 text-zinc-400 hover:text-yellow-400 hover:bg-yellow-400/10 flex items-center justify-center transition-colors"
                >
                    <Headphones className="w-3 h-3" />
                </button>
            </div>

            <div className="text-center font-mono text-xs text-neon-cyan">
                -0.0 dB
            </div>
        </div>
    );
}
