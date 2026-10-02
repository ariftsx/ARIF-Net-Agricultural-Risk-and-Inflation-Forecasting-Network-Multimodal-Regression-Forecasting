# STEP 06 — PRODUCT REQUIREMENTS DOCUMENT

## ARIF Food Intelligence — PRD v0.1

**Status:** WORKING DRAFT
**Product:** ARIF Food Intelligence
**Research Model:** ARIF-Net
**Primary Domain:** Food Price Forecasting & Intelligence
**Primary Task:** Multimodal Regression Forecasting
**Target Market:** Jakarta
**Research/Product Relationship:** ARIF-Net = research/model layer; ARIF Food Intelligence = product/application layer.

> Catatan validasi sumber: file `ARIF-Net_Phase_0_Research_Contract_v2.0.0.md` secara internal memuat deklarasi akhir yang menyebut versi Research Contract v1.2.0. Ini merupakan inkonsistensi metadata versi pada dokumen sumber. Untuk isi metodologi, PRD ini mengikuti isi canonical Phase 0 yang ditandai frozen/ready for Phase 1, bukan mengubah keputusan penelitian berdasarkan perbedaan nomor versi tersebut.

---

# 1. Product Overview

## 1.1 Product Definition

**ARIF Food Intelligence** adalah platform web untuk membantu pengguna memahami kondisi harga pangan melalui kombinasi:

```text
Historical Price
       +
Climate / Supply
       +
News / Sentiment
       +
Macro / Logistics
       ↓
Multimodal Forecasting
       ↓
Forecast Movement
       ↓
Context
       ↓
Explanation
       ↓
Research Evidence
```

Produk tidak dirancang sebagai halaman yang hanya menerima input lalu menampilkan satu angka prediksi.

Research source sendiri menetapkan arah pengalaman:

> Data → Context → Forecast → Explanation → Evidence

serta journey dari current price, historical trend, forecast, climate, news/sentiment, macro/logistics sampai methodology dan experimental evidence.

---

# 2. Product Vision

### Vision

> **Membangun platform food-price intelligence yang menghubungkan kondisi harga, dinamika historis, konteks multimodal, forecasting, dan bukti penelitian dalam satu pengalaman eksplorasi yang transparan.**

### Product positioning

ARIF Food Intelligence bukan sekadar:

> **Price Prediction Website**

tetapi:

> **Food Price Intelligence Platform**

Karena forecast merupakan salah satu capability dalam sistem, bukan satu-satunya objek produk.

---

# 3. Product Goals

PRD ini menetapkan enam tujuan utama.

| ID   | Goal                     | Penjelasan                                                                      |
| ---- | ------------------------ | ------------------------------------------------------------------------------- |
| G-01 | Price Understanding      | Pengguna dapat memahami harga saat ini dan histori                              |
| G-02 | Price Dynamics           | Pengguna dapat melihat perubahan, tren, dan volatility                          |
| G-03 | Forecast Intelligence    | Pengguna dapat melihat forecast multi-horizon                                   |
| G-04 | Contextual Understanding | Pengguna dapat melihat konteks climate, supply, news/sentiment, macro/logistics |
| G-05 | Research Transparency    | Pengguna dapat memahami bagaimana model dibangun dan dievaluasi                 |
| G-06 | Educational Value        | Pengunjung non-teknis tetap dapat memahami hubungan data → model → forecast     |

Tujuan tersebut konsisten dengan baseline product yang sudah ada di Implementation Plan.

---

# 4. Non-Goals

Produk **tidak** ditujukan untuk:

| Non-goal                                                               | Status |
| ---------------------------------------------------------------------- | ------ |
| Rekomendasi jual/beli komoditas                                        | OUT    |
| Trading/investment advisor                                             | OUT    |
| Menentukan kapan petani harus menjual                                  | OUT    |
| Farm profit optimizer                                                  | OUT    |
| Menentukan keputusan kebijakan pemerintah                              | OUT    |
| Causal policy simulator                                                | OUT    |
| Menjamin harga masa depan                                              | OUT    |
| Mengklaim hubungan kausal antara climate/news dan harga                | OUT    |
| Mengklaim ARIF-Net sebagai model terbaik sebelum benchmark tervalidasi | OUT    |
| Mengklaim generalisasi nasional sebelum diuji                          | OUT    |

Ini penting karena Research Contract secara eksplisit mewajibkan pembedaan antara observed fact, proposed mechanism, hypothesis, inference, dan final experimental result.

