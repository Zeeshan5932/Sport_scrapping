import MatchHeader from "../../../components/MatchHeader";
import MatchTabs from "../../../components/MatchTabs";
import Link from "next/link";
import { getMatchById } from "../../../services/api";

export const revalidate = 60;

interface Props {
  params: { id: string };
}

export default async function MatchPage({ params }: Props) {
  const match = await getMatchById(params.id);

  if (!match) {
    return (
      <div className="compact-section text-center">
        <p className="text-gray-600 text-sm mb-2">Match not found</p>
        <Link href="/" className="text-red-600 text-xs font-semibold hover:underline">
          Back to Matches
        </Link>
      </div>
    );
  }

  return (
    <div>
      <Link
        href="/"
        className="inline-block text-red-600 text-xs font-semibold mb-3 hover:underline"
      >
        ← Back
      </Link>

      <MatchHeader match={match} />

      <div className="mt-3">
        <MatchTabs match={match} />
      </div>
    </div>
  );
}
