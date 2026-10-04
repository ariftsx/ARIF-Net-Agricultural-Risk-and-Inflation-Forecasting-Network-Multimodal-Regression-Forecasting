# Phase 1 — Koleksi News: Analisis, Probe Kelayakan, dan Decision Gate

**Otoritas:** Implementation Plan v2.0.0 (§4.1 modality 3, §8 Group 3, §9 Data Contract, §9.2, §10.4, §12.1 Sentiment, §22, §37 risk register, §36 DG-09) → Phase 0 Research Contract v2.1.0 (§2.2 information availability, §5.1 master matrix, §5.3 News, §18.3, §19 News checklist, §21 GDELT, DG-04, DG-10).
**Status (3 Okt 2026): Probe & verifikasi pola URL SELESAI. P1-DG-25…30 DIPUTUSKAN. Berikutnya: rencana collector (disetujui peneliti) → codebase → smoke → full.**

---

## 1. Ketentuan dari dokumen otoritas (wajib dipatuhi)

| Aspek | Ketentuan | Rujukan |
|---|---|---|
| Status modality | News/sentiment adalah modality eksternal inti | Plan DG-09 `LOCKED DIRECTION`; Contract DG-10 `DECIDED` |
| Cakupan topik | Berita terkait **pangan, harga, inflasi, cuaca, supply, BBM/logistik** | Plan §4.1 |
| Sumber kandidat | "GDELT / sumber berita yang relevan"; GDELT disebut kandidat kuat | Contract §5.1, §5.3, §21 |
| Aturan waktu | Fitur untuk origin `t` hanya dari artikel **terbit ≤ cutoff `t`**; future realized news dilarang | Contract §2.2, §5.1; Plan §9.1–9.2 |
| Timestamp | Wajib ada **publication/availability timestamp** per artikel | Plan §9, §10.4; Contract §19, DG-04 |
| Pipeline | raw → source + publication timestamp → dedup → topic/relevance filter → normalisasi teks → model sentimen → skor artikel → agregasi harian → temporal cutoff | Plan §10.4 |
| Fitur (Phase 3) | Bukan hanya `sentiment_mean`: volume, keseimbangan positif/negatif, intensity, persistence, recency, topic relevance, source count, event burst, negative ratio | Contract §5.3, §18.3; Plan §8, §12.1 |
| Provenance model | Model sentimen yang benar-benar dipakai **wajib dicatat**, termasuk fallback lexicon | Plan §10.4, §37 |
| Data dummy | Dummy news dari notebook lama **dilarang** dipakai sebagai data penelitian | Plan §22 |
| Checklist audit | Sumber dapat dilacak · artikel relevan · publication time tersedia · model sentimen & fallback tercatat · agregasi tanpa berita masa depan | Contract §19 |
| Risiko | Data news lemah/berisik, dimitigasi dengan provenance + relevance filter | Plan §37 |

**Batas tahap:** collection layer (folder ini) hanya mengumpulkan **artikel mentah, metadata, dan timestamp**, lalu menormalisasi, dedup, dan memberi relevance flag berbasis aturan. **Skor sentimen, agregasi harian, dan fitur adalah Phase 3**, sama seperti aturan t−5 iklim yang diterapkan di feature layer.

## 2. Hasil probe kelayakan (Langkah 0, read-only, 3 Okt 2026)

Bukti mentah ada di `data/raw/news/probe/` (byte-identik), laporan di `reports/probe_*.json`, dan script di `scripts/probe_*.py`. **Tidak ada artikel yang dikoleksi.**

