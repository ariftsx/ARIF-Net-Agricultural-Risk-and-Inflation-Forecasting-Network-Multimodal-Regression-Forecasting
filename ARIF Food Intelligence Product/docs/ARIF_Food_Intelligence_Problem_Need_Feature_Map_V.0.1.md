# STEP 03 — Problem → Need → Feature Map

## 1. Prinsip pemetaan

Kita jangan mulai dari:

> “Fitur apa yang bagus ditambahkan?”

Tetapi:

```text
USER PROBLEM
      ↓
USER NEED
      ↓
INFORMATION NEEDED
      ↓
PRODUCT CAPABILITY
      ↓
FEATURE
      ↓
DATA / MODEL SOURCE
```

Dengan begitu setiap fitur memiliki alasan keberadaan.

---

# 2. Problem Domain A — Masyarakat & Konsumen

## Masalah A1

Pengguna hanya melihat **angka harga**, tetapi sulit memahami apakah harga sedang naik, turun, stabil, atau mengalami perubahan yang relatif besar.

### Need

Pengguna membutuhkan cara sederhana untuk memahami **pergerakan harga**, bukan hanya nilai harga.

### Information

```text
Current Price
Previous Price
7D Change
30D Change
Historical Trend
Volatility Context
```

### Feature

**Price Overview**

**Historical Price Chart**

**Movement Indicator**

**Trend Summary**

**Volatility Context**

### Source

```text
Price Dataset
+
Derived Price Analytics
```

### Model dependency

**Tidak wajib bergantung pada ARIF-Net.**

Ini penting karena produk tetap berguna walaupun model sedang offline.

---

# 3. Problem A2

Masyarakat tidak selalu memahami apa arti perubahan harga pada periode yang berbeda.

Misalnya:

```text
+2% dalam 1 hari
vs
+2% dalam 30 hari
```

konteksnya berbeda.

### Need

Pengguna perlu melihat perubahan berdasarkan **time horizon**.

### Information

```text
1D
3D
7D
14D
30D
90D
```

dan untuk research-supported forecast:

```text
180D
365D
```

Phase 0 memang mendefinisikan multi-horizon forecasting dengan grid 1, 3, 7, 14, 30, 90, 180, dan 365 hari, dengan kelayakan data sebagai syarat implementasi tiap horizon. 

### Feature

**Horizon Comparison**

Contoh:

```text
7 Hari
+3.2%

30 Hari
+6.4%

90 Hari
...
```

### Source

```text
ARIF-Net
```

untuk forecast, sedangkan historical movement dapat dihitung dari price data.

---

# 4. Problem A3

Pengguna melihat forecast tetapi tidak tahu bahwa forecast tersebut merupakan **estimasi model**, bukan nilai aktual.

### Need

Mereka membutuhkan interpretasi forecast yang sederhana dan transparan.

### Feature

**Forecast Explanation**

Contoh:

> Forecast 7 hari menunjukkan estimasi perubahan relatif harga sebesar X%.

> Estimasi harga nominal direkonstruksi berdasarkan harga pada forecast origin.

Ini konsisten dengan target internal `r(t,h)` dan rekonstruksi `P̂(t+h)`. 

### Supporting feature

**Forecast disclaimer**

**Data cutoff**

**Model version**

**Dataset version**

---

# 5. Problem Domain B — Petani / Produsen

Di sini saya ingin lebih presisi daripada konsep awal “harga hasil panen”.

Data penelitian saat ini berfokus pada **target market Jakarta**, sementara wilayah produksi/supplier menjadi external context. Jadi produk sebaiknya tidak mengklaim farm-gate price. Phase 0 memang menetapkan Jakarta sebagai forecast market dan supplier regions sebagai konteks pemasok. 

## Masalah B1

Petani/produsen sulit mendapatkan gambaran perkembangan harga komoditas di pasar referensi secara historis.

### Need

**Market visibility**

### Information

```text
Commodity
Target Market
Current Price
Historical Price
Recent Movement
Forecast
```

### Feature

**Market Reference View**

Contoh:

```text
Cabai Merah Keriting
Market Reference: PIKJ

Current:
Rp XX.XXX

7D:
↑ X.X%

30D:
↑ X.X%

Forecast:
7D → ...
30D → ...
```

### Source

Price data + ARIF-Net forecast.

---

# 6. Problem B2

Petani tidak hanya membutuhkan harga, tetapi konteks yang berhubungan dengan wilayah pemasok.

### Need

**Supplier / production context**

### Information

Untuk komoditas tertentu:

```text
Supplier Region
Climate
Rainfall
Temperature
Supply signal
Logistics context
```

