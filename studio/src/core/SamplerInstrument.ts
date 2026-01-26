import * as Tone from 'tone';
import { TrackChannel } from './TrackChannel';

export class SamplerInstrument {
    private sampler: Tone.Sampler;
    private channel: TrackChannel;

    constructor(channel: TrackChannel, samples: { [note: string]: string }, baseUrl: string) {
        this.channel = channel;

        this.sampler = new Tone.Sampler({
            urls: samples,
            baseUrl: baseUrl,
            onload: () => {
                console.log(`Sampler loaded for track ${channel.name}`);
            }
        });

        // Connect Sampler -> Track Channel Input
        this.sampler.connect(this.channel.getInstrumentInput());
    }

    public triggerAttackRelease(note: string, duration: string, time?: number) {
        this.sampler.triggerAttackRelease(note, duration, time);
    }
}
