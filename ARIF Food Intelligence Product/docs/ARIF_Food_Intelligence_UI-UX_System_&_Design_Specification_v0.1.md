# STEP 09 — UI/UX SYSTEM & DESIGN SPECIFICATION

## ARIF Food Intelligence v0.1

**Status:** WORKING DESIGN SPECIFICATION
**Design Scope:** Web application
**Primary experience:** Public-first
**Core object:** Commodity Intelligence
**Primary flow:** Price → Dynamics → Forecast → Context → Explanation → Evidence

---

# 1. UX NORTH STAR

Prinsip utama:

> **User should understand the forecast before being asked to understand the model.**

Urutan informasi:

```text
WHAT IS HAPPENING?
        ↓
HOW HAS IT CHANGED?
        ↓
WHAT IS PROJECTED?
        ↓
WHAT CONTEXT EXISTS?
        ↓
HOW DOES THE MODEL WORK?
        ↓
WHAT IS THE EVIDENCE?
```

Jadi halaman tidak boleh dibuka dengan diagram neural network atau tabel metric.

---

# 2. CORE EXPERIENCE MODEL

Setiap halaman utama menggunakan 5 lapisan informasi:

```text
┌──────────────────────────────────────┐
│ 1. SUMMARY                           │
│ Apa yang sedang terjadi?             │
├──────────────────────────────────────┤
│ 2. VISUAL EVIDENCE                   │
│ Trend / chart / movement             │
├──────────────────────────────────────┤
│ 3. CONTEXT                           │
│ Climate / News / Supply / Macro      │
├──────────────────────────────────────┤
│ 4. EXPLANATION                       │
│ Mengapa informasi ini relevan?       │
├──────────────────────────────────────┤
│ 5. SOURCE / LIMITATION               │
│ Dari mana data + apa batasannya?     │
└──────────────────────────────────────┘
```

---

# 3. PROPOSED VISUAL DIRECTION

Sumber tidak menetapkan design style visual secara eksplisit, jadi bagian ini merupakan **PROPOSED DESIGN DIRECTION**, bukan keputusan penelitian.

Arah visual yang cocok:

> **Editorial Data Intelligence + Modern Analytical Dashboard**

Karakter:

```text
Clean
Data-centric
Scientific
Calm
Trustworthy
Modern
Readable
```

Bukan:

```text
Crypto dashboard
Trading terminal
Futuristic neon AI
Dense enterprise admin
```

Alasannya: produk adalah food-price intelligence dan academic demonstration, bukan trading terminal. Proposal juga menempatkan ARIF Food Intelligence sebagai media eksplorasi histori, prediksi, konteks multimodal, serta informasi model. 

---

# 4. DESIGN LANGUAGE

## 4.1 Visual Personality

### Primary

```text
Analytical
Precise
Informative
Transparent
Human-readable
```

### Secondary

```text
Editorial
Educational
Contemporary
Lightweight
```

---

# 5. COLOR SYSTEM

Ini **proposal design token**, bukan berasal dari research contract.

Saya sarankan jangan menggunakan terlalu banyak warna.

### Base

```text
Background
Surface
Elevated Surface
Border
Primary Text
Secondary Text
Muted Text
```

### Semantic

```text
Positive / Up
Negative / Down
Warning
Info
Unavailable
```

### Modality identifiers

Boleh memiliki identifier visual kecil:

```text
Price
Climate
News
Supply
Macro
Logistics
```

Tetapi jangan membuat setiap modality memiliki warna dominan yang memenuhi seluruh interface.

Tujuannya supaya:

```text
DATA
```

tetap lebih kuat daripada dekorasi.

---

# 6. TYPOGRAPHY

Proposed hierarchy:

```text
Display
48–64px

Page Heading
36–48px

Section Heading
24–32px

Card Heading
18–20px

Body
14–16px

Metadata
12–13px
```

Data numeric dapat menggunakan font treatment yang berbeda dari body text agar:

```text
Rp 52.400
+3.8%
7 DAYS
```

mudah dipindai.

---

# 7. SPACING SYSTEM

Gunakan spacing scale konsisten:

```text
4
8
12
16
24
32
48
64
96
```

Jangan membuat margin custom per halaman tanpa alasan.

---

# 8. LAYOUT GRID

### Desktop

```text
12-column grid
Max width: ~1280–1440px
```

### Tablet

```text
8-column grid
```

### Mobile

```text
4-column grid
```

Recommended page structure:

```text
┌────────────────────────────────────────────┐
│ NAVBAR                                     │
├────────────────────────────────────────────┤
│ PAGE HEADER                                │
├────────────────────────────────────────────┤
│ PRIMARY CONTENT                            │
│                                            │
│  ┌─────────────┐ ┌──────────────────────┐ │
│  │ Summary     │ │ Main Visualization   │ │
│  └─────────────┘ └──────────────────────┘ │
│                                            │
│  ┌────────────────────────────────────────┐ │
│  │ Context                                │ │
│  └────────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

---

# 9. GLOBAL APP SHELL

```text
┌────────────────────────────────────────────┐
│ ARIF     Harga Pangan  Forecast  Konteks   │
│         Edukasi  Research                  │
├────────────────────────────────────────────┤
│                                            │
│                PAGE CONTENT                │
│                                            │
├────────────────────────────────────────────┤
│ Source • Model Version • Dataset • About   │
└────────────────────────────────────────────┘
```

Navbar harus sederhana.

Public navigation:

```text
Harga Pangan
Forecast
Konteks
Edukasi
Research
```

Route teknis seperti methodology, benchmark, ablation, climate detail, dan news detail tidak perlu semuanya berada di top-level navigation.

---

# 10. HOME PAGE

## Objective

Menjawab:

> "Apa sebenarnya ARIF Food Intelligence?"

Bukan langsung membanjiri user dengan seluruh data.

### Structure

```text
HERO
│
├── Value proposition
├── Short explanation
└── Explore button

FEATURED COMMODITIES
│
├── Cabai Merah Keriting
├── Bawang Merah
└── Beras

CURRENT SNAPSHOT
│
├── Current price
├── Movement
└── Latest forecast availability

HOW IT WORKS
│
Data
 ↓
Context
 ↓
Forecast
 ↓
Evidence

RESEARCH PREVIEW

LIMITATIONS / TRANSPARENCY

FOOTER
```

---

# 11. HOME HERO

Proposed copy:

### Heading

> **Understand food prices through data, context, and forecasting.**

### Supporting text

> Explore historical price dynamics, multimodal context, and forecast information for selected food commodities in Jakarta.

Karena hasil penelitian belum boleh ditampilkan seolah-olah selalu final, wording harus menghindari klaim seperti:

> "Prediksi harga paling akurat."

---

# 12. COMMODITY DISCOVERY

Card:

```text
┌─────────────────────────────┐
│ CABAI MERAH KERITING        │
│                             │
│ Rp XX.XXX                   │
│ ↑ X.X%                      │
│                             │
│ PIKJ                        │
│                             │
│ View Intelligence →        │
└─────────────────────────────┘
```

Informasi yang paling penting:

```text
Commodity
Current price
Movement
Market
Data date
```

---

# 13. `/prices`

Fungsi:

> Eksplorasi harga, bukan forecast.

Layout:

```text
HEADER
Harga Pangan

FILTER BAR
Commodity | Market | Period

CURRENT PRICE CARDS

PRICE TABLE / CHART

PRICE HISTORY

MOVEMENT SUMMARY
```

---

# 14. Price Chart

Chart utama:

```text
Price
│
│                 ╭───╮
│      ╭──────────╯   │
│──────╯              ╰──
│
└──────────────────────── Time
```

### Interaction

Hover/tap:

```text
Date
Price
Change
Market
Source
```

Jangan hanya menampilkan garis tanpa reference metadata.

---

# 15. `/commodities/[slug]`

Ini **core UX page**.

### Header

```text
Cabai Merah Keriting
Pasar Induk Kramat Jati

Last updated:
YYYY-MM-DD
```

### Summary cards

```text
Current Price
Movement
Volatility
Forecast Availability
```

### Main content

```text
Historical Price
        ↓
Recent Movement
        ↓
Forecast
        ↓
Context
        ↓
Evidence
```

---

# 16. Commodity Intelligence Header

Proposed:

```text
Cabai Merah Keriting
PIKJ · Jakarta

Rp 52.400 / unit
+3.2% from previous observation

[7D Forecast]
[Explore Context]
```

Tetap tampilkan **tanggal data**.

Jangan membuat angka current price terlihat real-time jika sebenarnya dataset memiliki cutoff tertentu.

---

# 17. MOVEMENT CARD

```text
RECENT MOVEMENT

+3.2%

Moderate upward movement

