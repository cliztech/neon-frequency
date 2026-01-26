import { Folder, FileAudio, Search } from 'lucide-react';

export default function FileBrowser() {
    const folders = ["Drums", "Bass", "Synths", "Vocals", "FX"];
    const samples = [
        "Hyper_Kick_01.wav",
        "Neon_Snare_04.wav",
        "Cyber_Hat_Closed.wav",
        "Glitch_Perc_09.wav"
    ];

    return (
        <div className="w-64 bg-zinc-950 border-r border-zinc-900 flex flex-col h-full text-sm">
            {/* Header */}
            <div className="h-8 flex items-center px-2 border-b border-zinc-900 bg-zinc-950">
                <span className="font-bold text-zinc-500 text-xs tracking-wider">BROWSER</span>
            </div>

            {/* Search */}
            <div className="p-2 border-b border-zinc-900">
                <div className="bg-zinc-900 rounded flex items-center px-2 py-1 gap-2 border border-zinc-800 focus-within:border-neon-cyan/50 transition-colors">
                    <Search className="w-3 h-3 text-zinc-500" />
                    <input
                        type="text"
                        placeholder="Search..."
                        className="bg-transparent border-none outline-none text-xs w-full text-zinc-300 placeholder-zinc-600"
                    />
                </div>
            </div>

            {/* List */}
            <div className="flex-1 overflow-y-auto p-2 scrollbar-thin scrollbar-thumb-zinc-800">
                {/* Folders */}
                <div className="mb-4">
                    <div className="text-[10px] font-bold text-zinc-600 mb-1 px-1">FOLDERS</div>
                    {folders.map(folder => (
                        <div key={folder} className="flex items-center gap-2 px-2 py-1 hover:bg-zinc-900 rounded cursor-pointer text-zinc-400 hover:text-white transition-colors group">
                            <Folder className="w-3 h-3 fill-zinc-800 group-hover:fill-zinc-700" />
                            <span>{folder}</span>
                        </div>
                    ))}
                </div>

                {/* Samples */}
                <div>
                    <div className="text-[10px] font-bold text-zinc-600 mb-1 px-1">SAMPLES</div>
                    {samples.map(sample => (
                        <div key={sample} className="flex items-center gap-2 px-2 py-1 hover:bg-zinc-900 rounded cursor-pointer text-zinc-500 hover:text-neon-cyan transition-colors draggable" draggable>
                            <FileAudio className="w-3 h-3" />
                            <span className="truncate">{sample}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Footer Mockup */}
            <div className="h-24 border-t border-zinc-900 p-2 bg-zinc-950/50">
                <div className="w-full h-full border border-dashed border-zinc-800 rounded flex items-center justify-center text-[10px] text-zinc-700">
                    Preview Waveform
                </div>
            </div>
        </div>
    );
}
