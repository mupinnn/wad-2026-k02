"""Register dan login."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.response import error_response, success_response
from app.schemas import (
    ErrorResponse,
    LoginRequest,
    RegisterRequest,
    SuccessResponse,
    TokenData,
    UserPublic,
)
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Dipakai saat email tidak ditemukan, supaya waktu respons tetap mirip
# dan penyerang tidak bisa menebak email mana yang terdaftar.
_DUMMY_HASH = hash_password("kata-sandi-palsu")

_EMAIL_SUDAH_ADA = "Email sudah terdaftar."
_LOGIN_GAGAL = "Email atau kata sandi salah."


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[UserPublic],
    responses={409: {"model": ErrorResponse}},
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == payload.email)) is not None:
        return JSONResponse(status_code=409, content=error_response(_EMAIL_SUDAH_ADA))

    user = User(
        nama=payload.nama,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role="user",  # selalu user, apa pun yang dikirim klien
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # dua permintaan bersamaan dengan email sama: yang kedua kalah di sini
        db.rollback()
        return JSONResponse(status_code=409, content=error_response(_EMAIL_SUDAH_ADA))
    db.refresh(user)

    return success_response(
        "Registrasi berhasil", UserPublic.model_validate(user).model_dump()
    )


@router.post(
    "/login",
    response_model=SuccessResponse[TokenData],
    responses={401: {"model": ErrorResponse}},
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    hash_to_check = user.password_hash if user else _DUMMY_HASH
    password_ok = verify_password(payload.password, hash_to_check)

    if user is None or not password_ok:
        return JSONResponse(status_code=401, content=error_response(_LOGIN_GAGAL))

    token = create_access_token(user.id)
    return success_response(
        "Login berhasil", {"access_token": token, "token_type": "bearer"}
    )