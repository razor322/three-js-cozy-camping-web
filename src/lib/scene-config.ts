export const sceneConfig = {
  camera: {
    position: [12, 10, 12] as [number, number, number],
    fov: 40,
    minDistance: 8,
    maxDistance: 30,
    maxPolarAngle: Math.PI / 2.35,
    minPolarAngle: Math.PI / 6,
  },
  lighting: {
    ambientIntensity: 0.55,
    directionalIntensity: 1.35,
    directionalPosition: [8, 12, 6] as [number, number, number],
  },
  sky: {
    day: "#aee2ff",
  },
} as const;
