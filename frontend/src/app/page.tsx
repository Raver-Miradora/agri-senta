export const dynamic = "force-dynamic";

import Link from "next/link";
import {
  LayoutDashboard,
  ShoppingBasket,
  MapPin,
  Receipt,
  ArrowRight,
  Calendar,
  Layers,
} from "lucide-react";

import DashboardTable from "@/components/DashboardTable";
import { Commodity, PaginatedLatestPrices, Region, fetchFromApiOrDefault } from "@/lib/api";

export default async function HomePage() {
  const [commodities, regions, initialPrices] = await Promise.all([
    fetchFromApiOrDefault<Commodity[]>("/commodities", []),
    fetchFromApiOrDefault<Region[]>("/regions", []),
    fetchFromApiOrDefault<PaginatedLatestPrices>("/prices/latest?limit=12&offset=0", {
      items: [],
      total: 0,
      limit: 12,
      offset: 0,
    }),
  ]);

  const latestDate = initialPrices.items[0]?.date ?? "N/A";
  const categories = Array.from(new Set(commodities.map((c) => c.category))).sort();
  const categoryCount = categories.length;

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-blue">
            <LayoutDashboard size={22} />
          </div>
          <div>
            <h1>Lagonoy Agricultural Price Dashboard</h1>
            <p className="subtitle">
              Real-time commodity price intelligence for Lagonoy, Camarines Sur.
            </p>
          </div>
        </div>
      </div>

      {/* ── Date indicator ── */}
      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", color: "var(--muted)", fontSize: "0.85rem" }}>
        <Calendar size={14} />
        <span>Latest snapshot: <strong style={{ color: "var(--text)" }}>{latestDate}</strong></span>
      </div>

      {/* ── KPI Cards ── */}
      <div className="grid grid-4">
        <div className="card kpi kpi-accent-blue">
          <div className="kpi-top">
            <p className="kpi-label">Commodities</p>
            <div className="kpi-icon kpi-icon-blue">
              <ShoppingBasket size={20} />
            </div>
          </div>
          <p className="kpi-value">{commodities.length}</p>
          <p className="kpi-detail">Tracked commodities</p>
        </div>

        <div className="card kpi kpi-accent-red">
          <div className="kpi-top">
            <p className="kpi-label">Barangays</p>
            <div className="kpi-icon kpi-icon-red">
              <MapPin size={20} />
            </div>
          </div>
          <p className="kpi-value">{regions.length}</p>
          <p className="kpi-detail">Lagonoy barangays</p>
        </div>

        <div className="card kpi kpi-accent-yellow">
          <div className="kpi-top">
            <p className="kpi-label">Price Records</p>
            <div className="kpi-icon kpi-icon-yellow">
              <Receipt size={20} />
            </div>
          </div>
          <p className="kpi-value">{initialPrices.total}</p>
          <p className="kpi-detail">Latest price entries</p>
        </div>

        <div className="card kpi kpi-accent-green">
          <div className="kpi-top">
            <p className="kpi-label">Categories</p>
            <div className="kpi-icon kpi-icon-green">
              <Layers size={20} />
            </div>
          </div>
          <p className="kpi-value">{categoryCount}</p>
          <p className="kpi-detail">Commodity groups</p>
        </div>
      </div>

      {/* ── Recent Prices Table with category filter ── */}
      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue">
            <Receipt size={18} />
          </div>
          <div>
            <h3 className="section-title">Recent Prices</h3>
            <p className="section-subtitle">Latest prevailing market prices — filter by commodity type, region, or search</p>
          </div>
        </div>

        {initialPrices.total === 0 ? (
          <div className="empty">
            <div className="empty-icon">
              <Receipt size={24} />
            </div>
            <p>No price data available yet. Data will appear once scraping runs.</p>
          </div>
        ) : (
          <DashboardTable
            regions={regions}
            categories={categories}
            initialData={initialPrices}
          />
        )}

        <div style={{ marginTop: "1rem", textAlign: "center" }}>
          <Link className="btn btn-outline" href="/prices">
            View all prices
            <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </section>
  );
}
