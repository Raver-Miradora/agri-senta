import { LatestPrice, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function PricesPage() {
  const latest = await fetchFromApiOrDefault<LatestPrice[]>("/prices/latest", []);

  return (
    <section>
      <h1>Price Explorer</h1>
      <p>Current average market prices by commodity and region.</p>
      <div className="card" style={{ marginTop: "1rem" }}>
        {latest.length === 0 ? (
          <p>No price data yet. Trigger scraping from admin endpoint or wait for scheduler.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left" }}>Commodity</th>
                <th style={{ textAlign: "left" }}>Region</th>
                <th style={{ textAlign: "left" }}>Date</th>
                <th style={{ textAlign: "right" }}>Avg Price</th>
              </tr>
            </thead>
            <tbody>
              {latest.map((row) => (
                <tr key={`${row.commodity_id}-${row.region_id}`}>
                  <td>{row.commodity_name}</td>
                  <td>{row.region_code}</td>
                  <td>{row.date}</td>
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
