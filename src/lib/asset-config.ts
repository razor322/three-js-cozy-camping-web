export const assets = {
  ground: "/models/ground.glb",
  pineTree: "/models/pine-tree.glb",
  tent: "/models/tent.glb",
  campfire: "/models/campfire.glb",
  rocks: "/models/rocks.glb",
  bush: "/models/bush.glb",
  lantern: "/models/lantern.glb",
  stump: "/models/stump.glb",
} as const;

export type AssetKey = keyof typeof assets;
