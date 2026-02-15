"use client";

import {
  Area,
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
    return <p>No forecast data available.</p>;
  }

  return (
    <div style={{ width: "100%", height: 340 }}>
      <ResponsiveContainer>
        <ComposedChart data={data}>
          <XAxis dataKey={xKey} />
          <YAxis />
          <Tooltip />
          <Area dataKey="confidence_upper" stroke="#FCD116" fill="#FCD116" fillOpacity={0.2} />
          <Area dataKey="confidence_lower" stroke="#FCD116" fill="#ffffff" fillOpacity={1} />
          <Line dataKey="predicted_price" stroke="#0038A8" strokeWidth={2} dot={false} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
