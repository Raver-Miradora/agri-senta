"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { ArrowRight, Calendar, Search, Download, FileText } from "lucide-react";
import Pagination from "@/components/Pagination";
import CategoryFilter from "@/components/CategoryFilter";
import { ForecastSummary, formatPeso } from "@/lib/api";
import { downloadCSV, downloadPDF } from "@/lib/export";

type ForecastTableProps = {
  data: ForecastSummary[];
};

const ITEMS_PER_PAGE = 20;

export default function ForecastTable({ data }: ForecastTableProps) {
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

  const handleCategoryChange = (cat: string) => {
    setCategory(cat);
    setPage(1);
  };
  const handleSearchChange = (value: string) => {
    setSearch(value);
    setPage(1);
  };

  const forecastColumns = [
    { key: "commodity_name" as const, label: "Commodity" },
    { key: "commodity_category" as const, label: "Category" },
    { key: "region_code" as const, label: "Barangay" },
    { key: "forecast_date" as const, label: "Forecast Date" },
    { key: "predicted_price" as const, label: "Predicted Price" },
    { key: "model_used" as const, label: "Model" },
  ];

  const handleExportCSV = () => {
    downloadCSV(filtered, forecastColumns, "agri-senta-forecasts.csv");
  };

  const handleExportPDF = () => {
    downloadPDF(filtered, forecastColumns, "agri-senta-forecasts.pdf", "Agri-Senta — Forecast Results");
  };

  return (
    <>
      <div className="toolbar">
        <CategoryFilter categories={categories} selected={category} onChange={handleCategoryChange} />
        <div className="search-box">
          <Search size={16} />
          <input
            type="text"
            placeholder="Search commodity or barangay…"
            value={search}
            onChange={(e) => handleSearchChange(e.target.value)}
            className="search-input"
            aria-label="Search forecasts"
          />
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

      <div className="results-summary">
        Showing <strong>{pageData.length}</strong> of <strong>{filtered.length}</strong> forecasts
        {category !== "All" && (
          <span className="results-filter">
            in <span className="badge badge-blue">{category}</span>
          </span>
        )}
      </div>

      {filtered.length === 0 ? (
        <div className="empty">
          <p>No forecasts match your search criteria.</p>
        </div>
      ) : (
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Commodity</th>
                <th className="text-left">Category</th>
                <th className="text-left">Barangay</th>
                <th className="text-left">Forecast Date</th>
                <th className="text-right">Predicted Price</th>
                <th className="text-center">Model</th>
                <th className="text-center">Detail</th>
              </tr>
            </thead>
            <tbody>
              {pageData.map((row) => (
                <tr key={`${row.commodity_id}-${row.region_id}-${row.forecast_date}`}>
                  <td style={{ fontWeight: 600 }}>{row.commodity_name}</td>
                  <td>
                    <span className="badge badge-yellow">{row.commodity_category}</span>
                  </td>
                  <td>
                    <span className="badge badge-red">{row.region_code}</span>
                  </td>
                  <td>
                    <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
                      <Calendar size={13} style={{ color: "var(--muted)" }} />
                      {row.forecast_date}
                    </span>
                  </td>
                  <td className="text-right font-mono">{formatPeso(Number(row.predicted_price))}</td>
                  <td className="text-center">
                    <span className="badge badge-green">{row.model_used}</span>
                  </td>
                  <td className="text-center">
                    <Link className="chip-link" href={`/forecast/${row.commodity_id}`}>
                      <ArrowRight size={12} />
                      Open
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Pagination currentPage={safePage} totalPages={totalPages} onPageChange={setPage} />
    </>
  );
}
