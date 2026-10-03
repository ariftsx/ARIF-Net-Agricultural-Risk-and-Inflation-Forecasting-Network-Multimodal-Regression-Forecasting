# ARIF-Net — Project Implementation Plan & Research Knowledge Base

**Document ID:** `ARIF-NET-DOC-001`  
**Document Version:** `v2.0.0`  
**Document Status:** **OFFICIAL BASELINE / RESEARCH-ENGINEERING KNOWLEDGE BASE — PHASE 1 SCOPE REVISION**  
**Last Validated:** 02 Oktober 2026  
**Previous Version:** `v1.1.0` (28 September 2026) — superseded; perubahan tercatat di §0.5 dan §52  
**Project Repository:** https://github.com/ariftsx/ARIF-Net-Foot-Price-Shock  
**Primary Product Working Name:** ARIF Food Intelligence  
**Research Model:** ARIF-Net (*Agricultural Risk and Inflation Forecasting Network*)  
**Institutional Context:** Program Studi Teknik Informatika, Fakultas Ilmu Komputer, Universitas Mercu Buana  
**Researcher / Project Owner:** Muhamad Nur Arif  

---

> **PURPOSE OF THIS DOCUMENT**
>
> Dokumen ini adalah *single source of truth* untuk memahami ARIF-Net secara global dan teknis: tujuan, masalah, alur berpikir, ruang lingkup, data, pipeline, arsitektur, eksperimen, aplikasi/website, dokumentasi akademik, roadmap Capstone → Tugas Akhir → pengembangan penelitian, serta aturan ketat bagi AI/agen lain yang membantu proyek.
>
> Dokumen ini sengaja membedakan antara **fakta yang terverifikasi**, **keputusan yang sudah dikunci**, **usulan yang masih membutuhkan keputusan peneliti**, dan **bagian yang harus diaudit ulang**. AI tidak boleh mengubah status tersebut tanpa bukti dan/atau keputusan pemilik proyek.

### 0.4 Post-Phase-0 synchronization rule — FROZEN

Dokumen ini pada versi `v1.1.0` telah diselaraskan dengan **`ARIF-Net_Phase_0_Research_Contract_v2.0.0.md`** yang berstatus `FROZEN — READY FOR PHASE 1` pada 24 September 2026. Phase 0 merupakan **otoritas metodologis terbaru** untuk seluruh keputusan yang sudah dibekukan.

Hirarki dokumen operasional proyek:

```text
ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v2.0.0.md
                ↓
ARIF-Net_Phase_0_Research_Contract_v2.1.0.md   (inti v2.0.0 FROZEN + Phase 1 Amendment)
                ↓
Phase 1 implementation / data artifacts / experiment evidence
```

Aturan sinkronisasi:

1. Keputusan Phase 0 yang berstatus `LOCKED` atau `DECIDED` tidak boleh lagi ditampilkan sebagai `OPEN` di Implementation Plan.
2. Temuan repository yang berbeda dari kontrak Phase 0 tetap dicatat sebagai `OBSERVED` dan menjadi objek perbaikan implementasi, bukan alasan untuk mengubah kontrak secara diam-diam.
3. Status `PROPOSED`, `CANDIDATE`, atau `OPEN` pada Phase 0 tetap dipertahankan sebagai status tersebut; sinkronisasi tidak boleh menaikkannya menjadi keputusan final tanpa evidence.
4. Appendix/arsip historis boleh mempertahankan keputusan lama untuk traceability, tetapi tidak boleh menjadi sumber keputusan aktif.
5. Jika evidence Phase 1–3 kemudian menuntut perubahan terhadap keputusan yang dibekukan, perubahan wajib melalui decision gate baru dan menghasilkan versi dokumen baru.

### 0.5 Phase 1 Decision Record — v2.0.0

Versi `v2.0.0` adalah rilis **MAJOR** karena scope proyek berubah (§31.1): sumber harga, target market, scope komoditas, dan sumber iklim ditetapkan ulang melalui 24 decision gate Phase 1 (`P1-DG-01` s.d. `P1-DG-24`) yang diputuskan project owner pada 1–2 Oktober 2026. Prefix `P1-DG` dipakai agar tidak bentrok dengan penomoran DG di Plan (§36), Contract §15, dan Validation Gates Contract Appendix A.

**Yang TIDAK berubah:** research goal, primary task (regression), target `r(t,h)`, horizon grid 1/3/7/14/30/90/180/365, Explicit Historical Price Backbone, protokol anti-leakage, status candidate untuk reliability-aware dan horizon-conditioned fusion, serta seluruh Strict AI Governance Rules.

| ID | Keputusan | Status | Dampak utama |
|---|---|---|---|
| P1-DG-01 | Sumber harga target utama = **PIHPS Bank Indonesia** (survei pasar tradisional, harga eceran). Website **PIBC** dan **IPJ** menjadi sumber pelengkap (multi-sumber), menyusul. | `DECIDED` | Contract §5.1; Plan §4.1, §10.1; `DATA_PROVENANCE.md` |
| P1-DG-02 | Target market = **Pasar Kramatjati** (PIHPS level-3, harga eceran) untuk ketiga komoditas, termasuk beras. PIKJ dan PIBC **tidak lagi** menjadi target market. PIBC tetap dipakai sebagai konteks pasokan beras dan sumber pelengkap. Jakarta tetap forecast market (DG-09 Contract tidak berubah). | `DECIDED` | Contract §3.1; Plan §4.1; penulisan akademik wajib menyebut level harga = eceran |
| P1-DG-03 | Identitas market = **nama pasar + level 3** (`Pasar Kramatjati`, `level=3`). Label regency PIHPS ("Kota Jakarta Pusat") dicatat sebagai *source quirk* dan tidak dipakai; secara geografis pasar berada di Jakarta Timur. | `DECIDED` | `DATA_DICTIONARY.md` |
| P1-DG-04 | Primary evidence Capstone = **3 komoditas**: Cabai Merah Keriting, Bawang Merah Ukuran Sedang, Beras Kualitas Medium I. Komoditas PIHPS lain yang sudah dikoleksi (Beras Bawah I/II, Medium II, Super I/II, Cabai Merah Besar, Cabai Rawit Hijau, Cabai Rawit Merah) = *extended scope* untuk generalisasi TA. | `DECIDED` | Contract §3; DG-07/08; beban eksperimen; BAB I §1.5 |
| P1-DG-05 | Grade beras = **Beras Kualitas Medium I** (`com_3`). Definisi resmi grade diverifikasi dan dicatat di `DATA_DICTIONARY.md`. Pemetaan ke taxonomy PIBC wajib dibuat sebelum PIBC dipakai sebagai pengisi. | `DECIDED` | Contract §3.1 catatan taxonomy |
| P1-DG-06 | Integrasi multi-sumber: **hanya nilai null** pada seri target yang boleh diisi dari sumber lain. Harga yang sama berhari-hari adalah **observasi valid** dan tidak ditambal. Pengaman wajib: (1) kolom `value_source` + `is_filled`, seri PIHPS asli tidak ditimpa; (2) prioritas sumber paling sejenis (eceran, pasar sama → eceran Jakarta → grosir dengan kalibrasi); (3) validasi pada hari overlap sebelum dipakai; (4) parameter kalibrasi fit pada training saja; (5) eksperimen dilaporkan dengan dan tanpa nilai isian. | `DECIDED` (aturan); implementasi menunggu data PIBC/IPJ | Plan §9.2, §10.1; `LEAKAGE_AUDIT_REPORT.md` |
| P1-DG-07 | Horizon `h` dinyatakan dalam **hari kalender**. Aturan target ketika `t+h` jatuh pada hari tanpa observasi ditetapkan di `TARGET_HORIZON_SPEC.md` (Phase 2). | `DECIDED` (detail Phase 2) | DG-05/06 (definisi teknis, grid tidak berubah) |
| P1-DG-08 | Q95 pada seri harga lengket (mis. beras h=1, Q95=0 pada audit awal full-data) dicatat sebagai **known issue**. Opsi (A) tandai tidak informatif, (B) kuantil dari r≠0, (C) floor threshold diuji sebagai sensitivity di Phase 2 **memakai data training saja**. DG-15 Contract tidak diubah. | `DEFERRED / KNOWN ISSUE` | Contract §8; RQ4 |
| P1-DG-09 | Sumber iklim = **Open-Meteo Historical Weather API** (data *reanalysis*, bukan observasi stasiun), menggantikan BMKG. Alasan: portal BMKG tidak dapat diakses secara andal saat diperiksa peneliti (observasi peneliti, Oktober 2026). | `DECIDED` | Contract §5.1–5.2; `DATA_PROVENANCE.md` |
| P1-DG-10 | Model reanalysis = **ERA5-Seamless**. Jika variabel tertentu kosong saat smoke test, turun ke **ERA5** dan dicatat. Best Match tidak digunakan (sumber model dapat berganti). | `DECIDED` | Konsistensi seri iklim |
| P1-DG-11 | Wilayah pemasok per komoditas mengikuti Tier 1/Tier 2 (lihat tabel wilayah). Tier = **kekuatan bukti** sebagai pemasok Jakarta, bukan volume. Semua lokasi dikoleksi; **Tier 1 dimodelkan lebih dulu**, Tier 2 diuji sebagai eksperimen pembanding. Status wilayah tetap *candidate* (Contract §4.5). | `DECIDED` | `SUPPLIER_REGION_MAPPING.md` |
| P1-DG-12 | Titik koordinat = **centroid poligon batas administrasi kabupaten**; sumber data batas dicatat. Keterbatasan (centroid dapat jatuh di luar lahan sentra) ditulis di Limitations. | `DECIDED` | Location registry |
| P1-DG-13 | **Bawang putih dikeluarkan** dari scope (90–95% kebutuhan dipenuhi impor). | `DECIDED` | Scope |
| P1-DG-14 | Variabel iklim: **9 variabel core** dipakai untuk modelling. Variabel cadangan tetap dikoleksi dan disimpan terpisah (`raw_json/reserve/`), **tidak dipakai** dalam modelling; aktivasi hanya lewat decision gate baru. Variabel lain tidak dikoleksi. | `DECIDED` | Contract §5.2; Plan §12.1 |
| P1-DG-15 | Unit & waktu: Celsius, m/s, mm, ISO 8601, timezone **Asia/Jakarta**. | `DECIDED` | `DATA_DICTIONARY.md` |
| P1-DG-16 | Iklim mulai **2018-01-01** (konteks lag/rolling); harga target mulai **2019-01-01** (PIHPS dikoleksi ulang dari 2019). | `DECIDED` | Collection config |
| P1-DG-17 | *Release lag* iklim: fitur iklim untuk forecast origin `t` hanya memakai data bertanggal **≤ t−5**. Lag diterapkan pada feature layer, bukan collection layer. | `DECIDED` | `TEMPORAL_AVAILABILITY_MATRIX.md`; leakage audit |
| P1-DG-18 | Versi: Implementation Plan → **v2.0.0** (MAJOR, scope berubah); Contract → **v2.1.0** (Phase 1 Amendment; inti frozen dipertahankan). | `DECIDED` | Dokumen ini |
| P1-DG-19 | Gambar pipeline: header diperbarui (market = Pasar Kramatjati eceran; komoditas = CMK, Bawang Merah, Beras Medium I). | `ACTION — owner` | Materi presentasi |
| P1-DG-20 | Gambar pipeline: Multi-Horizon Head mengikuti grid 1/3/7/14/30/90/180/365 (tambah H3, perbaiki typo H365). | `ACTION — owner` | Materi presentasi |
| P1-DG-21 | Gambar pipeline: tahap "Augmentation" (text/image augmentation, balance data) dihapus; tidak ada di kontrak. | `ACTION — owner` | Materi presentasi |
| P1-DG-22 | Validasi = **chronological train → validation → test**; *rolling-origin (time-series) validation* bila diperlukan. Random k-fold cross-validation **dilarang**. | `DECIDED` | Plan §16; Contract §6 |
| P1-DG-23 | Metrik final (lihat tabel metrik), termasuk **R² dipertahankan** sebagai metrik pelengkap atas keputusan owner. | `DECIDED` | Contract §11; Plan §17 |
| P1-DG-24 | Arsitektur tetap mengikuti **Contract §9**: Explicit Price Backbone `DECIDED`; reliability-aware dan horizon-conditioned fusion tetap `PROPOSED CANDIDATE`; DG-18 (pemilihan arsitektur lewat eksperimen) tetap `LOCKED`. Gambar pipeline dikoreksi agar sesuai kontrak. | `DECIDED` (kontrak tidak berubah) | Contract §9; gambar pipeline |

Keputusan di tabel ini mengungguli teks v1.1.0 yang bertentangan. Teks lama yang terdampak tetap dipertahankan dengan penanda `SUPERSEDED BY P1-DG-xx` untuk traceability (RULE 22).

---

## 0. Document Control & Governance

### 0.1 Tujuan dokumen

Dokumen ini harus dapat diunggah ke AI lain sebagai konteks tunggal. Setelah membaca dokumen ini, AI diharapkan memahami:

1. Masalah penelitian yang hendak diselesaikan.
2. Goal utama model dan posisi `regression forecasting`.
3. Hubungan antara historical price dynamics dan faktor eksternal.
4. Peran climate/supply, news sentiment, dan macro/logistics.
5. Posisi `price shock` sebagai fenomena sekunder, bukan perubahan tugas utama menjadi classification.
6. Struktur pipeline penelitian dari data acquisition sampai evaluasi.
7. Struktur aplikasi/website yang menjadi produk Capstone.
8. Bagaimana Capstone menjadi fondasi Tugas Akhir tanpa membuat proyek kedua yang terpisah.
9. Apa yang benar-benar sudah ada di repository.
10. Apa yang masih salah, perlu diperbaiki, belum dipilih, atau belum terbukti.
11. Batasan yang tidak boleh dilanggar saat memberikan analisis, saran, kode, atau kesimpulan.

