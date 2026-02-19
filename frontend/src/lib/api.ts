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

/* ── Auth helpers (client-side only) ── */

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("agrisenta_token");
}

export function setStoredToken(token: string): void {
  localStorage.setItem("agrisenta_token", token);
}

export function clearStoredToken(): void {
  localStorage.removeItem("agrisenta_token");
}

export async function loginApi(username: string, password: string): Promise<{ access_token: string; token_type: string }> {
  const body = new URLSearchParams({ username, password });
  const res = await fetch(`${resolveApiBaseUrl()}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => null);
    throw new Error(detail?.detail ?? `Login failed: ${res.status}`);
  }
  return res.json();
}

export async function fetchMe(): Promise<AuthUser | null> {
  const token = getStoredToken();
  if (!token) return null;
  const res = await fetch(`${resolveApiBaseUrl()}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return null;
  return res.json();
}

export async function fetchWithAuth<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getStoredToken();
  const headers: HeadersInit = { ...options.headers as Record<string, string> };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(`${resolveApiBaseUrl()}${path}`, { ...options, headers });
  if (!res.ok) {
    const detail = await res.json().catch(() => null);
    throw new Error(detail?.detail ?? `Request failed: ${res.status}`);
  }
  return res.json();
}

export type AuthUser = {
  id: number;
  username: string;
  email: string | null;
  is_active: boolean;
  is_admin: boolean;
};

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
  commodity_category: string;
  region_id: number;
  region_code: string;
  date: string;
  avg_price: number;
};

export type PaginatedLatestPrices = {
  items: LatestPrice[];
  total: number;
  limit: number;
  offset: number;
};

export type LatestPriceQuery = {
  search?: string;
  category?: string;
  region_id?: number;
  limit?: number;
  offset?: number;
};

export function buildLatestPricesUrl(params: LatestPriceQuery = {}): string {
  const sp = new URLSearchParams();
  if (params.search) sp.set("search", params.search);
  if (params.category) sp.set("category", params.category);
  if (params.region_id) sp.set("region_id", String(params.region_id));
  if (params.limit) sp.set("limit", String(params.limit));
  if (params.offset !== undefined) sp.set("offset", String(params.offset));
  const qs = sp.toString();
  return `/prices/latest${qs ? `?${qs}` : ""}`;
}

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
  commodity_category: string;
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