### 2a. GDELT
| Jalur | Hasil probe | Implikasi |
|---|---|---|
| DOC 2.0 API (`api.gdeltproject.org/api/v2/doc/doc`) | **HTTP 429 pada ke-7 request**, termasuk request pertama dan retry tunggal setelah 90 detik. Pesan: *"Please limit requests to one every 5 seconds … high-traffic users should switch to our ngrams dataset"* | Dari jaringan ini API ditolak konsisten (kemungkinan pembatasan IP). **Tidak bisa diandalkan** tanpa jaringan lain atau izin dari GDELT |
| File mentah GDELT 2.0 (`data.gdeltproject.org/gdeltv2/masterfilelist.txt`) | HTTP 200/206; file GKG per 15 menit tersedia **2015-02-18 → 2026-10-03** | Data ada, tetapi **±3–11 MB per file × ±270 ribu file (2019–2026) ≈ 1 TB** ter-kompres. Tidak realistis diunduh di laptop |
| Google BigQuery (`gdelt-bq`) | Tidak diprobe (butuh akun Google Cloud) | Jalur historis GDELT paling realistis: filter `SourceCommonName` media Indonesia dan tema di server |
| Catatan isi | GDELT **tidak menyimpan teks penuh**: hanya URL, judul (GKG Extras), tema, tone (lexicon atas terjemahan mesin), lokasi | Tone GDELT ≠ IndoBERT. Untuk sentimen bahasa Indonesia tetap perlu judul/teks asli |

### 2b. Portal media Indonesia (`robots.txt`, sitemap, indeks per tanggal 2019-01-02)
| Portal | robots.txt (User-agent *) | Sitemap | Indeks arsip 2019-01-02 |
|---|---|---|---|
| Kompas | Disallow `/search/?q=` (search dilarang) | Hanya terkini | **Tersedia**: `indeks.kompas.com/?site=all&date=…`, 20 tautan artikel 2019-01-02 di halaman 1 |
| Detik | Tidak ada disallow | `sitemap_news` (terkini) | **Tersedia**: `news.detik.com/indeks?date=MM/DD/YYYY`, 18 tautan |
| CNN Indonesia | Tidak ada disallow | Terkini | **Tersedia**: `cnnindonesia.com/indeks?date=YYYY/MM/DD`, 10 tautan |
| CNBC Indonesia | Tidak ada disallow | `sitemap_news` per kanal | **Tersedia**: `cnbcindonesia.com/indeks?date=YYYY/MM/DD`, 10 tautan |
| Kontan | Tidak ada disallow | Terkini | **Tersedia**: `kontan.co.id/search/indeks?tanggal=&bulan=&tahun=`, 38 tautan |
| Antara | Disallow `/ajax/*` | Tidak dicantumkan | **Belum terverifikasi**: pola URL yang dicoba → 404. Butuh tangkapan DevTools |
| Katadata | Tidak ada disallow | **Sitemap bulanan `sitemap/post/YYYY-MM.xml`**, tertua **2021-01** | Tidak menjangkau 2019–2020 |
| Bisnis.com | Disallow beberapa path (feed, rss) | **HTTP 403** | Diblokir untuk akses otomatis |
| Tempo | Tidak ada disallow | Tidak dicantumkan | **HTTP 403** pada halaman indeks |
| Liputan6, Republika | Disallow `/search` | Ada per kanal | Tidak diprobe |
| Okezone | Disallow beberapa path | Ada | Tidak diprobe |
| beritajakarta.id (Pemprov DKI) | Koneksi gagal | — | — |
| badanpangan.go.id (Bapanas) | robots.txt 404 | — | — |

**Catatan:** pola URL indeks di atas adalah pola publik yang terbukti merespons. Pola ini **tetap harus dikonfirmasi peneliti lewat DevTools** (pagination, parameter kanal) sebelum koleksi, sama seperti proses PIHPS/PIBC/IPJ. Ketentuan penggunaan (ToS) setiap media juga harus dicatat peneliti.

## 3. Rekomendasi sumber (untuk decision gate)

> **SUPERSEDED BY P1-DG-25 (2026-10-03):** sumber tetap = Kompas, Detik, CNN Indonesia, CNBC Indonesia, Kontan (lihat §3a, §5). Tabel di bawah dipertahankan untuk keterlacakan analisis.

