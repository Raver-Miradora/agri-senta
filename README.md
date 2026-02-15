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

## Next Build Steps

- Add forecast training and prediction services
