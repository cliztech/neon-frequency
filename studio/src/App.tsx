import { useState } from 'react';
import HolographicStage from './components/3d/HolographicStage';
import RadioDashboard from './components/RadioDashboard';
import PromptLibrary from './components/PromptLibrary';
import ScriptQueue from './components/ScriptQueue';

type TabId = 'dashboard' | 'prompts' | 'scripts';

const TABS: { id: TabId; label: string; icon: string }[] = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'prompts', label: 'Prompt Library', icon: '📝' },
    { id: 'scripts', label: 'Script Queue', icon: '🎙️' },
];

function App() {
    const [isReady, setIsReady] = useState(false);
    const [activeTab, setActiveTab] = useState<TabId>('dashboard');

    const handleStart = async () => {
        setIsReady(true);
    };

    if (!isReady) {
        return (
            <div className="w-screen h-screen flex items-center justify-center bg-zinc-950 relative overflow-hidden">
                <div className="absolute inset-0 z-0">
                    <HolographicStage />
                </div>

                <div className="relative z-10 text-center bg-zinc-950/50 p-12 rounded-2xl backdrop-blur-sm border border-white/10 shadow-2xl">
                    <h1 className="text-5xl font-bold tracking-tighter mb-4 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-600 drop-shadow-[0_0_15px_rgba(34,211,238,0.5)]">
                        NEON STUDIO
                    </h1>
                    <p className="text-zinc-400 mb-8 font-mono text-sm tracking-widest">ROBODJ V2 AUTOMATION SUITE</p>
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

    const renderContent = () => {
        switch (activeTab) {
            case 'dashboard':
                return <RadioDashboard />;
            case 'prompts':
                return <PromptLibrary />;
            case 'scripts':
                return <ScriptQueue />;
            default:
                return <RadioDashboard />;
        }
    };

    return (
        <div className="w-screen h-screen flex flex-col bg-zinc-950 text-white overflow-hidden relative">
            {/* 3D Background - only for dashboard */}
            {activeTab === 'dashboard' && <HolographicStage />}

            {/* Top Navigation */}
            <header className="h-14 flex items-center justify-between px-6 border-b border-white/10 bg-zinc-950/90 backdrop-blur-md z-20">
                <div className="flex items-center gap-6">
                    <div>
                        <p className="text-xs uppercase tracking-[0.4em] text-cyan-400">Neon Frequency</p>
                    </div>

                    {/* Tabs */}
                    <nav className="flex items-center gap-1">
                        {TABS.map((tab) => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                                    activeTab === tab.id
                                        ? 'bg-white/10 text-white'
                                        : 'text-zinc-400 hover:text-white hover:bg-white/5'
                                }`}
                            >
                                <span className="mr-2">{tab.icon}</span>
                                {tab.label}
                            </button>
                        ))}
                    </nav>
                </div>

                <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5">
                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                        <span className="text-xs text-zinc-300">On Air · 128 BPM</span>
                    </div>
                    <button className="px-4 py-2 rounded-full bg-white text-black text-xs font-semibold tracking-[0.2em] uppercase">
                        Go Live
                    </button>
                </div>
            </header>

            {/* Content Area */}
            <div className={`flex-1 overflow-hidden ${activeTab === 'dashboard' ? 'absolute inset-0 pt-14 z-10' : ''}`}>
                {renderContent()}
            </div>
        </div>
    );
}

export default App;
