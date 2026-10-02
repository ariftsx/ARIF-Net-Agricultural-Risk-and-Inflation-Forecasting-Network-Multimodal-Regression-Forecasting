# STEP 02 — ARIF Food Intelligence Stakeholder & Persona Definition V.0.1

## 1. Prinsip Dasar Persona ARIF Food Intelligence

Ada satu hal yang menurut saya perlu kita kunci secara konseptual:

> **ARIF Food Intelligence memiliki satu data domain yang sama, tetapi kebutuhan pengguna berbeda berdasarkan pertanyaan yang mereka bawa ke sistem.**

Karena itu kita jangan membangun:

```text
1 persona = 1 aplikasi
```

tetapi:

```text
                 ARIF FOOD INTELLIGENCE
                          │
             Shared Food Price Data
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
     PUBLIC            PRODUCER          ACADEMIC
       │                  │                  │
   "Berapa harga?"   "Bagaimana trend?"  "Bagaimana model?"
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                      ARIF-Net
```

Ini sangat cocok dengan tujuan produk yang sudah didefinisikan sebagai media eksplorasi histori, forecast, konteks multimodal, model information, dan evidence. 

---

# 2. Stakeholder Map

Saya membaginya menjadi dua kelompok besar.

## A. Product Users

Mereka menggunakan aplikasi secara langsung.

### U1 — Masyarakat Umum

**Primary public user**

Pertanyaan utama:

> “Harga pangan sekarang bagaimana?”

> “Naik atau turun dibanding sebelumnya?”

> “Bagaimana perkembangan harganya?”

---

### U2 — Konsumen / Pembeli

**Public use case yang lebih spesifik**

Pertanyaan:

> “Komoditas yang saya konsumsi sedang mengalami perubahan harga seperti apa?”

Perbedaan dengan masyarakat umum tidak perlu diwujudkan sebagai akun atau role berbeda. Ini lebih tepat sebagai **context/use case**, bukan sistem role.

---

### U3 — Petani / Produsen

Pertanyaan:

> “Bagaimana perkembangan harga komoditas yang saya produksi pada pasar referensi?”

Perlu boundary yang sangat jelas:

```text
ARIF:
Market reference
✓

ARIF belum:
Farm-gate price
✗
Production cost
✗
Profit optimization
✗
Selling recommendation
✗
```

Karena Phase 0 menetapkan Jakarta sebagai forecast target market dan wilayah produksi/supplier sebagai external context; bukan sebagai model harga petani. 

---

### U4 — Pelajar / Mahasiswa / Pembelajar

Pertanyaan:

> “Mengapa harga pangan berubah?”

> “Bagaimana data cuaca, berita, dan harga digunakan?”

> “Bagaimana forecasting dilakukan?”

Ini sangat cocok dengan perluasan **food-price literacy** yang baru kita definisikan.

---

## B. Supporting Stakeholders

### S1 — Researcher / Project Owner

Kepentingan:

* model berjalan;
* hasil forecasting tersaji;
* dataset/model version terlihat;
* evidence dapat dipresentasikan;
* research dan product tetap sinkron.

---

### S2 — Dosen / Evaluator

Kepentingan:

* memahami problem;
* memahami pipeline;
* melihat metodologi;
* melihat benchmark;
* melihat ablation;
* melihat limitations.

Product baseline memang sudah menyebut methodology/model explanation, benchmark/ablation evidence, serta model/data version. 

---

### S3 — System / Data Operator

Ini bukan public persona, tetapi stakeholder operasional.

Kepentingannya:

* memastikan data valid;
* versioning;
* API/inference;
* model artifact;
* availability;
* monitoring.

Ini penting nanti untuk arsitektur backend meskipun tidak perlu menjadi fokus utama UI publik.

---

# 3. Primary Persona Matrix

Sekarang kita perdalam.

