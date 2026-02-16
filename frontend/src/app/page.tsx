import Link from "next/link";
import {
  LayoutDashboard,
  ShoppingBasket,
  MapPin,
  Receipt,
  TrendingUp,
  BarChart3,
  ArrowRight,
  Calendar,
} from "lucide-react";

import { Commodity, LatestPrice, Region, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function HomePage() {
  const [commodities, regions] = await Promise.all([
    fetchFromApiOrDefault<Commodity[]>("/commodities", []),
    fetchFromApiOrDefault<Region[]>("/regions", []),
  ]);

  const latestPrices = await fetchFromApiOrDefault<LatestPrice[]>("/prices/latest", []);
  const latestDate = latestPrices[0]?.date ?? "N/A";

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <LayoutDashboard size={22} />
          </div>
          <div>
            <h1>Smart Palengke Dashboard</h1>
            <p className="subtitle">
              Real-time commodity price intelligence across Philippine regions.
            </p>
          </div>
        </div>
      </div>

      {/* ── Date indicator ── */}
      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", color: "var(--muted)", fontSize: "0.85rem" }}>
        <Calendar size={14} />
        <span>Latest snapshot: <strong style={{ color: "var(--text)" }}>{latestDate}</strong></span>
      </div>

      {/* ── KPI Cards ── */}
      <div className="grid">
        <div className="card kpi kpi-accent-blue">
          <div className="kpi-top">
            <p className="kpi-label">Commodities</p>
            <div className="kpi-icon kpi-icon-blue">
              <ShoppingBasket size={20} />
            </div>
          </div>
          <p className="kpi-value">{commodities.length}</p>
          <p className="kpi-detail">Tracked commodities</p>
        </div>

        <div className="card kpi kpi-accent-red">
          <div className="kpi-top">
            <p className="kpi-label">Regions</p>
            <div className="kpi-icon kpi-icon-red">
              <MapPin size={20} />
            </div>
          </div>
          <p className="kpi-value">{regions.length}</p>
          <p className="kpi-detail">Philippine regions monitored</p>
        </div>

        <div className="card kpi kpi-accent-yellow">
          <div className="kpi-top">
            <p className="kpi-label">Price Records</p>
            <div className="kpi-icon kpi-icon-yellow">
              <Receipt size={20} />
            </div>
          </div>
          <p className="kpi-value">{latestPrices.length}</p>
          <p className="kpi-detail">Latest price entries</p>
        </div>
      </div>

      {/* ── Recent Prices Table ── */}
      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <Receipt size={18} />
          </div>
          <div>
            <h3 className="section-title">Recent Prices</h3>
            <p className="section-subtitle">Latest prevailing market prices</p>
          </div>
        </div>

        {latestPrices.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">
              <Receipt size={24} />
            </div>
            <p>No price data available yet. Data will appear once scraping runs.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th className="text-left">Commodity</th>
                  <th className="text-left">Region</th>
                  <th className="text-right">Average Price</th>
                  <th className="text-center">Actions</th>
                </tr>
              </thead>
              <tbody>
                {latestPrices.slice(0, 10).map((row) => (
                  <tr key={`${row.commodity_id}-${row.region_id}`}>
                    <td style={{ fontWeight: 600 }}>{row.commodity_name}</td>
                    <td>
                      <span className="badge badge-blue">{row.region_code}</span>
                    </td>
                    <td className="text-right font-mono">{formatPeso(Number(row.avg_price))}</td>
                    <td className="text-center">
                      <Link className="chip-link" href={`/trends/${row.commodity_id}`}>
                        <TrendingUp size={12} />
                        Trend
                      </Link>{" "}
                      <Link className="chip-link" href={`/forecast/${row.commodity_id}`}>
                        <BarChart3 size={12} />
                        Forecast
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {latestPrices.length > 10 && (
          <div style={{ marginTop: "1rem", textAlign: "center" }}>
            <Link className="btn btn-outline" href="/prices">
              View all prices
              <ArrowRight size={16} />
            </Link>
          </div>
        )}
      </div>
    </section>
  );
}
