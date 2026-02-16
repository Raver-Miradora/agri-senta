export default function AboutPage() {
  return (
    <section className="page">
      <div className="page-header">
        <h1>About Agri-Senta</h1>
        <p className="subtitle">
          A Smart Palengke Dashboard for tracking, comparing, and forecasting commodity prices
          across Philippine regions.
        </p>
      </div>

      <div className="grid">
        <div className="card kpi kpi-accent-blue">
          <p className="kpi-label">Data Sources</p>
          <p className="kpi-value" style={{ fontSize: "1.1rem" }}>DA Price Watch &bull; PSA OpenSTAT</p>
        </div>
        <div className="card kpi kpi-accent-red">
          <p className="kpi-label">ML Models</p>
          <p className="kpi-value" style={{ fontSize: "1.1rem" }}>Linear Regression &bull; ARIMA</p>
        </div>
        <div className="card kpi kpi-accent-yellow">
          <p className="kpi-label">Stack</p>
          <p className="kpi-value" style={{ fontSize: "1.1rem" }}>Next.js &bull; FastAPI &bull; PostgreSQL</p>
        </div>
      </div>

      <div className="card">
        <h3 className="section-title">How it works</h3>
        <p className="subtitle">
          Agri-Senta automatically scrapes official government price data daily, cleans and stores
          it in PostgreSQL, then uses machine-learning models to generate 7-day commodity price
          forecasts. The dashboard gives consumers and small food businesses actionable pricing
          intelligence at a glance.
        </p>
      </div>
    </section>
  );
}
