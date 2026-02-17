import type { Metadata } from "next";
import Link from "next/link";

import Navbar from "@/components/Navbar";
import { AuthProvider } from "@/lib/AuthContext";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agri-Senta — Smart Palengke Dashboard",
  description:
    "Track, compare, and forecast commodity prices across Philippine regions.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <Navbar />
          <main>{children}</main>
          <footer className="footer">
          <div className="footer-inner">
            <span>&copy; {new Date().getFullYear()} Agri-Senta &mdash; Smart Palengke Dashboard</span>
            <div className="footer-links">
              <Link href="/about">About</Link>
              <a
                href="https://www.da.gov.ph/price-monitoring/"
                target="_blank"
                rel="noopener noreferrer"
              >
                DA Price Watch
              </a>
              <a
                href="https://openstat.psa.gov.ph/"
                target="_blank"
                rel="noopener noreferrer"
              >
                PSA OpenSTAT
              </a>
            </div>
          </div>
        </footer>
        </AuthProvider>
      </body>
    </html>
  );
}
