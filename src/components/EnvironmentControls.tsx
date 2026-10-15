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
  const autoTime = useCampingStore((s) => s.autoTime);
  const muted = useCampingStore((s) => s.muted);
  const setTimeMode = useCampingStore((s) => s.setTimeMode);
  const setWeather = useCampingStore((s) => s.setWeather);
  const toggleAutoTime = useCampingStore((s) => s.toggleAutoTime);
  const toggleMuted = useCampingStore((s) => s.toggleMuted);
  const photoMode = useCampingStore((s) => s.photoMode);
  const setPhotoMode = useCampingStore((s) => s.setPhotoMode);

  const pill = (active: boolean) =>
    `min-h-11 shrink-0 rounded-full px-3.5 text-xs font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-300 ${
      active ? "bg-orange-400 text-slate-900" : "bg-slate-800/70 text-[#f5ead6] hover:bg-slate-700"
    }`;

  return (
    <nav
      aria-label="Camp controls"
      className="pointer-events-auto absolute bottom-4 left-1/2 flex max-w-[calc(100vw-2rem)] -translate-x-1/2 items-center gap-1 overflow-x-auto rounded-full bg-black/50 px-2 py-1.5 backdrop-blur max-sm:bottom-3"
    >
      <span className="sr-only">Time of day</span>
      {times.map(({ id, label }) => (
        <button key={id} type="button" onClick={() => setTimeMode(id)} aria-pressed={timeMode === id} className={pill(timeMode === id)}>
          {label}
        </button>
      ))}
      <button
        type="button"
        onClick={toggleAutoTime}
        aria-pressed={autoTime}
        title="Cycle day, sunset and night automatically"
        className={pill(autoTime)}
      >
        Auto
      </button>
      <span className="mx-1 h-4 w-px shrink-0 bg-white/20" aria-hidden="true" />
      <span className="sr-only">Weather</span>
      {weathers.map(({ id, label }) => (
        <button key={id} type="button" onClick={() => setWeather(id)} aria-pressed={weather === id} className={pill(weather === id)}>
          {label}
        </button>
      ))}
      <span className="mx-1 h-4 w-px shrink-0 bg-white/20" aria-hidden="true" />
      <button
        type="button"
        onClick={toggleMuted}
        aria-pressed={!muted}
        aria-label={muted ? "Unmute ambience" : "Mute ambience"}
        title={muted ? "Sound off" : "Sound on"}
        className={pill(!muted)}
      >
        {muted ? "Sound off" : "Sound on"}
      </button>
      <span className="mx-1 h-4 w-px shrink-0 bg-white/20" aria-hidden="true" />
      <button
        type="button"
        onClick={() => setPhotoMode(!photoMode)}
        aria-pressed={photoMode}
        title="Hide the interface and download a photo"
        className={pill(photoMode)}
      >
        Photo
      </button>
    </nav>
  );
}
