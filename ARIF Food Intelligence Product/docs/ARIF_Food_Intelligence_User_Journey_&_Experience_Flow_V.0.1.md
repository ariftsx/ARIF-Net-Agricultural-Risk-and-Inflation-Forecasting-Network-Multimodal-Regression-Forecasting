# STEP 04 — User Journey & Experience Flow

## 1. Prinsip dasar journey

Saya menyarankan **satu produk, satu mental model, beberapa jalur penggunaan**.

Bukan:

```text
Masyarakat → Website A
Petani → Website B
Mahasiswa → Website C
```

Tetapi:

```text
                    ARIF FOOD INTELLIGENCE
                             │
                    Choose your intent
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
      INFORM               EXPLORE              LEARN
        │                    │                    │
     Harga                Forecast              Edukasi
     Trend                Context               Data story
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                          RESEARCH
                             │
                       Model / Evidence
```

Jadi **entry point pengguna bisa berbeda, tetapi domain datanya sama**.

---

# 2. Master Experience Flow

Saya usulkan master flow sebagai:

```text
LANDING
   ↓
DISCOVER COMMODITY
   ↓
UNDERSTAND CURRENT CONDITION
   ↓
EXPLORE PRICE HISTORY
   ↓
VIEW FORECAST
   ↓
EXPLORE CONTEXT
   ↓
INTERPRET
   ↓
EXPLORE EVIDENCE
```

Dalam bentuk product:

```text
Home
 ↓
Commodity
 ↓
Price
 ↓
Trend
 ↓
Forecast
 ↓
Context
 ↓
Explanation
 ↓
Evidence
```

Ini sebenarnya merupakan elaborasi dari core journey yang sudah ada di Implementation Plan. 

---

# 3. Journey A — Masyarakat Umum

## Intent

> “Saya ingin tahu kondisi harga pangan.”

### Flow

```text
Home
 ↓
Harga Pangan
 ↓
Pilih Komoditas
 ↓
Current Price
 ↓
Recent Movement
 ↓
Historical Trend
 ↓
Optional Forecast
 ↓
Simple Context
```

### Contoh pengalaman

User membuka:

> **Harga Pangan**

Melihat:

```text
Cabai Merah Keriting
Rp42.500/kg
↑ 3.2%

Bawang Merah
Rp38.000/kg
↓ 1.1%

Beras
Rp...
```

Klik cabai:

```text
Cabai Merah Keriting
PIKJ

Harga sekarang
Rp42.500

7 hari terakhir
+3.2%

30 hari terakhir
+7.1%

[ Lihat Forecast ]
```

User tidak perlu memahami ARIF-Net.

### Experience objective

> **Dari “berapa harganya?” menjadi “bagaimana pergerakannya?”**

---

# 4. Journey B — Konsumen

Intent:

> “Saya ingin memahami perubahan harga komoditas yang saya konsumsi.”

Flow:

```text
Home
 ↓
Commodity Explorer
 ↓
Commodity
 ↓
Current Price
 ↓
Historical Trend
 ↓
Movement
 ↓
Forecast
 ↓
Context
```

Perbedaan dengan masyarakat umum hanya pada **kedalaman eksplorasi**, bukan role aplikasi.

Karena itu saya tidak merekomendasikan akun `CONSUMER`.

---

# 5. Journey C — Petani / Produsen

Di sini kita harus mempertahankan terminologi **market reference**, bukan harga farm-gate.

Phase 0 menetapkan Jakarta sebagai forecast target market, sementara wilayah supplier/produksi dipakai sebagai external context. 

### Intent

> “Bagaimana perkembangan harga komoditas saya di pasar referensi?”

### Flow

```text
Home
 ↓
Komoditas
 ↓
Market Reference
 ↓
Current Market Price
 ↓
Historical Market Trend
 ↓
Recent Movement
 ↓
Forecast
 ↓
Supplier / Climate Context
```

### Pengalaman

```text
CABAI MERAH KERITING

Market Reference
PIKJ — DKI Jakarta

Current
Rp42.500/kg

Trend 30D
↑ 7.1%

Forecast
7D  +X.X%
30D +X.X%

Context
Cianjur
Bandung
Sumedang
...
```

