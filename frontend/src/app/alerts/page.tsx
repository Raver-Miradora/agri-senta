export const dynamic = "force-dynamic";

import {
  ShieldAlert,
  AlertTriangle,
  Bell,
  CheckCircle2,
  AlertCircle,
  Info,
} from "lucide-react";
import { PriceAlertItem, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

const SEVERITY_CONFIG: Record<string, { badge: string; icon: typeof AlertTriangle }> = {
  critical: { badge: "badge-red", icon: AlertCircle },
  high: { badge: "badge-red", icon: AlertTriangle },
  medium: { badge: "badge-yellow", icon: Bell },
  low: { badge: "badge-green", icon: Info },
};

export default async function AlertsPage() {
  const alerts = await fetchFromApiOrDefault<PriceAlertItem[]>("/alerts", []);
  const unresolved = alerts.filter((a) => !a.is_resolved);
  const critical = alerts.filter((a) => a.severity === "critical" && !a.is_resolved);

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-red">
            <ShieldAlert size={22} />
          </div>
          <div>
            <h1>Price Monitoring &amp; Alerts</h1>
            <p className="subtitle">
              Automated alerts when commodity prices deviate beyond normal thresholds.
              Helps the MAO detect and prevent potential price manipulation.
            </p>
          </div>
        </div>
      </div>

      {/* KPI */}
      <div className="grid-4">
        <div className="card kpi kpi-accent-red">
          <div className="kpi-top">
            <span style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Active Alerts</span>
            <div className="kpi-icon kpi-icon-red"><AlertTriangle size={20} /></div>
          </div>
          <p className="kpi-value">{unresolved.length}</p>
          <p className="kpi-label">unresolved alerts</p>
        </div>
        <div className="card kpi kpi-accent-yellow">
          <div className="kpi-top">
            <span style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Critical</span>
            <div className="kpi-icon kpi-icon-yellow"><AlertCircle size={20} /></div>
          </div>
          <p className="kpi-value">{critical.length}</p>
          <p className="kpi-label">need immediate attention</p>
        </div>
        <div className="card kpi kpi-accent-green">
          <div className="kpi-top">
            <span style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Resolved</span>
            <div className="kpi-icon kpi-icon-green"><CheckCircle2 size={20} /></div>
          </div>
          <p className="kpi-value">{alerts.length - unresolved.length}</p>
          <p className="kpi-label">previously resolved</p>
        </div>
      </div>

      {/* Alerts table */}
      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-red"><Bell size={18} /></div>
          <div>
            <h3 className="section-title">All Alerts</h3>
            <p className="section-subtitle">{alerts.length} total alert{alerts.length !== 1 ? "s" : ""}</p>
          </div>
        </div>

        {alerts.length === 0 ? (
          <div className="empty">
            <div className="empty-icon"><ShieldAlert size={24} /></div>
            <p>No price alerts detected. The system monitors prices automatically and generates alerts when anomalies occur.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Severity</th>
                  <th>Commodity</th>
                  <th>Barangay</th>
                  <th>Type</th>
                  <th style={{ textAlign: "right" }}>Price</th>
                  <th style={{ textAlign: "right" }}>Threshold</th>
                  <th>Triggered</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((a) => {
                  const cfg = SEVERITY_CONFIG[a.severity] ?? SEVERITY_CONFIG.low;
                  const Icon = cfg.icon;
                  return (
                    <tr key={a.id} style={{ opacity: a.is_resolved ? 0.6 : 1 }}>
                      <td>
                        <span className={`badge ${cfg.badge}`} style={{ display: "inline-flex", alignItems: "center", gap: "0.25rem" }}>
                          <Icon size={12} /> {a.severity}
                        </span>
                      </td>
                      <td style={{ fontWeight: 600 }}>{a.commodity_name}</td>
                      <td>{a.region_name ?? "All"}</td>
                      <td>{a.alert_type}</td>
                      <td style={{ textAlign: "right", fontWeight: 700, color: "var(--agri-red)" }}>
                        {formatPeso(a.current_price)}
                      </td>
                      <td style={{ textAlign: "right", color: "var(--muted)" }}>
                        {a.threshold_price !== null ? formatPeso(a.threshold_price) : "—"}
                      </td>
                      <td style={{ whiteSpace: "nowrap", fontSize: "0.85rem" }}>
                        {new Date(a.triggered_at).toLocaleDateString("en-PH", { month: "short", day: "numeric", year: "numeric" })}
                      </td>
                      <td>
                        <span className={`badge ${a.is_resolved ? "badge-green" : "badge-red"}`}>
                          {a.is_resolved ? "Resolved" : "Active"}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Info card */}
      <div className="card" style={{ borderLeft: "3px solid var(--agri-blue)" }}>
        <p style={{ margin: 0, color: "var(--text-secondary)", fontSize: "0.9rem", lineHeight: 1.6 }}>
          <strong>How it works:</strong> The system compares daily commodity prices against historical
          moving averages. When a price deviates significantly (spike or sudden drop), an alert is
          automatically generated for review by the Municipal Agriculture Office. This helps
          ensure fair pricing at public markets.
        </p>
      </div>
    </section>
  );
}