### 0.2 Status label yang digunakan

| Status | Arti | Aturan AI |
|---|---|---|
| `LOCKED` | Sudah menjadi arah/tujuan resmi proyek | Jangan diubah diam-diam. Perubahan harus menjadi decision gate. |
| `OBSERVED` | Fakta yang ditemukan dari repository, dataset, atau dokumen | Jangan diperlakukan sebagai rancangan ideal. |
| `PROPOSED` | Rekomendasi desain/metodologi yang kuat tetapi belum menjadi keputusan final | Wajib disebut sebagai usulan, bukan fakta. |
| `OPEN` | Keputusan atau detail belum dikunci | Jangan mengarang jawabannya. Tampilkan sebagai pertanyaan/decision gate. |
| `DEPRECATED` | Informasi lama yang bertentangan dengan baseline baru | Jangan digunakan sebagai dasar keputusan baru kecuali untuk histori/audit. |
| `VERIFIED` | Klaim telah diverifikasi melalui sumber yang disebutkan | Tetap cantumkan sumber/bukti bila dipakai untuk klaim akademik. |
| `UNVERIFIED` | Belum diverifikasi | Dilarang dipresentasikan sebagai temuan final. |

### 0.3 Otoritas pengambilan keputusan

Pemilik keputusan metodologi dan arah penelitian adalah **peneliti/proyek owner**.

AI berfungsi sebagai:

- research assistant,
- software/data engineering assistant,
- reviewer,
- analyst,
- documentation assistant,
- implementation assistant.

AI **bukan** pengambil keputusan final. Perubahan pada salah satu hal berikut harus diperlakukan sebagai *decision gate*:

- research goal,
- primary task,
- target variable,
- forecasting horizon,
- modality utama,
- arsitektur inti,
- loss/objective utama,
- definisi shock,
- research questions,
- novelty claim,
- experimental protocol,
- scope Capstone/TA.

---

# 1. Project Identity

## 1.1 Nama proyek

**ARIF-Net — Agricultural Risk and Inflation Forecasting Network**

Repository saat ini menggunakan nama:

`ARIF-Net-Foot-Price-Shock`

Nama tersebut merupakan identitas repository/histori implementasi. Secara konseptual, identitas penelitian telah diarahkan menjadi **multimodal food price forecasting and intelligence**, bukan sekadar shock detection.

## 1.2 Tema penelitian

> **Multimodal Food Price Forecasting and Intelligence**

Fokus utama adalah membangun model **forecasting berbasis regresi** yang dapat menggabungkan:

- historical price dynamics,
- climate/supply signals,
- news sentiment,
- macro/logistics signals,

untuk menghasilkan prediksi pergerakan harga komoditas pangan pada periode berikutnya.

## 1.3 Produk aplikasi

Nama kerja produk:

> **ARIF Food Intelligence**

ARIF Food Intelligence adalah lapisan aplikasi/web di atas model penelitian ARIF-Net. Aplikasi bukan tujuan penelitian yang berdiri sendiri; aplikasi berfungsi sebagai:

- demonstrator Capstone,
- interface eksplorasi hasil model,
- media interpretasi data multimodal,
- media visualisasi hasil eksperimen,
- proof-of-concept pemanfaatan model forecasting.

## 1.4 Sasaran jangka panjang

Pipeline yang sama ditujukan untuk berkembang secara berurutan:

```text
CAPSTONE FOUNDATION
      ↓
Validated Research + Working Product
      ↓
TUGAS AKHIR
      ↓
Deeper Experimental Evidence
      ↓
OPTIONAL INTERNATIONAL JOURNAL / RESEARCH EXTENSION
```

Tidak dibuat dua proyek terpisah. Capstone dan Tugas Akhir adalah dua tahap kedalaman dari proyek yang sama.

---

# 2. Research Goal — LOCKED

## 2.1 Goal utama

> **Mengembangkan model forecasting berbasis regresi yang mengintegrasikan historical price dynamics dengan beberapa sumber data eksternal untuk memprediksi pergerakan harga komoditas pangan pada periode berikutnya.**

Informasi flow yang wajib dipertahankan:

```text
Historical Price Dynamics
          +
Climate / Supply
          +
News Sentiment
          +
Macro / Logistics
          ↓
Multimodal Representation / Fusion
          ↓
Regression
          ↓
Forecast Price Movement
```

## 2.2 Konsekuensi langsung dari goal

ARIF-Net **bukan** proyek yang primary task-nya:

- klasifikasi price shock,
- klasifikasi naik/turun semata,
- prediksi shock sebagai label utama,
- causal inference,
- policy simulation tanpa desain kausal.

`Price shock` tetap penting, tetapi berada sebagai **secondary phenomenon/capability**, misalnya:

- shock-aware loss,
- subset evaluation pada periode ekstrem,
- extreme-movement monitoring,
- error analysis,
- early-warning indicator.

## 2.3 Masalah inti yang hendak diselesaikan

Model forecasting price-only dapat gagal menangkap konteks perubahan harga yang datang dari luar seri harga, terutama ketika terjadi perubahan eksternal yang memiliki sinyal temporal berbeda.

ARIF-Net menguji apakah integrasi beberapa modality heterogen dapat memberikan informasi tambahan terhadap forecasting dibanding model yang hanya menggunakan historical price atau satu kelompok fitur tertentu.

Masalah tersebut dipecah menjadi empat kebutuhan penelitian:

1. **Temporal price understanding** — model harus mempelajari pola historis harga, bukan hanya membaca faktor eksternal.
2. **External signal integration** — model harus dapat menggunakan sinyal climate/supply, macro/logistics, dan news sentiment.
3. **Multimodal fusion** — model membutuhkan mekanisme untuk menyatukan representasi yang berbeda.
4. **Extreme movement awareness** — evaluasi dan/atau objective perlu memperhatikan kondisi perubahan harga ekstrem tanpa mengubah primary task menjadi classification.

---

# 3. Mental Model / Alur Berpikir Penelitian

Bagian ini adalah pondasi reasoning yang harus dijaga oleh manusia maupun AI.

## 3.1 Alur berpikir level-1

```text
Fenomena Harga Pangan
        ↓
Mengapa harga berubah?
        ↓
Tidak hanya karena harga sebelumnya
        ↓
Ada internal dynamics + external signals
        ↓
Kelompokkan external signals
        ├── Supply / Climate
        ├── Macro / Logistics
        └── Information / Sentiment
        ↓
Satukan data yang heterogen secara temporal
        ↓
Bangun regression forecasting model
        ↓
Bandingkan dengan baseline
        ↓
Uji apakah modality memberi tambahan informasi
        ↓
Uji apakah fusion / shock-aware mechanism memberi kontribusi
        ↓
Evaluasi error keseluruhan + kondisi ekstrem
        ↓
Interpret predictive contribution
        ↓
Bangun product layer untuk demonstrasi dan penggunaan
```

## 3.2 Alur berpikir level-2: research logic

Setiap keputusan teknis harus dapat menjawab pertanyaan berikut:

```text
PROBLEM
  └─ Apa fenomena nyata yang ingin diprediksi?

TARGET
  └─ Besaran apa yang menjadi Y?

INFORMATION SET
  └─ Informasi apa yang tersedia sebelum prediction cutoff?

TEMPORAL CONTRACT
  └─ Informasi tersebut tersedia kapan?

REPRESENTATION
  └─ Bagaimana data heterogen direpresentasikan?

MODEL
  └─ Bagaimana model memetakan input → target?

BENCHMARK
  └─ Dibandingkan dengan apa?

ABLATION
  └─ Komponen mana yang benar-benar memberi kontribusi?

EVALUATION
  └─ Apakah hasil konsisten dan sah secara temporal?

INTERPRETATION
  └─ Apa yang dapat dikatakan dari model, dan apa yang tidak dapat dikatakan?
```

## 3.3 Prinsip reasoning utama

### Prinsip A — Forecasting lebih dulu, shock kemudian

Jangan membalik logika menjadi:

`Shock → classification → price`

Logika yang benar:

`forecast price movement → evaluasi extreme subset → shock-aware intelligence`

### Prinsip B — Historical price harus eksplisit

Jika research goal menyatakan model mempelajari `price dynamics`, historical price tidak boleh hanya menjadi target.

Model final wajib memiliki input historical price yang eksplisit dalam bentuk yang disepakati melalui decision gate, misalnya:

- raw/laged price,
- return/pct change history,
- price encoder branch,
- atau gabungan temporal representation yang secara jelas memuat dinamika harga.

### Prinsip C — Prediction ≠ causation

SHAP, attention, correlation, cross-correlation, gate activation, feature importance, dan model coefficient tidak boleh langsung disebut sebagai bukti hubungan kausal.

Gunakan istilah:

- predictive contribution,
- association,
- model attribution,
- feature contribution,
- predictive influence,

kecuali penelitian benar-benar menggunakan causal inference dengan asumsi, identification strategy, treatment/intervention definition, dan estimasi yang sesuai.

### Prinsip D — Test set adalah blind evidence

Test set tidak boleh digunakan untuk:

- pemilihan model,
- pemilihan epoch terbaik,
- tuning hyperparameter,
- keputusan arsitektur.

Validation set dipakai untuk model selection. Test set dipakai sekali/terkontrol untuk final evaluation.

### Prinsip E — Angka final harus dapat direproduksi

Tidak ada angka “terlihat bagus” yang boleh dimasukkan ke laporan tanpa:

- dataset version,
- preprocessing version,
- split protocol,
- model config,
- seed,
- metric implementation,
- experiment identifier,
- artifact/result file.

---

# 4. Scope Penelitian

## 4.1 Scope saat ini

### Primary target domain

**Status: AMENDED v2.0.0 (P1-DG-01 s.d. P1-DG-05, P1-DG-13)**

- Tiga komoditas prioritas Capstone (primary evidence): **Cabai Merah Keriting, Bawang Merah Ukuran Sedang, Beras Kualitas Medium I**.
- Forecast market: **DKI Jakarta**.
- Target market: **Pasar Kramatjati** (PIHPS Bank Indonesia, level-3, harga **eceran** pasar tradisional) untuk ketiga komoditas.
- Sumber harga target utama: **PIHPS Bank Indonesia**; PIBC dan IPJ sebagai sumber pelengkap untuk nilai null (P1-DG-06).
- Satuan: Rp/kg (PIHPS). Identitas market = nama pasar + level 3 (P1-DG-03).
- Fokus temporal: data historis harian (PIHPS terbit hari kerja); harga mulai 2019-01-01.
- Extended scope TA: Beras Bawah I/II, Medium II, Super I/II, Cabai Merah Besar, Cabai Rawit Hijau, Cabai Rawit Merah. Bawang putih dikeluarkan (P1-DG-13).
- Generalisasi ke komoditas lain tetap bukan evidence Capstone sebelum diuji.

> *SUPERSEDED BY P1-DG-02 (teks v1.1.0):* "Target market prioritas: PIKJ untuk CMK dan bawang merah; PIBC untuk beras."

### Candidate external modalities

1. **Climate / Supply**
   - curah hujan,
   - suhu,
   - indikator anomali bila valid,
   - wilayah pemasok/sentra produksi.

2. **Macro / Logistics**
   - harga BBM,
   - event perubahan harga BBM,
   - indikator logistik lain yang benar-benar tersedia dan dapat dipertanggungjawabkan.

3. **News / Sentiment**
   - berita terkait pangan, harga, inflasi, cuaca, supply, BBM/logistics,
   - sentiment score dan agregasi harian,
   - provenance artikel.

4. **Calendar**
   - hari,
   - minggu,
   - bulan,
   - hari libur,
   - event kalender yang diketahui sebelum prediction time.

## 4.2 Batasan utama

Proyek tidak secara otomatis mencakup:

- causal policy simulation,
- intervention effect estimation,
- economic equilibrium modeling,
- seluruh komoditas nasional sekaligus,
- generalisasi global,
- production-grade market intervention system,
- automatic government decision system.

Perluasan hanya melalui decision gate.

---

# 5. Research Questions — BASELINE / PROPOSED

RQ yang menjadi baseline rancangan saat ini:

### RQ1 — Forecasting

**Seberapa efektif model regresi multimodal yang mengintegrasikan historical price dynamics dan faktor eksternal dalam memprediksi pergerakan harga komoditas pangan dibandingkan baseline?**

### RQ2 — Informasi multimodal

**Sejauh mana climate, sentiment, dan macro/logistics memberi tambahan informasi dibandingkan price-only atau reduced-modality models?**

### RQ3 — Fusion mechanism

**Apakah mekanisme multimodal fusion dan/atau Cross-Modal Shock Gating memberikan kontribusi terukur terhadap regression forecasting?**

### RQ4 — Extreme movement

**Bagaimana performa model pada periode pergerakan harga ekstrem dibandingkan keseluruhan periode?**

### RQ5 — Interpretability

**Bagaimana model memberikan predictive contribution information tanpa menyimpulkan hubungan kausal yang belum diuji?**

> **RULE:** RQ ini adalah baseline kerja. Perubahan RQ harus menjadi decision gate dan harus diikuti audit terhadap objective, experiment, dan struktur laporan.

---

# 6. Target Variable & Forecast Horizon

## 6.1 Kondisi repository saat ini — OBSERVED

Repository saat ini menggunakan:

- nominal price sebagai sumber target,
- `target_pct_change` sebagai target modeling,
- rekonstruksi nominal predicted price saat evaluasi.

Code `build_master_dataset.py` membentuk `target_pct_change` dari perubahan harga harian dan juga membuat beberapa target-derived features. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/preprocessing/build_master_dataset.py

## 6.2 Target final — DECIDED BY PHASE 0

Target internal canonical ARIF-Net adalah **relative price movement / percentage change**:

```text
r(t,h) = (P(t+h) - P(t)) / P(t)
```

Dengan:

- `P(t)` = harga aktual pada forecast origin;
- `P(t+h)` = harga aktual pada horizon `h`;
- `r(t,h)` = relative price movement.

Direct/nominal price bukan target model kedua. Harga nominal untuk aplikasi direkonstruksi sebagai:

```text
P_hat(t+h) = P(t) × (1 + r_hat(t,h))
```

**Status:** `DECIDED`. Implementasi Phase 1 harus mengikuti kontrak ini kecuali decision gate baru dibuka berdasarkan evidence metodologis.

## 6.3 Forecast horizon — DECIDED BY PHASE 0

ARIF-Net menggunakan **multi-horizon forecasting** dengan batas maksimum **365 hari**. Horizon grid standar:

```text
1, 3, 7, 14, 30, 90, 180, 365 hari
```

Model harus menghasilkan output multi-horizon/trajectory dan **tidak boleh dipaksa monoton**. Horizon yang akhirnya dapat dieksekusi pada suatu komoditas tetap harus memenuhi feasibility data dan jumlah observasi efektif; batas 365 hari adalah research boundary, bukan jaminan kualitas semua horizon.

Aturan temporal: pada forecast origin `t`, hanya informasi yang telah tersedia pada `t` yang boleh menjadi input. Future realized climate, news, BBM, supply, dan logistics pada `t+1...t+h` dilarang digunakan sebagai observasi input. Future-known calendar dapat digunakan bila memang diketahui sebelum forecast.

---

### 6.4 Phase 1 amendment — satuan horizon (P1-DG-07)

`h` dinyatakan dalam **hari kalender**. Karena PIHPS hanya terbit pada hari kerja, aturan penentuan `P(t+h)` ketika `t+h` jatuh pada hari tanpa observasi wajib ditetapkan di `TARGET_HORIZON_SPEC.md` (Phase 2). Grid horizon tidak berubah.

---

# 7. Price Shock Definition

## 7.1 Final shock protocol — PHASE 0 DECIDED

Shock merupakan **secondary phenomenon**, bukan target classification utama. Threshold utama tidak lagi menggunakan fixed 3% sebagai definisi universal lintas horizon.

Untuk setiap horizon `h`, gunakan threshold berbasis distribusi historical relative movement:

```text
Shock(t,h) = |r(t,h)| >= Q_alpha(|r_h|)
```

Dengan `Q_alpha` dihitung **hanya dari training set**. Primary threshold:

```text
alpha = 0.95
```

Sensitivity yang direncanakan:

```text
Q90 / Q95 / Q97.5 / Q99
```

### 7.2 Legacy threshold

`|ΔP| > 3%` dipertahankan hanya sebagai **legacy repository threshold / comparison / sensitivity reference**. Ia tidak boleh dipresentasikan sebagai threshold ilmiah universal untuk seluruh horizon.

### 7.3 Rules

- Primary task tetap regression.
- Shock digunakan untuk subset evaluation, shock-aware objective apabila diperlukan, monitoring, dan error analysis.
- Shock threshold harus dihitung split-aware dan tidak boleh menggunakan distribusi test untuk menentukan threshold.
- Jika metric shock-detection tambahan dibuat, definisi actual/predicted shock harus terdokumentasi dan konsisten.

### 7.4 Existing repository issue — OBSERVED

`evaluate_models.py` saat ini menggunakan konfigurasi 3% untuk actual shock dan 2% pada bagian predicted shock recall. Temuan ini tetap dipertahankan sebagai **implementation debt** yang harus diperbaiki pada Phase 1; jangan mengubah kontrak Phase 0 untuk menyesuaikan implementasi lama.

### 7.5 Known issue — Q95 pada seri lengket (P1-DG-08)

Audit awal (full-data, non-final) menunjukkan sebagian besar hari beras memiliki `r(t,1)=0`, sehingga Q95 dapat bernilai 0 pada horizon pendek dan definisi shock kehilangan makna. Status: `DEFERRED / KNOWN ISSUE`. Alternatif diuji sebagai sensitivity di Phase 2 memakai data training saja; DG-12/DG-13 Plan tidak diubah.

---

# 8. Triple-Shock Conceptual Framework

Triple-Shock digunakan sebagai **conceptual grouping**, bukan klaim bahwa ketiga faktor terbukti kausal.

```text
                    FOOD PRICE MOVEMENT
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 Supply / Climate     Macro / Logistics   Information / Sentiment
      Shock                  Shock                Shock
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                   Multimodal Forecasting
                            │
                            ▼
                     Price Movement ŷ
```

### Group 1 — Supply / Climate

Contoh:

- rainfall,
- temperature,
- climate anomaly,
- producer-region conditions.

### Group 2 — Macro / Logistics

Contoh:

- BBM state,
- BBM change event,
- logistical cost proxy yang terverifikasi.

### Group 3 — Information / Sentiment

Contoh:

- news sentiment,
- negative-news ratio,
- news volume,
- topic-specific sentiment.

---

# 9. Data Contract — CORE RESEARCH GOVERNANCE

Setiap dataset harus mempunyai minimal metadata:

| Field | Wajib |
|---|---|
| Dataset name | Ya |
| Source organization / URL | Ya |
| Collection method | Ya |
| Coverage date | Ya |
| Frequency | Ya |
| Timezone | Ya |
| Publication/availability time | Jika tersedia |
| Raw file hash/version | Disarankan |
| License/usage condition | Ya |
| Missing-value policy | Ya |
| Imputation policy | Ya |
| Transformation | Ya |
| Feature list | Ya |
| Temporal cutoff rule | Ya |
| Leakage audit status | Ya |

## 9.1 Temporal availability rule

Untuk setiap waktu prediksi `t`, hanya informasi yang tersedia sebelum atau pada cutoff yang sesuai yang boleh digunakan.

```text
                     Prediction Cutoff(t)
                           │
            ┌──────────────┼──────────────┐
            │              │              │
        Price History   Climate       News / Macro
            │              │              │
      available ≤ t   available ≤ t   published/known ≤ t
            │              │              │
            └──────────────┼──────────────┘
                           ▼
                        Model(t)
                           ▼
                       Forecast(t+1)
```

## 9.2 Anti-leakage rules

Periksa secara eksplisit:

- future row access,
- centered rolling windows,
- full-dataset scaling,
- full-dataset imputation,
- backward fill across boundary,
- future news publication,
- post-event labels,
- target-derived features yang tidak tersedia pada prediction time,
- sequence boundary,
- model checkpointing memakai test data.

---

# 10. Dataset & Pipeline — Current State

Dokumentasi penelitian sebelumnya mencatat rentang **1 Januari 2024 – 3 Agustus 2026** dan sekitar **946 observasi harian**. Angka tersebut adalah snapshot dokumentasi, bukan angka final yang boleh diasumsikan permanen. Dataset final wajib dibangun ulang dan diberi version identifier. https://github.com/ariftsx/ARIF-Net-Foot-Price-Shock

## 10.1 Price / Commodity Pipeline

```text
Raw commodity data
      ↓
Date normalization
      ↓
Duplicate check
      ↓
Missing-value audit
      ↓
Market/calendar handling
      ↓
Price series
      ↓
Target construction
      ↓
Historical price features
      ↓
Temporal split
```

Current repository memiliki preprocessing komoditas. Komponen ini dapat direuse, tetapi kebijakan `ffill/bfill` harus diaudit terutama di boundary temporal.

### 10.1a Phase 1 amendment — Price source & multi-source rule

```text
PIHPS Bank Indonesia (Pasar Kramatjati, level-3, eceran)  ← sumber utama
        ↓
Raw JSON evidence (tidak diubah)
        ↓
Null audit (nilai berulang = observasi valid, bukan missing)
        ↓
Pengisian null dari PIBC / IPJ   ← P1-DG-06, dengan value_source + is_filled
        ↓
Validasi overlap + kalibrasi split-aware
        ↓
Price series ber-versi (asli & terisi disimpan terpisah)
```

## 10.2 Climate Pipeline

```text
Open-Meteo / climate source
      ↓
Fetch daily weather
      ↓
Map producer regions
      ↓
Aggregate regional signals
      ↓
Rainfall / temperature features
      ↓
Optional anomaly features
      ↓
Temporal alignment
```

Repository saat ini mempunyai climate preprocessing dan sebelumnya menggunakan statistik full-period pada salah satu fitur deviasi suhu. Fitur yang bergantung pada statistik masa depan harus dihitung menggunakan statistik yang hanya tersedia pada training period atau dihilangkan dari final feature set.

### 10.2a Phase 1 amendment — Climate contract

**Status: AMENDED v2.0.0.** Pipeline di atas (Open-Meteo) kini menjadi sumber resmi; BMKG tidak lagi menjadi sumber utama (P1-DG-09).

**Kontrak iklim (P1-DG-09/10/12/14/15/16/17)**

| Elemen | Ketetapan |
|---|---|
| Sumber | Open-Meteo Historical Weather API, endpoint `/v1/archive` |
| Sifat data | Reanalysis (gabungan model + observasi), **bukan** observasi stasiun |
| Model | ERA5-Seamless; fallback ERA5 bila variabel kosong (dicatat) |
| Titik | Centroid poligon batas administrasi kabupaten; sumber batas dicatat |
| Periode | 2018-01-01 s.d. tanggal akhir koleksi harga |
| Unit/waktu | `temperature_unit=celsius`, `wind_speed_unit=ms`, `precipitation_unit=mm`, `timeformat=iso8601`, `timezone=Asia/Jakarta` |
| Release lag | Fitur untuk origin `t` hanya dari data bertanggal ≤ `t−5` (diterapkan di feature layer) |
| Imputasi | Tidak ada pada collection layer; nilai kosong dilaporkan |

**Variabel core (dipakai modelling — 9):** Precipitation Sum, Precipitation Hours, Mean Temperature (2 m), Maximum Temperature (2 m), Minimum Temperature (2 m), Mean Relative Humidity (2 m), Sunshine Duration, Reference Evapotranspiration (ET₀), Mean Soil Moisture (7–28 cm).

**Variabel reserve (dikoleksi, disimpan terpisah, tidak dipakai):** Maximum & Minimum Relative Humidity (2 m), Maximum Vapour Pressure Deficit, Shortwave Radiation Sum, Mean Cloud Cover, Maximum & Mean Wind Speed (10 m), Mean Soil Moisture (0–7 cm), Mean Soil Moisture (28–100 cm), Mean Soil Temperature (0–7 cm), Rain Sum (QC).

**Tidak dikoleksi:** Snowfall Sum, Snowfall Water Equivalent Sum, Apparent Temperature (mean/max/min), Sunrise, Sunset, Daylight Duration, Wet Bulb Temperature, Dewpoint, Sea Level/Surface Pressure, Dominant Wind Direction, Wind Gusts, Weather Code, Soil Temperature (7–28, 28–100, 0–100 cm), Soil Moisture (0–100 cm).


**Wilayah pemasok (P1-DG-11) — status `CANDIDATE`, bukan bobot market share**

| Komoditas | Tier 1 (dimodelkan lebih dulu) | Tier 2 (eksperimen pembanding) |
|---|---|---|
| Cabai Merah Keriting | Kab. Garut, Kab. Cianjur, Kab. Bandung Barat, Kab. Bandung, Kab. Sumedang, Kab. Magelang | Kab. Temanggung |
| Bawang Merah Ukuran Sedang | Kab. Brebes, Kab. Cirebon, Kab. Indramayu | Kab. Demak, Kab. Nganjuk, Kab. Bima, Kab. Garut |
| Beras Kualitas Medium I | Kab. Karawang, Kab. Subang, Kab. Indramayu, Kab. Cirebon, Kab. Demak | Kab. Sragen, Kab. Cilacap, Kab. Sukoharjo |

Lokasi unik untuk request iklim: **18** — Garut, Cianjur, Bandung Barat, Bandung, Sumedang, Magelang, Brebes, Cirebon, Indramayu, Karawang, Subang, Demak, Temanggung, Nganjuk, Bima, Sragen, Cilacap, Sukoharjo. Satu lokasi dapat memiliki tier berbeda per komoditas (mis. Garut: Tier 1 untuk CMK, Tier 2 untuk bawang merah); tier dicatat pada pasangan (lokasi, komoditas).

Kriteria tier: **Tier 1** = tercantum di Contract Phase 0 dan/atau muncul berulang pada bukti resmi/berita terbaru sebagai pemasok langsung ke PIKJ/PIBC; **Tier 2** = sentra produksi yang diketahui tetapi buktinya sebagai pemasok Jakarta lebih lemah, lebih lama, atau musiman. Wilayah terkait cabai rawit (Banyuwangi, Wonosobo, Boyolali, Sleman, Blitar, Jember, Enrekang) dan bawang putih (Lombok Timur/Sembalun) dikeluarkan bersama penyempitan scope. Bila data asal pasokan harian PIBC berhasil dikoleksi, bobot `w(i,t)` beras dapat dibangun berbasis evidence (Contract §4.5).


## 10.3 BBM / Macro Pipeline

```text
Official price/event source
      ↓
Date normalization
      ↓
Fuel state / change event
      ↓
Forward state representation where valid
      ↓
Temporal alignment
```

