# Agri-Senta

Agri-Senta is a Smart Palengke Dashboard for tracking and forecasting commodity prices across Philippine regions.

## Stack

- Frontend: Next.js 14 + TypeScript
- Backend: FastAPI + SQLAlchemy (async)
- Database: PostgreSQL 16
- Orchestration: Docker Compose

## Quick Start (Docker)

1. From project root, run:

   ```bash
   docker compose up --build
   ```

2. Open apps:
   - Frontend: http://localhost:3000
   - Backend docs: http://localhost:8000/docs
   - Health: http://localhost:8000/api/v1/health

## Implemented Baseline

- Backend startup auto-creates tables for `regions`, `commodities`, `markets`, `daily_prices`, `price_forecasts`, and `scrape_logs`
- Backend seeds initial regions, commodities, and markets
- API endpoints:
  - `GET /api/v1/health`
  - `GET /api/v1/commodities`
  - `GET /api/v1/regions`
  - `POST /api/v1/admin/scrape/trigger?source=DA|PSA`
  - `GET /api/v1/admin/scrape/logs`
- Frontend route shell:
  - `/`, `/prices`, `/compare`, `/forecast`, `/forecast/[commodityId]`, `/trends/[commodityId]`, `/analytics`, `/about`

## Phase 2 Scaffolding Included

- DA/PSA scraper modules and data cleaner
- Upsert loader for `daily_prices`
- Scrape log writer and basic ingestion service orchestration
- APScheduler wiring for daily scrape schedule (Asia/Manila)

## Phase 3 API Included

- Price endpoints:
  - `GET /api/v1/prices/daily`
  - `GET /api/v1/prices/latest`
  - `GET /api/v1/prices/history/{commodity_id}`
- Analytics endpoints:
  - `GET /api/v1/analytics/weekly-variance`
  - `GET /api/v1/analytics/regional-comparison`
  - `GET /api/v1/analytics/price-spikes`
  - `GET /api/v1/analytics/cheapest-region/{commodity_id}`
  - `GET /api/v1/analytics/rolling-average/{commodity_id}`
  - `GET /api/v1/analytics/seasonal/{commodity_id}`

## Phase 4 Forecasting Included

- ML training pipeline with Linear Regression + ARIMA fallback in `backend/app/ml/`
- Forecast generation service stores 7-day predictions in `price_forecasts`
- Forecast endpoints:
  - `GET /api/v1/forecast/summary`
  - `GET /api/v1/forecast/{commodity_id}`
- Startup warm generation of forecasts and weekly scheduler regeneration job

## Phase 5 Frontend Views Included

- Dashboard home now shows live summary cards and recent price rows
- Price Explorer now renders a live latest-prices table
- Regional Comparison now includes bar chart + table from analytics API
- Analytics page now includes weekly variance line chart and spike table
- Forecast pages now render summary table and per-commodity confidence-band chart
- Trends page now renders historical line chart and table by commodity

## Phase 6 Reliability & QA Included

- Frontend global `loading.tsx`, `error.tsx`, and `not-found.tsx` routes for resilient UX
- Docker Compose healthchecks for `postgres`, `backend`, and `frontend`
- Service startup dependency ordering based on health state (`depends_on.condition: service_healthy`)
- Backend smoke/unit tests:
  - `tests/test_health_router.py`
  - `tests/test_ml_forecast.py`
- Pytest config added in `backend/pytest.ini`

## Next Build Steps

- Add advanced filters (commodity/region/date) and richer dashboard UI components
