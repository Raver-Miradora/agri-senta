"use client";

import { AlertTriangle, RotateCcw } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <section className="page">
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "40vh", gap: "1.5rem" }}>
        <div className="empty-icon" style={{ background: "#fef2f2", color: "var(--agri-red)" }}>
          <AlertTriangle size={32} />
        </div>
        <div style={{ textAlign: "center", maxWidth: "420px" }}>
          <h2 style={{ margin: "0 0 0.5rem", fontSize: "1.25rem" }}>Something went wrong</h2>
          <p style={{ color: "var(--muted)", margin: "0 0 1.5rem", fontSize: "0.9rem" }}>
            {error.message || "An unexpected error occurred while loading this page."}
          </p>
          <button className="btn" type="button" onClick={reset} style={{ display: "inline-flex", alignItems: "center", gap: "0.5rem" }}>
            <RotateCcw size={16} />
            Try again
          </button>
        </div>
      </div>
    </section>
  );
}
