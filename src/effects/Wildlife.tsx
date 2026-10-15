import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { GROUND_Y } from "../lib/scene-config.ts";

type RabbitSpec = {
  x0: number; z0: number; x1: number; z1: number;
  speed: number; phase: number; color: string;
};

// ponytail: two rabbits on straight back-and-forth paths. Primitives only,
// no GLB. frustumCulled left on; they stay inside the frustum.
const RABBITS: RabbitSpec[] = [
  { x0: -4.5, z0: 3.2, x1: -1.5, z1: 5.4, speed: 0.35, phase: 0, color: "#c9b48f" },
  { x0: 4.2, z0: 3.8, x1: 6.4, z1: 1.2, speed: 0.28, phase: 0.5, color: "#b8a07a" },
];

function Rabbit({ spec }: { spec: RabbitSpec }) {
  const group = useRef<THREE.Group>(null);

  const parts = useMemo(
    () => ({
      body: new THREE.SphereGeometry(0.16, 10, 8),
      head: new THREE.SphereGeometry(0.1, 8, 8),
      ear: new THREE.ConeGeometry(0.035, 0.18, 6),
      tail: new THREE.SphereGeometry(0.06, 6, 6),
      mat: new THREE.MeshStandardMaterial({ color: spec.color, roughness: 0.9, flatShading: true }),
    }),
    [spec.color],
  );

  useFrame(({ clock }) => {
    const g = group.current;
    if (!g) return;
    const t = clock.elapsedTime;
    // triangle wave 0..1..0 -> ping-pong along the segment
    const raw = (t * spec.speed + spec.phase) % 2;
    const u = raw < 1 ? raw : 2 - raw;
    const x = THREE.MathUtils.lerp(spec.x0, spec.x1, u);
    const z = THREE.MathUtils.lerp(spec.z0, spec.z1, u);
    const hop = Math.abs(Math.sin(t * 6 + spec.phase * 6)) * 0.09;
    g.position.set(x, GROUND_Y + hop, z);
    g.rotation.y = Math.atan2(spec.x1 - spec.x0, spec.z1 - spec.z0) + (raw < 1 ? 0 : Math.PI);
  });

  return (
    <group ref={group}>
      <mesh geometry={parts.body} material={parts.mat} castShadow />
      <mesh geometry={parts.head} material={parts.mat} position={[0, 0.14, 0.13]} castShadow />
      <mesh geometry={parts.ear} material={parts.mat} position={[-0.04, 0.26, 0.13]} rotation-x={0.2} />
      <mesh geometry={parts.ear} material={parts.mat} position={[0.04, 0.26, 0.13]} rotation-x={0.2} />
      <mesh geometry={parts.tail} material={parts.mat} position={[0, 0.06, -0.15]} />
    </group>
  );
}

export default function Wildlife() {
  return (
    <>
      {RABBITS.map((r, i) => (
        <Rabbit key={i} spec={r} />
      ))}
    </>
  );
}
