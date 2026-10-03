# ARIF-Net — Phase 0 Research Contract v2.1.0
## Research Contract / Research Charter — FINAL CONSOLIDATED BASELINE

**Proyek:** ARIF-Net — Agricultural Risk and Inflation Forecasting Network  
**Tema:** Multimodal Food Price Forecasting and Intelligence  
**Produk:** ARIF Food Intelligence  
**Status:** **FROZEN CORE (v2.0.0) + PHASE 1 AMENDMENT (v2.1.0)**  
**Tanggal Freeze:** 24 September 2026  
**Tanggal Amendment:** 02 Oktober 2026  
**Pasangan dokumen:** `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v2.0.0.md`  
**Basis utama:** `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v1.0.0(1).md`, `Literatur Review Refrensi Jurnal ARIF-Net.md`, 10 PDF paper utama, bibliografi tambahan 17 paper, serta validasi sumber eksternal.


## 0A. Aturan Konsolidasi v2.0.0

Dokumen v2.0.0 merupakan konsolidasi final dari `v1.0.0`, `v1.1.0`, dan `v1.2.0_ID_FROZEN`.

Urutan otoritas isi:
```text
v1.0.0 → v1.1.0 → v1.2.0 → v2.0.0
        perubahan terbaru selalu mengungguli keputusan sebelumnya
```

Aturan konsolidasi:

1. Informasi yang sama atau bertentangan menggunakan versi terbaru yang tersedia.
2. Informasi unik dari versi lama dipertahankan sebagai bukti/evidence historis apabila belum terwakili di versi terbaru.
3. Arsip versi lama bersifat **non-operatif**; keputusan aktif hanya berasal dari kontrak canonical v2.0.0.
4. Materi novelty yang belum terbukti tetap diberi status kandidat/hypothesis, bukan fakta.
5. Phase 0 tetap diperlakukan sebagai kontrak metodologis; Phase 1–3 bertugas menjalankan dan membuktikan kontrak tersebut.
---

## 0B. Phase 1 Amendment v2.1.0

Amendment ini **tidak membuka ulang** inti metodologis yang dibekukan pada v2.0.0: goal, primary task, target `r(t,h)`, horizon grid, explicit price backbone, protokol anti-leakage, shock protocol (DG-15), status candidate fusion (DG-13/14), dan DG-18 tetap berlaku. Yang diamandemen adalah **implementasi data**: sumber harga, target market, taxonomy komoditas (§3), wilayah pemasok (§4), sumber dan kontrak iklim (§5), serta penegasan metrik (§11). Teks asli bagian yang diamandemen diarsipkan di **Appendix D**.

Urutan otoritas: `v2.0.0 (core) → v2.1.0 (amendment)`. Jika bertentangan pada bagian yang diamandemen, v2.1.0 berlaku.

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

---

## 0. Status Freeze

Phase 0 dinyatakan **beku secara metodologis** dan siap dilanjutkan ke Phase 1.

Freeze ini berarti:

- arah masalah dan tujuan penelitian sudah ditetapkan;
- primary task tetap regression forecasting;
- target penelitian sudah ditetapkan sebagai **relative price movement / percentage change**;
- nominal/direct price diposisikan sebagai **hasil rekonstruksi/output produk**;
- penelitian menggunakan **multi-horizon forecasting** dengan batas maksimum 365 hari;
- tiga komoditas prioritas Capstone/TA adalah **cabai, bawang merah, dan beras**;
- Jakarta menjadi **forecast target market**;
- faktor eksternal ditautkan ke wilayah pemasok/sentra produksi yang relevan;
- seluruh external modalities tetap masuk scope penelitian;
- explicit historical-price representation ditetapkan sebagai backbone;
- experimental protocol dan leakage policy telah ditentukan;
- shock definition tidak lagi bergantung pada satu threshold 3% universal;
- research gap dan novelty claim dibatasi agar tidak melampaui evidence literature terbaru;
- indexing jurnal sudah ditentukan status verifikasinya;
- Phase 1 menjadi tahap **eksekusi data, audit temporal, dan implementasi**, bukan membuka ulang arah fundamental penelitian.

Freeze dapat dibuka kembali hanya melalui decision gate baru dengan bukti yang jelas.

---

# 1. Research Contract Final

## 1.1 Masalah Penelitian

Harga pangan bersifat dinamis dan dapat dipengaruhi oleh historical price dynamics, kondisi iklim, supply, informasi berita, kondisi makro, dan tekanan logistik. Literatur yang diperiksa menunjukkan bahwa masing-masing sumber informasi tersebut sudah digunakan dalam penelitian forecasting, tetapi pendekatan, frekuensi, domain, dan cara fusion berbeda-beda.

Masalah penelitian ARIF-Net bukan lagi sekadar mencari model yang lebih kompleks, tetapi menguji apakah **representasi historical price yang eksplisit**, ketika digabungkan dengan external signals dari climate/supply, news/sentiment, macro/logistics, dan calendar melalui forecasting multi-horizon, memberikan informasi prediktif tambahan yang terukur.

## 1.2 Goal Utama — LOCKED

> Mengembangkan dan mengevaluasi kerangka **regression forecasting multimodal** untuk memprediksi pergerakan harga komoditas pangan pada berbagai horizon waktu dengan historical price dynamics sebagai backbone dan informasi eksternal sebagai sumber informasi tambahan.

## 1.3 Primary Task — LOCKED

**Supervised regression forecasting.**

Price shock hanya merupakan fenomena sekunder untuk:

- evaluasi subset ekstrem;
- shock-aware objective apabila terbukti diperlukan;
- error analysis;
- monitoring/early-warning layer.

---

# 2. Target Variable dan Forecast Horizon

## 2.1 Target Final — DECIDED

Target internal model:

\[
r_{t,h}=\frac{P_{t+h}-P_t}{P_t}
\]

Dengan:

- `P_t` = harga aktual pada forecast origin;
- `P_{t+h}` = harga pada horizon `h`;
- `r_{t,h}` = relative price movement / percentage change.

Nominal price direkonstruksi dari:

\[
\hat P_{t+h}=P_t(1+\hat r_{t,h})
\]

Dengan demikian **satu target modeling** dapat melayani dua kebutuhan:

1. analisis ilmiah terhadap price movement;
2. penyajian direct price pada aplikasi.

Tidak perlu membuat dua model independen untuk direct price dan percentage change kecuali hasil eksperimen Phase 1–3 menunjukkan kebutuhan metodologis yang nyata.

## 2.2 Horizon Final — DECIDED

Maksimum forecasting horizon: **365 hari**.

Horizon grid standar:

| Horizon | Interpretasi |
|---:|---|
| `1` hari | sangat jangka pendek |
| `3` hari | short-term |
| `7` hari | short-term mingguan |
| `14` hari | short-term/biweekly |
| `30` hari | monthly |
| `90` hari | seasonal/intermediate |
| `180` hari | medium-term |
| `365` hari | long horizon / stress/generalization horizon |

### Aturan penting horizon

Forecast tidak boleh diwujudkan sebagai satu angka monoton dari `t` sampai `t+365`.

Model harus menghasilkan **trajectory** atau vector multi-horizon sehingga:

```text
h=1   → r1
h=3   → r3
h=7   → r7
...
h=365 → r365
```

Grafik aplikasi akan menampilkan pergerakan prediksi sebagai kurva yang dapat naik/turun sesuai output model.

### Information availability rule

Untuk forecast origin `t`, model hanya boleh menerima informasi yang **sudah tersedia pada waktu `t`**.

Karena itu, nilai aktual external variables pada `t+1 ... t+365` **tidak boleh digunakan sebagai input observasi masa depan**.

Implikasinya:

- historical lags dan rolling context boleh digunakan;
- calendar deterministik masa depan boleh digunakan bila memang diketahui sebelum forecast;
- future realized weather/climate tidak boleh digunakan langsung;
- future realized news tidak boleh digunakan;
- future realized BBM tidak boleh digunakan;
- future realized supply/logistics tidak boleh digunakan;
- apabila future exogenous forecast kelak ingin dimasukkan, diperlukan skenario/forecast exogenous terpisah dan itu menjadi extension tersendiri.

---

# 3. Scope Komoditas dan Lokasi

## 3.1 Prioritas Capstone → TA — AMENDED v2.1.0

| Prioritas | Komoditas (taxonomy PIHPS) | `comcat_id` | Market target |
|---|---|---|---|
| 1 | **Cabai Merah Keriting** | `com_14` | Pasar Kramatjati (PIHPS level-3, eceran), DKI Jakarta |
| 2 | **Bawang Merah Ukuran Sedang** | `com_11` | Pasar Kramatjati (PIHPS level-3, eceran), DKI Jakarta |
| 3 | **Beras Kualitas Medium I** | `com_3` | Pasar Kramatjati (PIHPS level-3, eceran), DKI Jakarta |

Sumber: P1-DG-01 s.d. P1-DG-05. Satuan Rp/kg. PIKJ dan PIBC tidak lagi menjadi target market; PIBC tetap menjadi konteks pasokan beras dan sumber pelengkap (P1-DG-06). Bawang putih dikeluarkan (P1-DG-13). Komoditas PIHPS lain yang telah dikoleksi = extended scope TA.

### Catatan taxonomy

Taxonomy kini terkunci pada nama komoditas PIHPS di atas. Definisi resmi grade "Medium I" dan pemetaan ke kategori beras PIBC wajib dicatat di `DATA_DICTIONARY.md` sebelum PIBC digunakan sebagai pengisi. Teks asli §3.1 diarsipkan di Appendix D.

## 3.2 Future Generalization — LOCKED DIRECTION

ARIF-Net dirancang agar framework dapat diperluas ke komoditas lain pada penelitian lanjutan. Namun generalisasi ke seluruh komoditas **bukan evidence Capstone** sampai benar-benar diuji.

---

# 4. Feasibility Wilayah Pemasok

## 4.1 Prinsip pemetaan

Jakarta merupakan **forecast market**, sedangkan climate/supply/logistics harus merepresentasikan wilayah yang relevan terhadap pasokan komoditas menuju Jakarta.

Wilayah berikut diperlakukan sebagai **candidate supplier/production regions**, bukan sebagai market-share aktual kecuali data distribusi harian membuktikannya.

## 4.2 Cabai Merah Keriting

### Prioritas wilayah

1. **Cianjur, Jawa Barat**
2. **Bandung/Bandung Barat, Jawa Barat**
3. **Sumedang, Jawa Barat**
4. **Magelang, Jawa Tengah**
5. **Garut, Jawa Barat** sebagai tambahan bila data mendukung

Dokumen pemerintah menunjukkan aliran cabai dari Cianjur, Bandung, Sumedang dan Magelang menuju PIKJ pada berbagai periode, sementara Bandung Barat/Lembang juga dilaporkan memasok PIKJ secara rutin. Bapanas juga mencatat distribusi cabai ke PIKJ dari pusat produksi Jawa Barat, Jawa Tengah dan Sulawesi Selatan pada periode tertentu.

**Enrekang** dapat menjadi wilayah tambahan apabila target diperluas dari cabai merah keriting ke **cabai rawit**, karena bukti distribusi Enrekang → PIKJ lebih eksplisit pada komoditas rawit. Jangan mencampurkannya ke target CMK tanpa validasi taxonomy.

## 4.3 Bawang Merah

### Prioritas wilayah

1. **Brebes, Jawa Tengah**
2. **Cirebon, Jawa Barat**
3. **Nganjuk, Jawa Timur**
4. **Garut/Bandung, Jawa Barat** bila coverage tersedia
5. **Probolinggo/Bima** sebagai wilayah tambahan

Brebes memiliki evidence distribusi langsung ke PIKJ dalam volume besar, sementara Bapanas/Kementan juga mencatat Brebes, Nganjuk, Cirebon, Garut dan beberapa sentra lain sebagai lokasi penting produksi/pasokan bawang.

## 4.4 Beras

### Prioritas wilayah

1. **Karawang, Jawa Barat**
2. **Subang, Jawa Barat**
3. **Indramayu, Jawa Barat**
4. **Cirebon, Jawa Barat**
5. **Demak, Jawa Tengah**
6. **Cilacap, Jawa Tengah**
7. **Sragen/Sukoharjo** sebagai tambahan

Bukti pemerintah menunjukkan PIBC menerima beras dari Karawang, Subang, Indramayu, Cirebon, Demak dan sentra Jawa lainnya. Program ketahanan pasokan Food Station DKI juga mencakup beberapa wilayah tersebut.

## 4.5 Aturan data supplier

Jangan mengubah daftar wilayah di atas menjadi bobot kontribusi tanpa evidence.

Jika tersedia data distribusi harian:

\[
Climate_t = \sum_i w_{i,t}\,Climate_{i,t}
\]

\[
Distance_t = \sum_i w_{i,t}\,Distance_i
\]

Jika bobot `w_{i,t}` tidak tersedia, gunakan:

- multi-origin features per wilayah; atau
- bobot statis yang diperlakukan sebagai experimental assumption dan diuji sensitivity.


## 4.6 Phase 1 Amendment — Wilayah pemasok final

**Wilayah pemasok (P1-DG-11) — status `CANDIDATE`, bukan bobot market share**

| Komoditas | Tier 1 (dimodelkan lebih dulu) | Tier 2 (eksperimen pembanding) |
|---|---|---|
| Cabai Merah Keriting | Kab. Garut, Kab. Cianjur, Kab. Bandung Barat, Kab. Bandung, Kab. Sumedang, Kab. Magelang | Kab. Temanggung |
| Bawang Merah Ukuran Sedang | Kab. Brebes, Kab. Cirebon, Kab. Indramayu | Kab. Demak, Kab. Nganjuk, Kab. Bima, Kab. Garut |
| Beras Kualitas Medium I | Kab. Karawang, Kab. Subang, Kab. Indramayu, Kab. Cirebon, Kab. Demak | Kab. Sragen, Kab. Cilacap, Kab. Sukoharjo |

Lokasi unik untuk request iklim: **18** — Garut, Cianjur, Bandung Barat, Bandung, Sumedang, Magelang, Brebes, Cirebon, Indramayu, Karawang, Subang, Demak, Temanggung, Nganjuk, Bima, Sragen, Cilacap, Sukoharjo. Satu lokasi dapat memiliki tier berbeda per komoditas (mis. Garut: Tier 1 untuk CMK, Tier 2 untuk bawang merah); tier dicatat pada pasangan (lokasi, komoditas).

Kriteria tier: **Tier 1** = tercantum di Contract Phase 0 dan/atau muncul berulang pada bukti resmi/berita terbaru sebagai pemasok langsung ke PIKJ/PIBC; **Tier 2** = sentra produksi yang diketahui tetapi buktinya sebagai pemasok Jakarta lebih lemah, lebih lama, atau musiman. Wilayah terkait cabai rawit (Banyuwangi, Wonosobo, Boyolali, Sleman, Blitar, Jember, Enrekang) dan bawang putih (Lombok Timur/Sembalun) dikeluarkan bersama penyempitan scope. Bila data asal pasokan harian PIBC berhasil dikoleksi, bobot `w(i,t)` beras dapat dibangun berbasis evidence (Contract §4.5).

Titik koordinat iklim = centroid poligon batas administrasi kabupaten (P1-DG-12). Aturan §4.5 tetap berlaku.

---

# 5. Data Modality dan Temporal Availability Contract

## 5.1 Master matrix

| Modality | Kandidat sumber | Frequency | Informasi tersedia | Aturan temporal | Status |
|---|---|---|---|---|---|
| **Harga target** | ~~Bapanas Panel Harga / PIKJ / PIBC~~ → **PIHPS BI, Pasar Kramatjati (v2.1.0)**; PIBC/IPJ pelengkap | Harian | Harga, tanggal, market | nilai hari `t` boleh dipakai untuk origin `t` bila sudah tercatat pada cutoff | **FEASIBLE** |
| **Supply** | Bapanas/PIKJ/PIBC, FDP/logistics records bila tersedia | Harian/episodik | volume/pasokan/event | hanya data yang sudah dilaporkan sebelum cutoff | **FEASIBLE, coverage must audit** |
| **Climate** | ~~BMKG/Data Online/PTSP + station data~~ → **Open-Meteo ERA5-Seamless (v2.1.0)** | Harian tersedia sesuai station/access | RR, Tavg, Tn, Tx, RH, sunshine, wind, dll. | gunakan observed past; aggregate per supplier region | **FEASIBLE, access/data retrieval Phase 1** |
| **News** | GDELT / sumber berita yang relevan | Near-real-time | article time, source, text, tone/metadata | hanya publikasi `≤ cutoff` | **FEASIBLE** |
| **Sentiment** | IndoBERT/Indonesian sentiment pipeline | event/day-derived | sentiment, intensity, volume, recency | feature hanya berasal dari artikel yang telah tersedia | **FEASIBLE, validate model provenance** |
| **BBM** | ESDM/Pertamina official records | Event/effective-date; dapat diperluas menjadi daily step function | price effective date | gunakan harga efektif pada tanggal `t`; jangan melihat perubahan di masa depan | **FEASIBLE** |
| **Distance** | Road-network routing/static road distance | Static/event-independent | km, baseline travel cost | gunakan sebagai static origin feature; jangan perlakukan sebagai historical traffic | **FEASIBLE** |
| **Calendar** | Calendar resmi | Deterministic | day/week/month/holiday | future-known calendar boleh digunakan | **FEASIBLE** |

## 5.2 Climate

BMKG menyediakan data meteorologi harian, tetapi ketersediaan < monthly pada portal tertentu dapat bergantung pada akses PTSP/station. Karena itu Phase 1 wajib membuat **station/regional coverage matrix** sebelum modelling.

Minimum climate variables:

- curah hujan;
- suhu minimum;
- suhu maksimum;
- suhu rata-rata;
- kelembapan;
- sunshine duration bila tersedia;
- wind variables bila relevan.

Feature engineering yang diperbolehkan:

- lag;
- rolling mean;
- anomaly;
- cumulative rainfall;
- extreme-weather indicators.

Semua anomaly/statistics harus dihitung menggunakan data yang tersedia untuk periode training/forecasting dan tidak boleh memakai informasi test masa depan untuk parameter fitting.

## 5.3 News

GDELT merupakan kandidat kuat untuk news acquisition karena bersifat open, global, multibahasa, historis, dan diperbarui secara near-real-time.

Untuk ARIF-Net, news feature minimum jangan hanya:

```text
sentiment_mean
```

tetapi pertimbangkan:

- article volume;
- positive/negative sentiment balance;
- intensity;
- persistence;
- recency;
- topic relevance;
- source count;
- event burst.

Evidence literatur menunjukkan article volume/intensity/persistence dapat membawa informasi prediktif selain polarity murni.

## 5.4 BBM

Harga BBM adalah fitur **event/effective-date based**, bukan sensor harian independen.

Contoh transformasi valid:

```text
Harga BBM efektif sejak 1 Mei
→ diterapkan ke seluruh tanggal berikutnya sampai ada perubahan resmi
```

Jangan mengisi backward ke tanggal sebelum effective date.

## 5.5 Jarak tempuh

Jarak jalan merupakan fitur struktural antar wilayah dan Jakarta.

Untuk penelitian awal, gunakan:

```text
distance_km(origin, Jakarta)
```

sebagai static feature.

Travel time historis tidak boleh dibuat seolah-olah tersedia bila sumber hanya mampu memberikan routing saat ini. Jika digunakan:

```text
logistics_cost_proxy_t
= distance_km × fuel_price_t
```

boleh diuji sebagai proxy sederhana, tetapi harus dilabeli sebagai **proxy**, bukan biaya logistik aktual.


## 5.6 Phase 1 Amendment — Kontrak harga & iklim

**Harga.** Sumber utama PIHPS Bank Indonesia (survei pasar tradisional, harga eceran; pelaporan hari kerja). Harga hari `t` boleh dipakai untuk origin `t`. Pengisian null mengikuti P1-DG-06; nilai berulang adalah observasi valid.

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

