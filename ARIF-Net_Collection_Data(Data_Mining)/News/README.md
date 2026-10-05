# ARIF-Net — Phase 1 · Koleksi News (berita pangan, harga, inflasi, cuaca, supply, BBM)

Folder ini berisi collector **news** ARIF-Net, setara dengan `Iklim\` dan `Historical_Komoditas\`. News/sentiment adalah modality eksternal inti (Plan DG-09, Contract DG-10). Collection layer di sini hanya mengumpulkan **artikel mentah, metadata, dan timestamp terbit**. Skor sentimen dan fitur harian dikerjakan di **Phase 3**.

> **Status (3 Okt 2026):** Smoke PASS. **Sumber: Kompas, detikFinance, CNN Indonesia, CNBC Indonesia, Kontan, Liputan6 · 2019-01-01 → 2026-09-30 · judul + waktu + metadata (tanpa isi) · kolom `topics_matched` & `wilayah_pemasok`.** Full collection: **93 fase × 1 bulan (±40–60 menit/fase)**.
> Data, hasil probe, dan laporan run tidak disertakan di repositori; jalankan collector (lihat di bawah) untuk membuatnya di mesin sendiri.

## Ringkasan hasil probe (dasar keputusan P1-DG-25)

| Sumber | Arsip 2019 | Catatan |
|---|---|---|
| Kompas, Detik, CNBC Indonesia, Kontan, CNN Indonesia | ✅ Indeks per tanggal tersedia | Kompas melarang search, sehingga wajib lewat indeks |
| Antara | ⚠️ Belum terverifikasi | Butuh tangkapan DevTools |
| Katadata | ❌ Sitemap mulai 2021-01 | Cadangan untuk 2021+ |
| Bisnis.com, Tempo | ❌ HTTP 403 | Tidak disarankan |
| GDELT DOC API | ❌ HTTP 429 konsisten dari jaringan ini | Alternatif: GDELT via BigQuery (butuh GCP) |

## Struktur

```text
News/
├── README.md · .gitignore · .gitattributes
├── config/news_scope_DRAFT.json     ← draf topik/kata kunci (BELUM keputusan)
├── config/sources.json              ← pola URL indeks per media (terverifikasi), strategi waktu terbit
├── scripts/collect_index.py · collect_articles.py · normalize_news.py · audit_news.py · verify_setup.py
│           common.py · parsers.py · index_items.py   ← collector
├── scripts/probe_*.py · verify_kompas.py · verify_media.py   ← probe & verifikasi (read-only)
├── data/raw/news/probe/             ← bukti probe byte-identik (robots, sitemap, indeks, GDELT)
├── data/processed/news/             ← articles.csv
├── reports/                         ← hasil probe dan laporan per fase
└── logs/ · tests/                   ← data, reports, dan logs dibuat oleh script; tidak di-commit
```

## Menjalankan full collection (93 fase × 1 bulan, dari folder `News`, env `arif-net`)

```cmd
conda run -n arif-net --no-capture-output python scripts\run_phase.py --month 2019-01 --max-minutes 60
:: lalu --month 2019-02, 2019-03, … 2026-09. Bila terhenti, jalankan ulang perintah yang sama (resume otomatis).
```
Satu fase berlangsung ±40–60 menit. Laptop hanya perlu menyala selama fase berjalan. Hasil tiap fase ada di `reports/phase_<YYYY-MM>.json`.

## Menjalankan probe (dari folder `News`, env `arif-net`)

```cmd
conda run -n arif-net python scripts\probe_portals.py
conda run -n arif-net python scripts\probe_sitemaps.py
conda run -n arif-net python scripts\probe_indeks.py
conda run -n arif-net python scripts\probe_gdelt.py
```

## Aturan (Plan §10.4, Contract §5.3, §19)
1. Setiap artikel wajib punya **sumber dan timestamp terbit**. Artikel tanpa timestamp tidak dipakai. Fitur untuk origin `t` hanya dari artikel terbit ≤ `t`.
2. Raw (indeks dan halaman) disimpan byte-identik dengan sha256 dan tidak pernah ditimpa.
3. **Teks penuh artikel tidak dikoleksi** (hak cipta media); yang dikoleksi cukup metadata dan judul. Data hasil koleksi juga tidak di-commit.
4. Dummy news dari notebook lama dilarang dipakai.
5. Filter relevansi di collection layer berupa aturan kata kunci yang transparan. Model sentimen dan relevansi masuk Phase 3, dan model aktual (termasuk fallback) wajib dicatat.
6. Search page yang di-Disallow `robots.txt` tidak dipakai; arsip diambil lewat halaman indeks per tanggal, dengan jeda sopan.
