# Product Requirements Document (PRD)

# Cozy Camping 3D Web

**Version:** 1.1.0  
**Status:** Ready for Development  
**Type:** Interactive 3D Single Page Application  
**Platform:** Web  
**Primary Stack:** React + Vite + React Router  
**3D Stack:** Three.js + React Three Fiber  
**3D Asset Pipeline:** Blender â†’ GLB

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
   â”‚
   â–¼
Vite
   â”‚
   â–¼
React SPA
   â”‚
   â”œâ”€â”€ React Router
   â”‚
   â”œâ”€â”€ Zustand
   â”‚
   â””â”€â”€ React Three Fiber
          â”‚
          â–¼
       Three.js
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
â””â”€â”€ /camping
```

Recommended structure:

```text
/
â”œâ”€â”€ /camping
â”œâ”€â”€ /about
â””â”€â”€ /experiments
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
rocks.glb
stump.glb
bush.glb
lantern.glb
```

Recommended public structure:

```text
public/
â””â”€â”€ models/
    â”œâ”€â”€ ground.glb
    â”œâ”€â”€ pine-tree.glb
    â”œâ”€â”€ tent.glb
    â”œâ”€â”€ campfire.glb
    â”œâ”€â”€ stump.glb
    â”œâ”€â”€ rocks.glb
    â”œâ”€â”€ bush.glb
    â””â”€â”€ lantern.glb
```

---

# 12. Ground

Ground specification:

```text
Shape: Rounded Square
Size: approximately 18m Ã— 18m
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
â”œâ”€â”€ Rocks
â”œâ”€â”€ Logs
â””â”€â”€ Campfire_Flame
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
                    ðŸŒ²

          ðŸŒ²                 ðŸŒ²

              ðŸª¨       ðŸŒ¿

                    â›º

                         ðŸ”¥
                       ðŸªµðŸªµ

          ðŸŒ¿                  ðŸª¨

              ðŸŒ²        ðŸŒ²
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

## FR-001 â€” 3D Scene

The application MUST render the camping environment using React Three Fiber.

Required objects:

```text
Ground
Pine Trees
Tent
Campfire
Stump seats
Rocks
Bushes
Lantern
```

---

## FR-002 â€” GLB Loading

All Blender assets MUST be loaded as GLB.

Recommended approach:

```tsx
useGLTF("/models/tent.glb")
```

Drei's `useGLTF` SHOULD be used for asset loading.

---

## FR-003 â€” Camera

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

## FR-004 â€” Object Hover

Interactive objects MUST provide visual feedback.

Possible implementation:

```text
Hover
 â†“
Subtle scale
+
Emissive/highlight
+
Cursor change
```

The effect should remain subtle.

---

## FR-005 â€” Object Selection

Interactive objects:

```text
Campfire
Tent
Lantern
```

When selected:

```text
Object
   â†“
Selection State
   â†“
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
   â†•
rotation.z
   â†•
position.y
   â†•
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
1â€“2 seconds
```

Example:

```text
DAY
 â†“
fade/lerp
 â†“
SUNSET
 â†“
fade/lerp
 â†“
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
500â€“1500
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
 â†“
Campfire intensity decreases slightly
 â†“
Ambient sound changes
```

---

# 25. UI

The UI must remain minimal and integrated with the scene.

It MUST NOT look like an admin dashboard.

Example:

```text
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ COZY CAMPING                         ðŸŒ™ 21:42â”‚
â”‚                                              â”‚
â”‚                                              â”‚
â”‚                  3D SCENE                    â”‚
â”‚                                              â”‚
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
â”‚   â”œâ”€â”€ scenes/
â”‚   â”‚   â””â”€â”€ camping/
â”‚   â”‚       â”œâ”€â”€ CampingScene.tsx
â”‚   â”‚       â”œâ”€â”€ Ground.tsx
â”‚   â”‚       â”œâ”€â”€ Forest.tsx
â”‚   â”‚       â”œâ”€â”€ Tent.tsx
â”‚   â”‚       â”œâ”€â”€ Campfire.tsx
â”‚   â”‚       â”œâ”€â”€ Lantern.tsx
â”‚   â”‚       â”œâ”€â”€ Rocks.tsx
â”‚   â”‚       â”œâ”€â”€ Bushes.tsx
â”‚   â”‚       â””â”€â”€ Stump.tsx
â”‚   â”‚
â”‚   â”œâ”€â”€ effects/
â”‚   â”‚   â”œâ”€â”€ FireEffect.tsx
â”‚   â”‚   â”œâ”€â”€ RainEffect.tsx
â”‚   â”‚   â”œâ”€â”€ DayNightEffect.tsx
â”‚   â”‚   â””â”€â”€ LightingEffect.tsx
â”‚   â”‚
â”‚   â”œâ”€â”€ components/
â”‚   â”‚   â”œâ”€â”€ Header.tsx
â”‚   â”‚   â”œâ”€â”€ EnvironmentControls.tsx
â”‚   â”‚   â”œâ”€â”€ ObjectPanel.tsx
â”‚   â”‚   â””â”€â”€ LoadingScreen.tsx
â”‚   â”‚
â”‚   â”œâ”€â”€ stores/
â”‚   â”‚   â””â”€â”€ campingStore.ts
â”‚   â”‚
â”‚   â”œâ”€â”€ lib/
â”‚   â”‚   â”œâ”€â”€ scene-config.ts
â”‚   â”‚   â””â”€â”€ asset-config.ts
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

# 28. Routing Structure

Initial:

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
Target: 30â€“60 FPS
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
 â†“
GLB
 â†“
Optimize
 â†“
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
      â†“
   Instance
      â”œâ”€â”€ tree 1
      â”œâ”€â”€ tree 2
      â”œâ”€â”€ tree 3
      â”œâ”€â”€ tree 4
      â””â”€â”€ tree 5
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
1920 Ã— 1080
1440 Ã— 900
1280 Ã— 720
```

