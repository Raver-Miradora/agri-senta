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
    return <p>No chart data available.</p>;
  }

  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xKey} />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey={yKey} stroke={color} strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
