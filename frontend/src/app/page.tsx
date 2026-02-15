import Link from "next/link";

import { Commodity, LatestPrice, Region, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function HomePage() {
  const [commodities, regions] = await Promise.all([
    fetchFromApiOrDefault<Commodity[]>("/commodities", []),
    fetchFromApiOrDefault<Region[]>("/regions", []),
  ]);

  const latestPrices = await fetchFromApiOrDefault<LatestPrice[]>("/prices/latest", []);
  const latestDate = latestPrices[0]?.date ?? "N/A";

  return (
    <section className="page">
      <div className="page-header">
        <h1>Smart Palengke Dashboard</h1>
        <p className="subtitle">Live baseline data from the Agri-Senta API. Latest snapshot: {latestDate}</p>
      </div>

      <div className="grid">
        <div className="card kpi kpi-accent-blue">
          <p className="kpi-label">Tracked Commodities</p>
          <p className="kpi-value">{commodities.length}</p>
        </div>
        <div className="card kpi kpi-accent-red">
          <p className="kpi-label">Tracked Regions</p>
          <p className="kpi-value">{regions.length}</p>
        </div>
        <div className="card kpi kpi-accent-yellow">
          <p className="kpi-label">Latest Price Rows</p>
          <p className="kpi-value">{latestPrices.length}</p>
        </div>
      </div>

      <div className="card">
        <h3 className="section-title">Recent Prices</h3>
        {latestPrices.length === 0 ? (
          <p className="empty">No latest price data available yet.</p>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Commodity</th>
                <th className="text-left">Region</th>
                <th className="text-right">Average Price</th>
                <th className="text-left">Trend</th>
                <th className="text-left">Forecast</th>
              </tr>
            </thead>
            <tbody>
              {latestPrices.slice(0, 10).map((row) => (
                <tr key={`${row.commodity_id}-${row.region_id}`}>
                  <td>{row.commodity_name}</td>
                  <td>{row.region_code}</td>
                  <td className="text-right">{formatPeso(Number(row.avg_price))}</td>
                  <td>
                    <Link className="chip-link" href={`/trends/${row.commodity_id}`}>
                      View trend
                    </Link>
                  </td>
                  <td>
                    <Link className="chip-link" href={`/forecast/${row.commodity_id}`}>
                      View forecast
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