---

# 5. Target Users

## 5.1 Public User

Kebutuhan utama:

> "Berapa harga komoditas sekarang dan bagaimana pergerakannya?"

Membutuhkan:

- current price,
- historical trend,
- movement,
- forecast sederhana,
- konteks dasar.

---

## 5.2 Consumer

Kebutuhan utama:

> "Bagaimana perubahan harga pangan yang saya lihat sekarang?"

Membutuhkan:

- current price,
- perubahan harga,
- historical pattern,
- forecast,
- context.

---

## 5.3 Farmer / Producer

Kebutuhan utama:

> "Bagaimana kondisi pasar Jakarta terhadap komoditas saya?"

Membutuhkan:

- market reference,
- historical movement,
- forecast,
- supplier-region context,
- climate/supply context.

Produk tidak boleh mengubah market reference tersebut menjadi klaim tentang **farm-gate price** atau optimal selling strategy.

---

## 5.4 Student / Learner

Kebutuhan utama:

> "Bagaimana data multimodal digunakan untuk forecasting?"

Membutuhkan:

- data,
- pipeline,
- model,
- visualization,
- experiment,
- explanation,
- educational material.

---

## 5.5 Academic / Evaluator

Kebutuhan utama:

> "Apa metode yang digunakan dan apakah hasilnya dapat dipertanggungjawabkan?"

Membutuhkan:

- research problem,
- methodology,
- dataset,
- temporal protocol,
- model architecture,
- benchmark,
- ablation,
- metrics,
- limitations,
- versioning.

---

# 6. Product Experience Principle

Seluruh experience menggunakan progressive disclosure:

```text
Level 1
Current Price

      ↓

Level 2
Trend + Movement

      ↓

Level 3
Forecast

      ↓

Level 4
Context

      ↓

Level 5
Explanation

      ↓

Level 6
Research Evidence
```

Pengguna umum tidak dipaksa memahami arsitektur model terlebih dahulu.

Sebaliknya, evaluator dapat masuk ke lapisan teknis kapan pun dibutuhkan.

---

# 7. Core Product Capabilities

Produk mempunyai enam capability utama.

```text
┌──────────────────────┐
│ PRICE INTELLIGENCE   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ FORECAST INTELLIGENCE│
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ CONTEXT INTELLIGENCE │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ MOVEMENT MONITORING  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ LEARNING             │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ RESEARCH EVIDENCE    │
└──────────────────────┘
```

---

# 8. Functional Requirements

## 8.1 Price Intelligence

| ID       | Requirement                                      | Priority |
| -------- | ------------------------------------------------ | -------: |
| PRICE-01 | User dapat melihat current commodity price       |     MUST |
| PRICE-02 | User dapat melihat historical price              |     MUST |
| PRICE-03 | User dapat memilih periode                       |     MUST |
| PRICE-04 | User dapat melihat price movement                |     MUST |
| PRICE-05 | User dapat melihat volatility context            |   SHOULD |
| PRICE-06 | User dapat melihat market yang digunakan         |     MUST |
| PRICE-07 | User dapat melihat tanggal/reference observation |     MUST |

Implementation Plan memang menetapkan current/historical price, period selection, movement, historical trend dan volatility sebagai baseline product capability.

---

# 9. Commodity Intelligence Page

Ini merupakan **halaman paling penting dalam product architecture**.

Contoh:

```text
/commodities/cabai-merah-keriting
```

Struktur:

```text
┌─────────────────────────────────────────┐
│ Commodity Header                        │
│ Cabai Merah Keriting                    │
│ Market: PIKJ                            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ CURRENT PRICE                           │
│ Rp XX.XXX / unit                        │
│ ↑/↓ XX.X%                               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ PRICE HISTORY                           │
│                                         │
│        ─────╮                           │
│    ─────    ╰─────                      │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ RECENT MOVEMENT                         │
│ trend / volatility / movement context   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ FORECAST                                │
│ 1D │ 7D │ 30D │ 90D ...                 │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ MARKET CONTEXT                          │
│ Climate │ News │ Supply │ Macro         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ RESEARCH / EXPLANATION                  │
└─────────────────────────────────────────┘
```

Halaman commodity menjadi resource utama sementara domain model seperti `Commodity`, `Market`, `Price Observation`, dan `Forecast Run` tetap dipisahkan secara konseptual.

