import { useEffect } from "react";
import { useCampingStore, type TimeMode } from "../stores/campingStore.ts";

const order: TimeMode[] = ["day", "sunset", "night"];

// Advances timeMode on a slow loop while autoTime is on. Cycle stops and
// leaves the scene at the current mode when toggled off.
export function useAutoTime(periodMs = 16000) {
  const autoTime = useCampingStore((s) => s.autoTime);
  useEffect(() => {
    if (!autoTime) return;
    const id = window.setInterval(() => {
      const { timeMode, setTimeMode } = useCampingStore.getState();
      setTimeMode(order[(order.indexOf(timeMode) + 1) % order.length]);
    }, periodMs);
    return () => window.clearInterval(id);
  }, [autoTime, periodMs]);
}
