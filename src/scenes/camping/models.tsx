import { useGLTF } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { Suspense, useEffect, useMemo, useRef, useState } from "react";
import type { JSX } from "react";
import * as THREE from "three";
import { assets } from "../../lib/asset-config.ts";
import { useCampingStore, type SelectableId } from "../../stores/campingStore.ts";

function hygiene(root: THREE.Object3D) {
  // textureless pipeline: GLB ships M_ mats + vertex colors; keep them, only fix flags
  root.traverse((o) => {
    const mesh = o as THREE.Mesh;
    if (!mesh.isMesh) return;
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    const m = mesh.material as THREE.MeshStandardMaterial | THREE.MeshStandardMaterial[];
    const mats = Array.isArray(m) ? m : [m];
    for (const mat of mats) {
      if (!mat || !("roughness" in mat)) continue;
      const n = (mat.name || "").toLowerCase();
      if (n.includes("pine") || n.includes("bush") || n.includes("foliage") ||
        n.includes("rock") || n.includes("stone") || n.includes("flame")
      ) {
        if (!mat.flatShading) {
          mat.flatShading = true;
          mat.needsUpdate = true;
        }
      }
    }
  });
}

function findNode(root: THREE.Object3D, names: string[]): THREE.Object3D | null {
  let hit: THREE.Object3D | null = null;
  root.traverse((o) => {
    if (!hit && names.includes(o.name)) hit = o;
  });
  return hit;
}

function Model({ url, ...props }: { url: string } & JSX.IntrinsicElements["group"]) {
  const { scene } = useGLTF(url);
  // ponytail: clone(true) shares geometries/materials across instances
  const obj = useMemo(() => {
    const c = scene.clone(true);
    hygiene(c);
    return c;
  }, [scene]);
  return <primitive object={obj} {...props} />;
}

function Loader({ url, children }: { url: string; children: (url: string) => React.ReactNode }) {
  return <Suspense fallback={null}>{children(url)}</Suspense>;
}

function Interactive({
  objectId,
  children,
  ...props
}: { objectId: SelectableId; children: React.ReactNode } & Omit<
  JSX.IntrinsicElements["group"],
  "id"
>) {
  const group = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);
  const selected = useCampingStore((s) => s.selected === objectId);
  const select = useCampingStore((s) => s.select);

  useEffectCursor(hovered);

  useFrame((_, dt) => {
    const g = group.current;
    if (!g) return;
    const target = selected ? 1.06 : hovered ? 1.03 : 1;
    const s = THREE.MathUtils.damp(g.scale.x, target, 12, dt);
    g.scale.setScalar(s);
  });

  return (
    <group
      ref={group}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
      }}
      onPointerOut={() => setHovered(false)}
      onClick={(e) => {
        e.stopPropagation();
        select(selected ? null : objectId);
      }}
      {...props}
    >
      {children}
    </group>
  );
}

function useEffectCursor(hovered: boolean) {
  // ponytail: tiny helper inline vs separate file
  useEffect(() => {
    if (typeof document !== "undefined") {
      document.body.style.cursor = hovered ? "pointer" : "auto";
    }
  }, [hovered]);
}

export function Ground(props: JSX.IntrinsicElements["group"]) {
  return (
    <Loader url={assets.ground}>{(url) => <Model url={url} {...props} />}</Loader>
  );
}

export function PineTree({
  scale = 1,
  ...props
}: { scale?: number } & JSX.IntrinsicElements["group"]) {
  return (
    <Loader url={assets.pineTree}>
      {(url) => <Model url={url} scale={scale} {...props} />}
    </Loader>
  );
}

export function Tent(props: JSX.IntrinsicElements["group"]) {
  return (
    <Loader url={assets.tent}>
      {(url) => (
        <Interactive objectId="tent" {...props}>
          <Model url={url} />
        </Interactive>
      )}
    </Loader>
  );
}

export function Campfire(props: JSX.IntrinsicElements["group"]) {
  return (
    <Loader url={assets.campfire}>
      {(url) => <CampfireInner url={url} {...props} />}
    </Loader>
  );
}

