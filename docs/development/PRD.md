# Product Requirements Document (PRD)

# Cozy Camping 3D Web

**Version:** 1.1.0  
**Status:** Ready for Development  
**Type:** Interactive 3D Single Page Application  
**Platform:** Web  
**Primary Stack:** React + Vite + React Router  
**3D Stack:** Three.js + React Three Fiber  
**3D Asset Pipeline:** Blender → GLB

---

# 1. Product Overview

## 1.1 Description

Cozy Camping 3D Web is a lightweight interactive 3D web experience built as a Single Page Application using React and Vite.

The application presents a stylized low-poly camping diorama created from Blender assets and rendered using Three.js through React Three Fiber.

Users can explore the scene, interact with selected objects, control environmental states, and experience simple animations such as a flickering campfire and day/night transitions.

The project is intentionally designed to remain lightweight and focused on client-side rendering.

---

# 2. Product Goals

## 2.1 Primary Goals

1. Build a lightweight interactive 3D web application.
2. Learn and demonstrate Three.js through React Three Fiber.
3. Integrate Blender-created GLB assets into a web application.
4. Implement an isometric-style 3D environment.
5. Implement interactive 3D objects.
6. Implement simple real-time animations.
7. Implement day, sunset, and night environments.
8. Implement basic weather effects.
9. Maintain good WebGL performance.
10. Produce a polished portfolio-quality project.

---

# 3. Non-Goals

The project is NOT intended to be a full game.

The following are out of scope for the initial versions:

- Multiplayer
- Authentication
- Backend API
- Database
- User accounts
- Inventory
- Crafting
- Survival mechanics
- Character controller
- Combat
- Complex physics
- AI
- Procedural world generation
- Large open-world environment
- Game economy
- Server-side rendering

The application is primarily a **client-side interactive 3D experience**.

---

# 4. Target Users

## Primary

Developers, recruiters, clients, and portfolio visitors.

## Secondary

Users who want to explore a small interactive 3D environment.

---

# 5. Core Experience

When the user opens the application:

1. The camping scene loads.
2. A short loading indicator is displayed.
3. The camera presents an isometric-style view.
4. The user can rotate and zoom the scene.
5. Interactive objects respond to hover.
6. Interactive objects can be selected.
7. An information panel appears for selected objects.
8. Users can change time of day.
9. Users can toggle weather.
10. Scene animations continue smoothly.

---

# 6. Visual Direction

## 6.1 Art Style

- Stylized low-poly
- Cozy
- Warm
- Minimal
- Soft geometric shapes
- Handcrafted game environment
- Diorama-like composition
- No photorealism

## 6.2 Color Direction

Primary palette:

```text
Forest Green
Warm Orange
Cream
Muted Brown
Earthy Gray
Dark Blue
Warm Yellow
```

The tent uses:

```text
Outer canopy: Warm Orange
Inner tent: Cream
Trim: Dark Brown
```

The campfire uses:

```text
Outer flame: Orange
Inner flame: Yellow
```

---

# 7. Technical Architecture

The application uses a lightweight client-side architecture.

```text
Browser
   │
   ▼
Vite
   │
   ▼
React SPA
   │
   ├── React Router
   │
   ├── Zustand
   │
   └── React Three Fiber
          │
          ▼
       Three.js
          │
          ▼
        WebGL
          │
          ▼
       GLB Assets
          ▲
          │
       Blender
```

---

# 8. Technology Stack

## Core

```text
React
TypeScript
Vite
```

## Routing

```text
React Router
```

## 3D

```text
Three.js
@react-three/fiber
@react-three/drei
```

## State Management

```text
Zustand
```

## Styling

```text
Tailwind CSS
```

## Asset Creation

```text
Blender
GLB / glTF
```

---

# 9. Why Vite + React

The application does not require:

- SSR
- Server Components
- Server Actions
- API routes
- Server-side rendering
- Dynamic server data

The primary workload happens inside the browser:

```text
React
  +
Three.js
  +
WebGL
```

Therefore Vite is preferred for:

- Small bundle architecture
- Fast development server
- Fast HMR
- Simple production build
- Static deployment
- Minimal framework overhead

---

# 10. Routing

React Router will be used to support future expansion.

Initial route:

```text
/
└── /camping
```

Recommended structure:

```text
/
├── /camping
├── /about
└── /experiments
```

However, the initial MVP only requires:

