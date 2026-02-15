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
        <h1>Analytics</h1>
        <p className="subtitle">Weekly variance and detected price spike events from live data.</p>
      </div>

      <div className="card">
        <h3 className="section-title">Weekly Percentage Change (WoW)</h3>
        <SimpleLineChart data={lineData} xKey="week" yKey="wow_change" color="#CE1126" />
      </div>

      <div className="card">
        <h3 className="section-title">Detected Spikes</h3>
        {spikes.length === 0 ? (
          <p className="empty">No spikes detected from current seeded data.</p>
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
                  <td>{row.commodity_id}</td>
                  <td>{row.region_id}</td>
                  <td className="text-right">{formatPeso(Number(row.avg_price))}</td>
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
