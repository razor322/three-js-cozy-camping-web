export const sceneConfig = {
  camera: {
    position: [14, 12, 14] as [number, number, number],
    fov: 45,
    minDistance: 8,
    maxDistance: 30,
    maxPolarAngle: Math.PI / 2.35,
    minPolarAngle: Math.PI / 6,
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
