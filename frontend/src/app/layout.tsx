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
            <span className="title">Agri-Senta</span>
            <Link href="/">Dashboard</Link>
            <Link href="/prices">Prices</Link>
            <Link href="/compare">Compare</Link>
            <Link href="/forecast">Forecast</Link>
            <Link href="/analytics">Analytics</Link>
            <Link href="/about">About</Link>
          </div>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
