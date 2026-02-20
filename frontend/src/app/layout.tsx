import type { Metadata } from "next";
import Link from "next/link";

import Navbar from "@/components/Navbar";
import { AuthProvider } from "@/lib/AuthContext";
import { ThemeProvider } from "@/lib/ThemeContext";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agri-Senta — Lagonoy Smart Agricultural Price Tracker",
  description:
    "Smart agricultural price tracker & dashboard for the Municipal Agriculture Office of Lagonoy, Camarines Sur.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
        <AuthProvider>
          <Navbar />
          <main>{children}</main>
          <footer className="footer">
          <div className="footer-inner">
            <span>&copy; {new Date().getFullYear()} Agri-Senta &mdash; Municipal Agriculture Office, Lagonoy</span>
            <div className="footer-links">
              <Link href="/about">About</Link>
              <Link href="/price-board">Price Board</Link>
              <a
                href="https://www.da.gov.ph/price-monitoring/"
                target="_blank"
                rel="noopener noreferrer"
              >
                DA Price Watch
              </a>
            </div>
          </div>
        </footer>
        </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