Macro feature boleh bersifat step-function/event feature apabila perubahan harga memang diketahui sejak tanggal efektifnya.

Jangan mengubah static representation menjadi seolah-olah observation kontinu bila sifat datanya sebenarnya event-driven.

## 10.4 News / Sentiment Pipeline

```text
Raw news
   ↓
Source + publication timestamp
   ↓
Deduplication
   ↓
Topic / relevance filter
   ↓
Text normalization
   ↓
Sentiment model
   ↓
Article-level score
   ↓
Daily aggregation
   ↓
Temporal cutoff
```

Repository saat ini mencoba model sentiment berbasis Hugging Face dan memiliki fallback ke lexicon domain. Source code memperlihatkan kandidat model IndoBERT/Indonesian sentiment dan fallback lexicon. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/preprocessing/preprocess_sentimen.py

**Wajib:** hasil eksperimen harus mencatat model sentiment yang benar-benar digunakan. Tidak boleh menyatakan “menggunakan IndoBERT” bila run aktual menggunakan fallback lexicon.

## 10.5 Master Dataset Pipeline

```text
Commodity
    + Climate
    + Macro/BBM
    + News/Sentiment
    + Calendar
         ↓
Temporal alignment
         ↓
Feature engineering
         ↓
Leakage audit
         ↓
Dataset version
         ↓
Train / Validation / Test
```

Repository `build_master_dataset.py` menggabungkan empat sumber utama dan membuat calendar/lag/target-derived features. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/preprocessing/build_master_dataset.py

---

# 11. Historical Price Dynamics — REQUIRED CORRECTION

## 11.1 Existing limitation

Audit repository menunjukkan dynamic branch saat ini menerima sequence dynamic features yang pada dokumentasi terutama berisi climate/sentiment, sementara `target_pct_change` berfungsi sebagai target dan `target_volatility_7d` muncul sebagai target-derived feature yang digunakan. Ini belum cukup untuk mengklaim bahwa final model secara eksplisit belajar seluruh pola historical price dynamics.

## 11.2 Required design principle

Final model harus memiliki salah satu bentuk berikut:

### Candidate A — Unified temporal branch

```text
Price history
 + Climate history
 + Sentiment history
          ↓
Unified temporal sequence encoder
```

### Candidate B — Explicit price branch

```text
Price History → Price Encoder ─┐
Climate       → Climate Encoder ─┤
Sentiment     → News Encoder ────┤
Macro         → Macro Encoder ───┤
                               ▼
                         Multimodal Fusion
```

**Status:** `LOCKED / EXPLICIT HISTORICAL PRICE BACKBONE`

Phase 0 telah memilih **Explicit Historical Price Backbone** sebagai representasi utama harga. Detail encoder tetap merupakan candidate architecture dan harus divalidasi melalui experiment, tetapi historical price tidak boleh lagi diperlakukan sebagai keputusan arsitektural yang terbuka.

---

# 12. Feature Engineering Governance

## 12.1 Feature groups

### Price dynamics

Contoh kandidat:

- lagged price,
- lagged return/pct change,
- rolling volatility,
- rolling statistics yang hanya menggunakan masa lalu,
- range/spread jika tersedia.

### Climate

- rainfall current/lagged,
- temperature current/lagged,
- region aggregates,
- anomaly dengan baseline training-safe.

### Sentiment

- mean/median sentiment,
- negative ratio,
- article volume,
- positive/negative/neutral counts,
- topic-specific score.

### Macro/logistics

- fuel price state,
- change flag,
- cumulative change bila valid,
- event age/time-since-change bila relevan.

### Calendar

- day-of-week,
- month,
- seasonality markers,
- holiday,
- known-in-advance events.

## 12.2 Prohibited feature engineering

Jangan memasukkan feature yang:

- menggunakan target masa depan,
- menggunakan informasi publikasi setelah cutoff,
- memakai full-test statistics untuk scaling/normalization,
- membangun moving average centered,
- memakai future event state,
- dibuat berdasarkan hasil test lalu dimasukkan kembali ke training.

---

# 13. Current ARIF-Net Architecture — OBSERVED / IMPLEMENTATION SNAPSHOT

Repository saat ini menggunakan PyTorch dengan dual-branch architecture. Code `train_arif_net.py` menunjukkan:

### Branch A — Dynamic

- 2-layer BiLSTM,
- hidden dimension total 128,
- bidirectional,
- dropout 0.2,
- single temporal attention layer.

Attention aktual berupa linear layer ke satu scalar per timestep lalu softmax di dimension waktu; ini **bukan multi-head temporal attention**. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_arif_net.py

### Branch B — Static/Macro

- `Linear(stat_dim → 64)`,
- LayerNorm,
- ReLU,
- `Linear(64 → 64)`,
- Dropout 0.2.

### Fusion + SGU

```text
h_dyn (128)
      +
 h_stat (64)
      ↓
 h_cat (192)
      ↓
 gate = sigmoid(W_g h_cat + b)
      ↓
 h_gated = h_cat × (1 + gate)
```

### Prediction head

```text
192 → 64 → 32 → 1
```

Output saat ini adalah `target_pct_change`.

### Important

Arsitektur repository ini adalah **implementation snapshot**, bukan arsitektur penelitian final. Setelah Phase 0, yang sudah dikunci adalah **Explicit Historical Price Backbone**; reliability-aware fusion dan horizon-conditioned fusion tetap **candidate/proposed mechanisms** yang harus diuji. BiLSTM, temporal attention, SGU, dan Shock-Weighted MSE dari repository lama tidak boleh dianggap final hanya karena sudah diimplementasikan.

---

# 14. Shock-Weighted Objective — Terminology Governance

## 14.1 Current implementation — OBSERVED

Implementasi saat ini menghitung:

```text
MSE = (y_true - y_pred)^2
weight = 1 + shock × (penalty - 1)
loss = mean(MSE × weight)
```

Dengan shock ditentukan dari:

```text
abs(y_true) > threshold
```

Code menggunakan class `ShockWeightedLoss`. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_arif_net.py

## 14.2 Terminology rule

Dokumentasi lama menyebutnya **Shock-Weighted Focal Loss**.

Itu tidak boleh digunakan untuk menjelaskan implementasi aktual karena formula yang ada merupakan weighted MSE, bukan focal loss.

Nama kerja yang benar:

> **Shock-Weighted MSE**

Perubahan istilah ini adalah koreksi dokumentasi, bukan perubahan objective penelitian secara otomatis.

---

# 15. Candidate Models & Model Governance

## 15.1 Baseline purpose

Baseline digunakan untuk menjawab:

> “Apakah model multimodal yang diusulkan memiliki nilai tambah dibanding model yang lebih sederhana?”

## 15.2 Current baseline set — OBSERVED

Repository saat ini memiliki/menyebut:

- ARIMA,
- Ridge Regression,
- SVR,
- Random Forest,
- XGBoost,
- LightGBM,
- MLP,
- BiLSTM.

`train_baseline.py` adalah sumber implementasi baseline. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_baseline.py

## 15.3 Candidate advanced model — OPEN

**Temporal Fusion Transformer (TFT)** dapat diuji sebagai kandidat advanced architecture.

Aturan:

- jangan menyatakan TFT sebagai “model terbaik” sebelum eksperimen,
- jangan mengganti seluruh ARIF-Net hanya karena TFT populer,
- bandingkan secara fair setelah data contract dan protocol terkunci.

## 15.4 Candidate model matrix

| Model | Role |
|---|---|
| Naive / persistence | Sanity-check baseline |
| Price-only linear/tree model | Price dynamics baseline |
| ARIMA | Classical time-series baseline |
| Ridge/SVR | Classical regression baseline |
| RF/XGBoost/LightGBM | Tabular multivariate baseline |
| BiLSTM | Sequential deep baseline |
| TFT | Advanced temporal candidate |
| ARIF-Net | Proposed multimodal architecture |

---

# 16. Experimental Protocol — REQUIRED

## 16.1 Temporal split

Final protocol wajib kronologis.

Minimal:

```text
TRAIN → VALIDATION → TEST
```

Contoh kerja:

```text
2024 ------------------------- early 2026
|<----------- TRAIN ---------->|<- VAL ->|<- TEST ->|
```

Tanggal final harus ditentukan setelah dataset final dibangun ulang.

## 16.2 Model selection

```text
TRAIN
  ↓
train model
  ↓
VALIDATION
  ↓
hyperparameter / epoch selection
  ↓
freeze model/config
  ↓
TEST
  ↓
final metrics
```

**Phase 1 amendment (P1-DG-22):** validasi hanya kronologis; *rolling-origin (time-series) validation* boleh digunakan bila diperlukan. Random k-fold cross-validation dilarang.

## 16.3 Current major issue — OBSERVED

`train_arif_net.py` saat ini memuat train dan test, lalu menghitung `val_loss` menggunakan test tensor setiap epoch dan menyimpan checkpoint terbaik berdasarkan nilai tersebut. Ini menyebabkan test leakage/model selection bias. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_arif_net.py

**Tidak boleh dipertahankan untuk final evidence.**

## 16.4 Sequence boundary

Current loader membentuk sequence test hanya dari data test sehingga sebagian context historis sebelum boundary hilang.

Final pipeline harus memastikan:

- target test tetap berada setelah split,
- context historical sebelum split boleh dipakai untuk membentuk sequence jika secara forecasting memang tersedia saat cutoff,
- tidak ada target masa depan masuk ke context.

---

# 17. Evaluation Framework

## 17.1 Primary regression metrics

Minimal:

- RMSE,
- MAE,
- MAPE atau sMAPE jika kondisi data menyebabkan MAPE kurang sesuai,
- MASE bila diperlukan.

## 17.2 Direction metrics

- Directional Accuracy.

Direction bukan target utama penelitian, tetapi membantu menilai kualitas movement prediction.

## 17.3 Extreme / shock subset metrics

Minimal kandidat:

- Shock MAE,
- Shock RMSE,
- Shock Recall/Precision/F1 apabila shock classification sekunder dilakukan,
- PR-AUC jika secondary shock event classification benar-benar diimplementasikan.

## 17.4 Robustness

TA/jurnal dapat menambah:

- multiple seeds,
- temporal rolling evaluation,
- alternate shock thresholds,
- alternate horizons,
- cross-commodity,
- cross-location.

## 17.5 Uncertainty — FUTURE EXTENSION

Kandidat:

- prediction interval,
- PICP,
- interval width,
- calibration.

Tidak boleh dimasukkan sebagai hasil final jika implementasinya belum benar-benar tersedia.

## 17.6 Phase 1 amendment — Final metric set

**Metrik final (P1-DG-23)** — semua dilaporkan **per horizon** dan dihitung pada test set yang blind.

| Peran | Metrik | Dihitung pada | Catatan |
|---|---|---|---|
| Utama | MAE, RMSE | `r(t,h)` | Contract §11.1 |
| Pendukung | MAE, RMSE (Rp) | Harga rekonstruksi `P̂(t+h)` | Interpretasi produk |
| Pendukung | MAPE | Harga rekonstruksi | **Tidak** dihitung pada `r` (sering bernilai 0) |
| Pendukung | MASE terhadap naive persistence | `r(t,h)` | Menguji apakah model lebih baik dari "harga tidak berubah" |
| Pendukung | R² | `r(t,h)` | Dipertahankan atas keputusan owner. Interpretasi hati-hati: tidak stabil bila mayoritas target bernilai 0, dan R² pada level harga cenderung tinggi secara trivial — karena itu dihitung pada `r(t,h)` dan tidak dijadikan dasar pemilihan model |
| Pergerakan | Directional Accuracy | Hari dengan perubahan aktual ≠ 0; proporsi hari "tetap" dilaporkan terpisah | Arah tidak terdefinisi saat r = 0 |
| Ekstrem | Shock MAE, Shock RMSE | Subset shock (definisi Contract §8; known issue P1-DG-08) | Contract §11.3 |

---

# 18. Preliminary Results — DO NOT TREAT AS FINAL

Repository README mendokumentasikan benchmark berikut:

| Model | RMSE (Rp) | MAE (Rp) | MAPE | DA | Shock MAE (Rp) |
|---|---:|---:|---:|---:|---:|
| ARIF-Net | 1,966.54 | 1,427.26 | 2.68% | 41.98% | 2,591.03 |
| LightGBM | 2,006.93 | 1,477.85 | 2.77% | 42.59% | 2,638.88 |
| ARIMA | 2,013.39 | 1,467.14 | 2.76% | 40.74% | 2,778.51 |
| Random Forest | 2,071.53 | 1,555.40 | 2.93% | 38.89% | 2,746.33 |
| SVR | 2,112.84 | 1,603.16 | 3.02% | 42.59% | 2,745.39 |
| XGBoost | 2,129.70 | 1,618.45 | 3.05% | 38.89% | 2,811.06 |
| BiLSTM | 2,244.38 | 1,670.57 | 3.16% | 41.98% | 2,680.22 |
| Ridge | 2,374.15 | 1,869.72 | 3.51% | 43.21% | 2,674.40 |
| MLP | 6,869.13 | 5,834.40 | 11.16% | 41.36% | 5,753.22 |

Source: current repository README. https://github.com/ariftsx/ARIF-Net-Foot-Price-Shock

### Mandatory interpretation rule

Angka di atas adalah **PRELIMINARY / NON-FINAL** karena experimental protocol saat ini memiliki test-set checkpoint selection issue dan beberapa pipeline lain masih memerlukan audit.

Jangan menulis:

> “ARIF-Net terbukti terbaik.”

Gunakan:

> “Pada benchmark repository saat ini, ARIF-Net memiliki nilai RMSE/MAE/MAPE terendah dari model yang dilaporkan; hasil tersebut belum dianggap final sebelum protocol leakage diperbaiki dan benchmark diulang.”

Selain itu, DA dan shock recall tidak otomatis menjadi yang terbaik di seluruh baseline.

---

# 19. Ablation Study

## 19.1 Research purpose

Ablation harus menjawab kontribusi masing-masing komponen, bukan sekadar memperlihatkan banyak varian.

Minimal matrix:

| Variant | Price dynamics | Climate | Sentiment | Macro | Fusion | SGU | Shock-weighted loss |
|---|---|---|---|---|---|---|---|
| Price-only | ✓ | – | – | – | – | – | – |
| External-only | – | ✓ | ✓ | ✓ | ✓ | – | – |
| Reduced modalities | ✓ | subset | subset | subset | ✓ | – | – |
| Full w/o SGU | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| Full w/o shock weighting | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – |
| Full ARIF-Net | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Actual list dapat berubah setelah architecture decision.

## 19.2 Fairness rules

Semua varian harus sebisa mungkin menggunakan:

- dataset yang sama,
- split yang sama,
- preprocessing yang sama,
- seed yang terdokumentasi,
- evaluation protocol yang sama,
- model selection melalui validation yang sama.

---

# 20. Explainability & Interpretation

## 20.1 Current repository state

`explainability.py` melakukan SHAP terhadap **XGBoost baseline**, bukan terhadap ARIF-Net. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/explainability.py

Karena itu:

> “SHAP membongkar otak ARIF-Net”

adalah deskripsi yang tidak tepat untuk implementasi saat ini.

## 20.2 Correct interpretation mapping

```text
XGBoost SHAP
   ↓
Explains XGBoost baseline

ARIF-Net attention
   ↓
Temporal weighting / attention pattern

ARIF-Net SGU gate
   ↓
Latent gating behavior

Gradient / Integrated Gradients / suitable deep attribution
   ↓
Potential ARIF-Net feature attribution
```

Metode final harus ditentukan berdasarkan keandalan teknis dan kesesuaian dengan model.

## 20.3 Forbidden terminology

Tanpa causal design, jangan gunakan:

- causal effect,
- causality proof,
- causes,
- “biang kerok” sebagai scientific conclusion,
- “proves policy intervention effect”.

Gunakan:

- contribution,
- attribution,
- association,
- relationship observed by the model,
- predictive importance.

---

# 21. Invalid / Deprecated Analysis in Current Repository

## 21.1 Synthetic rolling error

`advanced_analysis.py` membuat rolling error memakai angka acak (`np.random.normal`) kemudian menambahkan penalti saat shock. Ini bukan residual model aktual dan **tidak boleh dipakai sebagai research evidence**. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/advanced_analysis.py

## 21.2 Hardcoded “causal interaction” graph

File yang sama membuat graph dengan bobot hardcoded seperti:

- climate → price = 0.71,
- sentiment → price = 0.45,
- BBM → price = 0.25,

dan label “causal”. Bobot ini bukan hasil estimasi causal inference dan harus dikeluarkan dari evidence ilmiah sampai diganti dengan analisis yang sah. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/advanced_analysis.py

## 21.3 Hardcoded semantic co-occurrence

Graph keyword/co-occurrence juga menggunakan pasangan dan bobot yang ditulis langsung di kode. Ini tidak boleh dipresentasikan sebagai hasil empiris dataset.

## 21.4 Repository documentation overclaim

Dokumentasi lama masih memuat klaim seperti “kausalitas nyata”, “Q1”, “state-of-the-art”, “standard baru”, serta framing shock sebagai tujuan utama. Klaim tersebut berstatus `DEPRECATED` untuk baseline dokumen ini dan harus direvisi agar selaras dengan evidence aktual.

---

# 22. Notebook & Reproducibility State

Repository memiliki notebook:

- `notebook/scraping_dataset.ipynb`
- `notebook/preprocessing.ipynb`
- `notebook/modeling_evaluasi.ipynb`

README repo menyebut ketiganya. https://github.com/ariftsx/ARIF-Net-Foot-Price-Shock

Namun audit sebelumnya menemukan ketidaksesuaian antara notebook dan fungsi preprocessing saat ini. Notebook preprocessing memanggil nama fungsi lama yang tidak sama dengan definisi fungsi pada script terkini.

Selain itu, notebook scraping pernah memuat contoh/dummy records untuk news/BBM. Data contoh tidak boleh dianggap sebagai provenance data penelitian.

### Rule

Notebook bukan otomatis source of truth. Source of truth implementasi harus diverifikasi terhadap:

1. current source code,
2. actual dataset artifact,
3. experiment configuration,
4. reproducible execution.

---

# 23. Proposed Final Research Architecture

**Status:** `PROPOSED / PARTIALLY LOCKED`

Yang terkunci adalah information flow, bukan satu jenis neural architecture tertentu.

```text
┌──────────────────────┐
│ Historical Price     │
│ Dynamics              │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Price / Temporal      │
│ Encoder               │
└──────────┬───────────┘
           │
           │
┌──────────────────────┐       ┌──────────────────────┐
│ Climate / Supply     │       │ News / Sentiment     │
│ Temporal Encoder     │       │ NLP / Temporal      │
└──────────┬───────────┘       └──────────┬───────────┘
           │                              │
           └──────────────┬───────────────┘
                          │
                   ┌──────▼─────────┐
                   │ Macro/Logistics │
                   │ Event Encoder   │
                   └──────┬─────────┘
                          │
                   ┌──────▼─────────┐
                   │ Multimodal     │
                   │ Fusion         │
                   └──────┬─────────┘
                          │
                   ┌──────▼─────────┐
                   │ Optional SGU   │
                   └──────┬─────────┘
                          │
                   ┌──────▼─────────┐
                   │ Regression     │
                   │ Head           │
                   └──────┬─────────┘
                          │
                          ▼
                 Forecast Price Movement
```

Candidate implementation choices:

- retain BiLSTM + temporal attention,
- explicit price branch,
- unified temporal branch,
- TFT candidate,
- SGU retained and ablated.

No single choice is final until experiments justify it.

---

# 24. End-to-End Research Pipeline

## Phase 0 — Research Contract

```text
Problem
 ↓
Goal
 ↓
Scope
 ↓
Research Questions
 ↓
Literature Review
 ↓
Research Gap
 ↓
Working Title
 ↓
Decision Gates
```

### Outputs

- Research Charter,
- Research Question matrix,
- title candidates,
- literature matrix 10–15 recent papers minimum for Capstone foundation,
- indexing verification,
- gap map.

---

## Phase 1 — Data Provenance & Temporal Integrity

```text
Source audit
 ↓
Raw data registry
 ↓
Coverage audit
 ↓
Timestamp availability
 ↓
Missingness
 ↓
Deduplication
 ↓
Temporal alignment
 ↓
Leakage audit
```

### Outputs

- provenance manifest,
- source registry,
- data dictionary,
- temporal contract,
- leakage audit report.

---

## Phase 2 — Target & Price Dynamics

```text
Nominal price
 ↓
Target candidate construction
 ↓
Historical feature design
 ↓
Lagging / rolling-safe features
 ↓
Sequence boundary design
 ↓
Validation experiment
```

### Outputs

- locked target definition,
- horizon definition,
- price feature contract,
- sequence contract.

---

## Phase 3 — Multimodal Feature Pipeline

```text
Climate
Sentiment
Macro/BBM
Calendar
Price
   ↓
Feature engineering
   ↓
Cutoff enforcement
   ↓
Scaling / encoding
   ↓
Versioned master dataset
```

### Outputs

- master dataset vX,
- feature registry,
- preprocessing report,
- reproducible transformation pipeline.

---

## Phase 4 — Baseline & Candidate Models

```text
Naive
Price-only regression
ARIMA
Ridge / SVR
RF / XGBoost / LightGBM
BiLSTM
TFT candidate
ARIF-Net candidate
```

### Outputs

- benchmark-ready model suite,
- standardized train interface,
- standardized inference interface.

---

## Phase 5 — ARIF-Net Architecture

Focus:

- explicit historical price,
- multimodal representation,
- fusion,
- SGU,
- shock-weighted objective,
- regularization.

### Outputs

- architecture specification,
- mathematical notation,
- config file,
- model checkpoint protocol.

---

## Phase 6 — Experimental Protocol

Focus:

- chronological train/validation/test,
- validation-only model selection,
- blind test,
- seed,
- repeated runs where feasible,
- experiment registry.

### Outputs

- Experiment Protocol v1,
- experiment IDs,
- logs,
- reproducible command list.

---

## Phase 7 — Benchmark & Ablation

Focus:

- primary benchmark,
- reduced modality,
- no price dynamics,
- no SGU,
- no attention/fusion component as appropriate,
- no shock weighting.

### Outputs

- benchmark table,
- ablation table,
- statistical summary,
- robustness evidence.

---

## Phase 8 — Explainability & Error Analysis

Focus:

- actual residuals,
- attribution,
- attention pattern,
- gate activation,
- shock-period analysis,
- failure cases.

### Outputs

- valid explainability package,
- error-analysis report,
- limitations.

---

## Phase 9 — Product / API

```text
Validated model
      ↓
Inference contract
      ↓
Python inference service
      ↓
Forecast API
      ↓
Web application
```

### Outputs

- inference service,
- API documentation,
- result schema,
- model versioning,
- cached historical forecasts.

---

## Phase 10 — Capstone Freeze

Capstone minimum evidence:

- working web product,
- documented methodology,
- validated dataset pipeline,
- validated baseline + proposed model,
- evaluation evidence,
- screenshots/demo,
- limitations,
- reproducibility instructions,
- research handoff to TA.

---

## Phase 11 — Tugas Akhir Deepening

Setelah Capstone freeze:

- deeper literature gap,
- improved architecture if justified,
- multiple seeds,
- robustness,
- multi-horizon,
- uncertainty,
- cross-domain validation,
- stronger error analysis,
- publication-oriented discussion.

Optional causal/counterfactual design hanya dilakukan jika ada alasan ilmiah dan metodologi baru yang benar-benar dibangun.

---

# 25. Academic Documentation Mapping — UMB Capstone Template

Template Capstone Teknik Informatika Universitas Mercu Buana yang digunakan proyek ini menetapkan struktur BAB I–V dan referensi APA edisi ketujuh. Struktur ini harus menjadi format akhir laporan Capstone. [Source: TEMPLATE CAPSTONE TEKNIK INFORMATIKA MUHAMAD NUR ARIF.docx]

## BAB I — PENDAHULUAN

### 1.1 Latar Belakang

Isi:

- fenomena harga pangan,
- masalah forecasting,
- keterbatasan price-only perspective,
- kebutuhan multimodal information,
- arah solusi.

### 1.2 Identifikasi Permasalahan

Harus spesifik dan dapat diuji.

### 1.3 Tujuan Pengembangan

Selaras dengan regression forecasting + product.

### 1.4 Manfaat

- praktis,
- akademik,
- informasional.

### 1.5 Ruang Lingkup dan Batasan

Jangan melebihi dataset dan methodology actual.

### 1.6 Target Luaran Capstone

Minimal:

- web/application product,
- model pipeline,
- dokumentasi,
- evaluation evidence.

## BAB II — LANDASAN DAN ANALISIS SOLUSI

### 2.1 Landasan Teori dan Teknologi

Dapat mencakup:

- time-series forecasting,
- regression,
- price dynamics,
- multimodal learning,
- LSTM/BiLSTM,
- attention,
- fusion,
- shock-aware objective,
- sentiment analysis,
- climate features,
- XAI.

### 2.2 Studi Terkait

Target minimum awal:

- 10–15 paper recent 3–5 tahun,
- verifikasi Scopus/Sinta 1–3 sesuai kebutuhan kampus,
- matrix per paper: data, target, method, modalities, metrics, findings, limitations, gap.

### 2.3 Alternatif Solusi

Bandingkan:

- price-only,
- multivariate tabular,
- sequential deep learning,
- multimodal fusion.

### 2.4 Solusi yang Dipilih

Pilih berdasarkan problem, requirements, evidence literature, dan experiment—not hype.

## BAB III — METODE PENGEMBANGAN

### 3.1 Tahapan Pengembangan Capstone

Gunakan unified pipeline.

### 3.2 Metode Pengembangan

Pisahkan:

- software/product development,
- research/model development.

### 3.3 Data dan Sumber Data

Harus lengkap dengan provenance.

### 3.4 Perangkat dan Teknologi

Contoh:

- Python,
- PyTorch,
- pandas,
- scikit-learn,
- Transformers,
- FastAPI bila digunakan,
- Next.js/React bila product layer digunakan,
- database/result store sesuai final architecture.

### 3.5 Metode Pengujian

Harus meliputi:

- product functional testing,
- inference consistency,
- model metrics,
- benchmark,
- shock subset,
- limitations.

## BAB IV — PERANCANGAN, IMPLEMENTASI, DAN EVALUASI

Template mencakup:

- 4.1 Gambaran Sistem,
- 4.1.1 Kondisi Sistem Saat Ini,
- 4.1.2 Target Produk yang Dikembangkan,
- 4.1.3 Gambaran Umum Produk,
- 4.2 Analisis Kebutuhan,
- 4.2.1 Karakteristik Pengguna,
- 4.2.2 Functional Requirements,
- 4.2.3 Non-Functional Requirements,
- 4.3 Desain dan Arsitektur Produk,
- 4.4 Implementasi,
- 4.5 Pengujian dan Evaluasi Produk. [Source: TEMPLATE CAPSTONE TEKNIK INFORMATIKA MUHAMAD NUR ARIF.docx]

