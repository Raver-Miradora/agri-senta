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
    <section>
      <h1>Analytics</h1>
      <p>Weekly variance and detected price spike events from live data.</p>

      <div className="card" style={{ marginTop: "1rem" }}>
        <h3>Weekly Percentage Change (WoW)</h3>
        <SimpleLineChart data={lineData} xKey="week" yKey="wow_change" color="#CE1126" />
      </div>

      <div className="card" style={{ marginTop: "1rem" }}>
        <h3>Detected Spikes</h3>
        {spikes.length === 0 ? (
          <p>No spikes detected from current seeded data.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left" }}>Date</th>
                <th style={{ textAlign: "left" }}>Commodity ID</th>
                <th style={{ textAlign: "left" }}>Region ID</th>
                <th style={{ textAlign: "right" }}>Avg Price</th>
              </tr>
            </thead>
            <tbody>
              {spikes.slice(0, 20).map((row, index) => (
                <tr key={`${row.commodity_id}-${row.region_id}-${row.date}-${index}`}>
                  <td>{row.date}</td>
                  <td>{row.commodity_id}</td>
                  <td>{row.region_id}</td>
                  <td style={{ textAlign: "right" }}>{formatPeso(Number(row.avg_price))}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