| Persona           | Primary Question                                   | Primary Goal               | Information Need                          |
| ----------------- | -------------------------------------------------- | -------------------------- | ----------------------------------------- |
| Masyarakat        | Harga pangan bagaimana?                            | Memahami kondisi harga     | Current + history + trend                 |
| Konsumen          | Harga komoditas yang dikonsumsi bagaimana?         | Memahami perubahan harga   | Price + movement + context                |
| Petani/Produsen   | Harga pasar komoditas saya bergerak bagaimana?     | Market visibility          | Price + trend + forecast + market context |
| Pelajar/Mahasiswa | Mengapa dan bagaimana harga diprediksi?            | Belajar                    | Data + context + methodology              |
| Dosen/Evaluator   | Apakah pendekatan ini dapat dipertanggungjawabkan? | Evaluasi                   | Model + experiment + evidence             |
| Researcher        | Bagaimana hasil model digunakan?                   | Research/product operation | Forecast + artifacts + version            |

---

# 4. Persona 01 — Masyarakat Umum

## Profil penggunaan

Tidak diasumsikan memiliki pengetahuan statistik atau machine learning.

### Tujuan

Mengetahui:

* harga komoditas;
* perubahan harga;
* trend;
* forecast sederhana;
* konteks dasar.

### Pain point

Informasi harga sering dipahami sebagai angka tunggal:

```text
Cabai = Rp42.000
```

padahal user ingin mengetahui:

```text
Apakah ini naik?
Apakah ini turun?
Bagaimana trend-nya?
Bagaimana kemungkinan pergerakan berikutnya?
```

### Information Need

```text
Current Price
Historical Trend
Recent Movement
Forecast
Simple Explanation
```

### Preferred Experience

```text
Simple
Visual
Low cognitive load
Plain language
```

### Fitur utama

**Commodity Explorer + Price Overview + Forecast Snapshot**

---

# 5. Persona 02 — Konsumen

Persona ini secara praktis merupakan bagian dari public user, sehingga **tidak perlu membuat sistem akun/role konsumen terpisah**.

Itu penting agar arsitektur tidak menjadi terlalu kompleks.

### Tujuan

Melihat perkembangan harga komoditas yang relevan dengan konsumsi sehari-hari.

### Information Need

```text
Current
↓
7D movement
↓
30D movement
↓
Historical trend
↓
Forecast
```

### Fitur

**Price Explorer**

**Historical Trend**

**Forecast**

**Context**

**Educational explanation**

---

# 6. Persona 03 — Petani / Produsen

Ini persona yang menurut saya paling menarik untuk perluasan produk Anda, tetapi juga paling sensitif terhadap positioning.

### Pertanyaan utama

> “Bagaimana perkembangan harga komoditas saya pada pasar tujuan/referensi?”

Bukan:

> “Berapa harga panen saya?”

karena data tersebut belum termasuk dalam kontrak.

### Information Need

```text
Commodity
↓
Target Market
↓
Current Market Price
↓
Historical Trend
↓
Recent Movement
↓
Forecast
↓
Climate/Supply Context
```

Dan khusus untuk persona ini, supplier-region information menjadi lebih relevan karena Phase 0 memang mengaitkan external context dengan wilayah produksi/pemasok. 

### Fitur

**Market Reference**

**Commodity Trend**

**Forecast**

**Supplier / Climate Context**

**Price History**

### Yang tidak kita janjikan

```text
✗ "Harga jual ideal"
✗ "Waktu terbaik panen"
✗ "Waktu terbaik menjual"
✗ "Estimasi keuntungan"
```

Karena itu membutuhkan model/data tambahan.

---

# 7. Persona 04 — Pelajar / Mahasiswa

Di sinilah ARIF Food Intelligence bisa mempunyai nilai edukasi yang kuat.

### Tujuan

Memahami konsep melalui data nyata.

### Pertanyaan

> Mengapa harga berubah?

> Apa hubungan historical price dengan forecast?

> Apa kegunaan climate?

> Bagaimana berita direpresentasikan?

> Apa arti forecast 7 hari dibanding 30 hari?

### Information Need

```text
DATA
 ↓
CONTEXT
 ↓
MODEL
 ↓
FORECAST
 ↓
INTERPRETATION
```

### Fitur

**Data Stories**

**Food Price Literacy**

**Commodity Education**

**How Forecasting Works**

**How to Read the Chart**

**ARIF-Net Methodology**

---

# 8. Persona 05 — Dosen / Evaluator

Persona ini bukan target public consumption, tetapi penting untuk Capstone.

### Tujuan

Menilai apakah:

* problem jelas;
* solusi konsisten;
* model benar-benar sesuai;
* evidence ada;
* klaim tidak berlebihan.

