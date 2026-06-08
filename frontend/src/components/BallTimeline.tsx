"use client";
import type { BallEvent } from "../types/match";

export default function BallTimeline({ balls }: { balls?: BallEvent[] }) {
  if (!balls || balls.length === 0) return <div className="p-4 text-slate-300">No recent balls</div>;

  return (
    <div className="flex gap-2 overflow-x-auto py-2">
      {balls.map((b, i) => (
        <div key={i} className="min-w-[140px] p-3 bg-white/5 rounded-md text-slate-200">
          <div className="text-sm">Over {b.over}.{b.ball}</div>
          <div className="font-semibold text-white">{b.run} runs</div>
          <div className="text-xs text-slate-300">{b.summary}</div>
        </div>
      ))}
    </div>
  );
}
