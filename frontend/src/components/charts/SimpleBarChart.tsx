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
    return <p>No chart data available.</p>;
  }

  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xKey} />
          <YAxis />
          <Tooltip />
          <Bar dataKey={yKey} fill={color} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
