# STEP 05 — Product Domain Model + Information Architecture

## 1. Pergeseran model mental

Pada tahap awal kita sempat melihat produk sebagai:

```text
Model
↓
Forecast
↓
Dashboard
```

Sekarang, setelah STEP 01–04, model mental yang lebih tepat adalah:

```text
COMMODITY
    ↓
MARKET
    ↓
PRICE
    ↓
CONTEXT
    ↓
FORECAST
    ↓
EXPLANATION
    ↓
EDUCATION / RESEARCH
```

Jadi **Commodity menjadi domain object utama**.

Model ARIF-Net bukan object utama yang dilihat pengguna publik.

---

# 2. Core Domain Objects

Saya mengusulkan domain object berikut.

| Entity                      | Fungsi                                               | Status     |
| --------------------------- | ---------------------------------------------------- | ---------- |
| **Commodity**               | Komoditas yang dieksplorasi                          | `PROPOSED` |
| **Market**                  | Pasar referensi/target                               | `PROPOSED` |
| **Price Observation**       | Harga aktual berdasarkan tanggal                     | `PROPOSED` |
| **Forecast Run**            | Satu hasil forecasting pada forecast origin tertentu | `PROPOSED` |
| **Forecast Point**          | Output forecast per horizon                          | `PROPOSED` |
| **Context Snapshot**        | Konteks multimodal yang tersedia pada cutoff         | `PROPOSED` |
| **Supplier Region**         | Wilayah pemasok/sentra produksi                      | `PROPOSED` |
| **News Context**            | Informasi berita terkait                             | `PROPOSED` |
| **Climate Context**         | Informasi iklim                                      | `PROPOSED` |
| **Supply Context**          | Informasi pasokan                                    | `PROPOSED` |
| **Macro/Logistics Context** | Informasi ekonomi/logistik                           | `PROPOSED` |
| **Model Version**           | Identitas model artifact                             | `REQUIRED` |
| **Dataset Version**         | Identitas dataset                                    | `REQUIRED` |
| **Experiment**              | Artefak eksperimen                                   | `PROPOSED` |
| **Education Content**       | Materi literasi/edukasi                              | `PROPOSED` |
| **Research Artifact**       | Methodology/evidence/documentation                   | `PROPOSED` |

Sebagian besar object di atas adalah **product abstraction** dari domain dan research artifact yang sudah ada, bukan daftar entity yang secara eksplisit sudah dibakukan dalam Phase 0.

---

# 3. Commodity

## Definisi

Komoditas adalah object pusat dari pengalaman pengguna.

Contoh current scope:

```text
Cabai Merah Keriting
Bawang Merah
Beras
```

Phase 0 menetapkan tiga komoditas prioritas tersebut. 

### Data minimum

```text
commodity_id
name
slug
category
unit
description
status
```

Contoh:

```json
{
  "id": "cmk",
  "name": "Cabai Merah Keriting",
  "slug": "cabai-merah-keriting",
  "unit": "kg"
}
```

---

# 4. Market

Saya sangat menyarankan Market menjadi entity terpisah.

Kenapa?

Karena Phase 0 tidak menjadikan satu market sebagai global default untuk semua komoditas.

Canonical mapping sekarang:

```text
CMK
→ PIKJ

Bawang Merah
→ PIKJ

Beras
→ PIBC
```

Phase 0 menetapkan Jakarta sebagai target market, dengan PIKJ untuk CMK/bawang merah dan PIBC untuk beras. 

### Model

```text
Market
├── id
├── name
├── city
├── region
├── market_type
└── description
```

### Relasi

```text
Commodity
    │
    └── Target Market
```

Untuk future expansion:

```text
Commodity
   ├── Market A
   ├── Market B
   └── Market C
```

Jadi kita tidak membuat schema yang hanya cocok untuk PIKJ.

---

# 5. Price Observation

Ini adalah **fakta historis/observed data**, bukan forecast.

```text
PriceObservation
├── commodity_id
├── market_id
├── observation_date
├── price
├── unit
├── source_id
└── availability_time
```

Perbedaan yang sangat penting:

```text
OBSERVED
Price = data aktual
```

vs

```text
PREDICTED
Price = hasil rekonstruksi forecast
```

Jangan mencampur keduanya dalam satu concept.

---

# 6. Price Analytics

Di atas `PriceObservation`, kita bisa memiliki derived analytics:

```text
Price Analytics
├── daily_change
├── cumulative_change
├── rolling_change
├── volatility
└── movement_regime
```

Ini tidak harus disimpan sebagai raw database record jika bisa dihitung dari price series atau precomputed artifact.

