# 🇵🇭 Agri-Senta — The Smart Palengke Dashboard

## Complete System Blueprint

---

## 1. Executive Summary

**Agri-Senta** is a full-stack data dashboard that tracks, visualizes, and predicts daily commodity prices (rice, onion, pork, vegetables, meat, fish) across Philippine regions (NCR, Bicol, Visayas, Mindanao). It empowers consumers, sari-sari store owners, and carinderia operators with actionable pricing intelligence sourced from the Department of Agriculture (DA) and PSA.

---

## 2. Final Tech Stack

| Layer | Technology | Justification |
|---|---|---|
| **Frontend** | **Next.js 14 (App Router)** + TypeScript | SSR/SSG for SEO, file-based routing, React Server Components for speed |
| **Charting** | **Recharts** | React-native, composable, great for line/area/bar charts |
| **UI Components** | **shadcn/ui + Tailwind CSS** | Modern, accessible, highly customizable Filipino-themed UI |
| **State Management** | **TanStack Query (React Query)** | Server-state caching, background refetching, optimistic updates |
| **Backend API** | **Python FastAPI** | Async, auto OpenAPI docs, Pydantic validation, ML-friendly ecosystem |
| **Database** | **PostgreSQL 16** | Robust relational DB, excellent for time-series price data, window functions |
| **ORM** | **SQLAlchemy 2.0 + Alembic** | Async support, migration management |
| **Data Scraping** | **httpx + BeautifulSoup4 + Playwright** | httpx for API calls, BS4 for HTML parsing, Playwright for JS-rendered pages |
| **Task Scheduler** | **APScheduler** (or Celery + Redis for scale) | Scheduled daily scraping jobs |
| **ML / Forecasting** | **Scikit-learn + Statsmodels** | Linear regression, ARIMA for price forecasting |
| **Data Processing** | **Pandas + NumPy** | Data cleaning, transformation, statistical calculations |
| **Containerization** | **Docker + Docker Compose** | Consistent dev/prod environments |
| **Testing** | **Pytest (Backend)**, **Vitest + Playwright (Frontend)** | Unit, integration, E2E coverage |

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AGRI-SENTA ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐    │
│  │  DA Website   │     │  PSA Website  │     │  BangkoPilipinas │    │
│  │  Price Watch  │     │  OpenSTAT     │     │  (Exchange Rate) │    │
│  └──────┬───────┘     └──────┬───────┘     └────────┬─────────┘    │
│         │                    │                       │              │
│         ▼                    ▼                       ▼              │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │              DATA INGESTION LAYER (Python)               │       │
│  │  ┌──────────┐  ┌───────────┐  ┌──────────────────────┐  │       │
│  │  │ Scrapers │  │ Cleaners  │  │  Scheduled Jobs      │  │       │
│  │  │ (httpx/  │  │ (Pandas)  │  │  (APScheduler)       │  │       │
│  │  │  BS4/    │  │           │  │  Daily @ 6AM PHT     │  │       │
│  │  │Playwright)│  │           │  │                      │  │       │
│  │  └──────────┘  └───────────┘  └──────────────────────┘  │       │
│  └─────────────────────────┬───────────────────────────────┘       │
│                            │                                        │
│                            ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │                  PostgreSQL 16 Database                   │       │
│  │  ┌────────────┐ ┌──────────┐ ┌────────────────────────┐  │       │
│  │  │ Commodities│ │  Prices  │ │  Forecasts (cached)    │  │       │
│  │  │ Regions    │ │  Markets │ │  Scrape Logs           │  │       │
│  │  └────────────┘ └──────────┘ └────────────────────────┘  │       │
│  └─────────────────────────┬───────────────────────────────┘       │
│                            │                                        │
│                            ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │              FastAPI Backend (Python 3.12)                │       │
│  │  ┌──────────┐ ┌───────────┐ ┌──────────────────────┐    │       │
│  │  │ REST API │ │ ML Engine │ │  Analytics Engine     │    │       │
│  │  │ Endpoints│ │ (Scikit)  │ │  (SQL + Pandas)      │    │       │
│  │  └──────────┘ └───────────┘ └──────────────────────┘    │       │
│  └─────────────────────────┬───────────────────────────────┘       │
│                            │                                        │
│                            ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │              Next.js 14 Frontend (TypeScript)             │       │
│  │  ┌──────────┐ ┌───────────┐ ┌──────────────────────┐    │       │
│  │  │Dashboard │ │  Charts   │ │  Forecast View       │    │       │
│  │  │  Pages   │ │ (Recharts)│ │  Region Comparison   │    │       │
│  │  └──────────┘ └───────────┘ └──────────────────────┘    │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Module Breakdown

