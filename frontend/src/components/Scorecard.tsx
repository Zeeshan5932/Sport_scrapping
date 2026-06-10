"use client";

import type { ScorecardEntry } from "../types/match";

export default function Scorecard({ rows }: { rows?: ScorecardEntry[] }) {
  if (!rows || rows.length === 0) {
    return <div className="empty-state">No batting data available</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="scorecard-table">
        <thead>
          <tr>
            <th>Batsman</th>
            <th>R</th>
            <th>B</th>
            <th>4s</th>
            <th>6s</th>
            <th>SR</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => {
            const sr = row.strike_rate ?? row.strikeRate ?? 0;
            return (
              <tr key={index}>
                <td>{row.name}</td>
                <td>{row.runs}</td>
                <td>{row.balls}</td>
                <td>{row.fours}</td>
                <td>{row.sixes}</td>
                <td>{sr.toFixed(2)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
