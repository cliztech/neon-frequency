export class ChordGenerator {
    private scales: { [key: string]: string[] } = {
        "C Major": ["C", "D", "E", "F", "G", "A", "B"],
        "A Minor": ["A", "B", "C", "D", "E", "F", "G"],
        "F Lydian": ["F", "G", "A", "B", "C", "D", "E"],
        "G Mixolydian": ["G", "A", "B", "C", "D", "E", "F"]
    };

    /**
     * Generate a chord progression.
     * @param scaleKey The scale to use (e.g., "C Major")
     * @param complexity 1-10
     */
    public generateProgression(scaleKey: string, complexity: number): string[][] {
        const scale = this.scales[scaleKey] || this.scales["C Major"];
        const progression: string[][] = [];

        // Basic I-V-vi-IV progression logic (mockup)
        // In a real system, this would use a Markov chain or rules engine.

        const romanNumerals = [0, 4, 5, 3]; // I, V, vi, IV (index based)

        romanNumerals.forEach(rootIndex => {
            const root = scale[rootIndex % 7];
            const third = scale[(rootIndex + 2) % 7];
            const fifth = scale[(rootIndex + 4) % 7];

            const chord = [root + "3", third + "3", fifth + "3"]; // Add octave

            if (complexity > 5) {
                const seventh = scale[(rootIndex + 6) % 7];
                chord.push(seventh + "3");
            }

            progression.push(chord);
        });

        return progression;
    }
}
