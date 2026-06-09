"use client";

import type { MatchStats } from "../types/match";

export default function Statistics({ stats }: { stats?: MatchStats[] }) {
  if (!stats || stats.length === 0) {
    return (
      <div className="compact-section">
        <p className="text-xs text-gray-600 text-center">No statistics available</p>
      </div>
    );
  }

  return (
    <div className="compact-section p-2">
      {stats.map((stat, index) => (
        <div key={index} className="stat-item">
          <span className="stat-label">{stat.label}</span>
          <span className="stat-value">{stat.value}</span>
        </div>
      ))}
    </div>
  );
}
