# STEP 08 — DATA CONTRACT & API CONTRACT SPECIFICATION

## ARIF Food Intelligence v0.1

**Status:** Working Specification
**Product:** ARIF Food Intelligence
**Research Engine:** ARIF-Net
**Purpose:** Menentukan bentuk data, identifier, metadata, request/response, validation, versioning, dan boundary komunikasi antara **research artifacts → API → frontend**.

Dokumen ini merupakan turunan langsung dari arsitektur Step 07. Ia belum menentukan database atau ORM tertentu; yang dikunci di sini adalah **kontrak data dan interface**, bukan teknologi penyimpanannya.

---

# 1. Mengapa Step 08 Penting

Tanpa data contract, implementasi mudah berubah menjadi:

```text
Frontend
   ↓
API
   ↓
"ambil data apa saja"
   ↓
Model
```

Itu berbahaya untuk ARIF-Net karena penelitian mempunyai aturan ketat mengenai:

* temporal availability,
* leakage,
* historical price backbone,
* multimodal data,
* model/data version,
* reproducibility.

Phase 0 secara eksplisit menyatakan bahwa inference harus menggunakan preprocessing contract yang sama dengan training dan bahwa product tidak boleh mengubah preprocessing research secara diam-diam. 

Maka kontrak kita:

```text
DATA CONTRACT
      ↓
PREPROCESSING CONTRACT
      ↓
INFERENCE CONTRACT
      ↓
RESULT CONTRACT
      ↓
PRODUCT API CONTRACT
```

---

# 2. Contract Hierarchy

Kita perlu membedakan lima kontrak.

```text
┌──────────────────────────────┐
│ 1. SOURCE DATA CONTRACT      │
│ Bentuk data dari sumber      │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ 2. RESEARCH DATA CONTRACT    │
│ Bentuk data setelah cleaning │
│ + temporal alignment         │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ 3. MODEL INPUT CONTRACT      │
│ Tensor/features yang model   │
│ benar-benar konsumsi         │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ 4. FORECAST RESULT CONTRACT  │
│ Output model + metadata      │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ 5. PRODUCT API CONTRACT      │
│ Data yang dikirim ke web     │
└──────────────────────────────┘
```

**Tidak semua layer ini harus memiliki schema identik.**

Yang harus konsisten adalah hubungan dan transformation contract-nya.

---

# 3. Canonical Domain Objects

Berdasarkan domain model Step 05, object utama kita:

```text
Commodity
Market
Price Observation
Forecast Run
Forecast Point
Context Snapshot
Supplier Region
Climate Context
News Context
Supply Context
Macro/Logistics Context
Data Source
Data Provenance
Model Version
Dataset Version
Experiment
Research Artifact
```

---

# 4. Entity: Commodity

## Purpose

Representasi komoditas yang menjadi subject intelligence.

### Logical schema

```json
{
  "id": "commodity_cmk",
  "slug": "cabai-merah-keriting",
  "name": "Cabai Merah Keriting",
  "category": "pangan",
  "unit": "...",
  "status": "active"
}
```

### Required

```text
id
slug
name
unit
status
```

### Important rule

Jangan menggunakan:

```text
"cabai"
"beras"
"bawang"
```

sebagai taxonomy final tanpa definisi grade/type.

Phase 0 mewajibkan taxonomy final mengunci jenis komoditas, grade, satuan harga, dan definisi market. 

---

# 5. Canonical Commodity Scope

Untuk Capstone, baseline-nya:

| Commodity            | Forecast Market |
| -------------------- | --------------- |
| Cabai Merah Keriting | PIKJ            |
| Bawang Merah         | PIKJ            |
| Beras                | PIBC            |

Beras masih memerlukan penguncian type/grade pada Data Contract final. 

---

# 6. Entity: Market

Market harus berdiri sendiri.

```json
{
  "id": "market_pikj",
  "code": "PIKJ",
  "name": "Pasar Induk Kramat Jati",
  "city": "Jakarta",
  "region": "DKI Jakarta",
  "status": "active"
}
```

Relasi:

```text
Commodity
   │
   └── Forecast Market
             │
             └── Price Observations
```

