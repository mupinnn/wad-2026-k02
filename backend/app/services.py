"""Operasi atas daftar konsultasi di app.data.

Belum diisi. Tambahkan fungsi baru di berkas ini sesuai
docs/uts-consultation-contract.md. Jangan mengubah fungsi milik anggota lain.
"""

from datetime import datetime, timezone

from app.data import CONSULTATIONS
from app.response import success_response, error_response
from app.models import Consultation, User
from app.schemas import Consultation as ConsultationSchema
from app.schemas import ConsultationCreate, ConsultationRead, ConsultationUpdate

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

def _to_dict(row: Consultation) -> dict:
    return ConsultationSchema.model_validate(row, from_attributes=True).model_dump(mode="json")

def can_access(user: User, row: Consultation) -> bool:
    return user.role == "admin" or row.user_id == user.id

def list_consultations(
    db: Session,
    skip: int = 0,
    limit: int = 5,
    search: str | None = None,
) -> dict:
    stmt = select(Consultation)

    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(
                Consultation.nama_pasien.ilike(pattern),
                Consultation.nama_dokter.ilike(pattern),
            )
        )

    stmt = (
        stmt.order_by(
            Consultation.waktu_konsultasi.desc(),
            Consultation.id.desc(),  # tie-breaker
        )
        .offset(skip)
        .limit(limit)
    )

    rows = db.scalars(stmt).all()

    return success_response(
        "Daftar konsultasi berhasil diambil",
        [ConsultationRead.model_validate(r).model_dump(mode="json") for r in rows],
    )


def get_consultation(db: Session, consultation_id: int) -> Consultation | None:
    return db.get(Consultation, consultation_id)

def create_consultation(db: Session, payload: ConsultationCreate, user_id: int) -> dict:
    row = Consultation(**payload.model_dump(), user_id=user_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_dict(row)

def update_consultation(db: Session, row: Consultation, payload: ConsultationUpdate) -> dict:
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in changes.items():
        setattr(row, key, value)

    db.commit()
    db.refresh(row)
    return _to_dict(row)

def delete_consultation(db: Session, row: Consultation) -> dict:
    data = _to_dict(row)  # serialisasi SEBELUM dihapus
    db.delete(row)
    db.commit()
    return data