function CampfireInner({ url, ...props }: { url: string } & JSX.IntrinsicElements["group"]) {
  const { scene } = useGLTF(url);
  const { scene: rockScene } = useGLTF(assets.rocks);
  const active = useCampingStore((s) => s.campfireActive);
  const group = useRef<THREE.Group>(null);
  const light = useRef<THREE.PointLight>(null);
  const flames = useMemo(() => {
    const c = scene.clone(true);
    hygiene(c);
    const outer = findNode(c, ["Campfire_Flame_Outer"]);
    const mid = findNode(c, ["Campfire_Flame_Mid"]);
    const inner = findNode(c, ["Campfire_Flame_Inner"]);
    // ponytail: baked Campfire_Rocks removed at source; stones come from rocks.glb
    return { root: c, outer, mid, inner };
  }, [scene]);

  const stones = useMemo(() => {
    const src = findNode(rockScene, ["Rock_Small"]);
    if (!src) return null;
    const g = new THREE.Group();
    const N = 7;
    for (let i = 0; i < N; i++) {
      const s = src.clone(true);
      const a = (i / N) * Math.PI * 2;
      s.position.set(Math.cos(a) * 0.75, 0, Math.sin(a) * 0.75);
      s.rotation.y = a * 1.7;
      s.scale.setScalar(0.9 + (i % 3) * 0.12);
      g.add(s);
    }
    hygiene(g);
    return g;
  }, [rockScene]);

  useFrame(({ clock }, dt) => {
    const t = clock.elapsedTime;
    if (flames.outer) {
      flames.outer.visible = active;
      flames.outer.scale.set(1 + Math.sin(t * 9) * 0.06, 1 + Math.sin(t * 11) * 0.14, 1 + Math.cos(t * 9) * 0.06);
      flames.outer.rotation.y = Math.sin(t * 3) * 0.25;
    }
    if (flames.mid) {
      flames.mid.visible = active;
      flames.mid.scale.set(
        1 + Math.sin(t * 10.5 + 1) * 0.07,
        1 + Math.sin(t * 12 + 2) * 0.16,
        1 + Math.cos(t * 10.5) * 0.07,
      );
      flames.mid.rotation.y = -Math.sin(t * 3.5 + 1) * 0.28;
    }
    if (flames.inner) {
      flames.inner.visible = active;
      flames.inner.scale.set(1 + Math.cos(t * 12) * 0.08, 1 + Math.sin(t * 13 + 1) * 0.18, 1 + Math.sin(t * 12) * 0.08);
      flames.inner.rotation.y = -Math.sin(t * 4) * 0.3;
    }
    if (light.current) {
      const target = active ? 6 + Math.sin(t * 10) * 1.2 + Math.sin(t * 23) * 0.6 : 0;
      light.current.intensity = THREE.MathUtils.damp(light.current.intensity, target, 10, dt);
    }
  });

  return (
    <Interactive objectId="campfire" {...props}>
      <group ref={group}>
        <primitive object={flames.root} />
        {stones && <primitive object={stones} />}
        <pointLight ref={light} position={[0, 1.2, 0]} intensity={6} color="#ff9a3c" distance={9} />
      </group>
    </Interactive>
  );
}

export function RockSet(props: JSX.IntrinsicElements["group"]) {
  return (
    <Loader url={assets.rocks}>{(url) => <Model url={url} {...props} />}</Loader>
  );
}

// ponytail: stump seat from stump.glb (M_Bark + M_LogEnd)
export function Stump(props: JSX.IntrinsicElements["group"]) {
  return (
    <Loader url={assets.stump}>{(url) => <Model url={url} {...props} />}</Loader>
  );
}

export function Bush(props: JSX.IntrinsicElements["group"]) {
  return (
    <Loader url={assets.bush}>{(url) => <Model url={url} {...props} />}</Loader>
  );
}

export function Lantern(props: JSX.IntrinsicElements["group"]) {
  return (
    <Loader url={assets.lantern}>
      {(url) => <LanternInner url={url} {...props} />}
    </Loader>
  );
}

function LanternInner({ url, ...props }: { url: string } & JSX.IntrinsicElements["group"]) {
  const { scene, animations } = useGLTF(url);
  const active = useCampingStore((s) => s.lanternActive);
  const group = useRef<THREE.Group>(null);
  const light = useRef<THREE.PointLight>(null);
  const glowMat = useRef<THREE.MeshStandardMaterial | null>(null);
  const root = useMemo(() => {
    const c = scene.clone(true);
    c.traverse((o) => {
      if ((o as THREE.Mesh).isMesh) {
        o.castShadow = true;
        o.receiveShadow = true;
      }
      if (o.name === "Lantern_Light") {
        const mesh = o as THREE.Mesh;
        const m = (mesh.material as THREE.MeshStandardMaterial).clone();
        m.emissiveIntensity = 2.8;
        mesh.material = m;
        glowMat.current = m;
      }
    });
    return c;
  }, [scene]);
  const mixer = useMemo(() => new THREE.AnimationMixer(root), [root]);
  const actions = useMemo(
    () => animations.map((clip) => mixer.clipAction(clip, root)),
    [mixer, animations, root],
  );
  const hasClips = actions.length > 0;
  const swing = useRef<THREE.Group>(null);

  useFrame(({ clock }, dt) => {
    const t = clock.elapsedTime;
    if (hasClips) {
      actions.forEach((a) => {
        if (active && !a.isRunning()) a.play();
        if (!active && a.isRunning()) a.stop();
      });
      mixer.update(active ? dt : 0);
    } else if (swing.current) {
      // ponytail: GLB ships no clips â€” procedural swing + glow pulse fallback
      const target = active ? Math.sin(t * 1.8) * 0.12 : 0;
      swing.current.rotation.z = THREE.MathUtils.damp(swing.current.rotation.z, target, 4, dt);
      swing.current.rotation.x = THREE.MathUtils.damp(
        swing.current.rotation.x, active ? Math.sin(t * 1.3 + 1) * 0.06 : 0, 4, dt,
      );
    }
    if (light.current) {
      const target = active ? 3 : 0;
      light.current.intensity = THREE.MathUtils.damp(light.current.intensity, target, 8, dt);
    }
    if (glowMat.current) {
      glowMat.current.emissiveIntensity = THREE.MathUtils.damp(
        glowMat.current.emissiveIntensity,
        active ? 2.8 : 0.15,
        8,
        dt,
      );
    }
  });

  return (
    <Interactive objectId="lantern" {...props}>
      <group ref={group}>
        <group ref={swing}>
          <primitive object={root} />
        </group>
        <pointLight ref={light} position={[0, 0.5, 0]} intensity={3} color="#ffc93c" distance={6} />
      </group>
    </Interactive>
  );
}

Object.values(assets).forEach((url) => useGLTF.preload(url));
