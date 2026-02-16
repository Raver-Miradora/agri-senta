import ForecastBandChart from "@/components/charts/ForecastBandChart";
import { ForecastPoint, fetchFromApiOrDefault, formatPeso } from "@/lib/api";

type ForecastCommodityPageProps = {
  params: Promise<{ commodityId: string }>;
};

export default async function ForecastCommodityPage({ params }: ForecastCommodityPageProps) {
  const { commodityId } = await params;
  const rows = await fetchFromApiOrDefault<ForecastPoint[]>(`/forecast/${commodityId}`, []);
  const chartData = rows.map((row) => ({
    day: row.forecast_date,
    predicted_price: Number(row.predicted_price),
    confidence_lower: Number(row.confidence_lower ?? row.predicted_price),
    confidence_upper: Number(row.confidence_upper ?? row.predicted_price),
  }));

  return (
    <section className="page">
      <div className="page-header">
        <h1>Forecast Detail: {commodityId}</h1>
        <p className="subtitle">7-day prediction with confidence band.</p>
      </div>
      <div className="card">
        <ForecastBandChart data={chartData} xKey="day" />
      </div>
      <div className="card">
        <div className="table-wrap">
          <table className="data-table">
          <thead>
            <tr>
              <th className="text-left">Date</th>
              <th className="text-right">Predicted</th>
              <th className="text-right">Lower</th>
              <th className="text-right">Upper</th>
              <th className="text-left">Model</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={`${row.region_id}-${row.forecast_date}`}>
                <td>{row.forecast_date}</td>
                <td className="text-right">{formatPeso(Number(row.predicted_price))}</td>
                <td className="text-right">{formatPeso(Number(row.confidence_lower ?? row.predicted_price))}</td>
                <td className="text-right">{formatPeso(Number(row.confidence_upper ?? row.predicted_price))}</td>
                <td>{row.model_used}</td>
              </tr>
            ))}
          </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
