"use client";

import Link from "next/link";
import type { Match } from "../types/match";

export default function MatchCard({ match }: { match: Match }) {
  return (
    <Link href={`/match/${match.id}`}>
      <div className="match-card mb-2">
        <div className="match-header">
          <div className="match-header-text">{match.tournament || "Match"}</div>
        </div>
        <div className="match-body">
          <div className="match-team-row">
            <span className="match-team-name">{match.team1}</span>
            <span className="match-score">{match.score1}</span>
          </div>
          <div className="match-team-row">
            <span className="match-team-name">{match.team2}</span>
            <span className="match-score">{match.score2}</span>
          </div>
          <div className="match-status">{match.status}</div>
        </div>
      </div>
    </Link>
  );
}
