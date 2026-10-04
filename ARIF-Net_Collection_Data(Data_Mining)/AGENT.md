# AGENT.md — ARIF-Net · Phase 1 · Pengumpulan Data (Iklim · PIHPS · PIBC · IPJ · News)

> **Untuk:** Claude Code atau agen AI lain yang mengeksekusi, memelihara, atau memperpanjang koleksi data Phase 1 ARIF-Net.
> **Isi:** §1–§12 = **Iklim (Open-Meteo)** · §13 = **Harga target PIHPS** · §14 = **Harga pelengkap PIBC** · §15 = status lintas sumber · §16 = **Harga pelengkap IPJ** · §17 = **News**. Aturan peran (§1), integritas (§8), dan format laporan (§10) **berlaku untuk semua sumber**.
> **Folder kerja:** `ARIF-Net_Collection_Data(Data_Mining)\` → `Iklim\` (iklim), `Historical_Komoditas\` (semua sumber harga: `PIHPS\`, `PIBC\`, `IPJ\`), `News\` (berita). Ketiganya setara.
> **Alur kerja wajib (semua sumber):** analisis dokumen otoritas → probe read-only → **rencana disetujui pengguna** → codebase + test offline → smoke → ⛔ persetujuan → full → normalisasi → audit → docs. Setiap keputusan metodologis = decision gate pengguna, dicatat di docs paket.
> **Env:** Conda **`arif-net`** (Python 3.13). Env lama `arifnet-climate` sudah **dihapus** dan tidak dipakai lagi.
> **Otoritas:** `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v2.0.0.md` (§0.5, §9, §10.2a) → `ARIF-Net_Phase_0_Research_Contract_v2.1.0.md` (§0B, §4.5–4.6, §5.6, §6.4).
> **Status (3 Okt 2026):** Langkah A, 1–7 **PASS**. Dataset iklim lengkap 324/324 chunk. Langkah 8 (dokumentasi) berjalan di `Iklim/docs/PHASE1_COLLECTION_OPENMETEO.md`.

Baca dokumen ini **seluruhnya** sebelum menjalankan perintah apa pun. Jika instruksi pengguna, README, atau kode bertentangan dengan dokumen ini atau dengan kedua dokumen otoritas, **berhenti dan tanyakan**. Jangan merekonsiliasi diam-diam.

---

## 1. Peran dan batas wewenang

Kamu adalah **data engineering assistant**, **bukan** pengambil keputusan metodologi.

**Boleh:**
- menjalankan script di paket ini sesuai urutan langkah;
- membaca output, log, dan laporan, lalu meringkas hasil untuk pengguna;
- memperbaiki bug teknis (crash, path, parsing) **tanpa** mengubah perilaku metodologis, lalu melaporkan perubahannya;
- mengoreksi nama parameter API yang salah eja **hanya** bila dokumentasi resmi Open-Meteo menunjukkan nama yang benar untuk variabel yang **sama** (lihat §7.3).

**Tidak boleh tanpa persetujuan eksplisit pengguna (= decision gate baru):**
- menambah, mengurangi, atau mengganti variabel, lokasi, periode, unit, timezone, atau model;
- memakai model `best_match` atau berpindah model otomatis;
- mengimputasi, mengisi, menghaluskan, atau mengagregasi data di collection layer;
- menerapkan lag t−5, pemotongan `usable_end_date`, rolling, anomaly, atau feature engineering apa pun (semuanya Phase 3);
- mengedit, menimpa, atau menghapus raw JSON;
- menaikkan batas kuota di `rate_limit` di atas nilai default;
- mengubah status keputusan (`DECIDED`, `LOCKED`, `CANDIDATE`, dst.) di dokumen proyek;
- mengarang angka, hasil, nama parameter, URL, atau status verifikasi.

Jika ragu, **tanyakan pengguna**. Lebih baik berhenti daripada mengubah riset diam-diam.

---

## 2. Konteks proyek (ringkas)

- **ARIF-Net** = *Agricultural Risk and Inflation Forecasting Network*. Primary task: **supervised multimodal regression forecasting** pergerakan harga pangan harian di Jakarta.
- Target: `r(t,h) = (P(t+h) − P(t)) / P(t)`, multi-horizon 1/3/7/14/30/90/180/365 hari. Historical price adalah explicit backbone (`DECIDED`).
- Modality eksternal: climate/supply, news/sentiment, macro/logistics, calendar. **Dokumen ini hanya mencakup modality climate.**
- Capstone dan Tugas Akhir memakai satu pipeline. Pemilik keputusan: project owner (pengguna).

### 2.1 Riwayat keputusan yang relevan

1. **Phase 0** dibekukan 24 Sep 2026 (Contract v2.0.0). Phase 1 mencakup eksekusi data, audit temporal, dan implementasi.
2. 1–2 Okt 2026: 24 decision gate Phase 1 (`P1-DG-01…24`) diputuskan pengguna → **Plan v2.0.0** dan **Contract v2.1.0**.
3. 2 Okt 2026: paket iklim lama (v1) dihapus pengguna. Paket baru dibangun dari dokumen otoritas dan dokumentasi resmi Open-Meteo.
4. 2 Okt 2026, **CP2**: centroid Kabupaten Cirebon jatuh di dalam Kota Cirebon (1,7 km dari batas kabupaten). **Keputusan: tetap centroid** (P1-DG-12), dicatat sebagai keterbatasan.
5. 2 Okt 2026, **CP3/CP4**: smoke core dan reserve PASS dengan `era5_seamless`. **Fallback ERA5 tidak dipakai.**
6. 2 Okt 2026, **CP5**: full collection 324/324. Batas harian dinaikkan sementara 8.000 → 9.000 atas izin pengguna, lalu dikembalikan.
7. 3 Okt 2026, **CP6 — opsi A**: seri iklim untuk fitur **dipotong di 2026-09-24** (`usable_end_date`), diterapkan di Phase 3. Raw dan processed tetap utuh sampai 2026-09-30.
8. 3 Okt 2026: CSV processed dilacak **Git LFS**. Env `arifnet-climate` dihapus.

### 2.2 Scope komoditas (P1-DG-04/05/13)

| Komoditas (taxonomy PIHPS) | comcat_id |
|---|---|
| Cabai Merah Keriting | `com_14` |
| Bawang Merah Ukuran Sedang | `com_11` |
| Beras Kualitas Medium I | `com_3` |

Bawang putih **dikeluarkan**. Komoditas PIHPS lain termasuk extended scope TA.

---

## 3. Keputusan yang dikodekan dan WAJIB dipatuhi

| Gate | Keputusan | Implementasi |
|---|---|---|
| P1-DG-09 | Sumber iklim = **Open-Meteo Historical Weather API** (data *reanalysis*, bukan observasi stasiun) | `config/request_settings.json` → `endpoint` |
| P1-DG-10 | Model = **ERA5-Seamless**; fallback **ERA5** hanya lewat smoke test (dicatat). **Best Match dilarang** | `model_primary`, `model_fallback`; model terpakai di `config/state.json` → `model_in_use` = `era5_seamless` |
| P1-DG-11 | 18 lokasi pemasok kandidat, Tier 1/Tier 2 per komoditas; **semua dikoleksi** | `config/locations.json` |
| P1-DG-12 | Titik = **centroid poligon kabupaten** (GADM 4.1, EPSG:6933 → WGS84) | `scripts/compute_centroids.py` |
| P1-DG-14 | **9 variabel core** + **11 reserve**; request dan folder terpisah | `config/variables.json` |
| P1-DG-15 | `celsius`, `ms`, `mm`, `iso8601`, `Asia/Jakarta` | `config/request_settings.json` |
| P1-DG-16 | Periode koleksi **2018-01-01 → 2026-09-30** | `start_date`, `end_date` |
| P1-DG-17 | Release lag fitur ≤ **t−5**, diterapkan di **Phase 3** | `release_lag_days_for_features` |
| CP6 opsi A | Seri fitur iklim berakhir **2026-09-24**, diterapkan di **Phase 3** | `usable_end_date` |

`scripts/verify_setup.py` menyimpan nilai-nilai yang dikunci di atas dan memberi **FAIL** bila config menyimpang.

### 3.1 Lokasi (P1-DG-11) — status CANDIDATE, koordinat final

| location_id | Kabupaten | Provinsi | Tier per komoditas | lat | lon |
|---|---|---|---|---|---|
| garut | Garut | Jawa Barat | CMK 1 · Bawang 2 | -7.35951 | 107.78883 |
| cianjur | Cianjur | Jawa Barat | CMK 1 | -7.13358 | 107.15776 |
| bandung_barat | Bandung Barat | Jawa Barat | CMK 1 | -6.89711 | 107.41495 |
| bandung | Bandung | Jawa Barat | CMK 1 | -7.09994 | 107.61075 |
| sumedang | Sumedang | Jawa Barat | CMK 1 | -6.82506 | 107.98087 |
| magelang | Magelang | Jawa Tengah | CMK 1 | -7.50157 | 110.24663 |
| brebes | Brebes | Jawa Tengah | Bawang 1 | -7.05928 | 108.92756 |
| cirebon | Cirebon | Jawa Barat | Bawang 1 · Beras 1 | -6.74541 | 108.55129 ⚠️ |
| indramayu | Indramayu | Jawa Barat | Bawang 1 · Beras 1 | -6.44857 | 108.16875 |
| karawang | Karawang | Jawa Barat | Beras 1 | -6.25204 | 107.35394 |
| subang | Subang | Jawa Barat | Beras 1 | -6.48414 | 107.73220 |
| demak | Demak | Jawa Tengah | Beras 1 · Bawang 2 | -6.91109 | 110.63202 |
| temanggung | Temanggung | Jawa Tengah | CMK 2 | -7.25788 | 110.13565 |
| nganjuk | Nganjuk | Jawa Timur | Bawang 2 | -7.59737 | 111.93840 |
| bima | Bima | Nusa Tenggara Barat | Bawang 2 | -8.47469 | 118.61870 |
| sragen | Sragen | Jawa Tengah | Beras 2 | -7.38720 | 110.97751 |
| cilacap | Cilacap | Jawa Tengah | Beras 2 | -7.49089 | 108.89037 |
| sukoharjo | Sukoharjo | Jawa Tengah | Beras 2 | -7.68080 | 110.83464 |

Semua adalah **Kabupaten** (bukan Kota). Tier menunjukkan kekuatan bukti sebagai pemasok Jakarta, **bukan** volume. ⚠️ Centroid Cirebon berada di dalam Kota Cirebon; keputusannya tetap dipakai (§2.1 butir 4).

### 3.2 Variabel (P1-DG-14) — semua TERVERIFIKASI (smoke PASS 2 Okt 2026)

**Core (9), dipakai modelling:** `precipitation_sum` (mm), `precipitation_hours` (h), `temperature_2m_mean` / `_max` / `_min` (°C), `relative_humidity_2m_mean` (%), `sunshine_duration` (s), `et0_fao_evapotranspiration` (mm), `soil_moisture_7_to_28cm_mean` (m³/m³).

**Reserve (11), dikoleksi tetapi tidak dipakai modelling:** `relative_humidity_2m_max` / `_min` (%), `vapour_pressure_deficit_max` (kPa), `shortwave_radiation_sum` (MJ/m²), `cloud_cover_mean` (%), `wind_speed_10m_max` / `_mean` (m/s), `soil_moisture_0_to_7cm_mean` / `28_to_100cm_mean` (m³/m³), `soil_temperature_0_to_7cm_mean` (°C), `rain_sum` (mm, QC).

**Tidak dikoleksi (jangan ditambahkan):** snowfall, apparent temperature, sunrise/sunset, daylight duration, wet bulb, dewpoint, pressure, dominant wind direction, wind gusts, weather code, soil temperature 7–28/28–100/0–100 cm, soil moisture 0–100 cm. **Tidak ada variabel hourly.**

---

## 4. Metode API Open-Meteo (sesuai dokumentasi resmi)

Sumber: https://open-meteo.com/en/docs/historical-weather-api

### 4.1 Endpoint dan metode

```text
GET https://archive-api.open-meteo.com/v1/archive
```
- HTTP **GET** dengan query string. Tidak ada body, header khusus, atau login. `apikey` tidak dipakai (hanya untuk komersial).
- Sukses: HTTP 200, JSON. Gagal: **HTTP 400** `{"error": true, "reason": "..."}`.

### 4.2 Parameter yang dikirim (dibangun HANYA oleh `scripts/common.py::build_params`)

`latitude`, `longitude` (centroid, 5 desimal) · `start_date`, `end_date` · `daily` (core **atau** reserve) · `models=era5_seamless` · `temperature_unit=celsius` · `wind_speed_unit=ms` (default API `kmh`, jadi wajib dikirim) · `precipitation_unit=mm` · `timeformat=iso8601` · `timezone=Asia/Jakarta` (default API `GMT`) · `cell_selection=land`.
**Tidak dikirim:** `elevation`, `hourly`, `apikey`, `format`.

### 4.3 Bentuk respons (terverifikasi smoke test)

- `utc_offset_seconds = 25200`, `timezone = "Asia/Jakarta"`. Catatan: `timezone_abbreviation` = `"GMT+7"` (bukan "WIB"), dan itu normal.
- `latitude`/`longitude` di respons = pusat **grid cell** (0,1°), berjarak 1,2–8,5 km dari centroid.
- Kunci di `daily` **tidak** bersuffix nama model (parser tetap toleran terhadap suffix).
- `null` = data tidak tersedia dari sumber. **Jangan diisi.**

### 4.4 Kuota API (open-meteo.com/en/terms, /en/pricing)

- Free tier: **600 call/menit, 5.000/jam, 10.000/hari**.
- Request dengan lebih dari 10 variabel atau lebih dari 14 hari dihitung **pecahan**: bobot = `max(1, n_var/10) × max(1, n_hari/14)`. Satu chunk 1 tahun bernilai ±26 call (core) atau ±29 call (reserve). Koleksi penuh menghabiskan ±8.630 call.
- `common.ApiBudget` membatasi pemakaian ke **480/menit, 4.000/jam, 8.000/hari**. Ledger persisten ada di `logs/api_ledger.csv`. Saat jatah harian habis, `full` berhenti rapi dengan exit code 3 dan status `PAUSED_BUDGET`; run berikutnya melanjutkan dari manifest.
- **Jangan** menurunkan jeda atau menaikkan batas tanpa izin pengguna.

### 4.5 Fakta sumber

- ERA5 (0,25°) dan ERA5-Land (0,1°): **update harian, jeda ±5 hari**. Hasil audit menunjukkan hari terakhir lengkap untuk semua variabel adalah **2026-09-24**.
- ERA5-Seamless menggabungkan ERA5-Land (suhu, kelembapan) dengan ERA5 (angin, radiasi).
- Data ini **reanalysis**, dan wajib disebut demikian di provenance dan laporan.
- Lisensi data: **CC BY 4.0**, atribusi "Weather data by Open-Meteo.com". Sumber reanalysis: Copernicus C3S (ERA5/ERA5-Land).

---

## 5. Struktur paket

```text
Iklim/
├── README.md · environment.yml · requirements.txt · .gitignore · .gitattributes (LFS)
├── config/
│   ├── locations.json            ← 18 lokasi + centroid (terisi)
│   ├── variables.json            ← core 9 / reserve 11 + unit dokumentasi
│   ├── request_settings.json     ← endpoint, model, unit, tz, periode, usable_end_date, rate_limit
│   └── state.json                ← DITULIS SCRIPT: hasil smoke, model_in_use
├── scripts/
│   ├── common.py                 ← build_params, parser, sha256, write_new (anti-timpa), ApiBudget
│   ├── verify_setup.py           ← Langkah 1
│   ├── fetch_boundaries.py       ← Langkah 2a (GADM 4.1)
│   ├── compute_centroids.py      ← Langkah 2b
│   ├── collect_openmeteo.py      ← Langkah 3–4 (smoke) & 5 (full)
│   ├── normalize_openmeteo.py    ← Langkah 6
│   └── audit_openmeteo.py        ← Langkah 7
├── tests/test_offline.py         ← 14 test tanpa internet
├── docs/PHASE1_COLLECTION_OPENMETEO.md   ← provenance + status + log keputusan (Langkah 8)
├── data/
│   ├── raw/openmeteo/{core,reserve}/<lokasi>/<tahun>.json   ← 324 file evidence
│   ├── raw/openmeteo/smoke/<set>_<model>_<lokasi>.json
│   ├── raw/openmeteo/collection_manifest.csv · collection_summary.json
│   ├── processed/openmeteo/climate_{core,reserve}_long.csv  ← Git LFS
│   └── external/boundaries/      ← GADM (TIDAK di-commit; lisensi)
├── logs/                         ← log per run + api_ledger.csv (tidak di-commit)
└── reports/                      ← semua laporan cek/audit
```

Pengambilan ulang tidak pernah menimpa file: versi baru disimpan sebagai `<tahun>.rN.json`, dan manifest menunjuk ke entri sukses terbaru.

---

## 6. Lingkungan eksekusi

- OS: **Windows**. Env Conda: **`arif-net`** (Python 3.13.15, requests, pandas 3.x, numpy, geopandas, shapely, pyproj, pyogrio).
- Selalu gunakan `conda run` dari root folder `Iklim`:
  ```cmd
  conda run -n arif-net python scripts\verify_setup.py
  ```
  Tambahkan `--no-capture-output` untuk melihat log secara langsung. `conda run ... python -c` **tidak** menerima argumen multi-baris; tulis script ke file bila perlu.
- **Lokasi repo:** letakkan repo **di luar folder sinkron cloud** (OneDrive/Google Drive), karena raw HTML News ±11–12 GB. Atau isi `News/config/sources.json` → `raw_store` dengan path absolut di luar folder sinkron.
- **Batas path Windows:** nama file sengaja dibuat pendek; path terpanjang pipeline News = 215 karakter, dan `verify_setup.py` mengeceknya. `LongPathsEnabled=1` di sistem ini.
- Proses background agen dibatasi **2 jam**. Full collection yang terhenti cukup dijalankan ulang (resume).

---

## 7. Prosedur kerja per langkah (status per 3 Okt 2026)

Setiap ⛔ **CHECKPOINT** berarti berhenti, meringkas hasil untuk pengguna, dan menunggu konfirmasi.

| # | Langkah | Perintah (`conda run -n arif-net python …`) | Status |
|---|---|---|---|
| A | Test offline | `-m unittest discover -s tests -v` | PASS 14/14 |
| 1 | Setup | `scripts\verify_setup.py` | PASS (FAIL=0, WARN=0) |
| 2a | Batas GADM | `scripts\fetch_boundaries.py` | PASS (sha256 json `a30b7026…`) |
| 2b | Centroid | `scripts\compute_centroids.py --dry-run` → tanpa `--dry-run` | PASS 18/18, 1 WARN Cirebon (diputuskan) |
| 3 | Smoke core | `scripts\collect_openmeteo.py smoke --set core` | PASS `era5_seamless` |
| 4 | Smoke reserve | `scripts\collect_openmeteo.py smoke --set reserve` | PASS `era5_seamless` |
| 5 | Full | `scripts\collect_openmeteo.py full` | PASS 324/324, 0 error, 0 HTTP 429 |
| 6 | Normalisasi | `scripts\normalize_openmeteo.py` | PASS (core 517.590 baris, reserve 632.610 baris) |
| 7 | Audit | `scripts\audit_openmeteo.py` | PASS, 1 WARN tepi periode (diputuskan opsi A) |
| 8 | Dokumentasi | isi `docs/PHASE1_COLLECTION_OPENMETEO.md` dari artefak | berjalan |

### 7.1 Aturan per langkah (berlaku bila diulang atau diperpanjang)

- **Langkah 2b:** `[WARN] centroid di luar poligon` → **jangan** mengganti ke representative point; laporkan sebagai decision gate. Kecocokan ≠ 1 → laporkan kandidat dan jangan memilih fitur manual.
- **Langkah 3:** variabel kosong atau seluruhnya null → fallback P1-DG-10 `smoke --set core --model era5` (dicatat otomatis di `state.json`). HTTP 400 → lihat §7.3.
- **Langkah 4:** wajib memakai model yang sama dengan core (script menolak bila berbeda). Variabel reserve tidak tersedia → **berhenti dan laporkan**.
- **Langkah 5:** hanya setelah persetujuan pengguna. Script menolak berjalan bila koordinat kosong, smoke belum PASS, atau model antar-set berbeda. Error atau putus → jalankan ulang perintah yang sama. `--refetch` (wajib dengan `--location`) hanya atas izin pengguna.
- **Langkah 6:** sha256 tidak cocok berarti raw berubah → **berhenti**. Jangan "memperbaiki" raw.
- **Langkah 7:** null di ekor periode wajar. Grid collision adalah keterbatasan dan **tidak** diperbaiki dengan menggeser titik.

### 7.2 Memperpanjang periode (mis. setelah koleksi harga ulang)

Mengubah `end_date` = **decision gate** (P1-DG-16). Setelah disetujui: perbarui `LOCKED_SETTINGS` di `verify_setup.py` dan `end_date`, jalankan `full` (chunk lama tetap; tahun terakhir perlu `--refetch` per lokasi atas izin), lalu Langkah 6–7, dan evaluasi ulang `usable_end_date`.

### 7.3 Menangani HTTP 400 (nama parameter salah)

1. Baca `reason` di laporan smoke.
2. Bandingkan dengan daftar *Daily Weather Variables* di https://open-meteo.com/en/docs/historical-weather-api.
3. Bila nama resmi berbeda **untuk variabel yang sama** → ubah `api_param` di `config/variables.json` **dan** di `LOCKED_CORE`/`LOCKED_RESERVE` (`verify_setup.py`), catat di `docs/…` §4, ulangi smoke, lalu laporkan.
4. Bila variabel **tidak ada** → **berhenti** dan laporkan sebagai decision gate. Jangan mengganti dengan variabel lain.

---

## 8. Aturan integritas data (non-negotiable)

1. Raw JSON adalah evidence: tidak diedit, tidak diimputasi, tidak ditimpa (`common.write_new`).
2. Tidak ada imputasi, agregasi, lag, rolling, anomaly, scaling, atau pemotongan periode di collection layer.
3. Tanggal disimpan apa adanya (WIB). Aturan t−5 dan `usable_end_date` diterapkan di Phase 3.
4. Core dan reserve memakai request dan folder terpisah; reserve tidak dipakai modelling.
5. Satu model untuk seluruh seri (`era5_seamless`).
6. Lokasi adalah *candidate supplier region*, bukan bobot market share.
7. Reanalysis ≠ observasi stasiun. Gunakan istilah yang benar.
8. File GADM tidak di-commit (lisensi); sumber dan sha256 tercatat di `reports/boundaries_check.json`.
9. Setiap angka yang dilaporkan harus berasal dari artefak atau laporan nyata.

---

## 9. Hal yang sering salah (hindari)

| Salah | Benar |
|---|---|
| Menghilangkan `timezone` | Wajib saat memakai `daily`; nilainya `Asia/Jakarta` |
| Memakai default `wind_speed_unit` (km/h) | Kirim `ms` |
| `timeformat=unixtime` | `iso8601` |
| `models=best_match` atau tanpa `models` | `era5_seamless` |
| Satu request gabungan core+reserve | Dua request terpisah |
| Jeda tetap 1 detik tanpa memperhitungkan bobot | `ApiBudget` berbobot (chunk 1 tahun ≈ 26–29 call) |
| Mengisi null hari terakhir / memakai `precipitation_hours` 25–30 Sep 2026 | Biarkan; potong di 2026-09-24 pada Phase 3 |
| Menerapkan t−5 saat koleksi | Hanya di Phase 3 |
| Menambah variabel hourly atau lainnya "karena berguna" | Hanya 9 core + 11 reserve |
| Mengganti centroid yang jatuh di luar poligon | Laporkan sebagai decision gate |
| Memakai env `arifnet-climate` | Env **`arif-net`** |
| `random k-fold` / evaluasi model | Bukan tugas agen ini |

---

## 10. Format laporan ke pengguna (setiap checkpoint)

```text
LANGKAH <n> — <nama> : PASS / FAIL / PERLU KEPUTUSAN
Perintah dijalankan : ...
Ringkasan hasil     : (angka dari laporan, bukan perkiraan)
Temuan / WARN       : ...
Perubahan file      : (daftar file yang diubah agen + alasan)
Keputusan dibutuhkan: (jika ada — sebut opsi, jangan memilih sendiri)
Langkah berikutnya  : ...
```
Bahasa laporan: **Bahasa Indonesia**.

---

## 11. Di luar scope dokumen ini

- Halaman PIBC lain (Stok Beras, Beras Masuk, Beras Keluar) belum dikoleksi; mengoleksinya butuh keputusan pengguna.
- Pengisian null target dari PIBC/IPJ (P1-DG-06), kalibrasi, dan penggabungan sumber.
- Skor sentimen, agregasi harian, dan fitur news (Phase 3; lihat §17).
- Feature engineering, alignment ke kalender harga, split train/val/test, modelling, evaluasi.
- Perubahan dokumen otoritas (Plan/Contract), yang hanya dilakukan pengguna melalui decision gate.

---

## 12. Referensi

- Open-Meteo Historical Weather API — https://open-meteo.com/en/docs/historical-weather-api · Terms — https://open-meteo.com/en/terms · Licence — https://open-meteo.com/en/licence
- Zippenfenig, P. (2023). *Open-Meteo.com Weather API* [Computer software]. Zenodo. https://doi.org/10.5281/ZENODO.7970649
- Hersbach, H., et al. (2023). *ERA5 hourly data on single levels from 1940 to present* [Data set]. ECMWF. https://doi.org/10.24381/cds.adbb2d47
- Muñoz Sabater, J. (2019). *ERA5-Land hourly data from 2001 to present* [Data set]. ECMWF. https://doi.org/10.24381/CDS.E2161BAC
- GADM 4.1 — https://gadm.org
- Proyek: `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v2.0.0.md`, `ARIF-Net_Phase_0_Research_Contract_v2.1.0.md`, `Iklim/README.md`, `Iklim/docs/PHASE1_COLLECTION_OPENMETEO.md`

---

## 13. Harga target — PIHPS Bank Indonesia (`Historical_Komoditas\PIHPS\`)

**Otoritas:** P1-DG-01…06, 13, 16 (Plan §0.5, §10.1a; Contract §3.1, §5.1, §5.6). **Status (3 Okt 2026): Langkah A–5 PASS.**

| Elemen | Nilai |
|---|---|
| Endpoint | `GET https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas`, didahului warm-up `GET /hargapangan/TabelHarga/PasarTradisionalKomoditas` (cookie sesi; tanpa token hard-coded) |
| Parameter tetap | `price_type_id=1`, `province_id=13`, `regency_id=34`, `showKota=true`, `showPasar=true`, `tipe_laporan=1`, `start_date`/`end_date` (keduanya inklusif) |
| Market | **Pasar Kramatjati, level 3, harga ECERAN**. Label regency "Kota Jakarta Pusat" = *source quirk* (P1-DG-03) |
| Komoditas | `com_14` Cabai Merah Keriting · `com_11` Bawang Merah Ukuran Sedang · `com_3` Beras Kualitas Medium I (ID **terverifikasi** di `GetRefCommodityAndCategory`). Bawang putih dikeluarkan |
| Periode | 2019-01-01 → 2026-09-30, chunk bulanan (3 × 93 = 279 request, ±8 menit, jeda 1–1,5 s) |
| Respons | `{"data":[...]}`, 6 row (L0–L3). Kunci tanggal `DD/MM/YYYY`, hanya hari kerja. Nilai `"50,000"`; `"-"` = tidak dilaporkan |
| Output | raw `data/raw/pihps/<comcat_id>/<YYYY-MM>.json` (byte-identik) · `data/processed/pihps/pihps_kramatjati_long.csv` (6.066 baris; kolom `raw_value`, `is_reported`) |
| Arsip | `archive/run_2022/` = run lama 2022–2026 (12 komoditas); **jangan dihapus**, hanya dipakai sebagai pembanding audit |

**Perintah** (dari `Historical_Komoditas\PIHPS`, `conda run -n arif-net python …`): `scripts\verify_setup.py` → `scripts\collect_pihps.py smoke` → ⛔ → `scripts\collect_pihps.py full` (resume) → `scripts\normalize_pihps.py` → `scripts\audit_pihps.py`.

**Aturan khusus PIHPS:**
- `comcat_id` **tidak boleh ditebak**. Bila reference tidak cocok, smoke FAIL → berhenti dan laporkan.
- `"-"` **tidak diisi dan tidak di-ffill**. Harga yang sama berhari-hari adalah observasi valid (P1-DG-06).
- Target `r(t,h)` dan fitur harga tidak dihitung di sini (Phase 2).

**Temuan yang dibawa ke Phase 2:**
1. Ada 69 tanggal `"-"` per komoditas, identik di ketiga komoditas (pola libur nasional).
2. Jumlah `"-"` per tahun turun dari 13–20 (2019–2022) menjadi 4/3/1/0 (2023–2026), artinya sumber mulai mengisi hari libur.
3. Beras sangat lengket: tidak berubah di 96% hari, dengan run 243 hari kerja (relevan P1-DG-08).
4. Spike–reversal beras 2022-07-12/13.
5. Overlap dengan arsip 2022: 3.711/3.711 identik.

## 14. Harga pelengkap — PIBC Pasar Induk Beras Cipinang (`Historical_Komoditas\PIBC\`)

**Otoritas:** P1-DG-01, 02, 05, 06 (Plan §0.5, §10.1a; Contract §3.1). **Peran: pelengkap dan konteks pasokan, BUKAN target.** **Status (3 Okt 2026): Langkah A–5 PASS.**

| Elemen | Nilai |
|---|---|
| Endpoint | `GET https://pibc.foodstation.co.id/rice-price-detail` (DataTables server-side), didahului warm-up `GET /rice-price`. Cookie dari tangkapan DevTools pengguna **tidak** dipakai/disimpan |
| Semantik tanggal | **`start_date` EKSKLUSIF**, `end_date` inklusif (terverifikasi probe). `build_params` mengirim `start_date = S − 1`. Parameter `order` diabaikan server |
| Periode | 2019-01-01 → **2025-06-16** = data terakhir di sumber (situs tidak diperbarui lagi). 2.359 hari kalender, harian penuh termasuk akhir pekan, tanpa celah |
| Request | 7 chunk tahunan (`length=400`), jeda 1,5 s |
| Level harga | **GROSIR** pasar induk. Halaman: "Harga Rata-Rata dalam Rupiah"; satuan /kg tidak tertulis |
| Pemetaan (P1-DG-05) | **Beras Kualitas Medium I → `muncul1` (Muncul I)**, keputusan peneliti 2026-10-03 berbasis definisi mutu (`config/varieties.json`). Raw tetap 14 varietas; processed **hanya** `muncul1` |
| Output | raw `data/raw/pibc/<YYYY>.json` · `data/processed/pibc/pibc_medium_i_long.csv` (2.359 baris) · `reports/mapping_evidence.*` |

