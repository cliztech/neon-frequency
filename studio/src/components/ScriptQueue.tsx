import { useState, useEffect, useRef } from 'react';

// Types
interface GeneratedScript {
    id: string;
    name: string;
    prompt_id: string;
    content: string;
    status: string;
    voice_track_path: string | null;
    voice_generated_at: string | null;
    input_song: string | null;
    input_artist: string | null;
    created_at: string;
    updated_at: string;
}

interface ScriptStats {
    total: number;
    pending: number;
    under_review: number;
    approved: number;
    complete: number;
    failed: number;
}

interface Prompt {
    id: string;
    name: string;
    category: string;
}

const API_BASE = 'http://localhost:8000/api';

const STATUS_COLORS: Record<string, string> = {
    pending: 'bg-yellow-500/20 text-yellow-300 border-yellow-400/30',
    under_review: 'bg-cyan-500/20 text-cyan-300 border-cyan-400/30',
    approved: 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30',
    complete: 'bg-green-500/20 text-green-300 border-green-400/30',
    failed: 'bg-red-500/20 text-red-300 border-red-400/30',
};

const ScriptQueue = () => {
    const [scripts, setScripts] = useState<GeneratedScript[]>([]);
    const [selectedScript, setSelectedScript] = useState<GeneratedScript | null>(null);
    const [stats, setStats] = useState<ScriptStats | null>(null);
    const [prompts, setPrompts] = useState<Prompt[]>([]);
    const [filterStatus, setFilterStatus] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [generating, setGenerating] = useState(false);
    const [generatingVoice, setGeneratingVoice] = useState(false);

    // Generate dialog state
    const [showGenerateDialog, setShowGenerateDialog] = useState(false);
    const [generateForm, setGenerateForm] = useState({
        prompt_id: '',
        input_song: '',
        input_artist: '',
    });

    // Edit state
    const [editingContent, setEditingContent] = useState('');

    const audioRef = useRef<HTMLAudioElement>(null);

    useEffect(() => {
        fetchScripts();
        fetchStats();
        fetchPrompts();
    }, []);

    const fetchScripts = async () => {
        try {
            const res = await fetch(`${API_BASE}/scripts`);
            const data = await res.json();
            setScripts(data);
        } catch (error) {
            console.error('Failed to fetch scripts:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchStats = async () => {
        try {
            const res = await fetch(`${API_BASE}/scripts/stats`);
            const data = await res.json();
            setStats(data);
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        }
    };

    const fetchPrompts = async () => {
        try {
            const res = await fetch(`${API_BASE}/prompts`);
            const data = await res.json();
            setPrompts(data);
        } catch (error) {
            console.error('Failed to fetch prompts:', error);
        }
    };

    const selectScript = (script: GeneratedScript) => {
        setSelectedScript(script);
        setEditingContent(script.content);
    };

    const handleGenerate = async () => {
        if (!generateForm.prompt_id) return;

        setGenerating(true);
        try {
            const res = await fetch(`${API_BASE}/scripts/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(generateForm),
            });
            const newScript = await res.json();
            setScripts([newScript, ...scripts]);
            selectScript(newScript);
            setShowGenerateDialog(false);
            fetchStats();
        } catch (error) {
            console.error('Failed to generate script:', error);
        } finally {
            setGenerating(false);
        }
    };

    const handleSaveContent = async () => {
        if (!selectedScript) return;

        try {
            await fetch(`${API_BASE}/scripts/${selectedScript.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: editingContent }),
            });
            fetchScripts();
        } catch (error) {
            console.error('Failed to save content:', error);
        }
    };

    const handleApprove = async () => {
        if (!selectedScript) return;

        try {
            const res = await fetch(`${API_BASE}/scripts/${selectedScript.id}/approve`, {
                method: 'POST',
            });
            const updated = await res.json();
            setSelectedScript(updated);
            fetchScripts();
            fetchStats();
        } catch (error) {
            console.error('Failed to approve script:', error);
        }
    };

    const handleRegenerate = async () => {
        if (!selectedScript) return;

        setGenerating(true);
        try {
            const res = await fetch(`${API_BASE}/scripts/${selectedScript.id}/regenerate`, {
                method: 'POST',
            });
            const newScript = await res.json();
            setSelectedScript(newScript);
            setEditingContent(newScript.content);
            fetchScripts();
            fetchStats();
        } catch (error) {
            console.error('Failed to regenerate script:', error);
        } finally {
            setGenerating(false);
        }
    };

    const handleDelete = async () => {
        if (!selectedScript) return;
        if (!confirm('Delete this script?')) return;

        try {
            await fetch(`${API_BASE}/scripts/${selectedScript.id}`, {
                method: 'DELETE',
            });
            setSelectedScript(null);
            fetchScripts();
            fetchStats();
        } catch (error) {
            console.error('Failed to delete script:', error);
        }
    };

    const handleDeleteAll = async () => {
        if (!confirm('Delete ALL scripts? This cannot be undone.')) return;

        try {
            await fetch(`${API_BASE}/scripts`, {
                method: 'DELETE',
            });
            setScripts([]);
            setSelectedScript(null);
            fetchStats();
        } catch (error) {
            console.error('Failed to delete all scripts:', error);
        }
    };

    const handleGenerateVoice = async () => {
        if (!selectedScript) return;

        setGeneratingVoice(true);
        try {
            // TODO: Implement voice generation endpoint
            // For now, just show a placeholder
            alert('Voice generation will be implemented with ElevenLabs/Gemini TTS integration');
        } catch (error) {
            console.error('Failed to generate voice:', error);
        } finally {
            setGeneratingVoice(false);
        }
    };

    const filteredScripts = filterStatus ? scripts.filter((s) => s.status === filterStatus) : scripts;

    const formatDate = (dateStr: string) => {
        const date = new Date(dateStr);
        return date.toLocaleString();
    };

    return (
        <div className="flex h-full pointer-events-auto">
            {/* Left Panel - Script List */}
            <div className="w-80 border-r border-white/10 bg-zinc-950/80 flex flex-col">
                <div className="p-4 border-b border-white/10">
                    <h2 className="text-lg font-semibold">Script/VO Queue</h2>
                    <p className="text-xs text-zinc-400 mt-1">Generated scripts and voice tracks</p>
                </div>

                {/* Stats */}
                {stats && (
                    <div className="p-3 border-b border-white/10 grid grid-cols-3 gap-2 text-center">
                        <div className="bg-white/5 rounded-lg p-2">
                            <p className="text-lg font-bold">{stats.total}</p>
                            <p className="text-[10px] text-zinc-400">Total</p>
                        </div>
                        <div className="bg-cyan-500/10 rounded-lg p-2">
                            <p className="text-lg font-bold text-cyan-300">{stats.under_review}</p>
                            <p className="text-[10px] text-zinc-400">Review</p>
                        </div>
                        <div className="bg-emerald-500/10 rounded-lg p-2">
                            <p className="text-lg font-bold text-emerald-300">{stats.complete}</p>
                            <p className="text-[10px] text-zinc-400">Complete</p>
                        </div>
                    </div>
                )}

                {/* Filters */}
                <div className="p-3 border-b border-white/10 flex gap-2">
                    <select
                        value={filterStatus}
                        onChange={(e) => setFilterStatus(e.target.value)}
                        className="flex-1 bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                    >
                        <option value="">All Status</option>
                        <option value="pending">Pending</option>
                        <option value="under_review">Under Review</option>
                        <option value="approved">Approved</option>
                        <option value="complete">Complete</option>
                        <option value="failed">Failed</option>
                    </select>
                </div>

                {/* Script List */}
                <div className="flex-1 overflow-y-auto p-3 space-y-2">
                    {loading ? (
                        <p className="text-sm text-zinc-500">Loading...</p>
                    ) : filteredScripts.length === 0 ? (
                        <p className="text-sm text-zinc-500">No scripts yet. Generate one!</p>
                    ) : (
                        filteredScripts.map((script) => (
                            <button
                                key={script.id}
                                onClick={() => selectScript(script)}
                                className={`w-full text-left p-3 rounded-xl border transition-all ${selectedScript?.id === script.id
                                        ? 'border-cyan-400/50 bg-cyan-500/10'
                                        : 'border-white/10 bg-white/5 hover:bg-white/10'
                                    }`}
                            >
                                <p className="text-sm font-medium truncate">{script.name}</p>
                                <div className="flex items-center gap-2 mt-2">
                                    <span
                                        className={`text-[10px] px-2 py-0.5 rounded-full border ${STATUS_COLORS[script.status] || 'bg-white/10 text-zinc-400'
                                            }`}
                                    >
                                        {script.status.replace('_', ' ')}
                                    </span>
                                    {script.voice_track_path && (
                                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300">
                                            🎙️ Voice
                                        </span>
                                    )}
                                </div>
                            </button>
                        ))
                    )}
                </div>

                {/* Actions */}
                <div className="p-3 border-t border-white/10 space-y-2">
                    <button
                        onClick={() => setShowGenerateDialog(true)}
                        className="w-full py-2 rounded-full bg-cyan-500 text-black text-sm font-semibold"
                    >
                        + Generate New Script
                    </button>
                    {scripts.length > 0 && (
                        <button
                            onClick={handleDeleteAll}
                            className="w-full py-2 rounded-full border border-red-500/40 text-red-400 text-sm"
                        >
                            Delete All
                        </button>
                    )}
                </div>
            </div>

            {/* Right Panel - Script Editor */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {selectedScript ? (
                    <>
                        <div className="p-4 border-b border-white/10 flex items-center justify-between">
                            <div>
                                <h3 className="text-lg font-semibold">{selectedScript.name}</h3>
                                <p className="text-xs text-zinc-400 mt-1">
                                    Created: {formatDate(selectedScript.created_at)}
                                </p>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className={`px-3 py-1 rounded-full border text-xs ${STATUS_COLORS[selectedScript.status]}`}>
                                    {selectedScript.status.replace('_', ' ')}
                                </span>
                            </div>
                        </div>

                        <div className="flex-1 flex flex-col p-4 overflow-y-auto">
                            {/* Input Context */}
                            {(selectedScript.input_song || selectedScript.input_artist) && (
                                <div className="mb-4 p-3 rounded-xl bg-white/5 border border-white/10">
                                    <p className="text-xs text-zinc-400 mb-1">Generation Context</p>
                                    <p className="text-sm">
                                        {selectedScript.input_artist && <span>Artist: {selectedScript.input_artist}</span>}
                                        {selectedScript.input_artist && selectedScript.input_song && ' | '}
                                        {selectedScript.input_song && <span>Song: {selectedScript.input_song}</span>}
                                    </p>
                                </div>
                            )}

                            {/* Script Content */}
                            <div className="flex-1">
                                <p className="text-xs text-zinc-400 mb-2">Script Content</p>
                                <textarea
                                    value={editingContent}
                                    onChange={(e) => setEditingContent(e.target.value)}
                                    className="w-full h-48 bg-zinc-900 border border-white/10 rounded-xl p-4 text-sm resize-none focus:outline-none focus:border-cyan-400/50"
                                />
                                {editingContent !== selectedScript.content && (
                                    <button
                                        onClick={handleSaveContent}
                                        className="mt-2 px-4 py-1 rounded-full bg-white text-black text-xs font-semibold"
                                    >
                                        Save Changes
                                    </button>
                                )}
                            </div>

                            {/* Voice Track Section */}
                            <div className="mt-4 p-4 rounded-xl border border-white/10 bg-white/5">
                                <h4 className="text-sm font-semibold mb-3">Voice Generation</h4>

                                {selectedScript.voice_track_path ? (
                                    <div className="space-y-3">
                                        <div className="flex items-center gap-2">
                                            <span className="text-emerald-400">✓</span>
                                            <span className="text-sm">Voice track generated</span>
                                        </div>
                                        <audio ref={audioRef} controls className="w-full h-10">
                                            <source src={selectedScript.voice_track_path} type="audio/mpeg" />
                                        </audio>
                                        <p className="text-xs text-zinc-400">
                                            Generated: {selectedScript.voice_generated_at && formatDate(selectedScript.voice_generated_at)}
                                        </p>
                                    </div>
                                ) : (
                                    <button
                                        onClick={handleGenerateVoice}
                                        disabled={generatingVoice || selectedScript.status !== 'approved'}
                                        className={`w-full py-2 rounded-full text-sm font-semibold ${selectedScript.status === 'approved'
                                                ? 'bg-purple-500 text-white'
                                                : 'bg-zinc-700 text-zinc-400 cursor-not-allowed'
                                            }`}
                                    >
                                        {generatingVoice ? 'Generating...' : '🎙️ Generate Voice Track'}
                                    </button>
                                )}
                                {selectedScript.status !== 'approved' && !selectedScript.voice_track_path && (
                                    <p className="text-xs text-zinc-500 mt-2">Approve script first to generate voice</p>
                                )}
                            </div>

                            {/* Actions */}
                            <div className="mt-4 flex gap-2">
                                {selectedScript.status === 'under_review' && (
                                    <button
                                        onClick={handleApprove}
                                        className="flex-1 py-2 rounded-full bg-emerald-500 text-white text-sm font-semibold"
                                    >
                                        ✓ Approve
                                    </button>
                                )}
                                <button
                                    onClick={handleRegenerate}
                                    disabled={generating}
                                    className="flex-1 py-2 rounded-full border border-cyan-400/40 text-cyan-300 text-sm"
                                >
                                    {generating ? 'Regenerating...' : '↻ Regenerate'}
                                </button>
                                <button
                                    onClick={handleDelete}
                                    className="px-4 py-2 rounded-full border border-red-500/40 text-red-400 text-sm"
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    </>
                ) : (
                    <div className="flex-1 flex items-center justify-center">
                        <div className="text-center">
                            <p className="text-zinc-400">Select a script to view or edit</p>
                            <button
                                onClick={() => setShowGenerateDialog(true)}
                                className="mt-4 px-6 py-2 rounded-full bg-cyan-500 text-black text-sm font-semibold"
                            >
                                Generate New Script
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {/* Generate Dialog */}
            {showGenerateDialog && (
                <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
                    <div className="bg-zinc-900 rounded-2xl border border-white/10 p-6 w-[400px]">
                        <h3 className="text-lg font-semibold mb-4">Generate New Script</h3>

                        <div className="space-y-4">
                            <div>
                                <p className="text-xs text-zinc-400 mb-1">Select Prompt</p>
                                <select
                                    value={generateForm.prompt_id}
                                    onChange={(e) => setGenerateForm({ ...generateForm, prompt_id: e.target.value })}
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                >
                                    <option value="">Choose a prompt...</option>
                                    {prompts.map((p) => (
                                        <option key={p.id} value={p.id}>
                                            {p.name} ({p.category})
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <p className="text-xs text-zinc-400 mb-1">Artist (optional)</p>
                                <input
                                    type="text"
                                    value={generateForm.input_artist}
                                    onChange={(e) => setGenerateForm({ ...generateForm, input_artist: e.target.value })}
                                    placeholder="e.g., The Weeknd"
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                />
                            </div>

                            <div>
                                <p className="text-xs text-zinc-400 mb-1">Song (optional)</p>
                                <input
                                    type="text"
                                    value={generateForm.input_song}
                                    onChange={(e) => setGenerateForm({ ...generateForm, input_song: e.target.value })}
                                    placeholder="e.g., Blinding Lights"
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                />
                            </div>
                        </div>

                        <div className="flex gap-2 mt-6">
                            <button
                                onClick={() => setShowGenerateDialog(false)}
                                className="flex-1 py-2 rounded-full border border-white/10 text-sm"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleGenerate}
                                disabled={!generateForm.prompt_id || generating}
                                className="flex-1 py-2 rounded-full bg-cyan-500 text-black text-sm font-semibold disabled:opacity-50"
                            >
                                {generating ? 'Generating...' : 'Generate'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ScriptQueue;
