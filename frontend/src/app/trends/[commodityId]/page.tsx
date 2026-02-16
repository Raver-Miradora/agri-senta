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
      <div className="page-header">
        <h1>Price Trends: {commodityId}</h1>
        <p className="subtitle">Historical average prices for this commodity.</p>
      </div>
      <div className="card">
        <SimpleLineChart data={chartData} xKey="day" yKey="avg_price" />
      </div>
      <div className="card">
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
                <td>{row.date}</td>
                <td className="text-right">{formatPeso(Number(row.avg_price))}</td>
              </tr>
            ))}
          </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
