"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import type { Match } from "../types/match";

export default function MatchCard({ match }: { match: Match }) {
  return (
    <motion.div
      layout
      whileHover={{ y: -6 }}
      className="bg-white/5 backdrop-blur-sm rounded-xl p-4 shadow-lg hover:shadow-2xl transition-shadow"
    >
      <Link href={`/match/${match.id}`} className="block">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1">
            <div className="flex items-center gap-3">
              <div className="text-sm text-slate-300">{match.tournament}</div>
              {match.live && (
                <div className="ml-2 text-xs bg-red-600 text-white px-2 py-0.5 rounded-full">LIVE</div>
              )}
            </div>
            <div className="mt-3 flex items-center gap-6">
              <div className="flex flex-col">
                <div className="text-white font-semibold">{match.teamA}</div>
                <div className="text-slate-300 text-sm">{match.scoreA ?? "-"}</div>
              </div>
              <div className="flex flex-col">
                <div className="text-white font-semibold">{match.teamB}</div>
                <div className="text-slate-300 text-sm">{match.scoreB ?? "-"}</div>
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-slate-300">{match.overs ?? "-"}</div>
            <div className="mt-2 text-xs text-amber-100">{match.status}</div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
