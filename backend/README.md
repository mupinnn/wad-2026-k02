# backend/

FastAPI untuk jadwal konsultasi pasien (Kelompok 02). Route konsultasi belum ada. Kontrak yang harus diikuti ada di [`docs/uts-consultation-contract.md`](../docs/uts-consultation-contract.md).

```
backend/
├── alembic.ini
├── alembic/          # migrasi tabel users dan consultations
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py       # FastAPI, GET /health, CORS untuk http://localhost:5173
    ├── config.py     # DATABASE_URL dan kredensial seed dari .env root repo
    ├── database.py   # engine SQLite dan get_db
    ├── models.py     # tabel users dan consultations
    ├── seed.py       # admin, pengguna opsional, dan 12 jadwal
    ├── data.py       # 12 jadwal fiktif (sumber seed; API masih membaca daftar ini)
    ├── schemas.py    # skema Pydantic — ditambah pemilik endpoint
    └── services.py   # operasi data — ditambah pemilik endpoint
```

Jalankan dari folder ini:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

`venv/` tidak di-commit.

## Basis data

Route konsultasi masih memakai daftar di `app/data.py`. Tabel SQLAlchemy siap dipakai tugas login dan kepemilikan jadwal.

Isi `.env` di **root repo** (bukan di folder ini). Jangan commit `.env`. `SECRET_KEY` belum dipakai seeder.

```
ADMIN_EMAIL=admin@klinik.test
ADMIN_PASSWORD=ganti-dengan-kata-sandi-lokal
# opsional, supaya ada satu role user sebelum register ada
USER_EMAIL=petugas@klinik.test
USER_PASSWORD=ganti-dengan-kata-sandi-lokal
```

Dari folder `backend/`:

```bash
alembic upgrade head
python -m app.seed
```

Perintah seed boleh dijalankan ulang. Admin dibuat hanya jika email itu belum ada. Dua belas jadwal disalin sekali, selama tabel `consultations` masih kosong, dan `user_id`-nya adalah admin. Kalau `ADMIN_EMAIL` atau `ADMIN_PASSWORD` kosong, seed berhenti dan tidak membuat kata sandi sendiri.
