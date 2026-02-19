# Agri-Senta

**Smart Palengke Dashboard** — Real-time commodity price intelligence across Philippine regions.

Track, compare, and forecast market prices for 37 commodities across 17 regions using ML-powered predictions, with a modern responsive dashboard.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) · TypeScript · Recharts · Lucide Icons |
| Backend | FastAPI · SQLAlchemy 2 (async) · Pydantic v2 |
| Database | PostgreSQL 16 |
| ML Engine | scikit-learn (Linear Regression) · statsmodels (ARIMA) |
| Auth | JWT (python-jose) · bcrypt · OAuth2 password flow |
| Rate Limiting | slowapi (60/min default, 10/min auth) |
| Scheduler | APScheduler (daily scrape + weekly forecast) |
| Export | CSV (backend streaming + client-side) · PDF (jsPDF + autoTable) |
| Testing | pytest · pytest-asyncio · Jest · Testing Library |
| CI/CD | GitHub Actions (lint, test, build, Docker) |
| Infrastructure | Docker Compose · multi-stage Dockerfiles · healthchecks |

---

## Quick Start

### Docker (recommended)

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:3000 |
| API docs (Swagger) | http://localhost:8000/docs |
| Health check | http://localhost:8000/api/v1/health |

### Local Development

```bash
# 1. Start PostgreSQL (via Docker or local install)
docker compose up -d postgres

# 2. Backend
cd backend
python -m venv .venv
.venv/Scripts/activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 3. Frontend
cd frontend
npm install
npm run dev
```

> **Default admin:** `admin` / `admin123` (configurable via env vars)

---

## Features

### Dashboard & Data
- **KPI Cards** — Commodities, regions, price records, and category counts
- **37 Commodities** across 7 categories (Rice, Vegetables, Meat, Fish & Seafood, Fruits, Poultry & Dairy, Other Essentials)
- **17 Philippine Regions** — NCR, CAR, BARMM, R01–R13
- **Regional Comparison** — side-by-side bar charts
- **Historical Trends** — line charts per commodity

### ML Forecasting
- **Dual-model evaluation** — Linear Regression vs ARIMA(1,1,1) on 80/20 time-split
- **Best model selection** — winner retrained on full dataset for production
- **7-day forecasts** with confidence bands
- **Auto-regenerated** weekly via APScheduler

### Authentication & Authorization
- **JWT-based** auth with 60-minute token expiry
- **Role-based access** — admin-only endpoints protected
- **Admin dashboard** — scrape triggers, user management
- **Login page** with form validation

### Export
- **CSV Export** — backend streaming endpoints + client-side filtered export
- **PDF Export** — branded tables with jsPDF + autoTable
- **Per-table** — export buttons on Prices and Forecast tables

### Dark Mode
- **System preference detection** (`prefers-color-scheme`)
- **Toggle button** (Sun/Moon) in navbar
- **localStorage persistence** across sessions
- **Full CSS custom property** override system

### API Rate Limiting
- **60 requests/minute** default on all endpoints
- **10 requests/minute** on `/auth/login` (brute-force protection)
- **In-memory storage** via slowapi

---

## API Endpoints

### Health & Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/auth/login` | OAuth2 login (rate-limited 10/min) |
| `GET` | `/api/v1/auth/me` | Current user info |
| `POST` | `/api/v1/auth/register` | Register user (admin only) |

### Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/commodities` | List all commodities |
| `GET` | `/api/v1/regions` | List all regions |
| `GET` | `/api/v1/prices/daily` | Daily prices (filterable) |
| `GET` | `/api/v1/prices/latest` | Latest price per commodity-region |
| `GET` | `/api/v1/prices/history/{id}` | Price history for a commodity |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/analytics/weekly-variance` | Weekly price variance |
| `GET` | `/api/v1/analytics/regional-comparison` | Cross-region comparison |
| `GET` | `/api/v1/analytics/price-spikes` | Spike detection |
| `GET` | `/api/v1/analytics/cheapest-region/{id}` | Cheapest region for commodity |
| `GET` | `/api/v1/analytics/rolling-average/{id}` | Rolling average |
| `GET` | `/api/v1/analytics/seasonal/{id}` | Seasonal patterns |

### Forecasting & Export
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/forecast/summary` | All forecast summaries |
| `GET` | `/api/v1/forecast/{id}` | Forecast detail for commodity |
| `GET` | `/api/v1/export/prices.csv` | Stream all prices as CSV |
| `GET` | `/api/v1/export/forecasts.csv` | Stream all forecasts as CSV |

### Admin (requires admin JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/admin/scrape/trigger` | Trigger data scrape |
| `GET` | `/api/v1/admin/scrape/logs` | Scraping logs |

---

## Frontend Pages

