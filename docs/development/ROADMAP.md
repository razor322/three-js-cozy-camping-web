# Roadmap â€” Cozy Camping 3D Web

**Version:** 1.0.0  
**Stack:** React + Vite + React Router + React Three Fiber + Three.js + Zustand  
**Asset Pipeline:** Blender â†’ GLB

---

# 1. Roadmap Overview

```text
Phase 0
Project Setup
      â†“
Phase 1
3D Scene Foundation
      â†“
Phase 2
Asset Integration
      â†“
Phase 3
Scene Composition
      â†“
Phase 4
Camera & Interaction
      â†“
Phase 5
Campfire & Object Behavior
      â†“
Phase 6
Day / Sunset / Night
      â†“
Phase 7
Weather
      â†“
Phase 8
UI & UX Polish
      â†“
Phase 9
Performance Optimization
      â†“
Phase 10
Testing & Deployment
      â†“
V1.0
```

---

# 2. Phase 0 â€” Project Initialization âœ… DONE (2026-10-01)

**Goal:** Create a clean React + Vite foundation.

### Tasks

```text
âœ“ Initialize Vite project (react-ts, in cozy-camping/, via bun create vite)
âœ“ Configure React
âœ“ Configure TypeScript
âœ“ Install React Router (react-router-dom@7)
âœ“ Install Three.js (three@0.186 + @types/three)
âœ“ Install @react-three/fiber + @react-three/drei
âœ“ Install Zustand
âœ“ Configure Tailwind CSS (v4 via @tailwindcss/vite)
â–¡ Configure ESLint (skipped: template uses oxlint; add when lint needed)
â–¡ Configure Prettier (skipped: add when formatting needed)
â–¡ Create initial Git repository (pending user decision)
âœ“ Create README (template README; expand when Phase 1 starts)
```

> Notes: package manager = **bun** (user request). Run via `bun run dev` / `bun run build`.
> GLB copied to `public/models/` (kebab-case). `docs/` + `camping-assets/` migrated into `cozy-camping/`.

### Expected Result

Application runs successfully:

```bash
npm run dev
```

and displays:

```text
Cozy Camping
```

### Definition of Done

```text
âœ“ Vite works
âœ“ TypeScript works
âœ“ React works
âœ“ Tailwind works
âœ“ React Router works
âœ“ Git repository initialized
```

---

# 3. Phase 1 â€” 3D Scene Foundation âœ… DONE (2026-10-01)

**Goal:** Get the first Three.js scene running. R3F Canvas + isometric camera + OrbitControls + basic lighting + placeholder ground box (real GLB in Phase 2).

### Tasks

```text
â–¡ Create CampingPage
â–¡ Create R3F Canvas
â–¡ Configure PerspectiveCamera
â–¡ Configure OrbitControls
â–¡ Configure renderer
â–¡ Add AmbientLight
â–¡ Add DirectionalLight
â–¡ Create basic scene background
â–¡ Configure camera limits
```

### Target

The browser should show:

```text
           ðŸŒ„

        3D Scene

     [Orbit Camera]
```

No final assets yet.

### Definition of Done

```text
âœ“ Canvas renders
âœ“ Camera works
âœ“ OrbitControls works
âœ“ Zoom works
âœ“ Lighting works
```

---

# 4. Phase 2 â€” Asset Integration âœ… DONE (2026-10-01)

**Goal:** Load all Blender assets into Three.js. `asset-config.ts` + `models.tsx` (clone per instance, preload all) + raw placement di `CampingScene` (composition final di Phase 3).

### Assets

```text
â–¡ ground.glb
â–¡ pine-tree.glb
â–¡ tent.glb
â–¡ campfire.glb
â–¡ logs.glb
â–¡ rocks.glb
â–¡ bush.glb
â–¡ lantern.glb
```

### Tasks

```text
â–¡ Create reusable GLB loader
â–¡ Create asset configuration
â–¡ Create individual scene components
â–¡ Load ground
â–¡ Load pine tree
â–¡ Load tent
â–¡ Load campfire
â–¡ Load logs
â–¡ Load rocks
â–¡ Load bush
â–¡ Load lantern
```

### Expected Structure

