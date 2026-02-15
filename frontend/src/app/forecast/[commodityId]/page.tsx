import ForecastBandChart from "@/components/charts/ForecastBandChart";
import { ForecastPoint, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

type ForecastCommodityPageProps = {
  params: { commodityId: string };
};

export default async function ForecastCommodityPage({ params }: ForecastCommodityPageProps) {
  const rows = await fetchFromApiOrDefault<ForecastPoint[]>(`/forecast/${params.commodityId}`, []);
  const chartData = rows.map((row) => ({
    day: row.forecast_date,
    predicted_price: Number(row.predicted_price),
    confidence_lower: Number(row.confidence_lower ?? row.predicted_price),
    confidence_upper: Number(row.confidence_upper ?? row.predicted_price),
  }));

  return (
    <section>
      <h1>Forecast Detail: {params.commodityId}</h1>
      <p>7-day prediction with confidence band.</p>
      <div className="card" style={{ marginTop: "1rem" }}>
        <ForecastBandChart data={chartData} xKey="day" />
      </div>
      <div className="card" style={{ marginTop: "1rem" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left" }}>Date</th>
              <th style={{ textAlign: "right" }}>Predicted</th>
              <th style={{ textAlign: "right" }}>Lower</th>
              <th style={{ textAlign: "right" }}>Upper</th>
              <th style={{ textAlign: "left" }}>Model</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={`${row.region_id}-${row.forecast_date}`}>
                <td>{row.forecast_date}</td>
                <td style={{ textAlign: "right" }}>{formatPeso(Number(row.predicted_price))}</td>
                <td style={{ textAlign: "right" }}>{formatPeso(Number(row.confidence_lower ?? row.predicted_price))}</td>
                <td style={{ textAlign: "right" }}>{formatPeso(Number(row.confidence_upper ?? row.predicted_price))}</td>
                <td>{row.model_used}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
