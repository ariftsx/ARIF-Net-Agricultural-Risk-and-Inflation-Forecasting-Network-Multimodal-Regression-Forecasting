# ARIF-Net — Phase 1 · Koleksi Harga Komoditas

Folder ini berisi semua collector **harga komoditas** ARIF-Net. Setiap sumber adalah sub-paket mandiri dengan config, script, test, data, dan report-nya sendiri. Path di manifest dan report selalu relatif terhadap folder sub-paket, sehingga sub-paket bisa dipindah tanpa merusak bukti.

**Otoritas:** Plan v2.0.0 §0.5 (P1-DG-01…06, 13, 16), §10.1a · Contract v2.1.0 §3.1, §5.1, §5.6.

| Sumber | Folder | Peran | Level harga | Komoditas | Periode | Status |
|---|---|---|---|---|---|---|
| PIHPS Bank Indonesia | [`PIHPS/`](PIHPS/README.md) | **target** (P1-DG-01/02) | eceran, Pasar Kramatjati (L3) | CMK `com_14`, Bawang Merah `com_11`, Beras Medium I `com_3` | 2019-01-01 → 2026-09-30 | PASS |
| PIBC (Pasar Induk Beras Cipinang) | [`PIBC/`](PIBC/README.md) | **pelengkap** (P1-DG-06) & konteks pasokan | grosir pasar induk | Muncul I (= Beras Medium I, P1-DG-05) | 2019-01-01 → 2025-06-16 (akhir data sumber) | PASS |
| Info Pangan Jakarta (IPJ) | [`IPJ/`](IPJ/README.md) | **pelengkap** (P1-DG-06), prioritas tertinggi: eceran pasar sama | eceran, Pasar Kramat Jati (`market_id` 12) | CMK, Bawang Merah, Beras Muncul I | 2024-01-01 → 2026-09-30 (sebelum 2024 tidak tersedia) | PASS |

## Struktur

```text
Historical_Komoditas/
├── README.md · environment.yml · requirements.txt · .gitignore · .gitattributes   ← dipakai bersama
├── PIHPS/   config/ scripts/ tests/ data/ reports/ logs/
├── PIBC/    config/ scripts/ tests/ data/ reports/ logs/
└── IPJ/     config/ scripts/ tests/ data/ reports/ logs/
```

## Menjalankan

Env **`arif-net`** (`conda env update -n arif-net -f environment.yml` bila paket belum lengkap). Jalankan setiap sumber **dari foldernya sendiri**:

```cmd
cd Historical_Komoditas\PIHPS
conda run -n arif-net python -m unittest discover -s tests
conda run -n arif-net python scripts\verify_setup.py
conda run -n arif-net python scripts\collect_pihps.py smoke
conda run -n arif-net python scripts\collect_pihps.py full
conda run -n arif-net python scripts\normalize_pihps.py
conda run -n arif-net python scripts\audit_pihps.py

cd ..\PIBC
conda run -n arif-net python scripts\verify_setup.py
conda run -n arif-net python scripts\collect_pibc.py smoke
conda run -n arif-net python scripts\collect_pibc.py full
conda run -n arif-net python scripts\mapping_evidence.py
conda run -n arif-net python scripts\normalize_pibc.py
conda run -n arif-net python scripts\audit_pibc.py

cd ..\IPJ
conda run -n arif-net python scripts\verify_setup.py
conda run -n arif-net python scripts\collect_ipj.py smoke
conda run -n arif-net python scripts\collect_ipj.py full
conda run -n arif-net python scripts\normalize_ipj.py
conda run -n arif-net python scripts\audit_ipj.py
```

`PIBC/scripts/mapping_evidence.py`, `audit_pibc.py`, dan `IPJ/scripts/audit_ipj.py` membaca `PIHPS/data/processed/pihps/pihps_kramatjati_long.csv`, jadi PIHPS harus selesai lebih dulu.

## Aturan bersama

1. Raw adalah evidence: byte-identik dengan response, sha256 tercatat di manifest, dan tidak pernah ditimpa (pengambilan ulang menghasilkan `.rN.json`).
2. Tidak ada imputasi, ffill, kalibrasi, atau perhitungan target di collection layer.
3. Null pada seri target PIHPS **hanya** boleh diisi dari sumber pelengkap di tahap P1-DG-06 (terpisah dari folder ini), dengan syarat:
   - kolom `value_source` + `is_filled`;
   - validasi pada hari overlap;
   - kalibrasi yang di-fit hanya pada data training;
   - eksperimen dilaporkan dengan dan tanpa nilai isian.
4. Cookie atau token tidak pernah di-hardcode; sesi diambil lewat warm-up halaman publik.
5. Isi `data/`, `reports/`, `logs/`, dan `config/state.json` **tidak di-commit**. Setiap anggota tim menjalankan collector sendiri; repositori hanya menyimpan kode, config, dan README.
