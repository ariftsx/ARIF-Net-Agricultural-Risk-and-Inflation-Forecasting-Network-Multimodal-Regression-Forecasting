# STEP 07 — TECHNICAL PRODUCT ARCHITECTURE & SYSTEM DESIGN

## ARIF Food Intelligence v0.1

**Status:** WORKING ARCHITECTURE
**Product:** ARIF Food Intelligence
**Research Engine:** ARIF-Net
**Architecture Type:** Web Application + API + Python Inference Service + Versioned Research Artifacts

---

# 1. Architecture Objective

Arsitektur harus mampu memisahkan dua dunia:

```text
RESEARCH
────────────────────────────────────
Data
Preprocessing
Feature Engineering
Training
Experiments
Evaluation
Model Artifacts
         │
         │ versioned contract
         ▼
PRODUCT
────────────────────────────────────
API
Forecast Retrieval
Visualization
Interaction
Research Storytelling
```

Prinsip ini penting karena sumber menetapkan bahwa product implementation tidak boleh memiliki preprocessing berbeda dari research tanpa versioning dan transformation contract. 

---

# 2. Architectural Principles

## AP-01 — Research/Product Separation

```text
ARIF-Net
= Research / Model Layer

ARIF Food Intelligence
= Product / Presentation Layer
```

ARIF-Net bukan nama website.

---

## AP-02 — Historical Price Remains Backbone

Product harus merepresentasikan bahwa historical price merupakan fondasi forecasting.

External modalities:

```text
Climate / Supply
News / Sentiment
Macro / Logistics
Calendar
```

menjadi contextual inputs, bukan pengganti price dynamics.

Research Contract menetapkan historical price sebagai mandatory input dan explicit price backbone sebagai prinsip arsitektur kandidat. 

---

## AP-03 — No Hidden Research Logic

Frontend tidak boleh:

```text
menghitung ulang feature
mengubah scaling
mengubah target
mengimputasi data secara bebas
```

Frontend hanya membaca artifact/result yang sudah memiliki contract.

---

## AP-04 — Version Everything Important

Minimal:

```text
Dataset Version
Model Version
Preprocessing Version
Experiment Protocol Version
Forecast Result Version
```

---

## AP-05 — Forecast Is a Result Artifact

Jangan menjadikan forecast sebagai proses yang selalu harus dihitung ketika halaman dibuka.

Model yang source dokumentasinya sendiri menyarankan:

```text
Historical Exploration → Precomputed Forecast
Demo / Selected Origin → Limited Live Inference
```

karena public-first dan reliability menjadi pertimbangan product. 

---

# 3. High-Level System Architecture

Arsitektur target:

```text
                         INTERNET
                            │
                            ▼
              ┌─────────────────────────┐
              │   ARIF FOOD INTELLIGENCE│
              │       Next.js / React   │
              └────────────┬────────────┘
                           │ HTTPS
                           ▼
              ┌─────────────────────────┐
              │    Product API Layer    │
              │ Forecast / Price /      │
              │ Context / Research     │
              └────────────┬────────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
 ┌──────────────────────┐     ┌──────────────────────┐
 │ Research Result Store│     │ Python Inference      │
 │                      │     │ Service               │
 │ Forecast artifacts   │     │                      │
 │ Dataset metadata     │     │ Preprocessing        │
 │ Model metadata       │     │ ARIF-Net             │
 │ Experiments          │     │ Candidate models     │
 └──────────────────────┘     └───────────┬──────────┘
                                          │
                                          ▼
                              ┌────────────────────────┐
                              │ Versioned Model/Data   │
                              │ Artifacts               │
                              └────────────────────────┘
```

Ini merupakan pengembangan teknis dari arsitektur baseline yang sudah ditetapkan source:

**Next.js/React → Forecast/Analysis API → Python Inference Service → versioned data/result/model artifacts.** 

---

# 4. Architecture Layers

Saya sarankan sistem memiliki **5 logical layers**.