Jangan membuat:

```text
commodity.market = "Jakarta"
```

saja.

Karena `market` harus menjadi entity yang dapat memiliki metadata sendiri.

---

# 7. Entity: Supplier Region

Supplier region berbeda dari market.

```json
{
  "id": "region_cianjur",
  "name": "Cianjur",
  "province": "Jawa Barat",
  "role": "supplier_region"
}
```

Relasi:

```text
Commodity
     ↕
Supplier Region
     ↓
Climate / Supply Context
     ↓
Forecast
```

Phase 0 menegaskan Jakarta sebagai **forecast market**, sedangkan wilayah supplier/production merupakan external context dan tidak boleh dianggap sebagai market share tanpa evidence. 

---

# 8. Entity: Price Observation

Ini adalah object utama historical price.

```json
{
  "id": "priceobs_001",
  "commodity_id": "commodity_cmk",
  "market_id": "market_pikj",
  "observed_at": "YYYY-MM-DD",
  "price": 50000,
  "unit": "...",
  "source_id": "source_x",
  "availability_at": "YYYY-MM-DDTHH:MM:SS",
  "status": "valid"
}
```

### Required

```text
commodity_id
market_id
observed_at
price
unit
source_id
availability_at
status
```

### Why `availability_at`?

Karena:

```text
observed_at ≠ necessarily available_at
```

Forecasting menggunakan informasi yang tersedia pada forecast origin, bukan sekadar tanggal observasi.

---

# 9. Price Observation Rules

### Valid

```text
availability_at <= forecast_origin
```

### Invalid

```text
availability_at > forecast_origin
```

Walaupun tanggal observasinya secara kalender tampak lebih awal.

Ini merupakan konsekuensi langsung dari temporal availability contract. 

---

# 10. Entity: Forecast Run

`ForecastRun` adalah satu eksekusi/publikasi forecast.

```json
{
  "id": "forecast_run_001",
  "commodity_id": "commodity_cmk",
  "market_id": "market_pikj",
  "forecast_origin": "YYYY-MM-DD",
  "horizon": 7,
  "model_version": "arif-net-0.x.x",
  "dataset_version": "food-price-0.x.x",
  "preprocessing_version": "prep-0.x.x",
  "experiment_protocol_version": "exp-0.x.x",
  "data_cutoff": "YYYY-MM-DDTHH:MM:SS",
  "status": "validated"
}
```

---

# 11. Forecast Run Identity

Combination berikut harus dapat mengidentifikasi sebuah run:

```text
commodity
+
market
+
forecast_origin
+
horizon
+
model_version
+
dataset_version
+
preprocessing_version
```

Dengan begitu:

```text
CMK + PIKJ + 2026-09-01 + 7D
```

belum cukup sebagai identity global.

Versinya juga harus diketahui.

---

# 12. Entity: Forecast Point

Karena model dirancang untuk multi-horizon/trajectory, `ForecastRun` dapat memiliki banyak `ForecastPoint`.

```json
{
  "forecast_run_id": "forecast_run_001",
  "horizon_day": 1,
  "target_date": "YYYY-MM-DD",
  "predicted_change": 0.023,
  "predicted_price": 51150
}
```

Contoh:

```text
ForecastRun
   │
   ├── Day 1
   ├── Day 3
   ├── Day 7
   ├── Day 14
   ├── Day 30
   └── ...
```

Research Contract menetapkan horizon standard:

```text
1
3
7
14
30
90
180
365
```

dengan upper bound 365 hari. Output diperlakukan sebagai trajectory/vector, bukan satu angka monoton. 

---

# 13. Forecast Target Contract

Canonical modeling target:

```text
relative price movement
```

Sedangkan:

```text
predicted_price
```

merupakan reconstructed product output.

Secara konseptual:

```text
Reference Price
       +
Predicted Relative Movement
       ↓
Reconstructed Price
```

Jadi API sebaiknya **menyimpan/menampilkan keduanya**, tetapi tidak menyamakan keduanya sebagai jenis output model yang sama.

---

# 14. Forecast Point Contract

Minimum:

```text
forecast_run_id
horizon_day
target_date
predicted_change
predicted_price
```

Optional setelah model valid:

```text
prediction_interval
uncertainty
confidence
```

Tetapi uncertainty **belum dikunci** sebagai bagian core Capstone. Ia masih extension/future research scope.

---

# 15. Entity: Context Snapshot

Forecast membutuhkan snapshot kondisi multimodal pada origin.

```json
{
  "id": "context_001",
  "forecast_run_id": "forecast_run_001",
  "climate": {},
  "supply": {},
  "news": {},
  "macro": {},
  "logistics": {},
  "calendar": {}
}
```

Tujuannya bukan menampilkan semua raw data kepada user.

Tujuannya:

> mendokumentasikan context yang tersedia dan digunakan oleh forecast run.

---

# 16. Climate Context

Logical object:

```json
{
  "status": "available",
  "regions": [
    {
      "region_id": "region_cianjur",
      "rainfall": 120.5,
      "temperature_avg": 25.2,
      "anomaly": 0.8
    }
  ],
  "coverage": 0.91
}
```

Status dapat:

```text
available
partial
missing
insufficient_coverage
temporally_invalid
```

Phase 0 menempatkan climate sebagai external modality dan mewajibkan coverage/availability diaudit sebelum modeling. 

---

# 17. News Context

Logical object:

```json
{
  "status": "available",
  "article_count": 124,
  "sentiment": {
    "positive": 31,
    "negative": 62,
    "neutral": 31
  },
  "intensity": 0.71,
  "persistence": 0.64,
  "recency": 0.82,
  "topic_relevance": 0.88
}
```

Ini mengikuti arah Phase 0 bahwa news representation tidak ideal jika direduksi menjadi satu `sentiment_mean`; volume, sentiment balance, intensity, persistence, recency, topic relevance, dan source count dapat menjadi candidate features. 

---

# 18. Macro / Logistics Context

Logical object:

```json
{
  "status": "available",
  "fuel_price": 13500,
  "fuel_effective_date": "YYYY-MM-DD",
  "distance_km": 145.2,
  "logistics_cost_proxy": 1960200
}
```

Namun:

```text
logistics_cost_proxy
```

harus jelas sebagai **proxy**, bukan actual logistics cost.

Phase 0 secara eksplisit membatasi `distance_km × fuel_price` sebagai proxy sederhana. 

---

# 19. Entity: Data Source

Semua data harus dapat ditelusuri ke sumber.

```json
{
  "id": "source_bmkg",
  "name": "BMKG",
  "type": "climate",
  "url": "...",
  "license_or_terms": "...",
  "status": "active"
}
```

Field minimum:

```text
id
name
type
url
license_or_terms
status
```

---

# 20. Entity: Data Provenance

`DataSource` menjawab:

> "data berasal dari mana?"

`DataProvenance` menjawab:

> "record/result ini berasal dari data yang mana dan diproses bagaimana?"

Contoh:

```json
{
  "source_id": "source_bmkg",
  "dataset_version": "food-price-0.4.0",
  "retrieved_at": "...",
  "source_record_reference": "...",
  "transformation_version": "prep-0.4.0"
}
```

---

# 21. Entity: Dataset Version

Dataset harus immutable secara konseptual setelah dipublikasikan.

```json
{
  "id": "dataset_food_price_0.4.0",
  "version": "0.4.0",
  "created_at": "...",
  "date_range": {
    "start": "...",
    "end": "..."
  },
  "commodities": [],
  "markets": [],
  "modalities": [],
  "schema_version": "data-schema-0.3.0",
  "provenance_version": "prov-0.2.0",
  "status": "validated"
}
```

---

# 22. Entity: Model Version

```json
{
  "id": "model_arif_net_0.3.0",
  "name": "ARIF-Net",
  "version": "0.3.0",
  "framework": "PyTorch",
  "artifact_uri": "...",
  "dataset_version": "0.4.0",
  "preprocessing_version": "0.4.0",
  "status": "candidate"
}
```

### Status

```text
candidate
validated
published
deprecated
archived
```

