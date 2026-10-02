# STEP 01 — ARIF Food Intelligence Product Scope Map V.0.1

## 1. Product Identity

### Product

**ARIF Food Intelligence**

### Product category — PROPOSED

> **Public Food Price Information, Intelligence, and Forecasting Platform**

Dalam Bahasa Indonesia:

> **Platform informasi, literasi, dan forecasting harga pangan berbasis data multimodal.**

Ini merupakan perluasan dari product vision yang sudah ada, bukan perubahan terhadap research goal.

Research tetap:

```text
ARIF-Net
→ Multimodal Regression Forecasting
→ Relative Price Movement
```

Product menjadi:

```text
ARIF Food Intelligence
→ Information
→ Exploration
→ Forecasting
→ Context
→ Education
→ Research Evidence
```

---

# 2. Product Mission

### PROPOSED

> **Menyediakan informasi harga pangan yang mudah dipahami dan dapat dieksplorasi publik, sekaligus menghadirkan forecast dan konteks multimodal dari ARIF-Net sebagai lapisan intelligence untuk membantu pengguna memahami perkembangan harga pangan.**

Jadi produk tidak hanya menjawab:

> “Berapa harga pangan?”

tetapi juga:

> “Bagaimana pergerakannya?”

> “Bagaimana kemungkinan pergerakannya ke depan berdasarkan model?”

> “Informasi apa yang tersedia ketika forecast dibuat?”

> “Apa yang dapat dipelajari dari dinamika harga tersebut?”

Ini masih sangat dekat dengan Product Vision existing: `Data → Context → Forecast → Explanation → Evidence`. 

---

# 3. Masalah Produk yang Hendak Diselesaikan

Menurut saya kita perlu memisahkan **research problem** dan **product problem**.

## Research problem

Sudah cukup jelas dan `LOCKED`:

> Historical price tidak selalu menangkap external context; external modalities bersifat heterogen dan memiliki waktu ketersediaan berbeda; ARIF-Net menguji apakah integrasi tersebut memberi predictive gain yang terukur. 

## Product problem — PROPOSED

Masalah yang ingin disentuh oleh aplikasi:

### P1 — Informasi harga pangan sulit dipahami sebagai satu kesatuan

Pengguna bisa menemukan harga, berita, cuaca, dan informasi ekonomi secara terpisah. Produk ingin menyediakan **satu ruang eksplorasi**.

### P2 — Informasi harga sering berhenti pada angka

Harga tanpa historical trend, movement, dan context membuat pengguna hanya mengetahui **nilai**, bukan **pergerakan**.

### P3 — Forecast sering ditampilkan tanpa konteks

Produk ingin menghubungkan forecast dengan informasi multimodal yang memang tersedia pada forecast cutoff.

### P4 — Masyarakat membutuhkan media literasi data pangan

Produk dapat menjadi sarana edukasi tentang:

```text
harga
→ trend
→ volatility
→ supply
→ climate
→ news
→ logistics
→ forecasting
```

### P5 — Hasil penelitian sulit dipahami oleh non-peneliti

ARIF-Net mempunyai pipeline kompleks. Produk menerjemahkannya ke bentuk visual yang dapat dipahami publik.

P5 ini sangat konsisten dengan target exhibition Anda: visitor seharusnya dapat memahami problem → model → forecast → context → evidence → limitations tanpa membaca thesis terlebih dahulu. 

---

# 4. Target Stakeholder

Saya sarankan kita belum menyebut semuanya sebagai “primary user”. Kita bedakan **Target User** dan **Supporting Stakeholder**.

## A. Target Users — PROPOSED

| User                    | Kebutuhan utama                                      |
| ----------------------- | ---------------------------------------------------- |
| **Masyarakat umum**     | Mengetahui dan memahami harga pangan                 |
| **Konsumen**            | Melihat perkembangan harga komoditas yang dikonsumsi |
| **Petani / produsen**   | Melihat perkembangan harga pada pasar referensi      |
| **Pelajar / mahasiswa** | Belajar dinamika harga pangan dan forecasting        |

## B. Supporting Stakeholders — PROPOSED