---

# 10. Forecast Intelligence

## 10.1 Forecast Goal

Forecast bukan sekadar:

```text
Tomorrow = Rp 50.000
```

Tetapi:

```text
Forecast Origin
       ↓
Historical Price Backbone
       +
External Context
       ↓
Multi-Horizon Forecast
       ↓
Relative Movement
       ↓
Reconstructed Price
```

---

## 10.2 Multi-Horizon

Research Contract menetapkan horizon:

```text
1
3
7
14
30
90
180
365 days
```

dengan batas maksimum 365 hari. Output yang diharapkan berbentuk trajectory/vector multi-horizon, bukan satu kurva yang dipaksa monoton.

Dalam UI:

```text
Forecast Horizon

[ 1D ] [ 3D ] [ 7D ] [ 14D ] [ 30D ] [ 90D ] [ 180D ] [ 365D ]
```

---

# 11. Forecast Result Requirements

Setiap forecast result minimal harus memiliki:

| Field                          | Requirement                       |
| ------------------------------ | --------------------------------- |
| Commodity                      | REQUIRED                          |
| Market                         | REQUIRED                          |
| Forecast origin                | REQUIRED                          |
| Horizon                        | REQUIRED                          |
| Current/reference price        | REQUIRED                          |
| Relative movement              | REQUIRED                          |
| Predicted/reconstructed price  | REQUIRED bila target memungkinkan |
| Model version                  | REQUIRED                          |
| Dataset version                | REQUIRED                          |
| Preprocessing/version contract | REQUIRED                          |
| Context availability           | REQUIRED                          |
| Data cutoff                    | REQUIRED                          |
| Source/provenance              | REQUIRED                          |
| Limitation/status              | REQUIRED                          |

Requirement bahwa forecast tidak boleh keluar tanpa model/data version berasal langsung dari baseline product reliability requirement.

---

# 12. Target Representation

Research Contract merekomendasikan relative price movement sebagai canonical modeling target, dengan direct price direkonstruksi untuk output product.

Secara konseptual:

```text
Price(t)
   ↓
Relative Movement
   ↓
Model
   ↓
Predicted Movement
   ↓
Reconstructed Price
```

Ini membuat produk dapat menampilkan dua perspektif:

### Model view

```text
Expected movement:
+X.X%
```

### User view

```text
Estimated price:
Rp XX.XXX
```

Perlu dibedakan antara **output model** dan **representasi yang direkonstruksi oleh product layer**.

---

# 13. Context Intelligence

Context dibagi menjadi:

```text
Climate / Supply
       +
News / Sentiment
       +
Macro / Logistics
       +
Calendar
```

Research Contract menetapkan historical price sebagai mandatory input, sementara climate/supply, news/sentiment, dan macro/logistics berada dalam final research direction; calendar bersifat pendukung.

---

# 14. Climate Context

UI dapat menampilkan:

```text
Climate Context
────────────────────

Supplier Region
Cianjur

Rainfall
████████░░

Temperature
XX.X °C

Anomaly
+X.X%

Recent Condition
...
```

Namun UI **tidak boleh mengatakan**:

> "Curah hujan menyebabkan harga cabai naik."

Bahasa yang sesuai:

> "Climate-related features digunakan sebagai salah satu modality dalam forecasting."

Atau ketika experimental evidence sudah tersedia:

> "Climate-related features memberikan tambahan predictive information pada horizon/evaluasi tertentu."

Research Contract menegaskan bahwa kontribusi prediktif tidak boleh diterjemahkan menjadi hubungan kausal tanpa pengujian kausal.

---

# 15. News / Sentiment Context

News module tidak hanya menampilkan:

```text
Sentiment: -0.4
```

Karena Research Contract secara eksplisit mengarahkan news representation agar dapat mencakup:

```text
Article Volume
Sentiment Balance
Intensity
Persistence
Recency
Topic Relevance
Source Count
Event Burst
```

dengan temporal cutoff berdasarkan waktu publikasi/availability.

Contoh product view:

```text
NEWS INTELLIGENCE

Articles: 124
Negative: 62
Positive: 31
Neutral: 31

Intensity     ████████
Persistence   ██████
Relevance     ███████

Recent Topics
• supply disruption
• rainfall
• market price
```

---

# 16. Macro / Logistics Context

Context ini dapat meliputi:

```text
Fuel Price
       +
Effective Date
       +
Distance
       +
Logistics Proxy
       +
Relevant Events
```

Research Contract memberikan aturan khusus bahwa BBM berbasis **effective-date**, sedangkan `distance_km` merupakan static feature. `distance × fuel price` hanya boleh disebut sebagai proxy biaya/logistics, bukan biaya logistik aktual.

---

# 17. Monitoring

Monitoring merupakan capability sekunder.

Purpose:

> Membantu pengguna melihat apakah kondisi harga masuk regime pergerakan ekstrem.

Bukan:

> "Sistem memprediksi crash."

Karena shock ditetapkan sebagai secondary phenomenon, bukan classification task utama.

Primary threshold ditentukan berdasarkan distribusi historical relative movement pada masing-masing horizon dan dihitung hanya dari training set. Q95 menjadi primary recommendation, sedangkan threshold lain dapat digunakan sebagai sensitivity analysis.

UI:

```text
PRICE MOVEMENT MONITOR

Current Regime
────────────────
Normal Movement

Recent Movement
+1.8%

Historical Context
Within normal range
```

---

# 18. Research Transparency Module

Halaman Research harus menjawab:

```text
Why?
What data?
How?
Which model?
How evaluated?
What changed?
What worked?
What did not?
```

Struktur:

```text
/research
   ├── methodology
   ├── data
   ├── model
   ├── experiments
   ├── benchmark
   ├── ablation
   └── limitations
```

Implementation Plan memang mengarahkan public product agar menyediakan methodology/model explanation dan research evidence termasuk benchmark/ablation.

---

# 19. Research Evidence

Research evidence tidak boleh berupa:

```text
ARIF-Net Accuracy = 97%
Therefore ARIF-Net is best
```

Format yang benar:

```text
Model
ARIF-Net

Protocol
Chronological Test

Horizon
7 Days

Metric
MAE / RMSE / ...

Baseline
Price-only / ...

Result
X.XX

Comparison
...

Evidence
Benchmark + Ablation
```

Phase 0 menyatakan candidate novelty belum boleh dianggap validated contribution sampai terdapat leakage-free benchmark, improvement, ablation, horizon-specific evidence, shock-regime evidence, reproducibility, dan literature validation.

---

# 20. Education Module

Karena target product bukan hanya researcher, diperlukan lapisan edukasi.

### `/learn`

```text
What is Food Price Forecasting?
        ↓
Why price changes?
        ↓
What is historical price?
        ↓
What is sentiment?
        ↓
What is climate signal?
        ↓
How multimodal forecasting works?
        ↓
How to interpret a forecast?
```

Education tidak menciptakan klaim baru tentang model. Ia hanya menyederhanakan konsep yang sudah didukung research contract.

---

# 21. Trust Layer

Ini merupakan **cross-cutting requirement**.

Setiap forecast dan research result harus dapat menjawab:

```text
When?
Where?
Using what data?
Using what model?
Which version?
What information was available?
How reliable is the result?
What are the limitations?
```

Metadata minimum:

```text
Forecast Origin
Market
Commodity
Horizon
Model Version
Dataset Version
Data Cutoff
Data Availability
Source
Experiment/Protocol
Limitations
```

---

# 22. Data Availability State

Karena modalitas mempunyai frequency dan release time berbeda, product wajib memiliki status data.

### Valid

```text
AVAILABLE
```

### Tidak tersedia

```text
MISSING
```

### Tidak cukup coverage

```text
INSUFFICIENT_COVERAGE
```

### Tidak lolos temporal rule

```text
TEMPORALLY_INVALID
```

### Tidak lolos schema

```text
SCHEMA_INVALID
```

Frontend tidak boleh diam-diam mengubah missing data menjadi nilai yang tidak terkontrol.

API harus secara eksplisit menangani missing modality dan menolak incompatible schema.

---

# 23. Research ↔ Product Integration Contract

Ini salah satu bagian terpenting PRD.

```text
             RESEARCH LAYER
────────────────────────────────────
Dataset
Preprocessing
Feature Engineering
Model
Experiment
Evaluation
Versioning
             │
             │ Contract
             ▼
             PRODUCT LAYER
────────────────────────────────────
API
Forecast Result
Visualization
Interaction
Caching
Research Storytelling
```

Product **tidak boleh membuat versi preprocessing sendiri**.

Misalnya:

```text
Research:
rainfall_7d = rolling rainfall

Product:
rainfall_7d = average UI data
```

