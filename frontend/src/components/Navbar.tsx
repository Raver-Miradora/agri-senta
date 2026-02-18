"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
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
  Shield,
  LogIn,
  LogOut,
  Sun,
  Moon,
} from "lucide-react";
import { useAuth } from "@/lib/AuthContext";
import { useTheme } from "@/lib/ThemeContext";

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
  const router = useRouter();
  const { user, loading, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [open, setOpen] = useState(false);

  const handleLogout = () => {
    logout();
    setOpen(false);
    router.push("/");
  };

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

          {/* Admin link – only for admin users */}
          {user?.is_admin && (
            <Link
              href="/admin"
              className="nav-link"
              onClick={() => setOpen(false)}
              style={
                pathname.startsWith("/admin")
                  ? {
                      background: "var(--agri-blue-light)",
                      color: "var(--agri-blue)",
                      fontWeight: 600,
                    }
                  : undefined
              }
            >
              <Shield size={16} />
              Admin
            </Link>
          )}

          {/* Auth button */}
          {!loading && (
            user ? (
              <button
                className="nav-link"
                onClick={handleLogout}
                style={{ cursor: "pointer", border: "none", background: "none", font: "inherit" }}
              >
                <LogOut size={16} />
                Logout
              </button>
            ) : (
              <Link
                href="/login"
                className="nav-link"
                onClick={() => setOpen(false)}
                style={
                  pathname === "/login"
                    ? {
                        background: "var(--agri-blue-light)",
                        color: "var(--agri-blue)",
                        fontWeight: 600,
                      }
                    : undefined
                }
              >
                <LogIn size={16} />
                Login
              </Link>
            )
          )}
        </nav>

        <button
          className="theme-toggle"
          onClick={toggleTheme}
          aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
        >
          {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </div>
    </header>
  );
}
