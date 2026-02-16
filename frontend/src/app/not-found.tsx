import Link from "next/link";
import { SearchX, Home } from "lucide-react";

export default function NotFound() {
  return (
    <section className="page">
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "40vh", gap: "1.5rem" }}>
        <div className="empty-icon" style={{ background: "#eff6ff", color: "var(--agri-blue)" }}>
          <SearchX size={32} />
        </div>
        <div style={{ textAlign: "center", maxWidth: "420px" }}>
          <h2 style={{ margin: "0 0 0.5rem", fontSize: "1.25rem" }}>Page not found</h2>
          <p style={{ color: "var(--muted)", margin: "0 0 1.5rem", fontSize: "0.9rem" }}>
            The page you requested does not exist or has been moved.
          </p>
          <Link className="btn" href="/" style={{ display: "inline-flex", alignItems: "center", gap: "0.5rem" }}>
            <Home size={16} />
            Go back to dashboard
          </Link>
        </div>
      </div>
    </section>
  );
}