| Stakeholder                       | Kepentingan                              |
| --------------------------------- | ---------------------------------------- |
| **Researcher / Project Owner**    | Menyajikan hasil model                   |
| **Dosen / Evaluator**             | Memeriksa metodologi dan evidence        |
| **Academic / Research Community** | Memahami pendekatan dan hasil eksperimen |
| **Pengelola sistem**              | Menjaga data, model, API, dan artefak    |

Yang penting: kita **belum** menjadikan pemerintah, pedagang besar, distributor, investor, maupun lembaga kebijakan sebagai target utama karena product scope saat ini tidak mencakup automatic government decision system maupun policy intervention modeling. 

---

# 5. Persona → Problem → Need → Product Value

Ini versi yang lebih operasional.

| Persona             | Problem                                                | Need                                         | Product Value              |
| ------------------- | ------------------------------------------------------ | -------------------------------------------- | -------------------------- |
| **Masyarakat**      | Tidak tahu perkembangan harga pangan                   | Informasi sederhana dan aktual               | Price information + trend  |
| **Konsumen**        | Hanya mengetahui harga ketika membeli                  | Memahami perubahan harga dari waktu ke waktu | Commodity explorer         |
| **Petani/Produsen** | Sulit melihat gambaran perkembangan harga pasar tujuan | Market reference & trend                     | Price + forecast + context |
| **Pelajar**         | Sulit memahami hubungan data dan forecasting           | Media belajar berbasis data nyata            | Education + data story     |
| **Dosen/Evaluator** | Model penelitian terlalu teknis untuk dipahami cepat   | Transparansi metodologi                      | Model + evidence           |
| **Researcher**      | Hasil eksperimen tersebar di artefak penelitian        | Satu public research interface               | Research center            |

Perlu dicatat bahwa untuk petani/produsen, produk saat ini lebih tepat menyajikan **harga pasar referensi**. Belum tepat menyebutnya sebagai harga jual petani atau farm-gate price karena itu belum menjadi bagian dari kontrak data penelitian.

---

# 6. Product Scope Matrix

Sekarang bagian terpentingnya.

| Product Domain        | Fitur                      | Sumber                 | Hubungan dengan Model         | Scope          |
| --------------------- | -------------------------- | ---------------------- | ----------------------------- | -------------- |
| **Price Information** | Current price              | Price dataset          | Input/backbone                | **CORE**       |
|                       | Historical price           | Price dataset          | Input                         | **CORE**       |
|                       | Price trend                | Derived price data     | Input analysis                | **CORE**       |
|                       | Volatility                 | Derived price data     | Input analysis                | **CORE**       |
| **Forecasting**       | Forecast movement          | ARIF-Net               | Direct model output           | **CORE**       |
|                       | Reconstructed price        | ARIF-Net output        | Derived model output          | **CORE**       |
|                       | Multi-horizon forecast     | ARIF-Net               | Direct model output           | **CORE**       |
| **Context**           | Climate                    | Climate data           | Model modality                | **CORE**       |
|                       | Supply                     | Supply data            | Model modality                | **CORE**       |
|                       | News                       | News data              | Model modality                | **CORE**       |
|                       | Sentiment                  | NLP pipeline           | Model modality                | **CORE**       |
|                       | Macro                      | Macro data             | Model modality                | **CORE**       |
|                       | Logistics                  | Logistics/BBM          | Model modality                | **CORE**       |
|                       | Calendar                   | Calendar data          | Supporting modality           | **CORE**       |
| **Monitoring**        | Extreme movement           | Model/evaluation       | Secondary research capability | **SUPPORTING** |
|                       | Historical extreme periods | Price data             | Secondary analysis            | **SUPPORTING** |
| **Education**         | Commodity information      | Product content        | Outside model                 | **SUPPORTING** |
|                       | Price literacy             | Product content        | Outside model                 | **SUPPORTING** |
|                       | Forecast literacy          | Product content        | Uses model                    | **SUPPORTING** |
|                       | Data stories               | Data + context         | Product interpretation        | **SUPPORTING** |
| **Research**          | Methodology                | Research artifacts     | Model documentation           | **SUPPORTING** |
|                       | Architecture               | Research artifacts     | Model                         | **SUPPORTING** |
|                       | Benchmark                  | Experiment artifacts   | Model evidence                | **SUPPORTING** |
|                       | Ablation                   | Experiment artifacts   | Model evidence                | **SUPPORTING** |
|                       | Limitations                | Research documentation | Governance                    | **SUPPORTING** |
| **Platform**          | Data provenance            | Research metadata      | Indirect                      | **SUPPORTING** |
|                       | Model version              | Artifact registry      | Direct                        | **REQUIRED**   |
|                       | Dataset version            | Artifact registry      | Direct                        | **REQUIRED**   |
|                       | Forecast cutoff            | Temporal contract      | Direct                        | **REQUIRED**   |