Jangan memberi status `validated` hanya karena file model berhasil disimpan. Validasi harus berasal dari research evaluation process.

---

# 23. Entity: Experiment

```json
{
  "id": "exp_001",
  "name": "full_multimodal_7d",
  "protocol_version": "exp-protocol-0.2.0",
  "dataset_version": "dataset-0.4.0",
  "model_version": "arif-net-0.3.0",
  "status": "completed"
}
```

Experiment metadata digunakan untuk research transparency, bukan hanya product visualization.

---

# 24. Entity: Research Artifact

Artifact dapat berupa:

```text
dataset
model
forecast
benchmark
ablation
error_analysis
explainability
documentation
```

Logical schema:

```json
{
  "id": "artifact_001",
  "type": "benchmark",
  "version": "benchmark-0.2.0",
  "status": "validated",
  "created_at": "...",
  "source_experiment_id": "exp_001"
}
```

---

# 25. Universal Metadata

Semua artifact penting idealnya memiliki:

```text
id
version
created_at
updated_at
status
source
```

Untuk research artifact:

```text
dataset_version
model_version
experiment_version
```

ditambahkan sesuai konteks.

---

# 26. Canonical Status Enumeration

Kita sebaiknya memakai vocabulary terkontrol.

### General status

```text
draft
candidate
validated
published
deprecated
archived
```

### Data availability

```text
available
partial
missing
insufficient_coverage
temporally_invalid
schema_invalid
```

### Forecast status

```text
pending
generated
validated
published
failed
```

---

# 27. Product API Structure

Logical endpoint tree:

```text
/api
│
├── /commodities
│   ├── GET /
│   └── GET /:slug
│
├── /markets
│   └── GET /
│
├── /prices
│   ├── GET /
│   └── GET /history
│
├── /forecasts
│   ├── GET /
│   ├── GET /:id
│   └── GET /:id/points
│
├── /context
│   ├── /climate
│   ├── /news
│   └── /macro-logistics
│
├── /monitoring
│
├── /research
│   ├── /model
│   ├── /methodology
│   ├── /benchmark
│   └── /ablation
│
└── /metadata
    ├── /models
    ├── /datasets
    └── /sources
```

Nama endpoint ini masih **PROPOSED**.

---

# 28. Commodity API

### Request

```http
GET /api/commodities
```

### Response

```json
{
  "data": [
    {
      "id": "commodity_cmk",
      "slug": "cabai-merah-keriting",
      "name": "Cabai Merah Keriting",
      "unit": "...",
      "status": "active"
    }
  ]
}
```

---

# 29. Commodity Detail API

```http
GET /api/commodities/cabai-merah-keriting
```

Response:

```json
{
  "data": {
    "commodity": {},
    "markets": [],
    "supplier_regions": [],
    "latest_price": {},
    "latest_forecast": {},
    "available_context": {}
  }
}
```

Tujuannya agar Commodity Intelligence Page dapat mengambil satu resource utama.

---

# 30. Historical Price API

```http
GET /api/prices/history
  ?commodity=cabai-merah-keriting
  &market=PIKJ
  &from=YYYY-MM-DD
  &to=YYYY-MM-DD
```

Response:

```json
{
  "data": [
    {
      "date": "YYYY-MM-DD",
      "price": 50000,
      "unit": "...",
      "market": "PIKJ"
    }
  ],
  "meta": {
    "commodity": "...",
    "market": "...",
    "source": "...",
    "dataset_version": "..."
  }
}
```

---

# 31. Forecast API

### Historical/precomputed retrieval

```http
GET /api/forecasts
  ?commodity=cabai-merah-keriting
  &market=PIKJ
  &origin=YYYY-MM-DD
  &horizon=7
```

Response:

```json
{
  "data": {
    "forecast_run": {
      "id": "forecast_run_001",
      "origin": "YYYY-MM-DD",
      "horizon": 7
    },
    "reference_price": 50000,
    "points": [
      {
        "horizon_day": 1,
        "target_date": "YYYY-MM-DD",
        "predicted_change": 0.012,
        "predicted_price": 50600
      },
      {
        "horizon_day": 3,
        "target_date": "YYYY-MM-DD",
        "predicted_change": 0.019,
        "predicted_price": 50950
      },
      {
        "horizon_day": 7,
        "target_date": "YYYY-MM-DD",
        "predicted_change": 0.025,
        "predicted_price": 51250
      }
    ]
  },
  "provenance": {},
  "availability": {},
  "limitations": []
}
```

