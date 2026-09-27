# backend/

FastAPI untuk jadwal konsultasi pasien (Kelompok 02). Route konsultasi belum ada. Kontrak yang harus diikuti ada di [`docs/uts-consultation-contract.md`](../docs/uts-consultation-contract.md).

```
backend/
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py       # FastAPI, GET /health, CORS untuk http://localhost:5173
    ├── data.py       # 12 jadwal fiktif
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
