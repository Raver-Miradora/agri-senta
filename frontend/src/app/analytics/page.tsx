export const dynamic = "force-dynamic";

import { BarChart3, TrendingUp, AlertTriangle, Activity } from "lucide-react";
import SimpleLineChart from "@/components/charts/SimpleLineChart";
import { PriceSpike, WeeklyVariance, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function AnalyticsPage() {
  const [weeklyVariance, spikes] = await Promise.all([
    fetchFromApiOrDefault<WeeklyVariance[]>("/analytics/weekly-variance", []),
    fetchFromApiOrDefault<PriceSpike[]>("/analytics/price-spikes", []),
  ]);

  const lineData = weeklyVariance
    .filter((row) => row.wow_percent_change !== null)
    .slice(0, 24)
    .reverse()
    .map((row) => ({
      week: row.week_start,
      wow_change: Number(row.wow_percent_change ?? 0),
    }));

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-yellow">
            <BarChart3 size={22} />
          </div>
          <div>
            <h1>Analytics</h1>
            <p className="subtitle">Weekly variance and detected price spike events from live data.</p>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-red">
            <Activity size={18} />
          </div>
          <div>
            <h3 className="section-title">Weekly Percentage Change (WoW)</h3>
            <p className="section-subtitle">{lineData.length} data points</p>
          </div>
        </div>
        <div className="chart-container">
          <SimpleLineChart data={lineData} xKey="week" yKey="wow_change" color="#CE1126" />
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-yellow">
            <AlertTriangle size={18} />
          </div>
          <div>
            <h3 className="section-title">Detected Spikes</h3>
            <p className="section-subtitle">{spikes.length} spike event{spikes.length !== 1 ? "s" : ""} found</p>
          </div>
        </div>

        {spikes.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">
              <TrendingUp size={24} />
            </div>
            <p>No spikes detected from current data.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th className="text-left">Date</th>
                  <th className="text-left">Commodity ID</th>
                  <th className="text-left">Region ID</th>
                  <th className="text-right">Avg Price</th>
                </tr>
              </thead>
              <tbody>
                {spikes.slice(0, 20).map((row, index) => (
                  <tr key={`${row.commodity_id}-${row.region_id}-${row.date}-${index}`}>
                    <td>{row.date}</td>
                    <td>
                      <span className="badge badge-blue">{row.commodity_id}</span>
                    </td>
                    <td>
                      <span className="badge badge-red">{row.region_id}</span>
                    </td>
                    <td className="text-right font-mono">{formatPeso(Number(row.avg_price))}</td>
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
