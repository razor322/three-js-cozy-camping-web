import { useCampingStore, type TimeMode, type WeatherMode } from "../stores/campingStore.ts";

const times: { id: TimeMode; label: string }[] = [
  { id: "day", label: "Day" },
  { id: "sunset", label: "Sunset" },
  { id: "night", label: "Night" },
];

const weathers: { id: WeatherMode; label: string }[] = [
  { id: "clear", label: "Clear" },
  { id: "rain", label: "Rain" },
];

export default function EnvironmentControls() {
  const timeMode = useCampingStore((s) => s.timeMode);
  const weather = useCampingStore((s) => s.weather);
  const setTimeMode = useCampingStore((s) => s.setTimeMode);
  const setWeather = useCampingStore((s) => s.setWeather);

  const labelColor = (active: boolean) =>
    active ? "bg-orange-400 text-slate-900" : "bg-slate-800/70 hover:bg-slate-700";

  return (
    <nav
      aria-label="Environment controls"
      className="pointer-events-auto absolute bottom-4 left-1/2 max-w-[calc(100vw-2rem)] -translate-x-1/2 overflow-x-auto rounded-full bg-black/45 px-2 py-1.5 backdrop-blur max-sm:bottom-3"
    >
      <div className="flex items-center gap-1">
        <span className="sr-only">Time of day</span>
        {times.map(({ id, label }) => (
          <button
            key={id}
            onClick={() => setTimeMode(id)}
            aria-pressed={timeMode === id}
            className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${labelColor(timeMode === id)} focus-visible:outline focus-visible:outline-2`}
          >
            {label}
          </button>
        ))}
        <span className="mx-1 h-4 w-px bg-white/20" />
        <span className="sr-only">Weather</span>
        {weathers.map(({ id, label }) => (
          <button
            key={id}
            onClick={() => setWeather(id)}
            aria-pressed={weather === id}
            className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${labelColor(weather === id)} focus-visible:outline focus-visible:outline-2`}
          >
            {label}
          </button>
        ))}
      </div>
    </nav>
  );
}