Based on historical price observations
```

Kata "moderate" harus berasal dari rule/threshold yang memang didefinisikan, bukan interpretasi visual bebas.

Jika belum ada threshold product yang tervalidasi, gunakan:

```text
+3.2%
from previous observation
```

saja.

---

# 18. FORECAST PAGE

Route:

```text
/forecast
```

Tujuan:

> Menjadi pusat eksplorasi forecast.

Structure:

```text
FORECAST CENTER

Commodity
Market
Forecast Origin

HORIZON SELECTOR

CURRENT PRICE

FORECAST TRAJECTORY

FORECAST SUMMARY

CONTEXT

MODEL / DATA VERSION

LIMITATIONS
```

---

# 19. Horizon Selector

```text
1D   3D   7D   14D
30D  90D  180D 365D
```

Horizon berasal dari research contract. 

Pada mobile:

```text
[ Horizon ▾ ]
```

atau horizontal scroll.

---

# 20. Forecast Visualization

Chart:

```text
Price
│
│       Actual
│      ───────╮
│             ╲
│              ╲ Forecast
│               ╲──────
│
└──────────────────────── Time
        ↑
   Forecast Origin
```

Harus ada garis atau marker yang jelas membedakan:

```text
Observed
vs
Forecast
```

Jangan menyatukan keduanya tanpa visual distinction.

---

# 21. FORECAST SUMMARY

Misalnya:

```text
7-Day Forecast

Reference Price
Rp 52.400

Predicted Movement
+2.8%

Reconstructed Price
Rp 53.867

Forecast Origin
YYYY-MM-DD
```

Label:

> **Reconstructed Price**

lebih aman daripada menyebutnya seolah-olah model secara langsung menghasilkan nominal price apabila target internal memang relative movement.

Proposal menetapkan relative price movement sebagai target internal dengan harga nominal direkonstruksi untuk aplikasi. 

---

# 22. FORECAST CONTEXT PANEL

Di bawah forecast:

```text
What context was available?

┌────────────┬────────────┬────────────┐
│ Climate    │ News       │ Macro      │
│ Available  │ Available  │ Partial    │
└────────────┴────────────┴────────────┘
```

Klik salah satu → detail context.

---

# 23. CONTEXT EXPLORER

Route:

```text
/context
```

Subsections:

```text
Climate
News & Sentiment
Supply
Macro / Logistics
```

Layout:

```text
CONTEXT OVERVIEW

Climate        Available
News           Available
Supply         Partial
Macro          Available

────────────────────────

Selected Context
```

---

# 24. CLIMATE PAGE

```text
/context/climate
```

Struktur:

```text
CLIMATE CONTEXT

Forecast Commodity
Supplier Regions

Regional Overview
│
├── Rainfall
├── Temperature
├── Anomaly
└── Coverage

MAP / REGION VIEW

Historical Climate Context
```

Supplier-region context bukan market.

---

# 25. NEWS PAGE

```text
/context/news
```

Structure:

```text
NEWS & SENTIMENT

Articles
Sentiment Distribution
Intensity
Persistence
Recency

Recent Topics

Selected News
```

Proposed visual:

```text
Positive   ███████
Neutral    █████
Negative   ███████████

Volume
█████████████
```

Tidak perlu menjadikan sentiment sebagai "score kebenaran".

---

# 26. MACRO / LOGISTICS PAGE

```text
/context/macro-logistics
```

Structure:

```text
FUEL PRICE
────────────
Current effective state

EVENT TIMELINE
────────────
Event
Effective date

LOGISTICS CONTEXT
────────────
Distance
Proxy indicators
```

Label proxy wajib jelas.

---

# 27. RESEARCH EXPERIENCE

Research tidak boleh terasa seperti admin panel.

Route:

```text
/research
```

Landing research:

```text
Research
──────────────

Problem
Methodology
Data
Model
Experiments
Benchmark
Ablation
Limitations
```

---

# 28. RESEARCH PAGE VISUAL HIERARCHY

```text
┌──────────────────────────────────┐
│ Research Overview                │
├──────────────────────────────────┤
│ Research Question                │
├──────────────────────────────────┤
│ Data Architecture                │
├──────────────────────────────────┤
│ Model Architecture               │
├──────────────────────────────────┤
│ Evaluation Protocol              │
├──────────────────────────────────┤
│ Results                          │
├──────────────────────────────────┤
│ Limitations                      │
└──────────────────────────────────┘
```

Pengunjung tidak perlu membaca thesis untuk memahami cerita penelitian. Source memang menetapkan bahwa exhibition story harus dapat dijelaskan melalui food price → external context → ARIF-Net → forecast → supporting context → evidence → limitations. 

---

# 29. MODEL EXPLANATION

Route:

```text
/research/model
```

Visual:

```text
Historical Price
       │
       ▼
 Price Representation
       │
       ├──────── Climate
       ├──────── News
       ├──────── Supply
       ├──────── Macro
       └──────── Logistics
                   │
                   ▼
              Fusion
                   │
                   ▼
            Forecast Horizon
                   │
                   ▼
             Regression
