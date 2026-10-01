import { OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import { sceneConfig } from "../../lib/scene-config.ts";
import Environment from "../../effects/Environment.tsx";
import RainEffect from "../../effects/RainEffect.tsx";
import { Bush, Campfire, Ground, Lantern, PineTree, RockSet, Stump, Tent } from "./models.tsx";

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
      <Suspense fallback={null}>
        <Ground />
        {/* focal: tent left-center, front faces camera (+x+z) */}
        <Tent position={[-2.5, 0, -1.5]} rotation-y={-2.35} />
        {/* focal: campfire right-center */}
        <Campfire position={[2.5, 0, 1]} />
        {/* stump seats flanking fire (replaces logs.glb) */}
        <Stump position={[1, 0, 3]} rotation-y={0.5} />
        <Stump position={[4.2, 0, -0.2]} rotation-y={-0.9} />
        {/* lantern on path between tent and fire */}
        <Lantern position={[0.6, 0, 1.8]} />
        {/* back row framing */}
        <PineTree position={[-4, 0, -6.5]} scale={1.2} rotation-y={0.4} />
        <PineTree position={[0.5, 0, -7]} scale={1} rotation-y={2.1} />
        <PineTree position={[4.5, 0, -6]} scale={1.3} rotation-y={1.2} />
        {/* sides */}
        <PineTree position={[-7, 0, -1]} scale={0.9} rotation-y={2.8} />
        <PineTree position={[7, 0, -0.5]} scale={1.1} rotation-y={0.9} />
        {/* front corners, small so they don't block view */}
        <PineTree position={[-6, 0, 5.5]} scale={0.7} rotation-y={2.5} />
        <PineTree position={[6.2, 0, 6]} scale={0.85} rotation-y={0.7} />
        {/* rock piles */}
        <RockSet position={[-4.5, 0, -3.5]} rotation-y={0.6} />
        <RockSet position={[5, 0, 3.5]} rotation-y={2.2} />
        <RockSet position={[-1, 0, 6.2]} rotation-y={1.1} />
        {/* bushes fill gaps */}
        <Bush position={[-5.2, 0, 2]} rotation-y={0.3} />
        <Bush position={[5.5, 0, -3.2]} rotation-y={1.7} />
        <Bush position={[0, 0, 6.5]} rotation-y={2.9} />
        <Bush position={[-3, 0, -6]} rotation-y={1.1} />
      </Suspense>
      <OrbitControls
        makeDefault
        target={[0, 0.8, 0]}
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
