export const dynamic = "force-dynamic";

import Link from "next/link";
import { TrendingUp, Brain, ArrowRight, Calendar } from "lucide-react";

import { ForecastSummary, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function ForecastPage() {
  const rows = await fetchFromApiOrDefault<ForecastSummary[]>("/forecast/summary", []);

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <TrendingUp size={22} />
          </div>
          <div>
            <h1>Forecast</h1>
            <p className="subtitle">Nearest available forecast entry per commodity-region pair.</p>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <Brain size={18} />
          </div>
          <div>
            <h3 className="section-title">Forecast Results</h3>
            <p className="section-subtitle">{rows.length} forecast{rows.length !== 1 ? "s" : ""} generated</p>
          </div>
        </div>

        {rows.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">
              <TrendingUp size={24} />
            </div>
            <p>No forecast data yet. Ensure backend startup completed forecast generation.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th className="text-left">Commodity</th>
                  <th className="text-left">Region</th>
                  <th className="text-left">Forecast Date</th>
                  <th className="text-right">Predicted Price</th>
                  <th className="text-center">Model</th>
                  <th className="text-center">Detail</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={`${row.commodity_id}-${row.region_id}-${row.forecast_date}`}>
                    <td style={{ fontWeight: 600 }}>{row.commodity_name}</td>
                    <td>
                      <span className="badge badge-red">{row.region_code}</span>
                    </td>
                    <td>
                      <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
                        <Calendar size={13} style={{ color: "var(--muted)" }} />
                        {row.forecast_date}
                      </span>
                    </td>
                    <td className="text-right font-mono">{formatPeso(Number(row.predicted_price))}</td>
                    <td className="text-center">
                      <span className="badge badge-green">{row.model_used}</span>
                    </td>
                    <td className="text-center">
                      <Link className="chip-link" href={`/forecast/${row.commodity_id}`}>
                        <ArrowRight size={12} />
                        Open
                      </Link>
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