§5.2 (BMKG) tetap berlaku untuk prinsip feature engineering (lag, rolling, anomaly fit pada training), tetapi tidak lagi untuk sumber data.

---

# 6. Protokol Anti-Leakage dan Temporal Integrity

## 6.1 Split final

```text
TRAIN → VALIDATION → TEST
```

Pembagian harus kronologis.

## 6.2 Model selection

```text
TRAIN
  ↓
training
  ↓
VALIDATION
  ↓
hyperparameter / epoch / checkpoint selection
  ↓
FREEZE
  ↓
TEST
  ↓
FINAL METRICS
```

Test set tidak boleh ikut menentukan:

- epoch terbaik;
- checkpoint;
- hyperparameter;
- feature selection;
- threshold tuning;
- architecture selection.

## 6.3 Sequence boundary

Untuk test forecast origin, context historical sebelum boundary boleh digunakan apabila memang secara operasional tersedia pada waktu forecast.

Target future tetap harus berada di sisi test.

Contoh:

```text
Historical context ───────────────┐
                                  ▼
Train | Validation | Test origin → Test target
```

Bukan:

```text
Test-only context → kehilangan historical information
```

## 6.4 Transformations

Semua berikut harus **fit pada training** atau dilakukan secara split-aware:

- imputation parameter;
- scaling;
- normalization;
- anomaly baseline;
- quantile threshold;
- target transformations;
- feature selection.

---

# 7. Perbaikan Test-Selection Leakage — PHASE 1 IMPLEMENTATION CONTRACT

Current repository telah diaudit dan memiliki masalah: `train_arif_net.py` menggunakan test tensor sebagai `val_loss` untuk memilih checkpoint.

Ini harus diperbaiki.

## 7.1 Perubahan wajib

### Sebelum

```text
train → evaluate test setiap epoch → pilih best checkpoint
```

### Sesudah

```text
train → evaluate validation setiap epoch → pilih best checkpoint
→ freeze → evaluate test satu kali / controlled final run
```

## 7.2 Struktur loader

Harus ada tiga logical datasets:

```text
train_dataset
val_dataset
test_dataset
```

Namun `test_dataset` tidak boleh terlihat selama model training/selection.

## 7.3 Acceptance test

Sebuah run dinyatakan valid jika log tidak menunjukkan penggunaan test metrics untuk:

- early stopping;
- checkpoint selection;
- hyperparameter tuning;
- threshold optimization.

---

# 8. Shock Definition Final

## 8.1 Primary principle

Shock merupakan **secondary phenomenon**, bukan target classification utama.

## 8.2 Threshold recommendation

Fixed 3% tidak lagi dipakai sebagai satu-satunya threshold seluruh horizon.

Gunakan threshold berbasis distribusi historical relative movement untuk setiap horizon:

\[
Shock_{t,h}=|r_{t,h}|\ge Q_{\alpha}(|r_h|)
\]

dengan `Qα` dihitung **hanya dari training set**.

Primary threshold:

```text
α = 0.95
```

Sensitivity:

```text
Q90
Q95
Q97.5
Q99
```

## 8.3 Legacy operational threshold

`|ΔP| > 3%` tetap disimpan sebagai:

- legacy repository threshold;
- comparison/operational rule;
- sensitivity reference jika relevan.

Ia tidak boleh dipresentasikan sebagai threshold ilmiah universal untuk seluruh horizon.

## 8.4 Evaluasi shock

Untuk setiap horizon:

- overall MAE/RMSE;
- shock MAE/RMSE;
- error distribution;
- optional secondary shock detection metrics jika classifier tambahan benar-benar diimplementasikan.


## 8.5 Known issue — Q95 pada seri lengket (P1-DG-08)

Pada seri eceran yang jarang berubah (terutama beras, horizon pendek), Q95 dari `|r_h|` dapat bernilai 0. DG-15 tidak diubah; alternatif diuji sebagai sensitivity di Phase 2 memakai data training saja. Status: `DEFERRED / KNOWN ISSUE`.

---

# 9. Architecture Experiment Protocol

## 9.1 Architectural principle

**Explicit Historical Price Backbone** ditetapkan sebagai representasi utama harga.

Alasan:

- historical price merupakan informasi inti;
- external modalities bersifat tambahan;
- memudahkan modality ablation;
- mencegah external modality secara diam-diam menggantikan price signal.

## 9.2 Candidate architecture

Arsitektur kandidat ARIF-Net:

```text
Historical Price
      ↓
Explicit Price Encoder
      ↓
Price Representation

Climate/Supply ──→ Climate Encoder ─┐
News/Sentiment ─→ News Encoder ─────┤
Macro/Logistics ─→ Macro Encoder ───┤
Calendar ───────→ Calendar Encoder ─┘
                                    ↓
                         Reliability-Aware Fusion
                                    ↓
                         Horizon-Conditioning
                                    ↓
                         Multi-Horizon Decoder
                                    ↓
                         Regression Outputs
                         r1, r3, ..., r365
```

## 9.3 Reliability-aware gating

Reliability-aware fusion diposisikan sebagai **candidate contribution**, bukan novelty final.

Reliability signal dapat berasal dari:

- missingness;
- source availability;
- recency;
- coverage;
- data-quality flag.

Model tidak boleh mengklaim “reliability score” sebagai observasi objektif bila sebenarnya merupakan learned gate. Istilah harus dibedakan antara:

```text
observed data quality
vs
learned modality weight
```

## 9.4 Horizon-conditioned fusion

Model dapat menggunakan horizon embedding/conditioning sehingga kontribusi modality dapat berubah menurut `h`.

Hipotesis yang diuji, bukan asumsi final:

```text
h pendek  → recent market/news context mungkin lebih relevan
h menengah → climate/supply/calendar mungkin meningkat
h panjang → seasonal/macro structure mungkin lebih dominan
```

Hasil nyata harus datang dari experiment.

---

# 10. Benchmark dan Ablation Protocol

## 10.1 Baseline suite

Semua model wajib menggunakan:

- target yang sama;
- horizon yang sama;
- temporal split yang sama;
- feature availability policy yang sama;
- test set yang sama;
- evaluation metric yang sama.

### Model suite

```text
Naive / Persistence
Price-only Linear / Tree
ARIMA
Ridge / SVR
Random Forest / XGBoost / LightGBM
BiLSTM
TFT
ARIF-Net candidate
```

## 10.2 Minimum ablation

```text
A0 = Price-only
A1 = Price + Climate/Supply
A2 = Price + News/Sentiment
A3 = Price + Macro/Logistics
A4 = Price + Climate + News
A5 = Price + Climate + Macro
A6 = Price + News + Macro
A7 = Full multimodal
A8 = Full multimodal – Reliability Gate
A9 = Full multimodal – Horizon Conditioning
A10 = Full multimodal – Shock-aware objective
```

Jika arsitektur final tidak memakai salah satu komponen, ablation harus disesuaikan.

## 10.3 Repeated runs

Minimal **5 random seeds** untuk model deep learning apabila resource memungkinkan.

Laporkan:

- mean;
- standard deviation;
- best/worst run bila relevan;
- confidence/paired statistical analysis bila metodologis sesuai.

---

# 11. Metrics

## 11.1 Regression

Primary:

- MAE;
- RMSE.

Secondary:

- sMAPE atau MAPE bila aman terhadap nilai mendekati nol;
- MASE bila diperlukan.

## 11.2 Movement

- Directional Accuracy.

Direction bukan target utama.

## 11.3 Extreme movement

- Shock MAE;
- Shock RMSE;
- error distribution pada shock subset.

## 11.4 Multi-horizon

Semua metric harus dilaporkan menurut horizon:

| Horizon | MAE | RMSE | sMAPE/MASE | Direction |
|---:|---:|---:|---:|---:|
| 1 | ✓ | ✓ | ✓ | ✓ |
| 3 | ✓ | ✓ | ✓ | ✓ |
| 7 | ✓ | ✓ | ✓ | ✓ |
| 14 | ✓ | ✓ | ✓ | ✓ |
| 30 | ✓ | ✓ | ✓ | ✓ |
| 90 | ✓ | ✓ | ✓ | ✓ |
| 180 | ✓ | ✓ | ✓ | ✓ |
| 365 | ✓ | ✓ | ✓ | ✓ |


## 11.5 Phase 1 Amendment — Metrik final

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

Validasi: kronologis; rolling-origin bila diperlukan; random k-fold dilarang (P1-DG-22).

---

# 12. Literature Review dan Systematic Search Validation

## 12.1 Temuan setelah perluasan pencarian

Search tambahan menunjukkan bahwa novelty tidak boleh lagi diklaim sebagai:

- penggunaan Transformer;
- penggunaan sentiment;
- penggunaan weather;
- penggunaan macro;
- multimodal fusion secara umum;
- horizon-conditioned learning secara umum;
- reliability-aware learning secara umum.

Semua konsep tersebut telah muncul di literatur yang lebih baru.

Contoh penting:

1. **Wang, Yu & An (2025)** mengembangkan Two-Stream Reinforcement Ensemble dengan dynamic sentiment index untuk agricultural futures. Ini menunjukkan dynamic news weighting sudah memiliki precedent.
2. **Ghonge & Kulkarni (2026)** menggunakan market, weather, trade, dan supply untuk soybean price forecasting. Ini menunjukkan multi-source agricultural price forecasting sudah berkembang jauh.
3. **Amalia et al. (2026)** menggunakan TFT untuk multi-step forecasting 10 strategic food commodities Indonesia.
4. **Wang et al. (2025)** menggunakan multimodal Transformer untuk text, time series, dan satellite imagery pada supply-chain demand forecasting.
5. **McWilliams et al. (2026)** menunjukkan macroeconomic drivers dapat berubah menurut horizon dan regime.

## 12.2 Gap final yang dapat dipertanggungjawabkan

> **Berdasarkan literature corpus awal dan perluasan pencarian yang telah diperiksa, riset agricultural/food-price forecasting telah bergerak dari price-only menuju external-variable modeling, news/sentiment integration, multi-source agricultural forecasting, dan multimodal architectures. Namun, belum teridentifikasi dalam corpus yang diperiksa suatu kerangka yang secara spesifik menguji daily local-market food-price movement forecasting dengan historical price sebagai explicit backbone, multi-origin climate/supply alignment terhadap market target, news/sentiment dan macro/logistics signals, serta evaluasi kontribusi modality dan fusion menurut horizon dengan aturan temporal availability yang ketat.**

Pernyataan tersebut harus tetap ditulis sebagai **gap pada literature corpus yang direview**, bukan sebagai klaim absolut “penelitian pertama di dunia”.

## 12.3 Candidate novelty

Novelty candidate ARIF-Net:

> **A research framework for horizon-aware multimodal food-price movement forecasting that explicitly preserves local historical price dynamics as the price backbone, aligns external signals to relevant production origins and their temporal availability, and evaluates modality/fusion contribution across multiple forecast horizons and extreme-movement regimes.**

### Boundary

Novelty bukan satu layer.

Novelty bukan satu algoritme.

Novelty tidak boleh dinyatakan terbukti sebelum ablation dan blind test selesai.

---

# 13. Fenomena Penelitian

Fenomena yang diangkat:

```text
Harga pangan Jakarta
        ↑
        │
 ┌──────┼─────────┐
 │      │         │
Supply Climate   News
 │      │         │
 └──────┼─────────┘
        │
   Macro / Logistics
        │
        ↓
Price Movement
        ↓
Extreme Movement / Shock
```

### Interpretasi penelitian

- Climate dapat merepresentasikan tekanan kondisi produksi di wilayah pemasok.
- Supply merepresentasikan kondisi aliran barang ke market target.
- News merepresentasikan informasi publik yang dapat muncul sebelum atau bersama perubahan harga.
- Macro/logistics merepresentasikan tekanan eksternal seperti BBM dan biaya/jarak distribusi.
- Historical price merepresentasikan state/dynamics harga yang sedang berlangsung.

**Tidak satu pun komponen tersebut boleh ditulis sebagai penyebab kausal hanya berdasarkan attribution model.**

---

# 14. Status Indexing Bibliografi

## 14.1 Ringkasan

| No | Jurnal | Scopus | Web of Science | Status akademik |
|---:|---|---|---|---|
| 1 | Results in Engineering | **Ya, terverifikasi** | **Ya, terverifikasi (ESCI)** | Aman untuk bukti indexing internasional |
| 2 | Applied Soft Computing | **Ya, terverifikasi** | **Ya, terverifikasi (SCIE)** | Aman |
| 3 | Earth's Future | **Ya, terverifikasi** | **Ya, terverifikasi (SCIE)** | Aman |
| 4 | Journal of Commodity Markets | **Ya, terverifikasi** | **Ya, terverifikasi (SSCI)** | Aman |
| 5 | MethodsX | **Ya, terverifikasi** | **Ya, terverifikasi (WoS/ESCI evidence)** | Aman |
| 6 | Agriculture | **Ya, terverifikasi** | **Ya, terverifikasi (SCIE)** | Aman |
| 7 | International Journal of Scientific Research in Science and Technology | **Tidak terverifikasi / evidence cenderung tidak** | **Klaim jurnal ada, tetapi belum terverifikasi independen pada Master Journal List** | **Jangan dijadikan bukti utama indexing** |
| 8 | PLOS ONE | **Ya, terverifikasi** | **Ya, terverifikasi** | Aman |
| 9 | Nature Communications | **Ya, terverifikasi** | **Ya, terverifikasi** | Aman |
| 10 | Scientific Reports | **Ya, terverifikasi** | **Ya, terverifikasi** | Aman |
| 11 | Scientific Reports | **Ya, terverifikasi** | **Ya, terverifikasi** | Aman |
| 12 | Journal of Big Data | **Ya, terverifikasi** | **Ya, terverifikasi (SCIE evidence)** | Aman |
| 13 | Scientific Reports | **Ya, terverifikasi** | **Ya, terverifikasi** | Aman |
| 14 | IEEE Access | **Ya, terverifikasi** | **Ya, terverifikasi** | Aman |
| 15 | Applied Sciences | **Ya, terverifikasi** | **Ya, terverifikasi (SCIE)** | Aman |
| 16 | IEEE Access | **Ya, terverifikasi** | **Ya, terverifikasi** | Aman |
| 17 | PLOS ONE | **Ya, terverifikasi** | **Ya, terverifikasi** | Aman |

### Catatan

“Ya” pada tabel menunjukkan status journal-level indexing yang diverifikasi melalui sumber indeks/jurnal yang tersedia. Status kuartil (Q1/Q2/Q3/Q4) tidak dijadikan bagian kontrak karena dapat berubah menurut tahun, kategori, SJR/JCR, dan database.

Untuk persyaratan kampus yang secara eksplisit meminta **Sinta 1–3**, status Sinta harus diverifikasi terpisah pada portal Sinta untuk jurnal yang relevan; jangan menganggap Scopus/WoS otomatis setara dengan Sinta.

### Catatan Ewald & Li

PDF yang diunggah sebelumnya menandai versi yang tersedia sebagai preprint dan belum peer-reviewed. DOI bibliografi menyatakan artikel Journal of Commodity Markets. Untuk penulisan akademik final, gunakan metadata artikel jurnal final melalui DOI, bukan hanya metadata preprint.

---

# 15. Decision Gates — FROZEN

| Gate | Keputusan | Status freeze |
|---|---|---|
| DG-01 | Primary task = regression forecasting | **LOCKED** |
| DG-02 | Historical price sebagai explicit input | **LOCKED** |
| DG-03 | Target internal = percentage/relative change | **DECIDED** |
| DG-04 | Direct price = reconstructed output | **DECIDED** |
| DG-05 | Horizon maksimum = 365 hari | **DECIDED** |
| DG-06 | Horizon grid = 1/3/7/14/30/90/180/365 | **DECIDED** |
| DG-07 | Forecast output berupa trajectory/multi-horizon, tidak dipaksa monoton | **DECIDED** |
| DG-08 | Commodity priority = CMK, bawang merah, beras | **DECIDED** |
| DG-09 | Jakarta sebagai target market | **DECIDED** |
| DG-10 | External modalities retained | **DECIDED** |
| DG-11 | Supplier-region mapping digunakan untuk external context | **DECIDED** |
| DG-12 | Explicit price backbone | **DECIDED** |
| DG-13 | Reliability-aware fusion | **PROPOSED CANDIDATE** |
| DG-14 | Horizon-conditioned fusion | **PROPOSED CANDIDATE** |
| DG-15 | Shock threshold horizon-scaled Q95 primary + sensitivity | **DECIDED PROTOCOL** |
| DG-16 | Legacy 3% retained only as comparison/reference | **DECIDED** |
| DG-17 | Test set completely blind during selection | **LOCKED** |
| DG-18 | Architecture selected through controlled experiment | **LOCKED PROTOCOL** |
| DG-19 | Novelty claim limited to validated literature gap | **LOCKED** |
| DG-20 | Capstone → TA as one pipeline | **LOCKED** |


**Catatan v2.1.0:** DG-08 (komoditas) dan DG-09 (target market) diimplementasikan melalui P1-DG-02/04/05; DG-10/11 melalui P1-DG-09 s.d. P1-DG-17. Status DG lain tidak berubah. Register lengkap ada di §0B.

---

# 16. Phase 0 Exit Criteria

Semua berikut dinyatakan **READY/FROZEN**:

- [x] Problem statement disepakati
- [x] Research goal dikunci
- [x] Regression sebagai primary task dikunci
- [x] Target final ditentukan
- [x] Direct price reconstruction ditentukan
- [x] Horizon grid ditentukan
- [x] Batas maksimum 365 hari ditentukan
- [x] Forecast trajectory ditentukan
- [x] Tiga komoditas prioritas ditentukan
- [x] Jakarta sebagai target market ditentukan
- [x] Supplier-region framework ditentukan
- [x] External modalities masuk scope final
- [x] Temporal availability contract ditentukan
- [x] Leakage protocol ditentukan
- [x] Test-selection leakage ditemukan dan kontrak perbaikannya ditetapkan
- [x] Shock threshold protocol ditentukan
- [x] Architecture experiment protocol ditentukan
- [x] Benchmark + ablation protocol ditentukan
- [x] Literature corpus diperluas dan gap dipersempit
- [x] Novelty boundary ditentukan
- [x] Indexing status utama diverifikasi
- [x] Research Contract dibekukan

---

# 17. Phase 1 Handoff

Phase 1 dimulai dari **Data / Temporal Audit**, sesuai urutan pipeline resmi.

Urutan kerja:

```text
P1. Data / Temporal Audit
      ↓
P2. Supplier-region mapping + source provenance
      ↓
P3. Temporal alignment
      ↓
P4. Leakage audit
      ↓
P5. Target + multi-horizon dataset construction
      ↓
P6. Baseline-ready dataset
      ↓
P7. Train/validation/test repair
      ↓
P8. Reproducibility contract
```

### Deliverables Phase 1

1. `DATA_DICTIONARY.md`
2. `DATA_PROVENANCE.md`
3. `TEMPORAL_AVAILABILITY_MATRIX.md`
4. `SUPPLIER_REGION_MAPPING.md`
5. `TARGET_HORIZON_SPEC.md`
6. `LEAKAGE_AUDIT_REPORT.md`
7. `DATASET_VERSION_MANIFEST.md`
8. `EXPERIMENT_CONFIG_SCHEMA.md`

---

# 18. Aturan Akademik Akhir

ARIF-Net harus selalu membedakan:

```text
FACT / OBSERVED
PROPOSED
HYPOTHESIS
INFERENCE
EXTERNAL RESEARCH
FINAL EXPERIMENTAL RESULT
```

Jangan menggunakan bahasa:

> “Climate menyebabkan harga naik.”

