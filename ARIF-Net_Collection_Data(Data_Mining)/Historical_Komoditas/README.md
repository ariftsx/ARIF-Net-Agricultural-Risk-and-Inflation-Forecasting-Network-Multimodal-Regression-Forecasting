# ARIF-Net — Phase 1 · Koleksi Harga PIHPS (Pasar Kramatjati, 2019 → 2026-09-30)

Paket ini mengoleksi harga **eceran** harian dari **PIHPS Bank Indonesia** untuk target market **Pasar Kramatjati (level 3)**. Komoditas yang dikoleksi adalah 3 komoditas primary Capstone. Dasarnya adalah P1-DG-01…06, 13, dan 16 (Plan v2.0.0 §0.5, §10.1a; Contract v2.1.0 §3.1, §5.6). Detail provenance ada di [`docs/PHASE1_COLLECTION_PIHPS.md`](docs/PHASE1_COLLECTION_PIHPS.md).

| Komoditas | comcat_id |
|---|---|
| Cabai Merah Keriting | `com_14` |
| Bawang Merah Ukuran Sedang | `com_11` |
| Beras Kualitas Medium I | `com_3` |

Endpoint: `GET https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas` (`price_type_id=1`, `province_id=13`, `regency_id=34`, `tipe_laporan=1`), dengan chunk bulanan, 3 × 93 = **279 request**.

## Menjalankan (Windows CMD, dari folder `Historical_Komoditas`, env `arif-net`)

```cmd
conda run -n arif-net python -m unittest discover -s tests -v
conda run -n arif-net python scripts\verify_setup.py
conda run -n arif-net python scripts\collect_pihps.py smoke
conda run -n arif-net --no-capture-output python scripts\collect_pihps.py full
conda run -n arif-net python scripts\normalize_pihps.py
conda run -n arif-net python scripts\audit_pihps.py
```

Perintah `full` akan resume otomatis: chunk yang sukses (HTTP 200, check OK, sha256 cocok) di-skip saat dijalankan ulang.

## Struktur

```text
config/      commodities.json · request_settings.json · state.json (ditulis script)
scripts/     common.py · verify_setup.py · collect_pihps.py · normalize_pihps.py · audit_pihps.py
tests/       test_offline.py
data/raw/pihps/<comcat_id>/<YYYY-MM>.json   ← raw evidence (byte-identik dengan response)
data/raw/pihps/reference/ · smoke/ · collection_manifest.csv · collection_summary.json
data/processed/pihps/pihps_kramatjati_long.csv   ← Git LFS
archive/run_2022/   ← artefak run lama 2022-01 → 2026-09 (12 komoditas); hanya sebagai pembanding audit
reports/ · logs/
```

## Aturan integritas (ringkas)

1. Raw tidak pernah diedit atau ditimpa. Pengambilan ulang menghasilkan file `.rN.json`.
2. Nilai `"-"` dari sumber berarti **tidak dilaporkan**: `price_rp_per_kg` dikosongkan dan `is_reported=false`. **Tidak ada imputasi atau ffill.** Pengisian dari PIBC/IPJ hanya boleh dilakukan di layer terpisah (P1-DG-06).
3. Harga yang sama berhari-hari adalah **observasi valid** (P1-DG-06).
4. Level harga = **eceran**. Label regency PIHPS "Kota Jakarta Pusat" adalah *source quirk* (P1-DG-03); Pasar Kramatjati berada di Jakarta Timur.
5. Target `r(t,h)` dan fitur harga **tidak** dihitung di sini; keduanya bagian dari Phase 2.
