import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function SpectrumVisualizer3D() {
    const meshRef = useRef<THREE.InstancedMesh>(null);
    const dummy = useMemo(() => new THREE.Object3D(), []);
    const count = 16;
    const radius = 4;

    useFrame((state, delta) => {
        if (!meshRef.current) return;

        const time = state.clock.getElapsedTime();

        for (let i = 0; i < count; i++) {
            const angle = (i / count) * Math.PI * 2;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;

            // Simulating audio reaction with sine waves for now
            const freq = (i + 1) * 0.5;
            // Basic idle animation + simulated reaction
            const scaleY = 1 + Math.sin(time * 5 + i * freq) * 0.5 + Math.cos(time * 3 - i) * 0.3;

            dummy.position.set(x, 0, z);
            dummy.rotation.set(0, -angle, 0);
            dummy.scale.set(1, Math.max(0.1, scaleY), 1);

            dummy.updateMatrix();
            meshRef.current.setMatrixAt(i, dummy.matrix);
        }
        meshRef.current.instanceMatrix.needsUpdate = true;

        // Rotate the ring slowly
        meshRef.current.rotation.y += delta * 0.1;
    });

    return (
        <instancedMesh ref={meshRef} args={[undefined, undefined, count]} position={[0, 0, 0]}>
            <boxGeometry args={[0.5, 1, 0.2]} />
            <meshStandardMaterial
                color="#22d3ee"
                emissive="#22d3ee"
                emissiveIntensity={0.5}
                roughness={0.2}
                metalness={0.8}
            />
        </instancedMesh>
    );
}
