"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Tags,
  GitCompareArrows,
  TrendingUp,
  BarChart3,
  Info,
  Menu,
  X,
  Wheat,
} from "lucide-react";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/prices", label: "Prices", icon: Tags },
  { href: "/compare", label: "Compare", icon: GitCompareArrows },
  { href: "/forecast", label: "Forecast", icon: TrendingUp },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/about", label: "About", icon: Info },
];

export default function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="nav">
      <div className="nav-inner">
        <Link href="/" className="nav-brand" onClick={() => setOpen(false)}>
          <span className="nav-logo">
            <Wheat size={20} />
          </span>
          <span>
            <span className="nav-brand-text">Agri-Senta</span>
            <br />
            <span className="nav-brand-sub">Smart Palengke</span>
          </span>
        </Link>

        <button
          className="nav-toggle"
          onClick={() => setOpen(!open)}
          aria-label="Toggle navigation"
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>

        <nav className={`nav-links${open ? " open" : ""}`}>
          {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
            const isActive =
              href === "/" ? pathname === "/" : pathname.startsWith(href);

            return (
              <Link
                key={href}
                href={href}
                className="nav-link"
                onClick={() => setOpen(false)}
                style={
                  isActive
                    ? {
                        background: "var(--agri-blue-light)",
                        color: "var(--agri-blue)",
                        fontWeight: 600,
                      }
                    : undefined
                }
              >
                <Icon size={16} />
                {label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
