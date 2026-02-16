import {
  Info,
  Database,
  Brain,
  Server,
  Wheat,
  Globe,
  ShieldCheck,
  Clock,
} from "lucide-react";

export default function AboutPage() {
  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <Info size={22} />
          </div>
          <div>
            <h1>About Agri-Senta</h1>
            <p className="subtitle">
              A Smart Palengke Dashboard for tracking, comparing, and forecasting commodity prices
              across Philippine regions.
            </p>
          </div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid">
        <div className="feature-card">
          <div className="feature-icon feature-icon-blue">
            <Database size={24} />
          </div>
          <h3>Data Sources</h3>
          <p>DA Price Watch &bull; PSA OpenSTAT</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon feature-icon-red">
            <Brain size={24} />
          </div>
          <h3>ML Models</h3>
          <p>Linear Regression &bull; ARIMA</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon feature-icon-yellow">
            <Server size={24} />
          </div>
          <h3>Tech Stack</h3>
          <p>Next.js &bull; FastAPI &bull; PostgreSQL</p>
        </div>
      </div>

      {/* How it works */}
      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <Wheat size={18} />
          </div>
          <h3 className="section-title">How it works</h3>
        </div>
        <p style={{ color: "var(--muted)", lineHeight: 1.7 }}>
          Agri-Senta automatically scrapes official government price data daily, cleans and stores
          it in PostgreSQL, then uses machine-learning models to generate 7-day commodity price
          forecasts. The dashboard gives consumers and small food businesses actionable pricing
          intelligence at a glance.
        </p>
      </div>

      {/* Key features */}
      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-yellow">
            <ShieldCheck size={18} />
          </div>
          <h3 className="section-title">Key Features</h3>
        </div>
        <div className="grid-2">
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <div className="status-dot" style={{ background: "var(--agri-blue)" }} />
            <div>
              <strong>Real-time Scraping</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "0.25rem 0 0" }}>
                Automated daily data collection from government sources
              </p>
            </div>
          </div>
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <div className="status-dot" style={{ background: "var(--agri-red)" }} />
            <div>
              <strong>Spike Detection</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "0.25rem 0 0" }}>
                Automatic alerts when prices deviate significantly
              </p>
            </div>
          </div>
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <div className="status-dot" style={{ background: "var(--agri-yellow)" }} />
            <div>
              <strong>7-Day Forecasts</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "0.25rem 0 0" }}>
                ML-powered predictions with confidence intervals
              </p>
            </div>
          </div>
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <div className="status-dot" style={{ background: "#10b981" }} />
            <div>
              <strong>Regional Coverage</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "0.25rem 0 0" }}>
                Price tracking across all Philippine regions
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
