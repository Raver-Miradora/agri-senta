import Link from "next/link";
import { LineChart, ChevronRight, Calendar } from "lucide-react";
import SimpleLineChart from "@/components/charts/SimpleLineChart";
import { PriceHistory, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

type TrendPageProps = {
  params: Promise<{ commodityId: string }>;
};

export default async function TrendPage({ params }: TrendPageProps) {
  const { commodityId } = await params;
  const history = await fetchFromApiOrDefault<PriceHistory[]>(`/prices/history/${commodityId}`, []);
  const chartData = history.map((row) => ({ day: row.date, avg_price: Number(row.avg_price) }));

  return (
    <section className="page">
      {/* Breadcrumb */}
      <nav className="breadcrumb">
        <Link href="/">Dashboard</Link>
        <ChevronRight size={14} />
        <span>Trends</span>
        <ChevronRight size={14} />
        <span>Commodity {commodityId}</span>
      </nav>

      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <LineChart size={22} />
          </div>
          <div>
            <h1>Price Trends: Commodity {commodityId}</h1>
            <p className="subtitle">Historical average prices over time.</p>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <LineChart size={18} />
          </div>
          <h3 className="section-title">Price History Chart</h3>
        </div>
        <div className="chart-container">
          <SimpleLineChart data={chartData} xKey="day" yKey="avg_price" />
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <Calendar size={18} />
          </div>
          <div>
            <h3 className="section-title">Historical Data</h3>
            <p className="section-subtitle">{history.length} record{history.length !== 1 ? "s" : ""}</p>
          </div>
        </div>
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Date</th>
                <th className="text-right">Average Price</th>
              </tr>
            </thead>
            <tbody>
              {history.map((row) => (
                <tr key={row.date}>
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
      </div>
    </section>
  );
}
