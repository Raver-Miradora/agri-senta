import { LatestPrice, ForecastSummary, Commodity, Region } from "./api";

describe("API Types", () => {
  it("LatestPrice type accepts all required fields", () => {
    const price: LatestPrice = {
      commodity_id: 1,
      commodity_name: "Well-Milled Rice",
      commodity_category: "Rice",
      region_id: 1,
      region_code: "NCR",
      date: "2026-02-15",
      avg_price: 48.0,
    };
    expect(price.commodity_category).toBe("Rice");
    expect(price.avg_price).toBe(48.0);
  });

  it("ForecastSummary type accepts all required fields", () => {
    const forecast: ForecastSummary = {
      commodity_id: 1,
      commodity_name: "Well-Milled Rice",
      commodity_category: "Rice",
      region_id: 1,
      region_code: "NCR",
      forecast_date: "2026-02-20",
      predicted_price: 51.0,
      model_used: "linear_regression",
    };
    expect(forecast.commodity_category).toBe("Rice");
    expect(forecast.model_used).toBe("linear_regression");
  });

  it("Commodity type has expected shape", () => {
    const commodity: Commodity = {
      id: 1,
      name: "Well-Milled Rice",
      category: "Rice",
      unit: "kg",
    };
    expect(commodity.unit).toBe("kg");
  });

  it("Region type has expected shape", () => {
    const region: Region = {
      id: 1,
      name: "National Capital Region",
      code: "NCR",
      island_group: "Luzon",
    };
    expect(region.island_group).toBe("Luzon");
  });
});
