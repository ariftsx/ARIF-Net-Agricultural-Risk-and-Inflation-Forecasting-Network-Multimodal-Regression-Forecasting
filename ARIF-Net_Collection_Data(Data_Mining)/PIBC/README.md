# ARIF-Net — Phase 1 · Koleksi Harga Beras PIBC (Pasar Induk Beras Cipinang)

Paket ini mengoleksi harga beras **grosir** harian dari situs PIBC (PT Food Station Tjipinang Jaya). Di ARIF-Net, PIBC berperan sebagai **sumber pelengkap dan konteks pasokan beras**, bukan target (P1-DG-01/02/06). Detail provenance ada di [`docs/PHASE1_COLLECTION_PIBC.md`](docs/PHASE1_COLLECTION_PIBC.md).

- Endpoint: `GET https://pibc.foodstation.co.id/rice-price-detail` (DataTables server-side). Sebelumnya dilakukan warm-up `GET /rice-price` untuk cookie sesi; tidak ada cookie atau token yang di-hardcode.
- **Semantik tanggal (terverifikasi):** `start_date` eksklusif dan `end_date` inklusif, sehingga untuk rentang [S, E] collector mengirim `start_date = S − 1`. Server mengabaikan parameter `order`.
- **Periode:** 2019-01-01 → **2025-06-16**. Tanggal akhir ini adalah data terakhir di sumber, karena situs tidak diperbarui lagi. Totalnya 2.359 hari kalender, harian penuh termasuk akhir pekan.
- **Raw:** 7 file tahunan, byte-identik, masing-masing memuat 14 varietas.
- **Processed:** **hanya** kolom PIBC yang dipetakan ke **Beras Kualitas Medium I**. Pemetaan ini adalah keputusan peneliti (P1-DG-05) dan disimpan di `config/varieties.json` → `medium_i_mapping`.

## Menjalankan (dari folder `PIBC`, env `arif-net`)

```cmd
conda run -n arif-net python -m unittest discover -s tests -v
conda run -n arif-net python scripts\verify_setup.py
conda run -n arif-net python scripts\collect_pibc.py smoke
conda run -n arif-net python scripts\collect_pibc.py full
conda run -n arif-net python scripts\mapping_evidence.py      :: bahan keputusan pemetaan (2019–2020 saja)
:: → peneliti memutuskan medium_i_mapping
conda run -n arif-net python scripts\normalize_pibc.py
conda run -n arif-net python scripts\audit_pibc.py
```

## Aturan
1. Raw tidak pernah diedit atau ditimpa.
2. Tidak ada imputasi, ffill, kalibrasi, maupun pengisian null target di paket ini. Pengisian null PIHPS dari PIBC dilakukan di tahap P1-DG-06: kolom `value_source` + `is_filled`, validasi overlap, dan kalibrasi yang di-fit hanya pada data training.
3. Level harga PIBC = **grosir pasar induk**, berbeda dengan PIHPS yang eceran. Halaman sumber menyebut "Harga Rata-Rata dalam Rupiah" tanpa menulis satuan /kg secara eksplisit.
