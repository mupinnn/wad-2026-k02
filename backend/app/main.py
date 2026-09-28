from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.data import CONSULTATIONS
from app.response import success_response, error_response
from app.services import (delete_consultation)


app = FastAPI(title="Jadwal Konsultasi Klinik")

# B5: izinkan hanya origin frontend. Jangan menambah origin lain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def get_health():
    return {"status": "ok"}


# delete consultation
@app.delete("/consultations/{id}")
def delete_consultations(id: int):
    deleted_consultation = delete_consultation(id)

    if deleted_consultation is None:
        return JSONResponse(
            status_code=404,
            content=error_response(
                "Konsultasi tidak ditemukan"
            )
        )

    return success_response(
        "Konsultasi berhasil dihapus",
        deleted_consultation
    )