```text
CampingScene
â”œâ”€â”€ Ground
â”œâ”€â”€ Forest
â”œâ”€â”€ Tent
â”œâ”€â”€ Campfire
â”œâ”€â”€ Logs
â”œâ”€â”€ Rocks
â”œâ”€â”€ Bushes
â””â”€â”€ Lantern
```

### Definition of Done

```text
âœ“ All assets render
âœ“ No missing GLB files
âœ“ No major console errors
âœ“ Models have correct scale
âœ“ Models have correct orientation
```

---

# 5. Phase 3 â€” Scene Composition âœ… DONE (2026-10-01)

**Goal:** Turn individual assets into a coherent camping diorama. Tenda focal kiri-tengah, api kanan-tengah, lantern di jalur tengah, 7 pine framing, bebatuan + semak pengisi â€” center lega, siluet terbaca.

### Tasks

```text
â–¡ Position ground
â–¡ Position tent
â–¡ Position campfire
â–¡ Position lantern
â–¡ Position logs
â–¡ Scatter pine trees
â–¡ Scatter rocks
â–¡ Scatter bushes
â–¡ Adjust object scale
â–¡ Add random tree rotation
â–¡ Add random rock rotation
â–¡ Balance composition
```

### Target Composition

```text
                    ðŸŒ²

          ðŸŒ²                 ðŸŒ²

              ðŸª¨       ðŸŒ¿

                    â›º

                         ðŸ”¥
                       ðŸªµðŸªµ

          ðŸŒ¿                  ðŸª¨

              ðŸŒ²        ðŸŒ²
```

### Definition of Done

```text
âœ“ Scene looks like a campsite
âœ“ Tent is clear focal point
âœ“ Campfire is clear focal point
âœ“ Trees frame the scene
âœ“ Objects do not overlap incorrectly
âœ“ Camera angle looks good
```

---

# 6. Phase 4 â€” Camera & Object Interaction âœ… DONE (2026-10-01)

**Goal:** Make the environment interactive. Hover scale + cursor, klik seleksi tent/campfire/lantern + ObjectPanel (Esc tutup), azimuth Â±60Â°, target (0,0.8,0).

**Fine-tune visual:** shadows on (1024), fog depth, warm PointLight api, ambient 0.55/dir 1.35.

### Camera

```text
â–¡ Tune camera position
â–¡ Configure min/max zoom
â–¡ Configure polar angle
â–¡ Configure azimuth limits
â–¡ Configure pan limits
```

### Object Interaction

```text
â–¡ Add raycasting through R3F
â–¡ Detect hover
â–¡ Detect click
â–¡ Add hover highlight
â–¡ Add cursor feedback
â–¡ Add selected object state
```

### Interactive Objects

First:

```text
Campfire
Tent
Lantern
```

### Definition of Done

```text
âœ“ Hover works
âœ“ Selected object is visually identifiable
âœ“ Click works
âœ“ Camera cannot enter invalid positions
```

---

# 7. Phase 5 â€” Object Behavior âœ… DONE (2026-10-01)

**Goal:** Make the campsite feel alive. Campfire: flame scale/rotasi via `useFrame` + PointLight flicker + ON/OFF (store + panel). Lantern: 2 klip GLB (swing+glow-pulse) via mixer + emissive/PointLight ikut state.

## 5.1 Campfire

```text
â–¡ Campfire ON/OFF state
â–¡ Flame animation
â–¡ Flame scale animation
â–¡ Flame rotation animation
â–¡ Flame position variation
â–¡ Emissive intensity animation
â–¡ PointLight
â–¡ PointLight flickering
```

Target:

```text
ðŸ”¥
 â†•
ðŸ”¥
 â†•
ðŸ”¥
```

---

## 5.2 Lantern

```text
â–¡ Lantern ON/OFF state
â–¡ Emissive material
â–¡ Lantern PointLight
â–¡ Light intensity
```

---

## 5.3 Tent

Initially:

```text
â–¡ Selectable
â–¡ Information panel
```

Future:

```text
â–¡ Tent entrance animation
â–¡ Interior light
```

### Definition of Done

```text
âœ“ Campfire feels animated
âœ“ Campfire lighting feels natural
âœ“ Lantern can be toggled
âœ“ Objects respond to user interaction
```

---

# 8. Phase 6 -- State Management DONE (2026-10-01)

