import { useState, useEffect } from 'react';

// Types
interface VoiceSettings {
    provider: string;
    voice_profile: string;
    model_override: string | null;
}

interface TriggerRules {
    vt_marker_name: string | null;
    position: string;
    custom_filename: string | null;
}

interface AISettings {
    model_name: string | null;
    temperature: number;
    max_tokens: number;
}

interface Prompt {
    id: string;
    name: string;
    content: string;
    category: string;
    status: string;
    is_custom_script: boolean;
    voice_settings: VoiceSettings;
    trigger_rules: TriggerRules;
    ai_settings: AISettings;
    output_folder: string | null;
    created_at: string;
    updated_at: string;
}

interface Variable {
    name: string;
    syntax: string;
}

const API_BASE = 'http://localhost:8000/api';

const CATEGORIES = [
    'General',
    'Promos',
    'Weather',
    'News',
    'Song Intro',
    'Song Outro',
    'Station ID',
    'Ad Break',
    'ShoutOuts',
    'Custom',
];

const STATUSES = ['active', 'inactive', 'draft'];
const TTS_PROVIDERS = ['ElevenLabs', 'Gemini', 'OpenAI'];
const VT_POSITIONS = ['Before Marker', 'After Marker', 'Both'];

const PromptLibrary = () => {
    const [prompts, setPrompts] = useState<Prompt[]>([]);
    const [selectedPrompt, setSelectedPrompt] = useState<Prompt | null>(null);
    const [variables, setVariables] = useState<Variable[]>([]);
    const [filterCategory, setFilterCategory] = useState<string>('');
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    // Form state
    const [formData, setFormData] = useState({
        name: '',
        content: '',
        category: 'General',
        status: 'active',
        is_custom_script: false,
        voice_provider: 'ElevenLabs',
        voice_profile: 'Default',
        vt_marker_name: '',
        vt_position: 'After Marker',
        temperature: 0.8,
        max_tokens: 200,
    });

    useEffect(() => {
        fetchPrompts();
        fetchVariables();
    }, []);

    const fetchPrompts = async () => {
        try {
            const res = await fetch(`${API_BASE}/prompts`);
            const data = await res.json();
            setPrompts(data);
        } catch (error) {
            console.error('Failed to fetch prompts:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchVariables = async () => {
        try {
            const res = await fetch(`${API_BASE}/prompts/variables/list`);
            const data = await res.json();
            setVariables(data);
        } catch (error) {
            console.error('Failed to fetch variables:', error);
        }
    };

    const selectPrompt = (prompt: Prompt) => {
        setSelectedPrompt(prompt);
        setFormData({
            name: prompt.name,
            content: prompt.content,
            category: prompt.category,
            status: prompt.status,
            is_custom_script: prompt.is_custom_script,
            voice_provider: prompt.voice_settings.provider,
            voice_profile: prompt.voice_settings.voice_profile,
            vt_marker_name: prompt.trigger_rules.vt_marker_name || '',
            vt_position: prompt.trigger_rules.position,
            temperature: prompt.ai_settings.temperature,
            max_tokens: prompt.ai_settings.max_tokens,
        });
    };

    const insertVariable = (syntax: string) => {
        setFormData((prev) => ({
            ...prev,
            content: prev.content + syntax,
        }));
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            const payload = {
                name: formData.name,
                content: formData.content,
                category: formData.category,
                status: formData.status,
                is_custom_script: formData.is_custom_script,
                voice_settings: {
                    provider: formData.voice_provider,
                    voice_profile: formData.voice_profile,
                    model_override: null,
                },
                trigger_rules: {
                    vt_marker_name: formData.vt_marker_name || null,
                    position: formData.vt_position,
                    custom_filename: null,
                },
                ai_settings: {
                    model_name: null,
                    temperature: formData.temperature,
                    max_tokens: formData.max_tokens,
                },
            };

            if (selectedPrompt) {
                await fetch(`${API_BASE}/prompts/${selectedPrompt.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
            } else {
                await fetch(`${API_BASE}/prompts`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
            }
            fetchPrompts();
        } catch (error) {
            console.error('Failed to save prompt:', error);
        } finally {
            setSaving(false);
        }
    };

    const handleDelete = async () => {
        if (!selectedPrompt) return;
        if (!confirm('Delete this prompt?')) return;

        try {
            await fetch(`${API_BASE}/prompts/${selectedPrompt.id}`, {
                method: 'DELETE',
            });
            setSelectedPrompt(null);
            fetchPrompts();
        } catch (error) {
            console.error('Failed to delete prompt:', error);
        }
    };

    const newPrompt = () => {
        setSelectedPrompt(null);
        setFormData({
            name: '',
            content: '',
            category: 'General',
            status: 'active',
            is_custom_script: false,
            voice_provider: 'ElevenLabs',
            voice_profile: 'Default',
            vt_marker_name: '',
            vt_position: 'After Marker',
            temperature: 0.8,
            max_tokens: 200,
        });
    };

    const filteredPrompts = filterCategory
        ? prompts.filter((p) => p.category === filterCategory)
        : prompts;

    return (
        <div className="flex h-full pointer-events-auto">
            {/* Left Sidebar - Prompt List */}
            <div className="w-72 border-r border-white/10 bg-zinc-950/80 flex flex-col">
                <div className="p-4 border-b border-white/10">
                    <h2 className="text-lg font-semibold">Prompt Library</h2>
                    <p className="text-xs text-zinc-400 mt-1">Manage AI voice track templates</p>
                </div>

                <div className="p-3 border-b border-white/10">
                    <select
                        value={filterCategory}
                        onChange={(e) => setFilterCategory(e.target.value)}
                        className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                    >
                        <option value="">All Categories</option>
                        {CATEGORIES.map((cat) => (
                            <option key={cat} value={cat}>
                                {cat}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="flex-1 overflow-y-auto p-3 space-y-2">
                    {loading ? (
                        <p className="text-sm text-zinc-500">Loading...</p>
                    ) : (
                        filteredPrompts.map((prompt) => (
                            <button
                                key={prompt.id}
                                onClick={() => selectPrompt(prompt)}
                                className={`w-full text-left p-3 rounded-xl border transition-all ${
                                    selectedPrompt?.id === prompt.id
                                        ? 'border-cyan-400/50 bg-cyan-500/10'
                                        : 'border-white/10 bg-white/5 hover:bg-white/10'
                                }`}
                            >
                                <p className="text-sm font-medium truncate">{prompt.name}</p>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-zinc-400">
                                        {prompt.category}
                                    </span>
                                    <span
                                        className={`text-[10px] px-2 py-0.5 rounded-full ${
                                            prompt.status === 'active'
                                                ? 'bg-emerald-500/20 text-emerald-300'
                                                : 'bg-zinc-500/20 text-zinc-400'
                                        }`}
                                    >
                                        {prompt.status}
                                    </span>
                                </div>
                            </button>
                        ))
                    )}
                </div>

                <div className="p-3 border-t border-white/10">
                    <button
                        onClick={newPrompt}
                        className="w-full py-2 rounded-full bg-cyan-500 text-black text-sm font-semibold"
                    >
                        + New Prompt
                    </button>
                </div>
            </div>

            {/* Main Editor */}
            <div className="flex-1 flex flex-col overflow-hidden">
                <div className="p-4 border-b border-white/10 flex items-center justify-between">
                    <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        placeholder="Prompt Name"
                        className="text-xl font-semibold bg-transparent border-none focus:outline-none"
                    />
                    <div className="flex items-center gap-2">
                        {selectedPrompt && (
                            <button
                                onClick={handleDelete}
                                className="px-4 py-2 rounded-full border border-red-500/40 text-red-400 text-xs"
                            >
                                Delete
                            </button>
                        )}
                        <button
                            onClick={handleSave}
                            disabled={saving}
                            className="px-4 py-2 rounded-full bg-white text-black text-xs font-semibold"
                        >
                            {saving ? 'Saving...' : 'Save'}
                        </button>
                    </div>
                </div>

                <div className="flex-1 grid grid-cols-[1fr_280px] overflow-hidden">
                    {/* Content Editor */}
                    <div className="flex flex-col p-4 overflow-y-auto">
                        {/* Quick Insert Variables */}
                        <div className="mb-4">
                            <p className="text-xs text-zinc-400 mb-2">Quick Insert Variables</p>
                            <div className="flex flex-wrap gap-2">
                                {variables.map((v) => (
                                    <button
                                        key={v.syntax}
                                        onClick={() => insertVariable(v.syntax)}
                                        className="px-3 py-1 rounded-full border border-white/10 bg-white/5 text-xs hover:bg-white/10"
                                    >
                                        {v.name}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Prompt Content */}
                        <div className="flex-1">
                            <p className="text-xs text-zinc-400 mb-2">Prompt / Script Content</p>
                            <textarea
                                value={formData.content}
                                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                                placeholder="Enter your prompt template here. Use {{VARIABLE}} syntax for dynamic content."
                                className="w-full h-64 bg-zinc-900 border border-white/10 rounded-xl p-4 text-sm font-mono resize-none focus:outline-none focus:border-cyan-400/50"
                            />
                        </div>

                        {/* Category & Status */}
                        <div className="grid grid-cols-2 gap-4 mt-4">
                            <div>
                                <p className="text-xs text-zinc-400 mb-2">Category</p>
                                <select
                                    value={formData.category}
                                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                >
                                    {CATEGORIES.map((cat) => (
                                        <option key={cat} value={cat}>
                                            {cat}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <p className="text-xs text-zinc-400 mb-2">Status</p>
                                <select
                                    value={formData.status}
                                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                >
                                    {STATUSES.map((s) => (
                                        <option key={s} value={s}>
                                            {s}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        {/* Custom Script Toggle */}
                        <label className="flex items-center gap-2 mt-4 text-sm">
                            <input
                                type="checkbox"
                                checked={formData.is_custom_script}
                                onChange={(e) => setFormData({ ...formData, is_custom_script: e.target.checked })}
                                className="rounded"
                            />
                            <span>Custom Script (skip AI generation, use content as-is)</span>
                        </label>
                    </div>

                    {/* Settings Sidebar */}
                    <div className="border-l border-white/10 p-4 overflow-y-auto bg-zinc-950/50">
                        <h3 className="text-sm font-semibold mb-4">Voice Settings</h3>

                        <div className="space-y-4">
                            <div>
                                <p className="text-xs text-zinc-400 mb-1">TTS Provider</p>
                                <select
                                    value={formData.voice_provider}
                                    onChange={(e) => setFormData({ ...formData, voice_provider: e.target.value })}
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                >
                                    {TTS_PROVIDERS.map((p) => (
                                        <option key={p} value={p}>
                                            {p}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <p className="text-xs text-zinc-400 mb-1">Voice Profile</p>
                                <input
                                    type="text"
                                    value={formData.voice_profile}
                                    onChange={(e) => setFormData({ ...formData, voice_profile: e.target.value })}
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                />
                            </div>
                        </div>

                        <h3 className="text-sm font-semibold mt-6 mb-4">Trigger Rules</h3>

                        <div className="space-y-4">
                            <div>
                                <p className="text-xs text-zinc-400 mb-1">VT Marker Name</p>
                                <input
                                    type="text"
                                    value={formData.vt_marker_name}
                                    onChange={(e) => setFormData({ ...formData, vt_marker_name: e.target.value })}
                                    placeholder="e.g., VT or BREAK"
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                />
                            </div>

                            <div>
                                <p className="text-xs text-zinc-400 mb-1">Position</p>
                                <select
                                    value={formData.vt_position}
                                    onChange={(e) => setFormData({ ...formData, vt_position: e.target.value })}
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                >
                                    {VT_POSITIONS.map((p) => (
                                        <option key={p} value={p}>
                                            {p}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <h3 className="text-sm font-semibold mt-6 mb-4">AI Settings</h3>

                        <div className="space-y-4">
                            <div>
                                <p className="text-xs text-zinc-400 mb-1">Temperature: {formData.temperature}</p>
                                <input
                                    type="range"
                                    min="0"
                                    max="1"
                                    step="0.1"
                                    value={formData.temperature}
                                    onChange={(e) =>
                                        setFormData({ ...formData, temperature: parseFloat(e.target.value) })
                                    }
                                    className="w-full"
                                />
                            </div>

                            <div>
                                <p className="text-xs text-zinc-400 mb-1">Max Tokens</p>
                                <input
                                    type="number"
                                    value={formData.max_tokens}
                                    onChange={(e) => setFormData({ ...formData, max_tokens: parseInt(e.target.value) })}
                                    className="w-full bg-zinc-800 border border-white/10 rounded-lg px-3 py-2 text-sm"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PromptLibrary;