Phase 0 memang menyediakan framework supplier-region untuk menghubungkan external context dengan market Jakarta. 

### Feature

**Supplier Region Context**

Misalnya:

```text
Selected commodity
↓
Relevant supplier regions
↓
Climate overview
↓
Supply context
```

### Status

**Product capability + research-supported context**

Bukan fitur rekomendasi bisnis.

---

# 7. Yang tidak boleh kita simpulkan untuk petani

Contoh:

```text
Cuaca buruk
   ↓
Harga akan naik
   ↓
Petani harus menunda panen
```

Itu sudah mengubah predictive information menjadi decision/cause claim.

Research contract Anda secara eksplisit memisahkan prediction dengan causation. 

Jadi produk cukup mengatakan:

> **“Climate-related context yang tersedia pada wilayah pemasok ditampilkan sebagai bagian dari informasi yang digunakan dalam forecasting.”**

---

# 8. Problem Domain C — Food Price Literacy

Ini adalah perluasan product scope yang kita sepakati.

## Masalah C1

Masyarakat sering melihat harga pangan tanpa memahami bagaimana harga dapat berubah terhadap waktu dan konteks.

### Need

**Basic food-price literacy**

### Feature

**Price Literacy**

Isi dapat berupa:

```text
Apa itu harga komoditas?
Apa itu price movement?
Apa itu volatility?
Apa arti naik 5%?
Apa bedanya daily change dengan monthly change?
```

### Source

Product content.

### Model dependency

**Tidak bergantung pada model.**

Ini membuat produk tetap memiliki nilai edukasi.

---

# 9. Problem C2 — Sulit memahami kenapa model membutuhkan banyak informasi

Ini justru dapat menjadi fitur edukasi yang sangat unik.

### Need

Memahami:

> “Mengapa harga historis saja tidak selalu cukup?”

### Feature

**How Forecasting Works**

Visual:

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
Price Movement
```

Ini langsung berasal dari research framing ARIF-Net. 

---

# 10. Problem C3 — Pengguna tidak memahami peran masing-masing modality

### Need

Belajar dengan contoh data nyata.

### Feature

**Multimodal Context Explorer**

Misalnya:

```text
CLIMATE
Rainfall
Temperature

NEWS
Article Volume
Sentiment
Intensity

LOGISTICS
Fuel
Distance / Proxy
```

Phase 0 memang mendefinisikan candidate feature seperti rainfall, temperature, sentiment, volume, intensity, persistence, BBM, distance dan calendar. 

---

# 11. Problem Domain D — Research / Academic

## Masalah D1

Research workflow ARIF-Net kompleks dan sulit dipahami hanya dari hasil forecast.

### Need

**Transparency**

### Feature

**Model & Methodology**

Isi:

```text
Research Goal
Target Variable
Forecast Horizons
Modalities
Architecture
Temporal Alignment
Fusion
Inference
```

---

# 12. Problem D2

Orang tidak dapat mengetahui apakah angka yang tampil adalah hasil eksperimen yang benar-benar tervalidasi.

### Need

**Evidence traceability**

### Feature

**Research Evidence**

```text
Benchmark
Ablation
Metrics
Test Period
Dataset Version
Model Version
Experiment Version
```

Ini sangat sesuai dengan requirement product yang sudah ada untuk methodology, benchmark/ablation, dan model/data version. 

---

# 13. Problem D3

Forecast tanpa temporal provenance berpotensi disalahartikan.

### Need

Mengetahui:

> “Informasi apa yang tersedia ketika forecast dibuat?”

### Feature

**Forecast Data Cutoff**

Contoh:

```text
Forecast Origin
1 Oct 2026

Information available until
30 Sep 2026 18:00

Model
ARIF-Net vX.X

Dataset
ARIF-DATA vX.X
```

Ini merupakan fitur yang sangat penting karena temporal availability merupakan bagian fundamental dari research contract. 

---

# 14. Problem Domain E — Market Understanding

Sekarang kita masuk ke fitur yang menggabungkan semuanya.

## Masalah E1

User melihat banyak informasi tetapi tidak memiliki cara untuk melihat semuanya dalam satu konteks.

### Need

**Unified commodity view**

### Feature

# Commodity Intelligence Page

Ini menurut saya akan menjadi **object utama aplikasi**.

```text
Commodity
   ↓
Market
   ↓
Current Price
   ↓
Historical Trend
   ↓
Forecast
   ↓
Climate / Supply
   ↓
News / Sentiment
   ↓
Macro / Logistics
   ↓
Extreme Movement
   ↓
