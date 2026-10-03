# Phase 1 — Koleksi Harga PIHPS: Provenance & Status

**Otoritas:** Plan v2.0.0 (§0.5 P1-DG-01…06, 13, 16; §9; §10.1a) → Contract v2.1.0 (§0B, §3.1, §5.1, §5.6).
**Status dokumen:** diisi bertahap. Hanya fakta dari artefak di `reports/` dan `data/raw/pihps/` yang boleh dicantumkan. Bagian bertanda `[MENUNGGU …]` belum dijalankan.

---

## 1. Metadata dataset (Plan §9)

| Field | Nilai |
|---|---|
| Dataset name | ARIF-Net target price — PIHPS Pasar Kramatjati (eceran), 3 komoditas primary |
| Source organization / URL | Bank Indonesia — Pusat Informasi Harga Pangan Strategis (PIHPS), https://www.bi.go.id/hargapangan · endpoint `WebSite/TabelHarga/GetGridDataKomoditas` |
| Collection method | HTTP GET JSON backend (parameter dari tangkapan DevTools peneliti), warm-up cookie halaman publik, 1 request per (komoditas, bulan); raw response disimpan byte-identik + sha256 |
| Parameter tetap | `price_type_id=1` (pasar tradisional), `province_id=13` (DKI Jakarta), `regency_id=34`, `showKota=true`, `showPasar=true`, `tipe_laporan=1` |
| Market | **Pasar Kramatjati**, level 3 (P1-DG-02/03). Label regency sumber "Kota Jakarta Pusat" = *source quirk*; secara geografis Jakarta Timur |
| Level harga | **Eceran** (wajib disebut dalam penulisan akademik, P1-DG-02) |
| Commodity | Cabai Merah Keriting `com_14`, Bawang Merah Ukuran Sedang `com_11`, Beras Kualitas Medium I `com_3` (P1-DG-04/05) |
| Coverage date | 2019-01-01 → 2026-09-30 (P1-DG-16 + keputusan peneliti 2026-10-03) |
| Frequency | Harian, hari kerja (pelaporan PIHPS) |
| Timezone | Tanggal lokal (WIB) sebagaimana dikembalikan sumber |
| Publication/availability time | Harga hari `t` boleh dipakai untuk origin `t` bila sudah tercatat pada cutoff (Contract §5.1) |
| Raw file hash/version | sha256 per file di `data/raw/pihps/collection_manifest.csv` |
| License/usage condition | `[MENUNGGU — ketentuan penggunaan data situs BI dicatat peneliti]` |
| Missing-value policy | `"-"` = tidak dilaporkan → price kosong, `is_reported=false`; tanggal yang tidak dikembalikan dilaporkan di audit |
| Imputation policy | Tidak ada di collection layer. Pengisian null hanya dari PIBC/IPJ dengan `value_source` + `is_filled`, di layer terpisah (P1-DG-06) |
| Transformation | Hanya wide (kolom tanggal) → long; `"50,000"` → 50000 (koma = pemisah ribuan) |
| Feature list | `price_rp_per_kg` per (date, comcat_id) |
| Temporal cutoff rule | Nilai hari `t` tersedia untuk origin `t` (Contract §5.1) |
| Leakage audit status | `[MENUNGGU Phase 1 leakage audit]` |

## 2. Status langkah

| Langkah | Script | Status | Artefak |
|---|---|---|---|
| A — Codebase + test offline | `tests/test_offline.py` | PASS 13/13 (2026-10-03); simulasi normalisasi+audit dgn raw asli 2022-01..03 dari git: 192/192 identik dgn arsip | output unittest |
| 1 — Setup + arsip | `verify_setup.py` | PASS (FAIL=0; WARN=1 smoke belum jalan); arsip 2022 dipindah | `reports/setup_check.json` |
| 2 — Smoke | `collect_pihps.py smoke` | PASS (2026-10-03T09:58Z). ID terverifikasi di reference resmi: `{"id":"com_3","name":"Beras Kualitas Medium I","cat_id":"cat_1"}`, `com_11` = Bawang Merah Ukuran Sedang (cat_5), `com_14` = "Cabai Merah Keriting " (cat_7; spasi di akhir nama berasal dari sumber). Januari 2019: 23/23 hari kerja, 22 dilaporkan, 1 `-` (2019-01-01, libur Tahun Baru) di ketiga komoditas | `reports/smoke_pihps.json` |
| 3 — Full collection | `collect_pihps.py full` | PASS — 279/279 chunk (93 per komoditas), 0 error, 2026-10-03T09:59Z → 10:07Z | `collection_manifest.csv`, `collection_summary.json` |
| 4 — Normalisasi | `normalize_pihps.py` | PASS — sha256 279/279 cocok; 6.066 baris (2.022 per komoditas), 5.859 dilaporkan, 207 `-`; 0 duplikat | `reports/normalize_check.json` |
| 5 — Audit | `audit_pihps.py` | PASS — coverage hari kerja 100%; 0 tanggal akhir pekan; overlap arsip 2022: 3.711/3.711 identik (lihat §2a) | `reports/audit_pihps_*` |