```

Namun nama blok seperti:

```text
Reliability-Aware Fusion
Horizon-Conditioned Fusion
```

baru boleh dipresentasikan sebagai **implemented architecture** setelah architecture candidate benar-benar diputuskan dan diimplementasikan.

Proposal menempatkan keduanya sebagai candidate contribution yang perlu divalidasi melalui benchmark dan ablation. 

---

# 30. BENCHMARK UI

Jangan membuat tabel terlalu padat.

Lebih baik:

```text
Model Comparison

Metric: MAE
Horizon: 7D

┌─────────────┬────────────┐
│ Model       │ MAE        │
├─────────────┼────────────┤
│ Naive       │ ...        │
│ Price-only  │ ...        │
│ Multivariate│ ...        │
│ ARIF-Net    │ ...        │
└─────────────┴────────────┘
```

Tambahkan:

```text
Dataset
Test period
Protocol
Version
```

---

# 31. ABLATION UI

Ablation sebaiknya berbentuk comparison.

```text
Full Model
    │
    ├── Remove Climate
    ├── Remove News
    ├── Remove Macro
    ├── Remove Price Backbone
    └── Remove Fusion Component
```

Kemudian:

```text
Metric Change
```

Jangan memberi label:

> "Component X terbukti paling penting"

kecuali hasil memang mendukung dan wording sesuai protocol.

---

# 32. EXPLANATION UX

Produk sebaiknya memakai tiga tingkat.

### Level 1 — User

> Forecast bergerak naik sebesar X%.

### Level 2 — Intelligence

> Forecast menggunakan historical price dynamics dan contextual modalities yang tersedia.

### Level 3 — Research

> Detail feature, model, fusion, attribution, benchmark, dan ablation.

Dengan ini pengguna umum tidak dipaksa membaca tensor/architecture diagram.

---

# 33. DATA PROVENANCE COMPONENT

Setiap data-driven card penting dapat memiliki:

```text
Source
Date
Coverage
Version
```

Contoh:

```text
Climate Context
────────────────
Source: BMKG
Observation: YYYY-MM-DD
Coverage: 91%
Dataset: v0.4.0
```

---

# 34. FORECAST TRUST CARD

Saya mengusulkan komponen reusable:

```text
┌─────────────────────────────────┐
│ Forecast Metadata               │
├─────────────────────────────────┤
│ Origin       YYYY-MM-DD         │
│ Horizon      7 days             │
│ Model        ARIF-Net v0.x      │
│ Dataset      v0.x               │
│ Cutoff       YYYY-MM-DD HH:mm   │
│ Context      4 / 5 available    │
└─────────────────────────────────┘
```

Komponen ini akan muncul pada:

```text
Commodity Page
Forecast Page
Forecast Detail
Research Demo
```

---

# 35. STATE SYSTEM

UI wajib mendesain minimal enam state.

### Loading

```text
Loading price data...
```

### Empty

```text
No forecast is available for this origin.
```

### Missing

```text
Climate data unavailable.
```

### Partial

```text
Some contextual data is unavailable.
```

### Error

```text
Forecast could not be retrieved.
```

### Stale

```text
Showing the latest published forecast artifact.
```

Ini langsung berkaitan dengan requirement reliability bahwa missing modality harus ditangani eksplisit. 

---

# 36. MOBILE UX

Mobile bukan desktop yang diperkecil.

### Mobile priority

```text
1. Commodity
2. Current price
3. Movement
4. Forecast
5. Context
6. Metadata
7. Research
```

Chart:

```text
horizontal scroll
```

atau:

```text
compact interaction
```

Filter menggunakan:

```text
bottom sheet
```

bukan sidebar permanen.

---

# 37. MOBILE COMMODITY PAGE

Urutan:

```text
Commodity
↓
Price
↓
Movement
↓
Forecast
↓
Context tabs
↓
Evidence
```

Tidak:

```text
10 cards
↓
large empty whitespace
↓
chart
```

---

# 38. COMPONENT SYSTEM

Core component hierarchy:

```text
FOUNDATION
├── Button
├── Badge
├── Icon
├── Typography
├── Divider
└── Tooltip

