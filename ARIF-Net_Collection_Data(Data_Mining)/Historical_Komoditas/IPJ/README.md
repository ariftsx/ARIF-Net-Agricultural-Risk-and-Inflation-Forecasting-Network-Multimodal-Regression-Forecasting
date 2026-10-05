# ARIF-Net — Phase 1 · Koleksi Harga IPJ (Info Pangan Jakarta)

Paket ini mengoleksi harga **eceran** harian dari Info Pangan Jakarta untuk **Pasar Kramat Jati (`market_id` 12)**, yaitu pasar yang sama dengan target PIHPS. Di ARIF-Net, IPJ adalah **sumber pelengkap dengan prioritas pengisian tertinggi**, karena harganya eceran dan berasal dari pasar yang sama (P1-DG-06). Data tidak disertakan di repositori; jalankan collector (lihat di bawah) untuk membuatnya di mesin sendiri.

| Target PIHPS | Komoditas IPJ (id) |
|---|---|
| Cabai Merah Keriting `com_14` | Cabe Merah Keriting (8) |
| Bawang Merah Ukuran Sedang `com_11` | Bawang Merah (12). Catatan: IPJ tidak menyebut ukuran |
| Beras Kualitas Medium I `com_3` | Beras Muncul I (4), konsisten dengan P1-DG-05 di PIBC |

- **Endpoint:** `GET https://infopangan.jakarta.go.id/api2/v1/public/report?filterBy=market&Id=12&yearMonth=YYYY-MM`. Satu request = 1 bulan untuk semua komoditas pasar.
- **Periode yang diminta:** 2019-01 → 2026-09 (93 request). Hasil probe: data baru tersedia **mulai 2024-01**. Bulan yang kosong tetap disimpan sebagai bukti, dengan status `OK_EMPTY`.
- **Pasar Induk Kramat Jati** (`market_id` 1, grosir/PIKJ) **tidak dipakai** (P1-DG-02).

## Menjalankan (dari folder `Historical_Komoditas\IPJ`, env `arif-net`)

```cmd
conda run -n arif-net python -m unittest discover -s tests -v
conda run -n arif-net python scripts\verify_setup.py
conda run -n arif-net python scripts\collect_ipj.py smoke
conda run -n arif-net python scripts\collect_ipj.py full
conda run -n arif-net python scripts\normalize_ipj.py
conda run -n arif-net python scripts\audit_ipj.py
```

## Aturan
1. Raw byte-identik dan tidak pernah ditimpa. Raw memuat semua komoditas pasar, sedangkan data processed hanya berisi 3 komoditas terpetakan.
2. Nilai 0 atau kosong berarti tidak dilaporkan. Tidak ada imputasi, ffill, maupun kalibrasi. Pengisian null PIHPS dilakukan di tahap P1-DG-06.
3. Cookie atau token dari tangkapan browser tidak dipakai.
