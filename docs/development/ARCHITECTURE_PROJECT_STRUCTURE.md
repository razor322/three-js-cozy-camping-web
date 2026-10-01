# Architecture & Project Structure

# Cozy Camping 3D Web

**Version:** 1.0.0  
**Stack:** React + Vite + React Router + React Three Fiber + Three.js  
**State:** Zustand  
**Styling:** Tailwind CSS  
**3D Assets:** Blender → GLB

---

# 1. Architecture Overview

Cozy Camping uses a lightweight client-side architecture designed specifically for an interactive 3D SPA.

The architecture separates:

1. Application routing
2. UI components
3. 3D scene
4. 3D effects
5. Global state
6. Configuration
7. Static 3D assets

High-level architecture:

```text
                         Browser
                            │
                            ▼
                    ┌───────────────┐
                    │     Vite      │
                    │ Build / Dev   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     React     │
                    │      SPA      │
                    └───────┬───────┘
                            │
                ┌───────────┼───────────┐
                │           │           │
                ▼           ▼           ▼
           React Router   UI Layer   Zustand
                │           │           │
                │           │           │
                └───────────┼───────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Camping Feature  │
                  └────────┬─────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          Scene Layer            Effects Layer
                │                     │
                ▼                     ▼
       React Three Fiber          Three.js
                │                     │
                └──────────┬──────────┘
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

# 2. Architectural Principles

## 2.1 Client-Side First

The application is fully client-side.

There is no requirement for:

- SSR
- API server
- Database
- Authentication
- Server Components

Runtime architecture:

```text
Browser
  ↓
React
  ↓
React Three Fiber
  ↓
Three.js
  ↓
WebGL
```

---

# 2.2 Feature-Oriented Structure

The project should organize major functionality around features rather than creating one giant component directory.

Main feature:

```text
camping/
```

This keeps the project easy to extend.

Future features could become:

```text
features/
├── camping/
├── gallery/
└── experiments/
```

---

# 2.3 Separation of 2D UI and 3D Scene

The React UI and Three.js scene should remain logically separated.

```text
              Camping Page
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
       2D UI              3D Scene
          │                   │
      React DOM          R3F Canvas
          │                   │
          └─────────┬─────────┘
                    │
                 Zustand
```

Both layers can communicate through Zustand.

Example:

```text
User clicks "Night"
       │
       ▼
EnvironmentControls
       │
       ▼
campingStore.setTimeMode("night")
       │
       ├──────────────► UI updates
       │
       └──────────────► Scene lighting updates
```

---

# 3. Application Layers

The application consists of six logical layers.

```text
1. App Layer
2. Page / Feature Layer
3. UI Layer
4. 3D Scene Layer
5. State Layer
6. Infrastructure / Asset Layer
```

---

# 4. App Layer

Responsible for:

- Application bootstrap
- Router
- Global providers
- Global styles

```text
src/
├── main.tsx
└── app/
    ├── App.tsx
    └── routes.tsx
```

### `main.tsx`

Entry point:

```text
main.tsx
    ↓
ReactDOM
    ↓
App
```

### `App.tsx`

Responsible for:

- RouterProvider
- Global application configuration

### `routes.tsx`

Responsible for:

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

---

# 5. Feature Layer

The primary feature is:

```text
src/features/camping/
```

This contains everything specific to the camping experience.

Recommended structure:

```text
features/
└── camping/
    ├── pages/
    ├── components/
    ├── scene/
    ├── effects/
    ├── config/
    └── types/
```

This means the entire camping experience can eventually be moved or expanded without affecting unrelated features.

---

# 6. Page Layer

```text
features/camping/pages/
└── CampingPage.tsx
```

`CampingPage` acts as the composition root for the camping experience.

Conceptually:

```tsx
<CampingPage>
    <Header />

    <CampingScene />

    <ObjectPanel />

    <EnvironmentControls />
</CampingPage>
```

The page should NOT contain detailed Three.js logic.

---

# 7. UI Layer

```text
features/camping/components/
```

Recommended:

```text
components/
├── Header.tsx
├── EnvironmentControls.tsx
├── ObjectPanel.tsx
└── LoadingScreen.tsx
```

Responsibilities:

### `Header.tsx`

Displays:

- Project title
- Current time/environment
- Optional simulated clock

### `EnvironmentControls.tsx`

Controls:

```text
Day
Sunset
Night
Clear
Rain
```

### `ObjectPanel.tsx`

Displays information for selected objects.

Example:

```text
Campfire
─────────────
Status: Burning