Ini memungkinkan petani melihat **perkembangan market reference**, tanpa kita mengklaim:

```text
farm-gate price
profit
optimal selling price
optimal harvest time
```

---

# 6. Journey D — Pelajar / Mahasiswa

Ini adalah journey yang lebih eksploratif.

### Intent

> “Saya ingin memahami bagaimana harga pangan dipengaruhi berbagai informasi dan bagaimana forecasting dilakukan.”

### Flow

```text
Home
 ↓
Learn / Explore
 ↓
Komoditas
 ↓
Historical Price
 ↓
Climate Context
 ↓
News Context
 ↓
Macro / Logistics
 ↓
Forecast
 ↓
How ARIF-Net Works
 ↓
Research
```

### Experience pattern

User tidak hanya melihat:

> `Forecast = +5%`

tetapi bisa mengikuti:

```text
DATA
 ↓
CONTEXT
 ↓
FORECAST
 ↓
MODEL
```

Ini sangat sesuai dengan product purpose yang memang ingin menjelaskan data, context, forecast, explanation, dan evidence. 

---

# 7. Journey E — Dosen / Evaluator

### Intent

> “Saya ingin mengetahui bagaimana sistem ini dibuat dan bagaimana hasilnya diperoleh.”

### Flow

```text
Home
 ↓
Research
 ↓
Problem
 ↓
Research Goal
 ↓
Data
 ↓
Pipeline
 ↓
Architecture
 ↓
Model
 ↓
Experiment
 ↓
Benchmark
 ↓
Ablation
 ↓
Limitations
```

Ini **bukan** jalur utama public user.

Karena itu halaman Research sebaiknya dapat diakses dari global navigation, tetapi tidak mendominasi landing page.

---

# 8. Journey F — Researcher / Project Owner

Ini merupakan operational journey.

```text
Research/Admin
 ↓
Dataset
 ↓
Data Validation
 ↓
Model Version
 ↓
Experiment
 ↓
Inference Artifact
 ↓
Publish
 ↓
Public Product
```

Yang penting di sini:

```text
Research Artifact
      ↓
Validation
      ↓
Publishable Artifact
      ↓
Product
```

Bukan:

```text
Model
 ↓
langsung
 ↓
UI
```

Ini sesuai dengan separation of concerns pada Implementation Plan. 

---

# 9. Sekarang kita gabungkan menjadi satu journey architecture

```text
                             HOME
                               │
                    ┌──────────┼──────────┐
                    │          │          │
                    ▼          ▼          ▼
                 HARGA      FORECAST    EDUKASI
                    │          │          │
                    ▼          ▼          ▼
                COMMODITY   COMMODITY   DATA STORY
                    │          │          │
                    └────┬─────┴─────┬────┘
                         │           │
                         ▼           ▼
                       PRICE      CONTEXT
                         │           │
                         └─────┬─────┘
                               ▼
                           EXPLANATION
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
             PUBLIC VIEW               RESEARCH VIEW
                  │                         │
               Simple                  Deep Detail
                  │                         │
               Context                 Methodology
               Forecast                Experiment
                                         Evidence
```

Ini menurut saya sudah mulai menjadi **experience architecture**, bukan hanya sitemap.

---

# 10. Perjalanan inti yang harus menjadi “golden path”

Untuk demo dan penggunaan publik, saya menyarankan satu alur utama:

```text
HOME
 ↓
COMMODITY
 ↓
CURRENT PRICE
 ↓
PRICE HISTORY
 ↓
FORECAST
 ↓
WHY / CONTEXT
 ↓
EVIDENCE
```

Misalnya evaluator atau masyarakat hanya punya waktu satu menit:

### Step 1

**“Ini kondisi harga saat ini.”**

### Step 2

**“Ini bagaimana harganya bergerak.”**

### Step 3

**“Ini bagaimana model memperkirakan pergerakan selanjutnya.”**

### Step 4

**“Ini konteks yang tersedia ketika forecasting dilakukan.”**

### Step 5

**“Ini bagaimana model dan eksperimen dibangun.”**

### Step 6

**“Ini keterbatasannya.”**

