# Architecture & Project Structure

# Cozy Camping 3D Web

**Version:** 1.0.0  
**Stack:** React + Vite + React Router + React Three Fiber + Three.js  
**State:** Zustand  
**Styling:** Tailwind CSS  
**3D Assets:** Blender â†’ GLB

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
                            â”‚
                            â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚     Vite      â”‚
                    â”‚ Build / Dev   â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                            â”‚
                            â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚     React     â”‚
                    â”‚      SPA      â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                            â”‚
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â”‚           â”‚           â”‚
                â–¼           â–¼           â–¼
           React Router   UI Layer   Zustand
                â”‚           â”‚           â”‚
                â”‚           â”‚           â”‚
                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                            â”‚
                            â–¼
                  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                  â”‚ Camping Feature  â”‚
                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â”‚                     â”‚
                â–¼                     â–¼
          Scene Layer            Effects Layer
                â”‚                     â”‚
                â–¼                     â–¼
       React Three Fiber          Three.js
                â”‚                     â”‚
                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           â”‚
                           â–¼
                         WebGL
                           â”‚
                           â–¼
                       GLB Assets
                           â–²
                           â”‚
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
  â†“
React
  â†“
React Three Fiber
  â†“
Three.js
  â†“
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
â”œâ”€â”€ camping/
â”œâ”€â”€ gallery/
â””â”€â”€ experiments/
```

---

# 2.3 Separation of 2D UI and 3D Scene

The React UI and Three.js scene should remain logically separated.

```text
              Camping Page
                    â”‚
          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
          â”‚                   â”‚
          â–¼                   â–¼
       2D UI              3D Scene
          â”‚                   â”‚
      React DOM          R3F Canvas
          â”‚                   â”‚
          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                    â”‚
                 Zustand
```

Both layers can communicate through Zustand.

Example:

```text
User clicks "Night"
       â”‚
       â–¼
EnvironmentControls
       â”‚
       â–¼
campingStore.setTimeMode("night")
       â”‚
       â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º UI updates
       â”‚
       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º Scene lighting updates
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
â”œâ”€â”€ main.tsx
â””â”€â”€ app/
    â”œâ”€â”€ App.tsx
    â””â”€â”€ routes.tsx
```

### `main.tsx`

Entry point:

```text
main.tsx
    â†“
ReactDOM
    â†“
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
â””â”€â”€ /camping
```

Future:

```text
/
â”œâ”€â”€ /camping
â”œâ”€â”€ /about
â””â”€â”€ /experiments
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
â””â”€â”€ camping/
    â”œâ”€â”€ pages/
    â”œâ”€â”€ components/
    â”œâ”€â”€ scene/
    â”œâ”€â”€ effects/
    â”œâ”€â”€ config/
    â””â”€â”€ types/
```

This means the entire camping experience can eventually be moved or expanded without affecting unrelated features.

---

# 6. Page Layer

```text
features/camping/pages/
â””â”€â”€ CampingPage.tsx
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
â”œâ”€â”€ Header.tsx
â”œâ”€â”€ EnvironmentControls.tsx
â”œâ”€â”€ ObjectPanel.tsx
â””â”€â”€ LoadingScreen.tsx
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
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
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
â”œâ”€â”€ CampingScene.tsx
â”œâ”€â”€ Ground.tsx
â”œâ”€â”€ Forest.tsx
â”œâ”€â”€ Tent.tsx
â”œâ”€â”€ Campfire.tsx
â”œâ”€â”€ Lantern.tsx
â”œâ”€â”€ Stump.tsx
â”œâ”€â”€ Rocks.tsx
â””â”€â”€ Bushes.tsx
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
â”‚
â”œâ”€â”€ Camera
â”œâ”€â”€ OrbitControls
â”‚
â”œâ”€â”€ Environment
â”‚
â”œâ”€â”€ Ground
â”‚
â”œâ”€â”€ Forest
â”‚   â”œâ”€â”€ PineTree
â”‚   â”œâ”€â”€ PineTree
â”‚   â””â”€â”€ PineTree
â”‚
â”œâ”€â”€ Tent
â”‚
â”œâ”€â”€ Campfire
â”‚
â”œâ”€â”€ Logs
â”‚
â”œâ”€â”€ Rocks
â”‚
â”œâ”€â”€ Bushes
â”‚
â””â”€â”€ Lantern
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
â””â”€â”€ Environment.tsx
```

Responsible for:

- Sky/background
- Ambient lighting
- Directional lighting
- Environment configuration

The environment reads the current state:

```text
Zustand
   â”‚
   â–¼