[ Turn Off ]
```

### `LoadingScreen.tsx`

Displays scene loading progress.

---

# 8. 3D Scene Layer

The 3D scene lives under:

```text
features/camping/scene/
```

Recommended structure:

```text
scene/
├── CampingScene.tsx
├── Ground.tsx
├── Forest.tsx
├── Tent.tsx
├── Campfire.tsx
├── Lantern.tsx
├── Logs.tsx
├── Rocks.tsx
└── Bushes.tsx
```

---

# 9. CampingScene

`CampingScene.tsx` is the main R3F scene.

Responsibilities:

- Scene composition
- Camera
- OrbitControls
- Global scene lighting
- Environment
- Child objects

Conceptual structure:

```text
CampingScene
│
├── Camera
├── OrbitControls
│
├── Environment
│
├── Ground
│
├── Forest
│   ├── PineTree
│   ├── PineTree
│   └── PineTree
│
├── Tent
│
├── Campfire
│
├── Logs
│
├── Rocks
│
├── Bushes
│
└── Lantern
```

The component should focus on **composition**, not implementation details.

---

# 10. Scene Object Responsibilities

Each major asset gets its own component.

Example:

```text
Campfire.tsx
```

Responsible for:

- Loading `campfire.glb`
- Flame mesh
- Campfire state
- Campfire PointLight
- Interaction
- Animation integration

It should NOT contain unrelated UI.

---

# 11. Environment

Environment-specific logic:

```text
scene/
└── Environment.tsx
```

Responsible for:

- Sky/background
- Ambient lighting
- Directional lighting
- Environment configuration

The environment reads the current state:

```text
Zustand
   │
   ▼
timeMode
   │
   ▼
Environment
   │
   ├── day
   ├── sunset
   └── night
```

---

# 12. Effects Layer

Effects are separated from base 3D objects.

```text
features/camping/effects/
```

Structure:

```text
effects/
├── FireEffect.tsx
├── RainEffect.tsx
├── DayNightEffect.tsx
└── LightingEffect.tsx
```

---

# 13. FireEffect

Responsible for:

```text
Flame scale
Flame rotation
Flame position
Emissive intensity
PointLight flicker
```

Example architecture:

```text
Campfire
   │
   └── FireEffect
          ├── scale animation
          ├── rotation animation
          └── light flicker
```

Animation should use `useFrame`.

---

# 14. RainEffect

Responsible for:

- Rain particles
- Particle movement
- Particle reset
- Visibility

Architecture:

```text
RainEffect
    │
    └── Instanced / Particle system
            │
            ├── position
            ├── velocity
            └── reset
```

Rain should NOT be represented by hundreds of React components.

---

# 15. DayNightEffect

Responsible for smooth transitions between:

```text
DAY
SUNSET
NIGHT
```

It should interpolate:

- Light intensity
- Light color
- Environment color
- Sky color
- Fog
- Campfire visibility influence

---

# 16. State Layer

Global state:

```text
src/features/camping/store/
└── campingStore.ts
```

Recommended:

```text
campingStore
│
├── timeMode
├── weather
├── campfireActive
├── lanternActive
└── selectedObject
```

Example:

```ts
type TimeMode = "day" | "sunset" | "night";

type WeatherMode = "clear" | "rain";
```

---

# 17. State Flow

Example: changing time.

```text
User
 │
 ▼
EnvironmentControls
 │
 ▼
campingStore
 │
 │ setTimeMode("night")
 │
 ├───────────────┐
 ▼               ▼
Environment    UI
 │
 ▼
Lighting
 │
 ▼
Three.js
```

Example: campfire interaction.

```text
User clicks Campfire
        │
        ▼
Campfire.tsx
        │
        ▼
campingStore.toggleCampfire()
        │
        ├──────────────► ObjectPanel
        │
        └──────────────► FireEffect
                              │
                              ▼
                         PointLight