| Route | Description |
|-------|-------------|
| `/` | Dashboard — KPI cards, latest prices table |
| `/prices` | Price explorer — searchable, filterable, with CSV/PDF export |
| `/compare` | Regional comparison — bar charts |
| `/analytics` | Weekly variance, spike detection |
| `/forecast` | Forecast summary — all predictions with CSV/PDF export |
| `/forecast/[id]` | 7-day forecast detail with confidence band chart |
| `/trends/[id]` | Historical price trend line chart |
| `/login` | Authentication page |
| `/admin` | Admin dashboard (admin only) |
| `/about` | Project information |

---

## Testing

### Backend (95 tests)

```bash
cd backend
pytest -v                         # full suite
pytest tests/test_export.py -v    # specific module
```

Test coverage includes: models, schemas, all routers (health, auth, commodities, regions, prices, analytics, forecast, export), ML forecasting, data cleaner, rate limiting.

### Frontend (18 tests)

```bash
cd frontend
npm test                          # Jest + Testing Library
npx tsc --noEmit                  # type-check
npm run lint                      # ESLint
```

### CI/CD

GitHub Actions runs on every push/PR to `main`:
1. **Backend** — Ruff lint + format check + pytest (with PostgreSQL service)
2. **Frontend** — ESLint + TypeScript + Jest + Next.js build
3. **Docker** — Compose build verification

---

## Project Structure

```
agri-senta/
├── .github/workflows/ci.yml     # CI/CD pipeline
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI entry + lifespan
│   │   ├── config.py             # Pydantic settings
│   │   ├── database.py           # Async SQLAlchemy engine
│   │   ├── rate_limit.py         # slowapi limiter setup
│   │   ├── models/               # ORM models (8 models)
│   │   │   ├── commodity.py
│   │   │   ├── daily_price.py
│   │   │   ├── market.py
│   │   │   ├── price_forecast.py
│   │   │   ├── region.py
│   │   │   ├── scrape_log.py
│   │   │   └── user.py
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── routers/              # API route handlers (9 routers)
│   │   │   ├── admin.py
│   │   │   ├── analytics.py
│   │   │   ├── auth.py
│   │   │   ├── commodities.py
│   │   │   ├── export.py
│   │   │   ├── forecast.py
│   │   │   ├── health.py
│   │   │   ├── prices.py
│   │   │   └── regions.py
│   │   ├── services/             # Business logic layer
│   │   │   ├── analytics_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── forecast_service.py
│   │   │   ├── pipeline_service.py
│   │   │   └── price_service.py
│   │   ├── dependencies/         # FastAPI dependencies (auth guards)
│   │   ├── ml/                   # ML training & prediction
│   │   ├── scraping/             # Web scrapers, cleaner, loader
│   │   └── utils/                # Seed data (37×17)
│   ├── tests/                    # 12 test modules, 95 tests
│   ├── Dockerfile                # Python 3.12-slim
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── app/                  # Next.js App Router (10 routes)
│   │   ├── components/           # UI components + charts
│   │   │   ├── Navbar.tsx
│   │   │   ├── DashboardTable.tsx
│   │   │   ├── PricesTable.tsx
│   │   │   ├── ForecastTable.tsx
│   │   │   ├── SpikesTable.tsx
│   │   │   ├── Pagination.tsx
│   │   │   ├── CategoryFilter.tsx
│   │   │   └── charts/           # Recharts wrappers
│   │   └── lib/
│   │       ├── api.ts            # API client + types
│   │       ├── export.ts         # CSV/PDF export utilities
│   │       ├── AuthContext.tsx    # JWT auth context
│   │       └── ThemeContext.tsx   # Dark mode context
│   ├── Dockerfile                # Multi-stage Node 20-alpine
│   └── package.json
└── docker-compose.yml            # PostgreSQL + Backend + Frontend
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://agrisenta:password@localhost:5432/agrisenta` | PostgreSQL connection |
| `SECRET_KEY` | `dev-secret-change-in-production` | JWT signing key |
| `DEFAULT_ADMIN_USERNAME` | `admin` | Initial admin username |
| `DEFAULT_ADMIN_PASSWORD` | `admin123` | Initial admin password |
| `CORS_ORIGINS` | `["http://localhost:3000"]` | Allowed CORS origins |
| `RATE_LIMIT_DEFAULT` | `60/minute` | Default API rate limit |
| `RATE_LIMIT_AUTH` | `10/minute` | Auth endpoint rate limit |
| `SCRAPE_SCHEDULE_CRON` | `0 6 * * *` | Daily scrape schedule |
| `FORECAST_SCHEDULE_CRON` | `0 0 * * 0` | Weekly forecast schedule |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000/api/v1` | Frontend API base URL |

---

## License

This project is for educational and research purposes.