| # | Sumber | Tipe | Kekuatan untuk ARIF-Net | Jalur histori 2019 (bukti) | Risiko / catatan | Saran |
|---|---|---|---|---|---|---|
| 1 | **Kompas.com** | Nasional umum | Media nasional terbesar; banyak liputan harga pangan Jakarta | Indeks per tanggal ✅ | Search di-Disallow → wajib lewat indeks; volume besar per hari | **Utama** |
| 2 | **Detik.com** (detikNews/detikFinance) | Nasional umum + ekonomi | Volume sangat besar; liputan harian pasar dan harga | Indeks per tanggal ✅ | Volume tinggi, perlu filter kanal dan kata kunci | **Utama** |
| 3 | **CNBC Indonesia** | Ekonomi/pasar | Fokus komoditas, inflasi, kebijakan pangan; cocok untuk topic relevance | Indeks per tanggal ✅ | Sebagian konten pasar keuangan (perlu relevance filter) | **Utama** |
| 4 | **Kontan** | Ekonomi/bisnis | Liputan komoditas, Bulog, Bapanas, harga di pasar induk | Indeks per tanggal ✅ | — | **Utama** |
| 5 | **Antara News** | Kantor berita negara | Rujukan resmi, liputan daerah (sentra produksi), banyak dikutip | Belum terverifikasi ⚠️ | Butuh DevTools untuk pola indeks | **Utama bila indeks terkonfirmasi** |
| 6 | CNN Indonesia | Nasional umum | Liputan nasional | Indeks per tanggal ✅ | Tumpang tindih dengan Kompas/Detik | Cadangan |
| 7 | Katadata | Ekonomi berbasis data | Analisis harga & inflasi | Sitemap mulai 2021-01 ❌ untuk 2019–2020 | Tidak menjangkau 2019–2020 | Cadangan (2021+) |
| 8 | Bisnis.com | Ekonomi | Liputan komoditas | 403 ❌ | Diblokir akses otomatis | Tidak disarankan |
| 9 | Tempo | Nasional | Investigatif | 403 ❌ | Diblokir; sebagian berbayar | Tidak disarankan |
| 10 | Liputan6 / Republika / Okezone | Nasional umum | Volume besar | Belum diprobe | Search di-Disallow (Liputan6, Republika) | Opsional |
| 11 | **GDELT (via BigQuery)** | Agregator global | Disebut kontrak; volume/intensity/tone lintas media; timestamp terstandar | GKG 2015+ ✅ (via BigQuery) | DOC API 429 dari jaringan ini; butuh akun GCP; tone ≠ IndoBERT | **Pelengkap sistematis** (fitur volume/intensity) bila GCP tersedia |
| 12 | Rilis resmi (Bapanas, BI, Kementan, Pemprov DKI) | Pemerintah | Pengumuman kebijakan (operasi pasar, HET, impor) | Belum diprobe | Format beragam; bukan media berita | Opsional (event kebijakan) |

**Usulan konfigurasi:**
- **Inti:** Kompas, Detik, CNBC Indonesia, dan Kontan; keempatnya punya arsip 2019 yang terbukti. Antara ditambahkan kalau pola indeksnya terkonfirmasi.
- **Pelengkap:** GDELT via BigQuery, kalau Anda punya akun Google Cloud. Perannya sebagai fitur volume dan intensity lintas media, sesuai rujukan kontrak (Theofilou et al. 2026).
- **Alasan:** kombinasi media umum (Kompas, Detik) dan media ekonomi (CNBC, Kontan) memberi keragaman sumber (*source count*) dan liputan komoditas yang rinci, sementara teks bahasa Indonesianya cocok untuk IndoBERT di Phase 3.

## 3a. Sumber tetap & panduan tangkapan DevTools (P1-DG-25)