Gunakan:

> “Climate-related features menunjukkan kontribusi prediktif terhadap output model pada horizon/evaluasi tersebut.”

Jangan menggunakan:

> “ARIF-Net terbukti terbaik.”

Gunakan:

> “ARIF-Net memperoleh performa X pada protocol Y dan dibandingkan dengan baseline Z pada test period tertentu.”

---

# 19. Kontrak Novelty Final

Novelty ARIF-Net **belum dianggap terbukti pada Phase 0**.

Phase 0 hanya membekukan **candidate novelty**:

> explicit local price backbone + multi-origin external alignment + multi-horizon regression + temporal availability control + modality/fusion ablation.

Novelty baru dapat dipromosikan menjadi **validated contribution** setelah Phase 2–3 menghasilkan:

1. benchmark yang leakage-free;
2. full-model improvement;
3. ablation evidence;
4. horizon-specific evidence;
5. shock-regime evidence;
6. reproducible results;
7. literature gap tetap valid setelah final search.

---

# 20. Final Declaration

**Phase 0 — Research Contract ARIF-Net v1.2.0 dinyatakan FROZEN dan READY FOR PHASE 1.**

Mulai Phase 1, tujuan utama bukan lagi mengubah arah penelitian, melainkan membuktikan bahwa rancangan ini dapat diwujudkan dengan data aktual, temporal availability yang benar, dan experimental protocol yang bebas leakage.

Setiap perubahan terhadap target, horizon, commodity scope, modality, architecture core, objective, shock definition, RQ, atau novelty harus dibuat sebagai **Decision Gate baru** dan tidak boleh dilakukan diam-diam.

---

## Referensi sumber eksternal utama yang digunakan untuk validasi Phase 0

### Supplier / market context

- Bapanas — Panel/PIKJ distribution and food distribution records.
- Kementerian Pertanian — distribution and production-center reports for cabai, bawang merah, and rice.
- Food Station Tjipinang Jaya — Jakarta rice supply context / PIBC.

### Climate

- BMKG — Data Online / climate observation infrastructure.

### News

- GDELT Project — global news archive and near-real-time monitoring.

### Fuel / logistics

- Kementerian ESDM / Pertamina — fuel pricing and effective-date records.

### Literature / novelty expansion

- Wang, L., Yu, L., & An, W. (2025). Two-Stream Reinforcement Ensemble Framework for Agricultural Commodity Prices Forecasting Using Textual Data. *Journal of Forecasting*. DOI: 10.1002/for.70015.
- McWilliams, W., Stewart, S. L., & Massa, O. I. (2026). Food price inflation forecasting: Insights from a Macroeconomic Auto-Regressive Random Forest approach. *Food Policy, 142*, 103115. DOI: 10.1016/j.foodpol.2026.103115.
- Amalia, S., Dhini, A., Zulkarnain, Za’in, C., & Surjandari, I. (2026). A temporal fusion transformer for multi-step forecasting of Indonesia’s strategic food commodity prices. *Results in Engineering, 30*, 110131. DOI: 10.1016/j.rineng.2026.110131.
- Wang, Y., Ding, G.-Y., Zeng, Z.-Y., & Yang, S.-Y. (2025). Causal-Aware Multimodal Transformer for Supply Chain Demand Forecasting: Integrating Text, Time Series, and Satellite Imagery. *IEEE Access, 13*, 176813–176829. DOI: 10.1109/access.2025.3619552.

---

**END OF FROZEN PHASE 0 — PROCEED TO PHASE 1**

---

# APPENDIX A — DETAIL EVIDENCE TERKONSOLIDASI DARI v1.1.0

Bagian berikut mempertahankan detail penelitian yang terdapat pada v1.1.0 dan tidak seluruhnya direproduksi sebagai tabel penuh pada v1.2.0. Bagian ini tetap menjadi supporting evidence untuk canonical contract v2.0.0. Jika terdapat konflik dengan canonical contract, **canonical v2.0.0 yang berlaku**.

# 16. Research Matrix — 17 Paper Inti

| No. | Studi | Data/Konteks | Target/Horizon | Modality | Metode | Temuan utama | Celah terhadap ARIF-Net |
|---|---|---|---|---|---|---|---|
| 1 | Amalia et al. (2026) | 10 komoditas pangan strategis Indonesia, harian | Multi-step 30 hari | Price | TFT | TFT kuat terutama pada komoditas sangat variatif. | Price-centric; external signals dan systematic modality ablation belum menjadi fokus utama. |
| 2 | Avinash et al. (2024) | Harga komoditas pertanian, fokus volatilitas | 1, 4, 8, 12 minggu | Price + technical | HMM-guided DL | Hidden states + technical indicators membantu forecasting. | Tidak full multimodal; belum reliability-aware. |
| 3 | Busker et al. (2024) | Krisis ketahanan pangan Horn of Africa | Sampai 12 bulan | Climate/hazard + socioeconomics | XGBoost early warning | Menunjukkan potensi multimodal long-lead warning. | Target bukan harga; relevansi terutama untuk konsep early warning dan horizon panjang. |
| 4 | Ewald & Li (2024) | Salmon spot price + headline news | Weekly | Price + sentiment | CNN-LSTM/DL + FinBERT/TextBlob | Sentiment dapat menurunkan error. | Satu external modality; uploaded copy menyatakan preprint/not peer reviewed. |
| 5 | Ghonge & Kulkarni (2026) | Soybean India: market, weather, trade, supply | Multi-source forecasting | Price + weather + trade + supply | Wide-and-Deep | Integrasi multi-source membantu prediksi soybean. | Belum news/sentiment; belum reliability-aware/horizon-conditioned fusion. |
| 6 | Gu et al. (2022) | Cabbage/radish Korea + weather + trading volume | Monthly | Price + climate + trading | DIA-LSTM | Dynamic production-area weather dan attention meningkatkan MAPE. | Tidak news/macro/logistics; konteks bulanan. |
| 7 | Gupta et al. (2024) | 14 komoditas + economic indicators + historical/technical features | Price-change forecasting | Price + economic/technical | Beragam ML/DL | Mendukung penggunaan percentage change dan perbandingan banyak model. | Tidak menawarkan fusion multimodal khusus. |
| 8 | Han et al. (2023) | Global food prices + macro/oil/production/uncertainty | Monthly | Price + macro/global factors | ML + SHAP | Macro/global factors menunjukkan predictive importance. | Global bulanan; bukan daily local regression multimodal. |
| 9 | MacLachlan et al. (2025) | US food prices + macro/logistics | Monthly | Price + macro/logistics | Adaptive statistical learning | External macro/logistics membantu precision dan explanatory power. | Domain/frequency berbeda; bukan multimodal neural fusion. |
| 10 | Manogna et al. (2025) | 23 komoditas, 165 pasar India | Daily | Price | ARIMA, ML, DL | LSTM/GRU kuat menangkap nonlinear temporal behavior. | External context tidak digunakan. |
| 11 | Min et al. (2025) | 4 komoditas Korea + 6 weather variables | Short-term, termasuk 14 hari | Price + climate | LSTM, StemGNN, T-GCN | Multivariate/GNN dan smoothing membantu pada setting tertentu. | Belum news/macro/logistics. |
| 12 | Nayak et al. (2025) | Potato Northern India | Weekly | Price | Transformer + PSO/GWO/WOA | Metaheuristic tuning meningkatkan Transformer pada setting tertentu. | Price-only; optimization bukan novelty multimodal. |
| 13 | Nayak et al. (2024) | TOP crops India + weather | Crop-price forecasting | Price + climate | NBEATSX/TransformerX | Exogenous weather meningkatkan forecasting. | External modality terbatas. |
| 14 | Pan (2025) | Multi-source agriculture: Agmarknet/AGRIS/WorldCereal/GAEZ | Risk/early warning | Multisource | Deep learning + knowledge graph | Menggabungkan sumber data terstruktur dan heterogen. | Fokus lebih luas pada risk intelligence; bukan controlled daily price regression. |
| 15 | Theofilou et al. (2026) | Corn futures harian + GDELT news | Next-day | Price + news | LSTM + Ridge residual | Directional accuracy naik; volume/intensity/persistence berita informatif. | Belum full multimodal; sangat relevan untuk desain news branch. |
| 16 | Wang et al. (2025) | Demand + text + satellite imagery | 1–28 hari | Time series + text + image | Causal-Aware Multimodal Transformer | Cross-modal attention + specialized encoders membantu multimodal forecasting. | Domain demand, bukan food price; berguna sebagai precedent arsitektur. |
| 17 | Zhao et al. (2025) | Rice/wheat/corn historical data | Sliding window + dramatic movement | Price | TCN-XGBoost | Hybrid temporal/nonlinear kuat pada dramatic movements. | External modalities tidak terintegrasi. |

---

# 17. Literatur Tambahan untuk Validasi Research Gap

Literatur tambahan yang ditemukan saat menguji bibliografi memperkecil beberapa klaim gap lama.

| Studi tambahan | Dampak terhadap ARIF-Net |
|---|---|
| Yi et al. (2026) | Menunjukkan price + news + macro dan beberapa horizon; mengurangi kekuatan novelty “news + macro + multi-horizon”. |
| Wang, Yu & An (2025) | Menunjukkan dynamic sentiment weighting dan multi-stream agricultural forecasting; mengurangi novelty “dynamic sentiment weighting”. |
| Salsabila & Nooraeni (2025) | Menunjukkan news sentiment untuk food-price forecasting Indonesia; mengurangi novelty “news sentiment + Indonesia”. |
| Ünal et al. (2026) | Menunjukkan climate + macro + explainable time-series modeling; mengurangi novelty “climate + macro + explainability”. |

Konsekuensinya, novelty ARIF-Net **harus berada pada kombinasi desain yang lebih spesifik**, bukan pada satu komponen populer.

---

# 18. Fenomena → Literatur → Gap

## 18.1 Fenomena 1 — Perubahan harga dapat terjadi dua arah

**Fenomena:** harga dapat masuk kondisi rendah maupun tinggi, bukan hanya spike ke atas.  
**Literatur:** Amalia, Manogna, Zhao, Avinash, Min menunjukkan dinamika/volatilitas merupakan bagian penting forecasting.  
**Implikasi:** model perlu belajar relative movement dan extreme movement dua arah.

## 18.2 Fenomena 2 — External conditions berubah terhadap waktu

**Fenomena:** weather, supply, distribution, dan macro conditions tidak statis.  
**Literatur:** Gu, Nayak, Min, MacLachlan, Ghonge menunjukkan external variables dapat membantu.  
**Implikasi:** modality tidak boleh diperlakukan sebagai fitur statis sederhana.

## 18.3 Fenomena 3 — Informasi publik tidak hanya berupa polarity

**Fenomena:** informasi berita memiliki volume, intensity, persistence, recency, dan topic.  
**Literatur:** Ewald & Li mendukung sentiment; Theofilou menunjukkan coverage intensity/persistence dapat lebih informatif daripada tone polarity pada setting tertentu.  
**Implikasi:** news branch harus dibangun lebih kaya daripada satu skor sentiment.

## 18.4 Fenomena 4 — Horizon mengubah masalah forecasting

**Fenomena:** prediksi besok dan prediksi satu tahun bukan masalah yang identik.  
**Literatur:** Amalia, Yi dan studi multi-horizon menunjukkan perbedaan perilaku dan/atau kontribusi driver menurut horizon.  
**Implikasi:** fusion sebaiknya mempertimbangkan horizon.

## 18.5 Fenomena 5 — Ketersediaan data tidak seragam

**Fenomena:** price, news, climate, macro, dan supply memiliki frekuensi serta release time berbeda.  
**Literatur:** studi multimodal menunjukkan perlunya specialized encoders/cross-modal mechanisms, sementara ARIF-Net menambahkan aturan availability sebagai kebutuhan deployment.  
**Implikasi:** reliability-aware fusion menjadi kandidat methodological gap.

---

# 19. Research Gap yang Direvisi

## G1 — Integrasi modality telah maju, sehingga gap bukan lagi sekadar “belum multimodal”

Literatur terbaru telah menunjukkan price + climate, price + news, price + macro, bahkan market + weather + trade + supply dan multimodal transformer pada domain terkait.

**Konsekuensi:** ARIF-Net tidak boleh mengklaim “multimodal” sebagai novelty tunggal.

## G2 — Reliability/availability-aware fusion masih menjadi kandidat gap yang lebih spesifik

Pada kasus nyata, modality memiliki tingkat kelengkapan, freshness, dan waktu ketersediaan berbeda. Dalam corpus agricultural-price yang direview, belum teridentifikasi framework yang secara eksplisit menjadikan **availability/freshness/quality** sebagai bagian dari learned fusion weight untuk daily food-price forecasting.

## G3 — Horizon-conditioned external contribution masih memiliki ruang

Studi terdahulu menunjukkan bahwa driver atau performance dapat berubah menurut horizon, tetapi belum ditemukan pada corpus utama suatu desain yang secara eksplisit menggabungkan:

```text
explicit price backbone
+
multiple heterogeneous modalities
+
horizon-conditioned fusion
+
reliability-aware weighting
```

dalam satu daily food-price regression framework.

## G4 — Extreme movement perlu dinilai relatif terhadap horizon

Threshold fixed 3% tidak mempunyai makna statistik yang identik pada seluruh horizon. Karena itu, evaluasi extreme movement dapat menggunakan threshold yang diturunkan dari distribusi return setiap horizon.

## G5 — Research contribution harus dibuktikan melalui ablation

Model yang lebih besar dan lebih banyak fitur bisa saja menghasilkan improvement karena complexity, bukan karena informasi yang benar-benar berguna. Controlled ablation wajib membedakan:

```text
information gain
vs
fusion gain
vs
architecture gain
vs
shock-objective gain
```

---

# 20. Kandidat Novelty

## 20.1 Kandidat novelty utama

> **Kerangka regression forecasting multimodal yang mempertahankan explicit historical-price backbone dan secara dinamis mengondisikan kontribusi climate/supply, news/sentiment, dan macro/logistics berdasarkan forecast horizon serta reliabilitas/ketersediaan informasi untuk menghasilkan prediksi pergerakan harga pangan harian hingga satu tahun.**

## 20.2 Kontribusi metodologis pendukung

1. **Explicit Price Anchor** — historical price tetap menjadi backbone yang dapat diidentifikasi.
2. **Reliability-Aware Fusion** — bobot modality mempertimbangkan availability/freshness/quality.
3. **Horizon-Conditioned Fusion** — kontribusi modality dapat berubah menurut horizon.
4. **Dense Multi-Horizon Regression Path** — trajectory harian dapat dihasilkan hingga H ≤ 365 tanpa constraint monotonic.
5. **Horizon-Scaled Shock Evaluation** — extreme movement dievaluasi menggunakan threshold data-derived per horizon.
6. **Controlled Modality/Fusion Ablation** — kontribusi informasi dipisahkan dari sekadar bertambahnya kompleksitas.

Semua butir di atas masih **candidate contribution** sampai eksperimen menunjukkan kontribusi yang konsisten.

---

# 21. Batasan Klaim Novelty

Dilarang menulis:

> “ARIF-Net adalah model multimodal food-price forecasting pertama di dunia.”

Wording yang diperbolehkan pada tahap ini:

> “Dalam literatur yang direview untuk penelitian ini, ARIF-Net mengeksplorasi kombinasi yang masih kurang dieksplorasi berupa explicit historical-price backbone, reliability-aware fusion, dan horizon-conditioned multimodal regression pada daily local food-price forecasting.”

Wording tersebut harus diperbarui setelah systematic search yang lebih luas.

---

# 22. Research Questions Final — Versi Phase 0

### RQ1 — Efektivitas Forecasting Multimodal

> **Seberapa efektif model regresi multimodal ARIF-Net dalam memprediksi pergerakan harga pangan harian dibandingkan baseline price-only dan reduced-modality?**

### RQ2 — Nilai Tambah Setiap Modality

> **Sejauh mana climate/supply, news/sentiment, dan macro/logistics memberikan tambahan informasi prediktif terhadap historical price dynamics berdasarkan controlled modality ablation?**

### RQ3 — Reliability dan Horizon pada Fusion

> **Apakah mekanisme reliability-aware dan horizon-conditioned multimodal fusion meningkatkan kualitas forecasting dibandingkan fusion statis atau model yang tidak menggunakan mekanisme tersebut?**

### RQ4 — Ketahanan pada Pergerakan Ekstrem

> **Bagaimana performa ARIF-Net pada extreme price movement di berbagai horizon dibandingkan performa pada kondisi normal dengan menggunakan definisi shock yang diskalakan terhadap horizon?**

### RQ5 — Kontribusi Prediktif Lintas Horizon

> **Bagaimana kontribusi prediktif masing-masing modality berubah menurut forecast horizon tanpa menafsirkannya sebagai hubungan kausal?**

---

# 23. Working Title

## Judul kerja utama

> **ARIF-Net: Horizon-Conditioned Reliability-Aware Multimodal Regression Forecasting of Daily Food Price Movements**

## Judul khusus Capstone

> **ARIF-Net: Horizon-Conditioned Multimodal Regression Forecasting of Daily Red Chili Price Movements Using Climate-Supply, News, and Macro-Logistics Signals**

## Judul fleksibel untuk pengembangan TA/publikasi

> **ARIF-Net: Reliability-Aware Multimodal Forecasting of Food Price Movements Across Multiple Horizons**

Judul final dapat dikunci setelah target implementasi, horizon evaluasi, data scope, dan architecture candidate selesai divalidasi.

---

# 24. Modality Contract

| Modality | Status | Fitur kandidat | Aturan waktu |
|---|---|---|---|
| Historical Price | Wajib | price, return/change, volatility, lag, rolling statistics | Hanya informasi ≤ forecast origin |
| Climate | Final direction | rainfall, temperature, anomaly, drought/wetness | Harus sudah tersedia pada `t` |
| Supply | Final direction | production, arrival, supply proxy | Timestamp dan availability wajib diverifikasi |
| News | Final direction | sentiment, volume, intensity, persistence, topic, recency | Gunakan waktu publikasi/availability |
| Macro | Final direction | inflation/economic/market indicators | Gunakan waktu rilis, bukan kalender naif |
| Logistics | Final direction | fuel, transport/distribution proxy | Frequency dan release timing diaudit |
| Calendar | Pendukung | weekday, month, holiday/event | Nilai yang memang diketahui sebelumnya boleh digunakan |

Modality dapat diturunkan statusnya bila tidak lolos coverage, provenance, temporal availability, atau quality audit.

---

# 25. Rancangan Eksperimen Minimum

```text
M0  Naive / simple statistical baseline
M1  Price-only classical / ML
M2  Price-only deep learning
M3  Price + Climate/Supply
M4  Price + News
M5  Price + Macro/Logistics
M6  Price + Climate/Supply + News
M7  Price + Climate/Supply + Macro/Logistics
M8  Price + News + Macro/Logistics
M9  Full multimodal + fusion statis
M10 Full multimodal + horizon-conditioned fusion
M11 Full multimodal + reliability-aware fusion
M12 Full candidate ARIF-Net + shock-aware objective
```

Tujuannya bukan sekadar memenangkan benchmark, tetapi mengisolasi sumber improvement.

---

# 26. Validation Gates

