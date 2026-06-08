"use client";
import { useState } from "react";
import Scorecard from "./Scorecard";
import Statistics from "./Statistics";
import HeadToHead from "./HeadToHead";
import type { Match } from "../types/match";

export default function MatchTabs({ match }: { match: Match }) {
  const [tab, setTab] = useState<string>("scorecard");

  return (
    <div>
      <div className="flex gap-2 bg-white/3 rounded-md p-1 mb-4">
        <button
          onClick={() => setTab("scorecard")}
          className={`px-4 py-2 rounded-md text-sm ${tab === "scorecard" ? "bg-white/10 text-white" : "text-slate-300"}`}
        >
          Scorecard
        </button>
        <button
          onClick={() => setTab("statistics")}
          className={`px-4 py-2 rounded-md text-sm ${tab === "statistics" ? "bg-white/10 text-white" : "text-slate-300"}`}
        >
          Statistics
        </button>
        <button
          onClick={() => setTab("h2h")}
          className={`px-4 py-2 rounded-md text-sm ${tab === "h2h" ? "bg-white/10 text-white" : "text-slate-300"}`}
        >
          Head To Head
        </button>
      </div>

      <div>
        {tab === "scorecard" && <Scorecard rows={match.scorecard} />}
        {tab === "statistics" && <Statistics stats={match.statistics} />}
        {tab === "h2h" && <HeadToHead items={match.headToHead} />}
      </div>
    </div>
  );
}
