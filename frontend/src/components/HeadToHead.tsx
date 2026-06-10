"use client";

import type { HeadToHead } from "../types/match";

export default function HeadToHeadComponent({ data }: { data?: HeadToHead }) {
  if (!data) {
    return <div className="empty-state">No head-to-head data available</div>;
  }

  return (
    <div className="stats-list">
      <div className="stat-row">
        <span className="stat-label">Team 1 Wins</span>
        <span className="stat-value">{data.team1_wins}</span>
      </div>
      <div className="stat-row">
        <span className="stat-label">Team 2 Wins</span>
        <span className="stat-value">{data.team2_wins}</span>
      </div>
    </div>
  );
}