## BAB V — PENUTUP

- 5.1 Kesimpulan,
- 5.2 Rencana Pengembangan pada Tugas Akhir.

## Referensi

Template mengharuskan **APA edisi ketujuh** dan penggunaan reference manager seperti Mendeley/Zotero. [Source: TEMPLATE CAPSTONE TEKNIK INFORMATIKA MUHAMAD NUR ARIF.docx]

---

# 26. Product Vision — ARIF Food Intelligence

## 26.1 Product purpose

Website harus menjawab secara visual:

> “Bagaimana kondisi harga sekarang, bagaimana forecast berikutnya, dan konteks multimodal apa yang dipakai model untuk menghasilkan forecast tersebut?”

Website bukan sekadar:

```text
input → angka prediksi
```

Melainkan:

```text
Data
 ↓
Context
 ↓
Forecast
 ↓
Explanation
 ↓
Evidence
```

## 26.2 Core user journey

```text
Landing
  ↓
Pilih komoditas / periode
  ↓
Lihat current price
  ↓
Lihat historical trend
  ↓
Lihat forecast
  ↓
Lihat climate context
  ↓
Lihat news sentiment context
  ↓
Lihat macro/logistics event
  ↓
Lihat model explanation
  ↓
Lihat evidence / experiment
```

## 26.3 Proposed routes

| Route | Purpose |
|---|---|
| `/` | Project story + snapshot |
| `/forecast` | Forecast center |
| `/analysis/price` | Price dynamics |
| `/analysis/sentiment` | News/sentiment |
| `/analysis/climate` | Climate context |
| `/analysis/macro` | Macro/logistics |
| `/monitoring` | Secondary extreme movement monitoring |
| `/model` | Model architecture & methodology |
| `/research` | Research evidence & limitations |
| `/experiments` | Benchmark & ablation |

## 26.4 Product design principle

Public-first lebih cocok untuk pameran dan academic demonstration.

Gunakan precomputed historical forecast untuk eksplorasi stabil. Live inference dapat dibatasi sesuai resource deployment dan reliability.

---

# 27. Product Architecture

Proposed architecture:

```text
┌────────────────────────────┐
│ Next.js / React Frontend   │
│ Dashboard + Research UI    │
└─────────────┬──────────────┘
              │ HTTPS/API
              ▼
┌────────────────────────────┐
│ Forecast / Analysis API    │
└─────────────┬──────────────┘
              ▼
┌────────────────────────────┐
│ Python Inference Service   │
│ Preprocessing Contract     │
│ ARIF-Net / Candidate Model │
└─────────────┬──────────────┘
              ▼
┌────────────────────────────┐
│ Versioned Data / Results   │
│ Model artifacts            │
└────────────────────────────┘
```

Product implementation tidak boleh mengubah preprocessing model secara berbeda dari research preprocessing tanpa versioning dan explicit transformation contract.

---

# 28. Functional Requirements — Product Baseline

| ID | Requirement |
|---|---|
| FR-01 | User dapat melihat current/historical commodity price. |
| FR-02 | User dapat memilih tanggal/period yang didukung. |
| FR-03 | User dapat melihat forecast periode berikutnya. |
| FR-04 | User dapat melihat reconstructed predicted price jika target menggunakan pct change. |
| FR-05 | User dapat melihat forecast movement. |
| FR-06 | User dapat melihat price history dan volatility context. |
| FR-07 | User dapat melihat climate context. |
| FR-08 | User dapat melihat sentiment/news context. |
| FR-09 | User dapat melihat macro/logistics context. |
| FR-10 | User dapat melihat methodology/model explanation. |
| FR-11 | User dapat melihat benchmark/ablation evidence sesuai public scope. |
| FR-12 | Forecast result mempunyai model/data version. |

---

# 29. Non-Functional Requirements — Product Baseline

## Performance

- dashboard responsif,
- forecast retrieval tidak harus menjalankan full training,
- historical exploration menggunakan cache/precomputed artifacts bila sesuai.

## Reliability

- API tidak boleh menghasilkan angka tanpa model version,
- missing modality harus ditangani secara eksplisit,
- incompatible data schema harus ditolak, bukan diam-diam diperbaiki.

## Reproducibility

- inference harus menggunakan preprocessing contract yang sama dengan training.

## Transparency

- product harus dapat menjelaskan sumber data dan batasan.

## Security

- tidak ada secret key di frontend,
- API credentials disimpan server-side,
- external data access terkontrol.

---

# 30. Research Software Architecture

Suggested repository organization ke depan:

```text
ARIF-Net-Foot-Price-Shock/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── manifests/
├── preprocessing/
├── features/
├── modeling/
│   ├── baselines/
│   ├── arif_net/
│   ├── candidates/
│   └── evaluation/
├── experiments/
│   ├── configs/
│   ├── logs/
│   └── manifests/
├── models/
├── results/
├── notebooks/
├── product/
│   ├── api/
│   └── web/
├── docs/
│   ├── research/
│   ├── methodology/
│   ├── data/
│   ├── architecture/
│   └── experiments/
└── README.md
```

Ini adalah target organization, bukan klaim struktur repository saat ini.

---

# 31. Versioning Strategy

## 31.1 Project documentation versions

Gunakan Semantic Versioning-like discipline:

```text
MAJOR.MINOR.PATCH
```

### MAJOR

Perubahan pada:

- research goal,
- architecture philosophy,
- core target,
- project scope.

### MINOR

Perubahan pada:

- pipeline stage,
- feature groups,
- product architecture,
- new research phase.

### PATCH

Perubahan pada:

- typo,
- wording,
- source link,
- clarification,
- non-semantic correction.

## 31.2 Document freshness metadata

Setiap release dokumen resmi wajib memuat:

```text
Document Version
Last Validated
Repository Commit / Tag
Dataset Version
Model Version
Experiment Protocol Version
Literature Review Cutoff
Known Open Decisions
Known Deprecated Claims
```

## 31.3 Revalidation triggers

Dokumen wajib direview ulang jika salah satu terjadi:

- target model berubah,
- data source berubah,
- dataset rebuilt,
- preprocessing logic berubah,
- model architecture berubah,
- split protocol berubah,
- metrics berubah,
- product inference contract berubah,
- paper/research gap baru mengubah framing,
- Capstone/TA requirements berubah.

---

# 32. Official Source-of-Truth Hierarchy

Saat terjadi konflik informasi, gunakan urutan berikut.

## Level 1 — Researcher-approved decisions

Contoh:

- goal yang dikunci,
- decision gate yang sudah disetujui,
- scope resmi.

## Level 2 — Executable source code

Untuk menjawab “apa yang benar-benar dilakukan code saat ini”, gunakan source code actual.

## Level 3 — Versioned data / experiment artifacts

Untuk angka, metrics, dataset dimensions, gunakan artifact run yang dapat direproduksi.

## Level 4 — Official project documentation

Markdown/PDF implementation plan berfungsi menyatukan konsep dan design.

## Level 5 — README / presentation-oriented docs

README dapat ringkas tetapi harus diverifikasi sebelum dipakai untuk academic claim.

## Level 6 — External literature / web research

Digunakan untuk teori, related work, standards, technology update, and literature gap.

### Conflict rule

Jika README mengatakan sesuatu yang code tidak lakukan, **code adalah fakta implementasi aktual** dan README harus diperbaiki.

Jika code melakukan sesuatu yang belum disetujui secara metodologis, code adalah **observed implementation**, bukan otomatis keputusan penelitian.

---

# 33. Strict AI Governance Rules

Bagian ini **WAJIB dibaca dan dipatuhi** oleh AI/agent yang menggunakan dokumen ini sebagai knowledge base.

## RULE 01 — Do not change the core goal

AI tidak boleh menggeser:

```text
multimodal regression forecasting
```

menjadi:

```text
classification / shock detection as primary task
```

kecuali project owner secara eksplisit memutuskan perubahan tersebut.

## RULE 02 — Historical price is mandatory

AI tidak boleh merancang final model yang sepenuhnya menghilangkan historical price dynamics.

## RULE 03 — Do not silently choose OPEN decisions

Untuk item berstatus `OPEN`, AI harus:

- menjaga beberapa kandidat,
- menjelaskan trade-off,
- menyebut item sebagai decision gate.

AI tidak boleh menulis seolah-olah keputusan sudah final.

## RULE 04 — No invented facts

Dilarang mengarang:

- dataset count,
- source,
- paper,
- experiment result,
- benchmark,
- model architecture,
- deployment status,
- user number,
- API behavior.

## RULE 05 — No fabricated results

Dilarang membuat:

- RMSE,
- MAE,
- R²,
- accuracy,
- shock recall,
- SHAP percentage,
- confidence interval,
- significance test,

tanpa output eksperimen yang nyata.

## RULE 06 — No fabricated literature

Jangan membuat DOI, journal name, volume, indexing status, paper title, atau citation yang belum diverifikasi.

## RULE 07 — Novelty must be evidence-based

Jangan menyebut:

- “novel” final,
- “first”,
- “rare”,
- “state-of-the-art”,
- “Q1-worthy”,

hanya berdasarkan intuisi.

Gunakan wording:

> “potential contribution”

sampai literature gap dan evidence tervalidasi.

## RULE 08 — No causal overclaim

Correlation/SHAP/attention/gating ≠ causal effect.

## RULE 09 — Do not misuse XGBoost SHAP

SHAP pada XGBoost baseline tidak boleh disebut sebagai explanation of ARIF-Net.

## RULE 10 — No synthetic evidence

Data sintetis, random-generated error curve, hardcoded graph, dummy news, atau placeholder values tidak boleh dilaporkan sebagai empirical result.

## RULE 11 — Test set is sacred

Test set tidak boleh dipakai untuk model selection/tuning/checkpoint.

## RULE 12 — Code review precedes methodology claims

Jika user meminta review terhadap implementasi, AI harus membaca code actual terlebih dahulu.

## RULE 13 — Do not trust README blindly

README adalah documentation layer, bukan bukti final implementasi.

## RULE 14 — Preserve terminology accuracy

Jika code memakai `ShockWeightedLoss` dengan MSE, gunakan:

> Shock-Weighted MSE

bukan focal loss.

## RULE 15 — Every strong claim needs evidence category

AI harus bisa mengklasifikasikan klaim sebagai:

```text
FACT / OBSERVED
PROPOSED
OPEN
INFERENCE
EXTERNAL RESEARCH
```

## RULE 16 — Never hide uncertainty

Jika informasi kurang, katakan:

> “Belum terverifikasi dari source yang tersedia.”

Bukan mengisi kekosongan dengan asumsi.

## RULE 17 — Do not over-engineer

Tambahan technique harus punya alasan terhadap RQ atau product requirement.

Jangan menambah:

- transformer,
- graph neural network,
- reinforcement learning,
- causal model,
- agent,
- multi-task learning,

hanya agar terlihat canggih.

## RULE 18 — Every method must connect to an RQ

Jika technique tidak membantu RQ atau kebutuhan product yang valid, technique tersebut harus dipertanyakan.

## RULE 19 — Reproducibility over aesthetics

Paper-style graphics tidak lebih penting daripada validitas data/experiment.

## RULE 20 — Product cannot conceal research limitations

Website harus menunjukkan limitations secara jujur.

## RULE 21 — Separate current state from target state

Gunakan label:

```text
CURRENT / OBSERVED
TARGET / PROPOSED
```

## RULE 22 — Do not rewrite project history

Known bad implementation tetap dicatat sebagai histori. Jangan mengklaim bahwa masalah tidak pernah ada.

## RULE 23 — Do not silently reconcile contradictions

Jika dua source bertentangan:

1. tampilkan conflict,
2. cek authority hierarchy,
3. pilih sumber berdasarkan evidence,
4. dokumentasikan perubahan.

## RULE 24 — Methodology changes require impact analysis

Setiap perubahan target/model/split/feature wajib dianalisis dampaknya terhadap:

- RQ,
- experiments,
- metrics,
- report chapters,
- product API,
- existing artifacts.

## RULE 25 — Preserve user agency

AI boleh merekomendasikan, tetapi keputusan metodologi akhir tetap milik project owner.

---

# 34. Mandatory AI Response Protocol

Ketika AI diberi tugas terkait ARIF-Net, sebelum menghasilkan output AI harus secara internal mengikuti urutan:

```text
1. IDENTIFY TASK
       ↓
2. LOAD THIS DOCUMENT
       ↓
3. DETERMINE RELEVANT SOURCE
       ↓
4. CHECK CURRENT REPOSITORY / FILE IF NEEDED
       ↓
5. CLASSIFY INFORMATION
   FACT / PROPOSED / OPEN / DEPRECATED
       ↓
6. CHECK AGAINST LOCKED GOAL
       ↓
7. CHECK TEMPORAL / METHODOLOGICAL VALIDITY
       ↓
8. PRODUCE OUTPUT
       ↓
9. STATE DECISION GATES IF ANY
       ↓
10. DO NOT INVENT EVIDENCE
```

## 34.1 Jika diminta mengubah arsitektur

AI harus menjawab secara struktur:

```text
Current architecture
↓
Problem identified
↓
Why it matters to goal/RQ
↓
Candidate alternatives
↓
Expected trade-off
↓
Required experiment
↓
Decision gate
```

## 34.2 Jika diminta memperbaiki code

AI harus:

```text
Inspect current code
↓
Locate exact issue
↓
Explain effect
↓
Define acceptance criteria
↓
Patch/refactor
↓
Run tests
↓
Document changed behavior
```

## 34.3 Jika diminta menulis akademik

AI harus:

