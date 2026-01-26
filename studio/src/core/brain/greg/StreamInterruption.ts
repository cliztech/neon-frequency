import { engine } from '../../AudioEngine';

export class StreamInterruption {
    /**
     * Interrupt the stream for a breaking announcement or ad.
     * @param reason The reason for interruption
     * @param duration Approximate duration needed in seconds
     */
    public async interrupt(reason: string, duration: number) {
        console.log(`[Greg] INTERRUPTING STREAM: ${reason}`);

        // 1. Duck the audio (Future: use a Master Bus fader)
        // engine.master.volume.rampTo(-20, 0.5);

        // 2. Pause Transport (if meaningful) or insert audio clip
        engine.stopTransport();

        console.log(`[Greg] Stream paused. Resuming in ${duration}s...`);

        setTimeout(() => {
            console.log("[Greg] Resuming stream...");
            engine.startTransport();
        }, duration * 1000);
    }
}
