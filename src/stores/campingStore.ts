import { create } from "zustand";

export type SelectableId = "campfire" | "tent" | "lantern";
export type TimeMode = "day" | "sunset" | "night";
export type WeatherMode = "clear" | "rain";

interface CampingState {
  selected: SelectableId | null;
  campfireActive: boolean;
  lanternActive: boolean;
  timeMode: TimeMode;
  weather: WeatherMode;
  select: (id: SelectableId | null) => void;
  toggleCampfire: () => void;
  toggleLantern: () => void;
  setTimeMode: (mode: TimeMode) => void;
  setWeather: (mode: WeatherMode) => void;
}

export const useCampingStore = create<CampingState>()((set) => ({
  selected: null,
  campfireActive: true,
  lanternActive: true,
  timeMode: "day",
  weather: "clear",
  select: (selected) => set({ selected }),
  toggleCampfire: () => set((s) => ({ campfireActive: !s.campfireActive })),
  toggleLantern: () => set((s) => ({ lanternActive: !s.lanternActive })),
  setTimeMode: (timeMode) => set({ timeMode }),
  setWeather: (weather) => set({ weather }),
}));

export const timeTiers: Record<TimeMode, 0 | 0.5 | 1> = {
  day: 0,
  sunset: 0.5,
  night: 1,
};

export const objectInfo: Record<SelectableId, { title: string; desc: string }> = {
  campfire: {
    title: "Campfire",
    desc: "Click toggle or use the panel button. Flame scales + light flickers when ON.",
  },
  tent: {
    title: "Tent",
    desc: "Orange-cream A-frame for two. Flap hinge ready for open/close.",
  },
  lantern: {
    title: "Lantern",
    desc: "GLB swing + glow-pulse clips play when ON. PointLight follows state.",
  },
};