```text
/camping
```

The application may redirect `/` to `/camping`.

---

# 11. 3D Assets

The following Blender assets are already completed:

```text
ground.glb
pine-tree.glb
tent.glb
campfire.glb
logs.glb
rocks.glb
bush.glb
lantern.glb
```

Recommended public structure:

```text
public/
└── models/
    ├── ground.glb
    ├── pine-tree.glb
    ├── tent.glb
    ├── campfire.glb
    ├── logs.glb
    ├── rocks.glb
    ├── bush.glb
    └── lantern.glb
```

---

# 12. Ground

Ground specification:

```text
Shape: Rounded Square
Size: approximately 18m × 18m
Type: Low-poly terrain platform
Center: Mostly flat
Edges: Slight terrain variation
```

The center must remain sufficiently flat for:

- Tent
- Campfire
- Lantern
- Logs

---

# 13. Pine Tree

Only one base asset is required:

```text
pine-tree.glb
```

Three.js will generate visual variations through scale:

```text
Small:
scale = 0.7

Medium:
scale = 1.0

Large:
scale = 1.3
```

Optional random rotation and slight scale variation can prevent visual repetition.

---

# 14. Campfire

Campfire asset:

```text
campfire.glb
```

Structure:

```text
Campfire
├── Rocks
├── Logs
└── Campfire_Flame
```

The flame is a static low-poly emissive mesh.

Three.js is responsible for:

- Flame animation
- Scale animation
- Rotation animation
- Position variation
- PointLight flickering

No Blender animation is required.

---

# 15. Scene Composition

Recommended composition:

```text
                    🌲

          🌲                 🌲

              🪨       🌿

                    ⛺

                         🔥
                       🪵🪵

          🌿                  🪨

              🌲        🌲
```

The scene should maintain:

- Clear center
- Strong focal points
- Balanced object distribution
- Clear silhouettes
- Enough empty space
- Good depth from the isometric camera

---

# 16. Functional Requirements

## FR-001 — 3D Scene

The application MUST render the camping environment using React Three Fiber.

Required objects:

```text
Ground
Pine Trees
Tent
Campfire
Logs
Rocks
Bushes
Lantern
```

---

## FR-002 — GLB Loading

All Blender assets MUST be loaded as GLB.

Recommended approach:

```tsx
useGLTF("/models/tent.glb")
```

Drei's `useGLTF` SHOULD be used for asset loading.

---

## FR-003 — Camera

The application MUST provide an isometric-style perspective.

Recommended:

```text
PerspectiveCamera
OrbitControls
```

Initial camera should show the entire campsite.

Camera constraints should prevent:

- Flipping upside down
- Going below the ground
- Excessive zoom
- Excessive panning

---

## FR-004 — Object Hover

Interactive objects MUST provide visual feedback.

Possible implementation:

```text
Hover
 ↓
Subtle scale
+
Emissive/highlight
+
Cursor change
```

The effect should remain subtle.

---

## FR-005 — Object Selection

Interactive objects:

```text
Campfire
Tent
Lantern
```

When selected:

```text
Object
   ↓
Selection State
   ↓
Object Information Panel
```

---

# 17. Campfire Interaction

Campfire states:

```text
ON
OFF
```

ON:

```text
Flame visible
Flame animated
PointLight active
Light flickers
```

OFF:

```text
Flame hidden/inactive
PointLight disabled
Animation disabled
```

---

# 18. Lantern Interaction

Lantern states:

```text
ON
OFF
```

ON:

- Emissive intensity increases.
- PointLight becomes active.

OFF:

- Emissive intensity decreases.
- PointLight becomes inactive.

---

# 19. Fire Animation

Fire animation MUST run on the client using `useFrame`.

Animation properties:

```text
scale
rotation
position
emissive intensity
```

The animation must remain subtle.

Example concept:

```text
scale.y
   ↕
rotation.z
   ↕
position.y
   ↕
```

---

# 20. Lighting

The scene SHOULD use a small number of lights.

Recommended:

```text
AmbientLight
DirectionalLight
Campfire PointLight
Lantern PointLight
```

Dynamic lights MUST be limited to maintain performance.

---

# 21. Day / Sunset / Night

Supported modes:

```text
DAY
SUNSET
NIGHT
```

## Day

```text
Bright ambient
Bright sky
Higher directional light
Campfire less dominant
```

## Sunset