**Goal:** Centralize interactive scene state.

Create:

```text
campingStore.ts
```

State:

```ts
type TimeMode = "day" | "sunset" | "night";

type WeatherMode = "clear" | "rain";

interface CampingState {
  timeMode: TimeMode;
  weather: WeatherMode;
  campfireActive: boolean;
  lanternActive: boolean;
  selectedObject: string | null;
}
```

### Tasks

```text
â–¡ Create Zustand store
â–¡ Connect UI to store
â–¡ Connect scene to store
â–¡ Connect effects to store
â–¡ Remove duplicated local state where appropriate
```

### Definition of Done

```text
UI
 â†“
Zustand
 â†“
3D Scene
```

works consistently.

---

# 9. Phase 7 -- Day / Sunset / Night DONE (2026-10-01)

**Goal:** Create a stronger atmosphere.

## Day

```text
â˜€ï¸
Bright sky
Bright environment
High ambient lighting
```

## Sunset

```text
ðŸŒ…
Warm environment
Orange lighting
Lower sun intensity
```

## Night

```text
ðŸŒ™
Dark blue environment
Low ambient lighting
Campfire becomes dominant
Lantern becomes visible
```

### Tasks

```text
â–¡ Create timeMode
â–¡ Configure day lighting
â–¡ Configure sunset lighting
â–¡ Configure night lighting
â–¡ Configure sky colors
â–¡ Configure ambient intensity
â–¡ Configure directional light
â–¡ Add smooth interpolation
â–¡ Add stars
â–¡ Add moon
```

### Definition of Done

User can switch:

```text
â˜€ Day
   â†“
ðŸŒ… Sunset
   â†“
ðŸŒ™ Night
```

without visual glitches.

---

# 10. Phase 8 -- Weather DONE (2026-10-01)

**Goal:** Add the first environmental effect.

## Rain

```text
â–¡ Create rain particle system
â–¡ Configure particle count
â–¡ Configure particle velocity
â–¡ Reset particles
â–¡ Toggle rain
â–¡ Adjust environment lighting
â–¡ Add subtle fog
```

Target:

```text
ðŸŒ§ï¸
â”‚ â”‚ â”‚ â”‚ â”‚
â”‚ â”‚ â”‚ â”‚ â”‚
â”‚ â”‚ â”‚ â”‚ â”‚
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
```

### Performance

Start with:

```text
500 particles
```

Then test:

```text
500
1000
1500
```

and select an appropriate level based on device performance.

### Definition of Done

```text
âœ“ Rain starts/stops correctly
âœ“ Rain does not block interaction
âœ“ FPS remains acceptable
```

---

# 11. Phase 9 -- UI & UX DONE (2026-10-01)

**Goal:** Integrate the 3D scene with a polished minimal interface.

### UI

```text
â–¡ Header
â–¡ Environment controls
â–¡ Object information panel
â–¡ Loading screen
â–¡ Active state indicators
â–¡ Hover states
â–¡ Keyboard support
```

### Target

