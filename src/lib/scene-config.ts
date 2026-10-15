export const sceneConfig = {
  camera: {
    position: [14, 12, 14] as [number, number, number],
    fov: 45,
    minDistance: 8,
    maxDistance: 30,
    maxPolarAngle: Math.PI / 2.35,
    minPolarAngle: Math.PI / 6,
    // orbit pivot; focus rig lerps controls.target toward the active anchor
    homeTarget: [0, 0.8, 0] as [number, number, number],
  },
  lighting: {
    ambientIntensity: 0.7,
    directionalIntensity: 1.5,
    directionalPosition: [5, 10, 5] as [number, number, number],
  },
  sky: {
    day: "#aee2ff",
  },
} as const;

// Ground flat-top y; props sit on it. Single source for placement + focus.
export const GROUND_Y = 0.8;

// Focus anchor per selectable object: the point the camera dollies to.
// Kept next to the placements so adding an object updates both in one place.
export const focusAnchors = {
  tent: { position: [-2.6, GROUND_Y, -1.8] as [number, number, number], look: [-2.6, GROUND_Y + 1.1, -1.8] as [number, number, number] },
  campfire: { position: [1.2, GROUND_Y, 1.2] as [number, number, number], look: [1.2, GROUND_Y + 0.6, 1.2] as [number, number, number] },
  lantern: { position: [-0.7, GROUND_Y, 0.4] as [number, number, number], look: [-0.7, GROUND_Y + 0.5, 0.4] as [number, number, number] },
} as const;