### Information Need

```text
Problem
↓
Research Goal
↓
Data
↓
Architecture
↓
Experiment
↓
Benchmark
↓
Ablation
↓
Limitations
```

### Fitur

**Research Center**

```text
Model
Methodology
Pipeline
Experiment
Benchmark
Ablation
Limitations
```

Dan UI harus memperlihatkan model/data version karena itu memang sudah menjadi requirement product baseline. 

---

# 9. Persona 06 — Researcher / Project Owner

Ini adalah persona internal.

### Tujuan

Menghubungkan:

```text
Research Artifact
        ↓
Inference
        ↓
Product
```

### Information Need

```text
Dataset Version
Model Version
Inference Version
Experiment Version
Data Cutoff
Modality Availability
```

### Fitur

Ini nantinya lebih cocok berada di:

**Research/Admin layer**, bukan public dashboard.

---

# 10. Jobs-to-be-Done

Sekarang kita bisa menerjemahkan persona menjadi pekerjaan nyata.

### Masyarakat

> **When I want to know the condition of a food commodity, I want to see its current and historical movement so that I can understand the price trend rather than only seeing one price value.**

### Konsumen

> **When I notice food prices changing, I want to explore the recent trend and context so that I can understand the movement over time.**

### Petani/Produsen

> **When I monitor my commodity, I want to see its market-reference price trend and forecast so that I can understand how the destination market is moving.**

### Pelajar

> **When I study food-price dynamics, I want to explore real data, external context, and forecasting methodology so that I can understand how multimodal forecasting works.**

### Dosen/Evaluator

> **When I evaluate ARIF-Net, I want to inspect the methodology and experimental evidence so that I can understand how the system's conclusions were obtained.**

Perlu dicatat, kalimat JTBD tersebut adalah **product-design abstraction**, bukan klaim empiris bahwa semua anggota kelompok tersebut memiliki perilaku persis demikian.

---

# 11. Information Depth per Persona

Ini sangat penting untuk UI.

Kita tidak boleh membuat semua orang melihat informasi dengan kedalaman yang sama.

```text
                 INFORMATION DEPTH

Masyarakat
████░░░░░░
Price → Trend → Simple Forecast

Konsumen
█████░░░░░
Price → Trend → Context → Forecast

Petani/Produsen
███████░░░
Price → Trend → Market → Forecast → Supplier Context

Pelajar
████████░░
Data → Context → Forecast → Methodology

Academic
██████████
Data → Methodology → Experiment → Evidence
```

Bukan berarti ada lima UI berbeda.

Kita membuat **progressive disclosure**.

---

# 12. Konsep Progressive Disclosure

Contohnya user melihat:

```text
Cabai Merah Keriting
Rp42.500/kg
↑ 3.2%
```

Kemudian:

### Level 1

> Harga saat ini

### Klik detail

```text
Historical Trend
```

### Klik lagi

```text
Forecast
```

### Expand

```text
Climate
News
Supply
Macro
```

### Expand lagi

```text
Model / Evidence
```

Sehingga:

```text id="27ek3g"
PUBLIC
  ↓
INFORMATION
  ↓
INTELLIGENCE
  ↓
RESEARCH
```

Ini akan membuat produk jauh lebih ramah untuk publik.

---

# 13. Stakeholder Relationship

Sekarang kita bisa lihat hubungan antar pihak:

```text id="w5v6jd"
                     DATA SOURCES
                          │
                          ▼
                    ARIF-NET ENGINE
                          │
                          ▼
                ARIF FOOD INTELLIGENCE
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
      PUBLIC          PRODUCER        ACADEMIC
          │               │               │
     Masyarakat       Petani          Dosen
     Konsumen         Produsen        Mahasiswa
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                   FOOD INFORMATION
```

Researcher/system operator berada di belakang:

```text
Researcher
    │
    ↓
Data / Model / Experiment
    │
    ↓
Product
```

---

# 14. Yang tidak perlu kita lakukan

Ini penting supaya stakeholder model tidak membuat aplikasi menjadi enterprise system.

Kita **tidak perlu** pada v1 membuat:

```text
Farmer Account
Consumer Account
Student Account
Researcher Account
Government Account
```

semuanya berbeda.

