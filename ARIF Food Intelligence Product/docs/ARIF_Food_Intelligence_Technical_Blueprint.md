# STEP 10 — FRONTEND TECHNICAL BLUEPRINT

## ARIF Food Intelligence v0.1

**Target:** Next.js / React web application
**Architecture:** Public-first, API-driven, artifact-aware
**Status:** IMPLEMENTATION BLUEPRINT
**Research engine:** ARIF-Net

---

# 1. Frontend Mission

Frontend bertugas menerjemahkan research artifact menjadi pengalaman:

```text
DATA
 ↓
CONTEXT
 ↓
FORECAST
 ↓
EXPLANATION
 ↓
EVIDENCE
```

Bukan:

```text
UI
 ↓
mengolah data penelitian sendiri
 ↓
menciptakan prediction
```

Implementation Plan memang menempatkan Next.js/React sebagai frontend dan menjadikan API sebagai boundary menuju Python inference service serta versioned result/model artifacts. 

---

# 2. Frontend Architecture

Saya sarankan:

```text
product/web/
│
├── app/
├── components/
├── features/
├── lib/
├── hooks/
├── types/
├── config/
├── mocks/
├── styles/
└── public/
```

Tujuannya bukan membuat folder sebanyak mungkin, tetapi memisahkan:

```text
routing
UI
business-facing feature
API
types
mock
configuration
```

---

# 3. Route Architecture

```text
app/
├── page.tsx
│
├── prices/
│   └── page.tsx
│
├── commodities/
│   ├── page.tsx
│   └── [slug]/
│       ├── page.tsx
│       └── forecast/
│           └── page.tsx
│
├── forecast/
│   └── page.tsx
│
├── context/
│   ├── page.tsx
│   ├── climate/
│   │   └── page.tsx
│   ├── news/
│   │   └── page.tsx
│   └── macro-logistics/
│       └── page.tsx
│
├── monitoring/
│   └── page.tsx
│
├── learn/
│   ├── page.tsx
│   ├── food-price/
│   ├── forecasting/
│   └── data/
│
└── research/
    ├── page.tsx
    ├── model/
    ├── methodology/
    ├── data/
    ├── experiments/
    ├── benchmark/
    ├── ablation/
    └── limitations/
```

Route structure ini merupakan konkretisasi dari route/product structure yang telah ditetapkan pada Implementation Plan. 

---

# 4. Route Responsibility

| Route                          | Responsibility                        |
| ------------------------------ | ------------------------------------- |
| `/`                            | Product story + snapshot              |
| `/prices`                      | Historical/current prices             |
| `/commodities`                 | Commodity discovery                   |
| `/commodities/[slug]`          | Commodity Intelligence                |
| `/commodities/[slug]/forecast` | Commodity-specific forecast           |
| `/forecast`                    | Forecast center                       |
| `/context`                     | Context overview                      |
| `/context/climate`             | Climate intelligence                  |
| `/context/news`                | News/sentiment intelligence           |
| `/context/macro-logistics`     | Macro/logistics context               |
| `/monitoring`                  | Secondary extreme movement monitoring |
| `/learn`                       | Educational entry point               |
| `/research`                    | Research overview                     |
| `/research/model`              | Model explanation                     |
| `/research/methodology`        | Method                                |
| `/research/data`               | Data/provenance                       |
| `/research/experiments`        | Experiment overview                   |
| `/research/benchmark`          | Benchmark                             |
| `/research/ablation`           | Ablation                              |
| `/research/limitations`        | Limitations                           |

---

# 5. App Shell

```text
<AppShell>
  <Header />
  <Main>
    {children}
  </Main>
  <Footer />
</AppShell>
```

Global shell:

```text
Header
 ├── Logo
 ├── Harga Pangan
 ├── Forecast
 ├── Konteks
 ├── Edukasi
 └── Research

Main Content

Footer
 ├── Source
 ├── Version
 ├── About
 └── Limitations
```

---

