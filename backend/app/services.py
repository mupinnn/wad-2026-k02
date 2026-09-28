"""Operasi atas daftar konsultasi di app.data.

Belum diisi. Tambahkan fungsi baru di berkas ini sesuai
docs/uts-consultation-contract.md. Jangan mengubah fungsi milik anggota lain.
"""

from app.data import CONSULTATIONS
from app.schemas import ConsultationCreate


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