"""Jadwal konsultasi. Pemilik atau admin."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Consultation, User
from app.response import success_response
from app.schemas import Consultation as ConsultationSchema
from app.schemas import ConsultationCreate, ConsultationUpdate, ErrorResponse, SuccessResponse
from app.services import (
    can_access,
    create_consultation,
    delete_consultation,
    get_consultation,
    list_consultations,
    to_dict,
    update_consultation,
)

router = APIRouter(tags=["consultations"])

_MISSING = "Konsultasi tidak ditemukan"
_FORBIDDEN = "Anda tidak berhak mengakses konsultasi ini"


def _owned_row(db: Session, consultation_id: int, current_user: User) -> Consultation:
    row = get_consultation(db, consultation_id)
    if row is None:
        raise HTTPException(status_code=404, detail=_MISSING)
    if not can_access(current_user, row):
        raise HTTPException(status_code=403, detail=_FORBIDDEN)
    return row


@router.get("/consultations", response_model=SuccessResponse[list[ConsultationSchema]])
def get_consultations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=5, ge=1, le=100),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = list_consultations(
        db,
        current_user,
        skip=skip,
        limit=limit,
        search=search,
    )
    return success_response(
        "Daftar konsultasi berhasil diambil",
        [to_dict(row) for row in rows],
    )


@router.get(
    "/consultations/{id}",
    response_model=SuccessResponse[ConsultationSchema],
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def get_consultation_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return success_response("Konsultasi ditemukan", to_dict(_owned_row(db, id, current_user)))


@router.post(
    "/consultations",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[ConsultationSchema],
)
def post_consultation(
    payload: ConsultationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = create_consultation(db, payload, current_user.id)
    db.commit()
    db.refresh(row)
    return success_response("Konsultasi berhasil ditambahkan", to_dict(row))


@router.patch(
    "/consultations/{id}",
    response_model=SuccessResponse[ConsultationSchema],
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def patch_consultation(
    id: int,
    payload: ConsultationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = update_consultation(db, _owned_row(db, id, current_user), payload)
    db.commit()
    db.refresh(row)
    return success_response("Konsultasi berhasil diperbarui", to_dict(row))


@router.delete(
    "/consultations/{id}",
    response_model=SuccessResponse[ConsultationSchema],
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def delete_consultations(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_consultation(db, _owned_row(db, id, current_user))
    db.commit()
    return success_response("Konsultasi berhasil dihapus", deleted)
