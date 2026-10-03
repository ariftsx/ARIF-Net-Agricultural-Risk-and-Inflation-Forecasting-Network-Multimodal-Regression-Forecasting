# Phase 1 — Koleksi Harga IPJ (Info Pangan Jakarta): Provenance & Status

**Otoritas:** Plan v2.0.0 (§0.5 P1-DG-01, 02, 04–06, 16; §9; §10.1a) → Contract v2.1.0 (§0B, §3.1, §5.1, §5.6).
**Peran:** sumber **pelengkap**. Karena harganya eceran di **pasar yang sama** dengan target (Pasar Kramat Jati), IPJ menempati prioritas pengisian tertinggi dalam P1-DG-06 dan juga berfungsi sebagai validasi silang PIHPS. **Bukan** target.
**Status dokumen:** diisi bertahap. Hanya fakta dari artefak yang boleh dicantumkan.

---

## 1. Metadata dataset (Plan §9)

| Field | Nilai |
|---|---|
| Dataset name | ARIF-Net supplementary retail price — IPJ Pasar Kramat Jati, 3 komoditas terpetakan |
| Source organization / URL | Pemprov DKI Jakarta — Info Pangan Jakarta, https://infopangan.jakarta.go.id/statistic · `GET /api2/v1/public/report?filterBy=market&Id=12&yearMonth=YYYY-MM` |
| Collection method | JSON GET (parameter dari tangkapan DevTools peneliti 2026-10-03); 1 request per bulan berisi semua komoditas pasar; raw byte-identik + sha256 |
| Market | `market_id` 12 = **Pasar Kramat Jati** (Jakarta Timur, Jl. Raya Bogor KM.20), diverifikasi via `/api2/v1/master-data/market`. Bukan `market_id` 1 (Pasar Induk / PIKJ) |
| Level harga | **Eceran** |
| Pemetaan komoditas | Cabe Merah Keriting (8) → `com_14`; Bawang Merah (12) → `com_11`; **Beras Muncul I (4) → `com_3`** (keputusan peneliti 2026-10-03, konsisten dengan P1-DG-05 di PIBC) |
| Taxonomy caveat | "Bawang Merah" di IPJ tidak menyebut ukuran (PIHPS: "Ukuran Sedang"). Kategori IPJ "Beras Medium" (id 114) baru muncul 2026 dan sangat jarang, sehingga tidak dipakai |
| Coverage date | Diminta 2019-01 → 2026-09 (93 bulan). **Tersedia 2024-01-01 → 2026-09-30** (33 bulan berisi data; 60 bulan 2019-01…2023-12 = `OK_EMPTY`) |
| Frequency | Harian kalender (termasuk akhir pekan) |
| robots.txt | Tidak ada (server mengembalikan halaman SPA), 2026-10-03 |
| License/usage condition | `[MENUNGGU — ketentuan penggunaan data IPJ dicatat peneliti]` |
| Missing-value / imputation | 0/kosong = tidak dilaporkan; tanpa imputasi/ffill |
| Leakage audit status | `[MENUNGGU]` |

## 2. Status langkah

| Langkah | Script | Status |
|---|---|---|
| A+1 — Codebase + setup | `tests/`, `verify_setup.py` | PASS — 12/12 test; setup FAIL=0 (WARN: smoke belum jalan); path terpanjang 251 karakter, 2026-10-03 |
| 2 — Smoke | `collect_ipj.py smoke` | PASS — market_id 12 = 'Pasar Kramat Jati' (`market_level: eceran`, Jakarta Timur); 2024-01: 3 komoditas 31/31 hari |
| 3 — Full | `collect_ipj.py full` | PASS — 93/93 bulan (33 OK, 60 OK_EMPTY). Run 1: 2026-09 FAIL (2026-09-12 ganda); setelah keputusan peneliti diambil ulang → `2026-09.r2.json` OK (raw FAIL tetap disimpan) |
| 4 — Normalisasi | `normalize_ipj.py` | PASS — 2.890 baris (CMK 969, Bawang 969, Beras 952), 0 kosong, 0 duplikat; 3 duplikat identik 2026-09-12 disimpan 1 baris |
| 5 — Audit | `audit_ipj.py` | PASS (deskriptif) — lihat §2a |

