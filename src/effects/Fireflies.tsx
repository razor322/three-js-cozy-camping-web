import { useFrame } from "@react-three/fiber";
import { useMemo } from "react";
import * as THREE from "three";
import { useCampingStore } from "../stores/campingStore.ts";

const COUNT = 80;
const GROUND_TOP = 0.8;

// ponytail: skills threejs-geometry (Points + BufferGeometry) + threejs-shaders
// (time uniform, gl_PointCoord sprite). No new deps.
export default function Fireflies() {
  const timeMode = useCampingStore((s) => s.timeMode);
  const weather = useCampingStore((s) => s.weather);

  const geo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    const pos = new Float32Array(COUNT * 3);
    const phase = new Float32Array(COUNT);
    for (let i = 0; i < COUNT; i++) {
      pos[i * 3] = Math.random() * 16 - 8;
      pos[i * 3 + 1] = GROUND_TOP + 0.3 + Math.random() * 2.2;
      pos[i * 3 + 2] = Math.random() * 14 - 7;
      phase[i] = Math.random();
    }
    g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    g.setAttribute("aPhase", new THREE.BufferAttribute(phase, 1));
    return g;
  }, []);

  const mat = useMemo(
    () =>
      new THREE.ShaderMaterial({
        uniforms: {
          uTime: { value: 0 },
          uOpacity: { value: 0 },
          uSize: { value: 26 },
          uColor: { value: new THREE.Color("#d8ff7a") },
        },
        vertexShader: `
          attribute float aPhase;
          uniform float uTime;
          uniform float uSize;
          varying float vTwinkle;
          void main() {
            vec4 mv = modelViewMatrix * vec4(position, 1.0);
            mv.x += sin(uTime * 0.6 + aPhase * 12.0) * 0.25;
            mv.y += sin(uTime * 0.8 + aPhase * 20.0) * 0.15;
            float tw = 0.5 + 0.5 * sin(uTime * 2.0 + aPhase * 6.2831);
            vTwinkle = tw;
            gl_PointSize = uSize * (0.4 + tw) * (14.0 / -mv.z);
            gl_Position = projectionMatrix * mv;
          }
        `,
        fragmentShader: `
          uniform vec3 uColor;
          uniform float uOpacity;
          varying float vTwinkle;
          void main() {
            float d = length(gl_PointCoord - 0.5);
            float disc = smoothstep(0.5, 0.05, d);
            gl_FragColor = vec4(uColor, disc * vTwinkle * uOpacity);
          }
        `,
        transparent: true,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      }),
    [],
  );

  useFrame(({ clock }, dt) => {
    mat.uniforms.uTime.value = clock.elapsedTime;
    const base = timeMode === "night" ? 1 : timeMode === "sunset" ? 0.25 : 0;
    const target = weather === "rain" ? base * 0.4 : base;
    mat.uniforms.uOpacity.value = THREE.MathUtils.damp(mat.uniforms.uOpacity.value, target, 3, dt);
  });

  return <points geometry={geo} material={mat} frustumCulled={false} />;
}
