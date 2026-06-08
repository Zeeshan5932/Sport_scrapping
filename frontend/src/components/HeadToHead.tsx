import type { HeadToHeadItem } from "../types/match";

export default function HeadToHead({ items }: { items?: HeadToHeadItem[] }) {
  if (!items || items.length === 0) {
    return <div className="p-6 text-slate-300">No head-to-head data</div>;
  }

  return (
    <div className="space-y-3">
      {items.map((h, idx) => (
        <div key={idx} className="p-3 bg-white/5 rounded-lg flex items-center justify-between">
          <div>
            <div className="text-white font-medium">{h.tournament}</div>
            <div className="text-slate-300 text-sm">{h.date}</div>
          </div>
          <div className="text-right text-slate-200">
            <div className="font-semibold">{h.winner}</div>
            <div className="text-sm">{h.margin}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
