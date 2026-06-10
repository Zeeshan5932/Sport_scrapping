"use client";

import MatchRow from "./MatchRow";
import type { Match } from "../types/match";

interface TournamentSectionProps {
  tournament: string;
  matches: Match[];
}

export default function TournamentSection({ tournament, matches }: TournamentSectionProps) {
  return (
    <div>
      <div className="tournament-header">{tournament}</div>
      {matches.map((match) => (
        <MatchRow key={match.id} match={match} />
      ))}
    </div>
  );
}