Untuk **setiap** media di bawah, buka Chrome → F12 → tab **Network**, centang **Preserve log**, filter **Doc** dan **Fetch/XHR**, lalu buka URL berikut. Untuk setiap request utama, salin: **Request URL, Request Method, Status Code, Query String Parameters**, dan **potongan Response** (tab *Response*/*Preview*), sama seperti tangkapan PIBC/IPJ. Cookie **tidak perlu** disalin.

| # | Media | (A) Indeks 1 tanggal | (B) Halaman ke-2 indeks yang sama | (C) Kanal ekonomi (bila ada) | (D) 1 halaman artikel |
|---|---|---|---|---|---|
| 1 | **Kompas** | `https://indeks.kompas.com/?site=all&date=2019-01-02` | Klik halaman **2** di bawah daftar | Pilih kanal **Money** di filter indeks (catat parameternya, mis. `site=money`) | Klik 1 artikel dari daftar |
| 2 | **Detik** | `https://news.detik.com/indeks?date=01/02/2019` | Klik halaman **2** | Buka `https://finance.detik.com/indeks` lalu pilih tanggal 02/01/2019 | Klik 1 artikel |
| 3 | **CNN Indonesia** | `https://www.cnnindonesia.com/indeks?date=2019/01/02` | Klik halaman **2** / "selanjutnya" | Pilih kanal **Ekonomi** di indeks (catat parameternya) | Klik 1 artikel |
| 4 | **CNBC Indonesia** | `https://www.cnbcindonesia.com/indeks?date=2019/01/02` | Klik halaman **2** | Pilih kanal **News** atau **Market** di indeks (catat parameternya) | Klik 1 artikel |
| 5 | **Kontan** | `https://www.kontan.co.id/search/indeks?kanal=&tanggal=2&bulan=01&tahun=2019` | Klik halaman **2** | Pilih kanal (mis. **Industri/Keuangan**) di form indeks | Klik 1 artikel |

**Yang paling penting di setiap tangkapan:**
1. **(A)/(B):** apakah daftar artikel ada di HTML (request *Doc*), atau dimuat lewat request **XHR/Fetch** terpisah (mis. tombol "Muat lebih banyak"/scroll). Kalau lewat XHR, salin request XHR-nya.
2. **(B):** parameter pagination (mis. `page=2`, `/2`, `p=2`) dan total halaman yang terlihat.
3. **(D):** letak **waktu terbit**. Di *Response* halaman artikel, cari `article:published_time`, `datePublished`, atau `pubdate`, lalu salin baris tersebut (Contract §19 mewajibkan publication time).
4. **ToS:** tautan halaman "Pedoman Media Siber" / "Syarat & Ketentuan" setiap media, untuk dicatat di provenance.

### 3b. Pola URL terverifikasi per media

| Media | Indeks per tanggal | Pagination | Kanal ekonomi | Waktu terbit | Status |
|---|---|---|---|---|---|
| **Kompas** | `https://indeks.kompas.com/?site=all&date=YYYY-MM-DD` | `&page=N` (20 artikel/halaman; total halaman tidak tertulis → iterasi sampai kosong) | `site=money` (artikel `money.kompas.com` + `ekonomi.kompas.com`) | `<meta property="article:published_time">` dalam **UTC (+00:00)**; JSON-LD `datePublished` dalam **+07:00**; URL `/read/YYYY/MM/DD/HHMM…` = WIB. **Collector wajib menyimpan waktu dalam WIB** | ✅ **Terverifikasi 2026-10-03**: tangkapan peneliti (`?page=2`, meta UTC) + `scripts/verify_kompas.py` (2019-01-02: p1 20, p2 20, overlap 0; money 20; artikel 2019 meta 06:30Z = 13:30 WIB). Tangkapan peneliti ke-2 (2026-10-01): `?site=all&date=2026-10-01`, `&page=2`, `?site=money&date=2026-10-01`, artikel `/read/2026/10/01/224959226/` meta `15:49:59+00:00` = 22:49:59 WIB → pola berlaku di **kedua ujung periode (2019 & 2026)** |
| **Detik** | `https://news.detik.com/indeks?date=MM%2FDD%2FYYYY` | `&page=N` (2019-01-02: 18 halaman, ±20 artikel/halaman). **Tanggal WAJIB di-URL-encode (`%2F`)**: dengan `/` biasa, server mengembalikan halaman 1 untuk semua `page` | `https://finance.detik.com/indeks?date=…` (20 artikel 2019-01-02) | JSON-LD `datePublished` **+07:00** (WIB) | ✅ Terverifikasi (tangkapan peneliti + `scripts/verify_media.py` + uji `p2_encoded`) |
| **CNN Indonesia** | `https://www.cnnindonesia.com/indeks/?date=YYYY/MM/DD` | `/indeks/2?date=…&page=2` (10 artikel/halaman; p1∩p2 = 0) | `https://www.cnnindonesia.com/ekonomi/indeks/5?date=…` (10 artikel) | JSON-LD `datePublished` **+07:00**. ⚠️ Angka di URL (`20181231204448-…`) **bukan** waktu terbit (contoh peneliti: URL 2018-12-31 20:44, terbit 2019-01-01 23:15) → pakai `datePublished` | ✅ Terverifikasi |
| **CNBC Indonesia** | `https://www.cnbcindonesia.com/indeks?date=YYYY/MM/DD&tipe=` | `&page=N` (10/halaman; p1∩p2 = 0) | `…/mymoney/indeks/71?date=…` (6 artikel; kanal *MyMoney*/keuangan pribadi) | JSON-LD `datePublished` **+07:00**. ⚠️ Angka di URL bukan waktu terbit (contoh: URL 18:14, terbit 19:54) | ✅ Terverifikasi |
| **Kontan** | `https://www.kontan.co.id/search/indeks?kanal=&tanggal=D&bulan=MM&tahun=YYYY` | `&pos=indeks&per_page=20,40,60…` (offset kelipatan 20) | `kanal=` (pilih nilai kanal) | **Di halaman indeks**: `Rabu, 02 Januari 2019 \| 21:10 WIB`. ⚠️ **Halaman artikel 403 untuk script**, sehingga hanya judul + waktu dari indeks (tanpa teks) | ⚠️ Indeks OK, artikel diblokir |
| **Liputan6** *(baru)* | `https://www.liputan6.com/indeks/YYYY/MM/DD?start=…&end=…` | `&page=N` (24/halaman) | `https://www.liputan6.com/bisnis/indeks/YYYY/MM/DD` (24 artikel) | `article:published_time` & JSON-LD **+07:00** | ✅ Terverifikasi (sebelumnya "belum diprobe") |
| **Katadata** *(tangkapan peneliti)* | `https://katadata.co.id/indeks/search/{kanal\|-}/DD-MM-YYYY/DD-MM-YYYY` | ⚠️ Tidak ada halaman 2; tombol **"Tampilkan lebih banyak"** = request **XHR** (belum ditangkap) | `/indeks/search/4/…` (kanal finansial) | JSON-LD `+07:00`; meta tanpa zona waktu | ⚠️ Butuh tangkapan XHR "Tampilkan lebih banyak" |
| **Bisnis.com** *(tangkapan peneliti)* | `https://www.bisnis.com/index?categoryId=0&type=indeks&date=YYYY-MM-DD` | ❌ Tidak ada pagination: hanya ±40 artikel/hari (cakupan tidak lengkap) | `categoryId=43` | Di indeks: `02 Jan 2019 \| 23:36 WIB`. ❌ Halaman artikel = tantangan Cloudflare ("Just a moment…") | ❌ Tidak disarankan |
| **Tempo** *(tangkapan peneliti)* | `https://www.tempo.co/indeks?page=N&start_date=…&end_date=…` | `page=N` | `rubric_slug=ekonomi` | ❌ Meta `article:published_time` = **"null WIB"** | ❌ **HTTP 403 untuk script** (hanya terbuka di browser) |

