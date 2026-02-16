import { Tags, Calendar, Receipt } from "lucide-react";
import { LatestPrice, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

export default async function PricesPage() {
  const latest = await fetchFromApiOrDefault<LatestPrice[]>("/prices/latest", []);

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <Tags size={22} />
          </div>
          <div>
            <h1>Price Explorer</h1>
            <p className="subtitle">Current average market prices by commodity and region.</p>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <Receipt size={18} />
          </div>
          <div>
            <h3 className="section-title">Latest Market Prices</h3>
            <p className="section-subtitle">{latest.length} price records found</p>
          </div>
        </div>

        {latest.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">
              <Tags size={24} />
            </div>
            <p>No price data yet. Trigger scraping from admin endpoint or wait for scheduler.</p>
          </div>
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
                    <td style={{ fontWeight: 600 }}>{row.commodity_name}</td>
                    <td>
                      <span className="badge badge-blue">{row.region_code}</span>
                    </td>
                    <td>
                      <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
                        <Calendar size={13} style={{ color: "var(--muted)" }} />
                        {row.date}
                      </span>
                    </td>
                    <td className="text-right font-mono">{formatPeso(Number(row.avg_price))}</td>
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
