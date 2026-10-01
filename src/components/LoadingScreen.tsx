import { useProgress } from "@react-three/drei";

export default function LoadingScreen() {
  const { progress, active } = useProgress();
  if (!active) return null;
  return (
    <div
      role="status"
      aria-live="polite"
      className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-3 bg-[#101623]"
    >
      <h1 className="text-3xl font-semibold tracking-wide">COZY CAMPING</h1>
      <p className="text-xs opacity-70">Loading diorama… {Math.round(progress)}%</p>
      <div className="h-1.5 w-48 overflow-hidden rounded-full bg-white/15">
        <div
          className="h-full rounded-full bg-orange-400 transition-[width]"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
}