| Gate | Pertanyaan | Evidence yang dibutuhkan |
|---|---|---|
| DG-01 | Apakah data harga cabai merah keriting/DKI Jakarta feasible? | Coverage, missingness, frequency, provenance |
| DG-02 | Apakah percentage movement layak menjadi target kanonik? | Distribusi, stabilitas, reconstruction, metric compatibility |
| DG-03 | Apakah horizon hingga 365 hari feasible? | Effective sample size, backtest stability, coverage |
| DG-04 | Apakah external data tersedia pada forecast origin? | Release/publication timestamp + cutoff audit |
| DG-05 | Apakah tiap modality memberi nilai tambah? | Controlled ablation |
| DG-06 | Apakah explicit price backbone lebih tepat? | Unified-vs-explicit comparison |
| DG-07 | Apakah horizon-conditioned fusion membantu? | Static-vs-conditioned comparison |
| DG-08 | Apakah reliability-aware gate membantu? | Missing/stale modality tests + ablation |
| DG-09 | Apakah shock-aware objective membantu? | Loss ablation + threshold sensitivity |
| DG-10 | Apakah attribution robust? | SHAP/attention/gate analysis |
| DG-11 | Apakah generalisasi teruji? | Cross-time; cross-location/commodity bila data tersedia |
| DG-12 | Apakah novelty claim dapat dipertahankan? | Systematic literature search + final experimental evidence |

---

# 27. Experimental Validity Contract

Pipeline wajib:

```text
RAW SOURCES
    ↓
CLEANING
    ↓
TEMPORAL ALIGNMENT
    ↓
AVAILABILITY / CUTOFF AUDIT
    ↓
CHRONOLOGICAL TRAIN / VALIDATION / TEST
    ↓
TRAIN-ONLY TRANSFORM FIT
    ↓
MODEL SELECTION — VALIDATION ONLY
    ↓
MODEL FREEZE
    ↓
BLIND TEST
    ↓
ERROR / SHOCK / ATTRIBUTION ANALYSIS
```

Current repository audit telah menemukan historical test-selection leakage. Oleh karena itu, benchmark lama tidak boleh otomatis dijadikan evidence final sebelum protocol diperbaiki dan eksperimen dijalankan ulang.

---

# 28. Validasi Data yang Wajib Dilakukan pada Phase 1

## Price

- apakah daily observation kontinu;
- apakah definisi pasar/agregasi konsisten;
- apakah ada perubahan sumber atau metodologi pencatatan;
- apakah missing period dapat dijelaskan.

## Climate

- apakah stasiun/wilayah mewakili sentra produksi;
- apakah terdapat perubahan coverage;
- apakah agregasi harian valid;
- apakah data sudah tersedia pada saat forecast.

## Supply

- apakah volume supply/arrival tersedia harian atau perlu agregasi;
- apakah waktu publish sama dengan tanggal observasi;
- apakah data benar-benar menggambarkan pressure supply.

## News

- apakah sumber dapat dilacak;
- apakah artikel relevan terhadap commodity/market;
- apakah publication time tersedia;
- apakah sentiment model dan fallback tercatat;
- apakah agregasi harian tidak memasukkan berita masa depan.

## Macro/Logistics

- apakah frequency data cocok;
- apakah release time diketahui;
- apakah carry-forward/forward-fill dilakukan dengan benar;
- apakah indikator benar-benar tersedia ketika forecasting dilakukan.

---

# 29. Kriteria Phase 0 Selesai

### Sudah ditetapkan

- [x] Regression forecasting sebagai primary task.
- [x] Historical price sebagai input wajib.
- [x] External modality tetap menjadi arah scope.
- [x] Multi-horizon dengan batas maksimum 365 hari.
- [x] Direct price dan percentage movement dapat ditampilkan dari satu canonical forecast.
- [x] Explicit price backbone menjadi rekomendasi representasi.
- [x] Reliability-aware + horizon-conditioned fusion menjadi candidate architecture.
- [x] Shock tetap secondary phenomenon.
- [x] Research gap diperketat setelah memeriksa literatur 2025–2026.
- [x] RQ diperbarui.
- [x] Working title diperbarui.

### Wajib divalidasi sebelum freeze Phase 0 final

- [ ] Feasibility data komoditas/lokasi.
- [ ] Implementasi target final.
- [ ] Horizon grid final.
- [ ] Temporal availability tiap modality.
- [ ] Threshold shock final + sensitivity protocol.
- [ ] Perbaikan test-selection leakage.
- [ ] Architecture experiment protocol.
- [ ] Status indexing jurnal jika dibutuhkan untuk persyaratan akademik.
- [ ] Systematic literature search yang lebih luas untuk menguatkan novelty claim.

---

# 30. Snapshot Research Contract

| Elemen | Interpretasi Phase 0 | Status |
|---|---|---|
| Problem | Price-only tidak selalu menangkap external context; faktor eksternal bersifat heterogen dan asynchronous. | READY |
| Goal | Multimodal regression forecasting. | LOCKED |
| Primary task | Regression forecasting. | LOCKED |
| Secondary phenomenon | Extreme/price shock. | LOCKED AS SECONDARY |
| Scope awal | Red chili, DKI Jakarta, daily. | WORKING / FEASIBILITY GATE |
| Core inputs | Historical price + climate/supply + news/sentiment + macro/logistics + calendar. | LOCKED DIRECTION |
| Canonical target | Relative price movement. | RECOMMENDED |
| User output | Percentage movement + reconstructed direct price. | RECOMMENDED |
| Horizon | Variable, H ≤ 365 days. | LOCKED BOUNDARY |
| Price representation | Explicit price backbone. | RECOMMENDED |
| Fusion | Reliability-aware + horizon-conditioned. | CANDIDATE |
| Shock definition | Horizon-scaled empirical threshold. | RECOMMENDED |
| Main gap | Reliability-aware + horizon-conditioned heterogeneous fusion pada daily local food-price regression, within reviewed corpus. | PROPOSED |
| Novelty | Candidate, belum terbukti secara global. | OPEN |
| Final RQ | RQ1–RQ5 revised. | PROPOSED |
| Working title | Horizon-Conditioned Reliability-Aware Multimodal Regression Forecasting... | PROPOSED |
| Evidence protocol | Train → validation → freeze → blind test. | REQUIRED |

---

# 31. Phase 0 Bottom Line

ARIF-Net **tidak lagi diposisikan sekadar sebagai “model deep learning baru untuk prediksi harga pangan”**.

Posisi penelitian yang lebih tepat adalah:

> **Membangun dan menguji secara ketat kerangka regression forecasting multimodal yang mempertahankan historical price sebagai anchor, menggabungkan climate/supply, news/sentiment, dan macro/logistics secara kondisional berdasarkan horizon dan reliabilitas informasi, serta mengevaluasi pergerakan ekstrem menggunakan pendekatan yang sesuai dengan masing-masing horizon.**

Komponen seperti LSTM, Transformer, attention, sentiment, weather, XGBoost, dan multimodal fusion sudah memiliki precedent. Karena itu, keberhasilan novelty ARIF-Net bergantung pada apakah desain fusion dan evidence protocol di atas benar-benar menghasilkan kontribusi yang terukur.

Prinsip utama penelitian:

```text
HISTORICAL PRICE REMAINS CORE
          +
EXTERNAL MODALITIES ARE TESTED, NOT ASSUMED
          +
HORIZON MATTERS
          +
MODALITY RELIABILITY MATTERS
          +
SHOCK IS SECONDARY
          +
TEST SET REMAINS BLIND
```

---

# 32. Referensi Utama

1. Amalia, S., Dhini, A., Zulkarnain, Za’in, C., & Surjandari, I. (2026). *A Temporal Fusion Transformer for Multi-step Forecasting of Indonesia’s Strategic Food Commodity Prices*. Results in Engineering. DOI: 10.1016/j.rineng.2026.110131.
2. Avinash, G., Ramasubramanian, V., Ray, M., Paul, R., Godara, S., Nayak, G. H. H., Kumar, R., Manjunatha, B., Dahiya, S., & Iquebal, M. A. (2024). *Hidden Markov guided Deep Learning models for forecasting highly volatile agricultural commodity prices*. Applied Soft Computing, 158, 111557. DOI: 10.1016/j.asoc.2024.111557.
3. Busker, T., Van Den Hurk, B., De Moel, H., Van Den Homberg, M. V. D., Van Straaten, C., Odongo, R. A., & Aerts, J. C. J. H. (2024). *Predicting Food-Security Crises in the Horn of Africa Using Machine Learning*. Earth’s Future, 12. DOI: 10.1029/2023EF004211.
4. Ewald, C. O., & Li, Y.-Y. (2024). *The role of news sentiment in salmon price prediction using deep learning*. Journal of Commodity Markets. DOI: 10.1016/j.jcomm.2024.100438.
5. Ghonge, V., & Kulkarni, Y. R. (2026). *An advanced wide-and-deep learning framework for soybean price forecasting using market, weather, trade, and supply data*. MethodsX, 17, 104030. DOI: 10.1016/j.mex.2026.104030.
6. Gu, Y., Jin, D., Yin, H.-L., Zheng, R., Piao, X.-H., & Yoo, S.-J. (2022). *Forecasting Agricultural Commodity Prices Using Dual Input Attention LSTM*. Agriculture, 12(2), 256. DOI: 10.3390/agriculture12020256.
7. Gupta, H., Kumari, R., Rajput, S., & Puri, N. (2024). *Forecasting Commodity Prices using Machine Learning*. International Journal of Scientific Research in Science and Technology. DOI: 10.32628/IJSRST52411110.
8. Han, X., Yuan, T., Wang, D., Zhao, Z., & Gong, B. (2023). *How to understand high global food price? Using SHAP to interpret machine learning algorithm*. PLOS ONE, 18. DOI: 10.1371/journal.pone.0290120.
9. MacLachlan, M. J., Adjemian, M. K., Etienne, X. L., Sweitzer, M., Volpe, R. J., & Zeng, W. (2025). *Adaptive food price forecasting improves public information in times of rapid economic change*. Nature Communications. DOI: 10.1038/s41467-025-61660-x.
10. Manogna, R. L., Dharmaji, V., & Sarang, S. (2025). *Enhancing agricultural commodity price forecasting with deep learning*. Scientific Reports, 15. DOI: 10.1038/s41598-025-05103-z.
11. Min, Y., Kim, Y. R., Hyon, Y., Ha, T., Lee, S.-J., Hyun, J., & Lee, M.-R. (2025). *RNN and GNN based prediction of agricultural prices with multivariate time series and its short-term fluctuations smoothing effect*. Scientific Reports, 15. DOI: 10.1038/s41598-025-97724-7.
12. Nayak, G. H. H., Alam, M. W., Naik, B. S., Varshini, B. S., Avinash, G., Kumar, R. R., Ray, M., & Singh, K. N. (2025). *Meta-transformer: leveraging metaheuristic algorithms for agricultural commodity price forecasting*. Journal of Big Data, 12, 138. DOI: 10.1186/s40537-025-01196-5.
13. Nayak, G. H. H., Alam, M. W., Singh, K., Avinash, G., Kumar, R., Ray, M., & Deb, C. K. (2024). *Exogenous variable driven deep learning models for improved price forecasting of TOP crops in India*. Scientific Reports, 14. DOI: 10.1038/s41598-024-68040-3.
14. Pan, D. (2025). *A Price Risk Early Warning Model for Agricultural Products Based on the Integration of Deep Learning and Knowledge Graphs*. IEEE Access, 13, 162623–162638. DOI: 10.1109/ACCESS.2025.3609817.
15. Theofilou, A., Nastis, S., Mattas, K., & Theofilou, K. (2026). *AI-Driven News-Enhanced Machine Learning for Short-Term Corn Futures Price Forecasting*. Applied Sciences, 16, 1337. DOI: 10.3390/app16031337.
16. Wang, Y., Ding, G.-Y., Zeng, Z.-Y., & Yang, S.-Y. (2025). *Causal-Aware Multimodal Transformer for Supply Chain Demand Forecasting: Integrating Text, Time Series, and Satellite Imagery*. IEEE Access, 13, 176813–176829. DOI: 10.1109/ACCESS.2025.3619552.
17. Zhao, T.-W., Chen, G.-Q., Suraphee, S., Phoophiwfa, T., & Busababodhin, P. (2025). *A hybrid TCN-XGBoost model for agricultural product market price forecasting*. PLOS ONE, 20. DOI: 10.1371/journal.pone.0322496.

### Referensi tambahan untuk validasi gap

- Yi et al. (2026). *Unveiling dynamics in agricultural supply chain: A transformer-enhanced framework for commodity price modeling*. International Journal of Production Economics, 294, 109820. DOI: 10.1016/j.ijpe.2025.109820.
- Wang, L., Yu, L., & An, W. (2025). *Two-Stream Reinforcement Ensemble Framework for Agricultural Commodity Prices Forecasting Using Textual Data*. Journal of Forecasting, 44(8), 2386–2404. DOI: 10.1002/for.70015.
- Salsabila, A., & Nooraeni, R. (2025). *Forecasting Shallot Prices in Indonesia Using News-Based Sentiment Indicators*. Jurnal Online Informatika, 10(1), 165–176. DOI: 10.15575/join.v10i1.1422.
- Ünal, E. et al. (2026). *Temperature shocks and food inflation: Multicountry evidence from visual time-series transformers and attention-based feature selection*. Journal of Environmental Management, 413, 130268. DOI: 10.1016/j.jenvman.2026.130268.

---

# 33. Aturan Status untuk Dokumentasi Berikutnya

| Status | Makna |
|---|---|
| `LOCKED` | Keputusan resmi penelitian; tidak boleh diubah diam-diam. |
| `RECOMMENDED` | Rekomendasi teknis yang kuat, tetapi masih dapat diganti oleh peneliti. |
| `PROPOSED` | Kandidat yang harus mendapat pembuktian empiris. |
| `OPEN` | Belum diputuskan atau belum memiliki evidence yang cukup. |
| `VERIFIED` | Telah didukung oleh sumber/data yang diperiksa. |
| `REQUIRED` | Harus diselesaikan sebelum evidence final dapat diterima. |
| `UNVERIFIED` | Belum cukup bukti untuk dipresentasikan sebagai fakta. |

AI/agen tidak boleh mengubah `PROPOSED`, `OPEN`, atau `UNVERIFIED` menjadi `LOCKED` atau `VERIFIED` tanpa evidence atau keputusan peneliti.


---

# APPENDIX B — ARSIP HISTORIS v1.0.0

> Arsip ini disimpan untuk traceability. Isinya adalah salinan dokumen v1.0.0 yang pernah berlaku. **Bukan sumber keputusan aktif** jika berbeda dengan canonical v2.0.0.

