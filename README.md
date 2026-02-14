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

- Backend startup auto-creates tables for `regions` and `commodities`
- Backend seeds initial regions and commodities
- API endpoints:
  - `GET /api/v1/health`
  - `GET /api/v1/commodities`
  - `GET /api/v1/regions`
- Frontend route shell:
  - `/`, `/prices`, `/compare`, `/forecast`, `/forecast/[commodityId]`, `/trends/[commodityId]`, `/analytics`, `/about`

## Next Build Steps

- Add `markets`, `daily_prices`, `price_forecasts`, and `scrape_logs` models
- Add price history + analytics endpoints
- Add scraper ingestion pipeline (DA + PSA)
- Add forecast training and prediction services