- mengikuti struktur template kampus,
- menggunakan APA 7 untuk format Capstone sesuai template,
- tidak mengarang hasil,
- memisahkan evidence dari interpretation,
- menandai placeholder yang belum tersedia.

---

# 35. Sprint Plan — Canonical Implementation Roadmap

## S0 — Research Contract & Literature

### Goals

- freeze problem framing,
- confirm RQ,
- collect 10–15 recent papers,
- build literature gap matrix.

### Deliverables

- Research Charter,
- Literature Matrix,
- Working Title Matrix,
- Decision Register.

### Exit criteria

Tidak ada RQ yang tidak terhubung ke experiment.

---

## S1 — Data Provenance & Temporal Integrity

### Tasks

- audit all source URLs,
- audit coverage,
- source license/terms,
- publication timestamps,
- missingness,
- duplicates,
- ffill/bfill,
- rolling statistics,
- scaling boundary,
- sequence boundary.

### Exit criteria

Dataset dapat dipertanggungjawabkan secara temporal.

---

## S2 — Target & Price Dynamics

### Tasks

- implement the Phase-0-decided relative-movement target,
- implement multi-horizon target construction up to 365 days, subject to effective-observation feasibility,
- implement explicit historical price backbone,
- repair sequence boundary,
- test price-only baseline.

### Exit criteria

Model benar-benar memiliki historical price information.

---

## S3 — Multimodal Feature Pipeline

### Tasks

- climate feature registry,
- sentiment provenance,
- macro event representation,
- calendar features,
- temporal cutoff enforcement,
- feature schema.

### Exit criteria

Master dataset versioned dan reproducible.

---

## S4 — Baseline & Candidate Models

### Tasks

- naive baseline,
- price-only baseline,
- conventional multivariate baseline,
- BiLSTM,
- TFT candidate,
- ARIF-Net candidate.

### Exit criteria

Semua model menggunakan protocol yang sama.

---

## S5 — ARIF-Net Architecture

### Tasks

- explicit price representation,
- temporal encoder,
- external encoder,
- fusion,
- SGU,
- Shock-Weighted MSE,
- architecture config.

### Exit criteria

Architecture spec dan implementation match.

---

## S6 — Experimental Protocol

### Tasks

- chronological split,
- validation selection,
- blind test,
- seeds,
- experiment tracking,
- config versioning.

### Exit criteria

Test set tidak digunakan untuk selection.

---

## S7 — Benchmark & Ablation

### Tasks

- full benchmark,
- modality ablation,
- no-price ablation,
- no-SGU,
- no-shock-weighting,
- optional no-attention.

### Exit criteria

Contribution evidence tersedia.

---

## S8 — Explainability & Error Analysis

### Tasks

- actual residual curve,
- actual rolling error,
- model-specific attribution,
- attention diagnostics,
- gate activation,
- failure cases.

### Exit criteria

Tidak ada synthetic/hardcoded evidence.

---

## S9 — Product/API

### Tasks

- inference schema,
- API,
- result cache,
- dashboard,
- methodology page,
- experiment page.

### Exit criteria

User dapat mengikuti data → forecast → context → evidence.

---

## S10 — Product Testing & Capstone Freeze

### Tasks

- functional testing,
- API testing,
- inference consistency,
- performance smoke test,
- documentation,
- exhibition flow,
- screenshot evidence.

### Exit criteria

Capstone package ready.

---

## S11 — TA Deepening

### Candidate extensions

- stronger baseline,
- multiple seed statistical summary,
- additional robustness/uncertainty analysis,
- generalized dataset,
- cross-location/commodity beyond the Phase-0 priority scope,
- publication manuscript.

---

# 36. Decision Register

## Current gates

| ID | Decision | Status |
|---|---|---|
| DG-01 | Primary task = supervised regression forecasting | `LOCKED` |
| DG-02 | Historical price = explicit backbone/input wajib | `LOCKED` |
| DG-03 | Target internal = relative price movement / percentage change | `DECIDED` |
| DG-04 | Direct price = reconstructed product output | `DECIDED` |
| DG-05 | Forecast = multi-horizon, maximum 365 days | `DECIDED` |
| DG-06 | Standard horizon grid = 1/3/7/14/30/90/180/365 | `DECIDED` |
| DG-07 | Priority commodities = CMK, bawang merah, beras | `DECIDED` |
| DG-08 | Jakarta = forecast target market | `DECIDED` |
| DG-09 | External modalities = climate/supply, news/sentiment, macro/logistics + calendar support | `LOCKED DIRECTION` |
| DG-10 | Supplier-region mapping must be evidence-based | `LOCKED` |
| DG-11 | Reliability-aware + horizon-conditioned fusion | `CANDIDATE / HYPOTHESIS` |
| DG-12 | Shock = horizon-scaled empirical threshold; Q95 primary | `DECIDED` |
| DG-13 | 3% threshold retained only as legacy/sensitivity reference | `DECIDED` |
| DG-14 | Validation-only model selection; blind test | `LOCKED` |
| DG-15 | Capstone + TA = one continuous pipeline | `LOCKED` |
| DG-16 | Novelty = candidate until ablation/blind evidence | `LOCKED BOUNDARY` |
| DG-17 | Counterfactual policy simulation | `FUTURE / OPTIONAL` |

**Catatan v2.0.0:** DG-07 dan DG-08 di atas diamandemen oleh P1-DG-02/04/05 (komoditas: CMK, Bawang Merah Ukuran Sedang, Beras Kualitas Medium I; target market: Pasar Kramatjati, Jakarta). Register lengkap Phase 1 ada di §0.5.

---

# 37. Research Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Test leakage | Invalid final metrics | Temporal train/val/test + blind test |
| Future information | Artificially strong performance | Availability/cutoff audit |
| Historical price missing from input | Goal mismatch | Explicit price dynamics input |
| News data quality | Weak/noisy modality | Provenance + relevance filter |
| Sentiment fallback hidden | Method mismatch | Record actual model used |
| Full-period imputation | Leakage | Split-aware transformation |
| Hardcoded analysis | False evidence | Replace with actual computed analysis |
| Synthetic residual | False conclusion | Use actual predictions/residuals |
| Causal language | Academic overclaim | Predictive contribution language |
| Overfitting | Poor generalization | Validation + multiple seeds |
| Too many features | Complexity/noise | Feature governance + ablation |
| TFT hype | Unnecessary rewrite | Benchmark candidate |
| Dashboard-only contribution | Weak academic value | Show model/evidence/limitations |
| Preliminary numbers used as final | Invalid conclusion | Freeze final experiment protocol |
| Pengisian null lintas sumber/level harga | Bias level harga, leakage kalibrasi | P1-DG-06 safeguards 1–5 |
| Reanalysis ≠ observasi stasiun | Bias lokal iklim | Label provenance + Limitations |
| Release lag iklim diabaikan | Future information | P1-DG-17 (≤ t−5) |
| Centroid di luar lahan sentra | Sinyal iklim kurang representatif | Limitations; Tier 2 sebagai pembanding |
| Seri harga eceran lengket | Q95 = 0, DA ambigu, R² tidak stabil | P1-DG-08, P1-DG-23 |

---

# 38. Definition of Done — Research

ARIF-Net research stage hanya dapat dianggap valid untuk final reporting jika:

### Phase-0 contract compliance

- [ ] Target internal menggunakan relative price movement / percentage change.
- [ ] Forecasting menggunakan multi-horizon contract dan tidak melebihi 365 hari.
- [ ] Historical price hadir sebagai explicit backbone/input.
- [ ] Priority commodity taxonomy dan target market telah dikunci pada Data Contract.
- [ ] Future realized external information tidak masuk ke input forecast origin.
- [ ] Shock threshold primary dihitung split-aware dengan Q95 training distribution per horizon.
- [ ] Legacy 3% hanya digunakan sebagai comparison/sensitivity reference.
- [ ] Test set tidak digunakan untuk model/threshold/architecture selection.



- [ ] goal dan RQ konsisten,
- [ ] target dan horizon terdokumentasi,
- [ ] dataset provenance tersedia,
- [ ] source availability diketahui,
- [ ] historical price dynamics eksplisit,
- [ ] temporal leakage audit selesai,
- [ ] imputation split-aware,
- [ ] scaling train-only,
- [ ] sequence boundary valid,
- [ ] train/validation/test dipisahkan secara kronologis,
- [ ] model selection hanya menggunakan validation,
- [ ] test blind,
- [ ] baseline protocol identik,
- [ ] ARIF-Net protocol identik,
- [ ] shock threshold konsisten,
- [ ] ablation selesai untuk komponen inti,
- [ ] explainability sesuai model yang sebenarnya,
- [ ] synthetic/hardcoded evidence dihapus,
- [ ] final metrics reproducible,
- [ ] limitations ditulis,
- [ ] literature gap tervalidasi.

---

# 39. Definition of Done — Product

- [ ] user dapat memilih komoditas/periode yang didukung,
- [ ] historical price tampil,
- [ ] forecast tampil,
- [ ] forecast movement tampil,
- [ ] context multimodal tampil,
- [ ] model methodology tersedia,
- [ ] benchmark/ablation dapat dijelaskan,
- [ ] model/data version tersedia,
- [ ] product tidak membuat causal claims yang tidak didukung,
- [ ] API dan inference contract konsisten,
- [ ] demo exhibition memiliki alur singkat,
- [ ] limitations terlihat.

---

# 40. Academic Writing Rules

## 40.1 Language

Untuk laporan kampus gunakan Bahasa Indonesia formal.

Foreign terms dapat ditulis *italic* bila sesuai kebutuhan akademik.

## 40.2 Claim discipline

Bedakan:

```text
Observed result
vs
Interpretation
vs
Hypothesis
vs
Literature claim
```

## 40.3 Forbidden claim pattern

Jangan:

> “Model membuktikan climate menyebabkan harga naik.”

Gunakan:

> “Hasil attribution menunjukkan climate-related features memiliki kontribusi prediktif yang besar terhadap output model pada dataset/evaluasi tersebut.”

## 40.4 Result reporting

Gunakan:

- exact metric,
- test period,
- dataset version,
- comparison model,
- direction of metric (higher/lower better),
- limitations.

---

# 41. Literature Review Protocol

Karena proyek ditujukan untuk Capstone → TA → optional international publication, literature review harus bertahap.

## Capstone minimum

- 10–15 paper recent,
- target 3–5 tahun terakhir sesuai requirement akademik yang berlaku,
- status Scopus/Sinta diverifikasi,
- focus pada food price forecasting, multimodal forecasting, climate-price modeling, sentiment/news forecasting, deep time-series, explainable forecasting.

## TA / publication extension

Perluasan:

- lebih banyak paper,
- systematic search terms,
- inclusion/exclusion criteria,
- method comparison,
- clear research gap.

### Literature matrix fields

| Field | Isi |
|---|---|
| Citation | APA 7 reference record |
| Year | Tahun |
| Indexing | Scopus/Sinta status |
| Domain | Food/agriculture/etc. |
| Target | Price/return/shock/etc. |
| Data | Price/climate/news/macro |
| Method | Model |
| Horizon | t+1 / multi-horizon |
| Metrics | RMSE/MAE/etc. |
| Main finding | Ringkas |
| Limitation | Ringkas |
| Relevance to ARIF-Net | Tinggi/Sedang/Rendah |
| Gap | Apa yang belum disentuh |

---

# 42. What Can Be Reused From Current Repository

| Component | Reuse Status | Action |
|---|---|---|
| Raw data organization | `HIGH` | Keep + provenance manifest |
| Commodity preprocessing | `HIGH` | Audit fill/boundary |
| Climate preprocessing | `MEDIUM-HIGH` | Reuse + leakage audit |
| BBM preprocessing | `HIGH` | Reuse + source audit |
| Sentiment preprocessing | `HIGH` | Reuse if model provenance is recorded |
| Master dataset builder | `MEDIUM` | Refactor split-aware |
| BiLSTM encoder | `HIGH` | Candidate temporal encoder |
| Temporal attention | `HIGH` | Candidate, correct terminology |
| Macro branch | `MEDIUM-HIGH` | Reassess time-varying semantics |
| SGU | `HIGH` | Keep candidate + ablation |
| Shock-weighted MSE | `HIGH` | Keep with correct terminology |
| Baseline suite | `HIGH` | Re-run under valid protocol |
| Ablation code | `HIGH` | Re-run after protocol fix |
| XGBoost SHAP | `MEDIUM` | Baseline-only explanation |
| Synthetic/hardcoded advanced analysis | `LOW` | Remove from evidence |
| Notebooks | `MEDIUM` | Repair/reconcile with current scripts |

---

# 43. Known Current-State Findings

This section is a factual audit snapshot, not the target architecture.

### A. Test leakage in ARIF-Net training — VERIFIED

Current training evaluates the test set each epoch and saves the best checkpoint using that value. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_arif_net.py

### B. Loss naming mismatch — VERIFIED

Current formula is weighted MSE while old documentation calls it focal loss. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_arif_net.py

### C. Shock threshold mismatch — VERIFIED

Actual shock uses 3%; predicted shock recall currently uses 2%. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/evaluate_models.py

### D. XGBoost SHAP ≠ ARIF-Net explanation — VERIFIED

`explainability.py` loads XGBoost model for SHAP. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/explainability.py

### E. Synthetic rolling error — VERIFIED

Current advanced analysis uses random generated error values. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/advanced_analysis.py

### F. Hardcoded causal graph — VERIFIED

Causal interaction graph edge weights are hardcoded. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/advanced_analysis.py

### G. Current model attention is single temporal attention — VERIFIED

