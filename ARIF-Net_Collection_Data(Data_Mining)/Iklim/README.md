# ARIF-Net — Phase 1 · Koleksi Data Iklim (Open-Meteo)

Paket ini mengoleksi data iklim harian *reanalysis* dari **Open-Meteo Historical Weather API** untuk 18 kabupaten kandidat pemasok Jakarta. Dasarnya adalah keputusan P1-DG-09 sampai P1-DG-17 (Plan v2.0.0 §0.5, §10.2a; Contract v2.1.0 §5.6). Detail provenance ada di [`docs/PHASE1_COLLECTION_OPENMETEO.md`](docs/PHASE1_COLLECTION_OPENMETEO.md).

| Elemen | Nilai |
|---|---|
| Endpoint | `GET https://archive-api.open-meteo.com/v1/archive` |
| Model | `era5_seamless` (fallback `era5` hanya lewat smoke test, dicatat). Best Match dilarang |
| Periode | 2018-01-01 → 2026-09-30, chunk tahunan |
| Variabel | 9 core (modelling) + 11 reserve (disimpan terpisah, tidak dipakai) |
| Unit/waktu | celsius · m/s · mm · iso8601 · Asia/Jakarta |
| Titik | centroid poligon kabupaten GADM 4.1 (EPSG:6933 → WGS84) |

## Menjalankan (Windows CMD, dari folder `Iklim`)

Env: **`arif-net`**. `conda run` dipakai agar tidak bergantung pada `conda activate`.

```cmd
:: 0. sekali saja — paket geospasial untuk centroid
conda install -n arif-net -c conda-forge geopandas pyogrio pyproj shapely

:: test offline (tanpa internet)
conda run -n arif-net python -m unittest discover -s tests -v

:: Langkah 1 — verifikasi setup
conda run -n arif-net python scripts\verify_setup.py

:: Langkah 2 — batas GADM + centroid
conda run -n arif-net python scripts\fetch_boundaries.py
conda run -n arif-net python scripts\compute_centroids.py --dry-run
conda run -n arif-net python scripts\compute_centroids.py

:: Langkah 3–4 — smoke test (Brebes, Januari 2018)
conda run -n arif-net python scripts\collect_openmeteo.py smoke --set core
conda run -n arif-net python scripts\collect_openmeteo.py smoke --set reserve
::   bila core FAIL karena variabel kosong → fallback P1-DG-10:
::   ... smoke --set core --model era5   lalu   ... smoke --set reserve --model era5

:: Langkah 5 — full collection (resume otomatis; jalankan ulang perintah yang sama bila berhenti)
conda run -n arif-net python scripts\collect_openmeteo.py full

:: Langkah 6–7 — normalisasi & audit
conda run -n arif-net python scripts\normalize_openmeteo.py
conda run -n arif-net python scripts\audit_openmeteo.py
```

Supaya log tampil langsung di layar, tambahkan `--no-capture-output` setelah `conda run`.

## Kuota API

Free tier Open-Meteo dibatasi 600 call/menit, 5.000/jam, dan 10.000/hari. Request dengan lebih dari 10 variabel atau lebih dari 14 hari **dihitung pecahan**: bobot = `max(1, n_var/10) × max(1, n_hari/14)`. Dengan rumus itu, satu chunk 1 tahun bernilai sekitar 26 call untuk core dan 29 untuk reserve. Total koleksi sekitar 8.600 call.

- `common.ApiBudget` membatasi pemakaian ke 480/menit, 4.000/jam, dan 8.000/hari (bisa diatur di `config/request_settings.json`). Setiap request dicatat di `logs/api_ledger.csv`.
- Bila jatah harian habis, `full` berhenti dengan rapi (exit code 3) dan mencetak jam lanjutnya. Jalankan ulang perintah yang sama; chunk yang sudah sukses akan di-skip.
- Perkiraan durasi: sekitar 2,2 jam efektif, tersebar di **±2 hari** karena batas harian.

## Struktur

```text
config/      locations.json · variables.json · request_settings.json · state.json (ditulis script)
scripts/     common.py · verify_setup.py · fetch_boundaries.py · compute_centroids.py
             collect_openmeteo.py · normalize_openmeteo.py · audit_openmeteo.py
tests/       test_offline.py
data/raw/openmeteo/{core,reserve}/<lokasi>/<tahun>.json   ← raw evidence (byte-identik)
data/raw/openmeteo/smoke/  collection_manifest.csv  collection_summary.json
data/processed/openmeteo/climate_{core,reserve}_long.csv
data/external/boundaries/  (GADM — tidak di-commit)
reports/     setup_check · boundaries_check · centroids_* · smoke_* · normalize_check · audit_*
logs/        log per run + api_ledger.csv
```

## Catatan pemakaian data

- **`usable_end_date` = 2026-09-24** (keputusan peneliti, CP6 opsi A). Fitur Phase 3 memotong seri iklim di tanggal ini, karena 2026-09-25 sampai 09-30 berada di tepi rilis ERA5 (berisi null dan `precipitation_hours` bernilai artefak). Raw dan processed tetap utuh sampai 2026-09-30.
- CSV processed (70–92 MB) dilacak **Git LFS** lewat `.gitattributes` (`data/processed/**/*.csv`). Jalankan `git lfs install` sekali per mesin sebelum clone atau commit.

## Aturan integritas (ringkas)

1. Raw JSON tidak pernah diedit atau ditimpa. Pengambilan ulang menghasilkan file `.rN.json` dan manifest menunjuk ke versi terbaru.
2. Tidak ada imputasi, agregasi, lag t−5, rolling, anomaly, atau scaling di layer ini; semuanya dikerjakan di Phase 3.
3. Satu model untuk seluruh seri. Core dan reserve memakai model yang sama.
4. Lokasi berstatus *candidate supplier region*, bukan bobot market share.
5. Data ini adalah **reanalysis**, bukan observasi stasiun. Gunakan istilah yang benar di setiap laporan.
6. Atribusi: *Weather data by Open-Meteo.com* (CC BY 4.0), reanalysis ERA5/ERA5-Land dari Copernicus C3S.
