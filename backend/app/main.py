from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.response import success_response, error_response
from app.schemas import ConsultationCreate
from app.services import create_consultation, delete_consultation

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


@app.post("/consultations", status_code=status.HTTP_201_CREATED)
def post_consultation(payload: ConsultationCreate):
    new_consultation = create_consultation(payload)
    return success_response("Konsultasi berhasil ditambahkan", new_consultation)


@app.delete("/consultations/{id}")
def delete_consultations(id: int):
    deleted_consultation = delete_consultation(id)

    if deleted_consultation is None:
        return JSONResponse(
            status_code=404,
            content=error_response("Konsultasi tidak ditemukan"),
        )

    return success_response("Konsultasi berhasil dihapus", deleted_consultation)