**Perintah** (dari `Historical_Komoditas\PIBC`): `scripts\verify_setup.py` → `scripts\collect_pibc.py smoke` → `scripts\collect_pibc.py full` → `scripts\mapping_evidence.py` → ⛔ keputusan pemetaan → `scripts\normalize_pibc.py` → `scripts\audit_pibc.py`.

**Aturan khusus PIBC:**
- Jangan mengubah `medium_i_mapping` tanpa keputusan pengguna. `normalize_pibc.py` menolak berjalan bila mapping kosong.
- Bukti pemetaan hanya dihitung pada 2019–2020 (anti-leakage). Jangan memperluas jendelanya tanpa izin.
- **Tidak ada pengisian null PIHPS di paket ini.** Pengisian dilakukan di tahap P1-DG-06: `value_source` + `is_filled`, validasi overlap, kalibrasi yang di-fit hanya pada training, dan eksperimen dilaporkan dengan dan tanpa nilai isian.

**Temuan:**
- Ke-69 null PIHPS `com_3` semuanya memiliki nilai Muncul I di tanggal yang sama.
- Muncul I tidak berubah pada 86% hari, dengan run terpanjang 88 hari.
- Lompatan terbesar +10,4% (2023-09-20).
- PIBC tidak menjangkau 2025-06-17 → 2026-09-30, tetapi PIHPS juga tidak punya null di periode itu.

