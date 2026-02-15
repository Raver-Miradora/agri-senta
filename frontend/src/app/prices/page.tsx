import { LatestPrice, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function PricesPage() {
  const latest = await fetchFromApiOrDefault<LatestPrice[]>("/prices/latest", []);

  return (
    <section className="page">
      <div className="page-header">
        <h1>Price Explorer</h1>
        <p className="subtitle">Current average market prices by commodity and region.</p>
      </div>
      <div className="card">
        {latest.length === 0 ? (
          <p className="empty">No price data yet. Trigger scraping from admin endpoint or wait for scheduler.</p>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Commodity</th>
                <th className="text-left">Region</th>
                <th className="text-left">Date</th>
                <th className="text-right">Avg Price</th>
              </tr>
            </thead>
            <tbody>
              {latest.map((row) => (
                <tr key={`${row.commodity_id}-${row.region_id}`}>
                  <td>{row.commodity_name}</td>
                  <td>{row.region_code}</td>
                  <td>{row.date}</td>
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
