# ARIF-Net PIHPS Collection — Phase 1

Paket collection harga PIHPS dengan Conda + Python 3.13.

## Quick start (Windows CMD)

```cmd
conda env create -f environment.yml
conda activate arifnet-pihps
python --version
python -m pip install -r requirements.txt
python -m py_compile scripts\collect_pihps_arifnet.py
```

### Smoke test

```cmd
python scripts\collect_pihps_arifnet.py --start-date 2022-01-01 --end-date 2022-01-31 --chunk-months 1 --delay 0.75
```

### Full collection

```cmd
python scripts\collect_pihps_arifnet.py --start-date 2022-01-01 --end-date 2026-09-29 --chunk-months 1 --delay 0.75
```

Dokumentasi lengkap: `docs/PHASE1_COLLECTION_PIHPS.md`.
