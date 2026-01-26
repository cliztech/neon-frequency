import * as Tone from 'tone';
import { TrackChannel } from '../../TrackChannel';

export class SpectralAnalyzer {
    private fft: Tone.FFT;
    private channel: TrackChannel;

    constructor(channel: TrackChannel, fftSize: number = 1024) {
        this.channel = channel;
        this.fft = new Tone.FFT(fftSize);

        // Connect to channel output
        this.channel.getOutput().connect(this.fft);
    }

    public getFrequencyData(): Float32Array {
        return this.fft.getValue();
    }
}