Functional baseline existing juga sudah menetapkan current/historical price, period selection, forecast, reconstructed price, movement, volatility, climate, sentiment/news, macro/logistics, methodology, benchmark/ablation, dan model/data version. 

---

# 7. Tiga Lapisan Produk

Setelah scope map ini, saya rasa struktur produknya bisa kita definisikan menjadi tiga layer.

## Layer 1 — PUBLIC INFORMATION

**Tujuan:** membuat website berguna bahkan tanpa memakai forecasting.

```text
Harga Pangan
Komoditas
Histori
Trend
Informasi pasar
Edukasi
```

Ini menjawab kebutuhan masyarakat, konsumen, dan public literacy.

---

## Layer 2 — FOOD INTELLIGENCE

**Tujuan:** memberikan intelligence yang berasal dari ARIF-Net.

```text
Forecast
Movement
Multi-Horizon
Climate Context
Supply Context
News/Sentiment
Macro/Logistics
Extreme Movement
```

Ini merupakan pusat nilai tambah penelitian.

---

## Layer 3 — RESEARCH & EVIDENCE

**Tujuan:** menjadikan produk sebagai demonstrator akademik.

```text
Methodology
Architecture
Data
Experiments
Benchmark
Ablation
Model Version
Dataset Version
Limitations
```

Dengan struktur ini kita tidak memaksa masyarakat melihat interface penelitian, dan tidak memaksa evaluator menggunakan interface publik untuk mencari evidence.

---

# 8. Feature Boundary

Agar scope tidak liar, saya sarankan kita tetapkan tiga status.

## IN SCOPE — v1

```text
✓ Commodity information
✓ Current price
✓ Historical price
✓ Trend
✓ Multi-horizon forecast
✓ Forecast movement
✓ Reconstructed estimated price
✓ Climate context
✓ Supply context
✓ News/sentiment context
✓ Macro/logistics context
✓ Extreme movement monitoring
✓ Education
✓ Methodology
✓ Research evidence
✓ Data/model provenance
```

## FUTURE — bukan MVP

```text
? Weather forecast integration
? User personalization
? Notifications
? Additional commodities
? Additional markets
? More advanced uncertainty
? Scenario exploration
? Farmer-specific analytics
? Mobile application
```

Beberapa item tersebut membutuhkan data/metodologi tambahan sehingga belum layak diperlakukan sebagai bagian final.

## OUT OF SCOPE

```text
✗ Trading recommendation
✗ Buy/sell recommendation
✗ Automatic farmer profit optimization
✗ Causal policy simulator
✗ Automatic government recommendation
✗ Economic equilibrium simulator
✗ Guaranteed future price
✗ National-scale forecasting claim
```

Batas ini konsisten dengan batasan research contract saat ini. 

---

# 9. Khusus fitur untuk petani

Menurut saya ini perlu kita definisikan dengan hati-hati karena ide Anda bagus, tetapi mudah membuat klaim produk terlalu jauh.

### Yang bisa kita tawarkan sekarang

```text
Petani memilih:
Cabai Merah Keriting

↓
Lihat market reference:
PIKJ

↓
Current price

↓
Historical trend

↓
Recent movement

↓
Forecast

↓
Climate/supply context
```

Sehingga pertanyaan yang dijawab adalah:

> **“Bagaimana perkembangan harga komoditas saya pada pasar referensi?”**

Bukan:

> “Berapa harga yang harus saya jual?”

dan bukan:

> “Berapa keuntungan saya?”

Karena sistem belum memiliki model farm economics.

---

# 10. Khusus masyarakat/konsumen

Untuk mereka, kita tidak perlu memperlihatkan kompleksitas ARIF-Net.

Misalnya user membuka:

```text
HARGA PANGAN

Cabai Merah Keriting
Rp XX.XXX
↑ X.X%

Bawang Merah
Rp XX.XXX
↓ X.X%

Beras
Rp XX.XXX
→ X.X%
```

Klik:

```text
Cabai
↓
Trend 7D
↓
Trend 30D
↓
Forecast
↓
"Pelajari konteks"
```

Jadi masyarakat bisa menggunakan platform sebagai **price information portal** tanpa harus memahami machine learning.

---

# 11. Khusus edukasi

Saya kira fitur edukasi tidak boleh berbentuk “blog yang terpisah”.

Lebih kuat kalau:

> **data menjadi media edukasi.**

Contoh:

```text
Kenapa harga cabai berubah?

[Grafik harga]
       ↓
[Perubahan supply]
       ↓
[Climate context]
       ↓
[News activity]
       ↓
[Logistics context]
       ↓
[Forecast]
```

Lalu ada:

> **Pelajari cara membaca grafik ini**

> **Apa arti forecast 7 hari?**

> **Mengapa forecast 30 hari bisa berbeda dengan forecast 7 hari?**

Ini sangat sesuai dengan karakter multimodal dan multi-horizon ARIF-Net.

---

# 12. Satu konsep produk yang menurut saya sangat penting

Saya ingin memperkenalkan satu konsep yang bisa menjadi dasar nanti:

# **Commodity Intelligence Page**

Artinya object utama produk bukan “model”.

Object utama:

> **Commodity**

Misalnya:

```text
/commodities/cabai-merah-keriting
```

Di dalamnya:

```text
Commodity Profile
       ↓
Current Price
       ↓
Historical Trend
       ↓
Forecast
       ↓
Market Context
       ↓
Climate / Supply
       ↓
News / Sentiment
       ↓
Macro / Logistics
       ↓
Extreme Movement
       ↓
Learn More
```

Model ada di belakangnya.

Ini membuat produk terasa seperti **platform pangan**, bukan seperti **website thesis**.

---

# 13. Domain Model awal

Dari scope tersebut, saya melihat model domain seperti:

```text
                    COMMODITY
                        │
            ┌───────────┼───────────┐
            ↓           ↓           ↓
         MARKET      PRICE       FORECAST
                        │           │
                    HISTORY       MOVEMENT
                        │           │
                     TREND     RECONSTRUCTED
                  VOLATILITY       PRICE
                                    │
                                    ↓
                              MULTI-HORIZON
                                    │
                       ┌────────────┼────────────┐
                       ↓            ↓            ↓
                    CLIMATE       NEWS         MACRO
                       │         SENTIMENT    LOGISTICS
                       │
                     SUPPLY
```

Ditambah:

```text
COMMODITY
   ↓
SUPPLIER REGIONS
```

karena supplier-region mapping memang merupakan bagian dari research framework. 

---

# 14. Hubungan Product Scope dengan Research Scope

Ini perlu kita jadikan aturan arsitektur sejak awal.

```text
                PRODUCT SCOPE
                     │
       ┌─────────────┼─────────────┐
       │             │             │
    Public       Intelligence    Research
    Layer           Layer         Layer
       │             │             │
       └─────────────┼─────────────┘
                     ↓
              RESEARCH ENGINE
                   ARIF-Net
```

Dengan aturan:

> **Product boleh lebih luas daripada model, tetapi product tidak boleh mengklaim sesuatu yang tidak didukung oleh data atau model.**

Contoh:

### Boleh

```text
Historical price explorer
```

karena berasal langsung dari data.

### Boleh

```text
Commodity education
```

karena itu product content.

### Boleh

```text
Forecast
```

karena merupakan model output.

