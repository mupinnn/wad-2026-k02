from fastapi import FastAPI,Header ,HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Depends, Query

from app.response import success_response, error_response
from app.routers import users

from sqlalchemy.orm import Session
from app.database import get_db

from sqlalchemy import select
from app.models import User

from app.schemas import (
    Consultation,
    ConsultationCreate,
    ConsultationRead,
    ErrorResponse,
    HealthResponse,
    SuccessResponse,
    userUpdate,
    adminUserCreate 
    ConsultationUpdate
)
from app.services import (
    create_consultation,
    delete_consultation,
    get_consultation,
    list_consultations,
    can_access, get_consultation, update_consultation, _to_dict
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
app.include_router(users.router) 
@app.get("/consultations", response_model=SuccessResponse[list[Consultation]])
def get_consultations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=5, ge=1, le=100),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_consultations(db=db, skip=skip, limit=limit, search=search)

def get_current_user(
    db: Session = Depends(get_db),
    x_test_role: str = Header("admin"),
) -> User:
    user = db.scalars(
        select(User).where(User.role == x_test_role).order_by(User.id)
    ).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Tidak terautentikasi")
    return user

@app.get(
    "/consultations/{id}",
    response_model=SuccessResponse[Consultation],
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def get_consultation_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    consultation = get_consultation(db, id)

    if consultation is None:
        return JSONResponse(
            status_code=404,
            content=error_response("Konsultasi tidak ditemukan"),
        )

    if not can_access(current_user, consultation):
        return JSONResponse(
            status_code=403,
            content=error_response("Anda tidak berhak mengakses konsultasi ini"),
        )

    return success_response("Konsultasi ditemukan", _to_dict(consultation))


@app.get("/health", response_model=HealthResponse)
def get_health():
    return {"status": "ok"}


@app.post(
    "/consultations",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[Consultation],
)
def post_consultation(payload: ConsultationCreate, db: Session = Depends(get_db)):
    owner = db.scalars(select(User).order_by(User.id)).first()
    new_row = create_consultation(db, payload, user_id=owner.id)
    return success_response("Konsultasi berhasil ditambahkan", new_row)


@app.patch(
    "/consultations/{id}",
    response_model=SuccessResponse[Consultation],
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def patch_consultation(
    id: int,
    payload: ConsultationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = get_consultation(db, id)

    if row is None:
        return JSONResponse(
            status_code=404,
            content=error_response("Konsultasi tidak ditemukan"),
        )

    if not can_access(current_user, row):
        return JSONResponse(
            status_code=403,
            content=error_response("Anda tidak berhak mengakses konsultasi ini"),
        )

    updated = update_consultation(db, row, payload)
    return success_response("Konsultasi berhasil diperbarui", updated)


@app.delete(
    "/consultations/{id}",
    response_model=SuccessResponse[Consultation],
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def delete_consultations(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = get_consultation(db, id)

    if row is None:
        return JSONResponse(
            status_code=404,
            content=error_response("Konsultasi tidak ditemukan"),
        )

    if not can_access(current_user, row):
        return JSONResponse(
            status_code=403,
            content=error_response("Anda tidak berhak mengakses konsultasi ini"),
        )

    deleted = delete_consultation(db, row)
    return success_response("Konsultasi berhasil dihapus", deleted)