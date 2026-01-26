import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Icosahedron, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';

export interface AvatarProps {
    position: [number, number, number];
    scale?: number;
}

export default function MozartAvatar({ position, scale = 1 }: AvatarProps) {
    const meshRef = useRef<THREE.Mesh>(null);

    useFrame((state) => {
        if (meshRef.current) {
            const time = state.clock.getElapsedTime();
            // Gentle floating and rotation
            meshRef.current.position.y = position[1] + Math.sin(time) * 0.1;
            meshRef.current.rotation.x = time * 0.2;
            meshRef.current.rotation.y = time * 0.3;
        }
    });

    return (
        <group position={position} scale={scale}>
            <Icosahedron args={[1, 0]} ref={meshRef}>
                <MeshDistortMaterial
                    color="#f472b6" // Pink/Rose
                    emissive="#ec4899"
                    emissiveIntensity={0.5}
                    roughness={0.1}
                    metalness={0.8}
                    distort={0.3}
                    speed={2}
                />
            </Icosahedron>
            {/* Halo Ring */}
            <mesh rotation={[Math.PI / 2, 0, 0]}>
                <torusGeometry args={[1.5, 0.02, 16, 100]} />
                <meshBasicMaterial color="#fce7f3" transparent opacity={0.3} />
            </mesh>
        </group>
    );
}
