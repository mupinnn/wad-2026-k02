"""Skema Pydantic untuk jadwal konsultasi.

Belum diisi. Anggota yang memiliki endpoint menambahkan skema di berkas ini
sesuai docs/uts-consultation-contract.md. Tambahkan kelas baru; jangan mengubah
kelas milik anggota lain.
"""

from datetime import datetime
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

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


class RegisterRequest(BaseModel):
    nama: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=254)
    password: str = Field(min_length=8, max_length=72)

    @field_validator("nama")
    @classmethod
    def _nama_tidak_kosong(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Nama wajib diisi.")
        return value

    @field_validator("email")
    @classmethod
    def _email_valid(cls, value: str) -> str:
        value = value.strip().lower()
        nama, _, domain = value.partition("@")
        if not nama or "." not in domain:
            raise ValueError("Format email tidak valid.")
        return value

    @field_validator("password")
    @classmethod
    def _password_maks_72_byte(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Kata sandi terlalu panjang (maksimal 72 byte).")
        return value


class LoginRequest(BaseModel):
    email: str = Field(max_length=254)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def _normalisasi_email(cls, value: str) -> str:
        return value.strip().lower()


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nama: str
    email: str
    role: Literal["admin", "user"]


class TokenData(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"