```text
┌────────────────────────────────────┐
│ 1. EXPERIENCE LAYER                │
│ Next.js / React                    │
└─────────────────┬──────────────────┘
                  ↓
┌────────────────────────────────────┐
│ 2. APPLICATION/API LAYER           │
│ Forecast / Price / Context /       │
│ Research API                       │
└─────────────────┬──────────────────┘
                  ↓
┌────────────────────────────────────┐
│ 3. INTELLIGENCE RUNTIME            │
│ Python preprocessing + inference   │
└─────────────────┬──────────────────┘
                  ↓
┌────────────────────────────────────┐
│ 4. RESEARCH ARTIFACT LAYER         │
│ Dataset / Model / Forecast /       │
│ Experiment artifacts               │
└─────────────────┬──────────────────┘
                  ↓
┌────────────────────────────────────┐
│ 5. SOURCE / DATA LAYER             │
│ Price / Climate / News / Macro     │
│ / Logistics / Calendar             │
└────────────────────────────────────┘
```

---

# 5. Layer 1 — Experience Layer

## Technology

**Baseline:** Next.js / React.

Tugas frontend:

```text
Discovery
Visualization
Filtering
Forecast exploration
Context exploration
Research storytelling
```

Frontend **bukan** tempat model dijalankan.

### Frontend responsibilities

```text
✓ Fetch API
✓ Render charts
✓ Render tables
✓ Apply UI filters
✓ Display loading state
✓ Display error state
✓ Display data availability
✓ Display version metadata
✓ Display limitations
```

### Frontend forbidden

```text
✗ Training model
✗ Feature engineering research
✗ Scaling model input
✗ Reconstructing preprocessing
✗ Calling secret external API directly
✗ Generating unsupported research claims
```

---

# 6. Layer 2 — Product API Layer

API berfungsi sebagai **boundary antara UI dan research runtime**.

```text
Frontend
   │
   ▼
Product API
   │
   ├── Price Service
   ├── Forecast Service
   ├── Context Service
   ├── Research Service
   └── Metadata Service
```

API tidak perlu mengetahui detail internal seluruh training pipeline.

Contohnya frontend cukup meminta:

```http
GET /api/commodities/cabai-merah-keriting/forecast
```

dan tidak perlu mengetahui:

```text
PyTorch
tensor shape
scaler
feature columns
checkpoint path
```

---

# 7. API Domain

Saya mengusulkan pemisahan logical endpoint berdasarkan domain:

```text
/api/commodities
/api/markets
/api/prices
/api/forecasts
/api/context
/api/research
/api/metadata
```

Bukan:

```text
/api/do-everything
```

---

# 8. Forecast API Boundary

Forecast API menjadi boundary terpenting.

```text
                   ┌─────────────────────┐
                   │ Frontend            │
                   └─────────┬───────────┘
                             │
                             ▼
                  GET /api/forecasts/...
                             │
                             ▼
                   ┌─────────────────────┐
                   │ Forecast Service    │
                   └─────────┬───────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
      Precomputed Artifact          Live Inference
```

API menentukan apakah request dapat dipenuhi dari precomputed result atau perlu inference.

---

# 9. Forecast Retrieval Strategy

## Mode A — Precomputed

Untuk:

```text
historical forecast origin
historical exploration
exhibition browsing
benchmark visualization
```

flow:

```text
User
 ↓
API
 ↓
Forecast Artifact
 ↓
Response
```

Tidak perlu load model.

---

## Mode B — Live Inference

Untuk request yang memang diperbolehkan:

```text
User
 ↓
API
 ↓
validate request
 ↓
validate model
 ↓
validate preprocessing version
 ↓
prepare input
 ↓
Python inference
 ↓
validate output
 ↓
return result
```

---

# 10. Python Inference Service

Python service adalah **runtime model**, bukan seluruh research notebook environment.

Logical structure:

```text
python-inference/
├── api/
├── schemas/
├── preprocessing/
├── inference/
├── models/
├── postprocessing/
├── validators/
└── metadata/
```

### Responsibility

```text
Input Validation
       ↓
Preprocessing Contract
       ↓
Feature Transformation
       ↓
Model Loading
       ↓
Inference
       ↓
Output Reconstruction
       ↓
Result Validation
```

---

# 11. Model Runtime Contract

Python service tidak boleh bebas mengambil:

```text
"latest model"
```

Model harus dipanggil secara eksplisit:

```text
model_version = arif-net-0.x.x
```

Contoh:

```text
model/
  arif-net-0.1.0/
  arif-net-0.2.0/
```

Sehingga sebuah forecast dapat direproduksi.

---

# 12. Data Contract

Input model harus mempunyai schema terdefinisi.

Secara konseptual:

```json
{
  "commodity": "cabai_merah_keriting",
  "market": "PIKJ",
  "forecast_origin": "YYYY-MM-DD",
  "horizon": 7,
  "price": {},
  "climate": {},
  "supply": {},
  "news": {},
  "macro": {},
  "logistics": {},
  "calendar": {}
}
```

**Catatan:** field di atas adalah rancangan application contract, bukan klaim bahwa schema tersebut sudah digunakan repository.

Final schema harus mengikuti hasil Phase 1 data contract.

---

# 13. Temporal Integrity Boundary

Ini bagian yang sangat penting.

Pada:

```text
forecast_origin = t
```

sistem hanya boleh menggunakan informasi:

```text
information_available <= t
```

Tidak boleh:

```text
weather(t+7)
news(t+3)
future fuel price
future realized supply
future realized price
```

sebagai observed input.

Research Contract menetapkan aturan information availability ini secara eksplisit dan mengharuskan future realized exogenous variables dilarang sebagai input observasi. 

---

# 14. Canonical Forecast Flow

```text
┌────────────────────┐
│ Forecast Request   │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Request Validation │
│ commodity          │
│ market             │
│ origin             │
│ horizon            │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Availability Check │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Dataset Contract   │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Preprocessing      │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ ARIF-Net Inference │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Postprocessing     │
│ pct → price        │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Output Validation  │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Version Metadata   │
└─────────┬──────────┘
          ↓
      API Response
```

---

# 15. Historical Price Data Flow

```text
Price Source
    ↓
Raw Data
    ↓
Validation
    ↓
Normalization
    ↓
Temporal Alignment
    ↓
Feature Engineering
    ↓
Versioned Dataset
    ↓
Research / Inference
```

Historical price harus menjadi foundation karena penelitian menempatkannya sebagai mandatory input/backbone. 

---

# 16. Multimodal Data Flow

```text
                     ┌── Climate
                     │
                     ├── Supply
                     │
Historical Price ────┤
                     ├── News / Sentiment
                     │
                     ├── Macro
                     │
                     ├── Logistics
                     │
                     └── Calendar
                              │
                              ▼
                    Temporal Alignment
                              │
                              ▼
                    Feature Engineering
                              │
                              ▼
                     Dataset Contract
                              │
                              ▼
                         Model Input
```

Modality contract Phase 0 mengatur price, climate, supply, news, macro, logistics, dan calendar beserta aturan waktu masing-masing. 

---

# 17. Research Artifact Store

Arsitektur tidak seharusnya menyimpan hanya "model.pth".

Artifact harus memiliki struktur:

```text
artifacts/
├── datasets/
│   └── dataset-x.y.z/
├── models/
│   └── arif-net-x.y.z/
├── forecasts/
│   └── model-x/
├── experiments/
│   └── experiment-x/
├── benchmarks/
│   └── benchmark-x/
└── manifests/
```

Tujuan:

```text
reproducibility
traceability
rollback
comparison
publication
```

---

# 18. Forecast Artifact

Sebuah forecast result idealnya memiliki:

