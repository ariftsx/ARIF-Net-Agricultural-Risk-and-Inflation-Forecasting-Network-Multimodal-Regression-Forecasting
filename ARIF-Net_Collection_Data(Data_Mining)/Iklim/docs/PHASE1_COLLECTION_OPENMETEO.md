# Phase 1 — Koleksi Iklim Open-Meteo: Provenance & Status

**Otoritas:** Plan v2.0.0 (§0.5 P1-DG-09…17, §9 Data Contract, §10.2a) → Contract v2.1.0 (§0B, §4.5–4.6, §5.6, §6.4).
**Status dokumen:** diisi bertahap. Hanya fakta dari artefak di `reports/` dan `data/raw/openmeteo/` yang boleh dicantumkan. Bagian bertanda `[MENUNGGU …]` belum dijalankan.

---

## 1. Metadata dataset (Plan §9)

| Field | Nilai |
|---|---|
| Dataset name | ARIF-Net climate daily — Open-Meteo reanalysis (core / reserve) |
| Source organization / URL | Open-Meteo, Historical Weather API — https://open-meteo.com/en/docs/historical-weather-api · endpoint `https://archive-api.open-meteo.com/v1/archive` |
| Underlying data | ERA5 / ERA5-Land (ECMWF, Copernicus Climate Change Service) via model `era5_seamless` (fallback `era5`, P1-DG-10) |
| Sifat data | **Reanalysis** (gabungan model + asimilasi observasi), **bukan** observasi stasiun |
| Collection method | HTTP GET query-string, 1 request per (set, lokasi, tahun); raw response disimpan byte-identik + sha256 (`collection_manifest.csv`) |
| Coverage date | 2018-01-01 → 2026-09-30 (P1-DG-16) |
| Frequency | Harian (`daily`), tanpa variabel hourly |
| Timezone | Asia/Jakarta (WIB, `utc_offset_seconds = 25200`); batas hari 00:00 waktu lokal |
| Publication/availability time | ERA5/ERA5-Land diperbarui harian dengan jeda ±5 hari → fitur memakai data ≤ t−5 (P1-DG-17, diterapkan di Phase 3) |
| Raw file hash/version | sha256 per file di `data/raw/openmeteo/collection_manifest.csv` |
| License/usage condition | Data API: CC BY 4.0 ("Weather data by Open-Meteo.com"); free tier non-komersial (600/menit, 5.000/jam, 10.000/hari). Batas admin: GADM 4.1, akademik/non-komersial, tanpa redistribusi |
| Missing-value policy | Null dari sumber dibiarkan null; dilaporkan di audit (ekor vs tengah periode) |
| Imputation policy | Tidak ada imputasi di collection layer (Contract §5.6). Imputasi apa pun di Phase 3 harus split-aware (Contract §6.4) |
| Transformation | Hanya reshape raw JSON → CSV long (tanpa pembulatan, agregasi, atau konversi unit) |
| Feature list | Core 9: precipitation_sum, precipitation_hours, temperature_2m_mean/max/min, relative_humidity_2m_mean, sunshine_duration, et0_fao_evapotranspiration, soil_moisture_7_to_28cm_mean. Reserve 11: lihat `config/variables.json` (tidak dipakai modelling) |
| Temporal cutoff rule | Origin `t` hanya memakai data bertanggal ≤ t−5 (P1-DG-17) |
| Leakage audit status | `[MENUNGGU Phase 1 leakage audit]` |

## 2. Lokasi (P1-DG-11/12) — status CANDIDATE

Ada 18 kabupaten sesuai Contract §4.6, dengan tier dicatat per komoditas di `config/locations.json`. Titiknya adalah centroid poligon GADM 4.1 level 2, dihitung di EPSG:6933.

| location_id | GADM (NAME_2, TYPE_2, GID_2) | lat | lon | luas km² | centroid di dalam poligon |
|---|---|---|---|---|---|
| garut | Garut, Kabupaten, IDN.9.11_1 | -7.35951 | 107.78883 | 3089.4 | ya |
| cianjur | Cianjur, Kabupaten, IDN.9.7_1 | -7.13358 | 107.15776 | 3591.5 | ya |
| bandung_barat | BandungBarat, Kabupaten, IDN.9.1_1 | -6.89711 | 107.41495 | 1276.9 | ya |
| bandung | Bandung, Kabupaten, IDN.9.2_1 | -7.09994 | 107.61075 | 1755.4 | ya |
| sumedang | Sumedang, Kabupaten, IDN.9.25_1 | -6.82506 | 107.98087 | 1557.5 | ya |
| magelang | Magelang, Kabupaten, IDN.10.20_1 | -7.50157 | 110.24663 | 1131.0 | ya |
| brebes | Brebes, Kabupaten, IDN.10.6_1 | -7.05928 | 108.92756 | 1751.5 | ya |
| cirebon | Cirebon, Kabupaten, IDN.9.9_1 | -6.74541 | 108.55129 | 1067.9 | **tidak** |
| indramayu | Indramayu, Kabupaten, IDN.9.12_1 | -6.44857 | 108.16875 | 2088.1 | ya |
| karawang | Karawang, Kabupaten, IDN.9.13_1 | -6.25204 | 107.35394 | 1910.9 | ya |
| subang | Subang, Kabupaten, IDN.9.23_1 | -6.48414 | 107.73220 | 2162.1 | ya |
| demak | Demak, Kabupaten, IDN.10.8_1 | -6.91109 | 110.63202 | 999.7 | ya |
| temanggung | Temanggung, Kabupaten, IDN.10.33_1 | -7.25788 | 110.13565 | 873.1 | ya |
| nganjuk | Nganjuk, Kabupaten, IDN.11.24_1 | -7.59737 | 111.93840 | 1290.4 | ya |
| bima | Bima, Kabupaten, IDN.20.1_1 | -8.47469 | 118.61870 | 4211.0 | ya |
| sragen | Sragen, Kabupaten, IDN.10.29_1 | -7.38720 | 110.97751 | 977.9 | ya |
| cilacap | Cilacap, Kabupaten, IDN.10.7_1 | -7.49089 | 108.89037 | 2345.5 | ya |
| sukoharjo | Sukoharjo, Kabupaten, IDN.10.30_1 | -7.68080 | 110.83464 | 493.5 | ya |

