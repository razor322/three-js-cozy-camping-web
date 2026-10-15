import { useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { useCampingStore } from "../stores/campingStore.ts";

const COUNT = 24;

// ponytail: one Points draw call, no texture (soft disc via gl_PointCoord
// falloff). Rises and fades on a phase loop; thinner while it rains.
export default function SmokePlume({ position }: { position: [number, number, number] }) {
  const active = useCampingStore((s) => s.campfireActive);
  const weather = useCampingStore((s) => s.weather);

  const geo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    const pos = new Float32Array(COUNT * 3);
    const seed = new Float32Array(COUNT);
    for (let i = 0; i < COUNT; i++) seed[i] = Math.random();
    g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    g.setAttribute("aSeed", new THREE.BufferAttribute(seed, 1));
    return g;
  }, []);

  const mat = useMemo(
    () =>
      new THREE.ShaderMaterial({
        uniforms: {
          uTime: { value: 0 },
          uOpacity: { value: 0 },
          uSize: { value: 90 },
          uColor: { value: new THREE.Color("#9aa3ad") },
        },
        vertexShader: `
          attribute float aSeed;
          uniform float uTime;
          uniform float uSize;
          varying float vFade;
          void main() {
            float life = fract(uTime * 0.14 + aSeed);
            float rise = life * 2.6;
            float sway = sin(uTime * 0.5 + aSeed * 30.0) * 0.18 * life;
            vec3 p = position;
            p.y += rise;
            p.x += sway;
            p.z += sway * 0.6;
            vFade = (1.0 - life) * smoothstep(0.0, 0.15, life);
            vec4 mv = modelViewMatrix * vec4(p, 1.0);
            gl_PointSize = uSize * (0.3 + life) * (10.0 / -mv.z);
            gl_Position = projectionMatrix * mv;
          }
        `,
        fragmentShader: `
          uniform vec3 uColor;
          uniform float uOpacity;
          varying float vFade;
          void main() {
            float d = length(gl_PointCoord - 0.5);
            float disc = smoothstep(0.5, 0.15, d);
            gl_FragColor = vec4(uColor, disc * vFade * uOpacity * 0.35);
          }
        `,
        transparent: true,
        depthWrite: false,
      }),
    [],
  );

  const ref = useRef<THREE.Points>(null);
  useFrame(({ clock }, dt) => {
    if (ref.current) ref.current.visible = mat.uniforms.uOpacity.value > 0.02;
    mat.uniforms.uTime.value = clock.elapsedTime;
    const wet = weather === "rain" ? 0.4 : 1;
    const target = active ? 0.9 * wet : 0;
    mat.uniforms.uOpacity.value = THREE.MathUtils.damp(mat.uniforms.uOpacity.value, target, 2, dt);
  });

  return <points ref={ref} position={position} geometry={geo} material={mat} frustumCulled={false} />;
}