## 3c. Hasil smoke (2026-10-03; tanggal uji 2019-01-02 & 2026-09-15)

| Media | Halaman/hari (2019 / 2026) | Artikel/hari (2019 / 2026) | Waktu terbit artikel relevan | Status |
|---|---|---|---|---|
| Kompas | 23 / 53 | 424 / 1.016 | 33/33 (dari URL, detik) | ✅ |
| detikNews | 3 / 3 (hanya 20 artikel) | ⚠️ tidak lengkap | — | ❌ **Pagination tidak stabil dari script**: `page=N` kadang mengembalikan halaman sama (cache CDN); uji header `Accept-Encoding` & cache-buster `_=` tetap tidak konsisten (`reports/debug_detik_*.json`) |
| detikFinance | 6 / 5 | 91 / 80 | 13/13 (indeks, menit) | ✅ Konsisten di 2 smoke |
| CNN Indonesia | 22 / 34 | 207 / 330 | 9/10 (1 artikel kanal Teknologi tanpa JSON-LD) | ✅ (setelah perbaikan URL `/indeks/2?…&page=N`) |
| CNBC Indonesia | 19 / 27 | 178 / 256 | 18/18 (JSON-LD) | ✅ |
| Kontan | 11 / 19 | 195 / 343 | 6/6 (tanggal saja) | ✅ |
| Liputan6 | 6 / 4 | 90 / 51 | 5/5 (indeks, detik) | ✅ |