Tidak boleh terjadi.

Implementation Plan menyatakan bahwa implementasi product tidak boleh mengubah preprocessing model secara berbeda dari research tanpa versioning dan explicit transformation contract.

---

# 24. Product Architecture Requirement

Arsitektur awal:

```text
┌─────────────────────────────┐
│        Next.js / React      │
│     ARIF Food Intelligence  │
└──────────────┬──────────────┘
               │ HTTPS
               ▼
┌─────────────────────────────┐
│     Forecast / Analysis API │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ Python Inference Service    │
│                             │
│ Preprocessing Contract      │
│ ARIF-Net / Candidate Model  │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ Versioned Data              │
│ Forecast Results            │
│ Model Artifacts             │
│ Experiment Artifacts        │
└─────────────────────────────┘
```

Architecture tersebut berasal langsung dari product architecture baseline.

---

# 25. API Requirement

API minimal harus mampu menjawab:

```http
GET /api/commodities
GET /api/commodities/:slug
GET /api/prices
GET /api/prices/history
GET /api/forecasts
GET /api/forecasts/:id
GET /api/context/climate
GET /api/context/news
GET /api/context/macro-logistics
GET /api/research/model
GET /api/research/experiments
GET /api/research/benchmarks
GET /api/research/ablations
```

Ini merupakan **desain API yang diusulkan pada PRD**, bukan API yang diklaim sudah ada di repository.

---

# 26. Forecast API Contract

Contoh logical response:

```json
{
  "commodity": {
    "slug": "cabai-merah-keriting",
    "name": "Cabai Merah Keriting"
  },
  "market": {
    "code": "PIKJ",
    "name": "Pasar Induk Kramat Jati"
  },
  "forecast_origin": "YYYY-MM-DD",
  "horizon": 7,
  "reference_price": 0,
  "predicted_change": 0.0,
  "predicted_price": 0,
  "model_version": "arif-net-x.x.x",
  "dataset_version": "dataset-x.x.x",
  "preprocessing_version": "preprocess-x.x.x",
  "data_cutoff": "YYYY-MM-DDTHH:MM:SS",
  "modalities": {
    "price": "available",
    "climate": "available",
    "news": "available",
    "macro_logistics": "partial"
  },
  "limitations": []
}
```

Schema ini **belum merupakan final implementation contract**; ia adalah kandidat contract yang nantinya harus dibekukan setelah Phase 1–model pipeline menghasilkan schema penelitian yang sebenarnya.

---

# 27. MVP Scope

Karena Anda ingin product dikembangkan paralel dengan model, saya membedakan antara **Product MVP** dan **Model-dependent functionality**.

## Phase A — Bisa dibangun sekarang

```text
✓ Next.js application shell
✓ Navigation
✓ Home
✓ Commodity explorer
✓ Commodity detail
✓ Historical price visualization
✓ Context UI
✓ Education
✓ Research pages
✓ Domain model
✓ API interface
✓ Mock/precomputed data adapter
✓ Version metadata system
✓ Loading/error/empty states
```

## Phase B — Menunggu research artifact valid

```text
○ Actual ARIF-Net inference
○ Real multi-horizon forecast
○ Final model explanation
○ Benchmark result
○ Ablation result
○ Final shock analysis
```

Ini penting karena Research Contract masih menempatkan Phase 1 pada **Data / Temporal Audit → provenance → temporal alignment → leakage audit → target construction → baseline dataset → split repair → reproducibility contract**.

Jadi kita dapat **membangun produk sekarang**, tetapi jangan mengunci UI sebagai representasi "hasil final ARIF-Net" sebelum artifact penelitian valid.

---

# 28. Precomputed vs Live Inference

Product baseline secara eksplisit mengarahkan penggunaan precomputed historical forecasts untuk eksplorasi stabil; live inference boleh dibatasi berdasarkan resource dan reliability.

Maka arsitektur product sebaiknya:

```text
Historical Exploration
        ↓
Precomputed Forecast Artifact

Demo Current / Selected Origin
        ↓
Limited Inference API
```

Bukan:

```text
Every page visit
      ↓
Load model
      ↓
Run full inference
```

---

# 29. Non-Functional Requirements