## 2a. Temuan audit (2019-01-01 → 2026-09-30)

| | CMK `com_14` | Bawang Merah `com_11` | Beras Medium I `com_3` |
|---|---|---|---|
| Tanggal dikembalikan / hari kerja | 2.022 / 2.022 (100%) | 2.022 / 2.022 | 2.022 / 2.022 |
| Dilaporkan / `-` | 1.953 / 69 | 1.953 / 69 | 1.953 / 69 |
| Harga min – median – max (Rp/kg) | 20.000 – 50.000 – 150.000 | 25.000 – 40.300 – 82.500 | 11.950 – 14.000 – 16.100 |
| Hari tanpa perubahan harga | 68,65% | 80,89% | 96,41% |
| Run nilai berulang terpanjang | 24 hari kerja (s.d. 2021-09-06) | 49 (s.d. 2021-01-05) | **243** (s.d. 2021-03-30) |
| Lompatan harian terbesar | +66,67% (2022-01-17, 2024-04-29) | +37,5% (2022-09-13) | +14,34% lalu −12,54% (2022-07-12/13) |

1. **Tanggal `-` (69 per komoditas) identik di ketiga komoditas** dan berpola libur nasional/cuti bersama (contoh blok: 2019-06-05…07, 2020-05-21…25, 2022-04-29…05-06 = sekitar Idulfitri). Tidak diimputasi.
2. **Perubahan perilaku sumber:** jumlah `-` per tahun = 2019: 14 · 2020: 20 · 2021: 13 · 2022: 14 · **2023: 4 · 2024: 3 · 2025: 1 · 2026: 0**. Sejak 2023, PIHPS hampir selalu mengisi harga pada hari libur. Ini perlu dipertimbangkan di Phase 2 (konsistensi temporal dan definisi observasi), tetapi tidak diubah di collection layer.
3. **Seri lengket (sticky):** beras tidak berubah pada 96% hari dan memiliki run 243 hari kerja. Ini adalah observasi valid (P1-DG-06) dan relevan untuk known issue Q95 (P1-DG-08).
4. **Spike–reversal beras 2022-07-12/13** (+14,3% lalu −12,5%) dilaporkan apa adanya. Penilaiannya (outlier sumber atau bukan) diputuskan di Phase 2.
5. **Reproducibility:** 3.711 baris overlap dengan run 2022 (2022-01-03 → 2026-09-29) **100% identik**, termasuk status `-`. Sumber tidak merevisi data historis di periode tersebut.

Rincian: `reports/audit_pihps_summary.json`, `audit_pihps_not_reported.csv`, `audit_pihps_missing_weekdays.csv` (kosong), `audit_pihps_vs_archive2022.csv` (kosong = tidak ada perbedaan).

## 3. Log perubahan / keputusan

| Tanggal | Perubahan | Alasan | Referensi |
|---|---|---|---|
| 2026-10-03 | Koleksi ulang dari 2019; hanya 3 komoditas primary; end_date 2026-09-30 | Keputusan peneliti; P1-DG-04/16 | Plan §0.5 |
| 2026-10-03 | Artefak run 2022 dipindah ke `archive/run_2022/` (tidak dihapus) | Keputusan peneliti; hindari tercampur | `archive/run_2022/ARCHIVE_NOTE.md` |
| 2026-10-03 | Collector ditulis ulang: raw byte-identik, anti-timpa, resume, verifikasi ID via reference | Script lama menyimpan raw via `json.dumps` & menghapus manifest tiap run | git `aa3844f` |
| 2026-10-03 | CSV processed dilacak Git LFS | Konsisten dengan paket Iklim | `.gitattributes` |
| 2026-10-03 | Struktur: paket dipindah ke `Historical_Komoditas/PIHPS/` (satu folder untuk semua sumber harga komoditas); `environment.yml`, `requirements.txt`, `.gitignore`, `.gitattributes` disatukan di `Historical_Komoditas/` | Permintaan peneliti; manifest & raw tidak berubah (path relatif terhadap paket) | `Historical_Komoditas/README.md` |
