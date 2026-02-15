import SimpleBarChart from "@/components/charts/SimpleBarChart";
import { RegionalComparison, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function ComparePage() {
  const rows = await fetchFromApiOrDefault<RegionalComparison[]>("/analytics/regional-comparison", []);
  const chartData = rows.map((row) => ({ region: row.region_code, avg_price: Number(row.avg_price) }));

  return (
    <section className="page">
      <div className="page-header">
        <h1>Regional Comparison</h1>
        <p className="subtitle">Average prevailing prices by region (all commodities combined).</p>
      </div>
      <div className="card">
        <SimpleBarChart data={chartData} xKey="region" yKey="avg_price" />
      </div>
      <div className="card">
        <div className="table-wrap">
          <table className="data-table">
          <thead>
            <tr>
              <th className="text-left">Region</th>
              <th className="text-left">Code</th>
              <th className="text-right">Avg Price</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.region_id}>
                <td>{row.region_name}</td>
                <td>{row.region_code}</td>
                <td className="text-right">{formatPeso(Number(row.avg_price))}</td>
              </tr>
            ))}
          </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