| Category        | Requirement                                                                 |
| --------------- | --------------------------------------------------------------------------- |
| Performance     | Dashboard responsif                                                         |
| Performance     | Historical exploration menggunakan caching/precomputed artifact bila sesuai |
| Reliability     | Forecast tidak keluar tanpa model version                                   |
| Reliability     | Missing modality harus eksplisit                                            |
| Reliability     | Invalid schema ditolak                                                      |
| Reproducibility | Preprocessing inference = preprocessing research contract                   |
| Transparency    | Source dan limitation dapat dilihat                                         |
| Security        | Tidak ada secret di frontend                                                |
| Security        | External credentials server-side                                            |
| Deployment      | Forecast retrieval tidak membutuhkan training ulang                         |
| Versioning      | Data/model/result harus identifiable                                        |

Baseline tersebut secara langsung tercantum dalam Implementation Plan.

---

# 30. Error & Empty States

Produk harus memiliki state yang jelas.

### Loading

```text
Loading market data...
```

### Missing climate

```text
Climate context is unavailable for this forecast origin.
```

### Insufficient coverage

```text
Climate data coverage is insufficient for this period.
```

### Invalid forecast

```text
Forecast unavailable:
required model artifact is not available.
```

### Old result

```text
Forecast generated using:
Model vX.X
Dataset vX.X
```

---

# 31. Product Navigation

Final public navigation yang konsisten dengan IA sebelumnya:

```text
Harga Pangan
Forecast
Konteks
Edukasi
Research
```

Sedangkan route teknis tetap tersedia melalui halaman terkait:

```text
/commodities/[slug]
/context/climate
/context/news
/context/macro-logistics
/research/model
/research/methodology
/research/data
/research/experiments
/research/benchmark
/research/ablation
/research/limitations
```

Public navigation tidak perlu menampilkan semua route teknis.

---

# 32. Recommended Golden Path

Jalur utama exhibition/demo:

```text
HOME
  ↓
PILIH KOMODITAS
  ↓
CURRENT PRICE
  ↓
PRICE HISTORY
  ↓
RECENT MOVEMENT
  ↓
FORECAST
  ↓
CONTEXT
  ├── Climate
  ├── News
  └── Macro / Logistics
  ↓
HOW MODEL WORKS
  ↓
EVIDENCE
  ↓
LIMITATIONS
```

Ini adalah bentuk operasional dari product story yang telah ditetapkan dalam Implementation Plan: pengunjung memahami **data → model → forecast → factor context → evidence**.

---

# 33. Acceptance Criteria MVP

Product MVP dianggap siap secara product engineering ketika:

| ID    | Acceptance Criteria                                            |
| ----- | -------------------------------------------------------------- |
| AC-01 | User dapat menemukan komoditas                                 |
| AC-02 | User dapat melihat current price                               |
| AC-03 | User dapat melihat historical trend                            |
| AC-04 | User dapat melihat forecast artifact yang valid                |
| AC-05 | Forecast menampilkan horizon                                   |
| AC-06 | Forecast menampilkan model/data version                        |
| AC-07 | Context tersedia berdasarkan availability                      |
| AC-08 | Missing data ditampilkan secara eksplisit                      |
| AC-09 | Research methodology dapat dibaca                              |
| AC-10 | Benchmark/ablation hanya ditampilkan jika artifact tersedia    |
| AC-11 | Source/provenance dapat ditelusuri                             |
| AC-12 | Product tidak membuat klaim kausal yang tidak dibuktikan       |
| AC-13 | Product tidak mengubah preprocessing research secara diam-diam |
| AC-14 | Tidak ada credential sensitif di frontend                      |

---

# 34. Critical Product Rules

Saya sarankan rules berikut dibuat sebagai **hard rules untuk AI Agent maupun developer**:

### Rule 01 — No Fake Forecast

Jangan pernah membuat angka forecast dummy yang terlihat sebagai hasil model final.

Gunakan:

```text
mock
sample
simulation
precomputed research artifact
```

dengan status yang jelas.

---

### Rule 02 — No Unversioned Result

Tidak boleh ada:

```text
Forecast = 123
```

tanpa:

```text
model_version
dataset_version
forecast_origin
```

---

### Rule 03 — No Silent Imputation

Jika modality hilang:

```text
MISSING
```

bukan diam-diam:

```text
0
mean
latest value
```

kecuali transformation tersebut memang didefinisikan oleh preprocessing contract.

---

### Rule 04 — No Causal Language

Jangan:

> "Hujan menyebabkan harga naik."

Gunakan:

> "Climate features digunakan sebagai predictive modality."