timeMode
   â”‚
   â–¼
Environment
   â”‚
   â”œâ”€â”€ day
   â”œâ”€â”€ sunset
   â””â”€â”€ night
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
â”œâ”€â”€ FireEffect.tsx
â”œâ”€â”€ RainEffect.tsx
â”œâ”€â”€ DayNightEffect.tsx
â””â”€â”€ LightingEffect.tsx
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
   â”‚
   â””â”€â”€ FireEffect
          â”œâ”€â”€ scale animation
          â”œâ”€â”€ rotation animation
          â””â”€â”€ light flicker
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
    â”‚
    â””â”€â”€ Instanced / Particle system
            â”‚
            â”œâ”€â”€ position
            â”œâ”€â”€ velocity
            â””â”€â”€ reset
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
â””â”€â”€ campingStore.ts
```

Recommended:

```text
campingStore
â”‚
â”œâ”€â”€ timeMode
â”œâ”€â”€ weather
â”œâ”€â”€ campfireActive
â”œâ”€â”€ lanternActive
â””â”€â”€ selectedObject
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
 â”‚
 â–¼
EnvironmentControls
 â”‚
 â–¼
campingStore
 â”‚
 â”‚ setTimeMode("night")
 â”‚
 â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
 â–¼               â–¼
Environment    UI
 â”‚
 â–¼
Lighting
 â”‚
 â–¼
Three.js
```

Example: campfire interaction.

```text
User clicks Campfire
        â”‚
        â–¼
Campfire.tsx
        â”‚
        â–¼
