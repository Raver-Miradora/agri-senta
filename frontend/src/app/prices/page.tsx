export const dynamic = "force-dynamic";

import { Tags, Receipt } from "lucide-react";
import PricesTable from "@/components/PricesTable";
import { Commodity, PaginatedLatestPrices, Region, fetchFromApiOrDefault } from "@/lib/api";

export default async function PricesPage() {
  const [commodities, regions, initialPrices] = await Promise.all([
    fetchFromApiOrDefault<Commodity[]>("/commodities", []),
    fetchFromApiOrDefault<Region[]>("/regions", []),
    fetchFromApiOrDefault<PaginatedLatestPrices>("/prices/latest?limit=20&offset=0", {
      items: [],
      total: 0,
      limit: 20,
      offset: 0,
    }),
  ]);

  const categories = Array.from(new Set(commodities.map((c) => c.category))).sort();

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
              Use search, category filter, or region dropdown to narrow results.
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
            <p className="section-subtitle">{initialPrices.total} price records across all regions</p>
          </div>
        </div>

        {initialPrices.total === 0 ? (
          <div className="empty">
            <div className="empty-icon">
              <Tags size={24} />
            </div>
            <p>No price data yet. Trigger scraping from admin endpoint or wait for scheduler.</p>
          </div>
        ) : (
          <PricesTable
            regions={regions}
            categories={categories}
            initialData={initialPrices}
          />
        )}
      </div>
    </section>
  );
}
