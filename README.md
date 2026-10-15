# ⛺ Cozy Camping — Interactive 3D Diorama

A stylized low-poly camping diorama that runs in the browser. Orbit around the camp,
click the **tent**, **campfire** and **lantern**, then play with day / sunset / night,
rain, procedural ambience and a photo mode — all rendered in real time.

Built with **React + Vite + React Three Fiber + Three.js + Zustand**.
3D models come from a Blender → GLB pipeline included in this repo.

[![React](https://img.shields.io/badge/React-19-61dafb?logo=react&logoColor=06191f)](https://react.dev)
[![Three.js](https://img.shields.io/badge/Three.js-r186-black?logo=three.js)](https://threejs.org)
[![Vite](https://img.shields.io/badge/Vite-8-646cff?logo=vite&logoColor=white)](https://vite.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

## ✨ Live demo / deploy

This is a static SPA — `bun run build` outputs `dist/`, deployable anywhere.
SPA fallback is already configured (`vercel.json` + `public/_redirects`).

| Platform   | How |
| ---------- | --- |
| Vercel     | Import this repo → Framework preset **Vite** → Build `bun run build` (or npm), Output `dist`. `vercel.json` handles `/camping` rewrites. |
| Netlify    | Same build settings, Publish `dist`. `public/_redirects` handles SPA fallback. |
| Cloudflare Pages / any static host | Build command `bun run build`, output `dist`, add an SPA rule `/* → /index.html (200)`. |
| Local preview | `bun run build` then `bun run preview` → http://localhost:5173/camping |

> No environment variables or backend required. All audio is synthesized in-browser (WebAudio), no audio files.

## 🎮 What you can do

- **Orbit / zoom** — drag to orbit (azimuth limited ±60°), scroll or pinch to zoom (8–30 m)
- **Click objects** — tent, campfire and lantern focus the camera and open an info panel (`Esc` closes)
- **Tent flap** — opens / closes on click with a hinged animation
- **Campfire / lantern** — toggle on-off from the 3D click or the panel button
- **Time pills** — Day / Sunset / Night + auto-cycle (Day → Sunset → Night every 16 s)
- **Weather pills** — Clear / Rain (800 instanced drops, 400 on mobile; fire and sky dim with it)
- **Sound pill** — procedural WebAudio: fire crackle + night crickets. Starts muted (no autoplay)
- **Photo mode** — hides all UI and downloads a PNG snapshot of the canvas
- **Header status line** — live clock (`12:00 · day · clear`) reflecting time + weather state

## 🌌 Scene details

| System | Implementation |
| ------ | -------------- |
| Campfire | flame scale/rotation via `useFrame` + flickering `PointLight`, on/off state |
| Lantern | 2 baked GLB clips (swing + glow-pulse) driven by a mixer; emissive + light follow state |
| Environment | day/sunset/night lerp (~2 s): sky, sun, fog + 400 stars + moon |
| Rain | instanced drops + ambient/fog dim |
| Fireflies | 80 GPU points, custom twinkle/drift shader, night-only, dimmed by rain |
| Smoke | 24-point plume above the fire, fades out, thinner in rain |
| Wildlife | 2 hopping rabbits on seeded paths (three.js primitives) |
| Intro | short camera sweep on first load |
| Camera | isometric-ish `(14, 12, 14)`, fov 45, polar clamp, pan off, focus-dolly on select |
| Render | ACES tone mapping (exposure 1.05), PCF soft shadows 2048, hemisphere fill |
| Perf | DPR `[1, 1.5]`, `clone(true)` GLB sharing, preloaded models (~813 KB total) |

## 🛠️ Tech stack

```text
React 19 + TypeScript + Vite 8
three + @react-three/fiber + @react-three/drei
zustand (campfire / lantern / tent / time / weather / selection / photo)
react-router-dom (/ -> /camping)
tailwindcss v4 (@tailwindcss/vite)
```

## 🚀 Quickstart

Requires **Node 22+**. Bun is used below, npm works too.

```bash
bun install
bun run dev      # http://localhost:5173/camping
bun run build    # tsc + vite build -> dist/
bun run preview  # serve dist locally
```

npm equivalents: `npm install`, `npm run dev`, `npm run build`, `npm run preview`.

## 📜 Scripts

| Command | What it does |
| ------- | ------------ |
| `bun run dev` | start Vite dev server |
| `bun run build` | type-check (`tsc -b`) + production build to `dist/` |
| `bun run preview` | serve the production build locally |
| `bun run lint` | oxlint |

## 📁 Project structure

```text
cozy-camping/
  public/
    models/           9 GLB files (~813 KB): ground, pine-tree, tent,
                      campfire, logs, rocks, bush, lantern, meadow
    favicon.svg       tent + campfire icon
    _redirects        Netlify-style SPA fallback (also copied to dist/)
  vercel.json         Vercel SPA rewrite (/(.*) -> /index.html)
  src/
    app/App.tsx       router (/ -> /camping)
    pages/            CampingPage (Canvas + header + panels + controls)
    scenes/camping/   CampingScene (canvas + CameraRig) + models.tsx
                      (GLB loader + Interactive wrapper + fire/lantern + Meadow)
    effects/          Environment (day/night lerp), RainEffect, Fireflies,
                      SmokePlume, Wildlife, SceneIntro,
                      useAmbience (WebAudio synth), useAutoTime (cycle timer)
    components/       LoadingScreen, ObjectPanel, EnvironmentControls, PhotoMode
    stores/           campingStore.ts (zustand + object info)
    lib/              scene-config.ts (camera, focus anchors), asset-config.ts
  camping-assets/     Blender source (camping_scene.blend)
```

## 🎨 Blender → GLB pipeline

Models are authored in Blender with flat-shaded Principled materials,
origin at the base, applied transforms, selected-only export, +Y up.
Lantern keeps its swing + glow-pulse animations.

```bash
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python blender_build/run.py -- all
python tools/validate_glb.py   # 9 files, total must stay under 1.6 MB (target 1.5 MB)
```

Named nodes the code depends on: `Campfire_Flame_Outer` / `Campfire_Flame_Inner`,
`Lantern_Glow`, `Lantern_Pivot`. Renaming them in Blender breaks the scene.

## ⚡ Performance notes

- Total GLB payload ~813 KB, well under the 1.6 MB budget — safe for mobile networks.
- Rain and fireflies scale down on small screens; DPR is capped at 1.5.
- Production JS bundle is ~1.35 MB unminified-gzip (~379 KB gzip); three.js dominates it.
  Further work could code-split the 3D scene behind the loading screen.

## 🌐 Browser support

Any modern evergreen browser with WebGL2: Chrome, Edge, Firefox, Safari 15+.
Audio requires a user gesture (the Sound pill) per autoplay policy.

## 🤝 Contributing

Issues and PRs welcome. For Blender changes, export with the pipeline above and
keep the total GLB size under budget (`tools/validate_glb.py`).

## 📄 License

MIT — see [LICENSE](./LICENSE).
