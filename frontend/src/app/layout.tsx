import "./globals.css";
import Navbar from "../components/Navbar";

export const metadata = {
  title: "Cricket Live Scores",
  description: "Live cricket scores and match updates",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <div className="pt-14 pb-4 px-3 min-h-screen bg-slate-900">
          <div className="cricbuzz-container">{children}</div>
        </div>
      </body>
    </html>
  );
}
