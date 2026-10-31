"""Operasi jadwal konsultasi di SQLite. Route yang menyimpan dan membungkus respons."""

from app.models import Consultation, User
from app.schemas import Consultation as ConsultationSchema
from app.schemas import ConsultationCreate, ConsultationUpdate

from sqlalchemy import or_, select
from sqlalchemy.orm import Session


def to_dict(row: Consultation) -> dict:
    return ConsultationSchema.model_validate(row).model_dump(mode="json")


def can_access(user: User, row: Consultation) -> bool:
    return user.role == "admin" or row.user_id == user.id


def list_consultations(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 5,
    search: str | None = None,
) -> list[Consultation]:
    stmt = select(Consultation)
    if current_user.role != "admin":
        stmt = stmt.where(Consultation.user_id == current_user.id)

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
            Consultation.id.desc(),
        )
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


def get_consultation(db: Session, consultation_id: int) -> Consultation | None:
    return db.get(Consultation, consultation_id)


def create_consultation(db: Session, payload: ConsultationCreate, user_id: int) -> Consultation:
    row = Consultation(**payload.model_dump(), user_id=user_id)
    db.add(row)
    return row


def update_consultation(db: Session, row: Consultation, payload: ConsultationUpdate) -> Consultation:
    for key, value in payload.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(row, key, value)
    return row


def delete_consultation(db: Session, row: Consultation) -> dict:
    data = to_dict(row)
    db.delete(row)
    return data
