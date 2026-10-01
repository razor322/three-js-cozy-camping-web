import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { timeTiers, useCampingStore, type TimeMode } from "../stores/campingStore.ts";

const skyColors = {
  day: new THREE.Color("#aee2ff"),
  sunset: new THREE.Color("#ff9e5e"),
  night: new THREE.Color("#0d1b3d"),
};

const sunParams: Record<TimeMode, { intensity: number; color: string; position: [number, number, number] }> = {
  day: { intensity: 1.35, color: "#fff4e0", position: [8, 12, 6] },
  sunset: { intensity: 0.8, color: "#ff9e5e", position: [-10, 5, 4] },
  night: { intensity: 0.15, color: "#7a9cc6", position: [-4, 10, -6] },
};

const ambientParams: Record<TimeMode, number> = { day: 0.55, sunset: 0.35, night: 0.12 };
const fogParams: Record<TimeMode, [number, number]> = {
  day: [28, 55],
  sunset: [24, 50],
  night: [18, 42],
};

// ponytail: keyframe lerp rd smoothstep, 1.5s transition — no spring lib for 3 scalar lerps
export default function Environment() {
  const timeMode = useCampingStore((s) => s.timeMode);
  const tier = useRef(0);
  const target = timeTiers[timeMode];
  const ambient = useRef<THREE.AmbientLight>(null);
  const sun = useRef<THREE.DirectionalLight>(null);
  const stars = useMemo(() => makeStars(400), []);

  useFrame((_, dt) => {
    tier.current = THREE.MathUtils.damp(tier.current, target, 2.2, dt);
    const t = THREE.MathUtils.smootherstep(tier.current, 0, 1);
    const dayW = Math.max(0, 1 - t * 2);
    const sunsetW = Math.max(0, 1 - Math.abs(t - 0.5) * 2);
    const nightW = Math.max(0, t * 2 - 1);

    const sky = new THREE.Color("#000000")
      .add(skyColors.day.clone().multiplyScalar(dayW))
      .add(skyColors.sunset.clone().multiplyScalar(sunsetW))
      .add(skyColors.night.clone().multiplyScalar(nightW));

    const scene = ambient.current?.parent as THREE.Scene | undefined;
    const weather = useCampingStore.getState().weather;
    const rainW = weather === "rain" ? 1 : 0;
    const rainDim = 0.4;
    if (scene) {
      (scene.background as THREE.Color)?.copy?.(sky);
      if (scene.fog instanceof THREE.Fog) {
        scene.fog.color.copy(sky);
        const [near, far] = lerpFog(t);
        scene.fog.near = THREE.MathUtils.lerp(near, near * 0.6, rainW);
        scene.fog.far = THREE.MathUtils.lerp(far, far * 0.6, rainW);
      }
    }
    if (ambient.current) {
      ambient.current.intensity = (ambientParams.day * dayW + ambientParams.sunset * sunsetW + ambientParams.night * nightW) * (1 - rainDim * rainW);
    }
    if (sun.current) {
      const tier2 = tier.current;
      sun.current.intensity = lerp3(
        sunParams.day.intensity, sunParams.sunset.intensity, sunParams.night.intensity, tier2
      );
      sun.current.color.copy(
        new THREE.Color(sunParams.day.color).lerp(new THREE.Color(sunParams.sunset.color), Math.min(1, tier2 * 2))
          .lerp(new THREE.Color(sunParams.night.color), Math.max(0, tier2 * 2 - 1))
      );
      sun.current.position.set(...lerpPos(sunParams.day.position, sunParams.sunset.position, sunParams.night.position, tier2));
    }
    const mat = stars.material as THREE.PointsMaterial;
    mat.opacity = nightW * 0.9;
    stars.visible = nightW > 0.02;
  });

  return (
    <>
      <color attach="background" args={["#aee2ff"]} />
      <fog attach="fog" args={["#aee2ff", 28, 55]} />
      <ambientLight ref={ambient} intensity={0.55} />
      <directionalLight
        ref={sun}
        position={[8, 12, 6]}
        intensity={1.35}
        castShadow
        shadow-mapSize={[1024, 1024]}
        shadow-camera-left={-12}
        shadow-camera-right={12}
        shadow-camera-top={12}
        shadow-camera-bottom={-12}
      />
      {/* moon: small emissive disc, visible at night */}
      <mesh position={[-14, 14, -18]}>
        <sphereGeometry args={[1.1, 16, 16]} />
        <meshBasicMaterial color="#f4f1de" toneMapped={false} />
      </mesh>
      <primitive object={stars} />
    </>
  );
}

function makeStars(count: number) {
  const geo = new THREE.BufferGeometry();
  const pos = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const r = 38 + Math.random() * 14;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.random() * Math.PI * 0.45;
    pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    pos[i * 3 + 1] = r * Math.cos(phi) + 4;
    pos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  }
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const mat = new THREE.PointsMaterial({ color: "#ffffff", size: 0.22, transparent: true, opacity: 0, sizeAttenuation: true, depthWrite: false });
  const pts = new THREE.Points(geo, mat);
  pts.visible = false;
  return pts;
}

function lerp3(a: number, b: number, c: number, t: number) {
  return t < 0.5 ? THREE.MathUtils.lerp(a, b, t * 2) : THREE.MathUtils.lerp(b, c, (t - 0.5) * 2);
}

function lerpPos(a: [number, number, number], b: [number, number, number], c: [number, number, number], t: number): [number, number, number] {
  const lerp = (x: number, y: number, z: number) => THREE.MathUtils.lerp(x, y, z);
  return t < 0.5
    ? [lerp(a[0], b[0], t * 2), lerp(a[1], b[1], t * 2), lerp(a[2], b[2], t * 2)]
    : [lerp(b[0], c[0], (t - 0.5) * 2), lerp(b[1], c[1], (t - 0.5) * 2), lerp(b[2], c[2], (t - 0.5) * 2)];
}

function lerpFog(t: number): [number, number] {
  const near = lerp3(fogParams.day[0], fogParams.sunset[0], fogParams.night[0], t);
  const far = lerp3(fogParams.day[1], fogParams.sunset[1], fogParams.night[1], t);
  return [near, far];
}