```markdown
# ARIF-Net — Phase 0 Research Contract

**Dokumen:** Research Contract / Research Charter
**Versi:** v1.0.0
**Tanggal:** 22 September 2026
**Status:** Working Baseline — menunggu keputusan pada OPEN Decision Gates
**Research Model:** ARIF-Net (Agricultural Risk and Inflation Forecasting Network)
**Tema:** Multimodal Food Price Forecasting and Intelligence

---

## 0. Basis dan Aturan Dokumen

Dokumen ini disusun dengan tiga sumber utama:

1. `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v1.0.0(1).md` sebagai **official baseline / research-engineering knowledge base**.
2. `Literatur Review Refrensi Jurnal ARIF-Net.md` sebagai hasil literature screening/analysis dari Consensus AI.
3. Sepuluh PDF jurnal/paper yang diunggah, yang digunakan sebagai **evidence utama** untuk memeriksa ulang temuan literature review.

**Catatan corpus:** dokumen Consensus mencantumkan beberapa referensi tambahan di luar sepuluh PDF yang diunggah. Referensi tambahan tersebut tidak dihitung sebagai bagian dari matriks 10-paper utama dalam dokumen ini. Klaim terhadap sepuluh studi utama diprioritaskan dari PDF yang tersedia.

Aturan status mengikuti governance ARIF-Net:

| Status | Makna |
|---|---|
| `LOCKED` | Sudah menjadi arah resmi proyek dan tidak boleh diubah diam-diam. |
| `OBSERVED` | Fakta yang ditemukan pada repository/dokumen/data. |
| `PROPOSED` | Usulan metodologi yang didukung literatur tetapi belum dikunci. |
| `OPEN` | Belum diputuskan; harus menjadi decision gate. |
| `REQUIRED` | Harus diselesaikan sebelum evidence final dapat diterima. |
| `VERIFIED` | Didukung langsung oleh sumber yang diperiksa. |
| `UNVERIFIED` | Belum cukup bukti dari sumber yang tersedia. |

---

# 1. Temuan Masalah Penelitian

## 1.1 Masalah domain

Forecasting harga komoditas pangan merupakan masalah yang kompleks karena pergerakan harga bersifat nonlinear, nonstationary, dan volatil serta dipengaruhi oleh lebih dari satu kelompok faktor. Literatur yang diperiksa menunjukkan pengaruh historical price dynamics, cuaca/supply, informasi berita/sentiment, perdagangan, dan faktor makro/logistik pada konteks yang berbeda.

## 1.2 Masalah metodologis yang muncul dari 10 paper

| Temuan | Evidence dari corpus | Konsekuensi untuk ARIF-Net |
|---|---|---|
| Price-only tetap kuat, tetapi tidak cukup menjelaskan seluruh konteks | Manogna et al. menunjukkan performa kuat LSTM/GRU pada 23 komoditas; Amalia et al. menunjukkan TFT kuat untuk komoditas pangan Indonesia. [P2][P10] | Price history harus menjadi fondasi dan baseline, tetapi perlu diuji apakah sinyal eksternal memberi informasi tambahan. |
| Climate/supply memang relevan | Gu et al. memakai cuaca + volume perdagangan; Nayak et al. menunjukkan NBEATSX/TransformerX dengan weather mengungguli benchmark dalam studi TOP crops. [P1][P3] | Climate/supply layak menjadi modality terpisah dan harus diuji melalui ablation. |
| News/sentiment memiliki manfaat, tetapi polaritas bukan satu-satunya informasi | Ewald & Li menemukan sentiment menurunkan error; Theofilou et al. menemukan article volume/intensity/persistence lebih informatif daripada sentiment tone murni. [P7][P8] | News branch perlu memasukkan temporal aggregation dan provenance, bukan hanya satu sentiment score harian. |
| Macro/logistics dapat membawa informasi di luar harga | MacLachlan et al. memperlihatkan nilai exogenous macro/logistics variables pada adaptive food-price forecasting. [P9] | Macro/logistics relevan, tetapi domainnya berbeda dari daily commodity-price forecasting sehingga harus dipertanggungjawabkan melalui data contract ARIF-Net. |
| Fusion lintas modality sudah didukung secara parsial | DIA-LSTM, GNN, hybrid TCN-XGBoost, dan TFT menunjukkan nilai attention/hybrid/temporal representation. [P1][P4][P5][P10] | ARIF-Net perlu menguji kontribusi fusion, bukan mengasumsikan fusion otomatis lebih baik. |
| Performa pada kondisi ekstrem belum menjadi protokol universal | Zhao et al. melaporkan performa pada dramatic price movements; Min et al. menilai smoothing terhadap fluktuasi jangka pendek. [P4][P5] | Shock/exreme subset harus menjadi evaluasi sekunder yang eksplisit. |
| Bukti dari Indonesia kuat pada price-only, tetapi belum menutup kebutuhan multimodal | Amalia et al. berfokus pada 10 strategic food commodities Indonesia dengan TFT dan multi-step forecasting, tetapi modelnya menggunakan historical price. [P10] | Ada ruang untuk menguji external modalities dan contribution analysis dalam konteks Indonesia. |
| Publication status tidak seragam | Paper Ewald & Li pada PDF yang diunggah secara eksplisit menyatakan preprint dan belum peer reviewed. [P7] | Paper tersebut digunakan sebagai supporting evidence untuk news/sentiment, bukan satu-satunya fondasi novelty claim. |

## 1.3 Masalah validitas penelitian yang juga harus diperhatikan

Official implementation plan menyatakan bahwa experimental protocol adalah bagian dari research contract. Repository saat ini memiliki masalah pada proses model selection: `train_arif_net.py` menggunakan test tensor untuk menghitung nilai yang diperlakukan sebagai `val_loss` dan memilih checkpoint. Konsekuensinya adalah test leakage/model-selection bias.

Temuan ini **bukan research gap literatur**, melainkan **research validity risk**. Karena itu, hasil benchmark repository saat ini tidak boleh digunakan sebagai bukti final keunggulan ARIF-Net sebelum protokol diperbaiki dan eksperimen diulang.

---

# 2. Research Goal

## 2.1 Goal utama — `LOCKED`

> **Mengembangkan model forecasting berbasis regresi yang mengintegrasikan historical price dynamics dengan beberapa sumber data eksternal untuk memprediksi pergerakan harga komoditas pangan pada periode berikutnya.**

Information flow yang dipertahankan:

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

## 2.2 Primary task

**Regression forecasting** adalah primary task.

Price shock bukan target classification utama. Shock ditempatkan sebagai fenomena sekunder untuk:

- shock-aware loss,
- subset evaluation,
- error analysis,
- extreme-movement monitoring.

Causal inference, policy simulation, dan economic-equilibrium modeling berada di luar research goal saat ini.

---

# 3. Scope Penelitian

## 3.1 Scope baseline — `LOCKED / WORKING BASELINE`

| Dimensi | Scope |
|---|---|
| Domain | Food/commodity price forecasting |
| Komoditas prioritas awal | Cabai merah keriting |
| Lokasi price data | Pasar tradisional / agregasi harga DKI Jakarta |
| Frequency | Harian |
| Historical input | Historical price dynamics wajib eksplisit |
| Climate/Supply | Curah hujan, suhu, anomaly bila valid, wilayah pemasok/sentra produksi |
| News/Sentiment | Berita terkait pangan, harga, inflasi, cuaca, supply, BBM/logistics; sentiment + daily aggregation + provenance |
| Macro/Logistics | Harga/perubahan harga BBM dan indikator logistik yang tersedia serta dapat dipertanggungjawabkan |
| Calendar | Hari, minggu, bulan, hari libur, dan event kalender yang diketahui sebelum prediction time |
| Primary output | Forecast price movement berbasis regresi |
| Shock | Fenomena sekunder untuk weighted loss/evaluation/error analysis |

## 3.2 Batasan

Tidak termasuk tanpa decision gate:

- causal policy simulation,
- intervention effect estimation,
- economic equilibrium modeling,
- seluruh komoditas nasional sekaligus,
- global generalization,
- production-grade market intervention system,
- automatic government decision system.

---

# 4. Research Questions

RQ di bawah adalah **baseline/proposed** dari official implementation plan. RQ tidak boleh berubah diam-diam karena perubahan RQ otomatis memengaruhi objective, experiment, dan struktur laporan.

| ID | Research Question | Bukti yang dibutuhkan |
|---|---|---|
| **RQ1** | **Seberapa efektif model regresi multimodal yang mengintegrasikan historical price dynamics dan faktor eksternal dalam memprediksi pergerakan harga komoditas pangan dibandingkan baseline?** | Perbandingan temporal-holdout dengan baseline yang sama dataset, preprocessing, split, dan selection protocol-nya. |
| **RQ2** | **Sejauh mana climate, sentiment, dan macro/logistics memberi tambahan informasi dibandingkan price-only atau reduced-modality models?** | Ablation per modality dan reduced-modality experiments. |
| **RQ3** | **Apakah mekanisme multimodal fusion dan/atau Cross-Modal Shock Gating memberikan kontribusi terukur terhadap regression forecasting?** | Full model vs no-fusion/alternative fusion dan full model vs no-SGU. |
| **RQ4** | **Bagaimana performa model pada periode pergerakan harga ekstrem dibandingkan keseluruhan periode?** | Overall regression metrics + shock subset metrics + sensitivity analysis. |
| **RQ5** | **Bagaimana model memberikan predictive contribution information tanpa menyimpulkan hubungan kausal yang belum diuji?** | Explainability/contribution analysis dengan batas interpretasi predictive, bukan causal. |

### RQ design note

RQ1 menjawab **apakah forecasting multimodal efektif**. RQ2 menjawab **modalitas mana yang menambah informasi**. RQ3 menjawab **apakah cara menggabungkan modalitas memberi kontribusi**. RQ4 menjawab **apakah kualitas forecast bertahan pada kondisi ekstrem**. RQ5 menjawab **bagaimana kontribusi model dapat diinterpretasikan secara non-kausal**.

---

# 5. Literature Review — 10 Paper Utama

> Notasi modality: **P** = historical price, **C** = climate/supply/weather, **N** = news/sentiment, **M** = macro/logistics/trade-related external variables.

| No. | Studi | Data & konteks | Target / horizon | Modalitas | Metode utama | Temuan utama | Limitasi / Research implication | Posisi untuk ARIF-Net |
|---|---|---|---|---|---|---|---|---|
| **P1** | **Gu et al. (2022) — Forecasting Agricultural Commodity Prices Using Dual Input Attention LSTM** | Cabbage dan radish di Korea Selatan; price, weather, trading volume, dan dynamic main production area | Forecasting bulanan | P + C + trading context | DIA-LSTM dengan feature attention + temporal attention | Dynamic production-area weather memberikan MAPE lebih rendah dibanding static-area setup; model juga mengungguli benchmark. | Belum memasukkan news dan macro/logistics secara lengkap; konteks pasar Korea dan horizon bulanan. | Evidence untuk multivariate fusion, attention, dan climate/supply branch. |
| **P2** | **Manogna et al. (2025) — Enhancing agricultural commodity price forecasting with deep learning** | 23 komoditas, daily wholesale price, 165 markets, AGMARKNET India | Price forecasting; price-only | P | ARIMA, SVR, XGBoost, MLP, RNN, LSTM, GRU, ESN | LSTM/GRU menunjukkan performa kuat dan menangkap nonlinear temporal dynamics lebih baik pada banyak komoditas. | Main setup tidak memasukkan external variables; authors recommend weather/global/policy/external signals dan hybrid models. | Strong foundation untuk price-only baseline dan justification external-factor extension. |
| **P3** | **Nayak et al. (2024) — Exogenous variable driven deep learning models for improved price forecasting of TOP crops in India** | Tomato, onion, potato; selected Indian markets; historical prices + precipitation + temperature | Weekly price forecasting | P + C | NBEATSX, TransformerX; dibanding ARIMAX, MLR, ANN, SVR, RFR, XGBoost | Exogenous-variable DL menunjukkan error lebih rendah; NBEATSX dan TransformerX menjadi hasil utama. | Exogenous set masih terbatas; future work membuka multiple variables dan spatial-temporal extension. | Evidence terkuat untuk climate/supply as external information. |
| **P4** | **Min et al. (2025) — RNN and GNN based prediction of agricultural prices with multivariate time series and its short-term fluctuations smoothing effect** | Empat komoditas Korea Selatan; daily prices + enam weather variables + week number | 7–14 day horizons | P + C | Stacked LSTM, StemGNN, T-GCN | Multivariate + GNN mengungguli RNN pada setting tertentu; smoothing short-term fluctuations memberi dampak lebih besar pada model multivariate. | Tidak ada news/sentiment atau macro/logistics; geografi dan komoditas spesifik. | Evidence untuk multivariate temporal modeling, relational signals, dan extreme/volatility-aware analysis. |
| **P5** | **Zhao et al. (2025) — A hybrid TCN-XGBoost model for agricultural product market price forecasting** | 65,750 historical data points dari rice, wheat, corn; market price series | Sliding-window time-series forecasting | P | TCN + XGBoost | TCN-XGBoost mengungguli beberapa benchmark dan tetap menunjukkan kinerja pada dramatic price movements. | External climate/policy/news tidak dimasukkan; future work mengarah ke external variables. | Evidence untuk hybrid architecture dan evaluasi pada large price movements. |
| **P6** | **Nayak et al. (2025) — Meta-transformer: leveraging metaheuristic algorithms for agricultural commodity price forecasting** | Weekly potato prices di beberapa Northern Indian markets | Weekly future price steps | P | Transformer + PSO/GWO/WOA | Metaheuristic tuning dapat meningkatkan forecasting dibanding benchmark tertentu. | Price-only, single-crop/regional; computationally heavier; external indicators belum menjadi input utama. | Evidence untuk advanced temporal model/optimization, tetapi bukan dasar multimodal novelty. |
| **P7** | **Ewald & Li — The role of news sentiment in salmon price prediction using deep learning** | Salmon spot price 2018–2022 + news headlines; FinBERT/TextBlob | Weekly forecasting | P + N | CNN-LSTM, LSTM, GRU, CNN, MLP | Menambahkan sentiment scores menurunkan prediction error pada deep-learning setup; CNN-LSTM menjadi model utama dalam paper. | PDF yang diunggah menyatakan preprint belum peer-reviewed; satu komoditas dan weekly context; sentiment-only external modality. | Evidence untuk news/sentiment branch, dengan status evidence pendukung dan caveat publication. |
| **P8** | **Theofilou et al. (2026) — AI-Driven News-Enhanced Machine Learning for Short-Term Corn Futures Price Forecasting** | Daily Chicago corn futures 2021–2024 + GDELT agriculture/corn-related news | Next-day short-term forecasting | P + N | LSTM + Ridge residual correction | Absolute RMSE/MAE hampir sama dengan baseline, tetapi directional accuracy naik sekitar 2.4 percentage points; article intensity/persistence lebih informatif daripada tone polarity murni. | Hanya news modality; no full multimodal fusion; paper sendiri menghindari causal claims. | Evidence sangat relevan untuk daily news integration dan feature aggregation/persistence design. |
| **P9** | **MacLachlan et al. (2025) — Adaptive food price forecasting improves public information in times of rapid economic change** | US food-at-home price/inflation + core CPI, congestion, energy, wholesale food, wages, income, money supply | Monthly food-price/inflation forecasting | P + M | Adaptive statistical learning / SARIMAX framework | Exogenous macro/logistics variables meningkatkan precision/explanatory power dalam perubahan ekonomi cepat. | Target, frequency, dan domain berbeda dari commodity daily price forecasting; bukan multimodal neural model. | Evidence konseptual/empiris untuk macro/logistics branch, tetapi transfer harus diuji. |
| **P10** | **Amalia et al. (2026) — A temporal fusion transformer for multi-step forecasting of Indonesia’s strategic food commodity prices** | Daily national-average prices untuk 10 strategic food commodities Indonesia | 30-day multi-step forecasting | P | TFT vs LSTM, GRU, ARIMA, Naïve | TFT unggul terutama pada commodity dengan variability tinggi, termasuk beberapa strategic food commodities Indonesia. | Price-centric; external climate/supply/news/macro belum menjadi input utama. Computational cost lebih tinggi dan performa tidak selalu dominan untuk setiap commodity. | Closest Indonesian price-forecasting precedent; supports local domain + advanced fusion candidate while leaving external-modality gap. |

---

# 6. Sintesis Lintas Literatur

| Dimensi | Evidence pada 10 paper | Kesimpulan untuk ARIF-Net |
|---|---|---|
| Historical price dynamics | Sangat konsisten hadir sebagai backbone pada paper forecasting. | **Mandatory input — LOCKED.** |
| Climate / supply | Gu, Nayak 2024, dan Min menunjukkan weather/exogenous context dapat membantu. | Layak menjadi branch external yang diuji secara ablation. |
| News / sentiment | Ewald & Li serta Theofilou menunjukkan nilai informasi berita, tetapi cara agregasi menentukan manfaatnya. | Tidak cukup memakai polarity tunggal; perlu temporal aggregation dan provenance. |
| Macro / logistics | MacLachlan menunjukkan external macro/logistics dapat menambah informasi dalam food-price forecasting. | Kandidat modality yang kuat secara konsep, tetapi feasibility dataset ARIF-Net harus diverifikasi. |
| Multimodal fusion | Attention, GNN, TCN-XGBoost, dan TFT memberi precedent pada temporal/fusion modeling. | Fusion adalah research question, bukan asumsi performa. |
| Advanced Transformer | Nayak 2025 dan Amalia 2026 menunjukkan Transformer/Meta-Transformer/TFT relevan. | Transformer adalah candidate architecture, bukan novelty dengan sendirinya. |
| Extreme price movement | Zhao dan Min memberi contoh evaluasi/smoothing pada kondisi fluktuatif. | ARIF-Net layak memiliki shock subset evaluation tanpa mengubah task menjadi classification. |
| Indonesia | Amalia 2026 memberi evidence langsung pada strategic food prices Indonesia. | Context lokal punya precedent yang kuat, tetapi extension multimodal masih perlu diuji. |
| Predictive contribution | Attention/feature importance tersedia di beberapa studi, tetapi tidak otomatis causal. | RQ5 harus dibatasi pada predictive contribution. |
| Leakage-safe protocol | Tidak menjadi kontribusi universal dari 10 paper; official ARIF-Net plan jauh lebih eksplisit soal temporal integrity. | Temporal availability + leakage audit harus menjadi research-engineering requirement. |

---

# 7. Research Gap

## 7.1 Gap utama — corpus-grounded

> **Dalam 10-paper corpus yang direview, bukti yang tersedia masih terfragmentasi: sebagian penelitian menggabungkan historical price + climate/supply, sebagian price + news/sentiment, dan sebagian price + macro/exogenous variables. Belum terdapat paper pada corpus yang secara eksplisit menunjukkan satu kerangka daily food-price regression forecasting yang sekaligus mengintegrasikan historical price dynamics, climate/supply, news/sentiment, dan macro/logistics dalam satu experimental framework yang sama.**

Pernyataan ini sengaja dibatasi pada **10-paper corpus yang diperiksa**. Hal ini lebih kuat secara akademik daripada mengklaim bahwa tidak ada penelitian semacam itu di seluruh literatur dunia.

## 7.2 Gap turunan

| Gap | Evidence | Respons ARIF-Net yang direncanakan |
|---|---|---|
| **G1 — Fragmented modality integration** | P3, P7, P8, P9 masing-masing memperlihatkan nilai modality eksternal berbeda. | Menguji integrasi multi-branch secara eksplisit. |
| **G2 — Modality contribution belum terisolasi secara menyeluruh** | Studi individual menunjukkan gain, tetapi tidak seluruh corpus memakai ablation lintas modality yang sama. | Price-only → reduced-modality → full multimodal ablation. |
| **G3 — Indonesian daily/local context** | P10 menunjukkan Indonesia tetapi price-centric dan multi-step. | Uji multimodal pada scope awal cabai merah keriting DKI Jakarta, subject to data feasibility. |
| **G4 — News information quality vs sentiment polarity** | P7 mendukung sentiment; P8 menunjukkan volume/intensity/persistence dapat lebih informatif daripada tone. | News branch perlu lebih kaya daripada satu scalar sentiment. |
| **G5 — Extreme movement evaluation** | P5 dan P4 menunjukkan pentingnya kondisi fluktuatif. | Shock subset metrics + optional shock-weighted objective. |
| **G6 — Methodological temporal integrity** | Official ARIF-Net plan menuntut strict temporal availability dan validation-only selection. | Data contract, temporal cutoff, leakage audit, validation-only model selection. |
| **G7 — Novelty boundary** | Transformer, LSTM, attention, sentiment, weather, dan hybrid models semuanya sudah memiliki precedent. | Novelty tidak boleh diklaim dari pemakaian satu teknik; contribution harus berada pada integration/fusion/evaluation design yang teruji. |

---

# 8. Research Positioning

## 8.1 Posisi penelitian

ARIF-Net diposisikan sebagai:

> **Multimodal regression forecasting framework for daily food-price movement**, bukan price-shock classifier.

Secara konseptual:

```text
Historical Price Dynamics
          |
          +---- Climate / Supply
          |
          +---- News / Sentiment
          |
          +---- Macro / Logistics
          |
          +---- Calendar
          |
          v
   Temporal / Modality Encoders
          |
          v
     Multimodal Fusion
          |
          v
  Optional Shock-aware Gate
          |
          v
    Regression Head
          |
          v
 Forecast Price Movement