## 2a. Temuan audit (2024-01-01 → 2026-09-30)

| | CMK (`com_14`) | Bawang Merah (`com_11`) | Beras Muncul I (`com_3`) |
|---|---|---|---|
| Hari dikembalikan / hari kalender | 969 / 1.004 (35 hari tidak ada) | 969 / 1.004 (35) | 952 / 1.004 (52) |
| Min – max (Rp) | 18.000 – **300.000** | **4.000** – 80.000 | 13.500 – 17.500 |
| vs PIHPS (eceran, pasar sama, tanggal sama) | n=687, identik 11,5%, median \|Δ\| 6,67% | n=687, identik 15,1%, median \|Δ\| 5,66% | n=674, identik 3,9%, median \|Δ\| 5,06% |
| Null PIHPS dengan nilai IPJ di tanggal sama | 4 / 69 | 4 / 69 | 4 / 69 |

1. **Data hanya tersedia sejak 2024-01.** Ke-60 bulan 2019-01 sampai 2023-12 berupa respons valid tetapi kosong (`OK_EMPTY`). Tidak ada bulan kosong di antara bulan-bulan berisi data. Beberapa bulan tidak lengkap per hari (misalnya 2024-04: 19 hari; beras 2024-02: 14 hari).
2. **Kemungkinan salah input di sumber** (berbeda tajam dari nilai sebelum/sesudah). Nilai-nilai ini **tidak dikoreksi**; penanganannya diputuskan di Phase 2 / P1-DG-06 (validasi overlap):
   - CMK 2024-11-29 = 300.000 (sebelum 35.000, sesudah 30.000; PIHPS 35.000), indikasi kelebihan satu digit 0;
   - CMK 2024-06-16 = 18.000 (sebelum/sesudah 70.000; PIHPS null);
   - Bawang Merah 2025-01-14 = 4.000 (sebelum/sesudah 40.000; PIHPS 42.800), indikasi kurang satu digit 0.
3. **Duplikat sumber:** 2026-09-12 muncul dua kali dengan nilai identik di 33 komoditas IPJ (termasuk 3 komoditas terpetakan). Keputusan peneliti: diterima sebagai 1 baris.
4. **IPJ vs PIHPS di pasar yang sama berbeda rata-rata ±5–7%** dan jarang identik. Keduanya survei eceran yang terpisah, sehingga pemakaian IPJ sebagai pengisi wajib melalui validasi overlap dan kalibrasi training-only (P1-DG-06).
5. **Cakupan null target:** IPJ hanya mencakup 4 dari 69 null PIHPS (null PIHPS 2024+). Sisanya berada sebelum 2024 dan hanya tercakup PIBC.

## 3. Log perubahan / keputusan

| Tanggal | Perubahan | Alasan | Referensi |
|---|---|---|---|
| 2026-10-03 | Endpoint dari tangkapan DevTools peneliti; cookie tangkapan **tidak** dipakai/disimpan | — | — |
| 2026-10-03 | Semua bulan 2019-01 → 2026-09 diminta | Keputusan peneliti; probe menunjukkan data mulai 2024-01, kekosongan didokumentasikan sebagai bukti | `config/request_settings.json` |
| 2026-10-03 | Pemetaan 3 komoditas (Beras = Muncul I) | Keputusan peneliti | `config/commodities.json` |
| 2026-10-03 | Duplikat tanggal bernilai identik diterima (1 baris); duplikat bernilai berbeda tetap FAIL | Keputusan peneliti (kasus 2026-09-12) | `scripts/collect_ipj.py::check_month` |
