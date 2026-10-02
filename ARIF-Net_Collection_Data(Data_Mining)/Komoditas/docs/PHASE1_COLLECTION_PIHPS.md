# ARIF-Net — Phase 1 Data Collection: PIHPS Price Dataset

**Document type:** Phase 1 execution documentation  
**Scope:** price-data collection only  
**Source:** PIHPS Bank Indonesia  
**Target market:** Pasar Kramatjati, DKI Jakarta  
**Period:** 2022-01-01 through 2026-09-29  
**Environment:** Conda + Python 3.13

---

## 1. Purpose

Dokumen ini mendefinisikan prosedur operasional pengumpulan data harga PIHPS untuk ARIF-Net sebelum data masuk ke preprocessing/Phase 2.

Phase 0 menetapkan bahwa Phase 1 dimulai dari Data/Temporal Audit dan membutuhkan provenance, temporal availability, leakage audit, target construction, baseline-ready dataset, train/validation/test repair, serta reproducibility. Untuk tiga komoditas prioritas, target market penelitian adalah PIKJ untuk CMK dan bawang merah; data Phase 1 ini juga mencakup komoditas PIHPS lain sebagai perluasan dataset harga yang tetap harus melalui audit taxonomy dan market definition.  

**Catatan scope:** collector ini mengambil seluruh 12 komoditas yang diminta peneliti dari titik `Pasar Kramatjati`. Penggunaan setiap seri pada model final tetap tunduk pada audit scope dan Data Contract.

---

## 2. Source evidence used for the collector

Hasil DevTools PIHPS yang diverifikasi peneliti menunjukkan endpoint:

`GET https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas`

Parameter penting:

- `price_type_id=1`
- `province_id=13`
- `regency_id=34`
- `showKota=true`
- `showPasar=true`
- `tipe_laporan=1`
- `start_date=YYYY-MM-DD`
- `end_date=YYYY-MM-DD`

Dari response yang dicapture, `Pasar Kramatjati` muncul dengan `level=3`. Response juga mengembalikan beberapa tanggal sekaligus, sehingga collector menggunakan date-range request dan tidak melakukan scraping DOM satu tanggal demi satu tanggal.

ID komoditas yang sudah diverifikasi dari capture peneliti:

| Commodity | `comcat_id` |
|---|---|
| Cabai Merah Keriting | `com_14` |
| Bawang Merah Ukuran Sedang | `com_11` |

ID 10 komoditas lain tidak ditebak. Collector akan mencoba discovery dari reference endpoint PIHPS. Bila discovery gagal, mapping manual harus diisi dari DevTools/response referensi.

---

## 3. Commodity scope

1. Beras Kualitas Bawah I
2. Beras Kualitas Bawah II
3. Beras Kualitas Medium I
4. Beras Kualitas Medium II
5. Beras Kualitas Super I
6. Beras Kualitas Super II
7. Bawang Merah Ukuran Sedang
8. Bawang Putih Ukuran Sedang
9. Cabai Merah Besar
10. Cabai Merah Keriting
11. Cabai Rawit Hijau
12. Cabai Rawit Merah

---

## 4. Collection method

Method final:

```text
PIHPS web page
    ↓
backend JSON endpoint
    ↓
monthly date-range requests
    ↓
raw JSON preservation
    ↓
filter level=3 + Pasar Kramatjati
    ↓
wide → long normalization
    ↓
CSV + manifest + coverage report
```

Chunk default adalah 1 bulan. Koleksi bulanan dipakai agar retry, audit coverage, dan provenance lebih mudah dikelola.

**Tidak ada imputasi pada tahap collection.** Missing date dilaporkan, bukan diisi.

---

## 5. Folder structure

```text
ARIF-Net_PIHPS_COLLECTION_PHASE1/
│
├── environment.yml
├── requirements.txt
├── .gitignore
│
├── config/
│   └── commodity_ids.json
│
├── scripts/
│   └── collect_pihps_arifnet.py
│
├── docs/
│   └── PHASE1_COLLECTION_PIHPS.md
│
├── data/
│   ├── raw/
│   │   └── pihps/
│   │       └── raw_json/
│   │           └── <commodity>/
│   │
│   └── processed/
│       └── pihps/
│
├── logs/
└── reports/
```

Runtime output collector secara default berada di `data/raw/pihps/` relatif terhadap working directory saat script dijalankan.

---

## 6. Conda environment — recommended

### Option A: create from environment file

```cmd
conda env create -f environment.yml
conda activate arifnet-pihps
python --version
```

Expected major/minor:

```text
Python 3.13.x
```

### Option B: create manually

```cmd
conda create -n arifnet-pihps python=3.13 -y
conda activate arifnet-pihps
python -m pip install -r requirements.txt
```

`requests` adalah satu-satunya dependency runtime collector pada paket ini.

---

## 7. Preflight

Jalankan:

```cmd
python --version
python -c "import requests; print(requests.__version__)"
```

Lalu syntax check:

```cmd
python -m py_compile scripts\collect_pihps_arifnet.py
```

---

## 8. Smoke test — wajib sebelum full collection

Pertama, batasi ke Januari 2022:

```cmd
python scripts\collect_pihps_arifnet.py --start-date 2022-01-01 --end-date 2022-01-31 --chunk-months 1 --delay 0.75
```

Tujuan smoke test:

- API dapat diakses dari environment Conda;
- reference discovery berhasil;
- semua `comcat_id` ditemukan atau dilaporkan sebagai unresolved;
- row `Pasar Kramatjati` dapat ditemukan;
- parser wide → long bekerja;
- raw JSON tersimpan;
- coverage report terbentuk.

