"use client";

import type { MatchStats } from "../types/match";

export default function Statistics({ stats }: { stats?: MatchStats[] }) {
  if (!stats || stats.length === 0) {
    return <div className="empty-state">No statistics available</div>;
  }

  return (
    <div className="stats-list">
      {stats.map((stat, index) => (
        <div key={index} className="stat-row">
          <span className="stat-label">{stat.label}</span>
          <span className="stat-value">{stat.value}</span>
        </div>
      ))}
    </div>
  );
}