Untuk tahap awal saya justru mengusulkan:

```text
PUBLIC
   │
   ├── Anonymous browsing
   │
   └── Public information

INTERNAL
   │
   └── Research/Admin
```

Karena sebagian besar kebutuhan user publik dapat dilayani tanpa akun.

Ini juga cocok dengan prinsip **public-first** yang sudah ada di Implementation Plan. 

---

# 15. Prioritas Persona

Kita tidak harus membangun seluruh kebutuhan semua persona sekaligus.

### Product Core Audience

**Masyarakat + Konsumen**

Mereka membuat aplikasi memiliki manfaat publik.

### Product Intelligence Audience

**Petani / Produsen**

Memberikan use case yang lebih substantif pada data komoditas dan market reference.

### Product Learning Audience

**Pelajar / Mahasiswa**

Memberikan fungsi literacy dan education.

### Product Validation Audience

**Dosen / Evaluator**

Memastikan produk juga dapat berfungsi sebagai demonstrator akademik.

Jadi satu platform mempunyai:

```text
PUBLIC VALUE
      +
FOOD INTELLIGENCE
      +
EDUCATIONAL VALUE
      +
ACADEMIC EVIDENCE
```

Saya sengaja tidak menyebut salah satunya sebagai “lebih baik”; ini hanya pembagian **fungsi produk**.

---

# 16. Persona-to-Feature Matrix

Dengan semua ini, kita sekarang dapat membuat mapping awal:

| Feature          | Masyarakat | Konsumen | Petani | Pelajar | Academic |
| ---------------- | :--------: | :------: | :----: | :-----: | :------: |
| Current Price    |      ●     |     ●    |    ●   |    ●    |     ●    |
| Historical Price |      ●     |     ●    |    ●   |    ●    |     ●    |
| Trend            |      ●     |     ●    |    ●   |    ●    |     ●    |
| Forecast         |      ●     |     ●    |    ●   |    ●    |     ●    |
| Multi-Horizon    |      ○     |     ●    |    ●   |    ●    |     ●    |
| Climate Context  |      ○     |     ○    |    ●   |    ●    |     ●    |
| Supply Context   |      ○     |     ○    |    ●   |    ●    |     ●    |
| News/Sentiment   |      ○     |     ○    |    ●   |    ●    |     ●    |
| Macro/Logistics  |      ○     |     ○    |    ●   |    ●    |     ●    |
| Extreme Movement |      ○     |     ○    |    ●   |    ●    |     ●    |
| Education        |      ●     |     ●    |    ●   |    ●    |     ○    |
| Methodology      |      ○     |     ○    |    ○   |    ●    |     ●    |
| Benchmark        |      —     |     —    |    —   |    ○    |     ●    |
| Ablation         |      —     |     —    |    —   |    ○    |     ●    |
| Limitations      |      ●     |     ●    |    ●   |    ●    |     ●    |

Keterangan:

`●` relevan langsung
`○` relevan secara opsional/context
`—` bukan kebutuhan utama

---

# 17. Hasil STEP 02

Kita sekarang punya struktur stakeholder yang cukup jelas:

```text id="b1y2d6"
                  ARIF FOOD INTELLIGENCE
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       PUBLIC          PRODUCER         LEARNING
          │                │                │
    Masyarakat         Petani          Pelajar
    Konsumen           Produsen        Mahasiswa
          │                │                │
          └────────────────┼────────────────┘
                           │
                     INTELLIGENCE
                           │
                         Forecast
                           │
                     ARIF-Net Engine
                           │
                    RESEARCH / EVIDENCE
                           │
                    Dosen / Researcher
```

Dan ada satu keputusan desain konseptual yang menurut saya sebaiknya kita bawa ke tahap selanjutnya:

> **Jangan membangun aplikasi berdasarkan “role”. Bangun berdasarkan “intent”.**

Contohnya:

```text
Saya ingin tahu harga
→ Price Explorer

Saya ingin memahami pergerakan
→ Trend / Forecast

Saya ingin memahami konteks
→ Context

Saya ingin belajar
→ Education

Saya ingin memeriksa penelitian
→ Research
```

Ini memungkinkan satu pengguna berpindah kebutuhan tanpa harus berganti akun atau masuk ke dashboard khusus.