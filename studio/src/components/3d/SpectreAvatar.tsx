import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere } from '@react-three/drei';
import * as THREE from 'three';
import { AvatarProps } from './MozartAvatar';

export default function SpectreAvatar({ position, scale = 1 }: AvatarProps) {
    const pointsRef = useRef<THREE.Points>(null);

    useFrame((state) => {
        if (pointsRef.current) {
            const time = state.clock.getElapsedTime();
            pointsRef.current.rotation.y = -time * 0.1;
            // Simulated glitch effect could go here
        }
    });

    return (
        <group position={position} scale={scale}>
            {/* Core */}
            <Sphere args={[0.8, 32, 32]}>
                <meshStandardMaterial
                    color="#22d3ee" // Cyan
                    emissive="#0891b2"
                    emissiveIntensity={0.8}
                    wireframe
                    transparent
                    opacity={0.3}
                />
            </Sphere>

            {/* Particles (Mocked using Points) */}
            <points ref={pointsRef}>
                <sphereGeometry args={[1.2, 32, 32]} />
                <pointsMaterial
                    color="#67e8f9"
                    size={0.05}
                    transparent
                    opacity={0.6}
                    sizeAttenuation
                />
            </points>
        </group>
    );
}
