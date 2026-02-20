import {
  Info,
  Database,
  Brain,
  Server,
  Wheat,
  Globe,
  ShieldCheck,
  Clock,
  MapPin,
  Fish,
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
              A Smart Agricultural Price Tracker &amp; Dashboard for the Municipal Agriculture
              Office of Lagonoy, Camarines Sur.
            </p>
          </div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid">
        <div className="feature-card">
          <div className="feature-icon feature-icon-blue">
            <MapPin size={24} />
          </div>
          <h3>Lagonoy, Camarines Sur</h3>
          <p>30 barangays &bull; Lagonoy Gulf &bull; Bicol Region</p>
        </div>
        <div className="feature-card">
          <div className="feature-icon feature-icon-red">
            <Brain size={24} />
          </div>
          <h3>ML Forecasting</h3>
          <p>Linear Regression &bull; ARIMA models</p>
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
          Agri-Senta is a data-driven web application built for the Municipal Agriculture Office
          of Lagonoy. It allows the LGU to broadcast daily commodity prices to local farmers,
          track seasonal harvest yields across barangays, and help prevent price manipulation
          in the Lagonoy Public Market. The system uses machine-learning models to generate
          7-day price forecasts with confidence intervals, giving actionable pricing intelligence
          to farmers and market administrators alike.
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
              <strong>Daily Price Broadcasting</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "0.25rem 0 0" }}>
                Public price board for farmers and consumers to view today&apos;s market prices
              </p>
            </div>
          </div>
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <div className="status-dot" style={{ background: "var(--agri-red)" }} />
            <div>
              <strong>Price Manipulation Detection</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "0.25rem 0 0" }}>
                Automatic alerts when prices deviate beyond normal thresholds
              </p>
            </div>
          </div>
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <div className="status-dot" style={{ background: "var(--agri-yellow)" }} />
            <div>
              <strong>Harvest Yield Tracking</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "0.25rem 0 0" }}>
                Record and analyse crop yields per barangay and growing season
              </p>
            </div>
          </div>
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <div className="status-dot" style={{ background: "#10b981" }} />
            <div>
              <strong>7-Day Price Forecasts</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.85rem", margin: "0.25rem 0 0" }}>
                ML-powered predictions with confidence intervals for all commodities
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
