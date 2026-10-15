import { create } from "zustand";

export type SelectableId = "campfire" | "tent" | "lantern";
export type TimeMode = "day" | "sunset" | "night";
export type WeatherMode = "clear" | "rain";

interface CampingState {
  selected: SelectableId | null;
  campfireActive: boolean;
  lanternActive: boolean;
  tentOpen: boolean;
  timeMode: TimeMode;
  weather: WeatherMode;
  autoTime: boolean;
  muted: boolean;
  photoMode: boolean;
  select: (id: SelectableId | null) => void;
  toggleCampfire: () => void;
  toggleLantern: () => void;
  toggleTent: () => void;
  setTimeMode: (mode: TimeMode) => void;
  setWeather: (mode: WeatherMode) => void;
  toggleAutoTime: () => void;
  toggleMuted: () => void;
  setPhotoMode: (on: boolean) => void;
}

export const useCampingStore = create<CampingState>()((set) => ({
  selected: null,
  campfireActive: true,
  lanternActive: true,
  tentOpen: false,
  timeMode: "day",
  weather: "clear",
  autoTime: false,
  muted: true,
  photoMode: false,
  select: (selected) => set({ selected }),
  toggleCampfire: () => set((s) => ({ campfireActive: !s.campfireActive })),
  toggleLantern: () => set((s) => ({ lanternActive: !s.lanternActive })),
  toggleTent: () => set((s) => ({ tentOpen: !s.tentOpen })),
  setTimeMode: (timeMode) => set({ timeMode }),
  setWeather: (weather) => set({ weather }),
  toggleAutoTime: () => set((s) => ({ autoTime: !s.autoTime })),
  toggleMuted: () => set((s) => ({ muted: !s.muted })),
  setPhotoMode: (photoMode) => set({ photoMode }),
}));

export const timeTiers: Record<TimeMode, 0 | 0.5 | 1> = {
  day: 0,
  sunset: 0.5,
  night: 1,
};

export const objectInfo: Record<
  SelectableId,
  { title: string; desc: string; status: string; facts: string[] }
> = {
  campfire: {
    title: "Campfire",
    desc: "The heart of the camp. Click the flame to hear it breathe; rain makes it shrink.",
    status: "Fire",
    facts: ["Warm light reaches ~9m", "Ducks itself when it rains", "Smoke rises while lit"],
  },
  tent: {
    title: "Tent",
    desc: "An A-frame for two. Open the flap to peek at the cream interior.",
    status: "Flap",
    facts: ["Sleeps two campers", "Orange canvas, cream lining", "Flap swings open on click"],
  },
  lantern: {
    title: "Lantern",
    desc: "A little glass lamp. It swings and glows when switched on.",
    status: "Glow",
    facts: ["Swings gently when lit", "Warmer than the moonlight", "Guides the path to the tent"],
  },
};