```text
ForecastArtifact
│
├── identity
│   ├── commodity
│   ├── market
│   └── forecast_origin
│
├── prediction
│   ├── horizon
│   ├── relative_movement
│   └── reconstructed_price
│
├── provenance
│   ├── dataset_version
│   ├── model_version
│   ├── preprocessing_version
│   └── data_cutoff
│
├── context
│   ├── climate
│   ├── news
│   ├── macro
│   └── logistics
│
└── governance
    ├── availability
    ├── limitations
    └── status
```

---

# 19. Versioning Chain

Setiap output harus dapat ditelusuri:

```text
Forecast
   │
   ├── Model Version
   │       ↓
   ├── Dataset Version
   │       ↓
   ├── Preprocessing Version
   │       ↓
   └── Experiment Protocol
```

Contoh:

```text
Forecast:
2026-09-01 / CMK / 7D

Model:
arif-net-0.3.0

Dataset:
food-price-0.4.0

Preprocessing:
prep-0.4.0

Protocol:
exp-protocol-0.2.0
```

---

# 20. Domain-to-Architecture Mapping

Domain model Step 05 sekarang diterjemahkan ke system:

| Domain Entity           | Runtime                  |
| ----------------------- | ------------------------ |
| Commodity               | Product API              |
| Market                  | Product API              |
| Price Observation       | Price Service            |
| Forecast Run            | Forecast Service         |
| Forecast Point          | Forecast Artifact        |
| Context Snapshot        | Context Service          |
| Supplier Region         | Research/Data layer      |
| News Context            | Context Service          |
| Climate Context         | Context Service          |
| Macro/Logistics Context | Context Service          |
| Data Provenance         | Metadata/Artifact layer  |
| Model Version           | Model Registry concept   |
| Dataset Version         | Dataset Manifest         |
| Experiment              | Research Service         |
| Education Content       | CMS/static content layer |
| Research Artifact       | Research Artifact Store  |

---

# 21. API Response Architecture

Response tidak cukup:

```json
{
  "prediction": 12345
}
```

Minimum structure:

```json
{
  "data": {
    "prediction": {}
  },
  "context": {},
  "provenance": {
    "model_version": "...",
    "dataset_version": "...",
    "preprocessing_version": "...",
    "data_cutoff": "..."
  },
  "availability": {},
  "limitations": []
}
```

Dengan demikian frontend tidak perlu menebak status result.

---

# 22. Data Availability Protocol

API harus membedakan:

```text
AVAILABLE
PARTIAL
MISSING
INSUFFICIENT_COVERAGE
TEMPORALLY_INVALID
SCHEMA_INVALID
```

Contoh:

```json
{
  "climate": {
    "status": "INSUFFICIENT_COVERAGE"
  }
}
```

Lebih aman daripada:

```json
{
  "climate": 0
}
```

karena angka nol dapat salah ditafsirkan sebagai kondisi aktual.

Baseline product memang mewajibkan missing modality ditangani secara eksplisit dan incompatible schema ditolak. 

---

# 23. Market & Commodity Boundary

Arsitektur harus memisahkan:

```text
Commodity
≠
Market
≠
Supplier Region
```

Contoh:

```text
Commodity:
Cabai Merah Keriting

Forecast Market:
PIKJ

Supplier Regions:
Cianjur
Bandung
Sumedang
...
```

Tidak boleh membuat:

```text
Cianjur = market
```

atau menganggap sebuah supplier region otomatis memiliki market-share tertentu tanpa evidence.

Phase 0 memisahkan Jakarta sebagai forecast market dan supplier/production regions sebagai external context. 

---

# 24. Research Runtime vs Product Runtime

Saya menyarankan **jangan membuat frontend langsung membaca folder research**.

Salah:

```text
Next.js
   ↓
data/processed/*.csv
```

Lebih tepat:

```text
Next.js
   ↓
API
   ↓
Artifact / Database
```

Research pipeline:

```text
Raw
 ↓
Processed
 ↓
Model
 ↓
Experiment
 ↓
Publish Artifact
```