# 6. Component Architecture

Saya sarankan tiga level.

## Foundation

```text
Button
Input
Badge
Icon
Tooltip
Skeleton
Divider
Typography
```

## Shared domain

```text
PriceCard
ForecastCard
DataStatus
VersionBadge
SourceBadge
MetricCard
ChartCard
EmptyState
ErrorState
```

## Page-specific

```text
CommodityOverview
ForecastTrajectory
ClimateOverview
NewsSentimentPanel
BenchmarkMatrix
AblationMatrix
```

---

# 7. Feature-Based Organization

Daripada seluruh code dimasukkan ke `components/`, feature utama dapat dipisahkan:

```text
features/
├── commodities/
├── prices/
├── forecasts/
├── climate/
├── news/
├── macro-logistics/
├── monitoring/
├── research/
└── education/
```

Contoh:

```text
features/forecasts/
├── components/
│   ├── ForecastChart.tsx
│   ├── ForecastSummary.tsx
│   ├── HorizonSelector.tsx
│   └── ForecastMetadata.tsx
├── hooks/
│   └── useForecast.ts
├── api/
│   └── forecastApi.ts
├── types.ts
└── utils.ts
```

---

# 8. Separation of Concerns

Setiap feature menggunakan:

```text
UI
 ↓
Hook / Query
 ↓
API Client
 ↓
API
```

Bukan:

```text
Component
 ↓
fetch()
 ↓
transform research data
 ↓
calculate feature
 ↓
render
```

---

# 9. API Client Layer

Buat satu abstraction:

```text
lib/api/
├── client.ts
├── commodities.ts
├── markets.ts
├── prices.ts
├── forecasts.ts
├── context.ts
├── monitoring.ts
└── research.ts
```

Contoh:

```ts
export async function getForecast(params: ForecastQuery) {
  return apiClient.get<ForecastResponse>(
    "/api/forecasts",
    { params }
  );
}
```

Page tidak perlu mengetahui detail HTTP client.

---

# 10. Type System

TypeScript menjadi kontrak frontend.

```text
types/
├── commodity.ts
├── market.ts
├── price.ts
├── forecast.ts
├── context.ts
├── provenance.ts
├── research.ts
├── experiment.ts
└── api.ts
```

---

# 11. Core Type: Commodity

```ts
export interface Commodity {
  id: string;
  slug: string;
  name: string;
  category: string;
  unit: string;
  status: "active" | "inactive";
}
```

Schema final harus nantinya mengikuti backend/data contract final.

---

# 12. Core Type: Price Observation

```ts
export interface PriceObservation {
  id: string;
  commodityId: string;
  marketId: string;
  observedAt: string;
  price: number;
  unit: string;
  sourceId: string;
  availabilityAt: string;
  status: "valid" | "invalid";
}
```

`availabilityAt` tidak boleh dihapus hanya karena UI tidak menampilkannya.

Itu merupakan bagian penting dari temporal integrity contract.

---

# 13. Core Type: Forecast

```ts
export interface ForecastRun {
  id: string;
  commodityId: string;
  marketId: string;
  forecastOrigin: string;
  horizon: number;
  modelVersion: string;
  datasetVersion: string;
  preprocessingVersion: string;
  experimentProtocolVersion?: string;
  dataCutoff: string;
  status: ForecastStatus;
}
```

---

# 14. Core Type: Forecast Point

```ts
export interface ForecastPoint {
  horizonDay: number;
  targetDate: string;
  predictedChange: number;
  predictedPrice?: number;
}
```

Kemudian:

```ts
export interface ForecastResult {
  run: ForecastRun;
  referencePrice: number;
  points: ForecastPoint[];
  provenance: ForecastProvenance;
  availability: ContextAvailability;
  limitations: string[];
}
```

---

# 15. Data Fetching Strategy

Frontend sebaiknya membedakan:

### Server data

```text
Commodity
Price
Forecast
Research
```

### UI state

