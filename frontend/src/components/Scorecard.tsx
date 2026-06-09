"use client";

import type { ScorecardEntry } from "../types/match";

export default function Scorecard({ rows }: { rows?: ScorecardEntry[] }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="compact-section">
        <p className="text-xs text-gray-600 text-center">No batting data available</p>
      </div>
    );
  }

  return (
    <div className="compact-section p-2 overflow-x-auto">
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
                <td className="text-left font-medium text-gray-900">{row.name}</td>
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
