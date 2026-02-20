"use client";

import { useState, useMemo } from "react";
import Pagination from "@/components/Pagination";
import { PriceSpike, formatPeso } from "@/lib/api";

type SpikesTableProps = {
  data: PriceSpike[];
  commodityNames: Record<number, string>;
  regionCodes: Record<number, string>;
};

const ITEMS_PER_PAGE = 15;

export default function SpikesTable({ data, commodityNames, regionCodes }: SpikesTableProps) {
  const [page, setPage] = useState(1);

  const totalPages = Math.max(1, Math.ceil(data.length / ITEMS_PER_PAGE));
  const safePage = Math.min(page, totalPages);
  const pageData = data.slice((safePage - 1) * ITEMS_PER_PAGE, safePage * ITEMS_PER_PAGE);

  return (
    <>
      <div className="results-summary">
        Showing <strong>{pageData.length}</strong> of <strong>{data.length}</strong> spike events
      </div>

      {data.length === 0 ? (
        <div className="empty">
          <p>No spikes detected from current data.</p>
        </div>
      ) : (
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th className="text-left">Date</th>
                <th className="text-left">Commodity</th>
                <th className="text-left">Barangay</th>
                <th className="text-right">Avg Price</th>
              </tr>
            </thead>
            <tbody>
              {pageData.map((row, index) => (
                <tr key={`${row.commodity_id}-${row.region_id}-${row.date}-${index}`}>
                  <td>{row.date}</td>
                  <td style={{ fontWeight: 600 }}>
                    {commodityNames[row.commodity_id] ?? `#${row.commodity_id}`}
                  </td>
                  <td>
                    <span className="badge badge-red">
                      {regionCodes[row.region_id] ?? `#${row.region_id}`}
                    </span>
                  </td>
                  <td className="text-right font-mono">{formatPeso(Number(row.avg_price))}</td>
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
