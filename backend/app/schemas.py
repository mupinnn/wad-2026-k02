"""Skema Pydantic untuk jadwal konsultasi.

Belum diisi. Anggota yang memiliki endpoint menambahkan skema di berkas ini
sesuai docs/uts-consultation-contract.md. Tambahkan kelas baru; jangan mengubah
kelas milik anggota lain.
"""

from pydantic import BaseModel
from datetime import datetime


class Consultation(BaseModel):
    nama_pasien: str
    nama_dokter: str
    poli: str
    waktu_konsultasi: datetime
    keluhan: str