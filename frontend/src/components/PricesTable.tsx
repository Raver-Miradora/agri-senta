"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import Link from "next/link";
import { Calendar, TrendingUp, BarChart3, Search, Download, FileText, MapPin, ChevronDown } from "lucide-react";
import Pagination from "@/components/Pagination";
import CategoryFilter from "@/components/CategoryFilter";
import {
  Region,
  LatestPrice,
  PaginatedLatestPrices,
  LatestPriceQuery,
  buildLatestPricesUrl,
  fetchFromApi,
  formatPeso,
} from "@/lib/api";
import { downloadCSV, downloadPDF } from "@/lib/export";

type PricesTableProps = {
  regions: Region[];
  categories: string[];
  initialData: PaginatedLatestPrices;
};

const ITEMS_PER_PAGE = 20;
const DEBOUNCE_MS = 300;

export default function PricesTable({ regions, categories, initialData }: PricesTableProps) {
  const [category, setCategory] = useState("All");
  const [regionId, setRegionId] = useState<number | undefined>(undefined);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [data, setData] = useState<PaginatedLatestPrices>(initialData);
  const [loading, setLoading] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const fetchData = useCallback(
    async (params: LatestPriceQuery) => {
      setLoading(true);
      try {
        const url = buildLatestPricesUrl(params);
        const result = await fetchFromApi<PaginatedLatestPrices>(url);
        setData(result);
      } catch {
        /* keep stale data on error */
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    const params: LatestPriceQuery = {
      limit: ITEMS_PER_PAGE,
      offset: (page - 1) * ITEMS_PER_PAGE,
    };
    if (search.trim()) params.search = search.trim();
    if (category !== "All") params.category = category;
    if (regionId) params.region_id = regionId;

    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => fetchData(params), DEBOUNCE_MS);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [search, category, regionId, page, fetchData]);

  const totalPages = Math.max(1, Math.ceil(data.total / ITEMS_PER_PAGE));

  const handleCategoryChange = (cat: string) => {
    setCategory(cat);
    setPage(1);
  };
  const handleRegionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setRegionId(val ? Number(val) : undefined);
    setPage(1);
  };
  const handleSearchChange = (value: string) => {
    setSearch(value);
    setPage(1);
  };

  const priceColumns = [
    { key: "commodity_name" as const, label: "Commodity" },
    { key: "commodity_category" as const, label: "Category" },
    { key: "region_code" as const, label: "Region" },
    { key: "date" as const, label: "Date" },
    { key: "avg_price" as const, label: "Average Price" },
  ];

  // Export current page — for full export, server CSV endpoint is preferred
  const handleExportCSV = () => {
    downloadCSV(data.items, priceColumns, "agri-senta-prices.csv");
  };
  const handleExportPDF = () => {
    downloadPDF(data.items, priceColumns, "agri-senta-prices.pdf", "Agri-Senta — Market Prices");
  };

  return (
    <>
      {/* ── Toolbar: category + search + region + exports ── */}
      <div className="toolbar">
        <CategoryFilter categories={categories} selected={category} onChange={handleCategoryChange} />

        <div className="filter-row">
          <div className="search-box">
            <Search size={16} />
            <input
              type="text"
              placeholder="Search commodity or region…"
              value={search}
              onChange={(e) => handleSearchChange(e.target.value)}
              className="search-input"
              aria-label="Search commodities"
            />
          </div>

          <div className="select-wrap">
            <MapPin size={14} />
            <select
              value={regionId ?? ""}
              onChange={handleRegionChange}
              className="filter-select"
              aria-label="Filter by region"
            >
              <option value="">All Regions</option>
              {regions.map((r) => (
                <option key={r.id} value={r.id}>{r.code} — {r.name}</option>
              ))}
            </select>
            <ChevronDown size={14} className="select-chevron" />
          </div>

          <button className="chip-link" onClick={handleExportCSV} title="Export filtered data as CSV">
            <Download size={14} />
            CSV
          </button>
          <button className="chip-link" onClick={handleExportPDF} title="Export filtered data as PDF">
            <FileText size={14} />
            PDF
          </button>
        </div>
      </div>

      {/* ── Results summary ── */}
      <div className="results-summary">
        Showing <strong>{data.items.length}</strong> of <strong>{data.total}</strong> results
        {loading && <span className="loading-indicator"> Loading…</span>}
      </div>

      {/* ── Table ── */}
      {data.items.length === 0 ? (
        <div className="empty">
          <p>No prices match your search criteria. Try adjusting the filters.</p>
        </div>
      ) : (
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Commodity</th>
                <th className="text-left">Category</th>
                <th className="text-left">Region</th>
                <th className="text-left">Date</th>
                <th className="text-right">Avg Price</th>
                <th className="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((row: LatestPrice) => (
                <tr key={`${row.commodity_id}-${row.region_id}`}>
                  <td style={{ fontWeight: 600 }}>{row.commodity_name}</td>
                  <td>
                    <span className="badge badge-yellow">{row.commodity_category}</span>
                  </td>
                  <td>
                    <span className="badge badge-blue">{row.region_code}</span>
                  </td>
                  <td>
                    <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
                      <Calendar size={13} style={{ color: "var(--muted)" }} />
                      {row.date}
                    </span>
                  </td>
                  <td className="text-right font-mono">{formatPeso(Number(row.avg_price))}</td>
                  <td className="text-center">
                    <Link className="chip-link" href={`/trends/${row.commodity_id}`}>
                      <TrendingUp size={12} />
                      Trend
                    </Link>{" "}
                    <Link className="chip-link" href={`/forecast/${row.commodity_id}`}>
                      <BarChart3 size={12} />
                      Forecast
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* ── Pagination ── */}
      <Pagination currentPage={Math.min(page, totalPages)} totalPages={totalPages} onPageChange={setPage} />
    </>
  );
}