```text
Warm environment
Reduced directional intensity
Warm atmospheric lighting
Campfire becomes more visible
```

## Night

```text
Dark environment
Low ambient lighting
Dark blue environment
Campfire becomes primary light
Lantern becomes more visible
Optional stars
```

---

# 22. Environment Transition

Changing environment mode SHOULD be animated.

Target transition:

```text
1–2 seconds
```

Example:

```text
DAY
 ↓
fade/lerp
 ↓
SUNSET
 ↓
fade/lerp
 ↓
NIGHT
```

Lighting properties should interpolate instead of changing instantly.

---

# 23. Weather

Initial weather modes:

```text
CLEAR
RAIN
```

Rain should be implemented using Three.js particles.

Blender is NOT required for rain.

Recommended initial particle count:

```text
500–1500
```

Adaptive particle count SHOULD be considered for mobile devices.

---

# 24. Rain Effects

When rain is enabled:

```text
Rain particles
+
Slightly darker environment
+
Subtle fog
```

Optional future behavior:

```text
Rain
 ↓
Campfire intensity decreases slightly
 ↓
Ambient sound changes
```

---

# 25. UI

The UI must remain minimal and integrated with the scene.

It MUST NOT look like an admin dashboard.

Example:

```text
┌──────────────────────────────────────────────┐
│ COZY CAMPING                         🌙 21:42│
│                                              │
│                                              │
│                  3D SCENE                    │
│                                              │
│                                              │
│                         ┌───────────────┐    │
│                         │ CAMPFIRE      │    │
│                         │ Burning       │    │
│                         │               │    │
│                         │ [ Turn Off ]  │    │
│                         └───────────────┘    │
│                                              │
│       ☀ Day   🌅 Sunset   🌙 Night   🌧 Rain │
└──────────────────────────────────────────────┘
```

---

# 26. State Management

Zustand will manage global application state.

Example:

```ts
type TimeMode = "day" | "sunset" | "night";

type WeatherMode = "clear" | "rain";

interface CampingState {
  timeMode: TimeMode;
  weather: WeatherMode;

  campfireActive: boolean;
  lanternActive: boolean;

  selectedObject: string | null;

  setTimeMode: (mode: TimeMode) => void;
  setWeather: (weather: WeatherMode) => void;

  toggleCampfire: () => void;
  toggleLantern: () => void;

  selectObject: (id: string | null) => void;
}
```

---

# 27. Project Structure

```text
cozy-camping/
│
├── public/
│   └── models/
│       ├── ground.glb
│       ├── pine-tree.glb
│       ├── tent.glb
│       ├── campfire.glb
│       ├── logs.glb
│       ├── rocks.glb
│       ├── bush.glb
│       └── lantern.glb
│
├── src/
│   │
│   ├── app/
│   │   ├── App.tsx
│   │   └── routes.tsx
│   │
│   ├── scenes/
│   │   └── camping/
│   │       ├── CampingScene.tsx
│   │       ├── Ground.tsx
│   │       ├── Forest.tsx
│   │       ├── Tent.tsx
│   │       ├── Campfire.tsx
│   │       ├── Lantern.tsx
│   │       ├── Rocks.tsx
│   │       ├── Bushes.tsx
│   │       └── Logs.tsx
│   │
│   ├── effects/
│   │   ├── FireEffect.tsx
│   │   ├── RainEffect.tsx
│   │   ├── DayNightEffect.tsx
│   │   └── LightingEffect.tsx
│   │
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── EnvironmentControls.tsx
│   │   ├── ObjectPanel.tsx
│   │   └── LoadingScreen.tsx
│   │
│   ├── stores/
│   │   └── campingStore.ts
│   │
│   ├── lib/
│   │   ├── scene-config.ts
│   │   └── asset-config.ts
│   │
│   ├── styles/
│   │   └── globals.css
│   │
│   └── main.tsx
│
├── index.html
├── vite.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

---

# 28. Routing Structure

Initial:

```text
/
└── /camping
```

Future:

```text
/
├── /camping
├── /about
└── /experiments
```

Example:

```tsx
const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/camping" replace />,
  },
  {
    path: "/camping",
    element: <CampingPage />,
  },
]);
```

---

# 29. Performance Requirements

Performance is a major project requirement.

## Target

Desktop:

```text
Target: 60 FPS
Minimum: 30 FPS
```

Mobile:

```text
Target: 30–60 FPS
```

## Optimization Priorities

Performance optimization priority:

```text
1. GLB file size
2. Texture size
3. Draw calls
4. Number of objects
5. Dynamic lights
6. Shadow quality
7. Particle count
8. Device Pixel Ratio
9. Post-processing
```

The application SHOULD avoid unnecessary heavy post-processing.

---

# 30. Asset Optimization

Before production:

```text
Blender
 ↓