### MODULE 1: Data Ingestion & Scraping Pipeline

**Purpose:** Automated daily scraping and cleaning of commodity prices from government sources.

| Sub-module | Description |
|---|---|
| `scraper_da.py` | Scrapes DA Price Watch daily monitoring page for retail/wholesale prices |
| `scraper_psa.py` | Scrapes/downloads PSA OpenSTAT CSV datasets for historical price data |
| `scraper_bantay_presyo.py` | Scrapes Bantay Presyo (DTI) for consumer goods pricing |
| `data_cleaner.py` | Standardizes commodity names, normalizes units (per kg/per piece), handles missing values |
| `data_loader.py` | Batch inserts cleaned data into PostgreSQL with upsert logic (no duplicates) |
| `scheduler.py` | APScheduler cron jobs: daily scrape at 6 AM PHT, weekly forecast regeneration |
| `scrape_logger.py` | Logs scrape status, errors, row counts for monitoring |

**Data Sources:**
- DA Price Watch: `https://www.da.gov.ph/price-monitoring/`
- PSA OpenSTAT: `https://openstat.psa.gov.ph/`
- DTI Bantay Presyo (supplemental)

---

### MODULE 2: Database Layer

**Purpose:** Store, query, and aggregate commodity pricing data efficiently.

#### Database Schema (ERD)

```
┌──────────────────┐     ┌──────────────────────────────────┐
│   regions         │     │          commodities              │
├──────────────────┤     ├──────────────────────────────────┤
│ id          PK   │     │ id                    PK         │
│ name             │     │ name                             │
│ code (NCR, etc.) │     │ category (vegetable/meat/grain)  │
│ island_group     │     │ unit (kg/piece/bundle)           │
│ created_at       │     │ image_url                        │
└────────┬─────────┘     └──────────────┬───────────────────┘
         │                              │
         │         ┌────────────────┐   │
         │         │    markets      │   │
         │         ├────────────────┤   │
         │         │ id        PK   │   │
         │         │ name           │   │
         └────────►│ region_id FK   │   │
                   │ type (wet/dry) │   │
                   │ address        │   │
                   └───────┬────────┘   │
                           │            │
                           ▼            ▼
                   ┌─────────────────────────────┐
                   │        daily_prices           │
                   ├─────────────────────────────┤
                   │ id                 PK       │
                   │ commodity_id       FK       │
                   │ market_id          FK       │
                   │ region_id          FK       │
                   │ price_low          DECIMAL  │
                   │ price_high         DECIMAL  │
                   │ price_avg          DECIMAL  │
                   │ price_prevailing   DECIMAL  │
                   │ date               DATE     │
                   │ source             VARCHAR  │
                   │ created_at         TIMESTAMP│
                   └─────────────────────────────┘

┌──────────────────────────────┐    ┌──────────────────────────────┐
│       price_forecasts         │    │        scrape_logs            │
├──────────────────────────────┤    ├──────────────────────────────┤
│ id                 PK        │    │ id                 PK       │
│ commodity_id       FK        │    │ source             VARCHAR  │
│ region_id          FK        │    │ status (success/fail)       │
│ forecast_date      DATE      │    │ rows_ingested      INT     │
│ predicted_price    DECIMAL   │    │ error_message      TEXT     │
│ confidence_lower   DECIMAL   │    │ duration_seconds   FLOAT   │
│ confidence_upper   DECIMAL   │    │ executed_at        TIMESTAMP│
│ model_used         VARCHAR   │    └──────────────────────────────┘
│ generated_at       TIMESTAMP │
└──────────────────────────────┘

┌──────────────────────────────┐
│     price_alerts (future)     │
├──────────────────────────────┤
│ id                 PK        │
│ commodity_id       FK        │
│ region_id          FK        │
│ threshold_type     VARCHAR   │
│ threshold_value    DECIMAL   │
│ user_email         VARCHAR   │
│ is_active          BOOLEAN   │
└──────────────────────────────┘
```

#### Key SQL Analytics Queries (to be implemented)

| Query | Description |
|---|---|
| Average Weekly Price Variance | `AVG(price_avg) per commodity per week, with % change WoW` |
| Regional Price Comparison | Side-by-side average prices across regions for a commodity |
| 30-Day Rolling Average | Window function `AVG() OVER (ORDER BY date ROWS 30 PRECEDING)` |
| Price Spike Detection | Flag days where price deviates > 2 std deviations from 30-day mean |
| Cheapest Region Finder | For a commodity, rank regions by current prevailing price |
| Seasonal Pattern Analysis | Monthly averages grouped by commodity over multiple years |