Education
```

Ini merupakan sintesis dari seluruh scope yang sudah kita sepakati, bukan fitur yang berdiri sendiri dari dokumen awal.

---

# 15. Problem Domain F — Extreme Movement

Research Anda tidak menjadikan shock sebagai primary target, tetapi tetap mempertahankannya sebagai secondary phenomenon. 

## Masalah F1

Periode perubahan ekstrem bisa berbeda karakteristiknya dari kondisi normal.

### Need

Mengetahui kapan market berada dalam kondisi movement yang tidak biasa.

### Feature

**Extreme Movement Monitor**

Contoh:

```text
Current Movement
+4.8%

Historical Regime
NORMAL / EXTREME

Recent Extreme Periods
●
●
●
```

Tetapi jangan beri label seperti:

> “Market akan crash.”

cukup:

> **“Current movement is within/above the historical extreme-movement threshold used for analysis.”**

---

# 16. Problem → Feature Master Map

Sekarang seluruh hasilnya bisa diringkas:

| Problem                                  | Need                       | Feature                  | Source                 | Model?          |
| ---------------------------------------- | -------------------------- | ------------------------ | ---------------------- | --------------- |
| Tidak memahami harga saat ini            | Current market information | Current Price            | Price data             | No              |
| Tidak memahami perubahan                 | Trend visibility           | Historical Trend         | Price data             | No              |
| Tidak memahami volatility                | Movement context           | Volatility               | Derived price          | No              |
| Ingin melihat kemungkinan berikutnya     | Forecast                   | Forecast Explorer        | ARIF-Net               | **Yes**         |
| Ingin memahami horizon berbeda           | Multi-horizon view         | Horizon Selector         | ARIF-Net               | **Yes**         |
| Ingin memahami konteks forecast          | Multimodal context         | Context Panel            | Multiple modalities    | **Yes/Partial** |
| Petani ingin melihat pasar referensi     | Market visibility          | Market Reference         | Price data             | No              |
| Petani ingin memahami supplier context   | Production context         | Supplier Context         | Climate/Supply         | Partial         |
| Masyarakat ingin belajar                 | Literacy                   | Education                | Product content        | No              |
| Mahasiswa ingin belajar model            | Research literacy          | How It Works             | Research docs          | No              |
| User ingin tahu konteks berita           | Information context        | News Explorer            | News                   | Model modality  |
| User ingin memahami climate              | Climate context            | Climate Explorer         | Climate                | Model modality  |
| User ingin memahami macro/logistics      | Economic/logistics context | Macro/Logistics Explorer | External data          | Model modality  |
| User ingin memahami extreme movement     | Monitoring                 | Extreme Movement Monitor | Price/model evaluation | Secondary       |
| Dosen ingin memeriksa metode             | Transparency               | Methodology              | Research artifact      | No              |
| Dosen ingin memeriksa evidence           | Validation                 | Benchmark/Ablation       | Experiment artifact    | No              |
| Semua user perlu tahu validitas forecast | Provenance                 | Cutoff/Version           | Metadata               | **Required**    |

---

# 17. Dari sini saya melihat 6 Product Capability utama

Kita bisa berhenti berpikir dalam bentuk puluhan fitur kecil.

ARIF Food Intelligence pada dasarnya memiliki:

### 01 — PRICE

```text
Current Price
Historical Price
Trend
Volatility
Movement
```

### 02 — FORECAST

```text
Forecast
Multi-Horizon
Relative Movement
Reconstructed Price
Trajectory
```

### 03 — CONTEXT

```text
Climate
Supply
News
Sentiment
Macro
Logistics
Calendar
```

### 04 — MONITORING

```text
Extreme Movement
Historical Regime
Movement Analysis
```

### 05 — LEARNING

```text
Commodity Education
Food Price Literacy
Forecast Literacy
Data Stories
```

### 06 — RESEARCH

```text
Methodology
Architecture
Pipeline
Benchmark
Ablation
Evidence
Limitations
```

---

# 18. Tetapi ada satu lapisan tambahan yang harus selalu ada

## TRUST / TRANSPARENCY

Ini bukan halaman sendiri.

Ia menjadi **cross-cutting capability**.

Setiap forecast harus memiliki:

```text
Data Cutoff
Model Version
Dataset Version
Available Horizon
Data Availability
Source
```

Mengapa?

Karena research contract mengharuskan inference dan product menggunakan preprocessing contract yang sama, menangani missing modality secara eksplisit, serta tidak menghasilkan angka tanpa model version. 

Jadi:

```text
TRUST
 ├── Provenance
 ├── Versioning
 ├── Cutoff
 ├── Limitations
 └── Source