baru kemudian:

```text
Published Artifact
 ↓
Product API
 ↓
Frontend
```

Dengan demikian product hanya mengonsumsi output yang memang sudah dipublikasikan ke product contract.

---

# 25. Deployment Architecture

Untuk deployment awal, arsitektur logical-nya:

```text
                    INTERNET
                       │
                       ▼
                HTTPS / Domain
                       │
              ┌────────┴─────────┐
              │                  │
              ▼                  ▼
        Next.js App          Product API
                                  │
                                  ▼
                         Python Inference
                                  │
                 ┌────────────────┴──────────────┐
                 │                               │
                 ▼                               ▼
            Model Artifact                Result / Data Store
```

**Hosting provider, database engine, object storage, containerization dan orchestration belum dikunci oleh source**, sehingga belum saya tetapkan sebagai keputusan arsitektur final.

---

# 26. Authentication

Untuk public exhibition:

```text
Default:
Anonymous Public Access
```

Tidak perlu memaksakan:

```text
Login
Register
Role
Admin
```

untuk user umum.

Implementation Report memang mengarahkan public-first dan menyebut authentication bukan prioritas utama untuk exhibition. 

Authentication dapat muncul nanti untuk:

```text
Research operator
Artifact publisher
Internal experiment management
```

tetapi itu merupakan extension, bukan core public MVP.

---

# 27. Caching Strategy

Caching dibutuhkan terutama untuk:

```text
Commodity metadata
Historical prices
Historical forecasts
Research pages
Benchmark
Experiment results
```

Flow:

```text
User
 ↓
API
 ↓
Cache
 ├── HIT → response
 └── MISS
       ↓
  Artifact Store
       ↓
    Cache
       ↓
    response
```

Untuk live inference:

```text
Request fingerprint
        ↓
Existing result?
   ├── yes → return
   └── no → inference
```

Detail teknologi cache masih **OPEN**.

---

# 28. Reliability Strategy

API harus fail-safe.

Misalnya model tidak tersedia:

```text
HTTP 503
MODEL_UNAVAILABLE
```

bukan:

```text
prediction = 0
```

Dataset incompatibility:

```text
HTTP 422
INVALID_DATA_CONTRACT
```

Missing context:

```text
HTTP 200
context.status = "MISSING"
```

Dengan demikian tidak semua kondisi error diperlakukan sama.

---

# 29. Security Boundary

### Frontend

```text
PUBLIC
```

Tidak menyimpan:

```text
API Secret
Database Password
Model Credentials
External API Token
```

### Server

```text
SECRET
```

Menangani:

```text
credentials
external API access
database connection
model artifact access
```

Ini mengikuti security baseline product yang mensyaratkan secret tidak berada di frontend dan credentials external berada server-side. 

---

# 30. Observability

System perlu mengetahui:

```text
request count
latency
forecast request
inference duration
model load failure
artifact failure
schema failure
missing modality
API failure
```

Untuk setiap inference:

```text
request_id
forecast_id
model_version
dataset_version
duration
status
```

Contoh log:

```text
forecast_id=fc_001
model=arif-net-0.3.0
dataset=food-price-0.4.0
horizon=7
duration=842ms
status=success
```

---

# 31. Testing Architecture

Testing tidak hanya frontend.

```text
                    TESTING
                       │
      ┌────────────────┼─────────────────┐
      ▼                ▼                 ▼
   Frontend           API             Inference
      │                │                 │
      ▼                ▼                 ▼
Component         Contract         Preprocessing
E2E               Validation        Model Input
Visual            Error State       Output
                                        │
                                        ▼
                                  Research Integrity
```

Research-level test juga harus memastikan test set tidak digunakan untuk checkpoint/model selection. Phase 0 menetapkan train → validation → freeze → test sebagai kontrak selection/evaluation. 

---

# 32. API Contract Testing

Contoh:

```text
Given:
model_version exists
dataset_version exists
schema valid
availability valid

Then:
forecast request accepted
```

