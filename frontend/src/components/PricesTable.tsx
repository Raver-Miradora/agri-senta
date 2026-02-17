"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { Calendar, TrendingUp, BarChart3, Search } from "lucide-react";
import Pagination from "@/components/Pagination";
import CategoryFilter from "@/components/CategoryFilter";
import { LatestPrice, formatPeso } from "@/lib/api";

type PricesTableProps = {
  data: LatestPrice[];
};

const ITEMS_PER_PAGE = 20;

export default function PricesTable({ data }: PricesTableProps) {
  const [category, setCategory] = useState("All");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  const categories = useMemo(
    () => Array.from(new Set(data.map((r) => r.commodity_category))).sort(),
    [data]
  );

  const filtered = useMemo(() => {
    let result = data;
    if (category !== "All") {
      result = result.filter((r) => r.commodity_category === category);
    }
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(
        (r) =>
          r.commodity_name.toLowerCase().includes(q) ||
          r.region_code.toLowerCase().includes(q)
      );
    }
    return result;
  }, [data, category, search]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / ITEMS_PER_PAGE));
  const safePage = Math.min(page, totalPages);
  const pageData = filtered.slice((safePage - 1) * ITEMS_PER_PAGE, safePage * ITEMS_PER_PAGE);

  // Reset page when filter changes
  const handleCategoryChange = (cat: string) => {
    setCategory(cat);
    setPage(1);
  };
  const handleSearchChange = (value: string) => {
    setSearch(value);
    setPage(1);
  };

  return (
    <>
      {/* ── Toolbar: category filter + search ── */}
      <div className="toolbar">
        <CategoryFilter categories={categories} selected={category} onChange={handleCategoryChange} />
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
      </div>

      {/* ── Results summary ── */}
      <div className="results-summary">
        Showing <strong>{pageData.length}</strong> of <strong>{filtered.length}</strong> results
        {category !== "All" && (
          <span className="results-filter">
            in <span className="badge badge-blue">{category}</span>
          </span>
        )}
      </div>

      {/* ── Table ── */}
      {filtered.length === 0 ? (
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
              {pageData.map((row) => (
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
      <Pagination currentPage={safePage} totalPages={totalPages} onPageChange={setPage} />
    </>
  );
}
