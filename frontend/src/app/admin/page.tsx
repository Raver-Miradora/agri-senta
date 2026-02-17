"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Shield, Play, RefreshCw, Clock, AlertCircle, CheckCircle2 } from "lucide-react";
import { useAuth } from "@/lib/AuthContext";
import { fetchWithAuth } from "@/lib/api";

type ScrapeLog = {
  id: number;
  source: string;
  status: string;
  rows_ingested: number;
  error_message: string | null;
  duration_seconds: number | null;
  executed_at: string;
};

type TriggerResult = {
  status: string;
  source: string;
  rows_ingested: number;
};

export default function AdminPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const [logs, setLogs] = useState<ScrapeLog[]>([]);
  const [loadingLogs, setLoadingLogs] = useState(true);
  const [triggering, setTriggering] = useState(false);
  const [triggerResult, setTriggerResult] = useState<TriggerResult | null>(null);
  const [error, setError] = useState("");

  const loadLogs = useCallback(async () => {
    setLoadingLogs(true);
    try {
      const data = await fetchWithAuth<ScrapeLog[]>("/admin/scrape/logs?limit=20");
      setLogs(data);
    } catch {
      setError("Failed to load scrape logs");
    } finally {
      setLoadingLogs(false);
    }
  }, []);

  useEffect(() => {
    if (!authLoading && !user?.is_admin) {
      router.replace("/login");
      return;
    }
    if (user?.is_admin) {
      loadLogs();
    }
  }, [user, authLoading, router, loadLogs]);

  const handleTrigger = async (source: string) => {
    setTriggering(true);
    setError("");
    setTriggerResult(null);
    try {
      const result = await fetchWithAuth<TriggerResult>(
        `/admin/scrape/trigger?source=${source}`,
        { method: "POST" }
      );
      setTriggerResult(result);
      loadLogs(); // Refresh logs after trigger
    } catch (err) {
      setError(err instanceof Error ? err.message : "Trigger failed");
    } finally {
      setTriggering(false);
    }
  };

  if (authLoading) {
    return (
      <section className="section">
        <p style={{ textAlign: "center", color: "var(--text-secondary)" }}>Loading…</p>
      </section>
    );
  }

  if (!user?.is_admin) return null;

  return (
    <section className="section">
      <h1
        className="section-title"
        style={{ display: "flex", alignItems: "center", gap: 8 }}
      >
        <Shield size={24} />
        Admin Dashboard
      </h1>
      <p style={{ color: "var(--text-secondary)", marginBottom: "1.5rem" }}>
        Logged in as <strong>{user.username}</strong>
      </p>

      {/* Trigger Scrape */}
      <div className="card" style={{ padding: "1.5rem", marginBottom: "1.5rem" }}>
        <h2 style={{ fontSize: "1.125rem", fontWeight: 600, marginBottom: "1rem" }}>
          Trigger Data Scrape
        </h2>
        <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
          <button
            onClick={() => handleTrigger("DA")}
            disabled={triggering}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 6,
              padding: "0.625rem 1.25rem",
              background: "var(--agri-green)",
              color: "white",
              border: "none",
              borderRadius: 8,
              fontWeight: 600,
              cursor: triggering ? "not-allowed" : "pointer",
              opacity: triggering ? 0.7 : 1,
            }}
          >
            <Play size={16} />
            {triggering ? "Running…" : "Scrape DA"}
          </button>
          <button
            onClick={() => handleTrigger("PSA")}
            disabled={triggering}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 6,
              padding: "0.625rem 1.25rem",
              background: "var(--agri-blue)",
              color: "white",
              border: "none",
              borderRadius: 8,
              fontWeight: 600,
              cursor: triggering ? "not-allowed" : "pointer",
              opacity: triggering ? 0.7 : 1,
            }}
          >
            <Play size={16} />
            {triggering ? "Running…" : "Scrape PSA"}
          </button>
        </div>

        {triggerResult && (
          <div
            style={{
              marginTop: "1rem",
              padding: "0.75rem 1rem",
              background: "var(--agri-green-light, #dcfce7)",
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              gap: 8,
              fontSize: "0.875rem",
            }}
          >
            <CheckCircle2 size={16} style={{ color: "var(--agri-green)" }} />
            <span>
              <strong>{triggerResult.source}</strong> scrape completed —{" "}
              {triggerResult.rows_ingested} rows ingested ({triggerResult.status})
            </span>
          </div>
        )}

        {error && (
          <div
            style={{
              marginTop: "1rem",
              padding: "0.75rem 1rem",
              background: "var(--agri-red-light, #fee2e2)",
              color: "var(--agri-red, #dc2626)",
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              gap: 8,
              fontSize: "0.875rem",
            }}
          >
            <AlertCircle size={16} />
            {error}
          </div>
        )}
      </div>

      {/* Scrape Logs */}
      <div className="card" style={{ padding: "1.5rem" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "1rem",
          }}
        >
          <h2 style={{ fontSize: "1.125rem", fontWeight: 600 }}>
            Scrape Logs
          </h2>
          <button
            onClick={loadLogs}
            disabled={loadingLogs}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 4,
              padding: "0.5rem 0.75rem",
              background: "var(--surface)",
              border: "1px solid var(--border)",
              borderRadius: 8,
              cursor: "pointer",
              fontSize: "0.8125rem",
            }}
          >
            <RefreshCw size={14} />
            Refresh
          </button>
        </div>

        {loadingLogs ? (
          <p style={{ color: "var(--text-secondary)" }}>Loading logs…</p>
        ) : logs.length === 0 ? (
          <p style={{ color: "var(--text-secondary)" }}>No scrape logs yet.</p>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table className="data-table" style={{ width: "100%", fontSize: "0.875rem" }}>
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Status</th>
                  <th>Rows</th>
                  <th>Duration</th>
                  <th>Time</th>
                  <th>Error</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id}>
                    <td>
                      <strong>{log.source}</strong>
                    </td>
                    <td>
                      <span
                        style={{
                          display: "inline-flex",
                          alignItems: "center",
                          gap: 4,
                          padding: "2px 8px",
                          borderRadius: 12,
                          fontSize: "0.75rem",
                          fontWeight: 600,
                          background:
                            log.status === "success"
                              ? "var(--agri-green-light, #dcfce7)"
                              : "var(--agri-red-light, #fee2e2)",
                          color:
                            log.status === "success"
                              ? "var(--agri-green)"
                              : "var(--agri-red, #dc2626)",
                        }}
                      >
                        {log.status === "success" ? (
                          <CheckCircle2 size={12} />
                        ) : (
                          <AlertCircle size={12} />
                        )}
                        {log.status}
                      </span>
                    </td>
                    <td>{log.rows_ingested}</td>
                    <td>
                      {log.duration_seconds != null
                        ? `${log.duration_seconds.toFixed(1)}s`
                        : "—"}
                    </td>
                    <td style={{ whiteSpace: "nowrap" }}>
                      <Clock size={12} style={{ marginRight: 4, opacity: 0.5 }} />
                      {new Date(log.executed_at).toLocaleString()}
                    </td>
                    <td
                      style={{
                        maxWidth: 200,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                        color: "var(--agri-red, #dc2626)",
                      }}
                      title={log.error_message ?? undefined}
                    >
                      {log.error_message ?? "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}
