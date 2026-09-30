from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.response import success_response, error_response

from app.schemas import Consultation, ConsultationCreate
from app.services import (
    create_consultation,
    delete_consultation,
    get_consultation,
    list_consultations,
)


app = FastAPI(title="Jadwal Konsultasi Klinik")

# B5: izinkan hanya origin frontend. Jangan menambah origin lain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/consultations")
def get_consultations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=5, ge=1, le=100),
    search: str | None = Query(default=None),
):
    return list_consultations(skip=skip, limit=limit, search=search)


@app.get("/consultations/{id}", response_model=Consultation)
def get_consultation_by_id(id: int):
    consultation = get_consultation(id)

    if consultation is None:
        return JSONResponse(
            status_code=404,
            content=error_response(
                "Konsultasi tidak ditemukan"
            )
        )

    return success_response(
            "Konsultasi ditemukan",
            consultation
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
