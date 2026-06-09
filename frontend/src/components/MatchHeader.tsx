"use client";

import type { MatchDetailResponse } from "../types/match";

export default function MatchHeader({ match }: { match: MatchDetailResponse }) {
  return (
    <div className="compact-section p-0 overflow-hidden">
      <div className="match-header">
        <div className="match-header-text">{match.tournament || "Match"}</div>
      </div>
      <div className="match-body">
        <div className="flex justify-between items-center mb-2">
          <div>
            <div className="match-team-name">{match.team1}</div>
            <div className="match-score">{match.score1}</div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-600">vs</div>
          </div>
          <div className="text-right">
            <div className="match-team-name">{match.team2}</div>
            <div className="match-score">{match.score2}</div>
          </div>
        </div>
        <div className="match-status text-center">{match.status}</div>
      </div>
    </div>
  );
}
