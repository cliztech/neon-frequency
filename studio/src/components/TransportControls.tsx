import { Play, Square, Repeat, Rewind } from 'lucide-react';
import { engine } from '../core/AudioEngine';
import { useState } from 'react';

export default function TransportControls() {
    const [isPlaying, setIsPlaying] = useState(false);

    const togglePlay = () => {
        if (isPlaying) {
            engine.stopTransport();
        } else {
            engine.startTransport();
        }
        setIsPlaying(!isPlaying);
    };

    return (
        <div className="flex items-center gap-4 bg-zinc-900 border border-zinc-800 p-3 rounded-xl shadow-2xl">
            <div className="flex gap-2">
                <button
                    onClick={togglePlay}
                    className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${isPlaying
                            ? 'bg-neon-pink text-white shadow-[0_0_15px_#ff00ff]'
                            : 'bg-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-700'
                        }`}
                >
                    {isPlaying ? <Square className="w-4 h-4 fill-current" /> : <Play className="w-4 h-4 fill-current" />}
                </button>

                <button className="w-10 h-10 rounded-full bg-zinc-800 text-zinc-400 hover:text-white flex items-center justify-center">
                    <Rewind className="w-4 h-4" />
                </button>

                <button className="w-10 h-10 rounded-full bg-zinc-800 text-zinc-400 hover:text-neon-cyan hover:shadow-[0_0_10px_#00f3ff] flex items-center justify-center">
                    <Repeat className="w-4 h-4" />
                </button>
            </div>

            <div className="h-8 w-[1px] bg-zinc-700 mx-2" />

            <div className="font-mono text-xl font-bold text-neon-cyan">
                128.00 <span className="text-xs text-zinc-500">BPM</span>
            </div>
        </div>
    );
}
