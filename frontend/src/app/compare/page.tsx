export const dynamic = "force-dynamic";

import { GitCompareArrows, BarChart3, MapPin } from "lucide-react";
import SimpleBarChart from "@/components/charts/SimpleBarChart";
import { RegionalComparison, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function ComparePage() {
  const rows = await fetchFromApiOrDefault<RegionalComparison[]>("/analytics/regional-comparison", []);
  const chartData = rows.map((row) => ({ barangay: row.region_code, avg_price: Number(row.avg_price) }));

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-red">
            <GitCompareArrows size={22} />
          </div>
          <div>
            <h1>Barangay Comparison</h1>
            <p className="subtitle">Average prevailing prices by barangay (all commodities combined).</p>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <BarChart3 size={18} />
          </div>
          <h3 className="section-title">Price Distribution by Barangay</h3>
        </div>
        <div className="chart-container">
          <SimpleBarChart data={chartData} xKey="barangay" yKey="avg_price" />
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-red">
            <MapPin size={18} />
          </div>
          <div>
            <h3 className="section-title">Barangay Breakdown</h3>
            <p className="section-subtitle">{rows.length} barangays compared</p>
          </div>
        </div>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Barangay</th>
                <th className="text-left">Code</th>
                <th className="text-right">Avg Price</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.region_id}>
                  <td style={{ fontWeight: 600 }}>{row.region_name}</td>
                  <td>
                    <span className="badge badge-red">{row.region_code}</span>
                  </td>
                  <td className="text-right font-mono">{formatPeso(Number(row.avg_price))}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
