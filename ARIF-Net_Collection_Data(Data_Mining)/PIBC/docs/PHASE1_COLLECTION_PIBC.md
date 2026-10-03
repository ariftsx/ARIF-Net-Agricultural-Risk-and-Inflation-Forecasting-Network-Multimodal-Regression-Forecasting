# Phase 1 — Koleksi Harga Beras PIBC: Provenance & Status

**Otoritas:** Plan v2.0.0 (§0.5 P1-DG-01, 02, 05, 06, 16; §9; §10.1a) → Contract v2.1.0 (§0B, §3.1 catatan taxonomy, §5.1, §5.6).
**Peran:** sumber **pelengkap** untuk mengisi null seri target (P1-DG-06) dan konteks pasokan beras (P1-DG-02). **Bukan** target market.
**Status dokumen:** diisi bertahap. Hanya fakta dari artefak di `reports/` dan `data/raw/pibc/` yang boleh dicantumkan.

---

## 1. Metadata dataset (Plan §9)

| Field | Nilai |
|---|---|
| Dataset name | ARIF-Net supplementary rice price — PIBC (Pasar Induk Beras Cipinang), kolom terpetakan ke Beras Kualitas Medium I |
| Source organization / URL | PT Food Station Tjipinang Jaya — https://pibc.foodstation.co.id/rice-price · endpoint `GET /rice-price-detail` |
| Collection method | DataTables server-side JSON GET (parameter dari tangkapan DevTools peneliti, 2026-10-03), warm-up cookie halaman publik, 1 request per tahun (`length=400`); raw byte-identik + sha256 |
| Semantik tanggal | Terverifikasi probe 2026-10-03: `start_date` **eksklusif**, `end_date` inklusif, label `tgl` tidak bergeser → collector mengirim `start_date = S − 1` |
| Market / level harga | Pasar Induk Beras Cipinang, **grosir** (berbeda dengan target PIHPS yang **eceran**) |
| Unit | Halaman: "Harga Rata-Rata dalam Rupiah". **Satuan per kg tidak tertulis eksplisit** |
| Coverage date | 2019-01-01 → **2025-06-16** (data terakhir di sumber; situs tidak diperbarui setelahnya) |
| Frequency | Harian kalender penuh, termasuk akhir pekan |
| Varietas di sumber | 14: Cianjur Kepala, Cianjur Slyp, Setra, Saigon, Muncul I/II/III, IR-64 I/II/III, IR-42, Ketan Putih Lokal, Ketan Putih Paris, Ketan Hitam |
| Varietas diproses | **Hanya Muncul I** (`muncul1`), dipetakan ke Beras Kualitas Medium I (keputusan peneliti 2026-10-03, P1-DG-05) |
| robots.txt | `User-agent: *` / `Disallow:` kosong (2026-10-03) |
| License/usage condition | `[MENUNGGU — ketentuan penggunaan data situs PIBC dicatat peneliti]` |
| Missing-value / imputation | Tidak ada imputasi/ffill; nilai kosong dilaporkan |
| Leakage audit status | `[MENUNGGU]`. Bukti pemetaan dihitung hanya pada 2019–2020 (lihat §3) |

## 2. Status langkah

| Langkah | Script | Status |
|---|---|---|
| A+1 — Codebase + setup | `tests/`, `verify_setup.py` | PASS — 12/12 test; setup FAIL=0 (WARN: pemetaan belum diputuskan, smoke belum jalan), 2026-10-03 |
| 2 — Smoke | `collect_pibc.py smoke` | PASS — Jan 2019: 31/31 hari, baris pertama `2019 01 01` (pergeseran start_date terbukti benar), 0 nilai kosong |
| 3 — Full | `collect_pibc.py full` | PASS — 7/7 chunk, 2.359 baris (2019-01-01 → 2025-06-16), setiap chunk = jumlah hari kalender, 0 nilai kosong (14 varietas) |
| 4 — Bukti pemetaan | `mapping_evidence.py` | Selesai — 11 kandidat non-ketan, 489 tanggal berpasangan (2019–2020) |
| 5 — Normalisasi + audit | `normalize_pibc.py`, `audit_pibc.py` | PASS — `muncul1`: 2.359/2.359 hari, 0 kosong, 0 duplikat; Rp 9.925 – 11.150 (median) – 15.900; tanpa perubahan 85,96%; run terpanjang 88 hari |

## 3. Pemetaan Beras Kualitas Medium I → PIBC (P1-DG-05)

PIBC **tidak** memiliki kolom bernama "Medium I". Pemetaan adalah **keputusan peneliti** dan dicatat di `config/varieties.json` → `medium_i_mapping` beserta tanggalnya. Bahan keputusannya ada di `reports/mapping_evidence.{json,csv}`, yang dihitung **hanya pada 2019-01-01 → 2020-12-31** (anti-leakage).

**Keputusan peneliti (2026-10-03, CP2): Beras Kualitas Medium I (PIHPS `com_3`) → PIBC `Muncul I` (`muncul1`).**

Alasan peneliti: seri Muncul (I, II, III) membagi tingkatan kelas mutu Medium. Muncul I adalah tingkat tertinggi di kelas medium, dengan pemenuhan fisik medium kelas I (butir kepala minimal 80%, butir patah maksimal 18%). Rujukan standar mutu yang mendasari angka ini dicatat peneliti di `DATA_DICTIONARY.md`.

Bukti statistik 2019–2020 (`reports/mapping_evidence.*`) **lemah**. Seri PIHPS hampir datar, sehingga hanya ada 1–7 pasangan tanggal di mana keduanya sama-sama berubah. Untuk Muncul I: rasio PIHPS/PIBC = 1,21 (CV 3,4%) dan korelasi level −0,08. Karena itu keputusan ini **berbasis definisi mutu**, bukan statistik. Validasi overlap dan kalibrasi tetap wajib dilakukan pada tahap P1-DG-06 (hanya data training).

### Temuan audit seri terpetakan
- Data harian penuh 2019-01-01 → 2025-06-16 (2.359 hari), tanpa nilai kosong.
- **Semua 69 tanggal null PIHPS `com_3` memiliki nilai PIBC Muncul I pada tanggal yang sama.** Tidak ada null PIHPS setelah PIBC berakhir. Ini deskriptif saja; pengisian dilakukan di P1-DG-06 dengan `value_source` + `is_filled`.
- Lompatan harian terbesar: +10,37% (2023-09-20); −7,89% lalu +8,56% (2021-12-25/26, pola turun-naik di sekitar Natal). Dilaporkan, tidak dikoreksi.

## 4. Log perubahan / keputusan

| Tanggal | Perubahan | Alasan | Referensi |
|---|---|---|---|
| 2026-10-03 | Endpoint & parameter dari tangkapan DevTools peneliti; cookie tangkapan **tidak** dipakai/disimpan | Sesi diambil ulang via warm-up | — |
| 2026-10-03 | Periode 2019-01-01 → 2025-06-16 | Peneliti meminta verifikasi tanggal akhir; probe: data terakhir `2025 06 16`, query setelahnya 0 baris | `config/request_settings.json` |
| 2026-10-03 | Pemetaan Medium I → `muncul1` (Muncul I) | Keputusan peneliti di CP2 berbasis definisi mutu | `config/varieties.json` |
| 2026-10-03 | Hanya kolom terpetakan ke Beras Medium I yang diproses; raw tetap 14 varietas | Keputusan peneliti (sesuai kontrak) | P1-DG-05 |
