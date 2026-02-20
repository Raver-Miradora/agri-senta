export const dynamic = "force-dynamic";

import { Tags, Megaphone, TrendingUp, TrendingDown, Minus, Clock } from "lucide-react";
import { PriceBoardCategory, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

function TrendIcon({ change }: { change: number | null }) {
  if (change === null || change === 0) return <Minus size={14} className="trend-neutral" />;
  if (change > 0) return <TrendingUp size={14} className="trend-up" />;
  return <TrendingDown size={14} className="trend-down" />;
}

export default async function PriceBoardPage() {
  const categories = await fetchFromApiOrDefault<PriceBoardCategory[]>("/price-board", []);
  const totalItems = categories.reduce((s, c) => s + c.items.length, 0);
  const now = new Date().toLocaleDateString("en-PH", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <Megaphone size={22} />
          </div>
          <div>
            <h1>Daily Price Board</h1>
            <p className="subtitle">
              Official commodity prices from the Lagonoy Public Market.
              Updated daily by the Municipal Agriculture Office.
            </p>
          </div>
        </div>
      </div>

      {/* Date banner */}
      <div className="card" style={{ display: "flex", alignItems: "center", gap: "0.75rem", padding: "1rem 1.25rem" }}>
        <Clock size={18} style={{ color: "var(--agri-blue)", flexShrink: 0 }} />
        <div>
          <p style={{ margin: 0, fontWeight: 700, fontSize: "1rem" }}>{now}</p>
          <p style={{ margin: 0, color: "var(--muted)", fontSize: "0.82rem" }}>
            {totalItems} commodities tracked across {categories.length} categories
          </p>
        </div>
      </div>

      {categories.length === 0 ? (
        <div className="card">
          <div className="empty">
            <div className="empty-icon">
              <Tags size={24} />
            </div>
            <p>No price data for today yet. Prices are published every morning by the MAO staff.</p>
          </div>
        </div>
      ) : (
        categories.map((cat) => (
          <div className="card" key={cat.category}>
            <div className="card-header">
              <div className="card-header-icon page-icon-blue">
                <Tags size={18} />
              </div>
              <div>
                <h3 className="section-title">{cat.category}</h3>
                <p className="section-subtitle">{cat.items.length} item{cat.items.length !== 1 ? "s" : ""}</p>
              </div>
            </div>
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Commodity</th>
                    <th style={{ textAlign: "right" }}>Price</th>
                    <th style={{ textAlign: "right" }}>Prev</th>
                    <th style={{ textAlign: "right" }}>Change</th>
                  </tr>
                </thead>
                <tbody>
                  {cat.items.map((item) => (
                    <tr key={item.commodity_id}>
                      <td style={{ fontWeight: 600 }}>{item.commodity_name}</td>
                      <td style={{ textAlign: "right", fontWeight: 700, color: "var(--agri-blue)" }}>
                        {formatPeso(item.avg_price)}<span style={{ fontSize: "0.75rem", color: "var(--muted)", marginLeft: 2 }}>/{item.unit}</span>
                      </td>
                      <td style={{ textAlign: "right", color: "var(--muted)" }}>
                        {item.prev_price !== null ? formatPeso(item.prev_price) : "—"}
                      </td>
                      <td style={{ textAlign: "right" }}>
                        <span style={{
                          display: "inline-flex",
                          alignItems: "center",
                          gap: "0.25rem",
                          fontSize: "0.85rem",
                          fontWeight: 600,
                          color: item.change_percent === null || item.change_percent === 0
                            ? "var(--muted)"
                            : item.change_percent > 0
                              ? "var(--agri-red)"
                              : "var(--agri-green)",
                        }}>
                          <TrendIcon change={item.change_percent} />
                          {item.change_percent !== null ? `${Math.abs(item.change_percent).toFixed(1)}%` : "—"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))
      )}
    </section>
  );
}
