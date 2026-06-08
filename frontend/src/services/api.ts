import axios from "axios";
import type { Match } from "../types/match";

export const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 5000,
});

const dummyMatches: Match[] = [
  {
    id: "1",
    tournament: "International Tri-Series",
    teamA: "India",
    teamB: "Australia",
    scoreA: "198/4",
    scoreB: "--",
    overs: "37.2",
    status: "India 198/4 (37.2 ov)",
    live: true,
    scorecard: [
      { id: "b1", name: "Rohit Sharma", runs: 85, balls: 72, fours: 8, sixes: 2, strikeRate: 118.06 },
      { id: "b2", name: "Virat Kohli", runs: 60, balls: 50, fours: 6, sixes: 1, strikeRate: 120 },
    ],
    statistics: {
      teamA: { runs: 198, wickets: 4, overs: "37.2" },
      teamB: { runs: 0, wickets: 0, overs: "0" },
    },
    headToHead: [
      { date: "2025-11-12", tournament: "Asia Cup", winner: "India", margin: "7 wickets" },
    ],
    balls: [
      { over: 37, ball: 2, run: 4, summary: "FOUR by Rohit" },
      { over: 37, ball: 1, run: 1, summary: "Single" },
    ],
    runRate: [
      { over: 1, runRate: 4.2 },
      { over: 10, runRate: 5.1 },
      { over: 20, runRate: 5.6 },
      { over: 30, runRate: 5.4 },
      { over: 37, runRate: 5.33 },
    ],
  },
  {
    id: "2",
    tournament: "County Championship",
    teamA: "England",
    teamB: "Pakistan",
    scoreA: "250/7",
    scoreB: "--",
    overs: "50.0",
    status: "England 250/7 (50.0 ov)",
    live: false,
    live: false,
  },
];

export async function getMatches(): Promise<Match[]> {
  try {
    const res = await API.get<Match[]>("/matches");
    if (res?.data && res.data.length) return res.data;
  } catch (e) {
    // fallback to dummy
  }
  return Promise.resolve(dummyMatches);
}

export async function getMatchById(id: string): Promise<Match | null> {
  try {
    const res = await API.get<Match>(`/matches/${id}`);
    if (res?.data) return res.data;
  } catch (e) {
    // fallback
  }
  const found = dummyMatches.find((m) => m.id === id) || null;
  return Promise.resolve(found);
}
