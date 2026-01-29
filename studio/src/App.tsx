import { useState } from 'react';
import HolographicStage from './components/3d/HolographicStage';
import RadioDashboard from './components/RadioDashboard';

function App() {
    const [isReady, setIsReady] = useState(false);

    // Initialize Audio Engine on first interaction
    const handleStart = async () => {
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
                        ENTER CONTROL ROOM
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="w-screen h-screen flex flex-col bg-zinc-950 text-white overflow-hidden relative">
            <HolographicStage />
            <div className="absolute inset-0 z-10 flex flex-col pointer-events-none">
                <RadioDashboard />
            </div>
        </div>
    );
}

export default App;
