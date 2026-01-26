import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { Suspense } from 'react';
import SpectrumVisualizer3D from './SpectrumVisualizer3D';
import MozartAvatar from './MozartAvatar';
import SpectreAvatar from './SpectreAvatar';

export default function HolographicStage() {
    return (
        <div className="absolute inset-0 z-0 pointer-events-auto">
            <Canvas>
                <PerspectiveCamera makeDefault position={[0, 2, 8]} />
                <OrbitControls
                    enablePan={false}
                    minPolarAngle={Math.PI / 4}
                    maxPolarAngle={Math.PI / 2}
                />

                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} color="#22d3ee" />
                <pointLight position={[-10, 5, 10]} intensity={0.5} color="#d946ef" />

                <Suspense fallback={null}>
                    <SpectrumVisualizer3D />

                    {/* Agents */}
                    <MozartAvatar position={[-3, 1, 0]} />
                    <SpectreAvatar position={[3, 1, 0]} />
                </Suspense>

                {/* Floor Grid */}
                <gridHelper args={[20, 20, 0x333333, 0x111111]} position={[0, -1, 0]} />
            </Canvas>
        </div>
    );
}
