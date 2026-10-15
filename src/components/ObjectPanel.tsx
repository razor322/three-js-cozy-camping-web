import { useEffect, useRef } from "react";
import { objectInfo, useCampingStore, type SelectableId } from "../stores/campingStore.ts";
import type { JSX } from "react";

const ICONS: Record<SelectableId, JSX.Element> = {
  campfire: (
    <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
      <path d="M12 3c1.5 3 4 4.5 4 7a4 4 0 1 1-8 0c0-2.5 2.5-4 4-7Z" />
      <path d="M12 20a5 5 0 0 1-5-5" strokeLinecap="round" />
    </svg>
  ),
  tent: (
    <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
      <path d="M12 4 3 20h18L12 4Z" />
      <path d="M12 4v16" />
    </svg>
  ),
  lantern: (
    <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
      <path d="M9 4h6l1 3H8l1-3Z" />
      <path d="M8 7h8v11H8z" />
      <path d="M12 2v2M10 20h4" strokeLinecap="round" />
    </svg>
  ),
};

export default function ObjectPanel() {
  const selected = useCampingStore((s) => s.selected);
  const select = useCampingStore((s) => s.select);
  const campfireActive = useCampingStore((s) => s.campfireActive);
  const lanternActive = useCampingStore((s) => s.lanternActive);
  const tentOpen = useCampingStore((s) => s.tentOpen);
  const toggleCampfire = useCampingStore((s) => s.toggleCampfire);
  const toggleLantern = useCampingStore((s) => s.toggleLantern);
  const toggleTent = useCampingStore((s) => s.toggleTent);
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") select(null);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [select]);

  useEffect(() => {
    if (selected) closeRef.current?.focus();
  }, [selected]);

  if (!selected) return null;
  const info = objectInfo[selected];

  const toggle =
    selected === "campfire"
      ? { on: campfireActive, fn: toggleCampfire, onLabel: "Let it die", offLabel: "Light the fire" }
      : selected === "lantern"
        ? { on: lanternActive, fn: toggleLantern, onLabel: "Turn it off", offLabel: "Light the lantern" }
        : selected === "tent"
          ? { on: tentOpen, fn: toggleTent, onLabel: "Close the flap", offLabel: "Open the flap" }
          : null;

  const stateValue =
    selected === "campfire" ? (campfireActive ? "Burning" : "Out")
      : selected === "lantern" ? (lanternActive ? "Lit" : "Dark")
        : tentOpen ? "Open" : "Closed";

  return (
    <aside
      role="dialog"
      aria-labelledby="object-panel-title"
      className="absolute right-4 top-4 w-60 rounded-xl bg-black/55 p-4 backdrop-blur-sm max-sm:right-3 max-sm:top-3 max-sm:w-48 max-sm:p-3"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="text-orange-300">{ICONS[selected]}</span>
          <h2 id="object-panel-title" className="text-base font-semibold tracking-wide">
            {info.title}
          </h2>
        </div>
        <button
          ref={closeRef}
          type="button"
          aria-label="Close panel"
          onClick={() => select(null)}
          className="flex size-9 items-center justify-center rounded text-lg leading-none opacity-80 hover:opacity-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-300"
        >
          ×
        </button>
      </div>

      <dl className="mt-2 flex items-center gap-2 text-xs">
        <dt className="opacity-60">{info.status}</dt>
        <dd className="font-medium">{stateValue}</dd>
      </dl>

      <p className="mt-2 text-xs leading-relaxed opacity-80">{info.desc}</p>

      <ul className="mt-2 space-y-1">
        {info.facts.map((f) => (
          <li key={f} className="flex gap-1.5 text-[11px] leading-snug opacity-70">
            <span aria-hidden="true" className="text-orange-300">·</span>
            {f}
          </li>
        ))}
      </ul>

      {toggle && (
        <button
          type="button"
          onClick={toggle.fn}
          aria-pressed={toggle.on}
          className="mt-3 min-h-11 w-full rounded-lg bg-orange-500/90 px-3 text-sm font-medium text-black hover:bg-orange-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-300"
        >
          {toggle.on ? toggle.onLabel : toggle.offLabel}
        </button>
      )}
    </aside>
  );
}
