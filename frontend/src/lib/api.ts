const SERVER_API_BASE_URL =
  process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

const CLIENT_API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

function resolveApiBaseUrl(): string {
  return typeof window === "undefined" ? SERVER_API_BASE_URL : CLIENT_API_BASE_URL;
}

export async function fetchFromApi<T>(path: string): Promise<T> {
  const response = await fetch(`${resolveApiBaseUrl()}${path}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function fetchFromApiOrDefault<T>(path: string, fallback: T): Promise<T> {
  try {
    return await fetchFromApi<T>(path);
  } catch {
    return fallback;
  }
}

export type Commodity = {
  id: number;
  name: string;
  category: string;
  unit: string;
};

export type Region = {
  id: number;
  name: string;
  code: string;
  island_group: string;
};

export type LatestPrice = {
  commodity_id: number;
  commodity_name: string;
  region_id: number;
  region_code: string;
  date: string;
  avg_price: number;
};

export type PriceHistory = {
  date: string;
  avg_price: number;
};

export type RegionalComparison = {
  region_id: number;
  region_name: string;
  region_code: string;
  avg_price: number;
};

export type WeeklyVariance = {
  week_start: string;
  commodity_id: number;
  commodity_name: string;
  weekly_avg_price: number;
  wow_percent_change: number | null;
};

export type PriceSpike = {
  commodity_id: number;
  region_id: number;
  date: string;
  avg_price: number;
  rolling_mean_30: number | null;
  rolling_std_30: number | null;
};

export type ForecastPoint = {
  commodity_id: number;
  region_id: number;
  forecast_date: string;
  predicted_price: number;
  confidence_lower: number | null;
  confidence_upper: number | null;
  model_used: string;
  generated_at: string;
};

export type ForecastSummary = {
  commodity_id: number;
  commodity_name: string;
  region_id: number;
  region_code: string;
  forecast_date: string;
  predicted_price: number;
  model_used: string;
};

export function formatPeso(value: number): string {
  return new Intl.NumberFormat("en-PH", {
    style: "currency",
    currency: "PHP",
    maximumFractionDigits: 2,
  }).format(value);
}