Dengan demikian:

```text
Raw / canonical
→ Price Observation

Derived
→ Trend
→ Volatility
→ Movement
```

---

# 7. Supplier Region

Ini menjadi sangat penting karena sekarang product scope juga ingin melayani perspective petani/produsen.

Phase 0 menetapkan supplier-region framework dan secara eksplisit memperingatkan agar wilayah tersebut tidak dianggap sebagai market-share aktual tanpa evidence distribusi harian. 

### Entity

```text
SupplierRegion
├── id
├── name
├── province
├── latitude
├── longitude
└── description
```

Relasi:

```text
Commodity
      │
      ├── Supplier Region A
      ├── Supplier Region B
      └── Supplier Region C
```

Lebih tepat lagi:

```text
CommoditySupplierRegion
├── commodity_id
├── supplier_region_id
├── priority
└── evidence_reference
```

Karena hubungan tersebut **bergantung pada komoditas**.

---

# 8. Forecast Run

Ini menurut saya entity teknis yang paling penting.

Satu `Forecast Run` berarti:

> **Satu proses inference untuk satu commodity + market + forecast origin + model/data version.**

Contoh:

```text
Forecast Run
────────────────
Commodity:
Cabai Merah Keriting

Market:
PIKJ

Forecast Origin:
2026-10-01

Cutoff:
2026-09-30 18:00

Model:
ARIF-Net vX.X

Dataset:
ARIF-DATA vX.X
```

Ini sangat selaras dengan requirement bahwa forecast result harus mempunyai model/data version dan temporal cutoff. 

---

# 9. Forecast Point

Satu run menghasilkan banyak forecast point.

```text
ForecastRun
     │
     ├── h=1
     ├── h=3
     ├── h=7
     ├── h=14
     ├── h=30
     ├── h=90
     ├── h=180
     └── h=365
```

Phase 0 memang menetapkan vector/trajectory multi-horizon dan bukan satu angka monoton sampai 365 hari. 

### ForecastPoint

```text
horizon
relative_movement
reconstructed_price
```

Secara konsep:

```text
r_hat(t,h)
+
P_hat(t+h)
```

Harga nominal direkonstruksi dari relative movement dan harga pada forecast origin. 

---

# 10. Context Snapshot

Di sinilah product dan research bertemu.

Satu forecast jangan hanya memiliki:

```text
forecast = +5%
```

tetapi:

```text
Forecast Run
    │
    ├── Price Context
    ├── Climate Context
    ├── Supply Context
    ├── News Context
    ├── Macro Context
    ├── Logistics Context
    └── Calendar Context
```

Kenapa **Snapshot**?

Karena yang ingin kita tampilkan adalah:

> **informasi yang tersedia pada saat forecast dibuat**

bukan data yang belakangan diketahui.

Ini sangat penting karena temporal availability/cutoff adalah bagian fundamental dari research contract. 

---

# 11. Context tidak semuanya mempunyai struktur identik

Kita sebaiknya tidak memaksakan satu table besar:

```text
context
 ├── rainfall
 ├── sentiment
 ├── fuel
 ├── news
 └── ...
```

Lebih baik secara domain:

```text
Climate Context
Supply Context
News Context
Macro Context
Logistics Context
```

karena sumber, timestamp, dan semantics-nya berbeda.

Phase 0 sendiri memang memisahkan modality tersebut karena karakter temporal dan availability-nya berbeda. 

---

# 12. Data Source / Provenance

Ini sebaiknya menjadi entity cross-cutting.

```text
DataSource
├── id
├── organization
├── source_name
├── source_url
├── source_type
├── license
└── description
```

Kemudian setiap observation/artifact bisa ditelusuri:

```text
Price Observation
      ↓
Data Source

Climate Observation
      ↓
Data Source

News Article
      ↓
Data Source
```

Ini sesuai dengan Data Contract yang mewajibkan dataset name, source organization/URL, collection method, coverage date, frequency, timezone, availability time, license, transformation, feature list, cutoff rule, dan leakage status. 

---

# 13. News Context

Untuk news jangan membuat domain object hanya:

```text
sentiment = 0.3
```

karena Phase 0 memang sudah menetapkan bahwa news tidak cukup direpresentasikan sebagai scalar polarity.

Kandidat yang disebutkan:

```text
article_volume
sentiment_balance
intensity
persistence
recency
topic_relevance
source_count
event_burst
```



Jadi product object bisa berbentuk:

```text
News Context
├── article_count
├── sentiment_summary
├── intensity
├── persistence
├── relevant_topics
└── representative_articles
```

Untuk public UI, tidak semuanya harus ditampilkan.

