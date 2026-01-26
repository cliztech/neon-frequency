import * as Tone from 'tone';
import { TrackChannel } from './TrackChannel';

export class AudioMeter {
    private meter: Tone.Meter;
    public channel: TrackChannel;

    constructor(channel: TrackChannel) {
        this.channel = channel;
        this.meter = new Tone.Meter();
        this.meter.normalRange = true; // Returns 0-1

        // Connect Channel Output -> Meter
        this.channel.getOutput().connect(this.meter);
    }

    public getValue(): number {
        const val = this.meter.getValue();
        return Array.isArray(val) ? val[0] : val;
    }

    public dispose() {
        this.meter.dispose();
    }
}