Ini mempertahankan exhibition story yang memang sudah dirancang di Implementation Plan. 

---

# 11. Kita perlu membedakan “Navigation” dan “Journey”

Ini penting untuk desain nanti.

### Navigation

Apa saja yang tersedia:

```text
Harga
Forecast
Context
Monitoring
Edukasi
Research
```

### Journey

Apa yang dilakukan user:

```text
Harga
 ↓
Trend
 ↓
Forecast
 ↓
Context
 ↓
Explanation
```

Artinya user tidak harus mengikuti menu secara linear.

Misalnya:

```text
Homepage
→ Forecast
```

atau:

```text
Homepage
→ Harga Pangan
→ Cabai
→ Forecast
```

atau:

```text
Homepage
→ Edukasi
→ Mengapa harga berubah?
→ Commodity
```

---

# 12. Struktur navigasi yang mulai terlihat

Untuk produk publik saya menyarankan:

```text
ARIF Food Intelligence

[Harga Pangan]
[Forecast]
[Konteks]
[Edukasi]
[Research]
```

Sedangkan:

```text
[About]
```

atau informasi metodologi bisa berada di secondary navigation/footer.

---

# 13. Commodity Page menjadi pusat integrasi

Saya ingin menekankan ini karena hasil dari STEP 03 sekarang mengarah sangat jelas ke sini.

### `/commodity/[commodity]`

misalnya:

```text
Cabai Merah Keriting
```

Page tersebut menjadi:

```text
┌─────────────────────────────────────────┐
│ CABAI MERAH KERITING                    │
│ Market: PIKJ                            │
├─────────────────────────────────────────┤
│ CURRENT PRICE                           │
├─────────────────────────────────────────┤
│ PRICE TREND                             │
├─────────────────────────────────────────┤
│ FORECAST                                │
├─────────────────────────────────────────┤
│ MARKET CONTEXT                          │
│ Climate | Supply | News | Macro         │
├─────────────────────────────────────────┤
│ EXTREME MOVEMENT                        │
├─────────────────────────────────────────┤
│ LEARN ABOUT THIS COMMODITY              │
└─────────────────────────────────────────┘
```

Dengan ini halaman commodity menjadi **single source of user-facing truth** untuk kondisi komoditas.

---

# 14. Forecast tidak seharusnya menjadi halaman yang terisolasi

Karena forecast adalah hasil dari context.

Jadi:

```text
Commodity
      ↓
Forecast
      ↓
Forecast Context
```

bukan:

```text
Forecast
↓
Angka
↓
Selesai
```

Ketika user melihat:

```text
7D Forecast
+3.8%
Rp44.115
```

mereka harus bisa membuka:

> **“Lihat konteks forecast ini.”**

dan melihat:

```text
Data cutoff
Climate
News
Supply
Macro/Logistics
```

Dengan demikian produk mengimplementasikan konsep `Data → Context → Forecast → Explanation → Evidence`. 

---

# 15. Satu konsep UX yang sangat penting: Contextual Disclosure

Tidak semua informasi langsung ditampilkan.

Contoh:

```text
Forecast
+3.8%
```

↓

**Why this forecast?**

↓

```text
Historical price context
Climate context
News activity
Macro/logistics
```

↓

**How was this produced?**

↓

```text
Model
Architecture
Dataset
Experiment
```

Jadi user bisa berhenti kapan saja.

Ini membantu memenuhi dua target sekaligus:

```text
PUBLIC SIMPLICITY
        +
RESEARCH TRANSPARENCY
```

---

# 16. Journey untuk “Belajar”

Saya juga melihat Education tidak harus menjadi website terpisah.

Misalnya pada chart:

> **Tahukah Anda?**

> Perubahan harga 7 hari menunjukkan pergerakan kumulatif, sedangkan forecast 7 hari merupakan estimasi model dari forecast origin.

Kemudian:

**Learn more →**

masuk ke education.

Jadi:

```text
PRODUCT
   │
   ├── INFORMATION
   │
   ├── INTELLIGENCE
   │
   └── EDUCATION
```

bukan tiga aplikasi terpisah.

---

# 17. Journey untuk “Data Story”

Kita juga bisa membentuk entry point khusus:

```text
Edukasi
 ↓
Data Story
 ↓
"Perjalanan Harga Cabai"
 ↓
Historical
 ↓
Climate
 ↓
News
 ↓
Forecast
```

Namun **Data Story harus menggunakan data/artifact aktual**, bukan ilustrasi sintetis. Ini sangat penting karena Implementation Plan secara eksplisit melarang synthetic/hardcoded evidence digunakan sebagai research evidence. 

---

# 18. Journey Monitoring

Untuk extreme movement:

```text
Monitoring
 ↓
Commodity
 ↓
Historical Movement
 ↓
Extreme Period
 ↓
Context
 ↓
Forecast
```

Contohnya:

```text
EXTREME MOVEMENT
      ↓
"Periode ini memiliki relative movement
yang termasuk extreme menurut threshold
horizon yang digunakan."
      ↓
[Explore Context]
```

Bukan:

> “Harga akan shock.”

Ini mengikuti posisi shock sebagai secondary phenomenon. 

---

# 19. Journey comparison

Sekarang kita bisa melihat semua persona:

| Persona    | Entry             | Core Path                                    | End Goal           |
| ---------- | ----------------- | -------------------------------------------- | ------------------ |
| Masyarakat | Harga             | Price → Trend → Forecast                     | Memahami kondisi   |
| Konsumen   | Harga/Komoditas   | Price → Trend → Context                      | Memahami perubahan |
| Petani     | Komoditas         | Market → Trend → Forecast → Supplier context | Market visibility  |
| Pelajar    | Edukasi/Komoditas | Data → Context → Forecast → Learn            | Memahami konsep    |
| Dosen      | Research          | Problem → Model → Experiment → Evidence      | Evaluasi           |
| Researcher | Internal          | Data → Model → Experiment → Publish          | Operasionalisasi   |

---

# 20. Experience Architecture final sementara

```text
                         ARIF FOOD INTELLIGENCE
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                  INFORM        EXPLORE        LEARN
                    │             │             │
                  PRICE        FORECAST       EDUCATION
                    │             │             │
                  TREND         CONTEXT       DATA STORY
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                              EXPLAIN
                                  │
                         MODEL / METHODOLOGY
                                  │
                              EVIDENCE
                                  │
                        BENCHMARK / ABLATION
                                  │
                            LIMITATIONS
```

---

# 21. Satu perubahan penting dari sitemap awal

Implementation Plan sebelumnya mengusulkan route:

```text
/
 /forecast
 /analysis/price
 /analysis/sentiment
 /analysis/climate
 /analysis/macro
 /monitoring
 /model
 /research
 /experiments
```



Setelah STEP 01–04, saya melihat struktur **UX publik** sebaiknya tidak mengikuti struktur research pipeline secara mentah.

Lebih natural:

```text
/
├── /prices
├── /commodities/[slug]
├── /forecast
├── /context
├── /monitoring
├── /learn
└── /research
    ├── model
    ├── methodology
    ├── experiments
    └── evidence
```

Sedangkan:

```text
/analysis/climate
/analysis/sentiment
/analysis/macro
```

dapat menjadi **sub-view di dalam commodity/context**, bukan necessarily top-level navigation.

Ini proposal UX, bukan perubahan research contract.

---

# 22. Golden Product Journey

Saya akan jadikan ini sebagai alur yang nanti menjadi dasar PRD:

```text
                   USER ARRIVES
                        │
                        ▼
                WHAT COMMODITY?
                        │
                        ▼
                  CURRENT PRICE
                        │
                        ▼
                 WHAT'S THE TREND?
                        │
                        ▼
                WHAT'S NEXT?
                        │
                        ▼
                FORECAST MOVEMENT
                        │
                        ▼
              WHY / WHAT CONTEXT?
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Climate        News          Macro
       Supply       Sentiment      Logistics
          └─────────────┼─────────────┘
                        ▼
                  HOW IS IT MADE?
                        │
                        ▼
                     MODEL
                        │
                        ▼
                    EVIDENCE
                        │
                        ▼
                   LIMITATIONS
```

Ini menurut saya adalah **DNA UX ARIF Food Intelligence**.