---

# 14. Climate Context

Contoh:

```text
Climate Context
├── supplier_region
├── rainfall
├── temperature
├── humidity
├── anomaly
├── period
└── availability_time
```

Phase 0 memang memasukkan rainfall, temperature, humidity, anomaly, cumulative rainfall, extreme-weather indicators, dan fitur turunan lainnya sebagai candidate. 

---

# 15. Macro / Logistics Context

Misalnya:

```text
Macro Context
├── indicator
├── value
├── release_time
└── source

Logistics Context
├── fuel_price
├── effective_date
├── distance_km
└── proxy_flag
```

Phase 0 secara khusus menempatkan BBM sebagai event/effective-date based dan distance sebagai static feature; `distance × fuel price` hanya boleh disebut proxy biaya logistik, bukan actual logistics cost. 

---

# 16. Research Artifact

Sekarang kita keluar dari domain public.

```text
ResearchArtifact
├── type
├── title
├── version
├── publication_status
├── experiment_id
└── resource_location
```

Jenis:

```text
methodology
architecture
benchmark
ablation
evaluation
limitation
```

Ini nanti mengisi Research Center.

---

# 17. Model Version

Model version harus menjadi entity tersendiri atau minimal first-class metadata.

```text
ModelVersion
├── id
├── name
├── version
├── architecture
├── training_config
├── preprocessing_version
├── status
└── artifact_uri
```

Kenapa?

Karena nanti:

```text
ARIF-Net v0.1
ARIF-Net v0.2
ARIF-Net v1.0
```

bisa memiliki hasil berbeda.

Product baseline memang mensyaratkan forecast result memiliki model/data version. 

---

# 18. Dataset Version

Sama pentingnya:

```text
DatasetVersion
├── id
├── version
├── coverage_start
├── coverage_end
├── feature_schema
├── source_manifest
├── preprocessing_version
└── leakage_audit_status
```

Ini penting karena angka final tidak boleh berdiri tanpa reproducibility metadata. Implementation Plan mewajibkan dataset version, preprocessing version, split protocol, model config, seed, metric implementation, experiment ID, dan artifact/result file. 

---

# 19. Relasi Domain Utama

Sekarang semuanya bisa dirangkai:

```text id="3bffm4"
                 COMMODITY
                     │
               ┌─────┴─────┐
               │           │
               ▼           ▼
            MARKET   SUPPLIER REGION
               │           │
               ▼           │
          PRICE HISTORY     │
               │            │
               └──────┬─────┘
                      ▼
                FORECAST RUN
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
   FORECAST       CONTEXT      METADATA
     POINTS           │       Model Version
                      │       Dataset Version
           ┌──────────┼───────────┐
           ▼          ▼           ▼
        Climate      News     Macro/Logistics
        /Supply     /Sentiment
```

Dan di luar domain forecasting:

```text
Commodity
   │
   └── Education Content

Research
   ├── Model
   ├── Methodology
   ├── Experiment
   ├── Benchmark
   ├── Ablation
   └── Limitations
```

---

# 20. Canonical Domain Model

Kalau kita sederhanakan menjadi core:

```text
                    ┌─────────────┐
                    │  Commodity  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Market   │
                    └──────┬──────┘
                           │
                ┌──────────▼──────────┐
                │  Price Observation  │
                └──────────┬──────────┘
                           │
                     Historical
                           │
                           ▼
                   ┌──────────────┐
                   │ Forecast Run │
                   └──────┬───────┘
                          │
            ┌─────────────┼──────────────┐
            ▼             ▼              ▼
     Forecast Points   Context       Metadata
                       │
        ┌──────────────┼───────────────┐
        ▼              ▼               ▼
     Climate          News        Macro/Logistics
     Supply         Sentiment
```

Ini menurut saya cukup stabil untuk menjadi dasar engineering.

---

# 21. Sekarang masuk ke Information Architecture

Setelah domain object jelas, kita bisa membangun IA.

Saya menyarankan jangan mengikuti pipeline research secara mentah.

Public navigation:

```text
ARIF FOOD INTELLIGENCE

├── Harga Pangan
├── Forecast
├── Konteks
├── Edukasi
└── Research
```

---

# 22. Struktur route yang saya usulkan

```text
/
├── /prices
│
├── /commodities
│   ├── /commodities/[slug]
│   └── /commodities/[slug]/forecast
│
├── /forecast
│
├── /context
│   ├── /context/climate
│   ├── /context/news
│   └── /context/macro-logistics
│
├── /monitoring
│
├── /learn
│   ├── /learn/food-price
│   ├── /learn/commodities
│   ├── /learn/forecasting
│   └── /learn/data
│
└── /research
    ├── /research/model
    ├── /research/methodology
    ├── /research/data
    ├── /research/experiments
    ├── /research/benchmark
    ├── /research/ablation
    └── /research/limitations
```

