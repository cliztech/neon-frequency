import * as Tone from 'tone';

export type EffectType = 'reverb' | 'delay' | 'distortion' | 'bitcrusher';

export class EffectRack {
    private input: Tone.Gain;
    private output: Tone.Gain;
    private effects: Map<string, Tone.ToneAudioNode> = new Map();

    constructor() {
        this.input = new Tone.Gain(1);
        this.output = new Tone.Gain(1);

        // Initial chain: Input -> Output
        this.input.connect(this.output);
    }

    /**
     * Connect this rack to a destination node.
     */
    connect(destination: Tone.ToneAudioNode) {
        this.output.connect(destination);
    }

    /**
     * Get the input node for chaining.
     */
    getInput(): Tone.Gain {
        return this.input;
    }

    /**
     * Add an effect to the rack.
     */
    addEffect(id: string, type: EffectType) {
        let effect: Tone.ToneAudioNode;

        switch (type) {
            case 'reverb':
                effect = new Tone.Reverb(1.5).toDestination(); // Auto-generates impulse response
                (effect as Tone.Reverb).wet.value = 0.3;
                break;
            case 'delay':
                effect = new Tone.FeedbackDelay("8n", 0.5);
                break;
            case 'distortion':
                effect = new Tone.Distortion(0.4);
                break;
            case 'bitcrusher':
                effect = new Tone.BitCrusher(4);
                break;
            default:
                console.warn(`Unknown effect type: ${type}`);
                return;
        }

        this.effects.set(id, effect);
        this.rebuildChain();
    }

    /**
     * Remove an effect by ID.
     */
    removeEffect(id: string) {
        const effect = this.effects.get(id);
        if (effect) {
            effect.disconnect();
            effect.dispose();
            this.effects.delete(id);
            this.rebuildChain();
        }
    }

    /**
     * Reconstruct the audio graph chain.
     */
    private rebuildChain() {
        // 1. Disconnect everything
        this.input.disconnect();
        this.effects.forEach(ef => ef.disconnect());

        // 2. Build array of nodes: Input -> [Effects] -> Output
        const nodes = [this.input, ...Array.from(this.effects.values()), this.output];

        // 3. Connect them in series
        for (let i = 0; i < nodes.length - 1; i++) {
            // @ts-ignore - Tone.js types usage
            nodes[i].connect(nodes[i + 1]);
        }
    }
}
