import * as Tone from 'tone';
import { EffectRack } from './EffectRack';

export class TrackChannel {
    public id: string;
    public name: string;

    private channel: Tone.Channel;
    private rack: EffectRack;

    constructor(id: string, name: string) {
        this.id = id;
        this.name = name;

        // Native Tone Channel handles Volume, Pan, Solo, Mute logic
        this.channel = new Tone.Channel(0, 0);
        this.channel.toDestination(); // Connects to Master Output

        // Initialize Effect Rack
        this.rack = new EffectRack();

        // Routing: Rack -> Channel -> Master
        // We need to bypass the rack input logic slightly: 
        // Instrument -> Rack.input -> Rack.output -> Channel
        this.rack.connect(this.channel);
    }

    public getInstrumentInput(): Tone.Gain {
        return this.rack.getInput();
    }

    public getOutput(): Tone.Channel {
        return this.channel;
    }

    // --- CONTROLS ---

    public setVolume(db: number) {
        this.channel.volume.rampTo(db, 0.1);
    }

    public setPan(pan: number) {
        // -1 (Left) to 1 (Right)
        this.channel.pan.rampTo(pan, 0.1);
    }

    public toggleMute(muted: boolean) {
        this.channel.mute = muted;
    }

    public toggleSolo(soloed: boolean) {
        this.channel.solo = soloed;
    }

    public isMuted(): boolean {
        return this.channel.mute;
    }

    public isSoloed(): boolean {
        return this.channel.solo;
    }

    // --- EFFECTS ---

    public addEffect(type: any) {
        const id = crypto.randomUUID();
        this.rack.addEffect(id, type);
        return id;
    }
}
