"""Isi admin dan 12 jadwal fiktif. Aman dijalankan ulang.

Dari folder backend, setelah migrasi:

    python -m app.seed
"""

import sys
from datetime import datetime, timezone

import bcrypt
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError

from app.config import get_settings
from app.data import CONSULTATIONS
from app.database import SessionLocal
from app.models import Consultation, User


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def _as_utc(value: datetime | str) -> datetime:
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _require_admin_credentials() -> tuple[str, str]:
    settings = get_settings()
    email = settings.admin_email.strip().lower()
    password = settings.admin_password
    if not email or not password:
        print(
            "ADMIN_EMAIL dan ADMIN_PASSWORD wajib diisi di .env. Seed tidak membuat kata sandi sendiri.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return email, password


def _optional_user_credentials() -> tuple[str, str] | None:
    settings = get_settings()
    email = settings.user_email.strip().lower()
    password = settings.user_password
    if not email and not password:
        return None
    if not email or not password:
        print(
            "USER_EMAIL dan USER_PASSWORD harus diisi berpasangan. Pengguna biasa dilewati.",
            file=sys.stderr,
        )
        return None
    return email, password


def _get_or_create_user(
    session,
    *,
    email: str,
    password: str,
    nama: str,
    role: str,
) -> User:
    existing = session.scalar(select(User).where(User.email == email))
    if existing is not None:
        if existing.role != role:
            print(
                f"{email} sudah terdaftar dengan role {existing.role}, bukan {role}.",
                file=sys.stderr,
            )
            raise SystemExit(1)
        return existing

    user = User(
        nama=nama,
        email=email,
        password_hash=hash_password(password),
        role=role,
        dibuat_pada=datetime.now(timezone.utc),
    )
    session.add(user)
    session.flush()
    return user


def seed() -> None:
    admin_email, admin_password = _require_admin_credentials()
    user_credentials = _optional_user_credentials()

    try:
        with SessionLocal() as session:
            admin = _get_or_create_user(
                session,
                email=admin_email,
                password=admin_password,
                nama="Admin Klinik",
                role="admin",
            )

            if user_credentials is not None:
                user_email, user_password = user_credentials
                _get_or_create_user(
                    session,
                    email=user_email,
                    password=user_password,
                    nama="Petugas Klinik",
                    role="user",
                )

            consultation_count = session.scalar(
                select(func.count()).select_from(Consultation)
            )
            if not consultation_count:
                for row in CONSULTATIONS:
                    session.add(
                        Consultation(
                            id=row["id"],
                            nama_pasien=row["nama_pasien"],
                            nama_dokter=row["nama_dokter"],
                            poli=row["poli"],
                            keluhan=row["keluhan"],
                            waktu_konsultasi=_as_utc(row["waktu_konsultasi"]),
                            user_id=admin.id,
                        )
                    )

            session.commit()
    except OperationalError as exc:
        if "no such table" in str(exc).lower():
            print(
                "Tabel belum ada. Jalankan `alembic upgrade head` dari folder backend dulu.",
                file=sys.stderr,
            )
        else:
            print(exc, file=sys.stderr)
        raise SystemExit(1) from None

    print("Seed selesai.")


if __name__ == "__main__":
    seed()
