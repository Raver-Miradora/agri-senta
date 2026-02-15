const SERVER_API_BASE_URL =
  process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

const CLIENT_API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

function resolveApiBaseUrl(): string {
  return typeof window === "undefined" ? SERVER_API_BASE_URL : CLIENT_API_BASE_URL;
}

export async function fetchFromApi<T>(path: string): Promise<T> {
  const response = await fetch(`${resolveApiBaseUrl()}${path}`, {
    next: { revalidate: 3600 },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
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