campingStore.toggleCampfire()
        â”‚
        â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º ObjectPanel
        â”‚
        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º FireEffect
                              â”‚
                              â–¼
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
â”œâ”€â”€ ground.glb
â”œâ”€â”€ pine-tree.glb
â”œâ”€â”€ tent.glb
â”œâ”€â”€ campfire.glb
â”œâ”€â”€ stump.glb
â”œâ”€â”€ rocks.glb
â”œâ”€â”€ bush.glb
â””â”€â”€ lantern.glb
```

Assets are treated as static application resources.

---

# 19. Asset Configuration

Asset metadata should not be hardcoded throughout components.

Create:

```text
features/camping/config/
â””â”€â”€ asset-config.ts
```

Example:

```ts
export const CAMPING_ASSETS = {
  ground: "/models/ground.glb",
  pineTree: "/models/pine-tree.glb",
  tent: "/models/tent.glb",
  campfire: "/models/campfire.glb",
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
â””â”€â”€ scene-config.ts
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
â””â”€â”€ camping.ts
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
â”œâ”€â”€ components/
â”œâ”€â”€ hooks/
â”œâ”€â”€ utils/
â””â”€â”€ types/
```

Do NOT create a large shared abstraction prematurely.

Only move something here when it is actually shared by multiple features.

---

# 23. Final Project Structure

The recommended final structure is:

```text
cozy-camping/
â”‚
â”œâ”€â”€ public/
â”‚   â””â”€â”€ models/
â”‚       â”œâ”€â”€ ground.glb
â”‚       â”œâ”€â”€ pine-tree.glb
â”‚       â”œâ”€â”€ tent.glb
â”‚       â”œâ”€â”€ campfire.glb
â”‚       â”œâ”€â”€ stump.glb
â”‚       â”œâ”€â”€ rocks.glb
â”‚       â”œâ”€â”€ bush.glb
â”‚       â””â”€â”€ lantern.glb
â”‚
â”œâ”€â”€ src/
â”‚   â”‚
â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”œâ”€â”€ App.tsx
â”‚   â”‚   â””â”€â”€ routes.tsx
â”‚   â”‚
â”‚   â”œâ”€â”€ features/
â”‚   â”‚   â””â”€â”€ camping/
â”‚   â”‚       â”‚
â”‚   â”‚       â”œâ”€â”€ pages/
â”‚   â”‚       â”‚   â””â”€â”€ CampingPage.tsx
â”‚   â”‚       â”‚
â”‚   â”‚       â”œâ”€â”€ components/
â”‚   â”‚       â”‚   â”œâ”€â”€ Header.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ EnvironmentControls.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ ObjectPanel.tsx
â”‚   â”‚       â”‚   â””â”€â”€ LoadingScreen.tsx
â”‚   â”‚       â”‚
â”‚   â”‚       â”œâ”€â”€ scene/
â”‚   â”‚       â”‚   â”œâ”€â”€ CampingScene.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ Ground.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ Forest.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ Tent.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ Campfire.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ Lantern.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ Stump.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ Rocks.tsx
â”‚   â”‚       â”‚   â””â”€â”€ Bushes.tsx
â”‚   â”‚       â”‚
â”‚   â”‚       â”œâ”€â”€ effects/
â”‚   â”‚       â”‚   â”œâ”€â”€ FireEffect.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ RainEffect.tsx
â”‚   â”‚       â”‚   â”œâ”€â”€ DayNightEffect.tsx
â”‚   â”‚       â”‚   â””â”€â”€ LightingEffect.tsx
â”‚   â”‚       â”‚
â”‚   â”‚       â”œâ”€â”€ store/
â”‚   â”‚       â”‚   â””â”€â”€ campingStore.ts
â”‚   â”‚       â”‚
â”‚   â”‚       â”œâ”€â”€ config/
â”‚   â”‚       â”‚   â”œâ”€â”€ asset-config.ts
â”‚   â”‚       â”‚   â””â”€â”€ scene-config.ts
â”‚   â”‚       â”‚
â”‚   â”‚       â””â”€â”€ types/
â”‚   â”‚           â””â”€â”€ camping.ts
â”‚   â”‚
â”‚   â”œâ”€â”€ shared/
â”‚   â”‚   â”œâ”€â”€ components/
â”‚   â”‚   â”œâ”€â”€ hooks/
â”‚   â”‚   â”œâ”€â”€ utils/
â”‚   â”‚   â””â”€â”€ types/
â”‚   â”‚
â”‚   â”œâ”€â”€ styles/
â”‚   â”‚   â””â”€â”€ globals.css
â”‚   â”‚
â”‚   â””â”€â”€ main.tsx
â”‚
â”œâ”€â”€ index.html
â”œâ”€â”€ vite.config.ts
â”œâ”€â”€ tsconfig.json
â”œâ”€â”€ package.json
â””â”€â”€ README.md
```

---

# 24. Dependency Direction

Dependencies should flow inward toward the feature.

Preferred:

```text
app
 â†“
features
 â†“
scene / effects / components
 â†“
config / types / store
```

Shared utilities should remain independent.

Avoid:

```text
scene
 â†“
UI
 â†“
scene
```

Avoid circular dependencies.

---

# 25. UI â†” 3D Communication

UI and 3D objects should communicate through Zustand rather than directly referencing each other.

Bad:

```text
ObjectPanel
   â†“
Campfire component reference
```

Preferred:

```text
ObjectPanel
   â†“
Zustand
   â†“
Campfire
```

This keeps the architecture predictable.

---

# 26. 3D Component Rule

Each 3D component should follow this responsibility model:

```text
Component
â”‚
â”œâ”€â”€ Load asset
â”œâ”€â”€ Render asset
â”œâ”€â”€ Local visual behavior
â””â”€â”€ Interaction
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
    â””â”€â”€ FireEffect
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
  â†“
setState()
  â†“
React render
  â†“
60 times/second
```

Preferred:

```text
useFrame
  â†“
Three.js object mutation
  â†“
WebGL
```

React state should be used for application-level state, not per-frame animation values.

---

# 29. Rendering Strategy

The application uses:

```text
React
   â”‚
   â””â”€â”€ DOM UI

React Three Fiber
   â”‚
   â””â”€â”€ WebGL Canvas
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
  â”‚
  â–¼
Vite
  â”‚
  â–¼
npm run build
  â”‚
  â–¼
dist/
  â”‚
  â–¼
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
                            â”‚
                            â–¼
                     React Application
                            â”‚
                 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                 â”‚                     â”‚
                 â–¼                     â–¼
              DOM UI              WebGL Canvas
                 â”‚                     â”‚
                 â”‚                     â–¼
                 â”‚              React Three Fiber
                 â”‚                     â”‚
                 â”‚                     â–¼
                 â”‚                  Three.js
                 â”‚                     â”‚
                 â”‚                     â–¼
                 â”‚                   WebGL
                 â”‚
                 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                            â–¼
                         Zustand
                            â”‚
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â–¼           â–¼           â–¼
             UI State   Scene State   Effects
```

---

# 33. Example User Interaction Flow

## Campfire

```text
User
 â†“
Click Campfire
 â†“
Campfire.tsx
 â†“
campingStore.selectObject("campfire")
 â†“
ObjectPanel
 â†“
User clicks "Turn Off"
 â†“
campingStore.toggleCampfire()
 â†“
Campfire state changes
 â†“
FireEffect disabled
 â†“
PointLight disabled
 â†“
UI updated
```

---

# 34. Example Environment Flow

```text
User
 â†“
Click Night
 â†“
EnvironmentControls
 â†“
campingStore.setTimeMode("night")
 â†“
DayNightEffect
 â†“
Interpolate lighting
 â†“
Environment
 â†“
Three.js
 â†“
WebGL
```

---

# 35. Architecture Goals

The architecture should remain:

```text
Simple
        â†“
Predictable
        â†“
Modular
        â†“
Performant
        â†“
Easy to Extend
```

The project should avoid enterprise-level abstractions because the current application is intentionally small.

---

# 36. Future Expansion

If the project grows, new features can be added without restructuring the existing camping feature.

Example:

```text
features/
â”œâ”€â”€ camping/
â”œâ”€â”€ gallery/
â”œâ”€â”€ experiments/
â””â”€â”€ portfolio/
```

A future shared 3D system could also be introduced:

```text
shared/
â””â”€â”€ three/
    â”œâ”€â”€ Camera.tsx
    â”œâ”€â”€ Lighting.tsx
    â”œâ”€â”€ Model.tsx
    â””â”€â”€ Interaction.tsx
```

This should only happen when multiple features actually require the same functionality.

---

# 37. Final Architecture

The final architecture is intentionally lightweight:

```text
                    Vite
                     â”‚
                   React
                     â”‚
              React Router
                     â”‚
              Camping Feature
                     â”‚
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â”‚            â”‚            â”‚
       UI          Scene        Effects
        â”‚            â”‚            â”‚
        â”‚        R3F / Three.js   â”‚
        â”‚            â”‚            â”‚
        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                     â”‚
                  Zustand
                     â”‚
                     â–¼
                  WebGL
                     â”‚
                     â–¼
                 GLB Assets
                     â–²
                     â”‚
                  Blender
```

The key architectural principle is:

> **React manages the application and UI state; React Three Fiber/Three.js manages the 3D world; Zustand connects the two; Blender provides the static 3D assets.**