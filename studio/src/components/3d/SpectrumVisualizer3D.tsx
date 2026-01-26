import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function SpectrumVisualizer3D() {
    const groupRef = useRef<THREE.Group>(null);
    // Create 16 bars for the visualization
    const bars = Array.from({ length: 16 }, (_, i) => i);

    useFrame((state, delta) => {
        if (!groupRef.current) return;

        // Mock frequency data if engine not running or no analyzer attached yet
        // In real impl, we'd call engine.analyzer.getValue()
        const time = state.clock.getElapsedTime();

        groupRef.current.children.forEach((child, i) => {
            if (child instanceof THREE.Mesh) {
                // Simulating audio reaction with sine waves for now
                const freq = (i + 1) * 0.5;
                // Basic idle animation + simulated reaction
                const scaleY = 1 + Math.sin(time * 5 + i * freq) * 0.5 + Math.cos(time * 3 - i) * 0.3;
                child.scale.y = Math.max(0.1, scaleY);
            }
        });

        // Rotate the ring slowly
        groupRef.current.rotation.y += delta * 0.1;
    });

    return (
        <group ref={groupRef} position={[0, 0, 0]}>
            {bars.map((_, i) => {
                const angle = (i / bars.length) * Math.PI * 2;
                const radius = 4;
                const x = Math.cos(angle) * radius;
                const z = Math.sin(angle) * radius;

                return (
                    <mesh key={i} position={[x, 0, z]} rotation={[0, -angle, 0]}>
                        <boxGeometry args={[0.5, 1, 0.2]} />
                        <meshStandardMaterial
                            color="#22d3ee"
                            emissive="#22d3ee"
                            emissiveIntensity={0.5}
                            roughness={0.2}
                            metalness={0.8}
                        />
                    </mesh>
                );
            })}
        </group>
    );
}
