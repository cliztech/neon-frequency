import { useState, useEffect, useRef } from 'react';
import ChannelStrip from '../components/ChannelStrip';
import { TrackChannel } from '../core/TrackChannel';

export default function ChannelStripBenchmark() {
    const [count, setCount] = useState(0);
    const [results, setResults] = useState<string[]>([]);
    const startTimeRef = useRef<number>(0);
    const iterations = 1000;

    // Create a stable track instance
    const trackRef = useRef(new TrackChannel('test-track', 'Test Track'));

    useEffect(() => {
        runBenchmark();
    }, []);

    const runBenchmark = () => {
        setResults(prev => [...prev, 'Starting benchmark...']);
        startTimeRef.current = performance.now();

        // Start the update loop
        let i = 0;
        const update = () => {
            if (i < iterations) {
                setCount(c => c + 1);
                i++;
                // Use setTimeout to allow render to happen, or just rely on React batching not optimizing this away?
                // Actually, in React 18, updates inside timeouts are batched.
                // To force distinct updates we might need flushSync, but that's from react-dom.
                // For this simple bench, we just want to see if we can render many times.
                // We'll use requestAnimationFrame to space them out or just a tight loop if possible?
                // A tight loop of state updates will be batched into one render.
                // So we need to chain them.
                setTimeout(update, 0);
            } else {
                const endTime = performance.now();
                const duration = endTime - startTimeRef.current;
                setResults(prev => [...prev, `Benchmark complete: ${iterations} updates in ${duration.toFixed(2)}ms`]);
                setResults(prev => [...prev, `Average time per update: ${(duration / iterations).toFixed(4)}ms`]);
            }
        };

        update();
    };

    return (
        <div className="p-4 bg-black text-white">
            <h1 className="text-xl mb-4">ChannelStrip Benchmark</h1>
            <div className="mb-4">
                Count: {count}
            </div>
            <div className="flex gap-4 mb-4">
                {/* Render multiple strips to amplify impact */}
                {Array.from({ length: 50 }).map((_, i) => (
                    <ChannelStrip key={i} track={trackRef.current} />
                ))}
            </div>
            <div className="font-mono text-sm">
                {results.map((r, i) => (
                    <div key={i}>{r}</div>
                ))}
            </div>
        </div>
    );
}
