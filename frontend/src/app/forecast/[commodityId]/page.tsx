import Link from "next/link";
import { TrendingUp, ChevronRight, Brain, Calendar } from "lucide-react";
import ForecastBandChart from "@/components/charts/ForecastBandChart";
import { ForecastPoint, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

type ForecastCommodityPageProps = {
  params: Promise<{ commodityId: string }>;
};

export default async function ForecastCommodityPage({ params }: ForecastCommodityPageProps) {
  const { commodityId } = await params;
  const rows = await fetchFromApiOrDefault<ForecastPoint[]>(`/forecast/${commodityId}`, []);
  const chartData = rows.map((row) => ({
    day: row.forecast_date,
    predicted_price: Number(row.predicted_price),
    confidence_lower: Number(row.confidence_lower ?? row.predicted_price),
    confidence_upper: Number(row.confidence_upper ?? row.predicted_price),
  }));

  return (
    <section className="page">
      {/* Breadcrumb */}
      <nav className="breadcrumb">
        <Link href="/forecast">Forecast</Link>
        <ChevronRight size={14} />
        <span>Commodity {commodityId}</span>
      </nav>

      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <TrendingUp size={22} />
          </div>
          <div>
            <h1>Forecast Detail: Commodity {commodityId}</h1>
            <p className="subtitle">7-day prediction with confidence band.</p>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <TrendingUp size={18} />
          </div>
          <h3 className="section-title">Prediction Chart</h3>
        </div>
        <div className="chart-container">
          <ForecastBandChart data={chartData} xKey="day" />
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <Brain size={18} />
          </div>
          <div>
            <h3 className="section-title">Forecast Data</h3>
            <p className="section-subtitle">{rows.length} prediction{rows.length !== 1 ? "s" : ""}</p>
          </div>
        </div>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Date</th>
                <th className="text-right">Predicted</th>
                <th className="text-right">Lower</th>
                <th className="text-right">Upper</th>
                <th className="text-center">Model</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={`${row.region_id}-${row.forecast_date}`}>
                  <td>
                    <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
                      <Calendar size={13} style={{ color: "var(--muted)" }} />
                      {row.forecast_date}
                    </span>
                  </td>
                  <td className="text-right font-mono">{formatPeso(Number(row.predicted_price))}</td>
                  <td className="text-right font-mono">{formatPeso(Number(row.confidence_lower ?? row.predicted_price))}</td>
                  <td className="text-right font-mono">{formatPeso(Number(row.confidence_upper ?? row.predicted_price))}</td>
                  <td className="text-center">
                    <span className="badge badge-green">{row.model_used}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
