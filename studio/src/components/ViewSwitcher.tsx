import { LayoutGrid, Music2, FolderOpen } from 'lucide-react';

interface ViewSwitcherProps {
    view: 'arrangement' | 'piano';
    setView: (v: 'arrangement' | 'piano') => void;
}

export default function ViewSwitcher({ view, setView }: ViewSwitcherProps) {
    return (
        <div className="flex gap-1 bg-zinc-900/50 p-1 rounded-lg border border-zinc-800/50">
            <button
                onClick={() => setView('arrangement')}
                className={`p-2 rounded transition-all ${view === 'arrangement'
                        ? 'bg-zinc-800 text-neon-cyan shadow-[0_0_10px_rgba(34,211,238,0.2)]'
                        : 'text-zinc-500 hover:text-zinc-300'
                    }`}
                title="Arrangement View"
            >
                <LayoutGrid className="w-4 h-4" />
            </button>

            <button
                onClick={() => setView('piano')}
                className={`p-2 rounded transition-all ${view === 'piano'
                        ? 'bg-zinc-800 text-neon-pink shadow-[0_0_10px_rgba(255,0,255,0.2)]'
                        : 'text-zinc-500 hover:text-zinc-300'
                    }`}
                title="Piano Roll"
            >
                <Music2 className="w-4 h-4" />
            </button>

            <div className="w-[1px] h-4 bg-zinc-800 my-auto mx-1" />

            <button className="p-2 rounded text-zinc-500 hover:text-zinc-300">
                <FolderOpen className="w-4 h-4" />
            </button>
        </div>
    );
}