### Tidak boleh

```text
"Petani harus menjual sekarang."
```

karena itu decision recommendation.

---

# 15. Product Value Proposition

### PROPOSED

Saya akan merumuskannya seperti ini:

> **ARIF Food Intelligence membantu pengguna memahami perkembangan harga pangan melalui satu platform yang menggabungkan informasi harga historis, tren, forecasting multi-horizon, serta konteks climate, supply, news, dan macro/logistics, disertai materi edukasi dan transparansi mengenai sumber data serta model yang digunakan.**

Versi lebih pendek:

> **“Lihat harga. Pahami pergerakannya. Jelajahi konteksnya.”**

Dan untuk layer research:

> **“From multimodal data to food price intelligence.”**

Keduanya masih proposal, bukan kalimat yang sudah dikunci.

---

# 16. Product Scope Map final sementara

Sehingga bentuk besarnya sekarang menjadi:

```text
                       ARIF FOOD INTELLIGENCE
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
     PUBLIC INFO          FOOD INTELLIGENCE      RESEARCH
          │                     │                     │
     Harga pangan           Forecast              Methodology
     Komoditas              Movement              Architecture
     Histori                 Multi-Horizon         Data
     Trend                   Context               Benchmark
     Edukasi                 Monitoring            Ablation
          │                     │                   Evidence
          └─────────────────────┼─────────────────────┘
                                │
                         ARIF-NET ENGINE
                                │
                     Multimodal Regression
                                │
       ┌────────────┬───────────┼───────────┬────────────┐
       ↓            ↓           ↓           ↓            ↓
     Price       Climate      News        Macro       Calendar
                /Supply     /Sentiment   /Logistics
```

---

# 17. Hal yang sudah dapat kita anggap cukup kuat

### `LOCKED / DECIDED` dari sisi research

Historical price sebagai backbone, supervised regression, relative price movement, reconstructed nominal price, multi-horizon sampai maksimum 365 hari, commodity scope, Jakarta target market, external modalities, temporal integrity, dan blind test sudah ditetapkan dalam Phase 0. 

### `EXISTING PRODUCT BASELINE`

Current/historical price, forecast, movement, reconstructed price, volatility, climate, news/sentiment, macro/logistics, methodology, benchmark/ablation, serta model/data version sudah tercantum dalam product baseline Implementation Plan. 

### `PROPOSED PRODUCT EXPANSION`

Yang baru kita tambahkan melalui diskusi ini:

```text
Public information layer
Consumer-oriented price exploration
Farmer/producer market-reference perspective
Food-price literacy
Commodity education
Data storytelling
Public-first experience
```

Ini **belum** menjadi keputusan metodologis Phase 0. Ini adalah perluasan product scope yang perlu kita formalize di tahap PRD nanti.

---

# 18. Maka STEP 01 bisa kita anggap selesai dengan satu keputusan konseptual

Saya rasa kita sekarang sudah punya batas yang jauh lebih jelas:

> **ARIF Food Intelligence bukan hanya “aplikasi hasil forecasting”.**

Struktur produknya adalah:

```text
                       ARIF FOOD INTELLIGENCE
                                │
      ┌─────────────────────────┼─────────────────────────┐
      │                         │                         │
      ▼                         ▼                         ▼
   INFORM                     UNDERSTAND                FORECAST
      │                         │                         │
  Harga pangan              Literasi data              ARIF-Net
  Histori                   Edukasi                    Movement
  Komoditas                 Context                    Multi-horizon
  Trend                     Data Story                 Prediction
      │                         │                         │
      └─────────────────────────┼─────────────────────────┘
                                ↓
                           EVIDENCE
                                ↓
                         Research Layer
```

Dengan demikian, **model adalah intelligence engine, bukan keseluruhan produk**.

Dan menurut saya ini justru membuat hubungan Capstone → TA menjadi rapi: model dapat terus berkembang pada research track, sementara product track dapat berkembang menjadi platform informasi yang semakin matang tanpa harus mengubah research goal. Dokumen Anda sendiri memang mengunci Capstone dan TA sebagai satu pipeline berkelanjutan. 