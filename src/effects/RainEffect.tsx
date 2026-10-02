import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { useCampingStore } from "../stores/campingStore.ts";

const DESKTOP_COUNT = 800;
const MOBILE_COUNT = 400;
const DROP_LEN = 0.5;
const SPEED = 6; // m/s downward
const AREA = 10; // +/-10 in x/z covers the 18x18 terrain + margin
const TERRAIN_TOP = 0.8; // flat ground top (validated: bbox 0..0.814)
const RAIN_HEIGHT = 15; // spawn at top+15; column centre ~= top+7.5
const WIND_X = 0.06; // spec allows x -0.05..0.1
const WIND_Z = 0.03; // spec allows z 0..0.05

// ponytail: one coarse-pointer check, no resize listener for a toggleable effect
const COUNT =
  typeof window !== "undefined" &&
  (window.matchMedia("(pointer: coarse)").matches || window.innerWidth < 768)
    ? MOBILE_COUNT
    : DESKTOP_COUNT;

export default function RainEffect() {
  const weather = useCampingStore((s) => s.weather);
  const active = weather === "rain";
  const grp = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const geo = useMemo(() => new THREE.CylinderGeometry(0.008, 0.008, 1, 4), []);
  const mat = useMemo(
    () => new THREE.MeshStandardMaterial({ color: "#a0c8f0", roughness: 0.5, transparent: true, opacity: 0 }),
    [],
  );
  const positions = useMemo(() => {
    const a = new Float32Array(COUNT * 2);
    for (let i = 0; i < COUNT; i++) {
      a[i * 2] = Math.random() * 20 - 10;
      a[i * 2 + 1] = Math.random() * 20 - 10;
    }
    return a;
  }, []);

  useFrame((_, dt) => {
    if (!grp.current) return;
    const vis = active ? 1 : 0;
    mat.opacity = THREE.MathUtils.damp(mat.opacity, vis * 0.8, 4, dt);
    grp.current.visible = vis > 0.05;
    if (!grp.current.visible) return;
    const time = performance.now() * 0.001;
    for (let i = 0; i < COUNT; i++) {
      const bx = positions[i * 2];
      const bz = positions[i * 2 + 1];
      // phase grows -> y decreases: velocity.y = -SPEED, wraps top->top+RAIN_HEIGHT
      const phase = (time * SPEED + i * 1.37) % RAIN_HEIGHT;
      const y = TERRAIN_TOP + RAIN_HEIGHT - phase; // y in [0.8, 15.8], never below terrain
      const x = ((bx + WIND_X * time + AREA) % (AREA * 2)) - AREA; // wraps inside +/-10
      const z = ((bz + WIND_Z * time + AREA) % (AREA * 2)) - AREA;
      dummy.position.set(x, y, z);
      dummy.scale.set(1, DROP_LEN, 1);
      dummy.rotation.set(0, 0, 0); // vertical streaks, world-Y fall
      dummy.updateMatrixWorld();
      grp.current.setMatrixAt(i, dummy.matrixWorld);
    }
    grp.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={grp} args={[geo, mat, COUNT]} frustumCulled={false} />
  );
}
