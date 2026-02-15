import SimpleLineChart from "@/components/charts/SimpleLineChart";
import { PriceHistory, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

type TrendPageProps = {
  params: { commodityId: string };
};

export default async function TrendPage({ params }: TrendPageProps) {
  const history = await fetchFromApiOrDefault<PriceHistory[]>(`/prices/history/${params.commodityId}`, []);
  const chartData = history.map((row) => ({ day: row.date, avg_price: Number(row.avg_price) }));

  return (
    <section>
      <h1>Price Trends: {params.commodityId}</h1>
      <p>Historical average prices for this commodity.</p>
      <div className="card" style={{ marginTop: "1rem" }}>
        <SimpleLineChart data={chartData} xKey="day" yKey="avg_price" />
      </div>
      <div className="card" style={{ marginTop: "1rem" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left" }}>Date</th>
              <th style={{ textAlign: "right" }}>Average Price</th>
            </tr>
          </thead>
          <tbody>
            {history.map((row) => (
              <tr key={row.date}>
                <td>{row.date}</td>
                <td style={{ textAlign: "right" }}>{formatPeso(Number(row.avg_price))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