```

## 8.2 Kandidat kontribusi — `PROPOSED`, belum final

1. Integrasi empat kelompok informasi dalam satu daily food-price regression framework.
2. Explicit price-dynamics representation agar external modality tidak menggantikan price backbone.
3. Multimodal fusion yang diuji terhadap reduced-modality baselines.
4. Shock-aware evaluation dan/atau objective sebagai secondary capability.
5. Predictive contribution analysis tanpa causal overclaim.
6. Leakage-safe temporal research protocol sebagai bagian dari reliability of evidence.

**Catatan:** Keenam item di atas belum boleh dipromosikan menjadi “novel contribution terbukti” sebelum eksperimen final, ablation, dan literature expansion mendukungnya.

---

# 9. Working Title

## Primary working title — `PROPOSED`

> **ARIF-Net: Multimodal Regression Forecasting of Daily Food Price Movements Using Historical Price, Climate-Supply, News Sentiment, and Macro-Logistics Signals**

## Alternatif title candidates

| Kandidat | Fokus | Status |
|---|---|---|
| **ARIF-Net: Multimodal Regression Forecasting of Daily Food Price Movements Using Historical Price, Climate-Supply, News Sentiment, and Macro-Logistics Signals** | Paling dekat dengan research goal global | **PROPOSED / PRIMARY WORKING TITLE** |
| **ARIF-Net: Multimodal Forecasting of Daily Red Chili Price Movements in DKI Jakarta with Climate, News, and Macro-Logistics Signals** | Paling spesifik terhadap scope Capstone saat ini | **PROPOSED** |
| **ARIF-Net: External-Signal-Aware Regression Forecasting for Daily Food Commodity Prices** | Lebih fleksibel bila commodity scope berubah | **PROPOSED** |

Target variable dan final forecast horizon masih OPEN, sehingga judul final sebaiknya tidak mengunci “return”, “percentage change”, atau horizon tertentu sebelum Decision Gate diselesaikan.

---

# 10. Decision Gates

| Gate | Keputusan | Status saat Phase 0 | Evidence/Exit condition |
|---|---|---|---|
| **DG-01** | Apakah scope cabai merah keriting + DKI Jakarta + daily feasible dari sisi price data? | **OPEN** | Coverage, frequency, missingness, source provenance, temporal continuity. |
| **DG-02** | Apakah target final = percentage change/return atau direct price? | **OPEN** | Evaluasi stability, interpretability, reconstruction, metric compatibility, dan research question. |
| **DG-03** | Forecast horizon final untuk baseline Capstone | **OPEN** | Minimal satu horizon yang feasible dan defensible; one-step adalah candidate working choice dari plan, bukan final claim. |
| **DG-04** | Representasi historical price dynamics | **OPEN / MANDATORY** | Historical price harus masuk eksplisit; pilih unified temporal encoder atau explicit price branch berdasarkan architecture review/experiment. |
| **DG-05** | Modality external yang benar-benar retained | **OPEN** | Climate/supply, news, macro/logistics hanya retained bila availability timing, coverage, provenance, dan missingness defensible. |
| **DG-06** | Fusion architecture | **PROPOSED** | Bandingkan candidate fusion/temporal architectures secara fair; jangan mengunci Transformer/SGU sebagai superior sebelum evidence. |
| **DG-07** | Shock definition + shock-aware objective | **OPEN / PROPOSED** | Working threshold 3% dapat diuji melalui sensitivity; pastikan actual/predicted shock definition konsisten. |
| **DG-08** | Final experimental protocol | **REQUIRED** | Train → validation → freeze → test; checkpoint selection hanya dari validation; leakage audit lulus. |
| **DG-09** | Novelty claim | **OPEN** | Final literature expansion + gap map + ablation evidence harus mendukung wording novelty. |
| **DG-10** | Batas Capstone → TA | **OPEN** | Capstone mempertahankan feasible single-commodity/local scope; generalization/multi-horizon/multi-commodity masuk gate perluasan. |

### Gate wajib sebelum Phase 1/eksperimen final

**DG-01, DG-02, DG-03, DG-04, DG-05, dan DG-08** harus memiliki keputusan terdokumentasi. DG-06 sampai DG-10 dapat dituntaskan bertahap, tetapi tidak boleh digunakan untuk membuat klaim final sebelum evidence-nya tersedia.

---

# 11. Phase 0 Exit Criteria

Phase 0 dinyatakan siap ditutup apabila seluruh kondisi berikut tercapai:

| Exit criterion | Status target |
|---|---|
| Problem statement disepakati | `READY` |
| Research Goal tetap konsisten dengan regression forecasting | `LOCKED` |
| Scope commodity/location/frequency sudah feasible | `VERIFIED` |
| RQ1–RQ5 reviewed dan testable | `READY` |
| 10-paper literature matrix selesai | `READY` |
| Gap map dibatasi pada evidence yang benar-benar tersedia | `READY` |
| Working title dipilih | `READY` |
| Target variable diputuskan | `DECIDED` |
| Forecast horizon diputuskan | `DECIDED` |
| External modality contract diputuskan | `DECIDED` |
| Experimental protocol bebas test-selection leakage | `REQUIRED BEFORE FINAL EVIDENCE` |
| Indexing verification (Scopus/WoS/other) tersedia | `OPEN` bila belum diverifikasi dari sumber yang sesuai |

---

# 12. Research Contract Snapshot

| Elemen | Final Phase-0 interpretation | Status |
|---|---|---|
| Problem | Price-only forecasting belum selalu menangkap external context; external-factor evidence masih terfragmentasi antar studi. | `READY` |
| Goal | Regression forecasting dengan historical price + external modalities. | `LOCKED` |
| Primary task | Regression forecasting. | `LOCKED` |
| Secondary phenomenon | Price shock / extreme movement. | `LOCKED AS SECONDARY` |
| Initial scope | Red chili, DKI Jakarta, daily. | `WORKING / FEASIBILITY GATE` |
| Core modalities | Price + climate/supply + news/sentiment + macro/logistics + calendar. | `LOCKED DIRECTION / OPEN DATA FEASIBILITY` |
| Main RQ | RQ1–RQ5. | `BASELINE / PROPOSED` |
| Literature basis | 10 uploaded papers + Consensus literature analysis. | `READY` |
| Core gap | Fragmented modality integration within the reviewed corpus; local Indonesian multimodal daily validation remains open. | `PROPOSED GAP` |
| Working title | ARIF-Net multimodal daily food-price regression forecasting title. | `PROPOSED` |
| Target | Percentage change vs direct price. | `OPEN` |
| Horizon | One-step candidate vs multi-horizon extension. | `OPEN` |
| Architecture | Multimodal encoder/fusion with explicit price dynamics. | `PROPOSED / OPEN` |
| Shock | Secondary evaluation/objective; working threshold 3%. | `OPEN / PROPOSED` |
| Evidence rule | Validation-only model selection; test remains sacred. | `REQUIRED` |

---

# 13. Literature References — 10 Paper Corpus

1. Gu, Y. H., Jin, D., Yin, H., Zheng, R., Piao, X., & Yoo, S. J. (2022). *Forecasting Agricultural Commodity Prices Using Dual Input Attention LSTM*. Agriculture, 12(2), 256. DOI: 10.3390/agriculture12020256.
2. Manogna, R. L., Dharmaji, V., & Sarang, S. (2025). *Enhancing agricultural commodity price forecasting with deep learning*. Scientific Reports, 15, 20903. DOI: 10.1038/s41598-025-05103-z.
3. Nayak, G. H. H., Alam, M. W., Singh, K. N., Avinash, G., Kumar, R. R., Ray, M., & Deb, C. K. (2024). *Exogenous variable driven deep learning models for improved price forecasting of TOP crops in India*. Scientific Reports, 14, 17203. DOI: 10.1038/s41598-024-68040-3.
4. Min, Y., Kim, Y. R., Hyon, Y., Ha, T., Lee, S., Hyun, J., & Lee, M. R. (2025). *RNN and GNN based prediction of agricultural prices with multivariate time series and its short-term fluctuations smoothing effect*. Scientific Reports, 15, 13681. DOI: 10.1038/s41598-025-97724-7.
5. Zhao, T., Chen, G., Suraphee, S., Phoophiwfa, T., & Busababodhin, P. (2025). *A hybrid TCN-XGBoost model for agricultural product market price forecasting*. PLOS One, 20(5), e0322496. DOI: 10.1371/journal.pone.0322496.
6. Nayak, G. H. H., Alam, M. W., Naik, B. S., Varshini, B. S., Avinash, G., Kumar, R. R., Ray, M., & Singh, K. N. (2025). *Meta-transformer: leveraging metaheuristic algorithms for agricultural commodity price forecasting*. Journal of Big Data, 12, 138. DOI: 10.1186/s40537-025-01196-5.
7. Ewald, C. O., & Li, Y. *The role of news sentiment in salmon price prediction using deep learning*. Uploaded copy states that it is a preprint and not peer reviewed; the Consensus bibliography lists Journal of Commodity Markets (2024), DOI 10.1016/j.jcomm.2024.100438.
8. Theofilou, A., Nastis, S. A., Mattas, K., & Theofilou, K. (2026). *AI-Driven News-Enhanced Machine Learning for Short-Term Corn Futures Price Forecasting*. Applied Sciences, 16, 1337. DOI: 10.3390/app16031337.
9. MacLachlan, M. J., Adjemian, M. K., Etienne, X., Sweitzer, M., Volpe III, R., & Zeng, W. (2025). *Adaptive food price forecasting improves public information in times of rapid economic change*. Nature Communications, 16, 6282. DOI: 10.1038/s41467-025-61660-x.
10. Amalia, S., Dhini, A., Zulkarnain, Za’in, C., & Surjandari, I. (2026). *A temporal fusion transformer for multi-step forecasting of Indonesia’s strategic food commodity prices*. Results in Engineering, 30, 110131. DOI: 10.1016/j.rineng.2026.110131.

---

# 14. Final Phase-0 Interpretation

Berdasarkan pemeriksaan ulang terhadap sepuluh paper dan penyelarasan dengan official implementation plan, **landasan penelitian ARIF-Net sudah memiliki support literatur yang cukup untuk masuk ke Phase 1, tetapi bukan berarti seluruh desain teknis sudah final**.

Yang sudah cukup kuat adalah arah problem, primary task regression, kewajiban historical price dynamics, relevansi external modalities, dan kebutuhan evaluasi pada kondisi ekstrem. Yang masih harus diputuskan secara eksplisit adalah target variable, horizon, final modality contract, representation harga historis, fusion architecture, shock objective, dan experimental protocol.

Research gap yang paling defensible untuk saat ini bukan "membuat model deep learning baru" atau "menggunakan Transformer", karena keduanya sudah memiliki banyak precedent. Gap yang lebih tepat adalah **fragmented external-signal integration within the reviewed corpus**, ditambah kebutuhan untuk menguji **kontribusi setiap modality dan fusion mechanism** pada **daily food-price regression forecasting dalam konteks Indonesia**, dengan **temporal integrity/leakage control** sebagai syarat validitas evidence.

Phase 0 karena itu berfungsi sebagai kontrak agar implementasi berikutnya tidak bergeser menjadi price-shock classification, tidak menghilangkan historical price backbone, tidak memasukkan future information, dan tidak membuat novelty claim sebelum eksperimen membuktikannya.

```

---

# APPENDIX C — ARSIP HISTORIS v1.1.0

> Arsip ini disimpan untuk traceability. Isinya adalah salinan dokumen v1.1.0 yang pernah berlaku. **Bukan sumber keputusan aktif** jika berbeda dengan canonical v2.0.0.

```markdown
# ARIF-Net — Phase 0 Research Contract v1.1.0

**Status:** Kontrak Kerja Phase 0 yang Direvisi  
**Basis:** `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v1.0.0(1).md` + `Literatur Review Refrensi Jurnal ARIF-Net.md` + 10 PDF jurnal yang diunggah + 17 bibliografi yang diberikan peneliti + literatur tambahan untuk validasi research gap  
**Research Model:** ARIF-Net — *Agricultural Risk and Inflation Forecasting Network*  
**Tema Penelitian:** *Multimodal Food Price Forecasting and Intelligence*  
**Tugas Utama:** *Regression Forecasting*  
**Peneliti / Pemilik Proyek:** Muhamad Nur Arif  
**Tanggal Revisi:** 24 September 2026

---

## 0. Tujuan dan Status Dokumen

Dokumen ini merupakan kontrak penelitian Phase 0 untuk memastikan arah penelitian ARIF-Net tidak bergeser ketika memasuki tahap data engineering, pemodelan, eksperimen, productization, dan Tugas Akhir.

Dokumen ini harus selalu membedakan antara:

- **fakta yang telah diverifikasi**;
- **keputusan yang telah dikunci**;
- **rekomendasi metodologis**;
- **hal yang masih terbuka**;
- **hal yang wajib divalidasi sebelum evidence final diterima**.

Aturan governance mengikuti baseline resmi ARIF-Net: AI bertindak sebagai *research assistant*, reviewer, analyst, dan implementation assistant; keputusan akhir metodologi tetap berada pada peneliti. Perubahan terhadap *research goal*, target variable, horizon, modality, arsitektur inti, objective, definisi shock, research questions, novelty claim, experimental protocol, atau scope harus diperlakukan sebagai *decision gate*.

---

# 1. Ringkasan Revisi Phase 0

Phase 0 diperbarui setelah peneliti menetapkan arah berikut:

1. Model tetap menggunakan **regression forecasting** sebagai tugas utama.
2. Hasil penelitian harus dapat digunakan baik untuk **percentage change** maupun **direct price** pada kebutuhan pengguna.
3. Forecasting menggunakan **multi-horizon** dengan batas maksimum **365 hari**.
4. Hasil forecast harus dapat divisualisasikan sebagai **trajectory/pergerakan harga**, bukan kurva yang dipaksa monoton.
5. Historical price tetap menjadi sinyal inti dan direpresentasikan melalui **explicit price backbone**.
6. Climate/supply, news/sentiment, serta macro/logistics tetap berada dalam arah scope final.
7. Arsitektur boleh berkembang apabila research gap yang tervalidasi menunjukkan peluang kontribusi yang lebih kuat.
8. Shock tidak lagi diperlakukan sebagai sekadar ambang tetap 3%; definisi final harus mempertimbangkan **horizon dan distribusi data**, dengan 3% dipertahankan sebagai baseline/sensitivity reference.
9. Research gap tidak boleh dibangun hanya dari “belum ada model multimodal”; literature terbaru sudah mengandung berbagai kombinasi modality.
10. Kandidat novelty diarahkan pada **horizon-conditioned, reliability-aware multimodal fusion**, explicit historical-price backbone, controlled ablation, serta evaluasi extreme movement yang sesuai horizon.

### Catatan penting tentang novelty

Kandidat novelty di dalam dokumen ini **belum merupakan klaim novelty global yang telah terbukti**. Wording final novelty hanya boleh dibuat lebih kuat setelah systematic literature search dan eksperimen empiris selesai.

---

# 2. Status Keputusan Utama

| Elemen | Keputusan / Arah | Status |
|---|---|---|
| Tugas utama | Regression forecasting | **LOCKED** |
| Historical price | Input wajib dan menjadi backbone | **LOCKED** |
| Modality eksternal | Climate/supply, news/sentiment, macro/logistics | **LOCKED DIRECTION** |
| Target kanonik model | Relative price movement / percentage change | **RECOMMENDED** |
| Direct price | Direkonstruksi dari forecast relative movement | **RECOMMENDED** |
| Forecast horizon | Multi-horizon, maksimum 365 hari | **LOCKED BOUNDARY** |
| Trajectory forecast | Dapat menghasilkan jalur harian dan tidak dipaksa monoton | **PROPOSED** |
| Representasi harga | Explicit Historical Price Backbone | **RECOMMENDED** |
| Arsitektur | Reliability-aware + horizon-conditioned multimodal temporal fusion | **RECOMMENDED CANDIDATE** |
| Shock | Fenomena sekunder, bukan classification utama | **LOCKED** |
| Shock threshold | Horizon-scaled dan data-derived; 3% menjadi baseline/sensitivity | **RECOMMENDED** |
| Research Questions | RQ1–RQ5 versi revisi | **PROPOSED** |
| Working title | Horizon-conditioned multimodal regression | **PROPOSED** |
| Generalisasi | Dirancang reusable; bukti generalisasi harus diuji | **PROPOSED** |

---

# 3. Masalah Penelitian

## 3.1 Masalah domain

Harga komoditas pangan memiliki ketergantungan temporal, seasonality, nonlinearitas, volatilitas, serta pergerakan ekstrem. Perubahannya tidak hanya muncul dari sejarah harga itu sendiri, tetapi dapat berkaitan dengan kondisi cuaca, supply dan wilayah produksi, distribusi/logistik, kondisi ekonomi, serta informasi publik melalui berita.

Literatur yang direview menunjukkan bahwa berbagai sumber informasi tersebut dapat memberikan informasi prediktif, tetapi biasanya diteliti dalam kombinasi yang berbeda-beda. Dengan demikian, masalah penelitian ARIF-Net bukan sekadar mencari model yang lebih kompleks, tetapi mencari cara untuk **menggabungkan sinyal heterogen yang memiliki karakter temporal, frekuensi, kelengkapan, dan waktu ketersediaan yang berbeda** tanpa menghilangkan struktur utama dari historical price dynamics.

## 3.2 Fenomena lapangan yang relevan

Fenomena yang menjadi latar ARIF-Net bukan hanya “harga naik”, tetapi **perubahan rezim harga** dan **pergerakan ekstrem dua arah**.

Contoh konteks yang perlu diperhatikan:

- data anomali harga pangan Bapanas menunjukkan komoditas dapat berpindah antara kondisi harga rendah, normal, dan tinggi dalam periode berbeda;
- harga cabai dapat dipengaruhi oleh pola musiman, supply, distribusi, dan respons pasar;
- kondisi iklim 2026 di Indonesia menunjukkan dinamika lingkungan yang nyata, termasuk laporan BMKG tentang El Niño yang sangat kuat dan potensi keterlambatan awal musim hujan 2026/2027.

Fakta lapangan tersebut digunakan untuk membangun **research context**, bukan untuk menyimpulkan hubungan sebab-akibat. ARIF-Net tetap merupakan penelitian prediktif, bukan penelitian kausal.

---

# 4. Tujuan Penelitian

## 4.1 Tujuan utama

> **Mengembangkan kerangka regression forecasting multimodal yang menggunakan historical food-price dynamics sebagai backbone utama dan secara kondisional mengintegrasikan sinyal climate/supply, news/sentiment, serta macro/logistics untuk memprediksi pergerakan harga pangan pada berbagai horizon hingga maksimum satu tahun.**

## 4.2 Sasaran metodologis

ARIF-Net ditujukan untuk:

1. mempertahankan historical price sebagai sumber informasi utama;
2. menguji nilai tambah setiap modality eksternal;
3. menguji apakah mekanisme fusion benar-benar memberikan nilai tambah;
4. mengondisikan kontribusi modality berdasarkan horizon forecast;
5. mempertimbangkan availability/freshness/quality informasi ketika melakukan fusion;
6. menghasilkan trajectory forecast sampai horizon yang dipilih tanpa constraint monoton;
7. mengevaluasi robustness pada extreme price movement;
8. menyediakan analisis contribution tanpa membuat klaim kausal yang tidak diuji.

---

# 5. Target Variable

## 5.1 Target kanonik yang direkomendasikan

Target internal utama menggunakan **relative price movement**:

```text
y(t,h) = (P(t+h) - P(t)) / P(t)
```

atau dapat dievaluasi dalam bentuk transformasi log-return sebagai varian implementasi numerik, selama makna user-facing tetap berupa perubahan relatif harga.

## 5.2 Direct price sebagai output aplikasi

Direct price tidak perlu menjadi model kedua yang berdiri sendiri.

Dari prediksi perubahan relatif:

```text
P_hat(t+h) = P(t) × (1 + y_hat(t,h))
```

maka sistem dapat menampilkan dua representasi:

```text
Perubahan relatif : +8.2%
Harga estimasi     : Rp xx.xxx/kg
```

Pendekatan ini menjaga satu kontrak target penelitian sekaligus memenuhi kebutuhan aplikasi.

## 5.3 Alasan target relative movement diprioritaskan

Target ini lebih selaras dengan fokus penelitian terhadap **pergerakan**, dapat digunakan pada berbagai skala harga, dan memudahkan analisis lintas horizon maupun lintas objek. Namun keputusan implementasi final tetap harus melewati validasi distribusi data dan stabilitas target pada Phase 1.

---

# 6. Forecast Horizon Contract

## 6.1 Batas horizon

Penelitian menggunakan **multi-horizon forecasting** dengan batas maksimum:

> **365 hari setelah forecast origin**.

Batas ini merupakan *research boundary*, bukan berarti seluruh horizon sampai 365 hari pasti memiliki kualitas yang sama.

## 6.2 Horizon evaluasi yang direkomendasikan

```text
1 hari
3 hari
7 hari
14 hari
30 hari
90 hari
180 hari
365 hari
```

Grid ini merupakan kandidat evaluasi representatif. Horizon final yang digunakan pada Capstone harus disesuaikan dengan feasibility data dan jumlah observasi efektif.

## 6.3 Forecast trajectory

ARIF-Net tidak boleh memaksakan monotonicity.

Contoh trajectory yang valid secara konseptual:

```text
naik → datar → turun → naik → turun → naik
```

Model harus bebas menghasilkan pola tersebut apabila didukung oleh pola historis dan external signals.

## 6.4 Aturan informasi masa depan

Pada forecast origin `t`, model hanya boleh menggunakan informasi yang **telah tersedia pada saat t**.

Dilarang menggunakan:

- berita yang baru diterbitkan setelah `t`;
- cuaca aktual masa depan;
- macro/logistics yang belum dirilis pada `t`;
- nilai supply masa depan;
- hasil observasi lain yang baru tersedia setelah forecast origin.

Aturan ini sangat penting, khususnya untuk horizon panjang.

---

# 7. Representasi Historical Price

## Keputusan rekomendasi

ARIF-Net menggunakan **Explicit Historical Price Backbone**.

Arsitektur konseptual:

```text
Historical Price
       ↓
Price Encoder
       ↓
Price Representation
       │
       ├──────────────┐
       │              │
Climate/Supply ──────┤
News/Sentiment ──────┤
Macro/Logistics ─────┤
Calendar/Horizon ────┘
             ↓
   Reliability-Aware Fusion
             ↓
 Horizon-Conditioned Decoder
             ↓
 Multi-Horizon Regression Path
```

## Alasan

Historical price harus dapat dibedakan dari external modalities karena research goal mewajibkan model mempelajari **price dynamics**, bukan sekadar mengandalkan climate, sentiment, atau macro features.

Explicit branch juga memungkinkan eksperimen yang bersih:

```text
Price-only
Price + Climate
Price + News
Price + Macro
Price + Climate + News
Price + Climate + Macro
Price + News + Macro
Full ARIF-Net
```

Dengan demikian, penambahan modality dan mekanisme fusion dapat dievaluasi secara terpisah.

---

# 8. Kandidat Arsitektur Final

## 8.1 Nama kerja

> **HRA-MTF — Horizon-Conditioned Reliability-Aware Multimodal Temporal Fusion**

Nama ini bersifat sementara dan bukan klaim novelty final.

## 8.2 Lapisan 1 — Price Backbone

Kandidat utama:

```text
Historical price window
        ↓
Dilated Temporal Convolutional Encoder
        ↓
Lightweight temporal/recurrent block
        ↓