GLB
 ↓
Optimize
 ↓
Web
```

Recommended:

- Low-poly geometry
- Small textures
- Reuse materials
- Avoid duplicate geometry
- Compress GLB where practical
- Use appropriate texture resolution

Repeated objects should reuse the same loaded asset.

---

# 31. Instancing

Repeated environment objects SHOULD use instancing when beneficial.

Candidates:

```text
Pine Trees
Rocks
Bushes
```

Potential architecture:

```text
pine-tree.glb
      ↓
   Instance
      ├── tree 1
      ├── tree 2
      ├── tree 3
      ├── tree 4
      └── tree 5
```

Instancing should be introduced only where it provides measurable benefit.

---

# 32. Device Pixel Ratio

The application SHOULD cap rendering DPR to prevent excessive GPU workload on high-resolution displays.

Example concept:

```tsx
<Canvas
  dpr={[1, 1.5]}
>
```

Exact values should be adjusted based on performance testing.

---

# 33. Responsive Design

Supported desktop sizes:

```text
1920 × 1080
1440 × 900
1280 × 720
```

Supported mobile sizes:

```text
390 × 844
412 × 915
```

Mobile interaction should support:

- Touch rotation
- Pinch zoom
- Object selection
- Environment controls

---

# 34. Loading Experience

The application MUST show a loading state while required 3D assets are loaded.

Example:

```text
COZY CAMPING

Loading...

72%
```

Drei's loading utilities MAY be used.

The loading screen disappears when the required scene assets are ready.

---

# 35. Error Handling

If one GLB fails:

- The application MUST NOT crash entirely.
- The affected object may be hidden.
- The error should be logged during development.
- Other scene objects should continue rendering.

---

# 36. Accessibility

The project is primarily visual but should still support:

- Keyboard-accessible controls
- Accessible button labels
- Visible focus states
- Escape to close object panels
- State indicators that do not rely exclusively on color

---

# 37. Audio

Audio is not part of MVP.

Potential V1.1:

```text
Campfire sound
Forest ambience
Rain sound
```

Audio must have:

- User-controlled volume
- Mute option
- No automatic intrusive playback

---

# 38. Deployment

Because the application is a Vite SPA, production output is static.

Build:

```bash
npm run build
```

Output:

```text
dist/
```

The application can be deployed to:

- Vercel
- Netlify
- Cloudflare Pages
- GitHub Pages
- Static hosting
- Any CDN/static web server

No Node.js server is required for runtime rendering.

---

# 39. SPA Hosting Requirement

The production server MUST support SPA fallback.

All unknown application routes should resolve to:

```text
/index.html
```

This is required so routes such as:

```text
/camping
/about
/experiments
```

work correctly when accessed directly.

---

# 40. MVP Scope

MVP MUST contain:

```text
✓ React + Vite
✓ React Router
✓ TypeScript
✓ React Three Fiber
✓ Three.js
✓ Drei
✓ Zustand
✓ Tailwind CSS

✓ Ground
✓ Pine Trees
✓ Tent
✓ Campfire
✓ Logs
✓ Rocks
✓ Bushes
✓ Lantern

✓ Isometric camera
✓ OrbitControls
✓ GLB loading
✓ Object hover
✓ Object selection
✓ Object information panel

✓ Campfire ON/OFF
✓ Campfire animation
✓ Campfire lighting

✓ Lantern ON/OFF

✓ Day
✓ Sunset
✓ Night