Sumber batas: GADM 4.1 IDN level 2 (502 fitur). Zip sha256 `309c629141e05244cafd3d5a71597645a19ef2ed95da7b17bb3d8af469feff49`, json sha256 `a30b7026ad37fd02f67bad8bc454653e0ac31ad8a0ba855ed317e27e5c35fb75`, diunduh 2026-10-02T16:01:30Z (`reports/boundaries_check.json`). Centroid ditulis ke `config/locations.json` pada 2026-10-02T16:03:49Z (`reports/centroids_check.json`).

**Cirebon:** Wilayah Kabupaten Cirebon melingkari Kota Cirebon, sehingga centroid geometrisnya jatuh di dalam Kota Cirebon (GADM IDN.9.17_1), sekitar 1,7 km dari batas kabupaten. Representative point pembanding: (-6.76145, 108.45635). **Keputusan peneliti (2026-10-02, CP2): centroid tetap dipakai sesuai P1-DG-12** dan dicatat sebagai keterbatasan. Selisih 1,7 km jauh lebih kecil dari resolusi grid ERA5-Land (±11 km) maupun ERA5 (±25 km).

**Keterbatasan (wajib di Limitations):** centroid administratif bisa jatuh di luar lahan sentra produksi. Selain itu, resolusi grid ERA5 (±25 km) dan ERA5-Land (±11 km) bisa menyebabkan dua kabupaten memakai grid cell yang sama; hal ini dilaporkan sebagai grid collision di audit.

## 3. Status langkah

| Langkah | Script | Status | Artefak |
|---|---|---|---|
| A — Codebase + test offline | `tests/test_offline.py` | PASS (14/14 test, 2026-10-02) | output unittest |
| 1 — Setup | `verify_setup.py` | PASS (FAIL=0; 2026-10-02) | `reports/setup_check.json` |
| 2 — Batas + centroid | `fetch_boundaries.py`, `compute_centroids.py` | PASS 18/18; 1 WARN (Cirebon — diputuskan tetap centroid) | `reports/boundaries_check.json`, `reports/centroids_*` |
| 3 — Smoke core | `collect_openmeteo.py smoke --set core` | PASS — `era5_seamless`, tanpa fallback (2026-10-02T16:07:59Z); 9/9 variabel, 0 null; raw sha256 `09c758410ef2c8aa…` | `reports/smoke_core.json` |
| 4 — Smoke reserve | `collect_openmeteo.py smoke --set reserve` | PASS — `era5_seamless` (sama dengan core), 2026-10-02T16:09:31Z; 11/11 variabel, 0 null; raw sha256 `40c740b35286f9d3…` | `reports/smoke_reserve.json` |
| 5 — Full collection | `collect_openmeteo.py full` | PASS — 324/324 chunk (core 162, reserve 162), 0 error, 0 HTTP 429; dua run (2026-10-02T16:13Z, run 1 berhenti di 299/324 karena kuota → resume 18:49Z); selesai 2026-10-02T18:50:47Z; bobot API 24 jam 8.657 | `collection_manifest.csv`, `collection_summary.json` |
| 6 — Normalisasi | `normalize_openmeteo.py` | PASS — sha256 324/324 cocok; core 517.590 baris (684 null), reserve 632.610 baris (954 null); 0 duplikat | `reports/normalize_check.json` |
| 7 — Audit | `audit_openmeteo.py` | PASS — 0 tanggal hilang; 0 pelanggaran range fisik; 0 grid collision; QC rain_sum = precipitation_sum (selisih maks 0,0 mm); 1 WARN (null tepi periode, lihat §3a) | `reports/audit_*` |

## 3a. Temuan audit — tepi akhir periode (jeda rilis ERA5)

