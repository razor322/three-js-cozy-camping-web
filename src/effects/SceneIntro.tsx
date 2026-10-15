import { useFrame, useThree } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";
import { sceneConfig } from "../lib/scene-config.ts";

// ponytail: one-shot dolly-in. Runs until done, then yields to OrbitControls.
export default function SceneIntro() {
  const camera = useThree((s) => s.camera);
  const controls = useThree((s) => s.controls) as { update: () => void } | null;
  const start = useRef(new THREE.Vector3());
  const goal = useRef(new THREE.Vector3(...sceneConfig.camera.position));
  const t = useRef(0);
  const done = useRef(false);
  const primed = useRef(false);

  useFrame((_, dt) => {
    if (done.current) return;
    if (!primed.current) {
      start.current.copy(goal.current).multiplyScalar(1.35);
      camera.position.copy(start.current);
      primed.current = true;
    }
    t.current = Math.min(1, t.current + dt / 1.4);
    const e = THREE.MathUtils.smootherstep(t.current, 0, 1);
    camera.position.lerpVectors(start.current, goal.current, e);
    controls?.update();
    if (t.current >= 1) done.current = true;
  });

  return null;
}