---

### MODULE 3: FastAPI Backend (REST API)

**Purpose:** Serve cleaned data, analytics, and forecasts to the frontend.

#### API Endpoint Map

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/commodities` | List all tracked commodities with categories |
| `GET` | `/api/v1/commodities/{id}` | Single commodity details |
| `GET` | `/api/v1/regions` | List all regions |
| `GET` | `/api/v1/prices/daily` | Daily prices with filters (`?commodity_id=&region_id=&from=&to=`) |
| `GET` | `/api/v1/prices/latest` | Latest prices for all commodities (today or most recent) |
| `GET` | `/api/v1/prices/history/{commodity_id}` | 6-month price history for a commodity |
| `GET` | `/api/v1/analytics/weekly-variance` | Average weekly price variance report |
| `GET` | `/api/v1/analytics/regional-comparison` | Compare prices across regions |
| `GET` | `/api/v1/analytics/price-spikes` | Detected abnormal price movements |
| `GET` | `/api/v1/analytics/cheapest-region/{commodity_id}` | Cheapest region for a commodity |
| `GET` | `/api/v1/analytics/rolling-average/{commodity_id}` | 30-day rolling average data |
| `GET` | `/api/v1/analytics/seasonal/{commodity_id}` | Monthly seasonal patterns |
| `GET` | `/api/v1/forecast/{commodity_id}` | 7-day price forecast with confidence intervals |
| `GET` | `/api/v1/forecast/summary` | Forecast summary for all commodities |
| `POST`| `/api/v1/admin/scrape/trigger` | Manually trigger a scrape job (admin) |
| `GET` | `/api/v1/admin/scrape/logs` | View scrape history and status |
| `GET` | `/api/v1/health` | Service health check |

#### Backend File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry, CORS, lifespan
│   ├── config.py                  # Settings via pydantic-settings (.env)
│   ├── database.py                # Async SQLAlchemy engine & session
│   │
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── commodity.py
│   │   ├── region.py
│   │   ├── market.py
│   │   ├── daily_price.py
│   │   ├── price_forecast.py
│   │   └── scrape_log.py
│   │
│   ├── schemas/                   # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── commodity.py
│   │   ├── price.py
│   │   ├── analytics.py
│   │   └── forecast.py
│   │
│   ├── routers/                   # API route handlers
│   │   ├── __init__.py
│   │   ├── commodities.py
│   │   ├── prices.py
│   │   ├── analytics.py
│   │   ├── forecast.py
│   │   └── admin.py
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── price_service.py       # Price queries & aggregation
│   │   ├── analytics_service.py   # Variance, spikes, comparisons
│   │   └── forecast_service.py    # ML model training & prediction
│   │
│   ├── ml/                        # Machine Learning module
│   │   ├── __init__.py
│   │   ├── trainer.py             # Train regression/ARIMA models
│   │   ├── predictor.py           # Generate forecasts from saved models
│   │   └── models/                # Serialized model files (.joblib)
│   │
│   ├── scraping/                  # Data ingestion module
│   │   ├── __init__.py
│   │   ├── scraper_da.py          # DA Price Watch scraper
│   │   ├── scraper_psa.py         # PSA OpenSTAT scraper
│   │   ├── data_cleaner.py        # Standardization & validation
│   │   ├── data_loader.py         # DB insertion with upsert
│   │   └── scheduler.py           # APScheduler job definitions
│   │
│   └── utils/
│       ├── __init__.py
│       ├── constants.py           # Commodity mappings, region codes
│       └── helpers.py             # Date utils, peso formatting
│
├── alembic/                       # Database migrations
│   ├── versions/
│   └── env.py
├── alembic.ini
├── requirements.txt
├── Dockerfile
└── pytest.ini
```

---

### MODULE 4: ML / Forecasting Engine

**Purpose:** Predict commodity prices for the next 7 days using historical data.