```text
selected commodity
selected horizon
selected date range
open drawer
active tab
```

Dengan demikian:

```text
Server data ≠ UI state
```

---

# 16. Query State

Contoh:

```ts
interface ForecastQuery {
  commodity: string;
  market: string;
  origin: string;
  horizon: number;
}
```

Horizon hanya boleh berasal dari supported horizon configuration.

```ts
export const SUPPORTED_HORIZONS = [
  1,
  3,
  7,
  14,
  30,
  90,
  180,
  365,
] as const;
```

Ini mengikuti standard horizon yang ditetapkan dalam research contract. 

---

# 17. No Arbitrary Horizon

Jangan:

```text
?days=13
```

jika model/artifact tidak mendukung horizon tersebut.

Frontend harus membaca:

```text
supportedHorizons
```

dari model/product capability metadata atau configuration yang terversi.

---

# 18. State Architecture

Setiap data feature memiliki:

```text
idle
loading
success
empty
partial
error
```

Untuk research artifacts bisa ada:

```text
draft
candidate
validated
published
deprecated
```

Frontend tidak boleh menganggap semua result otomatis `validated`.

---

# 19. `DataStatus` Component

Komponen reusable:

```tsx
<DataStatus
  status="partial"
  label="Some context is unavailable"
/>
```

Visual language:

```text
AVAILABLE
PARTIAL
MISSING
INSUFFICIENT COVERAGE
TEMPORALLY INVALID
```

Status ini berasal dari data contract yang sudah kita desain dan konsisten dengan requirement bahwa missing modality harus ditangani secara eksplisit. 

---

# 20. `VersionBadge`

```tsx
<VersionBadge
  model="ARIF-Net 0.x"
  dataset="Food Price 0.x"
/>
```

Digunakan pada:

```text
Forecast
Research Result
Benchmark
Ablation
```

---

# 21. `SourceBadge`

```tsx
<SourceBadge
  name="BMKG"
  type="climate"
/>
```

Tidak harus selalu clickable, tetapi provenance harus dapat diakses.

---

# 22. `ForecastTrustCard`

Reusable component:

```tsx
<ForecastTrustCard
  origin="..."
  horizon={7}
  modelVersion="..."
  datasetVersion="..."
  preprocessingVersion="..."
  dataCutoff="..."
/>
```

Ini menjadi salah satu signature component ARIF Food Intelligence.

---

# 23. Chart Architecture

```text
components/charts/
├── PriceHistoryChart.tsx
├── ForecastTrajectoryChart.tsx
├── MovementChart.tsx
├── SentimentTrendChart.tsx
├── ClimateTrendChart.tsx
└── BenchmarkChart.tsx
```

Chart harus menerima data:

```ts
type ChartDataPoint = {
  date: string;
  value: number;
};
```

Bukan mengambil data API sendiri.

---

# 24. Price History Chart

Input:

```ts
interface PriceHistoryChartProps {
  observations: PriceObservation[];
  unit: string;
}
```

Chart responsibility hanya:

```text
render
tooltip
zoom
range
accessibility
```

Bukan menghitung research feature.

---

# 25. Forecast Chart

Input:

```ts
interface ForecastTrajectoryChartProps {
  history: PriceObservation[];
  forecast: ForecastPoint[];
  origin: string;
}
```

Chart harus visually distinguish:

```text
Observed
Forecast
Forecast Origin
```

---

# 26. No Misleading Visualization

Frontend tidak boleh membuat:

```text
actual ─────────────── forecast
```

terlihat seolah semuanya observed.

Gunakan boundary:

```text
Observed ────────│──────── Forecast
                 ↑
              Origin
```

---

# 27. Data Formatting Layer

Jangan format angka secara random di setiap component.

Buat:

```text
lib/format/
├── currency.ts
├── percentage.ts
├── date.ts
├── number.ts
└── units.ts
```

Contoh:

```ts
formatPrice(52400)
formatPercentage(0.032)
formatDate("2026-09-01")
```

