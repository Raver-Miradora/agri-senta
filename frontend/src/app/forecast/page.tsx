import Link from "next/link";

import { ForecastSummary, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function ForecastPage() {
  const rows = await fetchFromApiOrDefault<ForecastSummary[]>("/forecast/summary", []);

  return (
    <section>
      <h1>Forecast</h1>
      <p>Nearest available forecast entry per commodity-region pair.</p>
      <div className="card" style={{ marginTop: "1rem" }}>
        {rows.length === 0 ? (
          <p>No forecast data yet. Ensure backend startup completed forecast generation.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left" }}>Commodity</th>
                <th style={{ textAlign: "left" }}>Region</th>
                <th style={{ textAlign: "left" }}>Forecast Date</th>
                <th style={{ textAlign: "right" }}>Predicted Price</th>
                <th style={{ textAlign: "left" }}>Model</th>
                <th style={{ textAlign: "left" }}>Detail</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={`${row.commodity_id}-${row.region_id}-${row.forecast_date}`}>
                  <td>{row.commodity_name}</td>
                  <td>{row.region_code}</td>
                  <td>{row.forecast_date}</td>
                  <td style={{ textAlign: "right" }}>{formatPeso(Number(row.predicted_price))}</td>
                  <td>{row.model_used}</td>
                  <td>
                    <Link href={`/forecast/${row.commodity_id}`}>Open</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