Ini merupakan evolusi dari route awal dalam Implementation Plan yang sebelumnya memisahkan forecast, price analysis, sentiment, climate, macro, monitoring, model, research, dan experiments. 

---

# 23. Namun saya tidak ingin semuanya muncul di navbar

Navbar publik jangan terlalu berat.

Saya lebih menyarankan:

```text
Logo

Harga Pangan
Forecast
Konteks
Edukasi
Research
```

Kemudian:

```text
Search
Commodity selector
```

dan bagian lain berada di contextual navigation.

---

# 24. Home

Home bukan dashboard penuh.

Fungsinya:

> **“Orient user terhadap kondisi pangan dan mengarahkan mereka ke informasi yang dicari.”**

Struktur:

```text
Hero
 ↓
Price Snapshot
 ↓
Featured Commodities
 ↓
Recent Movement
 ↓
Forecast Snapshot
 ↓
Market Context
 ↓
Education / Data Story
 ↓
Research teaser
```

---

# 25. `/prices`

Tujuan:

> “Saya hanya ingin melihat harga.”

Isi:

```text
Commodity filters
Market filters

Current price
Daily change
7D change
30D change

Historical trend
```

Ini membuat produk berguna bahkan tanpa forecasting.

---

# 26. `/commodities/[slug]`

Ini akan menjadi **halaman paling penting**.

Contoh:

```text
/commodities/cabai-merah-keriting
```

Struktur:

```text
Commodity Header
      ↓
Current Market Price
      ↓
Historical Trend
      ↓
Recent Movement
      ↓
Forecast
      ↓
Market Context
      ↓
Extreme Movement
      ↓
Learn about this commodity
```

Dengan kata lain:

> **Commodity Intelligence Page**

Ini adalah pusat integrasi seluruh domain.

---

# 27. `/commodities/[slug]/forecast`

Untuk pengguna yang memang datang karena forecast.

```text
Forecast Origin
Market
Horizon

Current Price
Forecast Movement
Reconstructed Price

Forecast Trajectory

Forecast Context
├── Climate
├── Supply
├── News
├── Macro
└── Logistics

Forecast Metadata
├── Cutoff
├── Model Version
└── Dataset Version
```

---

# 28. `/context`

Ini untuk pengguna yang ingin mengeksplorasi **kenapa informasi tersebut relevan sebagai context**, bukan untuk membuat causal claim.

Subsection:

```text
Climate & Supply
News & Sentiment
Macro & Logistics
```

Data modality memang menjadi bagian scope external ARIF-Net. 

---

# 29. `/monitoring`

Fokus:

```text
Extreme Movement
Historical Movement
Current Regime
```

Bukan:

```text
BUY
SELL
CRASH
PANIC
```

Karena shock tetap secondary phenomenon dan bukan primary classification task. 

---

# 30. `/learn`

Ini adalah perluasan publik yang kita sepakati.

Struktur:

```text
Learn
│
├── Apa Itu Harga Pangan?
├── Mengenal Komoditas
├── Membaca Pergerakan Harga
├── Apa Itu Forecast?
├── Bagaimana ARIF-Net Bekerja?
└── Memahami Data Multimodal
```

Dan kontennya bisa terhubung langsung ke halaman commodity.

Contoh:

> “Apa arti kenaikan 5%?”

→ link ke Price Literacy.

> “Mengapa forecast 7D berbeda dengan 30D?”

→ link ke Forecast Literacy.

---

# 31. `/research`

Ini menjadi **deep information layer**.

```text
Research
│
├── Overview
├── ARIF-Net Model
├── Research Problem
├── Data & Pipeline
├── Methodology
├── Experiments
├── Benchmark
├── Ablation
└── Limitations
```

Pengunjung biasa tidak diwajibkan masuk sini.

Evaluator akademik dapat langsung masuk.

---

# 32. Public Experience vs Research Experience

Ini akhirnya menjadi sangat jelas:

```text
                    ARIF FOOD INTELLIGENCE
                              │
              ┌───────────────┴───────────────┐
              │                               │
        PUBLIC EXPERIENCE               RESEARCH EXPERIENCE
              │                               │
       Prices / Commodity                Methodology
       Forecast                          Model
       Context                           Data
       Monitoring                        Experiments
       Education                         Benchmark
                                         Ablation
                                         Limitations
```

Tetapi keduanya memakai domain/data yang sama.

---

