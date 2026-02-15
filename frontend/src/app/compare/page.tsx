import SimpleBarChart from "@/components/charts/SimpleBarChart";
import { RegionalComparison, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function ComparePage() {
  const rows = await fetchFromApiOrDefault<RegionalComparison[]>("/analytics/regional-comparison", []);
  const chartData = rows.map((row) => ({ region: row.region_code, avg_price: Number(row.avg_price) }));

  return (
    <section>
      <h1>Regional Comparison</h1>
      <p>Average prevailing prices by region (all commodities combined).</p>
      <div className="card" style={{ marginTop: "1rem" }}>
        <SimpleBarChart data={chartData} xKey="region" yKey="avg_price" />
      </div>
      <div className="card" style={{ marginTop: "1rem" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left" }}>Region</th>
              <th style={{ textAlign: "left" }}>Code</th>
              <th style={{ textAlign: "right" }}>Avg Price</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.region_id}>
                <td>{row.region_name}</td>
                <td>{row.region_code}</td>
                <td style={{ textAlign: "right" }}>{formatPeso(Number(row.avg_price))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