- **Perbaikan setelah smoke-1:** pola URL Detik (`?date=…&page=N`) dan CNN (`/indeks/2?…`). Stop rule menjadi "2 halaman berturut-turut tanpa artikel baru". `run_id` ditambahkan di manifest. Manifest smoke-1 diarsipkan sebagai `*_smoke1.csv` (tidak dihapus).
- **Konsistensi waktu:** 0 artikel relevan dengan tanggal terbit ≠ tanggal indeks.
- **Relevansi:** kata kunci luas (mis. "panen", "banjir", "pertalite", "el nino") juga menangkap berita di luar pangan (mis. "Panen Garam", "DBD saat El Nino"). Kolom `topics_matched` memungkinkan penyaringan di Phase 3. Semua judul disimpan lokal (`articles_all.csv.gz`), sehingga **kata kunci bisa diperketat kemudian tanpa scraping ulang**.
- **Estimasi full (median halaman/hari × 2.830 hari):** Kompas ±38 → ±107 ribu request; CNN ±28 → ±79 ribu; CNBC ±23 → ±65 ribu; Kontan ±15 → ±42 ribu; detikFinance ±5,5 → ±16 ribu; Liputan6 ±5 → ±14 ribu. **Total ±325 ribu request indeks**, dengan raw lokal ±11–12 GB (gzip). Dengan jeda 1,5 detik per media secara paralel, bottleneck Kompas **±2,5–3 hari** waktu jalan.

## 3d. Rencana eksekusi full (keputusan peneliti 2026-10-03)

**Yang dikumpulkan:** judul, waktu terbit (WIB), media/kanal, dan URL dari **semua** berita di indeks (dibutuhkan sebagai penyebut volume harian), **tanpa isi berita** (P1-DG-29). Untuk CNN dan CNBC, halaman artikel dibuka **hanya** untuk membaca waktu terbit artikel relevan. Setiap judul diberi penanda `topics_matched` (7 kelompok P1-DG-27), `keywords_matched`, dan **`wilayah_pemasok`** (kabupaten dari 18 wilayah P1-DG-11 yang disebut di judul; P1-DG-31).

| Estimasi (dari smoke) | Nilai |
|---|---|
| Total judul | ±4,6 juta (Kompas ±2,04 jt · CNN ±760 rb · Kontan ±760 rb · CNBC ±615 rb · detikFinance ±240 rb · Liputan6 ±200 rb) |
| Judul relevan | ±120 ribu |
| Request | ±365 ribu (indeks ±325 rb + waktu terbit CNN/CNBC ±39 rb) |
| Raw lokal | ±11–12 GB (gzip), **tetap di folder proyek/OneDrive** (keputusan peneliti; WARN di verify_setup) |

**93 fase kecil (revisi peneliti 2026-10-03, pilihan A):** 1 fase = **1 bulan data**, 6 media paralel, **±40–60 menit per fase** (2019 lebih ringan, 2026 lebih berat karena volume Kompas naik). Total waktu mesin tetap ±65–70 jam, tetapi terbagi menjadi sesi pendek. Laptop hanya perlu menyala **selama fase berjalan**.

