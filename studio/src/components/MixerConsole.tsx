import { TrackChannel } from '../core/TrackChannel';
import ChannelStrip from './ChannelStrip';

interface MixerConsoleProps {
    tracks: TrackChannel[];
}

export default function MixerConsole({ tracks }: MixerConsoleProps) {
    return (
        <div className="flex-1 bg-zinc-950 p-4 border-t border-zinc-800 flex gap-1 overflow-x-auto items-center justify-center min-h-[400px]">
            {/* Master Output Strip (Mockup) */}
            <div className="w-24 h-96 bg-zinc-900 border-r-2 border-zinc-800 flex flex-col p-2 gap-4 opacity-50 pointer-events-none">
                <div className="text-center font-mono text-xs font-bold text-zinc-500">MASTER</div>
                <div className="flex-1" />
            </div>

            {tracks.map(track => (
                <ChannelStrip key={track.id} track={track} />
            ))}

            {/* Add Track Button (Mockup) */}
            <button className="w-12 h-96 border border-dashed border-zinc-800 rounded flex items-center justify-center text-zinc-600 hover:text-zinc-400 hover:border-zinc-600 transition-colors">
                <span className="rotate-90 text-sm font-mono">+ ADD</span>
            </button>
        </div>
    );
}