```

---

# 18. Asset Layer

Assets are stored in:

```text
public/models/
```

```text
models/
├── ground.glb
├── pine-tree.glb
├── tent.glb
├── campfire.glb
├── logs.glb
├── rocks.glb
├── bush.glb
└── lantern.glb
```

Assets are treated as static application resources.

---

# 19. Asset Configuration

Asset metadata should not be hardcoded throughout components.

Create:

```text
features/camping/config/
└── asset-config.ts
```

Example:

```ts
export const CAMPING_ASSETS = {
  ground: "/models/ground.glb",
  pineTree: "/models/pine-tree.glb",
  tent: "/models/tent.glb",
  campfire: "/models/campfire.glb",
  logs: "/models/logs.glb",
  rocks: "/models/rocks.glb",
  bush: "/models/bush.glb",
  lantern: "/models/lantern.glb",
} as const;
```

Components then use:

```ts
useGLTF(CAMPING_ASSETS.campfire)
```

This avoids scattered asset paths.

---

# 20. Scene Configuration

Create:

```text
features/camping/config/
└── scene-config.ts
```

Contains:

- Camera configuration
- Object positions
- Scale
- Lighting configuration
- Environment settings
- Performance limits

Example:

```ts
export const SCENE_CONFIG = {
  camera: {
    position: [12, 12, 12],
    fov: 45,
  },

  trees: {
    count: 8,
    scaleRange: [0.7, 1.3],
  },

  rain: {
    maxParticles: 1000,
  },
};
```

---

# 21. Types

Feature-specific types:

```text
features/camping/types/
└── camping.ts
```

Example:

```ts
export type TimeMode = "day" | "sunset" | "night";

export type WeatherMode = "clear" | "rain";

export type InteractiveObject =
  | "campfire"
  | "tent"
  | "lantern";
```

This prevents duplicated type definitions.

---

# 22. Shared Layer

If reusable components appear later, they can move into:

```text
src/shared/
```

Potential structure:

```text
shared/
├── components/
├── hooks/
├── utils/
└── types/
```

Do NOT create a large shared abstraction prematurely.

Only move something here when it is actually shared by multiple features.

---

# 23. Final Project Structure

The recommended final structure is:

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
│   ├── features/
│   │   └── camping/
│   │       │
│   │       ├── pages/
│   │       │   └── CampingPage.tsx
│   │       │
│   │       ├── components/
│   │       │   ├── Header.tsx
│   │       │   ├── EnvironmentControls.tsx
│   │       │   ├── ObjectPanel.tsx
│   │       │   └── LoadingScreen.tsx
│   │       │
│   │       ├── scene/
│   │       │   ├── CampingScene.tsx
│   │       │   ├── Ground.tsx
│   │       │   ├── Forest.tsx
│   │       │   ├── Tent.tsx
│   │       │   ├── Campfire.tsx
│   │       │   ├── Lantern.tsx
│   │       │   ├── Logs.tsx
│   │       │   ├── Rocks.tsx
│   │       │   └── Bushes.tsx
│   │       │
│   │       ├── effects/
│   │       │   ├── FireEffect.tsx
│   │       │   ├── RainEffect.tsx
│   │       │   ├── DayNightEffect.tsx
│   │       │   └── LightingEffect.tsx
│   │       │
│   │       ├── store/
│   │       │   └── campingStore.ts
│   │       │
│   │       ├── config/
│   │       │   ├── asset-config.ts
│   │       │   └── scene-config.ts
│   │       │
│   │       └── types/
│   │           └── camping.ts
│   │
│   ├── shared/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── types/
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

# 24. Dependency Direction

Dependencies should flow inward toward the feature.

Preferred:

```text
app
 ↓
features
 ↓
scene / effects / components
 ↓
config / types / store
```

Shared utilities should remain independent.

Avoid:

```text
scene
 ↓
UI
 ↓
scene
```

Avoid circular dependencies.

---

# 25. UI ↔ 3D Communication

UI and 3D objects should communicate through Zustand rather than directly referencing each other.

Bad:

```text
ObjectPanel
   ↓
Campfire component reference
```

Preferred:

```text
ObjectPanel
   ↓
Zustand
   ↓
