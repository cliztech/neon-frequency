import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, Stars } from '@react-three/drei';
import * as THREE from 'three';

function Core() {
    const meshRef = useRef<THREE.Mesh>(null!);

    useFrame((state) => {
        const t = state.clock.getElapsedTime();
        meshRef.current.rotation.x = t * 0.2;
        meshRef.current.rotation.y = t * 0.3;
    });

    return (
        <group>
            {/* The Central Agent Core */}
            <Sphere ref={meshRef} args={[1.5, 64, 64]} position={[0, 0, 0]}>
                <MeshDistortMaterial
                    color="#00f3ff"
                    emissive="#bc13fe"
                    emissiveIntensity={0.5}
                    wireframe
                    distort={0.4}
                    speed={2}
                    roughness={0}
                />
            </Sphere>

            {/* Inner Glow */}
            <pointLight position={[0, 0, 0]} intensity={2} color="#ff00ff" distance={5} />
        </group>
    );
}

export default function ThreeScene() {
    return (
        <>
            <color attach="background" args={['#050510']} />
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} intensity={1} />

            <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

            <Core />

            {/* Environmental Fog for depth */}
            <fog attach="fog" args={['#050510', 5, 20]} />
        </>
    );
}
