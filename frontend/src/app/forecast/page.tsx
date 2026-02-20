export const dynamic = "force-dynamic";

import { TrendingUp, Brain } from "lucide-react";
import ForecastTable from "@/components/ForecastTable";
import { ForecastSummary, fetchFromApiOrDefault } from "@/lib/api";

export default async function ForecastPage() {
  const rows = await fetchFromApiOrDefault<ForecastSummary[]>("/forecast/summary", []);

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <TrendingUp size={22} />
          </div>
          <div>
            <h1>Forecast</h1>
            <p className="subtitle">
              ML-generated price predictions per commodity-barangay pair.
              Filter by category to find specific forecasts quickly.
            </p>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <Brain size={18} />
          </div>
          <div>
            <h3 className="section-title">Forecast Results</h3>
            <p className="section-subtitle">{rows.length} forecast{rows.length !== 1 ? "s" : ""} generated</p>
          </div>
        </div>

        {rows.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">
              <TrendingUp size={24} />
            </div>
            <p>No forecast data yet. Ensure backend startup completed forecast generation.</p>
          </div>
        ) : (
          <ForecastTable data={rows} />
        )}
      </div>
    </section>
  );
}
