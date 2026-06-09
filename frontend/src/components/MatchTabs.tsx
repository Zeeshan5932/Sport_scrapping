"use client";

import { useState } from "react";
import Scorecard from "./Scorecard";
import Statistics from "./Statistics";
import HeadToHeadComponent from "./HeadToHead";
import type { MatchDetailResponse } from "../types/match";

export default function MatchTabs({ match }: { match: MatchDetailResponse }) {
  const [activeTab, setActiveTab] = useState<"scorecard" | "statistics" | "h2h">("scorecard");

  return (
    <div className="compact-section p-0 overflow-hidden">
      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setActiveTab("scorecard")}
          className={`tab-button flex-1 ${activeTab === "scorecard" ? "active" : ""}`}
        >
          Scorecard
        </button>
        <button
          onClick={() => setActiveTab("statistics")}
          className={`tab-button flex-1 ${activeTab === "statistics" ? "active" : ""}`}
        >
          Stats
        </button>
        <button
          onClick={() => setActiveTab("h2h")}
          className={`tab-button flex-1 ${activeTab === "h2h" ? "active" : ""}`}
        >
          H2H
        </button>
      </div>

      <div className="p-2">
        {activeTab === "scorecard" && <Scorecard rows={match.scorecard} />}
        {activeTab === "statistics" && <Statistics stats={match.stats} />}
        {activeTab === "h2h" && <HeadToHeadComponent data={match.head_to_head} />}
      </div>
    </div>
  );
}
