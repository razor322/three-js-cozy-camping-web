import { useEffect } from "react";
import { useCampingStore } from "../stores/campingStore.ts";

export default function PhotoMode() {
  const photoMode = useCampingStore((s) => s.photoMode);
  const setPhotoMode = useCampingStore((s) => s.setPhotoMode);

  useEffect(() => {
    if (!photoMode) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setPhotoMode(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [photoMode, setPhotoMode]);

  if (!photoMode) return null;

  const capture = () => {
    const canvas = document.querySelector("canvas");
    if (!canvas) return;
    try {
      const url = canvas.toDataURL("image/png");
      const a = document.createElement("a");
      a.href = url;
      a.download = `cozy-camping-${Date.now()}.png`;
      a.click();
    } catch (err) {
      console.error("Photo capture failed", err);
    }
  };

  return (
    <div className="absolute inset-x-0 bottom-4 flex justify-center gap-2 max-sm:bottom-3">
      <button
        type="button"
        onClick={capture}
        className="min-h-11 rounded-full bg-orange-500/90 px-5 text-sm font-medium text-black hover:bg-orange-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-300"
      >
        Download photo
      </button>
      <button
        type="button"
        onClick={() => setPhotoMode(false)}
        aria-label="Exit photo mode"
        className="min-h-11 rounded-full bg-slate-800/80 px-5 text-sm font-medium text-[#f5ead6] hover:bg-slate-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-300"
      >
        Exit
      </button>
    </div>
  );
}
