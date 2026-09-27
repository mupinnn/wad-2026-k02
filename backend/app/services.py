"""Operasi atas daftar konsultasi di app.data.

Belum diisi. Tambahkan fungsi baru di berkas ini sesuai
docs/uts-consultation-contract.md. Jangan mengubah fungsi milik anggota lain.
"""
from app.data import CONSULTATIONS

def delete_consultation(consultation_id: int):
    for index, consultation in enumerate(CONSULTATIONS):
        if consultation["id"] == consultation_id:
            return CONSULTATIONS.pop(index)

    return None