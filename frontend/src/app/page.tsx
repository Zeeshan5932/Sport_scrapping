import { getMatches } from "../services/api";
import MatchCard from "../components/MatchCard";

export const revalidate = 60;

export default async function HomePage() {
  const matches = await getMatches();

  return (
    <div>
      <div className="mb-3">
        <h1 className="text-lg font-bold text-white">Cricket Matches</h1>
      </div>

      <div>
        {matches && matches.length > 0 ? (
          matches.map((match) => <MatchCard key={match.id} match={match} />)
        ) : (
          <div className="compact-section text-center">
            <p className="text-gray-600 text-sm">No matches available</p>
          </div>
        )}
      </div>
    </div>
  );
}
