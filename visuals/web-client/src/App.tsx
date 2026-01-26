import { Canvas } from '@react-three/fiber';
import ThreeScene from './components/ThreeScene';
import Interface from './components/Interface';

function App() {
    return (
        <div className="w-full h-screen relative bg-dark-bg">
            <Canvas className="absolute inset-0 z-0">
                <ThreeScene />
            </Canvas>
            <Interface />
        </div>
    );
}

export default App;
