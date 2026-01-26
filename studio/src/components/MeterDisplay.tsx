import { useRef, useEffect } from 'react';
import { TrackChannel } from '../core/TrackChannel';
import { AudioMeter } from '../core/AudioMeter';

interface MeterProps {
    track: TrackChannel;
}

export default function MeterDisplay({ track }: MeterProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const meterRef = useRef<AudioMeter | null>(null);
    const requestRef = useRef<number>();

    useEffect(() => {
        // Init Meter
        meterRef.current = new AudioMeter(track);

        const animate = () => {
            if (meterRef.current && canvasRef.current) {
                const val = meterRef.current.getValue();
                const ctx = canvasRef.current.getContext('2d');
                if (ctx) {
                    const width = canvasRef.current.width;
                    const height = canvasRef.current.height;

                    // Clear
                    ctx.clearRect(0, 0, width, height);

                    // Draw Background
                    ctx.fillStyle = '#18181b'; // zinc-900
                    ctx.fillRect(0, 0, width, height);

                    // Draw Level
                    const levelHeight = val * height;
                    const gradient = ctx.createLinearGradient(0, height, 0, 0);
                    gradient.addColorStop(0, '#0ea5e9'); // sky-500
                    gradient.addColorStop(0.6, '#a855f7'); // purple-500
                    gradient.addColorStop(1, '#f43f5e'); // rose-500

                    ctx.fillStyle = gradient;
                    ctx.fillRect(0, height - levelHeight, width, levelHeight);
                }
            }
            requestRef.current = requestAnimationFrame(animate);
        };

        requestRef.current = requestAnimationFrame(animate);

        return () => {
            if (requestRef.current) cancelAnimationFrame(requestRef.current);
            meterRef.current?.dispose();
        };
    }, [track]);

    return (
        <canvas
            ref={canvasRef}
            width={12}
            height={160}
            className="rounded border border-zinc-800"
        />
    );
}
