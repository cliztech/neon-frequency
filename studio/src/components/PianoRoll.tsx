import { useState } from 'react';

interface MidiNote {
    pitch: string; // e.g., "C4"
    start: number; // 16th steps
    duration: number; // 16th steps
}

export default function PianoRoll() {
    // Suppress setNotes warning by ignoring it in destructuring for now
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [notes] = useState<MidiNote[]>([
        { pitch: "C4", start: 0, duration: 4 },
        { pitch: "E4", start: 4, duration: 4 },
        { pitch: "G4", start: 8, duration: 4 },
        { pitch: "C5", start: 12, duration: 4 },
    ]);

    // 16 steps (1 bar), 12 keys (1 octave)
    const steps = Array.from({ length: 16 }, (_, i) => i);
    const keys = ["C5", "B4", "A#4", "A4", "G#4", "G4", "F#4", "F4", "E4", "D#4", "D4", "C#4", "C4"];

    return (
        <div className="h-full bg-zinc-900 overflow-y-auto flex">
            {/* Keys Column */}
            <div className="w-12 flex-shrink-0 bg-zinc-950 border-r border-zinc-800">
                {keys.map(key => (
                    <div key={key} className={`h-8 border-b border-zinc-900 flex items-center justify-end pr-1 text-[10px] font-mono ${key.includes('#') ? 'bg-zinc-900 text-zinc-600' : 'bg-zinc-800 text-zinc-400'}`}>
                        {key}
                    </div>
                ))}
            </div>

            {/* Grid */}
            <div className="flex-1 relative overflow-x-auto bg-zinc-900/50"
                style={{
                    backgroundImage: 'linear-gradient(to right, #27272a 1px, transparent 1px), linear-gradient(to bottom, #27272a 1px, transparent 1px)',
                    backgroundSize: '40px 32px'
                }}>

                {/* Vertical Grid Lines (using steps) */}
                {steps.map(step => (
                    <div key={step} className="absolute top-0 bottom-0 w-[1px] bg-zinc-800 pointer-events-none" style={{ left: `${step * 40}px` }} />
                ))}

                {/* Notes */}
                {notes.map((note, i) => (
                    <div
                        key={i}
                        className="absolute h-7 top-[1px] bg-neon-cyan/80 border border-neon-cyan rounded-sm shadow-[0_0_10px_rgba(34,211,238,0.3)] hover:brightness-110 cursor-move"
                        style={{
                            left: `${note.start * 40}px`,
                            width: `${note.duration * 40}px`,
                            top: `${keys.indexOf(note.pitch) * 32}px`
                        }}
                    >
                        <div className="h-full w-2 bg-white/20 absolute right-0 cursor-ew-resize" />
                    </div>
                ))}
            </div>
        </div>
    );
}