Implementation uses `Linear(hidden_dim,1)` + softmax over sequence, not multi-head attention. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_arif_net.py

### H. Sentiment has fallback — VERIFIED

The pipeline tries candidate transformer sentiment models and falls back to a domain lexicon if none is available. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/preprocessing/preprocess_sentimen.py

### I. Master dataset creates target-derived features — VERIFIED

The current builder creates `target_pct_change`, `target_volatility_7d`, moving averages, spike flag, and MA deviation. Some are excluded from current model features, but their creation/pipeline must still be audited for temporal leakage. https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/preprocessing/build_master_dataset.py

### J. Repository contains 12 commits and current directory structure — VERIFIED snapshot

Current public repository page shows 12 commits and the main folders `data`, `modeling`, `models`, `notebook`, `preprocessing`, `results`, and `scraping_data`, plus project documentation. https://github.com/ariftsx/ARIF-Net-Foot-Price-Shock

---

# 44. Current Documentation Conflicts / Deprecated Claims

The following old statements must not be used as current truth:

1. “ARIF-Net is already state-of-the-art.”
2. “ARIF-Net is a standard/new benchmark” without literature evidence.
3. “ARIF-Net proves causal relationships.”
4. “SHAP values are ARIF-Net SHAP” when using current XGBoost SHAP script.
5. “Shock-Weighted Focal Loss” for the current weighted-MSE implementation.
6. “Dynamic Multi-Head Attention” for current single temporal attention implementation.
7. “All baselines fail” or similarly universal claims.
8. “ARIF-Net wins every metric.”
9. “Counterfactual scenarios are directly supported by ordinary forecasting.”

These claims may exist in historical documentation for audit purposes, but they are `DEPRECATED` for new research writing.

---

# 45. Product / Research Separation of Concerns

## Research layer

Responsible for:

- dataset,
- preprocessing,
- modeling,
- experiments,
- metrics,
- attribution,
- scientific conclusions.

## Product layer

Responsible for:

- visualization,
- interaction,
- API,
- deployment,
- caching,
- research storytelling.

## Rule

Product UI must consume versioned research artifacts. UI may not silently recompute the model with different feature logic.

---

# 46. Future Counterfactual / Scenario Analysis

A desired product question may look like:

> “Jika curah hujan naik 20% dan subsidi BBM dihilangkan, bagaimana kemungkinan perubahan harga?”

This is **not automatically a forecasting output**.

Ordinary forecasting answers:

```text
Given observed/assumed inputs → predicted outcome
```

Counterfactual asks:

```text
If an intervention changes X while holding/adjusting other variables appropriately,
what would happen to Y?
```

The second question requires stronger assumptions and potentially causal modeling.

Therefore:

```text
Capstone
  → descriptive scenario visualization only, if carefully framed

TA / Research Extension
  → causal/counterfactual modeling only if formally justified
```

Never present a naive “change input by +20% and run model” as causal effect.

---

# 47. Expected Capstone Exhibition Story

Demonstration should be explainable in approximately this sequence:

```text
1. Food price is dynamic
        ↓
2. Historical price alone may miss external context
        ↓
3. Climate + News + Macro provide additional signals
        ↓
4. ARIF-Net fuses these signals
        ↓
5. Model forecasts next price movement
        ↓
6. User can inspect the supporting context
        ↓
7. User can see benchmark/evidence
        ↓
8. User can see limitations
```

A visitor should understand the research problem without reading the thesis first.

---

# 48. Handoff Contract for Other AI

Ketika dokumen ini diberikan ke AI lain, AI tersebut harus memperlakukan informasi berikut sebagai baseline:

### Must remember

- Research core = multimodal regression forecasting.
- Historical price dynamics = mandatory input.
- Climate/supply + macro/logistics + news sentiment = external modalities.
- Shock = secondary phenomenon/capability.
- ARIF-Net = proposed research architecture/candidate, not automatically proven best.
- TFT = candidate, not predetermined winner.
- Causal claims = prohibited without causal methodology.
- Current benchmark numbers = preliminary.
- Current repository has known experimental/documentation issues.
- Capstone and TA = one unified pipeline.
- Product = ARIF Food Intelligence working name.

### Must verify before asserting

- exact dataset size,
- exact final dates,
- exact model metrics,
- final target/horizon,
- final architecture,
- final literature gap,
- final novelty statement,
- actual sentiment model used in a run,
- final deployment status.

### Must not do

- invent evidence,
- fabricate papers,
- silently change goal,
- turn regression into classification,
- call predictive attribution causal,
- call XGBoost SHAP ARIF-Net SHAP,
- use synthetic graphs as empirical results.

---

# 49. Immediate Implementation Priority

The safest execution order is:

```text
P0. Research Contract
        ↓
P1. Data / Temporal Audit
        ↓
P2. Explicit Price Dynamics
        ↓
P3. Train/Validation/Test Repair
        ↓
P4. Rebuild Baselines
        ↓
P5. Rebuild ARIF-Net
        ↓
P6. Ablation
        ↓
P7. Explainability / Error Analysis
        ↓
P8. Freeze Research Evidence
        ↓
P9. Build Product
        ↓
P10. Capstone Evidence
        ↓
P11. TA Deepening
```

Jangan membangun website final sebelum core inference contract dan result validity cukup stabil.

---

# 50. Final Project Positioning

## Research

**Multimodal Food Price Forecasting and Intelligence**

## Research task

**Supervised multimodal regression forecasting**

## Input information

**Historical price dynamics + climate/supply + news sentiment + macro/logistics**

## Secondary capability

**Shock-aware learning + extreme-movement monitoring**

## Model

**ARIF-Net** sebagai proposed/candidate multimodal architecture yang masih harus divalidasi secara fair.

## Product

**ARIF Food Intelligence** sebagai web-based productization layer.

## Capstone

Working product + validated research foundation + BAB I–III/IV/V sesuai template dan ketentuan mata kuliah yang berlaku.

## Tugas Akhir

Same pipeline + deeper experimental evidence + stronger scientific validation.

## Long-term research

Optional extension menuju multimodal early-warning framework, uncertainty, generalization, atau causal/counterfactual extension apabila memiliki justifikasi metodologis.

---

# 51. Document Validation / Freshness Checklist

Dokumen ini dianggap **current** hanya apabila checklist berikut diperiksa setelah perubahan besar:

### Repository validation

- [ ] Repository URL masih benar.
- [ ] Current branch/commit dicatat.
- [ ] Relevant source files masih sesuai.
- [ ] Architecture implementation diverifikasi.

### Dataset validation

- [ ] Date range diverifikasi.
- [ ] Row count diverifikasi.
- [ ] Source provenance diverifikasi.
- [ ] Feature list diverifikasi.
- [ ] Leakage audit terbaru tersedia.

### Experiment validation

- [ ] Split protocol dicatat.
- [ ] Validation selection dicatat.
- [ ] Test blind.
- [ ] Seed/config dicatat.
- [ ] Metrics generated from reproducible run.

### Research validation

- [ ] Goal masih konsisten.
- [ ] RQ masih konsisten.
- [ ] Literature gap terbaru.
- [ ] Novelty wording tidak overclaim.

### Product validation

- [ ] Inference contract sama dengan training contract.
- [ ] Model/data version tersedia.
- [ ] UI tidak menampilkan klaim tidak terverifikasi.

---

# 52. Change Log

## v2.0.0 — 02 Oktober 2026

**Phase 1 scope revision (MAJOR).** Perubahan berdasarkan P1-DG-01 s.d. P1-DG-24 (§0.5):

- sumber harga target → PIHPS Bank Indonesia; PIBC & IPJ sebagai sumber pelengkap;
- target market → Pasar Kramatjati (eceran, level-3); PIKJ/PIBC bukan lagi target market;
- komoditas primary evidence → CMK, Bawang Merah Ukuran Sedang, Beras Kualitas Medium I; bawang putih dikeluarkan;
- aturan pengisian null multi-sumber dengan safeguards;
- horizon dalam hari kalender; known issue Q95 pada seri lengket;
- sumber iklim → Open-Meteo (ERA5-Seamless), 9 variabel core + reserve, centroid kabupaten, mulai 2018-01-01, release lag ≤ t−5;
- wilayah pemasok Tier 1/Tier 2 untuk 3 komoditas;
- validasi kronologis/rolling-origin; metrik final termasuk R² sebagai pelengkap;
- arsitektur tetap mengikuti Contract §9 (tidak berubah).

## v1.1.0 — 28 September 2026

**Post-Phase-0 synchronization release.** Implementation Plan diselaraskan dengan `ARIF-Net_Phase_0_Research_Contract_v2.0.0.md` yang telah frozen pada 24 September 2026.

Perubahan utama:

- target relative price movement / percentage change menjadi keputusan aktif;
- multi-horizon maksimum 365 hari menjadi kontrak aktif;
- explicit historical price backbone menjadi requirement terkunci;
- scope prioritas menjadi CMK, bawang merah, dan beras dengan Jakarta sebagai forecast market;
- supplier-region mapping dan temporal availability menjadi kontrak Phase 1;
- shock definition berpindah dari fixed 3% ke horizon-scaled empirical threshold dengan Q95 training sebagai primary;
- 3% dipertahankan sebagai legacy/sensitivity reference;
- Decision Register diperbarui agar tidak lagi membuka keputusan yang sudah frozen;
- reliability-aware/horizon-conditioned fusion tetap candidate dan tidak dipromosikan menjadi novelty final;
- Phase 1 handoff disesuaikan dengan deliverables Research Contract v2.0.0.

## v1.0.0 — 22 September 2026

Initial official baseline knowledge base (historical baseline).

Scope included:

- project identity,
- research goal,
- reasoning foundation,
- scope,
- target/horizon governance,
- triple-shock framework,
- data contract,
- pipeline,
- current repository audit snapshot,
- model architecture,
- evaluation framework,
- preliminary results disclaimer,
- explainability governance,
- product direction,
- Capstone mapping,
- TA continuity,
- sprint roadmap,
- decision register,
- strict AI rules,
- documentation freshness protocol.

Historical v1.0.0 intentionally did **not** freeze final target and final horizon. Those historical OPEN statuses are superseded by the Phase-0 freeze and must not be used as active project decisions.

---

# 53. Primary Source Register

## Project repository

- Repository: https://github.com/ariftsx/ARIF-Net-Foot-Price-Shock
- README: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/README.md
- Current implementation plan (historical/current repo): https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/IMPLEMENTATION%20PLAN.md
- Research documentation (historical/current repo): https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/DOKUMENTASI_PENELITIAN_ARIF_NET.md

## Key implementation sources

- ARIF-Net training: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_arif_net.py
- Evaluation: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/evaluate_models.py
- Baselines: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/train_baseline.py
- Ablation: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/ablation_study.py
- Explainability: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/explainability.py
- Advanced analysis: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/modeling/advanced_analysis.py
- Master dataset builder: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/preprocessing/build_master_dataset.py
- Sentiment preprocessing: https://raw.githubusercontent.com/ariftsx/ARIF-Net-Foot-Price-Shock/main/preprocessing/preprocess_sentimen.py

## Phase 1 data sources (v2.0.0)

- PIHPS Bank Indonesia — https://www.bi.go.id/hargapangan (endpoint `TabelHarga/GetGridDataKomoditas`)
- PIHPS FAQ / metodologi — https://www.bi.go.id/hargapangan/Informasi/FAQ
- Open-Meteo Historical Weather API — https://open-meteo.com/en/docs/historical-weather-api
- PIBC (Food Station) — https://pibc.foodstation.co.id/ (sumber pelengkap, belum dikoleksi)
- IPJ — sumber pelengkap, URL dicatat saat koleksi

## Internal project documents

- `ARIF-Net_Implementation_Report_v2_Research_Realignment.pdf`
- `ARIF-Net_Research_Workflow_TA_International_Journal.pdf`
- `TEMPLATE CAPSTONE TEKNIK INFORMATIKA MUHAMAD NUR ARIF.docx`

## Institutional template rules referenced by this KB

The current Capstone template defines BAB I–V, requires an abstract of 200–300 words, and specifies APA 7 with Mendeley/Zotero for references. It also specifies sections for system description, functional/non-functional requirements, architecture, implementation, and testing/evaluation. [Source: TEMPLATE CAPSTONE TEKNIK INFORMATIKA MUHAMAD NUR ARIF.docx]

---

# 54. Final Instruction to AI Using This Document

Before helping with ARIF-Net, **read this document completely**.

Then remember:

> **The project is a multimodal regression forecasting system for food-price movement. Historical price dynamics are a required part of the model input. Climate/supply, macro/logistics, and news sentiment are external modalities. Price shock is a secondary phenomenon used for shock-aware learning, evaluation, monitoring, and error analysis. ARIF-Net is a research candidate that must be validated with a leakage-safe temporal protocol. The web product exists to operationalize and demonstrate the validated model. Capstone and Tugas Akhir are one continuous research/product pipeline.**

If an instruction, source, old README, or existing code appears to conflict with this principle:

1. classify the conflict,
2. show the evidence,
3. do not silently change the project,
4. propose a decision gate,
5. wait for explicit project-owner decision when the change affects core methodology.

**Never fabricate certainty. Never fabricate results. Never silently redefine the research.**

---

## End of Document

**Document ID:** `ARIF-NET-DOC-001`  
**Version:** `v2.0.0`  
**Status:** `OFFICIAL BASELINE / PHASE 1 SCOPE REVISION`  
**Last Validated:** `2026-10-02`  
**Phase-0 Authority:** `ARIF-Net_Phase_0_Research_Contract_v2.1.0.md` — inti FROZEN 24 September 2026 + Phase 1 Amendment 02 Oktober 2026
