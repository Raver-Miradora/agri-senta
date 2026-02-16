"use client";

import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type ForecastBandChartProps = {
  data: Array<Record<string, string | number | null>>;
  xKey: string;
};

export default function ForecastBandChart({ data, xKey }: ForecastBandChartProps) {
  if (data.length === 0) {
    return (
      <div className="empty">
        <p>No forecast data available.</p>
      </div>
    );
  }

  return (
    <div style={{ width: "100%", height: 340 }}>
      <ResponsiveContainer>
        <ComposedChart data={data} margin={{ top: 8, right: 16, bottom: 4, left: 0 }}>
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
          <Area dataKey="confidence_upper" stroke="#FCD116" fill="#FCD116" fillOpacity={0.18} />
          <Area dataKey="confidence_lower" stroke="#FCD116" fill="#ffffff" fillOpacity={1} />
          <Line
            dataKey="predicted_price"
            stroke="#0038A8"
            strokeWidth={2.5}
            dot={{ r: 4, fill: "#0038A8", strokeWidth: 2, stroke: "#fff" }}
            activeDot={{ r: 6, strokeWidth: 2, fill: "#fff" }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
