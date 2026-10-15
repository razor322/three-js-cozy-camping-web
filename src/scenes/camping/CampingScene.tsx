import { OrbitControls } from "@react-three/drei";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { Suspense, useRef } from "react";
import * as THREE from "three";
import { focusAnchors, GROUND_Y, sceneConfig } from "../../lib/scene-config.ts";
import Environment from "../../effects/Environment.tsx";
import Fireflies from "../../effects/Fireflies.tsx";
import RainEffect from "../../effects/RainEffect.tsx";
import SceneIntro from "../../effects/SceneIntro.tsx";
import SmokePlume from "../../effects/SmokePlume.tsx";
import Wildlife from "../../effects/Wildlife.tsx";
import { useCampingStore } from "../../stores/campingStore.ts";
import { Bush, Campfire, Ground, Lantern, Meadow, PineTree, RockSet, Stump, Tent } from "./models.tsx";

const G = GROUND_Y;

// Dollies the orbit pivot toward the selected object, back to home on deselect.
// Keeps the user's orbit angle: only the target point and distance move.
function CameraRig() {
  const selected = useCampingStore((s) => s.selected);
  const controls = useThree((s) => s.controls) as { target: THREE.Vector3; update: () => void } | null;
  const home = sceneConfig.camera.homeTarget;
  const tmp = useRef(new THREE.Vector3());

  useFrame((_, dt) => {
    if (!controls) return;
    const anchor = selected ? focusAnchors[selected].look : null;
    const goal = tmp.current.set(...(anchor ?? home));
    // move the pivot smoothly; OrbitControls keeps its own camera offset
    controls.target.lerp(goal, 1 - Math.pow(0.001, dt));
    controls.update();
  });
  return null;
}

export default function CampingScene() {
  const { camera } = sceneConfig;
  return (
    <Canvas
      shadows
      dpr={[1, 1.5]}
      gl={{ antialias: true, powerPreference: "high-performance" }}
      camera={{ position: camera.position, fov: camera.fov }}
      onCreated={({ gl }) => {
        // ACES keeps highlights (flame, lantern) from clipping to flat white
        // while the low-poly palette stays warm. AgX is flatter; ACES reads cozy.
        gl.toneMapping = THREE.ACESFilmicToneMapping;
        gl.toneMappingExposure = 1.05;
      }}
      className="!fixed !inset-0"
    >
      <SceneIntro />
      <Environment />
      <RainEffect />
      <Fireflies />
      <SmokePlume position={[1.2, G, 1.2]} />
      <Wildlife />
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
        target={sceneConfig.camera.homeTarget}
        minDistance={camera.minDistance}
        maxDistance={camera.maxDistance}
        minPolarAngle={camera.minPolarAngle}
        maxPolarAngle={camera.maxPolarAngle}
        minAzimuthAngle={-Math.PI / 3}
        maxAzimuthAngle={Math.PI / 3}
        enablePan={false}
      />
      <CameraRig />
    </Canvas>
  );
}