```cmd
cd "<repo>\ARIF-Net_Collection_Data(Data_Mining)\News"
conda run -n arif-net --no-capture-output python scripts\run_phase.py --month 2019-01 --max-minutes 60
```

`--max-minutes 60` adalah batas pengaman. Kalau satu bulan belum selesai dalam 60 menit, koleksi berhenti rapi, dan perintah yang sama melanjutkannya.

| Tahun | Fase (bulan) | Selesai |
|---|---|---|
| 2019 | 01–12 | 0/12 |
| 2020 | 01–12 | 0/12 |
| 2021 | 01–12 | 0/12 |
| 2022 | 01–12 | 0/12 |
| 2023 | 01–12 | 0/12 |
| 2024 | 01–12 | 0/12 |
| 2025 | 01–12 | 0/12 |
| 2026 | 01–09 | 0/9 |

Setiap fase menghasilkan `reports/phase_<YYYY-MM>.json` (OK/FLAG/FAIL per media) dan memperbarui normalisasi serta audit kumulatif. Fase bisa dihentikan kapan saja; jalankan ulang perintah yang sama untuk melanjutkan. Kata kunci yang terlalu luas **diperketat di Phase 3**.

## 4. Rancangan pipeline koleksi (dibangun setelah decision gate)

```text
Indeks per tanggal (per portal, per halaman)  ──► raw HTML/JSON byte-identik + sha256 (manifest, resume)
        ↓  parse daftar artikel: url, judul, waktu tayang, kanal
Filter kata kunci pada JUDUL (+ kanal)         ──► kandidat relevan (aturan transparan, bukan model)
        ↓  ambil halaman artikel kandidat saja (jeda sopan)
Artikel: judul, waktu terbit (WIB), penulis/kanal, teks   ──► teks penuh disimpan LOKAL (tidak di-commit; hak cipta)
        ↓
Tabel artikel ter-normalisasi + dedup (URL kanonik, judul mirip)  ──► data/processed/news/articles.csv (LFS)
        ↓
Audit: volume/hari per sumber & topik, hari tanpa berita, sebaran waktu tayang, artikel tanpa timestamp
```

**Skema rencana `articles.csv`:** `article_id` (sha1 URL kanonik), `source`, `url`, `title`, `published_at_wib`, `collected_at_utc`, `channel`, `topics_matched`, `keywords_matched`, `is_relevant_rule`, `has_fulltext_local`, `raw_index_file`, `raw_article_sha256`.
**Aturan waktu:** `available_at = published_at` untuk berita online. Artikel tanpa timestamp terbit **tidak dipakai** (Contract §19).

**Estimasi beban:** ±2.830 hari × (1–20 halaman indeks per portal per hari), ditambah halaman artikel kandidat. Dengan jeda 1–2 detik, satu portal butuh **beberapa jam sampai belasan jam**. Opsi untuk mengurangi beban adalah membatasi ke kanal ekonomi/berita (decision gate N-4).

## 5. Decision gate

| ID | Pertanyaan | Status | Isi |
|---|---|---|---|
| **P1-DG-25** | Sumber tetap news | **DECIDED (revisi 2026-10-03)** | **Kompas, Detik, CNN Indonesia, CNBC Indonesia, Kontan, Liputan6**. Dikeluarkan: Katadata (pagination XHR belum terverifikasi), Bisnis.com (±40/hari tanpa pagination + Cloudflare), Tempo (403 + waktu "null WIB"), Antara, GDELT, Okezone/Republika, rilis resmi |
| **P1-DG-26** | Periode | **DECIDED** | **2019-01-01 → 2026-09-30** |
| **P1-DG-27** | Topik & kata kunci | **DECIDED** | Sesuai draf `config/news_scope_DRAFT.json` → `topics` (7 kelompok) |
| **P1-DG-28** | Cakupan kanal | **DECIDED** | Semua kanal (indeks umum tiap media) + filter kata kunci pada judul |
| **P1-DG-29** | Teks penuh | **DECIDED** | **Tidak**: hanya judul + waktu terbit + metadata |
| **P1-DG-30** | Aturan relevansi | **DECIDED** | Kata kunci (case-insensitive) pada judul |
| — | Model sentimen | Phase 3 | Kandidat IndoBERT; model aktual dan fallback wajib dicatat |