## 15. Status lintas sumber (3 Okt 2026)

| Sumber | Folder | Periode | Status |
|---|---|---|---|
| Iklim Open-Meteo (ERA5-Seamless) | `Iklim\` | 2018-01-01 → 2026-09-30 (fitur s.d. 2026-09-24) | PASS |
| Harga target PIHPS (eceran, Pasar Kramatjati) | `Historical_Komoditas\PIHPS\` | 2019-01-01 → 2026-09-30 | PASS |
| Harga pelengkap PIBC (grosir, Muncul I) | `Historical_Komoditas\PIBC\` | 2019-01-01 → 2025-06-16 | PASS |
| Harga pelengkap IPJ (eceran, Pasar Kramat Jati) | `Historical_Komoditas\IPJ\` | 2024-01-01 → 2026-09-30 (sebelum 2024 tidak tersedia) | PASS |
| News (Kompas, detikFinance, CNN Indonesia, CNBC Indonesia, Kontan, Liputan6) | `News\` | 2019-01-01 → 2026-09-30 | Smoke PASS; **full: 93 fase × 1 bulan** |

**Struktur harga komoditas (3 Okt 2026):** semua collector harga berada di `Historical_Komoditas\` sebagai sub-paket per sumber (`PIHPS\`, `PIBC\`), dengan `environment.yml`, `requirements.txt`, `.gitignore`, dan `.gitattributes` (LFS) dipakai bersama di `Historical_Komoditas\`. Path di manifest relatif terhadap sub-paket. Sumber baru (IPJ) ditambahkan sebagai sub-paket dengan pola yang sama.

## 16. Harga pelengkap — IPJ Info Pangan Jakarta (`Historical_Komoditas\IPJ\`)

**Otoritas:** P1-DG-01, 02, 04–06. **Peran: pelengkap dengan prioritas pengisian tertinggi** (eceran, pasar sama dengan target) dan validasi silang PIHPS. **Status (3 Okt 2026): Langkah A–5 PASS.**

| Elemen | Nilai |
|---|---|
| Endpoint | `GET https://infopangan.jakarta.go.id/api2/v1/public/report?filterBy=market&Id=12&yearMonth=YYYY-MM`. 1 request = 1 bulan × semua komoditas pasar. Tanpa login atau header khusus; cookie dari tangkapan browser pengguna **tidak** dipakai |
| Market | `market_id` **12 = "Pasar Kramat Jati"** (`market_level: eceran`, Jakarta Timur), diverifikasi via `/api2/v1/master-data/market?search_text=kramat` saat smoke. **Jangan** memakai `market_id` 1 (Pasar Induk / PIKJ, P1-DG-02) |
| Pemetaan (keputusan peneliti) | Cabe Merah Keriting (8) → `com_14` · Bawang Merah (12) → `com_11` (IPJ tidak menyebut ukuran) · **Beras Muncul I (4) → `com_3`** (konsisten dengan P1-DG-05). "Beras Medium" (id 114) tidak dipakai |
| Periode | Diminta 2019-01 → 2026-09 (93 request). **Data hanya 2024-01-01 → 2026-09-30**; 60 bulan sebelumnya `OK_EMPTY` |
| Status chunk | `OK` = ada data · `OK_EMPTY` = respons valid tanpa data · `FAIL` = struktur, nama komoditas berubah, tanggal di luar bulan, atau **duplikat bernilai berbeda**. Duplikat bernilai **identik** diterima sebagai 1 baris (keputusan peneliti, kasus 2026-09-12) |
| Output | raw `data/raw/ipj/<YYYY-MM>.json` (+ `.r2` untuk 2026-09) · `data/processed/ipj/ipj_kramatjati_long.csv` (2.890 baris) |

