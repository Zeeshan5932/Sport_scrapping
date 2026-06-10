import "./globals.css";

export const metadata = {
  title: "Cricket Live Scores",
  description: "Live cricket scores and match updates",
};

function NetworkBackground() {
  return (
    <svg className="network-svg" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice">
      <defs>
        <filter id="blur">
          <feGaussianBlur in="SourceGraphic" stdDeviation="2" />
        </filter>
      </defs>

      {/* Lines */}
      <line x1="100" y1="100" x2="300" y2="300" stroke="rgba(100, 150, 255, 0.3)" strokeWidth="1" filter="url(#blur)" />
      <line x1="300" y1="300" x2="500" y2="200" stroke="rgba(100, 150, 255, 0.3)" strokeWidth="1" filter="url(#blur)" />
      <line x1="500" y1="200" x2="700" y2="400" stroke="rgba(100, 150, 255, 0.3)" strokeWidth="1" filter="url(#blur)" />
      <line x1="100" y1="500" x2="400" y2="600" stroke="rgba(100, 150, 255, 0.3)" strokeWidth="1" filter="url(#blur)" />
      <line x1="400" y1="600" x2="800" y2="500" stroke="rgba(100, 150, 255, 0.3)" strokeWidth="1" filter="url(#blur)" />
      <line x1="800" y1="500" x2="1000" y2="700" stroke="rgba(100, 150, 255, 0.3)" strokeWidth="1" filter="url(#blur)" />
      <line x1="200" y1="700" x2="600" y2="650" stroke="rgba(100, 150, 255, 0.3)" strokeWidth="1" filter="url(#blur)" />

      {/* Nodes */}
      <circle cx="100" cy="100" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="300" cy="300" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="500" cy="200" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="700" cy="400" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="100" cy="500" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="400" cy="600" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="800" cy="500" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="1000" cy="700" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="200" cy="700" r="2" fill="rgba(100, 150, 255, 0.5)" />
      <circle cx="600" cy="650" r="2" fill="rgba(100, 150, 255, 0.5)" />
    </svg>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="network-bg">
          <NetworkBackground />
        </div>

        <div className="navbar">CRICKET LIVE MATCH TRACKER</div>

        <div className="main-content">{children}</div>
      </body>
    </html>
  );
}
