import EnvironmentControls from "../components/EnvironmentControls.tsx";
import LoadingScreen from "../components/LoadingScreen.tsx";
import ObjectPanel from "../components/ObjectPanel.tsx";
import PhotoMode from "../components/PhotoMode.tsx";
import CampingScene from "../scenes/camping/CampingScene.tsx";
import { useAmbience } from "../effects/useAmbience.ts";
import { useAutoTime } from "../effects/useAutoTime.ts";
import { useCampingStore, type TimeMode } from "../stores/campingStore.ts";

// Mounts side-effects that must run outside the Canvas: audio graph and the
// auto-cycle timer. Rendered once so both survive the whole page lifetime.
function SceneHooks() {
  useAmbience();
  useAutoTime();
  return null;
}

const CLOCK: Record<TimeMode, string> = {
  day: "12:00",
  sunset: "18:30",
  night: "21:42",
};

function StatusLine() {
  const timeMode = useCampingStore((s) => s.timeMode);
  const weather = useCampingStore((s) => s.weather);
  const autoTime = useCampingStore((s) => s.autoTime);
  return (
    <p className="text-xs capitalize opacity-70 max-sm:hidden">
      {CLOCK[timeMode]} · {timeMode} · {weather}
      {autoTime ? " · cycling" : ""}
    </p>
  );
}

export default function CampingPage() {
  const photoMode = useCampingStore((s) => s.photoMode);
  return (
    <main className="relative min-h-svh bg-[#101623] text-[#f5ead6]">
      <SceneHooks />
      <LoadingScreen />
      <CampingScene />
      {!photoMode && (
        <>
          <header className="pointer-events-none absolute left-4 top-4 max-sm:left-3 max-sm:top-3">
            <h1 className="text-2xl font-semibold max-sm:text-lg">Cozy Camping</h1>
            <StatusLine />
            <p className="text-xs opacity-60 max-sm:hidden">
              drag to orbit · scroll to zoom · click tent / fire / lantern
            </p>
            <p className="hidden text-[11px] opacity-60 max-sm:block">drag · pinch · tap objects</p>
          </header>
          <ObjectPanel />
          <EnvironmentControls />
          <footer className="pointer-events-none absolute bottom-1 left-1/2 -translate-x-1/2 text-[10px] tracking-wide text-[#f5ead6]/40 max-sm:hidden">
            Low-poly diorama · Blender to GLB · React Three Fiber
          </footer>
        </>
      )}
      <PhotoMode />
    </main>
  );
}