---

# 28. Indonesian Locale

Karena product target adalah Indonesia, formatting harus konsisten.

Contoh:

```text
Rp 52.400
+3,2%
1 September 2026
```

Tetapi raw API tetap menggunakan machine-readable numerical representation.

---

# 29. Context Architecture

```text
features/context/
├── climate/
├── news/
├── supply/
└── macro-logistics/
```

Setiap context mempunyai pola:

```text
Overview
 ↓
Availability
 ↓
Metrics
 ↓
Historical Context
 ↓
Source
 ↓
Limitation
```

---

# 30. Forecast Page Composition

```tsx
<ForecastPage>
  <PageHeader />

  <ForecastFilters />

  <ForecastSummary />

  <ForecastTrajectoryChart />

  <ForecastContext />

  <ForecastTrustCard />

  <ForecastLimitations />
</ForecastPage>
```

---

# 31. Commodity Page Composition

```tsx
<CommodityPage>
  <CommodityHeader />

  <CurrentPriceSummary />

  <PriceHistorySection />

  <MovementSection />

  <ForecastSection />

  <ContextSection />

  <ResearchEvidencePreview />
</CommodityPage>
```

Ini mempertahankan golden path yang sebelumnya kita tetapkan.

---

# 32. Research Page Composition

```tsx
<ResearchOverview>
  <ResearchHeader />
  <ResearchProblem />
  <ResearchGoal />
  <ResearchPipeline />
  <ResearchModel />
  <EvidencePreview />
  <Limitations />
</ResearchOverview>
```

---

# 33. Research Result Guard

Ini sangat penting.

Component:

```tsx
<ResearchArtifactGuard artifact={artifact}>
  ...
</ResearchArtifactGuard>
```

Logic:

```text
candidate
    ↓
display with Candidate label

validated
    ↓
display as validated evidence

deprecated
    ↓
display warning

missing
    ↓
not render result
```

Jangan mengubah:

```text
candidate → validated
```

di frontend.

---

# 34. Mock Data Architecture

Karena website akan dibangun paralel dengan model, kita membutuhkan:

```text
mocks/
├── commodities.json
├── prices.json
├── forecasts.json
├── contexts.json
└── research.json
```

Tetapi mock wajib dilabeli:

```text
MOCK
DEMO
SAMPLE
```

dan tidak boleh masuk ke production research evidence.

---

# 35. Mock Adapter

Frontend sebaiknya tidak tahu apakah data berasal dari mock atau API.

```ts
interface ForecastRepository {
  getForecast(
    query: ForecastQuery
  ): Promise<ForecastResult>;
}
```

Implementation:

```text
MockForecastRepository
ApiForecastRepository
```

Sehingga nanti:

```text
Mock
 ↓
Real API
```

tanpa mengubah UI.

---

# 36. Repository Pattern

```text
features/forecasts/
├── repositories/
│   ├── forecastRepository.ts
│   ├── mockForecastRepository.ts
│   └── apiForecastRepository.ts
```

Ini sangat berguna selama model belum selesai.

---

# 37. Environment Configuration

Contoh:

```text
NEXT_PUBLIC_APP_URL
NEXT_PUBLIC_API_BASE_URL
NEXT_PUBLIC_PRODUCT_VERSION
```

Yang **tidak boleh**:

```text
NEXT_PUBLIC_DATABASE_PASSWORD
NEXT_PUBLIC_API_SECRET
NEXT_PUBLIC_GDELT_KEY
```

Secret tetap server-side. Ini sesuai NFR security project. 

---

# 38. Loading Architecture

Setiap route harus dapat memiliki:

```text
loading.tsx
error.tsx
not-found.tsx
```

untuk route yang relevan.

Contoh:

```text
app/commodities/[slug]/
├── page.tsx
├── loading.tsx
├── error.tsx
└── not-found.tsx
```

---

# 39. Error Boundary

Error UX:

