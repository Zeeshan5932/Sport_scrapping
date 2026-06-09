"use client";

import type { HeadToHead } from "../types/match";

export default function HeadToHeadComponent({ data }: { data?: HeadToHead }) {
  if (!data) {
    return (
      <div className="compact-section">
        <p className="text-xs text-gray-600 text-center">No head-to-head data available</p>
      </div>
    );
  }

  return (
    <div className="compact-section p-2">
      <div className="stat-item">
        <span className="stat-label">Team 1 Wins</span>
        <span className="stat-value">{data.team1_wins}</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">Team 2 Wins</span>
        <span className="stat-value">{data.team2_wins}</span>
      </div>
    </div>
  );
}
