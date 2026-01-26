import * as Tone from 'tone';
import { TrackChannel } from './TrackChannel';

/**
 * The Heart of the Ultrathink DAW.
 * Manages the Web Audio Context, Transport, and Master Output.
 */
class AudioEngine {
    private static instance: AudioEngine;
    public isInitialized: boolean = false;

    // Track Management
    private tracks: Map<string, TrackChannel> = new Map();

    private constructor() {
        // Private constructor for singleton
    }

    public static getInstance(): AudioEngine {
        if (!AudioEngine.instance) {
            AudioEngine.instance = new AudioEngine();
        }
        return AudioEngine.instance;
    }

    /**
     * Initialize the Audio Context.
     * Must be called after a user interaction (click).
     */
    public async initialize() {
        if (this.isInitialized) return;

        await Tone.start();
        console.log("Ultrathink Audio Engine: STARTED");

        Tone.Transport.bpm.value = 128;
        this.isInitialized = true;
    }

    // --- TRACKS ---

    public createTrack(name: string): TrackChannel {
        const id = crypto.randomUUID();
        const track = new TrackChannel(id, name);
        this.tracks.set(id, track);
        return track;
    }

    public getTrack(id: string): TrackChannel | undefined {
        return this.tracks.get(id);
    }

    public getAllTracks(): TrackChannel[] {
        return Array.from(this.tracks.values());
    }

    // --- TRANSPORT ---

    public startTransport() {
        Tone.Transport.start();
    }

    public stopTransport() {
        Tone.Transport.stop();
    }

    public setBpm(bpm: number) {
        Tone.Transport.bpm.value = bpm;
    }
}

export const engine = AudioEngine.getInstance();
