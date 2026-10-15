import { useEffect, useRef } from "react";
import { useCampingStore } from "../stores/campingStore.ts";

// Procedural ambience: fire crackle (noise bursts through a bandpass) and
// night crickets (detuned short sine chirps). No audio files, no autoplay.
// PRD §37: user-controlled, muted by default, nothing plays until unmuted.
export function useAmbience() {
  const active = useCampingStore((s) => s.campfireActive);
  const timeMode = useCampingStore((s) => s.timeMode);
  const weather = useCampingStore((s) => s.weather);
  const muted = useCampingStore((s) => s.muted);

  const ctxRef = useRef<AudioContext | null>(null);
  const nodesRef = useRef<{ master: GainNode; fire: GainNode; crickets: GainNode } | null>(null);
  const fireTimer = useRef<number | null>(null);

  // build the graph once, on first unmute (needs a user gesture to start)
  useEffect(() => {
    if (muted || ctxRef.current) return;
    const Ctor = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const ctx = new Ctor();
    const master = ctx.createGain();
    master.gain.value = 0;
    master.connect(ctx.destination);

    // fire: brown-ish noise buffer, looping, band-limited for a crackle bed
    const fire = ctx.createGain();
    fire.gain.value = 0;
    const fireFilter = ctx.createBiquadFilter();
    fireFilter.type = "bandpass";
    fireFilter.frequency.value = 380;
    fireFilter.Q.value = 0.8;
    const fireSrc = ctx.createBufferSource();
    fireSrc.buffer = makeNoise(ctx);
    fireSrc.loop = true;
    fireSrc.connect(fireFilter).connect(fire).connect(master);
    fireSrc.start();

    // crickets: a high sines bed, gated on only at night by the volume effect
    const crickets = ctx.createGain();
    crickets.gain.value = 0;
    const cricketOsc = ctx.createOscillator();
    cricketOsc.type = "sine";
    cricketOsc.frequency.value = 4200;
    const cricketLfo = ctx.createOscillator();
    cricketLfo.frequency.value = 7.5;
    const cricketLfoGain = ctx.createGain();
    cricketLfoGain.gain.value = 900;
    cricketLfo.connect(cricketLfoGain).connect(cricketOsc.frequency);
    const cricketTrem = ctx.createGain();
    cricketTrem.gain.value = 0.5;
    cricketOsc.connect(cricketTrem).connect(crickets).connect(master);
    cricketOsc.start();
    cricketLfo.start();

    ctxRef.current = ctx;
    nodesRef.current = { master, fire, crickets };

    // crackle: schedule short noise pops at random intervals
    const pop = () => {
      const n = nodesRef.current;
      if (!n || !ctxRef.current) return;
      const c = ctxRef.current;
      const buf = c.createBuffer(1, c.sampleRate * 0.05, c.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / d.length, 3);
      const s = c.createBufferSource();
      s.buffer = buf;
      const g = c.createGain();
      g.gain.value = 0.5 + Math.random() * 0.5;
      const f = c.createBiquadFilter();
      f.type = "highpass";
      f.frequency.value = 900 + Math.random() * 1500;
      s.connect(f).connect(g).connect(n.fire);
      s.start();
      s.stop(c.currentTime + 0.05);
      fireTimer.current = window.setTimeout(pop, 60 + Math.random() * 260);
    };
    fireTimer.current = window.setTimeout(pop, 200);

    return () => {
      if (fireTimer.current) clearTimeout(fireTimer.current);
      fireSrc.stop();
      cricketOsc.stop();
      cricketLfo.stop();
      void ctx.close();
      ctxRef.current = null;
      nodesRef.current = null;
    };
  }, [muted]);

  // volumes follow scene state; everything is 0 while muted
  useEffect(() => {
    const n = nodesRef.current;
    const ctx = ctxRef.current;
    if (!n || !ctx) return;
    const t = ctx.currentTime;
    const target =
      muted ? 0 : weather === "rain" ? 0.22 : active ? 0.5 : 0.16; // rain ducks the fire
    n.master.gain.setTargetAtTime(target * 0.6, t, 0.4);
    n.fire.gain.setTargetAtTime(active ? 0.9 : 0.1, t, 0.5);
    n.crickets.gain.setTargetAtTime(timeMode === "night" && weather !== "rain" ? 0.05 : 0, t, 0.8);
  }, [muted, active, timeMode, weather]);
}

function makeNoise(ctx: AudioContext): AudioBuffer {
  const len = ctx.sampleRate * 2;
  const buf = ctx.createBuffer(1, len, ctx.sampleRate);
  const d = buf.getChannelData(0);
  let last = 0;
  for (let i = 0; i < len; i++) {
    const white = Math.random() * 2 - 1;
    last = (last + 0.02 * white) / 1.02; // brown-ish, warmer than white
    d[i] = last * 3.5;
  }
  return buf;
}