Campfire
```

This keeps the architecture predictable.

---

# 26. 3D Component Rule

Each 3D component should follow this responsibility model:

```text
Component
│
├── Load asset
├── Render asset
├── Local visual behavior
└── Interaction
```

Avoid putting:

- Routing
- Complex UI
- Global application configuration
- Unrelated state

inside a scene object.

---

# 27. Animation Rule

Animations that belong to an object may stay inside that object.

Example:

```text
Campfire.tsx
    └── FireEffect
```

Global environmental animation should remain in:

```text
effects/
```

Examples:

```text
RainEffect
DayNightEffect
LightingEffect
```

---

# 28. Performance Architecture

Performance-sensitive operations should remain inside Three.js/R3F.

Avoid excessive React state updates inside animation loops.

Bad:

```text
useFrame
  ↓
setState()
  ↓
React render
  ↓
60 times/second
```

Preferred:

```text
useFrame
  ↓
Three.js object mutation
  ↓
WebGL
```

React state should be used for application-level state, not per-frame animation values.

---

# 29. Rendering Strategy

The application uses:

```text
React
   │
   └── DOM UI

React Three Fiber
   │
   └── WebGL Canvas
```

The 3D canvas should be isolated from unnecessary React re-renders.

---

# 30. Performance Priorities

Optimization order:

```text
1. GLB size
2. Texture size
3. Draw calls
4. Number of objects
5. Dynamic lights
6. Shadows
7. Particle count
8. DPR
9. Post-processing
```

Do not optimize prematurely.

Measure first, then optimize.

---

# 31. Deployment Architecture

The project produces a static SPA.

```text
Source
  │
  ▼
Vite
  │
  ▼
npm run build
  │
  ▼
dist/
  │
  ▼
Static Hosting
```

Possible hosting:

```text
Vercel
Netlify
Cloudflare Pages
GitHub Pages
Static Web Server
```

No application server is required.

---

# 32. Runtime Architecture

At runtime:

```text
                         Browser
                            │
                            ▼
                     React Application
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
              DOM UI              WebGL Canvas
                 │                     │
                 │                     ▼
                 │              React Three Fiber
                 │                     │
                 │                     ▼
                 │                  Three.js
                 │                     │
                 │                     ▼
                 │                   WebGL
                 │
                 └──────────┐
                            ▼
                         Zustand
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
             UI State   Scene State   Effects
```

---

# 33. Example User Interaction Flow

## Campfire

```text
User
 ↓
Click Campfire
 ↓
Campfire.tsx
 ↓
campingStore.selectObject("campfire")
 ↓
ObjectPanel
 ↓
User clicks "Turn Off"
 ↓
campingStore.toggleCampfire()
 ↓
Campfire state changes
 ↓
FireEffect disabled
 ↓
PointLight disabled
 ↓
UI updated
```

---

# 34. Example Environment Flow

```text
User
 ↓
Click Night
 ↓
EnvironmentControls
 ↓
campingStore.setTimeMode("night")
 ↓
DayNightEffect
 ↓
Interpolate lighting
 ↓
Environment
 ↓
Three.js
 ↓
WebGL
```

---

# 35. Architecture Goals

The architecture should remain:

```text
Simple
        ↓
Predictable
        ↓
Modular
        ↓
Performant
        ↓
Easy to Extend
```

The project should avoid enterprise-level abstractions because the current application is intentionally small.

---

# 36. Future Expansion

If the project grows, new features can be added without restructuring the existing camping feature.

Example:

```text
features/
├── camping/
├── gallery/
├── experiments/
└── portfolio/
```

A future shared 3D system could also be introduced:

```text
shared/
└── three/
    ├── Camera.tsx
    ├── Lighting.tsx
    ├── Model.tsx
    └── Interaction.tsx
```

This should only happen when multiple features actually require the same functionality.

---

# 37. Final Architecture

The final architecture is intentionally lightweight:

```text
                    Vite
                     │
                   React
                     │
              React Router
                     │
              Camping Feature
                     │
        ┌────────────┼────────────┐
        │            │            │
       UI          Scene        Effects
        │            │            │
        │        R3F / Three.js   │
        │            │            │
        └────────────┼────────────┘
                     │
                  Zustand
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

The key architectural principle is:

> **React manages the application and UI state; React Three Fiber/Three.js manages the 3D world; Zustand connects the two; Blender provides the static 3D assets.**