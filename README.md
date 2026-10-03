# Cozy Camping 3D Web

Interactive stylized low-poly camping diorama — React + Vite + React Three Fiber + Three.js + Zustand. Blender assets via GLB.

## Quickstart

```bash
bun install
bun run dev      # http://localhost:5173/camping
bun run build    # tsc + vite build -> dist/
bun run preview  # serve dist locally
```

## Stack

```text
React 19 + TypeScript + Vite 8
three + @react-three/fiber + @react-three/drei
zustand (campfire/lantern/time/weather/selection)
react-router-dom (/ -> /camping)
tailwindcss v4 (@tailwindcss/vite)
```

## Controls

```text
drag        orbit (azimuth limited +-60deg)
scroll      zoom (8-30m)
click       tent / campfire / lantern -> info panel (Esc closes)
panel btn   Turn Fire / Lantern On-Off
pill bar    Day / Sunset / Night + Clear / Rain
```

## 3D features

```text
Campfire    flame scale/rotation useFrame + PointLight flicker + ON/OFF
Lantern     2 baked GLB clips (swing + glow-pulse) via mixer + emissive/light follow state
Environment day/sunset/night lerp (~2s): sky/sun/fog + 400 stars + moon
Rain        800 instanced drops (400 mobile) + ambient/fog dim
Fireflies   80 Points + custom shader (twinkle/drift), night-only, dimmed by rain
Camera      isometric-ish (12,10,12) fov 40, polar clamp, pan off
Perf        DPR [1,1.5], basic shadows 1024, clone(true) sharing, preloaded GLB

## Rebuild assets

```bash
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python blender_build/run.py -- all
python tools/validate_glb.py   # 9 files, total must stay under 1.6MB (target 1.5MB)
```
```

## Project structure

```text
cozy-camping/
  public/models/        9 GLB (~1.24MB total)
    ground, pine-tree, tent, campfire, logs, rocks, bush, lantern, meadow
  src/
    app/App.tsx         router (/ -> /camping)
    pages/              CampingPage (Canvas + header + panels + controls)
    scenes/camping/     CampingScene + models.tsx (loader + Interactive + fire/lantern + Meadow)
    effects/            Environment.tsx (day/night lerp) + RainEffect.tsx + Fireflies.tsx
    components/         LoadingScreen + ObjectPanel + EnvironmentControls
    stores/             campingStore.ts (zustand)
    lib/                scene-config.ts + asset-config.ts
  camping-assets/       Blender source (camping_scene.blend)
  docs/development/     PRD + ROADMAP + ARCHITECTURE
```

## Blender -> GLB pipeline

```text
Blender (flat-shade Principled, origin base, applied transforms)
  -> selected-only export, +Y up, animations where needed
  -> public/models/*.glb (useGLTF + clone(true) + preload)
```

Named nodes the code depends on: `Campfire_Flame_Outer/Inner`, `Lantern_Glow`, `Lantern_Pivot`.

## Deploy

Static SPA — output `dist/`. Host needs SPA fallback (`/camping` -> `index.html`).