# 33. Shared object = Commodity

Contohnya:

Public:

```text
Cabai Merah Keriting
→ Rp42.500
→ Trend
→ Forecast
```

Academic:

```text
Cabai Merah Keriting
→ Price Dataset
→ Climate
→ News
→ Macro
→ Forecast
→ Experiment
```

Jadi **bukan dua produk**.

---

# 34. Information hierarchy

Kita dapat mendefinisikan depth:

### Level 1 — Public

```text
Harga
Trend
Forecast
```

### Level 2 — Intelligence

```text
Context
Movement
Multi-Horizon
```

### Level 3 — Explanation

```text
Why this context?
How forecast is produced?
```

### Level 4 — Evidence

```text
Model
Experiment
Benchmark
Ablation
```

### Level 5 — Technical

```text
Dataset
Pipeline
Version
Limitations
```

Ini akan sangat membantu nanti dalam UX karena pengguna tidak dibombardir dengan technical detail.

---

# 35. Important: Data model vs UI model

Kita jangan membuat kesalahan:

```text
Database entity
=
Page
```

Tidak selalu begitu.

Contoh:

```text
Climate
Supply
News
Macro
Logistics
```

secara domain bisa entity/stream terpisah.

Tetapi UI:

```text
Market Context
```

bisa menjadi satu experience.

Sebaliknya:

```text
ForecastRun
ForecastPoint
ModelVersion
DatasetVersion
```

secara backend terpisah, tapi UI:

```text
Forecast Card
```

bisa menjadi satu component.

---

# 36. Canonical URL strategy

Saya sarankan URL publik berorientasi **resource**, bukan aktivitas.

Lebih natural:

```text
/commodities/cabai-merah-keriting
```

daripada:

```text
/forecast-cabai
```

Karena commodity merupakan object utama.

Sedangkan:

```text
/commodities/cabai-merah-keriting/forecast
```

merupakan view khusus dari commodity tersebut.

---

# 37. IA final sementara

```text
ARIF FOOD INTELLIGENCE
│
├── HOME
│
├── PRICES
│   └── Price Explorer
│
├── COMMODITIES
│   ├── Commodity Index
│   └── Commodity Intelligence
│
├── FORECAST
│   └── Forecast Explorer
│
├── CONTEXT
│   ├── Climate & Supply
│   ├── News & Sentiment
│   └── Macro & Logistics
│
├── MONITORING
│   └── Extreme Movement
│
├── LEARN
│   ├── Food Price Literacy
│   ├── Commodity Education
│   ├── Forecast Literacy
│   └── Data Stories
│
└── RESEARCH
    ├── Model
    ├── Methodology
    ├── Data
    ├── Experiments
    ├── Benchmark
    ├── Ablation
    └── Limitations
```

---

# 38. Hal yang sudah mulai bisa kita kunci secara konseptual

### Research-derived

```text
Commodity
Market
Price
Forecast
Context
Model
Dataset
Experiment
```

### Product-derived

```text
Commodity Intelligence
Price Explorer
Education
Data Story
Public Monitoring
```

### Cross-cutting

```text
Source
Provenance
Cutoff
Version
Limitations
```

---

# 39. Domain + Experience dalam satu diagram

```text
                           ARIF FOOD INTELLIGENCE
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
              INFORM              EXPLORE             LEARN
                │                   │                   │
             PRICE              FORECAST            EDUCATION
                │                   │                   │
          ┌─────┴─────┐       ┌─────┴──────┐       ┌────┴─────┐
          │           │       │            │       │          │
       Current      History  Movement    Context  Literacy  Data Story
          │           │       │            │
          └─────┬─────┘       └─────┬──────┘
                │                   │
                └─────────┬─────────┘
                          ▼
                    COMMODITY
                          │
                          ▼
                    ARIF-NET ENGINE
                          │
                          ▼
                      RESEARCH
                          │
                 ┌────────┼────────┐
                 ▼        ▼        ▼
              Model   Experiment Evidence
```

---

# 40. STEP 05 menghasilkan satu fondasi penting

Setelah tahap ini, kita sudah dapat membedakan:

```text
WHAT EXISTS IN THE DOMAIN
            ↓
Commodity
Market
Price
Context
Forecast
Research Artifact
            ↓
HOW USERS EXPERIENCE IT
            ↓
Prices
Commodity
Forecast
Context
Learn
Research
```

Ini penting karena mulai sekarang **PRD tidak lagi ditulis sebagai daftar fitur acak**.

PRD dapat ditulis berdasarkan:

```text
Domain
→ User intent
→ Capability
→ Feature
→ Data
→ API
→ UI
```