**Jangan langsung melakukan full collection sebelum smoke test PASS.**

---

## 9. Full collection

Setelah smoke test PASS:

```cmd
python scripts\collect_pihps_arifnet.py --start-date 2022-01-01 --end-date 2026-09-29 --chunk-months 1 --delay 0.75
```

Secara default setiap komoditas dikoleksi per bulan, sehingga jumlah request utama kira-kira `jumlah_komoditas × jumlah_bulan`, bukan satu request per hari.

---

## 10. Manual mapping fallback

Jika output menunjukkan sebagian `comcat_id` belum ditemukan, jangan menebak ID.

Isi:

```text
config/commodity_ids.json
```

dengan ID yang diverifikasi melalui DevTools/reference response PIHPS, kemudian jalankan:

```cmd
python scripts\collect_pihps_arifnet.py --start-date 2022-01-01 --end-date 2026-09-29 --skip-reference-discovery --commodity-map config\commodity_ids.json --delay 0.75
```

---

## 11. Output

```text
data/raw/pihps/
├── raw_json/
│   ├── <commodity-1>/
│   │   ├── 2022-01-01_2022-01-31.json
│   │   └── ...
│   └── <commodity-12>/
│
├── pihps_price_kramatjati_long.csv
├── collection_manifest.csv
├── coverage_report.csv
├── missing_weekdays.csv
├── collection_summary.json
├── commodity_id_mapping.json
└── reference_commodity_response.json
```

Jika ada request yang gagal secara metodologis/teknis:

```text
data/raw/pihps/errors/
```

akan berisi file diagnostik per chunk.

---

## 12. Raw data policy

Raw JSON diperlakukan sebagai evidence collection.

Raw tidak boleh:

- diubah manual;
- diimputasi;
- di-overwrite dengan hasil cleaning;
- digunakan sebagai tempat menyimpan transformed features.

Normalization dan preprocessing dilakukan pada layer terpisah.

---

## 13. Long-format schema

Collector menghasilkan minimal:

| Field | Meaning |
|---|---|
| `date` | observation date |
| `commodity` | requested PIHPS commodity |
| `comcat_id` | PIHPS commodity identifier |
| `market` | selected level-3 market |
| `market_level` | expected `3` |
| `price_rp_per_kg` | numeric price |
| `source` | PIHPS Bank Indonesia |
| `source_url` | backend endpoint |
| `collection_method` | backend JSON GET |
| `price_type_id` | PIHPS price type |
| `province_id` | PIHPS province identifier |
| `regency_id` | PIHPS regency identifier |
| `tipe_laporan` | report type |

---

## 14. Important temporal notes

PIHPS market observations are not equivalent to a continuously observed 7-day sensor. Missing dates can be caused by the source's market-observation schedule or by source availability.

Therefore:

```text
missing ≠ automatically error
missing ≠ automatically zero
missing ≠ automatically ffill
```

Collection hanya mencatat observation yang benar-benar dikembalikan source. Keputusan imputation, if any, belongs to the next Phase 1/Phase 2 audit and must remain split-aware.

---

## 15. Research integrity rules

Collector harus mempertahankan:

1. source provenance;
2. raw response evidence;
3. exact collection period;
4. market identity;
5. commodity identity;
6. no invented commodity IDs;
7. no fabricated observations;
8. no test-set logic at this stage;
9. no target-derived feature in raw collection;
10. no silent imputation.

---

## 16. Collection acceptance criteria

Collection phase dapat ditandai `PASS` jika:

- [ ] Conda environment aktif dan Python 3.13.x terverifikasi.
- [ ] API endpoint dapat diakses.
- [ ] Semua 12 commodity IDs resolved atau diverifikasi manual.
- [ ] `Pasar Kramatjati`, `level=3`, ditemukan.
- [ ] Raw JSON tersimpan untuk setiap successful chunk.
- [ ] Collection manifest tersedia.
- [ ] Coverage report tersedia.
- [ ] Missing dates dilaporkan.
- [ ] Tidak ada imputasi di collector.
- [ ] Normalized long-format CSV terbentuk.
- [ ] Collection period tepat 2022-01-01 s.d. 2026-09-29.
- [ ] Full collection summary tersedia.

---

## 17. Handoff to next stage

Setelah acceptance criteria PASS, output collection diserahkan ke:

```text
P1 Collection
    ↓
P1 Temporal/Data Audit
    ↓
Phase 2 — Target & Historical Price Dynamics
    ↓
relative movement target
    ↓
historical price features
    ↓
multi-horizon dataset
```

Jangan menghitung target `r(t,h)` pada raw collection layer. Target dan sequence construction dilakukan setelah collection lolos audit.

---

## 18. Source/contract alignment

Dokumen Phase 0 menetapkan bahwa target market adalah Jakarta, CMK dan bawang merah diarahkan ke PIKJ, taxonomy harus dikunci pada Phase 1, dan semua feature transformations harus split-aware. Dokumen juga menetapkan bahwa Phase 1 dimulai dari Data/Temporal Audit lalu supplier/source provenance, temporal alignment, leakage audit, target construction, baseline-ready dataset, split repair, dan reproducibility.  

Referensi internal:

- `ARIF-Net_PROJECT_IMPLEMENTATION_PLAN_v1.1.0_PHASE0_SYNC`
- `ARIF-Net_Phase_0_Research_Contract_v2.0.0`
- Browser DevTools capture / PIHPS API response supplied by researcher
