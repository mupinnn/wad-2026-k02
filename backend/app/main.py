from contextlib import asynccontextmanager
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.response import success_response, error_response

from app.schemas import (
    Consultation,
    ConsultationCreate,
    ErrorResponse,
    HealthResponse,
    SuccessResponse,
)
from app.services import (
    create_consultation,
    delete_consultation,
    get_consultation,
    list_consultations,
)
from app.routers.auth import router as auth_router
from app.seed import seed


BACKEND_DIR = Path(__file__).resolve().parents[1]


def run_migrations() -> None:
    # Config() tanpa file .ini supaya env.py tidak memanggil fileConfig
    # (yang mematikan logger uvicorn). URL database diatur env.py dari .env.
    cfg = Config()
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    command.upgrade(cfg, "head")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    run_migrations()
    seed()
    yield


app = FastAPI(title="Jadwal Konsultasi Klinik", lifespan=lifespan)

# B5: izinkan hanya origin frontend. Jangan menambah origin lain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get("/consultations", response_model=SuccessResponse[list[Consultation]])
def get_consultations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=5, ge=1, le=100),
    search: str | None = Query(default=None),
):
    return list_consultations(skip=skip, limit=limit, search=search)


@app.get(
    "/consultations/{id}",
    response_model=SuccessResponse[Consultation],
    responses={404: {"model": ErrorResponse}},
)
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


@app.get("/health", response_model=HealthResponse)
def get_health():
    return {"status": "ok"}


@app.post(
    "/consultations",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[Consultation],
)
def post_consultation(payload: ConsultationCreate):
    new_consultation = create_consultation(payload)
    return success_response("Konsultasi berhasil ditambahkan", new_consultation)


@app.delete(
    "/consultations/{id}",
    response_model=SuccessResponse[Consultation],
    responses={404: {"model": ErrorResponse}},
)
def delete_consultations(id: int):
    deleted_consultation = delete_consultation(id)

    if deleted_consultation is None:
        return JSONResponse(
            status_code=404,
            content=error_response("Konsultasi tidak ditemukan"),
        )

    return success_response("Konsultasi berhasil dihapus", deleted_consultation)