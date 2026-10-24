"""Tabel users dan consultations. Jangan ubah berkas ini di luar tugas model."""

from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, TypeDecorator
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class UtcDateTime(TypeDecorator):
    """Simpan dan baca datetime sebagai UTC. SQLite tidak menyimpan zona waktu."""

    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, value: datetime | None, _dialect) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    def process_result_value(self, value: datetime | None, _dialect) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('admin', 'user')", name="ck_users_role"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nama: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    dibuat_pada: Mapped[datetime] = mapped_column(UtcDateTime, default=utcnow)

    consultations: Mapped[list["Consultation"]] = relationship(back_populates="owner")

    @validates("email")
    def _lowercase_email(self, _key: str, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise ValueError("email wajib diisi")
        return normalized

    @validates("role")
    def _check_role(self, _key: str, value: str) -> str:
        if value not in {"admin", "user"}:
            raise ValueError("role harus admin atau user")
        return value


class Consultation(Base):
    __tablename__ = "consultations"

    id: Mapped[int] = mapped_column(primary_key=True)
    nama_pasien: Mapped[str] = mapped_column(String)
    nama_dokter: Mapped[str] = mapped_column(String)
    poli: Mapped[str] = mapped_column(String)
    keluhan: Mapped[str] = mapped_column(String)
    waktu_konsultasi: Mapped[datetime] = mapped_column(UtcDateTime)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        index=True,
    )

    owner: Mapped[User] = relationship(back_populates="consultations")