Sedangkan:

```text
Given:
model_version missing

Then:
request rejected
```

Dan:

```text
Given:
future external data supplied

Then:
request rejected
```

Ini mengubah prinsip penelitian menjadi guardrail teknis.

---

# 33. Repository Architecture

Target repository organization dari source adalah:

```text
ARIF-Net-Foot-Price-Shock/
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── manifests/
│
├── preprocessing/
│
├── features/
│
├── modeling/
│   ├── baselines/
│   ├── arif_net/
│   ├── candidates/
│   └── evaluation/
│
├── experiments/
│   ├── configs/
│   ├── logs/
│   └── manifests/
│
├── models/
│
├── results/
│
├── notebooks/
│
├── product/
│   ├── api/
│   └── web/
│
└── docs/
    ├── research/
    ├── methodology/
    ├── data/
    ├── architecture/
    └── experiments/
```

Source secara eksplisit menyebut ini sebagai **target organization**, bukan klaim bahwa repository sekarang sudah mempunyai struktur tersebut. 

---

# 34. Architecture Decision Register

| Decision                        | Status             |
| ------------------------------- | ------------------ |
| Next.js / React frontend        | BASELINE           |
| Python inference service        | BASELINE           |
| Forecast/Analysis API           | BASELINE           |
| Versioned result/artifact layer | BASELINE           |
| Historical price mandatory      | LOCKED             |
| Product/research separation     | LOCKED             |
| Precomputed historical forecast | BASELINE           |
| Limited live inference          | BASELINE           |
| Anonymous public-first product  | BASELINE           |
| Exact database technology       | OPEN               |
| Exact cache technology          | OPEN               |
| Exact deployment provider       | OPEN               |
| Exact API framework             | OPEN               |
| Exact object storage            | OPEN               |
| Final ARIF-Net architecture     | RESEARCH CANDIDATE |
| Reliability-aware fusion        | RESEARCH CANDIDATE |
| Horizon-conditioned fusion      | RESEARCH CANDIDATE |

Ini penting: **system architecture tidak boleh mengunci research model architecture terlalu dini.**

Research Contract sendiri menempatkan reliability-aware dan horizon-conditioned fusion sebagai candidate methodology yang harus diuji, bukan hasil final. 

---

# 35. Architecture Boundary: Yang Boleh Berubah

Ada beberapa bagian yang memang harus fleksibel.

```text
                STABLE
────────────────────────────────
Product Domain
API Boundary
Artifact Versioning
Research/Product Separation
Temporal Integrity
                   │
                   │
                   ▼
                FLEXIBLE
────────────────────────────────
Model Architecture
Fusion Mechanism
Encoder Type
Model Serving Implementation
Database
Cache
Deployment Infrastructure
```

Artinya, apabila hasil eksperimen nanti menunjukkan ARIF-Net membutuhkan perubahan architecture, website tidak perlu dibangun ulang dari nol.

---

# 36. Build Order

Dengan kondisi model Anda masih berjalan paralel, implementasi teknis sebaiknya:

```text
A. Domain Types
       ↓
B. API Contract
       ↓
C. Mock / Fixture Data
       ↓
D. Frontend Shell
       ↓
E. Commodity Explorer
       ↓
F. Price Explorer
       ↓
G. Forecast UI
       ↓
H. Context UI
       ↓
I. Research UI
       ↓
J. Artifact Contract
       ↓
K. Real API
       ↓
L. Python Inference
       ↓
M. Real ARIF-Net
```

Jadi Anda **tidak perlu menunggu model selesai untuk mulai membuat website**, tetapi bagian yang bergantung terhadap hasil penelitian tetap menggunakan contract/mock/precomputed artifact sampai valid.

---

# 37. Critical Architecture Rule

Saya menyarankan satu aturan menjadi dasar seluruh AI Agent/project development:

> **The product must consume validated, versioned research artifacts through an explicit contract; it must never recreate research logic implicitly inside the application.**

