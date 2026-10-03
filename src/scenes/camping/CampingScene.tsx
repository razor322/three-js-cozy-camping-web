import { OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import { sceneConfig } from "../../lib/scene-config.ts";
import Environment from "../../effects/Environment.tsx";
import Fireflies from "../../effects/Fireflies.tsx";
import RainEffect from "../../effects/RainEffect.tsx";
import { Bush, Campfire, Ground, Lantern, Meadow, PineTree, RockSet, Stump, Tent } from "./models.tsx";

// ground flat-top sits at y=0.8 (bbox 0..0.814); props use it as reference
const G = 0.8;

export default function CampingScene() {
  const { camera } = sceneConfig;
  return (
    <Canvas
      shadows="basic"
      dpr={[1, 1.5]}
      gl={{ antialias: true, powerPreference: "high-performance" }}
      camera={{ position: camera.position, fov: camera.fov }}
      className="!fixed !inset-0"
    >
      <Environment />
      <RainEffect />
      <Fireflies />
      <Suspense fallback={null}>
        <Ground />
        <Meadow />
        {/* focal: tent left-center, door faces camera */}
        <Tent position={[-2.6, G, -1.8]} rotation-y={Math.PI} />
        {/* focal: campfire right-center */}
        <Campfire position={[1.2, G, 1.2]} />
        <Lantern position={[-0.7, G, 0.4]} />
        {/* stump seat flanking fire */}
        <Stump position={[2.8, G, -1]} />
        <RockSet position={[2.4, G, 2.6]} />
        <RockSet position={[-4.6, G, -3.2]} />
        {/* bushes fill gaps */}
        <Bush position={[-3.4, G, 1.8]} />
        <Bush position={[5.5, G, -3.2]} />
        <Bush position={[0, G, 6.5]} />
        <Bush position={[-3, G, -6]} />
        {/* back row framing */}
        <PineTree position={[-4, G, -6.5]} scale={1.2} />
        <PineTree position={[0.5, G, -7]} scale={1} />
        <PineTree position={[4.5, G, -6]} scale={1.3} />
        {/* sides */}
        <PineTree position={[-7, G, -1]} scale={0.9} />
        <PineTree position={[7, G, -0.5]} scale={1.1} />
        <PineTree position={[-7, G, 3]} scale={0.8} />
        <PineTree position={[6.5, G, -3.5]} scale={1} />
        {/* front corners, small so they don't block view */}
        <PineTree position={[-6, G, 5.5]} scale={0.7} />
        <PineTree position={[6.2, G, 6]} scale={0.85} />
      </Suspense>
      <OrbitControls
        makeDefault
        target={[0, 0, 0]}
        minDistance={camera.minDistance}
        maxDistance={camera.maxDistance}
        minPolarAngle={camera.minPolarAngle}
        maxPolarAngle={camera.maxPolarAngle}
        minAzimuthAngle={-Math.PI / 3}
        maxAzimuthAngle={Math.PI / 3}
        enablePan={false}
      />
    </Canvas>
  );
}
