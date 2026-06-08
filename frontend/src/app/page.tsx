import { getMatches } from "../services/api";
import MatchCard from "../components/MatchCard";

export default async function Page() {
  const matches = await getMatches();

  return (
    <div>
      <section className="mb-6">
        <h1 className="text-3xl font-extrabold text-white">Cricket Live Tracker</h1>
        <p className="text-slate-300 mt-2">Live scores, stats and match insights</p>
      </section>

      <section>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {matches && matches.length ? (
            matches.map((m) => (
              <div key={m.id}>
                <MatchCard match={m} />
              </div>
            ))
          ) : (
            <div className="p-6 text-slate-300">No matches available</div>
          )}
        </div>
      </section>
    </div>
  );
}
