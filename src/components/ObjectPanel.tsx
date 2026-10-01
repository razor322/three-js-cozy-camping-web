import { useEffect } from "react";
import { objectInfo, useCampingStore } from "../stores/campingStore.ts";

export default function ObjectPanel() {
  const selected = useCampingStore((s) => s.selected);
  const select = useCampingStore((s) => s.select);
  const campfireActive = useCampingStore((s) => s.campfireActive);
  const lanternActive = useCampingStore((s) => s.lanternActive);
  const toggleCampfire = useCampingStore((s) => s.toggleCampfire);
  const toggleLantern = useCampingStore((s) => s.toggleLantern);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") select(null);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [select]);

  if (!selected) return null;
  const info = objectInfo[selected];
  const toggle =
    selected === "campfire"
      ? { on: campfireActive, fn: toggleCampfire, label: "Fire" }
      : selected === "lantern"
        ? { on: lanternActive, fn: toggleLantern, label: "Lantern" }
        : null;

  return (
    <aside className="absolute right-4 top-4 w-56 rounded-xl bg-black/55 p-4 backdrop-blur-sm max-sm:right-3 max-sm:top-3 max-sm:w-44 max-sm:p-3">
      <div className="flex items-start justify-between gap-2">
        <h2 className="text-base font-semibold uppercase tracking-wide">{info.title}</h2>
        <button
          aria-label="Close panel"
          onClick={() => select(null)}
          className="rounded px-1.5 text-lg leading-none opacity-70 hover:opacity-100 focus-visible:outline focus-visible:outline-2"
        >
          ×
        </button>
      </div>
      <p className="mt-1 text-xs leading-relaxed opacity-80">{info.desc}</p>
      {toggle && (
        <button
          onClick={toggle.fn}
          aria-pressed={toggle.on}
          className="mt-3 w-full rounded-lg bg-orange-500/90 px-3 py-1.5 text-sm font-medium text-black hover:bg-orange-400 focus-visible:outline focus-visible:outline-2"
        >
          Turn {toggle.label} {toggle.on ? "Off" : "On"}
        </button>
      )}
    </aside>
  );
}