Temporal attention
```

Blok temporal ringan dapat dibandingkan antara GRU, BiLSTM, atau Transformer ringan. Model besar tidak menjadi default karena data ARIF-Net relatif kecil dibanding dataset yang biasa dipakai untuk pretraining/foundation models.

## 8.3 Lapisan 2 — Encoder per modality

### Climate / Supply

Kandidat fitur:

- rainfall;
- temperature;
- anomaly;
- drought/wetness indicator;
- production-region signal;
- supply/arrival indicator;
- lag dan rolling features.

### News / Sentiment

News tidak boleh direduksi menjadi satu nilai polarity.

Kandidat fitur harian:

- rata-rata sentiment;
- dispersion sentiment;
- article volume;
- intensity;
- persistence;
- topic/category;
- recency/freshness;
- source count/provenance.

Temuan Theofilou et al. penting sebagai dasar karena volume, intensitas, dan persistence berita dapat lebih informatif daripada polarity murni dalam konteks tertentu.

### Macro / Logistics

Kandidat:

- BBM/fuel;
- indikator transport/logistics;
- inflation/economic indicator yang relevan;
- market indicator;
- distribution/supply proxy.

Hanya variabel yang dapat memenuhi aturan timestamp dan availability yang boleh dipertahankan.

### Calendar / Known-future information

Kandidat:

- hari;
- minggu;
- bulan;
- hari libur;
- event kalender yang memang telah diketahui sebelumnya.

Calendar diposisikan sebagai fitur pendukung, bukan sumber shock utama.

---

# 9. Reliability-Aware Multimodal Fusion

Ini merupakan kandidat kontribusi metodologis utama.

Masalah praktis ARIF-Net:

```text
Price       : lengkap
Climate     : lengkap
News        : sebagian / tidak merata
Macro       : frekuensi berbeda
Supply      : mungkin terdapat missingness
```

Model multimodal sederhana dapat memperlakukan seluruh modality seolah-olah tersedia dengan kualitas identik. ARIF-Net justru mengusulkan agar setiap modality memiliki informasi tambahan mengenai reliabilitasnya.

Untuk modality `m`, model dapat menerima:

```text
representation_m
availability_m
freshness_m
quality_m
```

kemudian mempelajari bobot:

```text
w_m(t,h) = Gate(representation, availability, freshness, horizon)
```

Sehingga kontribusi modality dapat berubah menurut waktu dan horizon.

**Catatan:** mekanisme ini masih harus diuji. Jika ablation menunjukkan tidak ada manfaat, mekanisme tidak boleh dipaksakan sebagai kontribusi final.

---

# 10. Horizon-Conditioned Fusion

Research gap yang lebih menarik dibanding sekadar “multimodal” adalah kemungkinan bahwa informasi yang relevan untuk horizon pendek tidak sama dengan horizon panjang.

Secara konseptual:

```text
Forecast horizon
        ↓
Horizon embedding
        ↓
Fusion weights
        ↓
Different modality contribution
```

Model tidak diasumsikan bahwa news, climate, atau macro selalu dominan. Dominasi tersebut harus menjadi **hasil eksperimen**.

Contoh hipotesis:

```text
h = 1–7 hari       → market/news context mungkin lebih cepat berubah
h = 14–30 hari     → climate/supply dapat menjadi lebih relevan
h = 90–365 hari    → seasonal/macro signals mungkin semakin penting
```

Contoh di atas hanya hipotesis desain dan tidak boleh dipresentasikan sebagai temuan sebelum diuji.

---

# 11. Cross-Modal Fusion

Kandidat mekanisme:

```text
Price Representation
        ↓
Price Query / Anchor
        ↓
Cross-Modal Attention
   ↙          ↓          ↘
Climate      News       Macro
   ↓          ↓           ↓
Reliability-aware fused state
```

Historical price diperlakukan sebagai **anchor/query** sehingga external modalities memberikan context terhadap price dynamics, bukan menggantikan backbone harga.

---

# 12. Decoder Multi-Horizon

Decoder harus menerima representasi horizon sehingga satu model dapat menghasilkan beberapa horizon tanpa memaksa proses forecasting menjadi recursive-only.

```text
Forecast origin t
       ↓
Shared context
       ↓
Horizon-conditioned decoder
       ↓
r(t+1), r(t+2), ..., r(t+H)
       ↓
H ≤ 365
```

Aplikasi dapat menampilkan seluruh trajectory harian atau hanya titik horizon utama.

---

# 13. Definisi Price Shock

## 13.1 Baseline lama

Repository sebelumnya menggunakan:

```text
|ΔP| > 3%
```

3% tidak dihapus dari histori proyek. Namun angka tersebut tidak lagi dianggap sebagai satu-satunya definisi final untuk seluruh horizon.

## 13.2 Definisi yang direkomendasikan

Untuk horizon `h`, gunakan threshold berbasis distribusi:

```text
τ_h = Qα(|r(t,h)|)
```

dengan `Qα` dihitung menggunakan **data TRAINING saja**.

Kandidat awal:

```text
α = 0.90
α = 0.95
α = 0.975
α = 0.99
```

Contoh interpretasi:

```text
Normal       : |r_h| < τ_h
Shock        : |r_h| ≥ τ_h
Severe shock : |r_h| ≥ Q99_h
```

## 13.3 Alasan

Perubahan 3% tidak memiliki makna statistik yang sama pada satu hari dan satu tahun. Threshold berbasis horizon lebih konsisten untuk multi-horizon forecasting.

## 13.4 Hubungan dengan fenomena lapangan

Definisi statistik harus tetap dapat dibandingkan dengan indikator operasional seperti anomali harga pangan Bapanas. Indikator operasional tersebut berfungsi sebagai konteks, bukan pengganti target regresi.

---

# 14. Shock-Aware Objective

Shock tetap merupakan fenomena sekunder.

Kandidat loss:

```text
L = L_base + λ × L_shock_weighted
```

Namun bobot shock harus menggunakan threshold yang telah ditentukan sebelumnya untuk setiap horizon.

Tujuan mekanisme ini adalah meningkatkan robustness terhadap rare/extreme movement tanpa mengubah primary task menjadi classification.

Eksperimen wajib membandingkan:

```text
Base Loss
vs
Shock-Weighted Loss
```

---

# 15. Literature Review dan Positioning

## 15.1 Temuan utama dari 17 paper inti

| Kelompok | Temuan | Implikasi |
|---|---|---|
| Price-only DL | LSTM/GRU/TCN/Transformer dapat memodelkan nonlinear temporal dynamics. | Price-only baseline wajib. |
| Climate / Supply | Weather dan supply-related variables dapat meningkatkan forecasting. | Climate/supply layak menjadi external branch. |
| News / Sentiment | Sentiment dan karakteristik coverage berita dapat menambah informasi. | News harus direpresentasikan lebih kaya dari satu polarity. |
| Macro / Logistics | Variabel makro dan logistik dapat membantu dalam kondisi ekonomi berubah cepat. | Macro/logistics relevan tetapi availability harus diverifikasi. |
| Multimodal | Fusion lintas modality mulai semakin umum. | “Multimodal” saja bukan novelty. |
| Multi-horizon | Forecast quality dan driver dapat berubah menurut horizon. | Horizon-conditioned design layak diuji. |
| Extreme movement | Model tertentu menunjukkan manfaat evaluasi khusus pada periode ekstrem. | Shock subset evaluation diperlukan. |
| Explainability | SHAP/attention/feature contribution dapat membantu analisis. | Gunakan predictive contribution, bukan causal claim. |

## 15.2 Paper yang paling dekat dengan tiap komponen

| Komponen ARIF-Net | Referensi utama |
|---|---|
| Explicit price dynamics | Manogna et al. (2025), Amalia et al. (2026), Zhao et al. (2025) |
| Price + climate | Gu et al. (2022), Nayak et al. (2024), Min et al. (2025) |
| Price + news | Ewald & Li (2024), Theofilou et al. (2026) |
| Price + macro/logistics | MacLachlan et al. (2025), Han et al. (2023) |
| Multi-source agricultural data | Ghonge & Kulkarni (2026) |
| Multimodal fusion | Wang et al. (2025), Pan (2025) |
| Multi-horizon food-price Indonesia | Amalia et al. (2026) |
| Extreme movement | Zhao et al. (2025), Min et al. (2025) |

---

# 16. Research Matrix — 17 Paper Inti

| No. | Studi | Data/Konteks | Target/Horizon | Modality | Metode | Temuan utama | Celah terhadap ARIF-Net |
|---|---|---|---|---|---|---|---|
| 1 | Amalia et al. (2026) | 10 komoditas pangan strategis Indonesia, harian | Multi-step 30 hari | Price | TFT | TFT kuat terutama pada komoditas sangat variatif. | Price-centric; external signals dan systematic modality ablation belum menjadi fokus utama. |
| 2 | Avinash et al. (2024) | Harga komoditas pertanian, fokus volatilitas | 1, 4, 8, 12 minggu | Price + technical | HMM-guided DL | Hidden states + technical indicators membantu forecasting. | Tidak full multimodal; belum reliability-aware. |
| 3 | Busker et al. (2024) | Krisis ketahanan pangan Horn of Africa | Sampai 12 bulan | Climate/hazard + socioeconomics | XGBoost early warning | Menunjukkan potensi multimodal long-lead warning. | Target bukan harga; relevansi terutama untuk konsep early warning dan horizon panjang. |
| 4 | Ewald & Li (2024) | Salmon spot price + headline news | Weekly | Price + sentiment | CNN-LSTM/DL + FinBERT/TextBlob | Sentiment dapat menurunkan error. | Satu external modality; uploaded copy menyatakan preprint/not peer reviewed. |
| 5 | Ghonge & Kulkarni (2026) | Soybean India: market, weather, trade, supply | Multi-source forecasting | Price + weather + trade + supply | Wide-and-Deep | Integrasi multi-source membantu prediksi soybean. | Belum news/sentiment; belum reliability-aware/horizon-conditioned fusion. |
| 6 | Gu et al. (2022) | Cabbage/radish Korea + weather + trading volume | Monthly | Price + climate + trading | DIA-LSTM | Dynamic production-area weather dan attention meningkatkan MAPE. | Tidak news/macro/logistics; konteks bulanan. |
| 7 | Gupta et al. (2024) | 14 komoditas + economic indicators + historical/technical features | Price-change forecasting | Price + economic/technical | Beragam ML/DL | Mendukung penggunaan percentage change dan perbandingan banyak model. | Tidak menawarkan fusion multimodal khusus. |
| 8 | Han et al. (2023) | Global food prices + macro/oil/production/uncertainty | Monthly | Price + macro/global factors | ML + SHAP | Macro/global factors menunjukkan predictive importance. | Global bulanan; bukan daily local regression multimodal. |
| 9 | MacLachlan et al. (2025) | US food prices + macro/logistics | Monthly | Price + macro/logistics | Adaptive statistical learning | External macro/logistics membantu precision dan explanatory power. | Domain/frequency berbeda; bukan multimodal neural fusion. |
| 10 | Manogna et al. (2025) | 23 komoditas, 165 pasar India | Daily | Price | ARIMA, ML, DL | LSTM/GRU kuat menangkap nonlinear temporal behavior. | External context tidak digunakan. |
| 11 | Min et al. (2025) | 4 komoditas Korea + 6 weather variables | Short-term, termasuk 14 hari | Price + climate | LSTM, StemGNN, T-GCN | Multivariate/GNN dan smoothing membantu pada setting tertentu. | Belum news/macro/logistics. |
| 12 | Nayak et al. (2025) | Potato Northern India | Weekly | Price | Transformer + PSO/GWO/WOA | Metaheuristic tuning meningkatkan Transformer pada setting tertentu. | Price-only; optimization bukan novelty multimodal. |
| 13 | Nayak et al. (2024) | TOP crops India + weather | Crop-price forecasting | Price + climate | NBEATSX/TransformerX | Exogenous weather meningkatkan forecasting. | External modality terbatas. |
| 14 | Pan (2025) | Multi-source agriculture: Agmarknet/AGRIS/WorldCereal/GAEZ | Risk/early warning | Multisource | Deep learning + knowledge graph | Menggabungkan sumber data terstruktur dan heterogen. | Fokus lebih luas pada risk intelligence; bukan controlled daily price regression. |
| 15 | Theofilou et al. (2026) | Corn futures harian + GDELT news | Next-day | Price + news | LSTM + Ridge residual | Directional accuracy naik; volume/intensity/persistence berita informatif. | Belum full multimodal; sangat relevan untuk desain news branch. |
| 16 | Wang et al. (2025) | Demand + text + satellite imagery | 1–28 hari | Time series + text + image | Causal-Aware Multimodal Transformer | Cross-modal attention + specialized encoders membantu multimodal forecasting. | Domain demand, bukan food price; berguna sebagai precedent arsitektur. |
| 17 | Zhao et al. (2025) | Rice/wheat/corn historical data | Sliding window + dramatic movement | Price | TCN-XGBoost | Hybrid temporal/nonlinear kuat pada dramatic movements. | External modalities tidak terintegrasi. |

---

# 17. Literatur Tambahan untuk Validasi Research Gap

Literatur tambahan yang ditemukan saat menguji bibliografi memperkecil beberapa klaim gap lama.

| Studi tambahan | Dampak terhadap ARIF-Net |
|---|---|
| Yi et al. (2026) | Menunjukkan price + news + macro dan beberapa horizon; mengurangi kekuatan novelty “news + macro + multi-horizon”. |
| Wang, Yu & An (2025) | Menunjukkan dynamic sentiment weighting dan multi-stream agricultural forecasting; mengurangi novelty “dynamic sentiment weighting”. |
| Salsabila & Nooraeni (2025) | Menunjukkan news sentiment untuk food-price forecasting Indonesia; mengurangi novelty “news sentiment + Indonesia”. |
| Ünal et al. (2026) | Menunjukkan climate + macro + explainable time-series modeling; mengurangi novelty “climate + macro + explainability”. |

Konsekuensinya, novelty ARIF-Net **harus berada pada kombinasi desain yang lebih spesifik**, bukan pada satu komponen populer.

---

# 18. Fenomena → Literatur → Gap

## 18.1 Fenomena 1 — Perubahan harga dapat terjadi dua arah

**Fenomena:** harga dapat masuk kondisi rendah maupun tinggi, bukan hanya spike ke atas.  
**Literatur:** Amalia, Manogna, Zhao, Avinash, Min menunjukkan dinamika/volatilitas merupakan bagian penting forecasting.  
**Implikasi:** model perlu belajar relative movement dan extreme movement dua arah.

## 18.2 Fenomena 2 — External conditions berubah terhadap waktu

**Fenomena:** weather, supply, distribution, dan macro conditions tidak statis.  
**Literatur:** Gu, Nayak, Min, MacLachlan, Ghonge menunjukkan external variables dapat membantu.  
**Implikasi:** modality tidak boleh diperlakukan sebagai fitur statis sederhana.

## 18.3 Fenomena 3 — Informasi publik tidak hanya berupa polarity

**Fenomena:** informasi berita memiliki volume, intensity, persistence, recency, dan topic.  
**Literatur:** Ewald & Li mendukung sentiment; Theofilou menunjukkan coverage intensity/persistence dapat lebih informatif daripada tone polarity pada setting tertentu.  
**Implikasi:** news branch harus dibangun lebih kaya daripada satu skor sentiment.

## 18.4 Fenomena 4 — Horizon mengubah masalah forecasting

**Fenomena:** prediksi besok dan prediksi satu tahun bukan masalah yang identik.  
**Literatur:** Amalia, Yi dan studi multi-horizon menunjukkan perbedaan perilaku dan/atau kontribusi driver menurut horizon.  
**Implikasi:** fusion sebaiknya mempertimbangkan horizon.

## 18.5 Fenomena 5 — Ketersediaan data tidak seragam

**Fenomena:** price, news, climate, macro, dan supply memiliki frekuensi serta release time berbeda.  
**Literatur:** studi multimodal menunjukkan perlunya specialized encoders/cross-modal mechanisms, sementara ARIF-Net menambahkan aturan availability sebagai kebutuhan deployment.  
**Implikasi:** reliability-aware fusion menjadi kandidat methodological gap.

---

# 19. Research Gap yang Direvisi

## G1 — Integrasi modality telah maju, sehingga gap bukan lagi sekadar “belum multimodal”

Literatur terbaru telah menunjukkan price + climate, price + news, price + macro, bahkan market + weather + trade + supply dan multimodal transformer pada domain terkait.

**Konsekuensi:** ARIF-Net tidak boleh mengklaim “multimodal” sebagai novelty tunggal.

## G2 — Reliability/availability-aware fusion masih menjadi kandidat gap yang lebih spesifik

Pada kasus nyata, modality memiliki tingkat kelengkapan, freshness, dan waktu ketersediaan berbeda. Dalam corpus agricultural-price yang direview, belum teridentifikasi framework yang secara eksplisit menjadikan **availability/freshness/quality** sebagai bagian dari learned fusion weight untuk daily food-price forecasting.

## G3 — Horizon-conditioned external contribution masih memiliki ruang

Studi terdahulu menunjukkan bahwa driver atau performance dapat berubah menurut horizon, tetapi belum ditemukan pada corpus utama suatu desain yang secara eksplisit menggabungkan:

```text
explicit price backbone
+
multiple heterogeneous modalities
+
horizon-conditioned fusion
+
reliability-aware weighting
```

dalam satu daily food-price regression framework.

## G4 — Extreme movement perlu dinilai relatif terhadap horizon

Threshold fixed 3% tidak mempunyai makna statistik yang identik pada seluruh horizon. Karena itu, evaluasi extreme movement dapat menggunakan threshold yang diturunkan dari distribusi return setiap horizon.

## G5 — Research contribution harus dibuktikan melalui ablation

Model yang lebih besar dan lebih banyak fitur bisa saja menghasilkan improvement karena complexity, bukan karena informasi yang benar-benar berguna. Controlled ablation wajib membedakan:

```text
information gain
vs
fusion gain
vs
architecture gain
vs
shock-objective gain
```

---

# 20. Kandidat Novelty

## 20.1 Kandidat novelty utama

> **Kerangka regression forecasting multimodal yang mempertahankan explicit historical-price backbone dan secara dinamis mengondisikan kontribusi climate/supply, news/sentiment, dan macro/logistics berdasarkan forecast horizon serta reliabilitas/ketersediaan informasi untuk menghasilkan prediksi pergerakan harga pangan harian hingga satu tahun.**

## 20.2 Kontribusi metodologis pendukung

1. **Explicit Price Anchor** — historical price tetap menjadi backbone yang dapat diidentifikasi.
2. **Reliability-Aware Fusion** — bobot modality mempertimbangkan availability/freshness/quality.
3. **Horizon-Conditioned Fusion** — kontribusi modality dapat berubah menurut horizon.
4. **Dense Multi-Horizon Regression Path** — trajectory harian dapat dihasilkan hingga H ≤ 365 tanpa constraint monotonic.
5. **Horizon-Scaled Shock Evaluation** — extreme movement dievaluasi menggunakan threshold data-derived per horizon.
6. **Controlled Modality/Fusion Ablation** — kontribusi informasi dipisahkan dari sekadar bertambahnya kompleksitas.

Semua butir di atas masih **candidate contribution** sampai eksperimen menunjukkan kontribusi yang konsisten.

---

# 21. Batasan Klaim Novelty

Dilarang menulis:

> “ARIF-Net adalah model multimodal food-price forecasting pertama di dunia.”

Wording yang diperbolehkan pada tahap ini:

> “Dalam literatur yang direview untuk penelitian ini, ARIF-Net mengeksplorasi kombinasi yang masih kurang dieksplorasi berupa explicit historical-price backbone, reliability-aware fusion, dan horizon-conditioned multimodal regression pada daily local food-price forecasting.”

Wording tersebut harus diperbarui setelah systematic search yang lebih luas.

---

# 22. Research Questions Final — Versi Phase 0

### RQ1 — Efektivitas Forecasting Multimodal

> **Seberapa efektif model regresi multimodal ARIF-Net dalam memprediksi pergerakan harga pangan harian dibandingkan baseline price-only dan reduced-modality?**

### RQ2 — Nilai Tambah Setiap Modality

> **Sejauh mana climate/supply, news/sentiment, dan macro/logistics memberikan tambahan informasi prediktif terhadap historical price dynamics berdasarkan controlled modality ablation?**

### RQ3 — Reliability dan Horizon pada Fusion

> **Apakah mekanisme reliability-aware dan horizon-conditioned multimodal fusion meningkatkan kualitas forecasting dibandingkan fusion statis atau model yang tidak menggunakan mekanisme tersebut?**

### RQ4 — Ketahanan pada Pergerakan Ekstrem

> **Bagaimana performa ARIF-Net pada extreme price movement di berbagai horizon dibandingkan performa pada kondisi normal dengan menggunakan definisi shock yang diskalakan terhadap horizon?**

### RQ5 — Kontribusi Prediktif Lintas Horizon

> **Bagaimana kontribusi prediktif masing-masing modality berubah menurut forecast horizon tanpa menafsirkannya sebagai hubungan kausal?**

---

# 23. Working Title

## Judul kerja utama

> **ARIF-Net: Horizon-Conditioned Reliability-Aware Multimodal Regression Forecasting of Daily Food Price Movements**

## Judul khusus Capstone

> **ARIF-Net: Horizon-Conditioned Multimodal Regression Forecasting of Daily Red Chili Price Movements Using Climate-Supply, News, and Macro-Logistics Signals**

## Judul fleksibel untuk pengembangan TA/publikasi

> **ARIF-Net: Reliability-Aware Multimodal Forecasting of Food Price Movements Across Multiple Horizons**

Judul final dapat dikunci setelah target implementasi, horizon evaluasi, data scope, dan architecture candidate selesai divalidasi.

---

# 24. Modality Contract

| Modality | Status | Fitur kandidat | Aturan waktu |
|---|---|---|---|
| Historical Price | Wajib | price, return/change, volatility, lag, rolling statistics | Hanya informasi ≤ forecast origin |
| Climate | Final direction | rainfall, temperature, anomaly, drought/wetness | Harus sudah tersedia pada `t` |
| Supply | Final direction | production, arrival, supply proxy | Timestamp dan availability wajib diverifikasi |
| News | Final direction | sentiment, volume, intensity, persistence, topic, recency | Gunakan waktu publikasi/availability |
| Macro | Final direction | inflation/economic/market indicators | Gunakan waktu rilis, bukan kalender naif |
| Logistics | Final direction | fuel, transport/distribution proxy | Frequency dan release timing diaudit |
| Calendar | Pendukung | weekday, month, holiday/event | Nilai yang memang diketahui sebelumnya boleh digunakan |

Modality dapat diturunkan statusnya bila tidak lolos coverage, provenance, temporal availability, atau quality audit.

---

# 25. Rancangan Eksperimen Minimum

```text
M0  Naive / simple statistical baseline
M1  Price-only classical / ML
M2  Price-only deep learning
M3  Price + Climate/Supply
M4  Price + News
M5  Price + Macro/Logistics
M6  Price + Climate/Supply + News
M7  Price + Climate/Supply + Macro/Logistics
M8  Price + News + Macro/Logistics
M9  Full multimodal + fusion statis
M10 Full multimodal + horizon-conditioned fusion
M11 Full multimodal + reliability-aware fusion
M12 Full candidate ARIF-Net + shock-aware objective
```

Tujuannya bukan sekadar memenangkan benchmark, tetapi mengisolasi sumber improvement.

---

# 26. Validation Gates

| Gate | Pertanyaan | Evidence yang dibutuhkan |
|---|---|---|
| DG-01 | Apakah data harga cabai merah keriting/DKI Jakarta feasible? | Coverage, missingness, frequency, provenance |
| DG-02 | Apakah percentage movement layak menjadi target kanonik? | Distribusi, stabilitas, reconstruction, metric compatibility |
| DG-03 | Apakah horizon hingga 365 hari feasible? | Effective sample size, backtest stability, coverage |
| DG-04 | Apakah external data tersedia pada forecast origin? | Release/publication timestamp + cutoff audit |
| DG-05 | Apakah tiap modality memberi nilai tambah? | Controlled ablation |
| DG-06 | Apakah explicit price backbone lebih tepat? | Unified-vs-explicit comparison |
| DG-07 | Apakah horizon-conditioned fusion membantu? | Static-vs-conditioned comparison |
| DG-08 | Apakah reliability-aware gate membantu? | Missing/stale modality tests + ablation |
| DG-09 | Apakah shock-aware objective membantu? | Loss ablation + threshold sensitivity |
| DG-10 | Apakah attribution robust? | SHAP/attention/gate analysis |
| DG-11 | Apakah generalisasi teruji? | Cross-time; cross-location/commodity bila data tersedia |
| DG-12 | Apakah novelty claim dapat dipertahankan? | Systematic literature search + final experimental evidence |

---

# 27. Experimental Validity Contract

Pipeline wajib:

```text
RAW SOURCES
    ↓
