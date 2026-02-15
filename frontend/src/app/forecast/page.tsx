import Link from "next/link";

import { ForecastSummary, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function ForecastPage() {
  const rows = await fetchFromApiOrDefault<ForecastSummary[]>("/forecast/summary", []);

  return (
    <section className="page">
      <div className="page-header">
        <h1>Forecast</h1>
        <p className="subtitle">Nearest available forecast entry per commodity-region pair.</p>
      </div>
      <div className="card">
        {rows.length === 0 ? (
          <p className="empty">No forecast data yet. Ensure backend startup completed forecast generation.</p>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Commodity</th>
                <th className="text-left">Region</th>
                <th className="text-left">Forecast Date</th>
                <th className="text-right">Predicted Price</th>
                <th className="text-left">Model</th>
                <th className="text-left">Detail</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={`${row.commodity_id}-${row.region_id}-${row.forecast_date}`}>
                  <td>{row.commodity_name}</td>
                  <td>{row.region_code}</td>
                  <td>{row.forecast_date}</td>
                  <td className="text-right">{formatPeso(Number(row.predicted_price))}</td>
                  <td>{row.model_used}</td>
                  <td>
                    <Link className="chip-link" href={`/forecast/${row.commodity_id}`}>
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
