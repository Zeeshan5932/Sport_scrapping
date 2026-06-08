import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="w-full bg-transparent px-4 py-3 flex items-center justify-between">
      <Link href="/" className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-red-500 to-yellow-400 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
          CB
        </div>
        <div className="text-white font-semibold text-lg">Cricket Live Tracker</div>
      </Link>
      <div className="text-sm text-slate-200 hidden sm:block">Live scores • Insights • Stats</div>
    </nav>
  );
}