**Perintah** (dari `Historical_Komoditas\IPJ`): `scripts\verify_setup.py` → `scripts\collect_ipj.py smoke` → `scripts\collect_ipj.py full` (resume, hanya mengulang FAIL) → `scripts\normalize_ipj.py` → `scripts\audit_ipj.py`.

**Temuan (jangan dikoreksi di collection layer):**
- Ada 3 nilai yang kemungkinan salah input di sumber: CMK 2024-11-29 = 300.000, CMK 2024-06-16 = 18.000, Bawang Merah 2025-01-14 = 4.000.
- IPJ vs PIHPS (pasar sama) berselisih median 5–7% dan jarang identik.
- IPJ hanya mencakup 4 dari 69 null PIHPS (null tahun 2024+).
- Ada hari yang tidak dikembalikan sumber: 35 hari untuk CMK dan Bawang Merah, 52 hari untuk Beras.

## 17. News — berita pangan, harga, inflasi, cuaca, supply, BBM (`News\`)

**Otoritas:** Plan v2.0.0 §4.1 (modality 3), §8 Group 3, §9–§9.2, **§10.4 pipeline**, §12.1/§12.2, §22, §37 · Contract v2.1.0 §2.2, §5.1, **§5.3**, §18.3, **§19 (News)**, §21, DG-04, DG-10. Plan DG-09 `LOCKED DIRECTION`.
**Status (3 Okt 2026):** probe, verifikasi, codebase (13 test), dan smoke **PASS**. Full collection = 93 fase × 1 bulan (±40–60 menit/fase). Rincian di `News/docs/PHASE1_COLLECTION_NEWS.md` (§3b–3d).

