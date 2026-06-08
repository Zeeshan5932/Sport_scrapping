"use client";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import type { RunRatePoint } from "../types/match";

export default function RunRateGraph({ data }: { data?: RunRatePoint[] }) {
  if (!data || data.length === 0) return <div className="p-6 text-slate-300">No run-rate data</div>;

  return (
    <div className="w-full h-64 bg-white/5 rounded-lg p-2">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
          <XAxis dataKey="over" stroke="#9CA3AF" />
          <YAxis stroke="#9CA3AF" />
          <Tooltip wrapperClassName="text-sm" />
          <Line type="monotone" dataKey="runRate" stroke="#fb7185" strokeWidth={3} dot={{ r: 2 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
