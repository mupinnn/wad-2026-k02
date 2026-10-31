"""Skema Pydantic untuk jadwal konsultasi.

Belum diisi. Anggota yang memiliki endpoint menambahkan skema di berkas ini
sesuai docs/uts-consultation-contract.md. Tambahkan kelas baru; jangan mengubah
kelas milik anggota lain.
"""

from datetime import datetime
from typing import Annotated, Generic, Literal, TypeVar
from pydantic import BaseModel, ConfigDict, Field, field_validator, StringConstraints


T = TypeVar("T")
NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


def normalize_email(value: str) -> str:
    value = value.strip().lower()
    local, _, domain = value.partition("@")
    if not local or "." not in domain:
        raise ValueError("Format email tidak valid.")
    return value


def limit_password_bytes(value: str) -> str:
    if len(value.encode("utf-8")) > 72:
        raise ValueError("Kata sandi terlalu panjang (maksimal 72 byte).")
    return value


class ConsultationCreate(BaseModel):
    """Data yang dikirim client saat menambah jadwal. Tidak ada id — id dibuat server."""

    nama_pasien: str
    nama_dokter: str
    poli: str
    waktu_konsultasi: datetime
    keluhan: str


class Consultation(ConsultationCreate):
    """Data yang dibalas server. Sama seperti ConsultationCreate, ditambah id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

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

class ConsultationUpdate(BaseModel):
    nama_pasien: str | None = None
    nama_dokter: str | None = None
    poli: str | None = None
    waktu_konsultasi: datetime | None = None
    keluhan: str | None = None

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
        return normalize_email(value)

    @field_validator("password")
    @classmethod
    def _password_maks_72_byte(cls, value: str) -> str:
        return limit_password_bytes(value)


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

class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nama: NonEmptyString | None = None
    email: NonEmptyString | None = None
    password: str | None = Field(default=None, min_length=8, max_length=72)

    @field_validator("email")
    @classmethod
    def _email_valid(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return normalize_email(value)

    @field_validator("password")
    @classmethod
    def _password_maks_72_byte(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return limit_password_bytes(value)


class AdminUserCreate(BaseModel):
    nama: NonEmptyString
    email: NonEmptyString
    password: str = Field(min_length=8, max_length=72)
    role: Literal["user", "admin"]

    @field_validator("email")
    @classmethod
    def _email_valid(cls, value: str) -> str:
        return normalize_email(value)

    @field_validator("password")
    @classmethod
    def _password_maks_72_byte(cls, value: str) -> str:
        return limit_password_bytes(value)

class TokenData(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"

