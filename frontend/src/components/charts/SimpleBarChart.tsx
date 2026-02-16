"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type SimpleBarChartProps = {
  data: Array<Record<string, string | number | null>>;
  xKey: string;
  yKey: string;
  color?: string;
  height?: number;
};

export default function SimpleBarChart({
  data,
  xKey,
  yKey,
  color = "#CE1126",
  height = 320,
}: SimpleBarChartProps) {
  if (data.length === 0) {
    return (
      <div className="empty">
        <p>No chart data available.</p>
      </div>
    );
  }

  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer>
        <BarChart data={data} margin={{ top: 8, right: 16, bottom: 4, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey={xKey} fontSize={12} tick={{ fill: "#6b7280" }} />
          <YAxis fontSize={12} tick={{ fill: "#6b7280" }} />
          <Tooltip
            contentStyle={{
              borderRadius: "8px",
              border: "1px solid #e5e7eb",
              boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
              fontSize: "0.85rem",
            }}
          />
          <Bar dataKey={yKey} fill={color} radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