### 17.1 Aturan yang dikunci dokumen otoritas
| Aturan | Isi |
|---|---|
| Topik | Pangan, harga, inflasi, cuaca, supply, BBM/logistik (Plan §4.1) |
| Waktu | Fitur origin `t` hanya dari artikel **terbit ≤ `t`**. Artikel tanpa timestamp terbit **tidak dipakai** (Contract §2.2, §19; DG-04) |
| Pipeline | raw → source + publication timestamp → dedup → topic/relevance filter → normalisasi teks → model sentimen → skor artikel → agregasi harian → temporal cutoff (Plan §10.4) |
| Batas collection | Folder `News\` hanya sampai **artikel ter-normalisasi + dedup + relevance flag berbasis aturan**. Sentimen, agregasi harian, dan fitur adalah **Phase 3** |
| Fitur (Phase 3) | Bukan hanya `sentiment_mean`: volume, pos/neg balance, intensity, persistence, recency, topic relevance, source count, event burst, negative ratio (Contract §5.3, §18.3) |
| Provenance model | Model sentimen yang benar-benar dipakai, termasuk fallback lexicon, **wajib dicatat**. Jangan menulis "IndoBERT" bila yang berjalan fallback (Plan §10.4, §37) |
| Larangan | Dummy news notebook lama tidak boleh dipakai (Plan §22) · halaman search yang di-Disallow `robots.txt` tidak dipakai · cookie/token pengguna tidak dipakai · **teks penuh artikel tidak di-commit** (hak cipta) |

### 17.2 Hasil probe (bukti di `News/data/raw/news/probe/`, laporan `News/reports/probe_*.json`)
- **GDELT DOC API:** HTTP 429 konsisten dari jaringan ini (7 request, termasuk retry setelah 90 detik). File mentah GKG tersedia sejak 2015-02-18, tetapi ±1 TB untuk 2019–2026. Jalur realistis: **BigQuery** (butuh akun GCP). Tone GDELT ≠ IndoBERT.
- **Indeks arsip per tanggal 2019 terbukti:** Kompas (`indeks.kompas.com/?site=all&date=`), Detik (`news.detik.com/indeks?date=`), CNN Indonesia & CNBC Indonesia (`/indeks?date=YYYY/MM/DD`), Kontan (`/search/indeks?tanggal=&bulan=&tahun=`).
- **Belum terverifikasi:** Antara (butuh DevTools). **Ditolak (403):** Bisnis.com, Tempo. **Katadata:** sitemap baru mulai 2021-01.
- Kompas, Liputan6, dan Republika men-Disallow `/search` → wajib lewat indeks.

### 17.3 Keputusan (DECIDED 2026-10-03)
| ID | Keputusan |
|---|---|
| P1-DG-25 | Sumber = **Kompas, Detik, CNN Indonesia, CNBC Indonesia, Kontan, Liputan6**. Jangan menambah sumber lain tanpa decision gate baru |
| P1-DG-26 | Periode **2019-01-01 → 2026-09-30** |
| P1-DG-27 | Topik/kata kunci = `News/config/news_scope_DRAFT.json` → `topics` |
| P1-DG-28 | Semua kanal (indeks umum) + filter kata kunci pada judul |
| P1-DG-29 | **Tanpa teks penuh**: hanya judul + waktu terbit + metadata |
| P1-DG-30 | Relevansi = kata kunci (case-insensitive) pada judul |

| P1-DG-28 (revisi CP2) | **Detik = detikFinance saja** (detikNews dikeluarkan: pagination tidak stabil dari script) · **Kompas = `site=news` + `site=money`** (revisi 2026-10-04; 91% artikel relevan Kompas ada di kanal ini) |
| P1-DG-31 | Kolom **`wilayah_pemasok`** = kabupaten dari 18 wilayah pemasok (P1-DG-11) yang disebut di judul |
| Eksekusi | **Revisi: 93 fase × 1 bulan** (±40–60 menit): `python scripts\run_phase.py --month YYYY-MM --max-minutes 60` (resume otomatis), dijalankan per giliran. Kata kunci yang terlalu luas **diperketat di Phase 3**. Raw ±11–12 GB disimpan lokal di dalam repo (default) atau di `raw_store`, **di luar folder sinkron cloud**; raw dan data News tidak di-commit |

**Kuirk per media (wajib diikuti collector; detail di docs §3b–3c):** Detik (detikFinance), tanggal di-URL-encode (`%2F`) dengan urutan `?date=…&page=N` · CNN, `/indeks/2?date=…&page=N` (`/indeks/1` = 404) · Kompas, meta waktu dalam **UTC** → konversi ke WIB (jam juga ada di URL) · CNN/CNBC, angka di URL **bukan** waktu terbit → pakai JSON-LD `datePublished` · Kontan, halaman artikel **403** → judul + waktu dari indeks saja · Detik, CNN Indonesia, dan CNBC Indonesia satu grup media (keterbatasan keragaman).

### 17.4 Sebelum membangun collector, agen WAJIB punya
1. ✅ P1-DG-25…30 sudah DECIDED (17.3).
2. ✅ Pola URL keenam media terverifikasi (docs §3b).
3. Catatan ToS/izin setiap media (diisi pengguna).
4. ✅ `beautifulsoup4` & `lxml` terpasang.
5. **Rencana collector disetujui pengguna** sebelum eksekusi.

### 17.4b Progres eksekusi (otomatis)
<!-- NEWS_PROGRESS:START -->
**Progres scraping News — belum ada koleksi di mesin ini.**

| Item | Nilai |
|---|---|
| Fase selesai | **0/93** |
| Fase berikutnya | 2019-01 |

Blok ini diisi otomatis oleh `News/scripts/update_progress.py` setelah fase pertama selesai (sumber kebenaran: `News/data/raw/news/manifest_index_days.csv` lokal). Data News **tidak** ada di repo: setiap mesin mengoleksi sendiri dari 2019-01.
<!-- NEWS_PROGRESS:END -->

### 17.4c Protokol eksekusi 93 fase (aturan pengguna, 2026-10-03) — WAJIB
1. **Jangan menjalankan kode scraping sebelum pengguna mengonfirmasi** di sesi berjalan.
2. Setelah dikonfirmasi, jalankan fase **berurutan terus-menerus** (`News/scripts/run_phase.py --month YYYY-MM --max-minutes 60`), mulai dari "Fase berikutnya" di blok progres. Satu fase sekitar 40–60 menit, dijalankan sebagai proses latar belakang.
3. **Bila pengguna menginterupsi:** segera hentikan proses scraping (hentikan proses `python … run_phase.py/collect_index.py/collect_articles.py`). Lalu jalankan `News/scripts/update_progress.py --note "dihentikan atas interupsi pengguna"` dan **laporkan sudah sampai fase/bulan/media mana**. Menghentikan proses aman: collector melanjutkan dari hari terakhir (resume).
4. **Setelah setiap fase** (dan saat berhenti), blok progres di bawah diperbarui otomatis oleh `update_progress.py`. Agen melaporkan ringkasan fase (OK/FLAG/FAIL per media) kepada pengguna.
5. Hari berstatus FAIL tidak boleh dilewati diam-diam: laporkan, lalu ulangi fase yang sama (resume hanya mengambil yang belum OK).
6. Normalisasi dan audit penuh dijalankan di fase **Desember** setiap tahun dan di fase terakhir (2026-09).

### 17.5 Hal yang sering salah (hindari)
| Salah | Benar |
|---|---|
| Memakai `config/news_scope_DRAFT.json` sebelum diputuskan | Tunggu status DECIDED |
| Mengagregasi berita per hari di collection layer | Phase 3 |
| Memakai tanggal crawl sebagai tanggal berita | Pakai `published_at` dari artikel. Tanpa timestamp → keluarkan |
| Menyimpulkan sentimen dari tone GDELT sebagai "IndoBERT" | Catat model aktual |
| Crawling halaman search yang dilarang robots.txt | Pakai indeks per tanggal, jeda sopan |
| Commit teks penuh artikel | Simpan lokal (`data/raw/news/fulltext/` di-ignore) |
