"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type SimpleLineChartProps = {
  data: Array<Record<string, string | number | null>>;
  xKey: string;
  yKey: string;
  color?: string;
  height?: number;
};

export default function SimpleLineChart({
  data,
  xKey,
  yKey,
  color = "#0038A8",
  height = 320,
}: SimpleLineChartProps) {
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
        <LineChart data={data} margin={{ top: 8, right: 16, bottom: 4, left: 0 }}>
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
          <Line
            type="monotone"
            dataKey={yKey}
            stroke={color}
            strokeWidth={2.5}
            dot={false}
            activeDot={{ r: 5, strokeWidth: 2, fill: "#fff" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