DATA
├── PriceCard
├── ForecastCard
├── MetricCard
├── DataStatus
├── SourceBadge
└── VersionBadge

CHART
├── PriceChart
├── ForecastChart
├── MovementChart
├── SentimentChart
└── ContextChart

LAYOUT
├── PageHeader
├── Section
├── Grid
├── Card
├── Tabs
├── FilterBar
└── Drawer

RESEARCH
├── MethodologyBlock
├── ArchitectureDiagram
├── BenchmarkTable
├── AblationTable
├── EvidenceCard
└── LimitationBlock
```

---

# 39. COMPONENT COMPOSITION

Contoh Commodity Page:

```text
CommodityPage
│
├── PageHeader
├── CommoditySummary
│   ├── PriceCard
│   ├── MovementCard
│   └── DataStatus
│
├── PriceHistorySection
│   └── PriceChart
│
├── ForecastSection
│   ├── HorizonSelector
│   ├── ForecastChart
│   └── ForecastTrustCard
│
├── ContextSection
│   ├── ClimateCard
│   ├── NewsCard
│   └── MacroCard
│
└── EvidenceSection
    ├── ModelInfo
    ├── VersionInfo
    └── LimitationBlock
```

---

# 40. DATA VISUALIZATION RULES

Karena product ini sangat bergantung pada chart, ada beberapa aturan:

### Rule A

Observed ≠ Forecast.

### Rule B

Actual price ≠ predicted movement.

### Rule C

Missing ≠ zero.

### Rule D

Proxy ≠ actual measurement.

### Rule E

Predictive contribution ≠ causal effect.

### Rule F

Candidate architecture ≠ validated architecture.

Aturan ini sangat penting agar visual tidak menciptakan interpretasi yang lebih kuat daripada evidence penelitian.

---

# 41. UX WRITING SYSTEM

Gunakan bahasa:

```text
Current price
Forecast
Predicted movement
Historical movement
Available context
Data source
Model version
Dataset version
```

Hindari:

```text
Guaranteed price
Expected market crash
Cause of price increase
Best model
Certain prediction
```

---

# 42. MICROCOPY EXAMPLE

### Forecast

> **Predicted movement**

bukan:

> **Price will increase**

### Context

> **Available climate context**

bukan:

> **Climate caused this price change**

### Research

> **Observed predictive contribution**

bukan:

> **Proven cause**

---

# 43. ACCESSIBILITY

Minimum:

```text
WCAG-conscious contrast
Keyboard navigation
Visible focus
Semantic HTML
Accessible chart fallback
Text alternative for critical data
No color-only meaning
```

Contoh:

Jangan:

```text
green = naik
red = turun
```

saja.

Gunakan:

```text
↑ +3.2%
↓ -2.1%
```

sehingga informasi tetap terbaca tanpa warna.

---

# 44. CHART ACCESSIBILITY

Setiap chart harus memiliki:

```text
Title
Unit
Time range
Source
Summary
```

Contoh:

> Price history, Cabai Merah Keriting, PIKJ, last 90 days.

---

# 45. DESIGN TOKEN STRUCTURE

Untuk implementasi frontend:

```text
tokens/
├── color
├── typography
├── spacing
├── radius
├── shadow
├── breakpoint
├── z-index
└── motion
```

Komponen tidak boleh memiliki nilai magic:

```css
margin: 17px;
border-radius: 13px;
```

tanpa token/design reason.

---

# 46. MOTION

Motion sebaiknya subtle.

Gunakan untuk:

```text
page transition
chart reveal
filter update
expand/collapse
loading
```

Jangan menggunakan animation berlebihan pada numerical dashboard.

Forecast harus terasa:

```text
stable
calm
analytical
```

---

# 47. INFORMATION DENSITY

Prinsip:

```text
Public pages
= low / medium density

Intelligence pages
= medium density

Research pages
= medium / high density
```

Jangan menggunakan density research dashboard pada homepage.

---

# 48. RESPONSIVE INFORMATION PRIORITY

| Component           | Desktop |      Mobile |
| ------------------- | ------: | ----------: |
| Current Price       |       ✓ |           ✓ |
| Movement            |       ✓ |           ✓ |
| Forecast            |       ✓ |           ✓ |
| Climate             |       ✓ |           ✓ |
| News                |       ✓ |           ✓ |
| Macro               |       ✓ |           ✓ |
| Benchmark           |       ✓ |   secondary |
| Detailed Experiment |       ✓ |   secondary |
| Full methodology    |       ✓ | collapsible |

---

# 49. MVP SCREEN MAP

Untuk implementasi awal, tidak perlu membuat seluruh route sekaligus.

### Tier 1 — Core Product

```text
/
 /prices
 /commodities
 /commodities/[slug]
 /forecast