Angka di atas hanyalah **schema example**, bukan data empiris ARIF-Net.

---

# 32. Forecast Request Contract

Untuk live inference:

```json
{
  "commodity": "cabai-merah-keriting",
  "market": "PIKJ",
  "forecast_origin": "YYYY-MM-DD",
  "horizon": 7
}
```

Server kemudian menentukan:

```text
1. dataset version
2. model version
3. preprocessing version
4. input availability
5. valid context
```

Client tidak boleh mengirim:

```json
{
  "model": "latest"
}
```

karena `latest` tidak reproducible.

---

# 33. Model Selection Rule

Server harus menerima explicit model version:

```json
{
  "model_version": "arif-net-0.3.0"
}
```

atau memilih model melalui **published product configuration** yang memiliki version sendiri.

Yang tidak boleh:

```text
frontend → latest_model.pth
```

karena hasil dapat berubah tanpa perubahan API contract.

---

# 34. Temporal Validation

Saat request:

```text
origin = T
```

server harus memvalidasi semua input:

```text
availability_at <= T
```

untuk historical/external observed data.

Contoh:

```text
News published:
09:00 → valid

News published:
14:00 → invalid
```

jika forecast cutoff:

```text
T = 12:00
```

Ini merupakan implementasi teknis dari information availability rule Phase 0. 

---

# 35. Future Exogenous Data Rule

Server harus menolak input seperti:

```text
future_weather_realized
future_news
future_fuel_price
future_supply
```

sebagai observed input.

Future calendar yang memang diketahui sebelumnya boleh digunakan.

Future exogenous forecast baru dapat digunakan jika nantinya dibuat sebagai separate exogenous forecasting/scenario mechanism. Phase 0 secara eksplisit memisahkan extension tersebut dari baseline forecasting. 

---

# 36. Schema Validation

Setiap request harus melewati:

```text
Schema Validation
      ↓
Semantic Validation
      ↓
Temporal Validation
      ↓
Availability Validation
      ↓
Model Compatibility Validation
```

Contoh:

```text
schema valid
≠
forecast valid
```

Karena data bisa valid secara JSON tetapi tetap invalid secara temporal.

---

# 37. Model Compatibility Contract

Model memiliki expected schema:

```json
{
  "dataset_schema_version": "schema-0.4.0",
  "preprocessing_version": "prep-0.4.0",
  "required_modalities": [
    "price",
    "climate",
    "news",
    "macro_logistics"
  ]
}
```

Jika dataset incompatible:

```text
REJECT
```

bukan:

```text
auto rename
auto fill
auto drop
```

karena baseline product memang mewajibkan incompatible schema ditolak, bukan diam-diam diperbaiki. 

---

# 38. Missing Modality Contract

Misalnya climate unavailable:

```json
{
  "availability": {
    "climate": {
      "status": "missing"
    }
  }
}
```

Apakah model tetap boleh inference?

**Tidak boleh ditentukan sembarang di frontend.**

Harus ada model contract:

```text
supports_missing_climate = true/false
```

Dengan demikian:

```text
Model A → boleh missing climate
Model B → wajib climate
```

merupakan keputusan runtime/model contract.

---

# 39. Forecast Result Metadata

Setiap result minimal:

```json
{
  "provenance": {
    "model_version": "...",
    "dataset_version": "...",
    "preprocessing_version": "...",
    "experiment_protocol_version": "...",
    "data_cutoff": "..."
  }
}
```

Ini merupakan syarat penting reproducibility dan transparency pada product. 

---

# 40. API Error Contract

Jangan mengembalikan error yang tidak terstruktur:

```text
Something went wrong
```

Gunakan:

```json
{
  "error": {
    "code": "MODEL_VERSION_NOT_FOUND",
    "message": "Requested model version is unavailable.",
    "request_id": "req_xxx"
  }
}
```

---

# 41. Error Codes

Baseline:

```text
INVALID_REQUEST
INVALID_COMMODITY
INVALID_MARKET
INVALID_HORIZON
INVALID_DATE_RANGE
SCHEMA_INVALID
DATASET_VERSION_NOT_FOUND
MODEL_VERSION_NOT_FOUND
MODEL_INCOMPATIBLE
TEMPORAL_DATA_INVALID
MODALITY_MISSING
INSUFFICIENT_COVERAGE
FORECAST_UNAVAILABLE
INFERENCE_FAILED
ARTIFACT_NOT_FOUND
```

---

# 42. HTTP Semantics

Usulan:

| HTTP | Meaning                     |
| ---: | --------------------------- |
|  200 | Request successful          |
|  400 | Invalid request             |
|  404 | Resource/version not found  |
|  409 | Version/contract conflict   |
|  422 | Semantically invalid data   |
|  503 | Model/inference unavailable |
|  500 | Unexpected server error     |

Ini adalah application design proposal, bukan rule dari research source.

---

# 43. API Response Envelope

Saya menyarankan standard:

```json
{
  "data": {},
  "meta": {},
  "provenance": {},
  "availability": {},
  "limitations": {},
  "error": null
}
```

Untuk error:

```json
{
  "data": null,
  "meta": {},
  "provenance": {},
  "availability": {},
  "limitations": [],
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

---

# 44. Why This Envelope Matters

Frontend tidak harus menebak:

```text
Apakah forecast valid?
Model apa?
Dataset apa?
Climate tersedia?
Hasil ini dari cache?
Apakah ada limitation?
```

Semua tersedia sebagai metadata contract.

---

# 45. Versioning Strategy

Kita memisahkan tiga hal.

### API Version

```text
v1
```

### Schema Version

```text
forecast-schema-0.1.0
```

### Research Artifact Version

```text
model: arif-net-0.3.0
dataset: food-price-0.4.0
```

Jadi:

```text
API v1
+
Forecast Schema 0.1.0
+
Model 0.3.0
+
Dataset 0.4.0
```

tidak dicampur menjadi satu nomor.

---

# 46. Breaking Change Rules

### MAJOR

Jika mengubah:

```text
field meaning
target semantics
core API contract
required fields
identifier semantics
```

### MINOR

Jika menambahkan:

```text
optional field
optional endpoint
additional context
new metadata
```

### PATCH

Jika:

```text
documentation
description
validation message
non-semantic clarification
```

Ini konsisten dengan discipline versioning yang sudah ada di Implementation Plan. 

---

# 47. Data Contract Manifest

Setiap dataset sebaiknya memiliki manifest seperti:

```json
{
  "dataset_version": "food-price-0.4.0",
  "schema_version": "data-schema-0.3.0",
  "created_at": "...",
  "date_range": {
    "start": "...",
    "end": "..."
  },
  "markets": ["PIKJ", "PIBC"],
  "commodities": [
    "cabai-merah-keriting",
    "bawang-merah",
    "beras"
  ],
  "modalities": [
    "price",
    "climate",
    "supply",
    "news",
    "sentiment",
    "macro",
    "logistics",
    "calendar"
  ],
  "temporal_policy": "information_available_at_origin",
  "status": "validated"
}
```

**Schema ini proposed**, sedangkan konsep provenance, modality, temporal policy, dan versioning berasal dari baseline research.

---

# 48. Model Manifest

```json
{
  "model_version": "arif-net-0.3.0",
  "model_name": "ARIF-Net",
  "artifact_type": "regression_forecaster",
  "dataset_version": "food-price-0.4.0",
  "preprocessing_version": "prep-0.4.0",
  "input_schema_version": "model-input-0.2.0",
  "supported_horizons": [1, 3, 7, 14, 30, 90, 180, 365],
  "required_modalities": [
    "price"
  ],
  "optional_modalities": [
    "climate",
    "supply",
    "news",
    "macro",
    "logistics",
    "calendar"
  ],
  "status": "candidate"
}
```

Perlu dicatat: exact `required_modalities` selain price belum boleh kita klaim final sebelum implementation model selesai. Source hanya mengunci arah modality research.

---

# 49. Product Forecast Artifact Manifest

```json
{
  "artifact_id": "forecast_2026_09_01_cmk_pikj_7d",
  "artifact_type": "forecast",
  "commodity": "cabai-merah-keriting",
  "market": "PIKJ",
  "forecast_origin": "2026-09-01",
  "horizon": 7,
  "model_version": "arif-net-0.3.0",
  "dataset_version": "food-price-0.4.0",
  "preprocessing_version": "prep-0.4.0",
  "data_cutoff": "2026-09-01T12:00:00+07:00",
  "status": "published"
}
```

---

# 50. Research → Product Publishing Flow

Ini menjadi flow canonical:

```text
                    RESEARCH
                       │
                       ▼
              Dataset Generation
                       │
                       ▼
                Model Training
                       │
                       ▼
                Evaluation
                       │
                       ▼
             Validated Artifact
                       │
                       ▼
               PUBLISH MANIFEST
                       │
                       ▼
                 PRODUCT API
                       │
                       ▼
                  FRONTEND
