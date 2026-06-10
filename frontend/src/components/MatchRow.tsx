"use client";

import Link from "next/link";
import type { Match } from "../types/match";

interface MatchRowProps {
  match: Match;
}

export default function MatchRow({ match }: MatchRowProps) {
  return (
    <Link href={`/match/${match.id}`}>
      <div className="match-row">
        <div className="match-row-teams">
          <div className="match-team-left">{match.team1}</div>
          <div className="match-score-center">{match.score1}</div>
          <div className="match-team-right">{match.team2}</div>
        </div>
        <div className="match-row-teams">
          <div className="match-score-center" style={{ width: "100%" }}>
            {/* Second row for score/status */}
          </div>
        </div>
        <div className="match-status">{match.status}</div>
      </div>
    </Link>
  );
}