```

### Tier 2 — Intelligence

```text
/context
/context/climate
/context/news
/context/macro-logistics
/monitoring
```

### Tier 3 — Research

```text
/research
/research/model
/research/methodology
/research/data
/research/experiments
/research/benchmark
/research/ablation
/research/limitations
```

### Tier 4 — Education

```text
/learn
/learn/food-price
/learn/forecasting
/learn/data
```

---

# 50. MVP USER FLOW

```text
              HOME
                │
                ▼
        CHOOSE COMMODITY
                │
                ▼
       COMMODITY INTELLIGENCE
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
      PRICE   FORECAST  CONTEXT
       │        │        │
       └────────┼────────┘
                ▼
           EXPLANATION
                │
                ▼
             EVIDENCE
```

Ini tetap mengikuti expected exhibition story dalam project baseline. 

---

# 51. UI/UX ACCEPTANCE CRITERIA

Step 09 dianggap selesai ketika:

| ID    | Requirement                                                      |
| ----- | ---------------------------------------------------------------- |
| UX-01 | Public user memahami fungsi produk dari homepage                 |
| UX-02 | Commodity menjadi central navigation object                      |
| UX-03 | Current price terlihat sebelum forecast                          |
| UX-04 | Historical price terlihat sebelum interpretasi forecast          |
| UX-05 | Observed vs forecast dibedakan secara visual                     |
| UX-06 | Horizon dapat dipilih                                            |
| UX-07 | Forecast metadata terlihat                                       |
| UX-08 | Data availability terlihat                                       |
| UX-09 | Climate/news/macro memiliki context view                         |
| UX-10 | Research evidence dapat ditelusuri                               |
| UX-11 | Limitations selalu dapat ditemukan                               |
| UX-12 | Missing data tidak direpresentasikan sebagai zero                |
| UX-13 | Causal interpretation tidak muncul dari UI wording               |
| UX-14 | Interface responsive                                             |
| UX-15 | Critical information dapat digunakan tanpa bergantung pada warna |

---

# 52. Final UX Architecture

Jadi seluruh produk sekarang memiliki struktur:

```text
                         ARIF FOOD INTELLIGENCE
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
           DISCOVER            INTELLIGENCE        RESEARCH
              │                   │                   │
        Commodities             Price               Model
        Prices                  History             Method
                                Forecast            Data
                                Context             Benchmark
                                Monitoring          Ablation
                                                    Limitations
```

Dengan **Commodity Intelligence Page** sebagai titik temu ketiganya.

---

# 53. Hubungan Semua Step Sampai Sekarang

Kita sekarang sudah menghasilkan:

```text
STEP 01
Product Scope
        ↓
STEP 02
Stakeholder & Persona
        ↓
STEP 03
Problem → Need → Feature
        ↓
STEP 04
User Journey
        ↓
STEP 05
Domain Model + IA
        ↓
STEP 06
PRD
        ↓
STEP 07
Technical Architecture
        ↓
STEP 08
Data + API Contract
        ↓
STEP 09
UI/UX + Design System
```

Yang penting, kesembilan langkah ini sekarang membentuk **satu sistem**, bukan dokumen-dokumen terpisah.

---

# 54. Kondisi Project Setelah Step 09

Kita sudah tahu:

```text
WHAT
→ ARIF Food Intelligence

FOR WHOM
→ Public / Consumer / Farmer / Student / Academic

WHY
→ Food price intelligence

WHAT DATA
→ Price + Climate/Supply + News/Sentiment + Macro/Logistics

WHAT MODEL
→ ARIF-Net candidate research model

HOW
→ API + Python inference + versioned artifacts

HOW USER INTERACTS
→ Commodity → Price → Forecast → Context → Evidence

HOW IT IS PRESENTED
→ Editorial analytical dashboard

WHAT IS NOT ALLOWED
→ unsupported causal claims, fake evidence, unversioned forecast
```

Research source juga menegaskan bahwa final product harus memperlihatkan historical price, forecast trajectory, multimodal context, architecture/methodology, benchmark/ablation, model/data version, dan limitations. 