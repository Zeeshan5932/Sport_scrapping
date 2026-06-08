import MatchHeader from "../../../components/MatchHeader";
import RunRateGraph from "../../../components/RunRateGraph";
import BallTimeline from "../../../components/BallTimeline";
import MatchTabs from "../../../components/MatchTabs";
import { getMatchById } from "../../../services/api";

interface Props {
  params: { id: string };
}

export default async function MatchPage({ params }: Props) {
  const match = await getMatchById(params.id);

  if (!match) {
    return <div className="p-6 text-slate-300">Match not found</div>;
  }

  return (
    <div className="space-y-6">
      <MatchHeader match={match} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          <div className="glass-card p-4 rounded-lg">
            <h3 className="text-sm text-slate-300">Run Rate</h3>
            <RunRateGraph data={match.runRate} />
          </div>

          <div className="glass-card p-4 rounded-lg">
            <h3 className="text-sm text-slate-300">Ball Timeline</h3>
            <BallTimeline balls={match.balls} />
          </div>

          <div className="glass-card p-4 rounded-lg">
            <MatchTabs match={match} />
          </div>
        </div>

        <aside className="space-y-4">
          <div className="glass-card p-4 rounded-lg">
            <h3 className="text-sm text-slate-300">Match Info</h3>
            <div className="mt-2 text-white">{match.tournament}</div>
            <div className="text-slate-300 text-sm">Status: {match.status}</div>
          </div>
        </aside>
      </div>
    </div>
  );
}
