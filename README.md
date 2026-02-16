# Agri-Senta

**Smart Palengke Dashboard** — Track, compare, and forecast commodity prices across Philippine regions.

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + TypeScript + Recharts |
| Backend | FastAPI + SQLAlchemy 2 (async) + Pydantic |
| Database | PostgreSQL 16 |
| ML Engine | scikit-learn (LinearRegression) + statsmodels (ARIMA) |
| Scheduler | APScheduler (daily scrape + weekly forecast) |
| Infrastructure | Docker Compose with healthchecks |

## Quick Start (Docker)

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API docs | http://localhost:8000/docs |
| Health check | http://localhost:8000/api/v1/health |

## Quick Start (Local)

```bash
# Backend
cd backend
python -m venv .venv && .venv/Scripts/activate  # or source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # update DATABASE_URL to your local PG
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## API Endpoints

### Core
- `GET /api/v1/health`
- `GET /api/v1/commodities`
- `GET /api/v1/regions`

### Prices
- `GET /api/v1/prices/daily?commodity_id=&region_id=&from=&to=&limit=200`
- `GET /api/v1/prices/latest`
- `GET /api/v1/prices/history/{commodity_id}`

### Analytics
- `GET /api/v1/analytics/weekly-variance`
- `GET /api/v1/analytics/regional-comparison`
- `GET /api/v1/analytics/price-spikes`
- `GET /api/v1/analytics/cheapest-region/{commodity_id}`
- `GET /api/v1/analytics/rolling-average/{commodity_id}`
- `GET /api/v1/analytics/seasonal/{commodity_id}`

### Forecasting
- `GET /api/v1/forecast/summary`
- `GET /api/v1/forecast/{commodity_id}`

### Admin
- `POST /api/v1/admin/scrape/trigger?source=DA|PSA`
- `GET /api/v1/admin/scrape/logs`

## Frontend Pages

| Route | Description |
|-------|-------------|
| `/` | Dashboard with KPI cards and latest price table |
| `/prices` | Price explorer — sortable latest prices |
| `/compare` | Regional price comparison with bar chart |
| `/analytics` | Weekly variance chart and spike detection |
| `/forecast` | Forecast summary table |
| `/forecast/[id]` | 7-day forecast detail with confidence band chart |
| `/trends/[id]` | Historical price trend line chart |
| `/about` | About page with project info |

## ML Engine

Models are evaluated on an 80/20 time-split, and the winner is retrained on the **full dataset** for production forecasting:

- **Linear Regression** — index-based trend model
- **ARIMA(1,1,1)** — time-series model with differencing

Forecasts are generated at startup and regenerated weekly via scheduler.

## Testing

```bash
cd backend
pytest -v
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry + lifespan
│   │   ├── config.py         # Pydantic settings
│   │   ├── database.py       # Async SQLAlchemy
│   │   ├── models/           # ORM models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routers/          # API route handlers
│   │   ├── services/         # Business logic
│   │   ├── ml/               # ML training & prediction
│   │   ├── scraping/         # Scrapers, cleaner, loader, scheduler
│   │   └── utils/            # Seed data
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # Chart components (Recharts)
│   │   └── lib/              # API client + types
│   ├── Dockerfile            # Multi-stage production build
│   └── package.json
├── docker-compose.yml
└── BLUEPRINT.md
```