| Component | Detail |
|---|---|
| **Model 1 — Linear Regression** | Simple trend-based forecast using Scikit-learn `LinearRegression`. Features: day-of-week, week-of-year, lagged prices (t-1, t-7) |
| **Model 2 — ARIMA** | Statsmodels `ARIMA(p,d,q)` for time-series with seasonality. Auto-tuned via `pmdarima.auto_arima` |
| **Training Frequency** | Weekly (every Sunday midnight PHT) |
| **Training Data** | Last 6 months of daily prices, per commodity-region pair |
| **Output** | 7 daily predictions + 90% confidence interval upper/lower bounds |
| **Model Storage** | Serialized via `joblib`, stored in `backend/app/ml/models/` |
| **Evaluation Metrics** | MAE (Mean Absolute Error), MAPE (Mean Absolute Percentage Error) logged per model |
| **Fallback** | If ARIMA fails to converge, fall back to Linear Regression |

#### Forecasting Pipeline Flow

```
Historical Prices (6mo) 
    → Feature Engineering (lag, rolling avg, day encoding)
    → Train/Test Split (80/20)
    → Model Training (LinearReg + ARIMA)
    → Evaluate (MAE, MAPE)
    → Select Best Model
    → Generate 7-day Forecast
    → Store in price_forecasts table
    → Serve via /api/v1/forecast/{commodity_id}
```

---

### MODULE 5: Next.js Frontend

**Purpose:** Interactive, mobile-responsive dashboard for viewing prices, trends, and forecasts.

#### Pages & Routes

| Route | Page | Description |
|---|---|---|
| `/` | Dashboard Home | Overview: top commodities, price alerts, latest prices ticker |
| `/prices` | Price Explorer | Filterable table of current prices by commodity + region |
| `/trends/{commodityId}` | Price Trends | Interactive 6-month line chart with date range picker |
| `/compare` | Regional Comparison | Side-by-side bar/line charts comparing regions |
| `/forecast` | Price Forecast | 7-day predictions with confidence bands |
| `/forecast/{commodityId}` | Commodity Forecast | Detailed forecast for a single commodity |
| `/analytics` | Analytics Dashboard | Weekly variance, spike alerts, seasonal patterns |
| `/about` | About | Data sources, methodology, disclaimers |

#### Frontend File Structure

```
frontend/
├── src/
│   ├── app/                          # Next.js App Router
│   │   ├── layout.tsx                # Root layout (nav, footer, theme)
│   │   ├── page.tsx                  # Dashboard home
│   │   ├── prices/
│   │   │   └── page.tsx              # Price explorer
│   │   ├── trends/
│   │   │   └── [commodityId]/
│   │   │       └── page.tsx          # Commodity trend charts
│   │   ├── compare/
│   │   │   └── page.tsx              # Regional comparison
│   │   ├── forecast/
│   │   │   ├── page.tsx              # Forecast overview
│   │   │   └── [commodityId]/
│   │   │       └── page.tsx          # Single commodity forecast
│   │   ├── analytics/
│   │   │   └── page.tsx              # Analytics dashboard
│   │   └── about/
│   │       └── page.tsx              # About page
│   │
│   ├── components/
│   │   ├── ui/                       # shadcn/ui primitives (button, card, etc.)
│   │   ├── layout/
│   │   │   ├── Navbar.tsx            # Top navigation with region selector
│   │   │   ├── Sidebar.tsx           # Commodity category sidebar
│   │   │   └── Footer.tsx
│   │   ├── charts/
│   │   │   ├── PriceTrendChart.tsx   # Recharts line chart (6-month trend)
│   │   │   ├── RegionalBarChart.tsx  # Bar chart for region comparison
│   │   │   ├── ForecastChart.tsx     # Line + area chart with confidence bands
│   │   │   ├── VarianceHeatmap.tsx   # Weekly variance heatmap
│   │   │   ├── SparklineCard.tsx     # Mini inline chart for dashboard cards
│   │   │   └── SeasonalChart.tsx     # Monthly seasonal pattern chart
│   │   ├── dashboard/
│   │   │   ├── PriceTicker.tsx       # Scrolling latest prices marquee
│   │   │   ├── CommodityCard.tsx     # Card with commodity name + price + sparkline
│   │   │   ├── PriceSpikeAlert.tsx   # Alert banner for abnormal price changes
│   │   │   └── SummaryStats.tsx      # Key stats: avg price, most expensive, etc.
│   │   ├── prices/
│   │   │   ├── PriceTable.tsx        # Sortable/filterable data table
│   │   │   └── PriceFilters.tsx      # Region, commodity, date range filters
│   │   └── common/
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorBoundary.tsx
│   │       └── EmptyState.tsx
│   │
│   ├── hooks/
│   │   ├── useCommodities.ts         # TanStack Query hook for commodities
│   │   ├── usePrices.ts              # Hook for price data with filters
│   │   ├── useForecast.ts            # Hook for forecast data
│   │   ├── useAnalytics.ts           # Hook for analytics endpoints
│   │   └── useRegions.ts             # Hook for region list
│   │
│   ├── lib/
│   │   ├── api.ts                    # Axios/fetch client with base URL config
│   │   ├── utils.ts                  # Peso formatter, date helpers, CN util
│   │   └── constants.ts              # API URLs, commodity icons mapping
│   │
│   ├── types/
│   │   ├── commodity.ts              # TypeScript interfaces
│   │   ├── price.ts
│   │   ├── forecast.ts
│   │   └── analytics.ts
│   │
│   └── styles/
│       └── globals.css               # Tailwind base + custom Filipino theme colors
│
├── public/
│   ├── commodities/                  # Commodity icons (rice.svg, onion.svg, etc.)
│   └── logo.svg
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── Dockerfile
```

