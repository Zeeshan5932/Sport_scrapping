"use client";
import type { ScorecardEntry } from "../types/match";

export default function Scorecard({ rows }: { rows?: ScorecardEntry[] }) {
  if (!rows || rows.length === 0) {
    return <div className="p-6 text-center text-slate-300">No batting data available</div>;
  }

  return (
    <div className="overflow-x-auto rounded-lg bg-white/5 p-3">
      <table className="w-full table-auto text-left">
        <thead>
          <tr className="text-slate-300 text-sm">
            <th className="py-2">Batsman</th>
            <th className="py-2">R</th>
            <th className="py-2">B</th>
            <th className="py-2">4s</th>
            <th className="py-2">6s</th>
            <th className="py-2">SR</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id} className="border-t border-white/5">
              <td className="py-2 text-white font-medium">{r.name}</td>
              <td className="py-2 text-slate-200">{r.runs}</td>
              <td className="py-2 text-slate-200">{r.balls}</td>
              <td className="py-2 text-slate-200">{r.fours}</td>
              <td className="py-2 text-slate-200">{r.sixes}</td>
              <td className="py-2 text-slate-200">{r.strikeRate.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