---

### Rule 05 — Research Result Only After Validation

Jangan menulis:

> "ARIF-Net unggul."

sebelum benchmark sesuai protocol selesai.

---

### Rule 06 — Product ≠ Research Notebook

Product hanya mengonsumsi:

```text
validated/versioned artifact
```

bukan menjalankan eksperimen penelitian secara bebas.

---

# 35. Build Strategy untuk Kondisi Anda Sekarang

Mengingat model masih dikembangkan paralel, struktur kerja yang paling aman adalah:

```text
                 ARIF-Net Research
                       │
              Phase 1 Data Audit
                       │
                       ▼
               Research Contract
                       │
                       ▼
                Model Artifacts
                       │
                       │
         ┌─────────────┴──────────────┐
         │                            │
         ▼                            ▼
   PRODUCT CONTRACT              UI / UX BUILD
         │                            │
         ▼                            ▼
      API Schema                 Next.js App
         │                            │
         └─────────────┬──────────────┘
                       ▼
               Integration Layer
                       ▼
              ARIF Food Intelligence
```

Dengan pola ini, pekerjaan website tidak perlu menunggu model selesai total, tetapi kita juga tidak memalsukan atau mengunci asumsi model yang belum tervalidasi.

---

# 36. Traceability ke Research Contract

| Product Requirement    | Research Basis           |
| ---------------------- | ------------------------ |
| Historical price       | Mandatory Price Backbone |
| Multi-horizon forecast | 1–365 days               |
| Climate context        | External modality        |
| News/sentiment         | External modality        |
| Macro/logistics        | External modality        |
| Forecast movement      | Relative movement target |
| Reconstructed price    | Product representation   |
| Model version          | Reproducibility          |
| Dataset version        | Reproducibility          |
| Data cutoff            | Temporal availability    |
| Context availability   | Anti-leakage             |
| Benchmark              | Research validation      |
| Ablation               | Contribution evidence    |
| Limitations            | Academic transparency    |

Research Contract menetapkan historical price sebagai backbone/input wajib, external modalities sebagai research direction final, serta temporal availability sebagai bagian fundamental dari forecasting protocol.

---

# 37. Status Keputusan Product

Agar tidak terjadi _scope drift_, saya membagi keputusan:

### LOCKED FROM RESEARCH

```text
Regression forecasting
Historical price mandatory
External modalities
Multi-horizon boundary ≤ 365 days
Temporal availability
Anti-leakage
Research transparency
No unsupported causal claims
```

### PRODUCT BASELINE

```text
Price Explorer
Commodity Intelligence Page
Forecast Center
Context Explorer
Monitoring
Education
Research
```

### PROPOSED — BELUM FINAL

```text
Exact API schema
Exact database schema
Exact model-serving technology
Exact caching technology
Exact authentication strategy
Exact visual design system
Exact live-inference strategy
```

### DEPENDENT ON PHASE 1–3

```text
Final forecast artifact
Final model architecture
Final model explanation
Benchmark values
Ablation results
Validated novelty
Final shock-regime evidence
```

Ini penting karena Phase 0 sendiri menyatakan candidate novelty baru dapat dipromosikan menjadi validated contribution setelah benchmark leakage-free, improvement, ablation, horizon-specific evidence, shock-regime evidence, reproducibility, dan literature validation terpenuhi.

---

# 38. Kesimpulan Step 06

Setelah Step 06 ini, kita sudah memiliki hubungan yang jelas:

```text
RESEARCH CONTRACT
       ↓
RESEARCH REQUIREMENTS
       ↓
PRODUCT REQUIREMENTS
       ↓
DOMAIN MODEL
       ↓
INFORMATION ARCHITECTURE
       ↓
USER JOURNEY
       ↓
PRODUCT FEATURES
```

Dan positioning produknya menjadi cukup jelas:

> **ARIF Food Intelligence adalah public-first food-price intelligence platform yang menggunakan ARIF-Net sebagai research forecasting engine, dengan pengalaman utama Current Price → Price Dynamics → Forecast → Multimodal Context → Explanation → Evidence.**

Yang paling penting, PRD ini **tidak mengubah penelitian menjadi product marketing claim**. Model yang masih _candidate_ tetap candidate, hasil yang belum divalidasi tetap belum dipublikasikan sebagai evidence, dan data yang belum lolos temporal/provenance audit belum dianggap siap menjadi input final.
