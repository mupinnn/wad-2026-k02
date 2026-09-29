"""Operasi atas daftar konsultasi di app.data.

Belum diisi. Tambahkan fungsi baru di berkas ini sesuai
docs/uts-consultation-contract.md. Jangan mengubah fungsi milik anggota lain.
"""

from datetime import datetime, timezone

from app.data import CONSULTATIONS
from app.response import success_response
from app.schemas import ConsultationCreate


def _consultation_datetime(value: datetime | str) -> datetime:
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


def list_consultations(
    skip: int = 0,
    limit: int = 5,
    search: str | None = None,
) -> list[dict]:
    rows = CONSULTATIONS

    if search:
        term = search.casefold()
        rows = [
            row
            for row in rows
            if term in row["nama_pasien"].casefold()
            or term in row["nama_dokter"].casefold()
        ]

    rows = sorted(
        rows,
        key=lambda row: _consultation_datetime(row["waktu_konsultasi"]),
        reverse=True,
    )

    return success_response(
        "Daftar konsultasi berhasil diambil",
        rows[skip : skip + limit],
    )


def get_consultation(consultation_id: int) -> dict | None:
    return next(        
        (row for row in CONSULTATIONS if row["id"] == consultation_id),
        None,
    )


def create_consultation(payload: ConsultationCreate) -> dict:
    """Simpan jadwal baru. id baru = id terbesar yang ada + 1."""
    new_id = max((row["id"] for row in CONSULTATIONS), default=0) + 1
    new_row = {"id": new_id, **payload.model_dump()}
    CONSULTATIONS.append(new_row)
    return new_row


def delete_consultation(consultation_id: int):
    for index, consultation in enumerate(CONSULTATIONS):
        if consultation["id"] == consultation_id:
            return CONSULTATIONS.pop(index)

    return None