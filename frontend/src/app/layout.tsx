// @ts-ignore: Allow importing global css in this environment
import "./globals.css";
import Navbar from "../components/Navbar";

export const metadata = {
  title: "Cricket Live Tracker",
  description: "Live cricket scores and match insights",
};

export default function RootLayout({ children }: { children: any }) {
  return (
    <html lang="en">
      <body className="animated-bg min-h-screen">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <Navbar />
          <main className="mt-6">{children}</main>
        </div>
      </body>
    </html>
  );
}
