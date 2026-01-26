import { useState } from 'react';
import { engine } from './core/AudioEngine';
import TransportControls from './components/TransportControls';
import MixerConsole from './components/MixerConsole';
import PianoRoll from './components/PianoRoll';
import ArrangementView from './components/ArrangementView';
import ViewSwitcher from './components/ViewSwitcher';
import FileBrowser from './components/FileBrowser';
import HolographicStage from './components/3d/HolographicStage';
import { TrackChannel } from './core/TrackChannel';

function App() {
    const [tracks, setTracks] = useState<TrackChannel[]>([]);
    const [isReady, setIsReady] = useState(false);
    const [currentView, setCurrentView] = useState<'arrangement' | 'piano'>('arrangement');

    // Initialize Audio Engine on first interaction
    const handleStart = async () => {
        await engine.initialize();

        // Create Default Session
        engine.createTrack("KICK");
        engine.createTrack("SNARE");
        engine.createTrack("BASS");
        engine.createTrack("LEAD");

        setTracks(engine.getAllTracks());
        setIsReady(true);
    };

    if (!isReady) {
        return (
            <div className="w-screen h-screen flex items-center justify-center bg-zinc-950 relative overflow-hidden">
                {/* 3D Background for Landing */}
                <div className="absolute inset-0 z-0">
                    <HolographicStage />
                </div>

                <div className="relative z-10 text-center bg-zinc-950/50 p-12 rounded-2xl backdrop-blur-sm border border-white/10 shadow-2xl">
                    <h1 className="text-5xl font-bold tracking-tighter mb-4 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-600 drop-shadow-[0_0_15px_rgba(34,211,238,0.5)]">
                        NEON STUDIO
                    </h1>
                    <p className="text-zinc-400 mb-8 font-mono text-sm tracking-widest">ULTRATHINK AUDIO ENGINE v1.0</p>
                    <button
                        onClick={handleStart}
                        className="px-8 py-3 bg-white text-black font-bold rounded-full hover:scale-105 transition-all shadow-[0_0_20px_rgba(255,255,255,0.3)]"
                    >
                        INITIALIZE SYSTEM
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="w-screen h-screen flex flex-col bg-zinc-950 text-white overflow-hidden relative">
            {/* 3D BACKGROUND (Absolute Position) */}
            <HolographicStage />

            {/* UI OVERLAY (Z-Index 10) */}
            <div className="absolute inset-0 z-10 flex flex-col pointer-events-none">
                {/* TOP BAR */}
                <header className="h-14 border-b border-white/10 flex items-center justify-between px-4 bg-zinc-950/80 backdrop-blur-md pointer-events-auto">
                    <div className="flex items-center gap-4">
                        <div className="font-bold tracking-widest text-zinc-500">ULTRATHINK STUDIO</div>
                        <ViewSwitcher view={currentView} setView={setCurrentView} />
                    </div>

                    <TransportControls />

                    <div className="flex gap-2">
                        <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-xs font-mono text-zinc-500">CPU: 12%</span>
                    </div>
                </header>

                {/* BOTTOM AREA (Browser + Workspace) */}
                <div className="flex-1 flex overflow-hidden pointer-events-auto">
                    {/* FILE BROWSER */}
                    <div className="bg-zinc-950/80 backdrop-blur-md border-r border-white/10">
                        <FileBrowser />
                    </div>

                    {/* MAIN WORKSPACE */}
                    <main className="flex-1 flex overflow-hidden flex-col bg-zinc-950/30 backdrop-blur-sm">
                        {/* DYNAMIC VIEW */}
                        <div className="flex-1 border-b border-white/10 flex overflow-hidden relative">
                            {currentView === 'arrangement' ? <ArrangementView /> : <PianoRoll />}
                        </div>

                        {/* MIXER VIEW */}
                        <div className="bg-zinc-950/80 backdrop-blur-md border-t border-white/10">
                            <MixerConsole tracks={tracks} />
                        </div>
                    </main>
                </div>
            </div>
        </div>
    );
}

export default App;