```text
We couldn't load this forecast.
Request ID: req_xxx

[Try again]
```

Tidak menampilkan stack trace kepada user.

---

# 40. Empty State

Misalnya belum ada forecast:

```text
No published forecast is available for this commodity and period.

View historical price →
```

Bukan:

```text
Prediction = 0
```

---

# 41. Partial State

Misalnya news tersedia tetapi climate tidak:

```text
Context

✓ News & Sentiment
✓ Macro / Logistics
— Climate unavailable
```

Forecast UI tetap dapat menjelaskan status context.

---

# 42. API Cache Boundary

Frontend tidak perlu tahu detail Redis/other cache.

```text
Frontend
 ↓
API
 ↓
Cache / Artifact Store
```

Jadi `useForecast()` hanya tahu:

```ts
const { data, isLoading, error } = useForecast(query);
```

---

# 43. Hook Architecture

```text
hooks/
├── useCommodities.ts
├── useCommodity.ts
├── usePrices.ts
├── useForecast.ts
├── useClimateContext.ts
├── useNewsContext.ts
├── useMacroContext.ts
└── useResearchArtifact.ts
```

---

# 44. Server vs Client Component Strategy

### Prefer Server Component

Untuk:

```text
page composition
SEO
static research content
commodity metadata
initial data
```

### Client Component

Untuk:

```text
interactive chart
filters
tabs
date selector
horizon selector
drawer
```

Tujuannya menjaga interactive JS tetap terisolasi.

---

# 45. SEO Architecture

Public product harus dapat di-index secara semantic.

Contoh:

```text
/commodities/cabai-merah-keriting
```

metadata:

```text
title
description
og:title
og:description
```

Tetapi SEO description tidak boleh membuat unsupported prediction claim.

---

# 46. Metadata Example

```text
Cabai Merah Keriting — ARIF Food Intelligence
Historical price, forecast movement, and contextual information for PIKJ.
```

Bukan:

```text
The most accurate chili price prediction.
```

---

# 47. Frontend Security Rules

AI Agent tidak boleh:

```text
fetch external source directly from browser
```

untuk source yang membutuhkan credentials.

Pattern:

```text
Browser
 ↓
Backend API
 ↓
External Source
```

---

# 48. Dependency Boundary

Frontend package set sebaiknya minimal:

```text
Next.js
React
TypeScript
Charting library
Validation library
HTTP/query client
UI primitives
```

Library spesifik belum saya kunci karena source project tidak memberikan keputusan tersebut.

---

# 49. Don't Overengineer

Tidak perlu langsung:

```text
micro frontend
event bus
GraphQL federation
WebSocket everything
complex RBAC
multi-tenant architecture
real-time streaming
```

Semua itu tidak dibutuhkan oleh product contract saat ini.

Core-nya:

```text
Public Web
 ↓
API
 ↓
Research Artifact
```

---

# 50. Suggested Frontend Folder

Berikut blueprint lengkap yang dapat langsung menjadi target coding:

```text
product/web/
│
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   │
│   ├── prices/
│   ├── commodities/
│   ├── forecast/
│   ├── context/
│   ├── monitoring/
│   ├── learn/
│   └── research/
│
├── components/
│   ├── ui/
│   ├── layout/
│   ├── data-display/
│   ├── charts/
│   ├── provenance/
│   └── states/
│
├── features/
│   ├── commodities/
│   ├── prices/
│   ├── forecasts/
│   ├── context/
│   ├── monitoring/
│   ├── education/
│   └── research/
│
├── lib/
│   ├── api/
│   ├── format/
│   ├── validation/
│   ├── config/
│   └── utils/
│
├── hooks/
│
├── types/
│
├── mocks/
│
├── config/
│
├── styles/
│
└── public/
```

---

# 51. AI Coding Agent Rules

Mulai Step 10, saya sarankan agent diberi aturan berikut.

### Rule 1

**Do not invent API response fields.**

Jika field belum didefinisikan:

```text
STOP → check contract
```