```

Tidak boleh:

```text
Notebook
  ↓
langsung dibaca frontend
```

---

# 51. Important Separation: Training Data vs Product Data

Kita perlu membedakan:

### Research Dataset

Untuk:

```text
training
validation
test
experiments
ablation
```

### Product Dataset

Untuk:

```text
current price
historical exploration
published context
published forecasts
```

Keduanya dapat berasal dari sumber yang sama, tetapi product harus mengambil **versioned/published representation**.

---

# 52. Important Separation: Prediction vs Context

Forecast response jangan menggabungkan semua hal menjadi satu giant object tanpa boundaries.

Lebih tepat:

```text
Forecast
 ├── Prediction
 ├── Provenance
 ├── Availability
 └── Context Reference
```

Kemudian:

```text
GET /forecast
GET /context/climate
GET /context/news
GET /context/macro-logistics
```

Hal ini membuat product lebih mudah dikembangkan.

---

# 53. Performance Consideration

Untuk historical exploration:

```text
Frontend
 ↓
API
 ↓
Precomputed Forecast Artifact
```

Untuk live inference:

```text
Frontend
 ↓
API
 ↓
Validation
 ↓
Inference
```

Implementasi Plan memang mengarahkan historical exploration menggunakan precomputed/cache ketika sesuai dan tidak mengharuskan full training saat retrieval. 

---

# 54. Contract Compatibility Matrix

Setiap forecast dapat dianggap valid hanya jika:

| Contract             | Must Match |
| -------------------- | ---------: |
| Commodity taxonomy   |          ✓ |
| Market definition    |          ✓ |
| Dataset schema       |          ✓ |
| Preprocessing        |          ✓ |
| Model expected input |          ✓ |
| Temporal policy      |          ✓ |
| Horizon              |          ✓ |
| Model version        |          ✓ |
| Dataset version      |          ✓ |
| Output schema        |          ✓ |

Jika satu komponen incompatible, result tidak boleh silently diterima.

---

# 55. Example End-to-End

User memilih:

```text
Cabai Merah Keriting
PIKJ
Forecast: 7 days
Origin: 2026-09-01
```

System:

```text
1. resolve commodity
2. resolve market
3. validate origin
4. resolve dataset
5. resolve model
6. resolve preprocessing
7. validate availability
8. obtain historical price
9. obtain permitted climate
10. obtain permitted news
11. obtain permitted macro/logistics
12. construct model input
13. inference
14. reconstruct predicted price
15. attach metadata
16. return API response
```

---

# 56. What the Frontend Should Never Know

Frontend **tidak perlu tahu**:

```text
PyTorch tensor shape
checkpoint path
optimizer
learning rate
loss implementation
GPU/CPU
training epoch
data-loader implementation
```

Frontend hanya perlu:

```text
forecast
context
metadata
availability
limitations
```

---

# 57. What the API Should Never Invent

API tidak boleh membuat:

```text
fake model version
fake confidence
fake attribution
fake source
fake benchmark
fake sentiment
fake climate status
```

Semua harus berasal dari artifact atau data source yang sah.

Ini sangat penting karena project baseline juga melarang synthetic/hardcoded evidence pada research layer. 

---

# 58. Contract Rules for AI Agent

Karena project Anda juga dikembangkan dengan AI Agent, Step 08 ini sebaiknya dijadikan hard constraint.

### AI Agent MUST

```text
1. Read schema before writing integration.
2. Validate version compatibility.
3. Preserve temporal cutoff.
4. Preserve field semantics.
5. Preserve provenance.
6. Reject incompatible schema.
7. Never fabricate unavailable values.
8. Never call "latest" model implicitly.
```

### AI Agent MUST NOT

```text
1. Rename semantic fields silently.
2. Add future information.
3. Replace missing data with arbitrary values.
4. Rebuild research preprocessing inside UI.
5. Create fake research metrics.
6. Turn predictive information into causal explanation.
```

---

# 59. Current Open Decisions

Setelah Step 08, masih ada beberapa hal yang **memang belum boleh kita putuskan**:

| Decision                        | Status          |
| ------------------------------- | --------------- |
| Physical database               | OPEN            |
| ORM                             | OPEN            |
| Object storage                  | OPEN            |
| Exact API framework             | OPEN            |
| Authentication implementation   | OPEN            |
| Cache implementation            | OPEN            |
| Real inference orchestration    | OPEN            |
| Final model input tensor schema | OPEN            |
| Final ARIF-Net architecture     | OPEN            |
| Final explainability schema     | OPEN            |
| Uncertainty output              | FUTURE/OPTIONAL |

---

# 60. Step 08 Acceptance Criteria

Step ini dapat dianggap selesai apabila:

```text
✓ Commodity contract defined
✓ Market contract defined
✓ Price Observation defined
✓ Forecast Run defined
✓ Forecast Point defined
✓ Context Snapshot defined
✓ Provenance defined
✓ Model Version defined
✓ Dataset Version defined
✓ API boundary defined
✓ Forecast request defined
✓ Forecast response defined
✓ Error contract defined
✓ Temporal validation defined
✓ Version compatibility defined
✓ Missing modality behavior defined
✓ Research/Product boundary defined
```

---

# 61. Hasil Arsitektur Kita Sekarang

Setelah Step 05 → 06 → 07 → 08, sistem sudah membentuk chain yang cukup kuat:

```text
                 ARIF-NET
                    │
          Research Contract
                    │
                    ▼
             Research Data
                    │
              Dataset Version
                    │
                    ▼
             Model / Experiment
                    │
               Model Version
                    │
                    ▼
             Forecast Artifact
                    │
              Data Contract
                    │
                    ▼
               Product API
                    │
               API Contract
                    │
                    ▼
            ARIF Food Intelligence
```

Dan secara user experience:

```text
Commodity
   ↓
Current Price
   ↓
Historical Dynamics
   ↓
Forecast
   ↓
Climate / News / Macro Context
   ↓
Explanation
   ↓
Evidence
```

Ini tetap konsisten dengan product direction yang ditetapkan sumber: **Data → Context → Forecast → Explanation → Evidence**. 

---

# 62. Satu Koreksi Penting terhadap Roadmap

Ada satu hal yang perlu kita jaga agar dokumentasi tidak kontradiktif.

Dokumen Implementation Plan di satu bagian menempatkan:

```text
P8 Research Freeze
   ↓
P9 Product
```

sebagai urutan aman, tetapi source yang sama juga menyediakan fase S9 Product/API. 

Interpretasi teknis yang paling konsisten adalah:

```text
BUILD PRODUCT SHELL NOW
        +
DEFINE CONTRACT NOW
        +
USE MOCK/PRECOMPUTED DATA NOW

BUT

PUBLISH FINAL MODEL RESULTS
ONLY AFTER RESEARCH VALIDATION
```

Jadi Anda tetap bisa mengerjakan UI/API sekarang tanpa mengorbankan integritas penelitian.