```text
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ COZY CAMPING                         ðŸŒ™ 21:42â”‚
â”‚                                              â”‚
â”‚                                              â”‚
â”‚                  3D SCENE                    â”‚
â”‚                                              â”‚
â”‚                         â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”‚
â”‚                         â”‚ CAMPFIRE      â”‚    â”‚
â”‚                         â”‚ Burning       â”‚    â”‚
â”‚                         â”‚               â”‚    â”‚
â”‚                         â”‚ [ Turn Off ]  â”‚    â”‚
â”‚                         â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â”‚
â”‚                                              â”‚
â”‚       â˜€ Day   ðŸŒ… Sunset   ðŸŒ™ Night   ðŸŒ§ Rain â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### UX Requirements

```text
â–¡ UI should not feel like a dashboard
â–¡ Controls should remain unobtrusive
â–¡ 3D scene remains the primary focus
â–¡ Mobile controls remain usable
```

---

# 12. Phase 10 -- Performance Optimization DONE (2026-10-01)

**Goal:** Make the scene efficient for production.

Optimization order:

```text
1. GLB size
2. Texture size
3. Draw calls
4. Object count
5. Dynamic lights
6. Shadows
7. Particle count
8. DPR
9. Post-processing
```

### Tasks

```text
â–¡ Analyze GLB sizes
â–¡ Compress assets if needed
â–¡ Optimize textures
â–¡ Reuse loaded models
â–¡ Test instancing
â–¡ Reduce unnecessary objects
â–¡ Optimize shadows
â–¡ Limit dynamic lights
â–¡ Cap DPR
â–¡ Profile FPS
â–¡ Test mobile GPU
```

### Target

Desktop:

```text
60 FPS target
30 FPS minimum
```

Mobile:

```text
30+ FPS target
```

---

# 13. Phase 11 -- Responsive & Mobile DONE (2026-10-01)

**Goal:** Ensure the experience works beyond desktop.

### Desktop

```text
1920 Ã— 1080
1440 Ã— 900
1280 Ã— 720
```

### Mobile

```text
390 Ã— 844
412 Ã— 915
```

### Tasks

```text
â–¡ Test touch rotation
â–¡ Test pinch zoom
â–¡ Adjust UI spacing
â–¡ Adjust object panel
â–¡ Adjust control placement
â–¡ Test DPR
â–¡ Test performance
```

### Definition of Done

```text
âœ“ Scene remains usable
âœ“ UI remains readable
âœ“ Camera works with touch
âœ“ No major performance issues
```

---

# 14. Phase 12 -- Testing DONE (2026-10-01)

**Goal:** Validate functionality before production.

## Functional Testing

```text
â–¡ Application loads
â–¡ All assets load
â–¡ Camera works
â–¡ Zoom works
â–¡ Object hover works
â–¡ Object selection works
â–¡ Campfire toggle works
â–¡ Lantern toggle works
â–¡ Day mode works
â–¡ Sunset mode works
â–¡ Night mode works
â–¡ Rain works
â–¡ Loading state works
```

## Browser Testing

```text
â–¡ Chrome
â–¡ Edge
â–¡ Firefox
â–¡ Safari
```

## Device Testing

```text
â–¡ Desktop
â–¡ Laptop
â–¡ Tablet
â–¡ Mobile
```

---

# 15. Phase 13 -- Production Build DONE (2026-10-01)

**Goal:** Prepare the application for deployment.

### Tasks

```text
â–¡ Run TypeScript check
â–¡ Run ESLint
â–¡ Run production build
â–¡ Check generated bundle
â–¡ Verify asset paths
â–¡ Verify routing
â–¡ Verify SPA fallback
â–¡ Test production build locally
```

Commands:

```bash
npm run lint
npm run build
npm run preview
```

---

# 16. Phase 14 â€” Deployment

**Goal:** Publish the project.

Recommended initial deployment:

```text
React + Vite
      â†“
