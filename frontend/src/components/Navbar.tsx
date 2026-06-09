"use client";

export default function Navbar() {
  return (
    <nav className="navbar-red fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-4 py-2 shadow-md">
      <div className="flex items-center gap-2">
        <div className="navbar-logo">CRICKET</div>
      </div>
      <div className="text-xs font-semibold">Live Scores</div>
    </nav>
  );
}
