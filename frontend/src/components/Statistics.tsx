import type { Statistics as StatsType } from "../types/match";

export default function Statistics({ stats }: { stats?: StatsType }) {
  if (!stats) return <div className="p-6 text-slate-300">Statistics unavailable</div>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div className="p-4 bg-white/5 rounded-lg">
        <div className="text-slate-300 text-sm">{stats.teamA && "Team A"}</div>
        <div className="text-white font-bold text-xl">{stats.teamA.runs}/{stats.teamA.wickets}</div>
        <div className="text-slate-300">Overs: {stats.teamA.overs}</div>
      </div>
      <div className="p-4 bg-white/5 rounded-lg">
        <div className="text-slate-300 text-sm">{stats.teamB && "Team B"}</div>
        <div className="text-white font-bold text-xl">{stats.teamB.runs}/{stats.teamB.wickets}</div>
        <div className="text-slate-300">Overs: {stats.teamB.overs}</div>
      </div>
    </div>
  );
}