**Catatan keragaman sumber:** Detik, CNN Indonesia, dan CNBC Indonesia berada dalam satu grup media (Trans Media / CT Corp). Untuk fitur *source count* (Contract §5.3), kelima sumber tetap dihitung sebagai media terpisah, tetapi keterbatasan ini dicatat di Limitations.

## 6. Kebutuhan dari peneliti

1. **Tangkapan DevTools** 5 media sesuai tabel §3a (A–D).
2. **Keputusan P1-DG-27…30**: kata kunci, kanal, teks penuh, aturan relevansi (§5).
3. **Tautan ToS / pedoman media** kelima sumber.
4. **Izin memasang `beautifulsoup4` dan `lxml`** ke env `arif-net` (parse HTML).
5. (Opsional) data berita **nyata** dari repo lama sebagai pembanding. Dummy tidak dipakai.

## 7. Log

| Tanggal | Kegiatan | Hasil |
|---|---|---|
| 2026-10-03 | Analisis Plan v2.0.0 & Contract v2.1.0 bagian news | §1 |
| 2026-10-03 | Probe GDELT DOC API (7 request) + file mentah GDELT (2 request) | DOC API 429 konsisten; file mentah tersedia tetapi ±1 TB |
| 2026-10-03 | Probe robots.txt 14 kandidat, sitemap 12, indeks 2019-01-02 6 portal | §2b |
| 2026-10-03 | Keputusan peneliti: P1-DG-25 (sumber hanya yang terbukti: Kompas, Detik, CNN Indonesia, CNBC Indonesia, Kontan) & P1-DG-26 (periode 2019-01-01 → 2026-09-30) | §5; `config/news_scope_DRAFT.json` |
| 2026-10-03 | Analisis tangkapan peneliti (8 media) + `scripts/verify_media.py` (uji dari script, tanggal 2019-01-02) | §3b: Detik/CNN/CNBC/Liputan6 ✅; Kontan indeks ✅ artikel 403; Katadata butuh XHR; Bisnis & Tempo ❌ |
| 2026-10-03 | Keputusan peneliti: P1-DG-25 revisi (+Liputan6; −Katadata, Bisnis, Tempo), P1-DG-27…30 sesuai saran | §5 |
| 2026-10-03 | `beautifulsoup4` 4.15.0 & `lxml` 6.1.1 dipasang ke env `arif-net` (izin peneliti) | — |
| 2026-10-03 | Tahap A: codebase collector (sources.json, common, parsers 6 media, collect_index, collect_articles, index_items, normalize_news, audit_news, verify_setup) + 11 test offline (fixture HTML probe) PASS; verify_setup PASS | `scripts/`, `tests/` |
| 2026-10-03 | Smoke-1 (FAIL CNN 404, detikNews p1=p2) → perbaikan URL + stop rule + run_id; smoke-2 PASS kecuali detikNews tidak stabil; Tahap 2, normalisasi, audit PASS | §3c |
| 2026-10-03 | Keputusan peneliti (CP2): Detik = **detikFinance saja**; detikNews dikeluarkan (pagination tidak stabil) | `config/sources.json` |
| 2026-10-03 | Keputusan peneliti: eksekusi pilihan B (8 fase/tahun, dijalankan peneliti), kolom `wilayah_pemasok` (P1-DG-31), kata kunci diperketat di Phase 3, raw tetap di OneDrive | §3d |
| 2026-10-03 | Revisi peneliti: eksekusi **pilihan A**, yaitu 93 fase × 1 bulan (±40–60 menit), karena laptop tidak bisa dibiarkan berjam-jam | §3d |
| 2026-10-04 | Keputusan peneliti: **Kompas dibatasi** ke `site=news` (nasional, megapolitan, regional, internasional) + `site=money` (money, ekonomi); bukti smoke 67% artikel, 91% artikel relevan; estimasi total waktu turun ±66 → ±48 jam | `config/sources.json` |