Dengan kata lain:

```text
Research decides:
"What the model means"

Product decides:
"How users understand and interact with it"
```

---

# 38. End-to-End Final Flow

Keseluruhan sistem sekarang dapat kita representasikan:

```text
             DATA SOURCES
                  │
      ┌───────────┼────────────┐
      │           │            │
    Price       Climate      News
      │           │         Sentiment
      │           │            │
      └───────────┼────────────┘
                  │
          Macro / Logistics
                  │
                  ▼
       ┌─────────────────────┐
       │ Temporal Alignment  │
       │ + Leakage Audit     │
       └──────────┬──────────┘
                  │
                  ▼
       ┌─────────────────────┐
       │ Dataset Version     │
       └──────────┬──────────┘
                  │
                  ▼
       ┌─────────────────────┐
       │ Model Training      │
       │ / Experiments       │
       └──────────┬──────────┘
                  │
                  ▼
       ┌─────────────────────┐
       │ Validated Artifact  │
       │ Model / Results     │
       └──────────┬──────────┘
                  │
             API Contract
                  │
                  ▼
       ┌─────────────────────┐
       │ Forecast API        │
       └──────────┬──────────┘
                  │
                  ▼
       ┌─────────────────────┐
       │ ARIF Food           │
       │ Intelligence Web    │
       └──────────┬──────────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
      Price    Forecast   Context
        │         │         │
        └─────────┼─────────┘
                  ▼
             Explanation
                  │
                  ▼
              Evidence
```

---

# 39. Architecture Acceptance Criteria

Step 07 dapat dianggap valid ketika:

| ID      | Criteria                                                                       |
| ------- | ------------------------------------------------------------------------------ |
| ARCH-01 | Frontend tidak menjalankan model                                               |
| ARCH-02 | API menjadi boundary utama                                                     |
| ARCH-03 | Python inference terpisah dari frontend                                        |
| ARCH-04 | Forecast memiliki model/data version                                           |
| ARCH-05 | Preprocessing inference mempunyai contract                                     |
| ARCH-06 | Historical price tetap mandatory                                               |
| ARCH-07 | Temporal availability dapat divalidasi                                         |
| ARCH-08 | Missing modality memiliki status eksplisit                                     |
| ARCH-09 | Invalid schema dapat ditolak                                                   |
| ARCH-10 | Product dapat menggunakan precomputed result                                   |
| ARCH-11 | Research artifacts dapat ditelusuri                                            |
| ARCH-12 | Model architecture dapat berevolusi tanpa merombak product                     |
| ARCH-13 | Tidak ada secret di frontend                                                   |
| ARCH-14 | Research result belum tervalidasi tidak dipresentasikan sebagai final evidence |

---

# 40. Hasil Step 07

Sekarang struktur project kita sudah memiliki tiga lapisan desain yang saling mengunci:

```text
STEP 05
Domain Model + Information Architecture
              ↓
STEP 06
Product Requirements
              ↓
STEP 07
Technical Architecture
```

Sehingga kita sudah tahu:

```text
USER
 ↓
PRODUCT PAGE
 ↓
API
 ↓
INFERENCE / ARTIFACT
 ↓
RESEARCH MODEL
 ↓
VERSIONED DATA
```

dan bukan sekadar:

```text
USER → WEBSITE → MODEL
```

## Satu hal yang sengaja belum saya kunci

Saya **belum menentukan database, ORM, hosting, Docker, Redis, message queue, cloud provider, atau framework Python API tertentu**. Source yang menjadi authority tidak menetapkan keputusan tersebut; memaksakannya sekarang justru akan mengubah bagian yang masih terbuka menjadi seolah-olah keputusan final.

Research Contract juga masih menganggap arsitektur ARIF-Net seperti reliability-aware fusion dan horizon-conditioned fusion sebagai **candidate**, sehingga Technical Architecture harus tetap menjadi *model-agnostic* pada boundary inference. 