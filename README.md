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
click       tent / campfire / lantern -> camera focus + info panel (Esc closes)
hover       floating name label on each interactive object
panel btn   Turn Fire / Lantern On-Off
pill bar    Day / Sunset / Night + Auto-cycle + Clear / Rain + Sound on-off
```

## Ambience

```text
Audio       procedural WebAudio synth (fire crackle + night crickets), no files
Default     muted; unmute via the Sound pill (PRD §37 - no autoplay)
Auto cycle  steps Day -> Sunset -> Night every 16s while enabled
```

## 3D features

```text
Campfire    flame scale/rotation useFrame + PointLight flicker + ON/OFF
Lantern     2 baked GLB clips (swing + glow-pulse) via mixer + emissive/light follow state
Environment day/sunset/night lerp (~2s): sky/sun/fog + 400 stars + moon
Rain        800 instanced drops (400 mobile) + ambient/fog dim
Fireflies   80 Points + custom shader (twinkle/drift), night-only, dimmed by rain
Smoke       24-point plume above the fire (fades, thinner in rain)
Tent        hinged flap opens/closes on click
Wildlife    2 hopping rabbits on seeded paths (three.js primitives)
Photo       photo mode hides the UI and downloads a PNG of the canvas
Camera      isometric-ish (14,12,14) fov 45, polar clamp, pan off, focus-dolly on select
Render      ACES tone mapping (exposure 1.05), PCF soft shadows 2048, hemi fill light
Perf        DPR [1,1.5], basic shadows, clone(true) sharing, preloaded GLB
```

## Rebuild assets

```bash
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python blender_build/run.py -- all
python tools/validate_glb.py   # 9 files, total must stay under 1.6MB (target 1.5MB)
```
```

## Project structure

```text
cozy-camping/
  public/models/        9 GLB (~813KB total)
    ground, pine-tree, tent, campfire, logs, rocks, bush, lantern, meadow
  src/
    app/App.tsx         router (/ -> /camping)
    pages/              CampingPage (Canvas + header + panels + controls)
    scenes/camping/     CampingScene (canvas + CameraRig) + models.tsx (loader + Interactive + fire/lantern + Meadow)
    effects/            Environment.tsx (day/night lerp) + RainEffect.tsx + Fireflies.tsx
                        useAmbience.ts (WebAudio) + useAutoTime.ts (cycle)
    components/         LoadingScreen + ObjectPanel + EnvironmentControls
    stores/             campingStore.ts (zustand)
    lib/                scene-config.ts (camera, focusAnchors) + asset-config.ts
  camping-assets/       Blender source (camping_scene.blend)
  docs/development/     PRD + ROADMAP + ARCHITECTURE + REPAIR_PLAN
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