#### UI/UX Design Guidelines

| Aspect | Decision |
|---|---|
| **Color Palette** | Philippine flag-inspired: Blue (`#0038A8`), Red (`#CE1126`), Yellow (`#FCD116`), with neutral grays |
| **Typography** | `Inter` for body, `Plus Jakarta Sans` for headings |
| **Mobile** | Mobile-first responsive design; bottom tab navigation on mobile |
| **Accessibility** | WCAG 2.1 AA compliance; color-blind safe chart palettes |
| **Language** | English with Tagalog commodity names shown parenthetically (e.g., "Onion (Sibuyas)") |
| **Price Format** | Philippine Peso: `₱XX.XX per kg` |

---

### MODULE 6: DevOps & Infrastructure

#### Docker Compose Services

| Service | Image/Build | Port |
|---|---|---|
| `frontend` | Build from `./frontend` | `3000` |
| `backend` | Build from `./backend` | `8000` |
| `postgres` | `postgres:16-alpine` | `5432` |
| `redis` | `redis:7-alpine` (future: task queue) | `6379` |

#### Environment Variables

```
# Backend (.env)
DATABASE_URL=postgresql+asyncpg://agrisenta:password@postgres:5432/agrisenta
SECRET_KEY=<random>
DA_SCRAPE_URL=https://www.da.gov.ph/price-monitoring/
PSA_API_URL=https://openstat.psa.gov.ph/
SCRAPE_SCHEDULE_CRON=0 6 * * *     # Daily 6 AM PHT
FORECAST_SCHEDULE_CRON=0 0 * * 0   # Weekly Sunday midnight
CORS_ORIGINS=http://localhost:3000

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 5. Data Flow (End-to-End)

```
Step 1: SCRAPE
  APScheduler triggers at 6 AM PHT daily
  → scraper_da.py hits DA Price Watch
  → scraper_psa.py hits PSA OpenSTAT
  → Raw HTML/CSV collected

Step 2: CLEAN
  → data_cleaner.py normalizes commodity names
  → Standardizes units to "per kg"
  → Fills missing values (forward-fill or interpolation)
  → Validates price ranges (rejects outliers > 5x median)

Step 3: LOAD
  → data_loader.py performs upsert into daily_prices
  → Logs result to scrape_logs table

Step 4: ANALYZE (on-demand via API)
  → analytics_service.py runs SQL window functions
  → Returns variance, comparisons, spike alerts

Step 5: FORECAST (weekly)
  → forecast_service.py pulls 6-month history
  → Trains LinearReg + ARIMA per commodity-region
  → Stores 7-day predictions in price_forecasts

Step 6: SERVE
  → FastAPI serves data via REST endpoints
  → JSON responses with pagination, filtering

Step 7: DISPLAY
  → Next.js fetches via TanStack Query
  → Recharts renders interactive visualizations
  → User explores trends, compares regions, views forecasts
