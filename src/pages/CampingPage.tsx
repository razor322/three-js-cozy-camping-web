import EnvironmentControls from "../components/EnvironmentControls.tsx";
import LoadingScreen from "../components/LoadingScreen.tsx";
import ObjectPanel from "../components/ObjectPanel.tsx";
import CampingScene from "../scenes/camping/CampingScene.tsx";

export default function CampingPage() {
  return (
    <main className="relative min-h-svh bg-[#101623] text-[#f5ead6]">
      <LoadingScreen />
      <CampingScene />
      <header className="pointer-events-none absolute left-4 top-4 max-sm:left-3 max-sm:top-3">
        <h1 className="text-2xl font-semibold max-sm:text-lg">Cozy Camping</h1>
        <p className="text-xs opacity-70 max-sm:hidden">
          drag to orbit · scroll to zoom · click tent / fire / lantern
        </p>
        <p className="hidden text-[11px] opacity-70 max-sm:block">drag · pinch · tap objects</p>
      </header>
      <ObjectPanel />
      <EnvironmentControls />
    </main>
  );
}