Supported mobile sizes:

```text
390 Ã— 844
412 Ã— 915
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
âœ“ React + Vite
âœ“ React Router
âœ“ TypeScript
âœ“ React Three Fiber
âœ“ Three.js
âœ“ Drei
âœ“ Zustand
âœ“ Tailwind CSS

âœ“ Ground
âœ“ Pine Trees
âœ“ Tent
âœ“ Campfire
âœ“ Logs
âœ“ Rocks
âœ“ Bushes
âœ“ Lantern

âœ“ Isometric camera
âœ“ OrbitControls
âœ“ GLB loading
âœ“ Object hover
âœ“ Object selection
âœ“ Object information panel

âœ“ Campfire ON/OFF
âœ“ Campfire animation
âœ“ Campfire lighting

âœ“ Lantern ON/OFF

âœ“ Day
âœ“ Sunset
âœ“ Night

âœ“ Loading state
âœ“ Responsive UI
âœ“ Basic performance optimization
```

---

# 41. V1.1

After MVP:

```text
â–¡ Rain particles
â–¡ Fog
â–¡ Stars
â–¡ Moon
â–¡ Improved day/night transitions
â–¡ Tree wind animation
â–¡ Better object highlighting
â–¡ Ambient audio
â–¡ Campfire audio
â–¡ Rain audio
â–¡ Screenshot/photo mode
```

---

# 42. V2

Potential future expansion:

```text
â–¡ Character
â–¡ Character movement
â–¡ Interactive tent
â–¡ Interactive backpack
â–¡ Dynamic weather
â–¡ Snow
â–¡ Wind
â–¡ Multiple camping locations
â–¡ Scene presets
â–¡ Photo mode
â–¡ More environmental props
```

---

# 43. Development Phases

## Phase 1 â€” Project Initialization

```text
â–¡ Initialize Vite
â–¡ Configure React
â–¡ Configure TypeScript
â–¡ Install React Router
â–¡ Install Three.js
â–¡ Install React Three Fiber
â–¡ Install Drei
â–¡ Install Zustand
â–¡ Configure Tailwind
```

## Phase 2 â€” Basic 3D Scene

```text
â–¡ Create Canvas
â–¡ Configure camera
â–¡ Configure OrbitControls
â–¡ Add basic lighting
â–¡ Load ground
â–¡ Render initial scene
```

## Phase 3 â€” Asset Integration

```text
â–¡ Ground
â–¡ Pine tree
â–¡ Tent
â–¡ Campfire
â–¡ Logs
â–¡ Rocks
â–¡ Bush
â–¡ Lantern
```

## Phase 4 â€” Scene Composition

```text
â–¡ Position tent
â–¡ Position campfire
â–¡ Position lantern
â–¡ Scatter pine trees
â–¡ Scatter rocks
â–¡ Scatter bushes
â–¡ Adjust composition
```

## Phase 5 â€” Interaction

```text
â–¡ Hover detection
â–¡ Object highlighting
â–¡ Object selection
â–¡ Object panel
â–¡ Campfire toggle
â–¡ Lantern toggle
```

## Phase 6 â€” Animation

```text
â–¡ Fire animation
â–¡ Fire light flickering
â–¡ Lantern glow
â–¡ Environment transitions
```

## Phase 7 â€” Environment

```text
â–¡ Day
â–¡ Sunset
â–¡ Night
â–¡ Stars
â–¡ Moon
```

## Phase 8 â€” Weather

```text
â–¡ Rain particles
â–¡ Rain toggle
â–¡ Fog
â–¡ Lighting adjustment
```

## Phase 9 â€” Performance

```text
â–¡ GLB optimization
â–¡ Texture optimization
â–¡ Object reuse
â–¡ Instancing where useful
â–¡ DPR optimization
â–¡ Shadow optimization
â–¡ FPS testing
```

## Phase 10 â€” Polish & Deployment

```text
â–¡ Loading screen
â–¡ Responsive UI
â–¡ Mobile testing
â–¡ Browser testing
â–¡ Production build
â–¡ Deploy
â–¡ Performance audit
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
                 ðŸŒ²        ðŸŒ²

                       â›º

                            ðŸ”¥
                          ðŸªµðŸªµ

            ðŸŒ¿                     ðŸª¨

                 ðŸŒ²        ðŸŒ²
```

The technology should remain intentionally simple:

```text
Vite
 â†“
React
 â†“
React Router
 â†“
React Three Fiber
 â†“
Three.js
 â†“
WebGL
 â†“
GLB
 â†“
Blender
```

The project is designed as a foundation for learning increasingly advanced 3D web development while keeping the first release small, performant, and visually polished.