```

---

## 6. Tracked Commodities (Initial Set — 20 Items)

| Category | Commodities |
|---|---|
| **Rice (Bigas)** | Well-Milled Rice, Regular-Milled Rice, Premium Rice |
| **Vegetables (Gulay)** | Red Onion (Sibuyas), Garlic (Bawang), Tomato (Kamatis), Kangkong, Sitaw, Pechay, Ampalaya, Squash (Kalabasa) |
| **Meat (Karne)** | Pork Kasim, Pork Liempo, Whole Chicken, Chicken Thigh |
| **Fish (Isda)** | Bangus (Milkfish), Tilapia, Galunggong |
| **Others** | Egg (Medium, per piece), Cooking Oil (per liter) |

---

## 7. Regions Tracked

| Code | Region | Island Group |
|---|---|---|
| `NCR` | National Capital Region | Luzon |
| `CAR` | Cordillera Administrative Region | Luzon |
| `R03` | Central Luzon | Luzon |
| `R04A` | CALABARZON | Luzon |
| `R05` | Bicol | Luzon |
| `R06` | Western Visayas | Visayas |
| `R07` | Central Visayas | Visayas |
| `R10` | Northern Mindanao | Mindanao |
| `R11` | Davao | Mindanao |
| `R12` | SOCCSKSARGEN | Mindanao |

---

## 8. Development Phases & Timeline

### Phase 1 — Foundation (Week 1-2)
- [ ] Project scaffolding (Next.js + FastAPI + Docker Compose)
- [ ] Database schema design & Alembic migrations
- [ ] Seed data: regions, commodities, markets
- [ ] Basic CRUD API endpoints (commodities, regions)
- [ ] Frontend layout: Navbar, Sidebar, routing

### Phase 2 — Data Pipeline (Week 3-4)
- [ ] DA Price Watch scraper implementation
- [ ] PSA OpenSTAT scraper implementation
- [ ] Data cleaning pipeline with Pandas
- [ ] Data loader with upsert logic
- [ ] APScheduler integration for daily scraping
- [ ] Scrape logging and monitoring

### Phase 3 — API & Analytics (Week 5-6)
- [ ] Price endpoints with filtering & pagination
- [ ] Analytics endpoints (variance, comparison, spikes)
- [ ] Complex SQL queries with window functions
- [ ] Cheapest region finder
- [ ] Rolling average calculations
- [ ] Seasonal pattern analytics

### Phase 4 — ML Forecasting (Week 7-8)
- [ ] Feature engineering pipeline
- [ ] Linear Regression model training
- [ ] ARIMA model training with auto-tuning
- [ ] Model evaluation & selection
- [ ] Forecast API endpoints
- [ ] Weekly retraining scheduler

### Phase 5 — Frontend Dashboard (Week 9-11)
- [ ] Dashboard home with commodity cards & sparklines
- [ ] Price explorer with filterable data table
- [ ] Price trend line charts (Recharts) with date picker
- [ ] Regional comparison views
- [ ] Forecast charts with confidence bands
- [ ] Analytics visualizations (heatmap, spike alerts)
- [ ] Mobile responsive design

### Phase 6 — Polish & Deploy (Week 12)
- [ ] Error handling & edge cases
- [ ] Loading states & empty states
- [ ] Testing (unit + integration + E2E)
- [ ] Performance optimization
- [ ] Documentation (API docs auto-generated via FastAPI)
- [ ] Production deployment

---

## 9. Key Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Async vs Sync** | Async (asyncpg + httpx) | Non-blocking I/O for scraping & DB; better concurrency |
| **ORM vs Raw SQL** | Hybrid (SQLAlchemy ORM + raw SQL for analytics) | ORM for CRUD; raw SQL for complex window functions |
| **Model serialization** | joblib | Faster than pickle for numpy arrays in sklearn models |
| **API versioning** | URL prefix `/api/v1/` | Clean upgrade path for breaking changes |
| **Auth** | None initially; API key for admin routes | MVP simplicity; add JWT later if user accounts needed |
| **Caching** | TanStack Query (frontend) + HTTP cache headers | Prices change daily; 1-hour cache is reasonable |
| **Error handling** | Structured error responses `{detail, code, timestamp}` | Consistent frontend error parsing |

---

## 10. Risk Mitigation

| Risk | Mitigation |
|---|---|
| DA/PSA website structure changes | Abstract scrapers behind interfaces; alert on scrape failures; add fallback manual CSV upload |
| Missing price data for some regions/days | Forward-fill strategy; show "No data available" in UI; exclude from ML training |
| ML model inaccuracy | Show confidence intervals; display MAE on forecast page; human-readable disclaimers |
| Rate limiting on government sites | Respectful scraping: 2-second delays, daily schedule only, cache responses |
| Data quality issues | Validation layer: reject prices outside reasonable bounds (e.g., ₱0 or ₱10,000/kg for onions) |

---

## 11. Final Project Directory Structure

```
Agri-Senta/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── ml/
│   │   ├── scraping/
│   │   └── utils/
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── types/
│   │   └── styles/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── BLUEPRINT.md                   # ← This document
```

---

*Blueprint v1.0 — Agri-Senta: The Smart Palengke Dashboard*
*Ready for implementation upon approval.*