CLEANING
    ↓
TEMPORAL ALIGNMENT
    ↓
AVAILABILITY / CUTOFF AUDIT
    ↓
CHRONOLOGICAL TRAIN / VALIDATION / TEST
    ↓
TRAIN-ONLY TRANSFORM FIT
    ↓
MODEL SELECTION — VALIDATION ONLY
    ↓
MODEL FREEZE
    ↓
BLIND TEST
    ↓
ERROR / SHOCK / ATTRIBUTION ANALYSIS
```

Current repository audit telah menemukan historical test-selection leakage. Oleh karena itu, benchmark lama tidak boleh otomatis dijadikan evidence final sebelum protocol diperbaiki dan eksperimen dijalankan ulang.

---

# 28. Validasi Data yang Wajib Dilakukan pada Phase 1

## Price

- apakah daily observation kontinu;
- apakah definisi pasar/agregasi konsisten;
- apakah ada perubahan sumber atau metodologi pencatatan;
- apakah missing period dapat dijelaskan.

## Climate

- apakah stasiun/wilayah mewakili sentra produksi;
- apakah terdapat perubahan coverage;
- apakah agregasi harian valid;
- apakah data sudah tersedia pada saat forecast.

## Supply

- apakah volume supply/arrival tersedia harian atau perlu agregasi;
- apakah waktu publish sama dengan tanggal observasi;
- apakah data benar-benar menggambarkan pressure supply.

## News

- apakah sumber dapat dilacak;
- apakah artikel relevan terhadap commodity/market;
- apakah publication time tersedia;
- apakah sentiment model dan fallback tercatat;
- apakah agregasi harian tidak memasukkan berita masa depan.

## Macro/Logistics

- apakah frequency data cocok;
- apakah release time diketahui;
- apakah carry-forward/forward-fill dilakukan dengan benar;
- apakah indikator benar-benar tersedia ketika forecasting dilakukan.

---

# 29. Kriteria Phase 0 Selesai

### Sudah ditetapkan

- [x] Regression forecasting sebagai primary task.
- [x] Historical price sebagai input wajib.
- [x] External modality tetap menjadi arah scope.
- [x] Multi-horizon dengan batas maksimum 365 hari.
- [x] Direct price dan percentage movement dapat ditampilkan dari satu canonical forecast.
- [x] Explicit price backbone menjadi rekomendasi representasi.
- [x] Reliability-aware + horizon-conditioned fusion menjadi candidate architecture.
- [x] Shock tetap secondary phenomenon.
- [x] Research gap diperketat setelah memeriksa literatur 2025–2026.
- [x] RQ diperbarui.
- [x] Working title diperbarui.

### Wajib divalidasi sebelum freeze Phase 0 final

- [ ] Feasibility data komoditas/lokasi.
- [ ] Implementasi target final.
- [ ] Horizon grid final.
- [ ] Temporal availability tiap modality.
- [ ] Threshold shock final + sensitivity protocol.
- [ ] Perbaikan test-selection leakage.
- [ ] Architecture experiment protocol.
- [ ] Status indexing jurnal jika dibutuhkan untuk persyaratan akademik.
- [ ] Systematic literature search yang lebih luas untuk menguatkan novelty claim.

---

# 30. Snapshot Research Contract

| Elemen | Interpretasi Phase 0 | Status |
|---|---|---|
| Problem | Price-only tidak selalu menangkap external context; faktor eksternal bersifat heterogen dan asynchronous. | READY |
| Goal | Multimodal regression forecasting. | LOCKED |
| Primary task | Regression forecasting. | LOCKED |
| Secondary phenomenon | Extreme/price shock. | LOCKED AS SECONDARY |
| Scope awal | Red chili, DKI Jakarta, daily. | WORKING / FEASIBILITY GATE |
| Core inputs | Historical price + climate/supply + news/sentiment + macro/logistics + calendar. | LOCKED DIRECTION |
| Canonical target | Relative price movement. | RECOMMENDED |
| User output | Percentage movement + reconstructed direct price. | RECOMMENDED |
| Horizon | Variable, H ≤ 365 days. | LOCKED BOUNDARY |
| Price representation | Explicit price backbone. | RECOMMENDED |
| Fusion | Reliability-aware + horizon-conditioned. | CANDIDATE |
| Shock definition | Horizon-scaled empirical threshold. | RECOMMENDED |
| Main gap | Reliability-aware + horizon-conditioned heterogeneous fusion pada daily local food-price regression, within reviewed corpus. | PROPOSED |
| Novelty | Candidate, belum terbukti secara global. | OPEN |
| Final RQ | RQ1–RQ5 revised. | PROPOSED |
| Working title | Horizon-Conditioned Reliability-Aware Multimodal Regression Forecasting... | PROPOSED |
| Evidence protocol | Train → validation → freeze → blind test. | REQUIRED |

---

# 31. Phase 0 Bottom Line

ARIF-Net **tidak lagi diposisikan sekadar sebagai “model deep learning baru untuk prediksi harga pangan”**.

Posisi penelitian yang lebih tepat adalah:

> **Membangun dan menguji secara ketat kerangka regression forecasting multimodal yang mempertahankan historical price sebagai anchor, menggabungkan climate/supply, news/sentiment, dan macro/logistics secara kondisional berdasarkan horizon dan reliabilitas informasi, serta mengevaluasi pergerakan ekstrem menggunakan pendekatan yang sesuai dengan masing-masing horizon.**

Komponen seperti LSTM, Transformer, attention, sentiment, weather, XGBoost, dan multimodal fusion sudah memiliki precedent. Karena itu, keberhasilan novelty ARIF-Net bergantung pada apakah desain fusion dan evidence protocol di atas benar-benar menghasilkan kontribusi yang terukur.

Prinsip utama penelitian:

```text
HISTORICAL PRICE REMAINS CORE
          +
EXTERNAL MODALITIES ARE TESTED, NOT ASSUMED
          +
HORIZON MATTERS
          +
MODALITY RELIABILITY MATTERS
          +
SHOCK IS SECONDARY
          +
TEST SET REMAINS BLIND
```

---

# 32. Referensi Utama

1. Amalia, S., Dhini, A., Zulkarnain, Za’in, C., & Surjandari, I. (2026). *A Temporal Fusion Transformer for Multi-step Forecasting of Indonesia’s Strategic Food Commodity Prices*. Results in Engineering. DOI: 10.1016/j.rineng.2026.110131.
2. Avinash, G., Ramasubramanian, V., Ray, M., Paul, R., Godara, S., Nayak, G. H. H., Kumar, R., Manjunatha, B., Dahiya, S., & Iquebal, M. A. (2024). *Hidden Markov guided Deep Learning models for forecasting highly volatile agricultural commodity prices*. Applied Soft Computing, 158, 111557. DOI: 10.1016/j.asoc.2024.111557.
3. Busker, T., Van Den Hurk, B., De Moel, H., Van Den Homberg, M. V. D., Van Straaten, C., Odongo, R. A., & Aerts, J. C. J. H. (2024). *Predicting Food-Security Crises in the Horn of Africa Using Machine Learning*. Earth’s Future, 12. DOI: 10.1029/2023EF004211.
4. Ewald, C. O., & Li, Y.-Y. (2024). *The role of news sentiment in salmon price prediction using deep learning*. Journal of Commodity Markets. DOI: 10.1016/j.jcomm.2024.100438.
5. Ghonge, V., & Kulkarni, Y. R. (2026). *An advanced wide-and-deep learning framework for soybean price forecasting using market, weather, trade, and supply data*. MethodsX, 17, 104030. DOI: 10.1016/j.mex.2026.104030.
6. Gu, Y., Jin, D., Yin, H.-L., Zheng, R., Piao, X.-H., & Yoo, S.-J. (2022). *Forecasting Agricultural Commodity Prices Using Dual Input Attention LSTM*. Agriculture, 12(2), 256. DOI: 10.3390/agriculture12020256.
7. Gupta, H., Kumari, R., Rajput, S., & Puri, N. (2024). *Forecasting Commodity Prices using Machine Learning*. International Journal of Scientific Research in Science and Technology. DOI: 10.32628/IJSRST52411110.
8. Han, X., Yuan, T., Wang, D., Zhao, Z., & Gong, B. (2023). *How to understand high global food price? Using SHAP to interpret machine learning algorithm*. PLOS ONE, 18. DOI: 10.1371/journal.pone.0290120.
9. MacLachlan, M. J., Adjemian, M. K., Etienne, X. L., Sweitzer, M., Volpe, R. J., & Zeng, W. (2025). *Adaptive food price forecasting improves public information in times of rapid economic change*. Nature Communications. DOI: 10.1038/s41467-025-61660-x.
10. Manogna, R. L., Dharmaji, V., & Sarang, S. (2025). *Enhancing agricultural commodity price forecasting with deep learning*. Scientific Reports, 15. DOI: 10.1038/s41598-025-05103-z.
11. Min, Y., Kim, Y. R., Hyon, Y., Ha, T., Lee, S.-J., Hyun, J., & Lee, M.-R. (2025). *RNN and GNN based prediction of agricultural prices with multivariate time series and its short-term fluctuations smoothing effect*. Scientific Reports, 15. DOI: 10.1038/s41598-025-97724-7.
12. Nayak, G. H. H., Alam, M. W., Naik, B. S., Varshini, B. S., Avinash, G., Kumar, R. R., Ray, M., & Singh, K. N. (2025). *Meta-transformer: leveraging metaheuristic algorithms for agricultural commodity price forecasting*. Journal of Big Data, 12, 138. DOI: 10.1186/s40537-025-01196-5.
13. Nayak, G. H. H., Alam, M. W., Singh, K., Avinash, G., Kumar, R., Ray, M., & Deb, C. K. (2024). *Exogenous variable driven deep learning models for improved price forecasting of TOP crops in India*. Scientific Reports, 14. DOI: 10.1038/s41598-024-68040-3.
14. Pan, D. (2025). *A Price Risk Early Warning Model for Agricultural Products Based on the Integration of Deep Learning and Knowledge Graphs*. IEEE Access, 13, 162623–162638. DOI: 10.1109/ACCESS.2025.3609817.
15. Theofilou, A., Nastis, S., Mattas, K., & Theofilou, K. (2026). *AI-Driven News-Enhanced Machine Learning for Short-Term Corn Futures Price Forecasting*. Applied Sciences, 16, 1337. DOI: 10.3390/app16031337.
16. Wang, Y., Ding, G.-Y., Zeng, Z.-Y., & Yang, S.-Y. (2025). *Causal-Aware Multimodal Transformer for Supply Chain Demand Forecasting: Integrating Text, Time Series, and Satellite Imagery*. IEEE Access, 13, 176813–176829. DOI: 10.1109/ACCESS.2025.3619552.
17. Zhao, T.-W., Chen, G.-Q., Suraphee, S., Phoophiwfa, T., & Busababodhin, P. (2025). *A hybrid TCN-XGBoost model for agricultural product market price forecasting*. PLOS ONE, 20. DOI: 10.1371/journal.pone.0322496.

### Referensi tambahan untuk validasi gap

- Yi et al. (2026). *Unveiling dynamics in agricultural supply chain: A transformer-enhanced framework for commodity price modeling*. International Journal of Production Economics, 294, 109820. DOI: 10.1016/j.ijpe.2025.109820.
- Wang, L., Yu, L., & An, W. (2025). *Two-Stream Reinforcement Ensemble Framework for Agricultural Commodity Prices Forecasting Using Textual Data*. Journal of Forecasting, 44(8), 2386–2404. DOI: 10.1002/for.70015.
- Salsabila, A., & Nooraeni, R. (2025). *Forecasting Shallot Prices in Indonesia Using News-Based Sentiment Indicators*. Jurnal Online Informatika, 10(1), 165–176. DOI: 10.15575/join.v10i1.1422.
- Ünal, E. et al. (2026). *Temperature shocks and food inflation: Multicountry evidence from visual time-series transformers and attention-based feature selection*. Journal of Environmental Management, 413, 130268. DOI: 10.1016/j.jenvman.2026.130268.

---

# 33. Aturan Status untuk Dokumentasi Berikutnya

| Status | Makna |
|---|---|
| `LOCKED` | Keputusan resmi penelitian; tidak boleh diubah diam-diam. |
| `RECOMMENDED` | Rekomendasi teknis yang kuat, tetapi masih dapat diganti oleh peneliti. |
| `PROPOSED` | Kandidat yang harus mendapat pembuktian empiris. |
| `OPEN` | Belum diputuskan atau belum memiliki evidence yang cukup. |
| `VERIFIED` | Telah didukung oleh sumber/data yang diperiksa. |
| `REQUIRED` | Harus diselesaikan sebelum evidence final dapat diterima. |
| `UNVERIFIED` | Belum cukup bukti untuk dipresentasikan sebagai fakta. |

AI/agen tidak boleh mengubah `PROPOSED`, `OPEN`, atau `UNVERIFIED` menjadi `LOCKED` atau `VERIFIED` tanpa evidence atau keputusan peneliti.

```

---

# APPENDIX D — ARSIP TEKS ASLI v2.0.0 YANG DIAMANDEMEN (NON-OPERATIF)

## D.1 Teks asli §3.1 (v2.0.0)

### 3.1 Prioritas Capstone → TA

Tiga komoditas prioritas:

| Prioritas | Komoditas | Market target |
|---|---|---|
| 1 | **Cabai Merah Keriting (CMK)** | Pasar Induk Kramat Jati (PIKJ), DKI Jakarta |
| 2 | **Bawang Merah** | Pasar Induk Kramat Jati (PIKJ), DKI Jakarta |
| 3 | **Beras** — tipe pasar harus dikunci saat Data Contract | Pasar Induk Beras Cipinang (PIBC), DKI Jakarta |

### Catatan taxonomy

Istilah “cabai”, “bawang”, dan “beras” tidak boleh dibiarkan sebagai label generik pada dataset final. Phase 1 harus mengunci:

- jenis cabai;
- jenis/grade bawang;
- kelas/grade beras;
- satuan harga;
- definisi pasar.

Untuk Capstone, **Cabai Merah Keriting** direkomendasikan sebagai bentuk utama komoditas cabai karena paling konsisten dengan kebutuhan harga pasar dan konteks PIKJ.


## D.2 Baris asli Master Matrix §5.1 (v2.0.0)

| **Harga target** | Bapanas Panel Harga / PIKJ / PIBC | Harian | Harga, tanggal, market | nilai hari `t` boleh dipakai untuk origin `t` bila sudah tercatat pada cutoff | **FEASIBLE** |
| **Climate** | BMKG/Data Online/PTSP + station data | Harian tersedia sesuai station/access | RR, Tavg, Tn, Tx, RH, sunshine, wind, dll. | gunakan observed past; aggregate per supplier region | **FEASIBLE, access/data retrieval Phase 1** |

**END OF CONTRACT v2.1.0**