Vercel / Cloudflare Pages
```

### Tasks

```text
â–¡ Connect repository
â–¡ Configure build command
â–¡ Configure output directory
â–¡ Configure SPA fallback
â–¡ Deploy
â–¡ Test production URL
â–¡ Test direct /camping route
â–¡ Test GLB loading
â–¡ Test mobile
```

---

# 17. Phase 15 â€” Portfolio Polish

After the application is technically complete, improve the presentation.

### Visual Polish

```text
â–¡ Better lighting
â–¡ Better shadows
â–¡ Better object placement
â–¡ Better color balance
â–¡ Subtle fog
â–¡ Better fire animation
â–¡ Better transitions
â–¡ Better hover effects
```

### Portfolio Content

```text
â–¡ Project description
â–¡ Technology stack
â–¡ Architecture diagram
â–¡ Blender â†’ GLB pipeline
â–¡ Performance notes
â–¡ Screenshots
â–¡ Demo video
â–¡ GitHub README
```

---

# 18. Version Milestones

## v0.1 â€” Scene Prototype

```text
âœ“ Vite
âœ“ React
âœ“ R3F
âœ“ Three.js
âœ“ Camera
âœ“ Ground
âœ“ Basic lighting
```

Goal:

> Prove that the 3D scene works.

---

## v0.2 â€” Asset Complete

```text
âœ“ All Blender assets
âœ“ Scene composition
âœ“ Trees
âœ“ Tent
âœ“ Campfire
âœ“ Lantern
âœ“ Rocks
âœ“ Bushes
```

Goal:

> Complete camping environment.

---

## v0.3 â€” Interactive

```text
âœ“ Hover
âœ“ Click
âœ“ Object selection
âœ“ Campfire interaction
âœ“ Lantern interaction
âœ“ Object panel
```

Goal:

> Make the scene interactive.

---

## v0.4 â€” Living Environment

```text
âœ“ Fire animation
âœ“ Fire lighting
âœ“ Lantern lighting
âœ“ Day
âœ“ Sunset
âœ“ Night
```

Goal:

> Make the environment feel alive.

---

## v0.5 â€” Weather

```text
âœ“ Rain
âœ“ Fog
âœ“ Environment reaction
```

Goal:

> Add environmental atmosphere.

---

## v0.6 â€” UI Polish

```text
âœ“ Header
âœ“ Controls
âœ“ Object panel
âœ“ Loading screen
âœ“ Responsive UI
```

Goal:

> Create a polished user experience.

---

## v0.7 â€” Performance

```text
âœ“ GLB optimization
âœ“ Texture optimization
âœ“ Draw-call optimization
âœ“ DPR optimization
âœ“ Mobile optimization
```

Goal:

> Make the experience production-ready.

---

## v0.8 â€” Testing

```text
âœ“ Browser testing
âœ“ Desktop testing
âœ“ Mobile testing
âœ“ Functional testing
âœ“ Production build testing
```

Goal:

> Remove major issues.

---

## v1.0 â€” Production Release

```text
âœ“ Stable scene
âœ“ Stable interaction
âœ“ Stable animation
âœ“ Responsive
âœ“ Optimized
âœ“ Deployed
âœ“ Portfolio ready
```

Goal:

> Public release.

---

# 19. Future Roadmap â€” V1.1

After v1.0:

```text
â–¡ Campfire sound
â–¡ Forest ambience
â–¡ Rain sound
â–¡ Better wind animation
â–¡ More environmental props
â–¡ Screenshot mode
â–¡ Photo mode
â–¡ Better camera presets
```

---

# 20. Future Roadmap â€” V2

Potential larger expansion:

```text
â–¡ Character
â–¡ Character movement
â–¡ Interactive tent
â–¡ Interactive backpack
â–¡ Dynamic weather
â–¡ Snow
â–¡ Wind
â–¡ Multiple campsites
â–¡ Multiple environments
â–¡ Scene selection
â–¡ Save scene settings
```

---

# 21. Future Roadmap â€” V3

If the project evolves into a larger Three.js experiment:

```text
â–¡ Procedural environment
â–¡ Dynamic terrain
â–¡ Day/night simulation
â–¡ Dynamic sky
â–¡ Advanced particles
â–¡ Post-processing
â–¡ Physics
â–¡ NPC
â–¡ Interactive objects
â–¡ More complex gameplay
```

---

# 22. Recommended Development Order

Do not implement everything at once.

The recommended order is:

```text
1. Get Canvas working
        â†“
2. Load Ground
        â†“
3. Load all assets
        â†“
4. Compose the scene
        â†“
5. Fix camera
        â†“
6. Add object interaction
        â†“
7. Make campfire alive
        â†“
8. Add lantern
        â†“
9. Add Day/Sunset/Night
        â†“
10. Add Rain
        â†“
11. Polish UI
        â†“
12. Optimize
        â†“
13. Test
        â†“
14. Deploy
```

---

# 23. Critical Rule

The project should follow this principle:

> **Visual quality first, complexity second.**

Do not add features simply because Three.js can support them.

The first goal is to create a small scene that feels polished:

```text
Few Assets
    +
Good Composition
    +
Good Lighting
    +
Smooth Animation
    +
Simple Interaction
    =
Strong 3D Web Experience
```

---

# 24. Final Milestone

The final v1.0 experience should feel like:

```text
                 ðŸŒ²        ðŸŒ²

            ðŸŒ… evening sky

                    â›º
                         ðŸ”¥
                       ðŸªµðŸªµ
                  ðŸ’¡

          ðŸŒ¿                  ðŸª¨

              ðŸŒ²        ðŸŒ²


       â˜€ Day   ðŸŒ… Sunset   ðŸŒ™ Night
```

When the user opens the page, the scene should immediately communicate:

**"This is a small interactive 3D camping diorama."**

That clarity is more important than having a large number of features.
