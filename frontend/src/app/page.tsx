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
    <section>
      <h1>Smart Palengke Dashboard</h1>
      <p>Live baseline data from the Agri-Senta API. Latest snapshot: {latestDate}</p>
      <div className="grid" style={{ marginTop: "1rem" }}>
        <div className="card">
          <h3>Tracked Commodities</h3>
          <p>{commodities.length}</p>
        </div>
        <div className="card">
          <h3>Tracked Regions</h3>
          <p>{regions.length}</p>
        </div>
        <div className="card">
          <h3>Latest Price Rows</h3>
          <p>{latestPrices.length}</p>
        </div>
      </div>

      <div className="card" style={{ marginTop: "1rem" }}>
        <h3>Recent Prices</h3>
        {latestPrices.length === 0 ? (
          <p>No latest price data available yet.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left" }}>Commodity</th>
                <th style={{ textAlign: "left" }}>Region</th>
                <th style={{ textAlign: "right" }}>Average Price</th>
                <th style={{ textAlign: "left" }}>Trend</th>
                <th style={{ textAlign: "left" }}>Forecast</th>
              </tr>
            </thead>
            <tbody>
              {latestPrices.slice(0, 10).map((row) => (
                <tr key={`${row.commodity_id}-${row.region_id}`}>
                  <td>{row.commodity_name}</td>
                  <td>{row.region_code}</td>
                  <td style={{ textAlign: "right" }}>{formatPeso(Number(row.avg_price))}</td>
                  <td>
                    <Link href={`/trends/${row.commodity_id}`}>View trend</Link>
                  </td>
                  <td>
                    <Link href={`/forecast/${row.commodity_id}`}>View forecast</Link>
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