✓ Loading state
✓ Responsive UI
✓ Basic performance optimization
```

---

# 41. V1.1

After MVP:

```text
□ Rain particles
□ Fog
□ Stars
□ Moon
□ Improved day/night transitions
□ Tree wind animation
□ Better object highlighting
□ Ambient audio
□ Campfire audio
□ Rain audio
□ Screenshot/photo mode
```

---

# 42. V2

Potential future expansion:

```text
□ Character
□ Character movement
□ Interactive tent
□ Interactive backpack
□ Dynamic weather
□ Snow
□ Wind
□ Multiple camping locations
□ Scene presets
□ Photo mode
□ More environmental props
```

---

# 43. Development Phases

## Phase 1 — Project Initialization

```text
□ Initialize Vite
□ Configure React
□ Configure TypeScript
□ Install React Router
□ Install Three.js
□ Install React Three Fiber
□ Install Drei
□ Install Zustand
□ Configure Tailwind
```

## Phase 2 — Basic 3D Scene

```text
□ Create Canvas
□ Configure camera
□ Configure OrbitControls
□ Add basic lighting
□ Load ground
□ Render initial scene
```

## Phase 3 — Asset Integration

```text
□ Ground
□ Pine tree
□ Tent
□ Campfire
□ Logs
□ Rocks
□ Bush
□ Lantern
```

## Phase 4 — Scene Composition

```text
□ Position tent
□ Position campfire
□ Position lantern
□ Scatter pine trees
□ Scatter rocks
□ Scatter bushes
□ Adjust composition
```

## Phase 5 — Interaction

```text
□ Hover detection
□ Object highlighting
□ Object selection
□ Object panel
□ Campfire toggle
□ Lantern toggle
```

## Phase 6 — Animation

```text
□ Fire animation
□ Fire light flickering
□ Lantern glow
□ Environment transitions
```

## Phase 7 — Environment

```text
□ Day
□ Sunset
□ Night
□ Stars
□ Moon
```

## Phase 8 — Weather

```text
□ Rain particles
□ Rain toggle
□ Fog
□ Lighting adjustment
```

## Phase 9 — Performance

```text
□ GLB optimization
□ Texture optimization
□ Object reuse
□ Instancing where useful
□ DPR optimization
□ Shadow optimization
□ FPS testing
```

## Phase 10 — Polish & Deployment

```text
□ Loading screen
□ Responsive UI
□ Mobile testing
□ Browser testing
□ Production build
□ Deploy
□ Performance audit
```

---

# 44. Acceptance Criteria

## Scene

- [ ] All required assets load successfully.
- [ ] Scene has a coherent low-poly camping composition.
- [ ] Camera provides an isometric-style view.
- [ ] Camera rotation works.
- [ ] Camera zoom works.

## Interaction

- [ ] Campfire responds to hover.
- [ ] Tent responds to hover.
- [ ] Lantern responds to hover.
- [ ] Campfire can be toggled.
- [ ] Lantern can be toggled.
- [ ] Object information panel works.

## Animation

- [ ] Campfire flame animates smoothly.
- [ ] Campfire light flickers.
- [ ] Lantern reacts to its state.
- [ ] Day/Sunset/Night transitions smoothly.

## UI

- [ ] UI is minimal.
- [ ] UI does not resemble an admin dashboard.
- [ ] Controls work on desktop.
- [ ] Controls work on mobile.

## Performance

- [ ] No major console errors.
- [ ] No unnecessary duplicate asset loading.
- [ ] Scene maintains acceptable FPS.
- [ ] GLB assets are appropriately optimized.
- [ ] Mobile remains usable.

## Deployment

- [ ] Production build succeeds.
- [ ] `/camping` works on direct navigation.
- [ ] Static deployment works correctly.
- [ ] 3D assets load correctly in production.

---

# 45. Definition of Done

The project is complete when:

1. Vite + React application is configured.
2. React Router is configured.
3. All Blender GLB assets are integrated.
4. Main camping scene renders correctly.
5. Camera controls work.
6. Interactive objects work.
7. Campfire animation works.
8. Lantern interaction works.
9. Day/Sunset/Night modes work.
10. UI is responsive.
11. Performance is acceptable on desktop and mobile.
12. Production build succeeds.
13. Application can be deployed as a static SPA.

---

# 46. Final Product Vision

Cozy Camping should feel like a **small interactive digital diorama**, not a conventional dashboard or website.

The experience should immediately present:

```text
                 🌲        🌲

                       ⛺

                            🔥
                          🪵🪵

            🌿                     🪨

                 🌲        🌲
```

The technology should remain intentionally simple:

```text
Vite
 ↓
React
 ↓
React Router
 ↓
React Three Fiber
 ↓
Three.js
 ↓
WebGL
 ↓
GLB
 ↓
Blender
```

The project is designed as a foundation for learning increasingly advanced 3D web development while keeping the first release small, performant, and visually polished.