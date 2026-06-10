"use client";

import { useState } from "react";
import Scorecard from "./Scorecard";
import Statistics from "./Statistics";
import HeadToHeadComponent from "./HeadToHead";
import type { MatchDetailResponse } from "../types/match";

export default function MatchTabs({ match }: { match: MatchDetailResponse }) {
  const [activeTab, setActiveTab] = useState<"scorecard" | "statistics" | "h2h">("scorecard");

  return (
    <div>
      <div className="tabs-container">
        <button
          onClick={() => setActiveTab("scorecard")}
          className={`tab-button ${activeTab === "scorecard" ? "active" : ""}`}
        >
          Scorecard
        </button>
        <button
          onClick={() => setActiveTab("statistics")}
          className={`tab-button ${activeTab === "statistics" ? "active" : ""}`}
        >
          Stats
        </button>
        <button
          onClick={() => setActiveTab("h2h")}
          className={`tab-button ${activeTab === "h2h" ? "active" : ""}`}
        >
          H2H
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "scorecard" && <Scorecard rows={match.scorecard} />}
        {activeTab === "statistics" && <Statistics stats={match.stats} />}
        {activeTab === "h2h" && <HeadToHeadComponent data={match.head_to_head} />}
      </div>
    </div>
  );
}
