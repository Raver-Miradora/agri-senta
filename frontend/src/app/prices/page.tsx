export const dynamic = "force-dynamic";

import { Tags, Receipt } from "lucide-react";
import PricesTable from "@/components/PricesTable";
import { LatestPrice, fetchFromApiOrDefault } from "@/lib/api";

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
            <p className="subtitle">
              Browse current market prices by commodity and region.
              Use the category filter to narrow results.
            </p>
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
            <p className="section-subtitle">{latest.length} price records across all regions</p>
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
          <PricesTable data={latest} />
        )}
      </div>
    </section>
  );
}
