"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import MatchTabs from "../../../components/MatchTabs";
import { getMatchById } from "../../../services/api";
import type { MatchDetailResponse } from "../../../types/match";

export default function MatchPage() {
  const params = useParams();
  const router = useRouter();
  const [match, setMatch] = useState<MatchDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMatch = async () => {
      setLoading(true);
      try {
        const data = await getMatchById(params.id as string);
        setMatch(data);
      } catch (error) {
        console.error("Error fetching match:", error);
        setMatch(null);
      } finally {
        setLoading(false);
      }
    };

    fetchMatch();
  }, [params.id]);

  if (loading) {
    return (
      <div className="match-detail-container">
        <div className="loading-message">Loading...</div>
      </div>
    );
  }

  if (!match) {
    return (
      <div className="match-detail-container">
        <div className="match-detail-box">
          <div className="empty-state">Match not found</div>
          <button className="back-link" onClick={() => router.back()}>
            ← Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="match-detail-container">
      <div className="match-detail-box">
        <div className="match-header">
          <div className="match-header-title">{match.tournament || "Match"}</div>
          <div className="match-header-teams">
            <span>{match.team1}</span>
            <span>{match.score1}</span>
          </div>
          <div className="match-header-teams" style={{ marginTop: "4px" }}>
            <span>{match.team2}</span>
            <span>{match.score2}</span>
          </div>
          <div className="match-header-status">{match.status}</div>
        </div>

        <div className="match-detail-body">
          <MatchTabs match={match} />
          <button className="back-link mt-3" onClick={() => router.back()}>
            ← Back
          </button>
        </div>
      </div>
    </div>
  );
}

