import type { Metadata } from "next";
import Link from "next/link";

import "./globals.css";

export const metadata: Metadata = {
  title: "Agri-Senta",
  description: "Smart Palengke Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <header className="nav">
          <div className="nav-inner">
            <span className="title">
              <span className="brand-pill">PH</span>
              Agri-Senta
            </span>
            <Link className="nav-link" href="/">
              Dashboard
            </Link>
            <Link className="nav-link" href="/prices">
              Prices
            </Link>
            <Link className="nav-link" href="/compare">
              Compare
            </Link>
            <Link className="nav-link" href="/forecast">
              Forecast
            </Link>
            <Link className="nav-link" href="/analytics">
              Analytics
            </Link>
            <Link className="nav-link" href="/about">
              About
            </Link>
          </div>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
