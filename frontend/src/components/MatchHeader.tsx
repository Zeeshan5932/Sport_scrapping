"use client";
import { motion } from "framer-motion";
import type { Match } from "../types/match";

export default function MatchHeader({ match }: { match: Match }) {
  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="w-full rounded-b-md overflow-hidden shadow-md"
    >
      <div className="bg-red-600 text-white px-4 py-3 flex items-center justify-between">
        <div>
          <div className="text-sm opacity-90">{match.tournament}</div>
          <div className="flex items-center gap-6 mt-1">
            <div className="text-lg font-bold">{match.teamA}</div>
            <div className="text-lg font-bold">vs</div>
            <div className="text-lg font-bold">{match.teamB}</div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-extrabold">{match.scoreA ?? "-"}</div>
          <div className="text-sm opacity-90">{match.status}</div>
        </div>
      </div>
    </motion.header>
  );
}
