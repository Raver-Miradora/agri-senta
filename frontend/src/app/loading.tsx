import { Loader2 } from "lucide-react";

export default function Loading() {
  return (
    <section className="page">
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "40vh", gap: "1.5rem" }}>
        <div className="spinner">
          <Loader2 size={32} />
        </div>
        <div style={{ textAlign: "center" }}>
          <h2 style={{ margin: "0 0 0.25rem", fontSize: "1.15rem" }}>Loading…</h2>
          <p style={{ color: "var(--muted)", margin: 0, fontSize: "0.9rem" }}>Please wait while Agri-Senta prepares your dashboard.</p>
        </div>
      </div>
      <div className="grid">
        <div className="card"><div className="skeleton-row" /><div className="skeleton-row" style={{ width: "60%" }} /></div>
        <div className="card"><div className="skeleton-row" /><div className="skeleton-row" style={{ width: "75%" }} /></div>
        <div className="card"><div className="skeleton-row" /><div className="skeleton-row" style={{ width: "50%" }} /></div>
      </div>
    </section>
  );
}
