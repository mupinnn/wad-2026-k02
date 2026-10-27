"""Skema Pydantic untuk jadwal konsultasi.

Belum diisi. Anggota yang memiliki endpoint menambahkan skema di berkas ini
sesuai docs/uts-consultation-contract.md. Tambahkan kelas baru; jangan mengubah
kelas milik anggota lain.
"""

from datetime import datetime
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ConsultationCreate(BaseModel):
    """Data yang dikirim client saat menambah jadwal. Tidak ada id — id dibuat server."""

    nama_pasien: str
    nama_dokter: str
    poli: str
    waktu_konsultasi: datetime
    keluhan: str


class Consultation(ConsultationCreate):
    """Data yang dibalas server. Sama seperti ConsultationCreate, ditambah id."""

    id: int

class userUpdate(BaseModel):
    """Data yang dikirim client saat mengupdate user. Tidak ada id — id dibuat server."""

    username: str | None = None
    email: str | None = None    
    password: str | None = None    
    role: str| None = None    

class adminUserCreate(BaseModel):
    """Data yang dikirim client saat menambah user. Tidak ada id — id dibuat server."""

    username: str
    email: str    
    password: str    
    role: Literal["user", "admin"]

class SuccessResponse(BaseModel, Generic[T]):
    status: Literal["success"]
    message: str
    data: T


class ErrorResponse(BaseModel):
    status: Literal["error"]
    message: str
    data: None = None


class HealthResponse(BaseModel):
    status: Literal["ok"]