---

### Rule 2

**Do not invent research numbers.**

Tidak boleh membuat:

```text
MAE
RMSE
accuracy
prediction
SHAP
confidence
```

sebagai empirical result tanpa artifact nyata.

Project source secara eksplisit melarang fabricated results. 

---

### Rule 3

**Do not silently modify research logic.**

Frontend hanya presentation/product layer.

---

### Rule 4

**Treat OPEN decisions as OPEN.**

Jika architecture research belum final:

```text
Candidate Architecture
```

bukan:

```text
Final ARIF-Net Architecture
```

---

### Rule 5

**Preserve metadata.**

Jangan membuang:

```text
model_version
dataset_version
data_cutoff
source
availability
limitations
```

hanya karena UI ingin lebih sederhana.

---

# 52. Definition of Done — Frontend

Frontend implementation dianggap siap ketika:

```text
✓ All routes compile
✓ No fake research values
✓ API types defined
✓ Mock adapter works
✓ Real API adapter can replace mock
✓ Loading states
✓ Empty states
✓ Error states
✓ Partial data states
✓ Responsive desktop/mobile
✓ Forecast metadata visible
✓ Source/provenance visible
✓ Research evidence status visible
✓ Observed vs forecast visually separated
✓ No credentials exposed
✓ Accessibility baseline implemented
```

---

# 53. Build Sequence dari Blueprint Ini

Jangan langsung membuat seluruh halaman sekaligus.

Urutan:

```text
01. App Shell
      ↓
02. Design Tokens
      ↓
03. Foundation Components
      ↓
04. API / Types
      ↓
05. Mock Repository
      ↓
06. Commodity Explorer
      ↓
07. Price Explorer
      ↓
08. Commodity Intelligence
      ↓
09. Forecast Center
      ↓
10. Context
      ↓
11. Research
      ↓
12. Education
      ↓
13. Monitoring
      ↓
14. Real API Integration
      ↓
15. Real Research Artifact
```

---

# 54. Parallel Development Strategy

Mulai sekarang kita bisa menjalankan **dua track**:

```text
TRACK A — RESEARCH
────────────────────────
Phase 1 Data Audit
Temporal
Leakage
Target
Baseline
ARIF-Net
Experiment
        │
        ▼
Validated Artifact
```

dan:

```text
TRACK B — PRODUCT
────────────────────────
Step 10 Frontend Blueprint
        ↓
UI implementation
        ↓
Mock artifact
        ↓
API integration
        ↓
Real artifact
```

Titik integrasinya:

```text
             RESEARCH
                 │
                 ▼
        Versioned Artifact
                 │
                 ▼
             Product API
                 │
                 ▼
              Product
```

Ini selaras dengan roadmap resmi yang memisahkan Data Engineering → Modeling → Validation → Productization → Capstone. 

---

# 55. Arsitektur Akhir Sementara

Sekarang blueprint kita sudah sampai:

```text
                         USER
                           │
                           ▼
              ┌──────────────────────┐
              │   Next.js Frontend   │
              │                      │
              │ Pages                │
              │ Features             │
              │ Components           │
              │ Charts               │
              │ State                │
              └──────────┬───────────┘
                         │
                    API Contract
                         │
                         ▼
              ┌──────────────────────┐
              │    Product API       │
              └──────────┬───────────┘
                         │
                ┌────────┴─────────┐
                │                  │
                ▼                  ▼
        Research Artifact    Python Inference
             Store                 Service
                │                  │
                └────────┬─────────┘
                         ▼
                Versioned Research
                   Ecosystem
```

---

# 56. Posisi Kita Sekarang

Secara dokumentasi, chain-nya telah menjadi:

```text
01 Product Scope
02 Stakeholder & Persona
03 Problem → Need → Feature
04 User Journey
05 Domain Model + IA
06 PRD
07 Technical Architecture
08 Data + API Contract
09 UI/UX + Design System
10 Frontend Technical Blueprint
```