- **Hari terakhir dengan 9 variabel core lengkap di semua lokasi: 2026-09-24.** Pada 2026-09-25 sampai 09-30, ketersediaan bervariasi per variabel:
  - null 6 hari terakhir: precipitation_sum, rain_sum, et0, sunshine_duration, shortwave_radiation_sum, cloud_cover_mean, wind_speed_10m_mean;
  - null 4 hari terakhir: suhu, RH, soil moisture/temperature, VPD, wind_speed_10m_max.
  Pola ini sama di semua lokasi dan sesuai jeda rilis ERA5/ERA5-Land ±5 hari.
- **wind_speed_10m_max:** null pada 2026-09-25 tetapi terisi pada 09-26, di 18/18 lokasi. Audit menghitungnya sebagai 18 "null tengah periode", padahal letaknya di tepi rilis, bukan gap historis. Di luar tepi akhir, **tidak ada null sama sekali** pada 2018-01-01 → 2026-09-24.
- **precipitation_hours (core):** pada 2026-09-25 sampai 09-30 variabel ini **tetap berisi angka** (90 dari 108 baris bernilai 0), padahal precipitation_sum pada hari yang sama null. Kemungkinan besar ini nilai turunan dari jam tanpa data (artefak sumber), bukan observasi "tidak hujan". Raw **tidak diubah**. Perlakuannya diputuskan peneliti untuk Phase 3, misalnya menganggap precipitation_hours tidak tersedia bila precipitation_sum null, atau memotong seri iklim di 2026-09-24.
- **Keputusan peneliti (2026-10-03, CP6) — opsi A:** seri iklim yang dipakai untuk fitur **dipotong di 2026-09-24** (`config/request_settings.json` → `usable_end_date`). Pemotongan dilakukan di feature layer (Phase 3); raw JSON dan CSV processed tetap utuh s.d. 2026-09-30 sebagai evidence.
- Dampaknya terhadap modelling kecil: aturan P1-DG-17 (≤ t−5) dan periode harga membuat tepi akhir jarang terpakai. Meski begitu, temuan ini wajib dicatat di leakage/missingness audit.

## 3b. Grid ERA5-Seamless yang dipakai

Tidak ada grid collision: 18 lokasi berada di 18 grid cell berbeda (resolusi 0,1°). Jarak centroid ke pusat grid adalah 1,19–8,50 km (maks: Temanggung). Elevasi grid berkisar 5 m (Demak) sampai 1.252 m (Garut). Detail ada di `reports/audit_grid.csv`.

## 4. Log perubahan parameter / keputusan teknis

| Tanggal | Perubahan | Alasan | Referensi |
|---|---|---|---|
| 2026-10-02 | Paket dibangun ulang dari dokumen otoritas; env `arif-net` | Paket v1 dihapus peneliti | Plan §10.2a; Contract §5.6 |
| 2026-10-02 | Nama 20 api_param dicocokkan dengan daftar resmi daily variables | Verifikasi dokumentasi sebelum smoke | open-meteo.com/en/docs/historical-weather-api |
| 2026-10-02 | Centroid Cirebon jatuh di dalam Kota Cirebon → tetap memakai centroid | Keputusan peneliti di CP2; konsisten dengan P1-DG-12 | `reports/centroids_report.csv` |
| 2026-10-02 | Rate limiter berbobot (480/m, 4.000/j, 8.000/h) | Aturan hitung call pecahan Open-Meteo; jeda tetap 1 s akan melanggar 600/menit | open-meteo.com/en/pricing, /en/terms |
| 2026-10-02 | `rate_limit.per_day` dinaikkan sementara 8.000 → 9.000 untuk 25 chunk terakhir, lalu dikembalikan ke 8.000 | Atas persetujuan peneliti; total 8.657 call tetap < batas resmi 10.000/hari | `logs/api_ledger.csv` |
| 2026-10-03 | Opsi A: `usable_end_date` = 2026-09-24 (pemotongan di Phase 3) | Keputusan peneliti di CP6; tepi rilis ERA5 berisi null & precipitation_hours artefak | §3a |
| 2026-10-03 | CSV processed dilacak Git LFS (`.gitattributes`: `data/processed/**/*.csv`) | Ukuran 70,8 MB & 91,5 MB (batas GitHub 100 MB/file) | Keputusan peneliti |
| 2026-10-03 | Env lama `arifnet-climate` dihapus; seluruh pipeline memakai env `arif-net` | Keputusan peneliti | README |
| 2026-10-02 | Run full ke-1 dihentikan batas waktu 2 jam proses background agen, saat menunggu kuota (bukan di tengah request) | Tidak ada data rusak; resume via manifest | `logs/collect_full_20261002T161311Z.log` |

## 5. Referensi

- Open-Meteo Historical Weather API — https://open-meteo.com/en/docs/historical-weather-api
- Zippenfenig, P. (2023). *Open-Meteo.com Weather API* [Computer software]. Zenodo. https://doi.org/10.5281/ZENODO.7970649
- Hersbach, H., et al. (2023). *ERA5 hourly data on single levels from 1940 to present*. ECMWF. https://doi.org/10.24381/cds.adbb2d47
- Muñoz Sabater, J. (2019). *ERA5-Land hourly data from 2001 to present*. ECMWF. https://doi.org/10.24381/CDS.E2161BAC
- GADM 4.1 — https://gadm.org