```

berada di seluruh sistem.

---

# 19. Sekarang kita bisa membedakan 4 jenis fitur

Ini akan sangat membantu ketika nanti kita membuat PRD.

## Type A — Research Output

Langsung berasal dari ARIF-Net:

```text
Forecast
Relative Movement
Multi-Horizon
Reconstructed Price
Model Attribution
```

## Type B — Research Context

Data/modality yang digunakan atau berkaitan dengan model:

```text
Climate
Supply
News
Sentiment
Macro
Logistics
Calendar
```

## Type C — Product Intelligence

Feature yang dibuat untuk membuat data lebih mudah digunakan:

```text
Trend
Commodity Explorer
Market Reference
Extreme Monitoring
Data Story
```

## Type D — Educational Product

Fitur khusus literasi:

```text
Price Literacy
Commodity Education
Forecast Explanation
How ARIF-Net Works
```

Pembagian ini sangat penting karena **tidak semua fitur harus menunggu Phase 1 model selesai**.

---

# 20. Dengan pembagian ini, produk bisa dikerjakan paralel

Kita sekarang dapat membentuk:

```text
                 PRODUCT DEVELOPMENT
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
     READY            PARALLEL          WAIT MODEL
       │                 │                 │
 Price Explorer     Education         Forecast Engine
 Commodity Page     Data Stories       ARIF-Net Adapter
 Historical Chart   Methodology        Inference
 Trend              Research UI
```

Jadi sambil Phase 1 berjalan, Anda sudah dapat membangun:

```text
✓ Home
✓ Commodity Explorer
✓ Historical Price
✓ Trend
✓ Education
✓ Methodology
✓ Research
✓ UI shell
✓ API contract
✓ Mock data layer
```

Kemudian ketika model siap:

```text
ARIF-Net
   ↓
Inference Contract
   ↓
Forecast API
   ↓
Forecast Explorer
```

---

# 21. MVP yang mulai terlihat

Berdasarkan mapping ini, saya tidak akan memasukkan semua capability sekaligus ke MVP.

### MVP Core

```text id="5y7w0f"
HOME
   ↓
COMMODITY
   ↓
CURRENT PRICE
   ↓
HISTORICAL TREND
   ↓
FORECAST
   ↓
CONTEXT
```

### MVP Supporting

```text
Education
Methodology
Data/Model metadata
Limitations
```

### Research showcase

```text
Benchmark
Ablation
Experiment Evidence
```

### Monitoring

```text
Extreme Movement
```

Jadi aplikasi tetap punya utility publik sekaligus tetap mampu menjadi demonstrator penelitian.

---

# 22. Diagram besar Product Scope setelah STEP 03

```text
                         ARIF FOOD INTELLIGENCE
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
            PRICE              FORECAST             CONTEXT
              │                   │                   │
       Current Price         Movement             Climate
       Historical            Multi-Horizon        Supply
       Trend                 Reconstructed        News
       Volatility            Price                Sentiment
                             Trajectory           Macro
                                                  Logistics
                                  │
                                  │
              ┌───────────────────┼───────────────────┐
              │                                       │
              ▼                                       ▼
          MONITORING                              LEARNING
              │                                       │
       Extreme Movement                      Price Literacy
       Market Regime                         Commodity Education
                                             Forecast Literacy
                                             Data Stories
              │                                       │
              └───────────────────┬───────────────────┘
                                  ▼
                              RESEARCH
                                  │
                         Methodology
                         Architecture
                         Experiments
                         Benchmark
                         Ablation
                         Limitations
                                  │
                                  ▼
                            ARIF-NET ENGINE
```

---

# 23. Hasil penting dari STEP 03

Ada satu insight yang menurut saya sekarang menjadi cukup jelas:

> **Fitur utama ARIF Food Intelligence bukan “Forecast”. Fitur utamanya adalah “Commodity Intelligence”, sedangkan Forecast adalah salah satu intelligence capability di dalamnya.**

Sehingga:

```text
Commodity
   ├── Price
   ├── Trend
   ├── Forecast
   ├── Context
   ├── Monitoring
   └── Learning
```

Ini membuat produk jauh lebih natural untuk publik.

Masyarakat tidak berpikir:

> “Saya ingin menggunakan model multimodal regression.”

Mereka berpikir:

> “Saya ingin tahu kondisi cabai.”

Dan aplikasi menjawab:

```text
Harga sekarang
↓
Trend
↓
Forecast
↓
Konteks
↓
Penjelasan
```

Sementara evaluator akademik dapat masuk lebih dalam:

```text
Forecast
↓
Model
↓
Architecture
↓
Experiment
↓
Ablation
↓
Evidence
```