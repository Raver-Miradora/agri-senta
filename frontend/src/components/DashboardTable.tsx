"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { Calendar, TrendingUp, BarChart3 } from "lucide-react";
import Pagination from "@/components/Pagination";
import CategoryFilter from "@/components/CategoryFilter";
import { LatestPrice, formatPeso } from "@/lib/api";

type DashboardTableProps = {
  data: LatestPrice[];
};

const ITEMS_PER_PAGE = 12;

export default function DashboardTable({ data }: DashboardTableProps) {
  const [category, setCategory] = useState("All");
  const [page, setPage] = useState(1);

  const categories = useMemo(
    () => Array.from(new Set(data.map((r) => r.commodity_category))).sort(),
    [data]
  );

  const filtered = useMemo(() => {
    if (category === "All") return data;
    return data.filter((r) => r.commodity_category === category);
  }, [data, category]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / ITEMS_PER_PAGE));
  const safePage = Math.min(page, totalPages);
  const pageData = filtered.slice((safePage - 1) * ITEMS_PER_PAGE, safePage * ITEMS_PER_PAGE);

  const handleCategoryChange = (cat: string) => {
    setCategory(cat);
    setPage(1);
  };

  return (
    <>
      <CategoryFilter categories={categories} selected={category} onChange={handleCategoryChange} />

      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th className="text-left">Commodity</th>
              <th className="text-left">Category</th>
              <th className="text-left">Region</th>
              <th className="text-right">Average Price</th>
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

      <Pagination currentPage={safePage} totalPages={totalPages} onPageChange={setPage} />
    </>
  );
}
