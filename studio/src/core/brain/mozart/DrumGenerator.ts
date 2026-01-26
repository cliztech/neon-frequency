export class DrumGenerator {
    /**
     * Generate a Euclidean rhythm pattern.
     * @param steps Total steps (e.g., 16)
     * @param pulses Number of hits (e.g., 4)
     * @returns Array of booleans (true = hit)
     */
    public generateEuclidean(steps: number, pulses: number): boolean[] {
        const pattern: boolean[] = new Array(steps).fill(false);

        if (pulses >= steps) return new Array(steps).fill(true);
        if (pulses <= 0) return pattern;

        // Bjorklund's algorithm simplified:
        // Distribute pulses as evenly as possible.

        // Add pulse value to each bucket
        let accumulator = 0;
        for (let i = 0; i < steps; i++) {
            accumulator += pulses;
            if (accumulator >= steps) {
                accumulator -= steps;
                pattern[i] = true;
            }
        }

        // Rotate to starting phase (optional, can add 'rotation' param later)
        return pattern;
    }
}
