
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import User
from app.deps import get_current_user, require_admin
from app.response import success_response, error_response
from app.schemas import UserPublic, UserUpdate, AdminUserCreate
from app.security import hash_password


router = APIRouter(prefix="/users", tags=["users"])


def public_user(user: User) -> dict:
    return UserPublic.model_validate(user).model_dump()


@router.get("/me")
def get_profile(user: User = Depends(get_current_user)):
    return success_response("Profil berhasil diambil", public_user(user))


@router.patch("/me")
def update_profile(
    payload: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = payload.model_dump(exclude_unset=True, exclude_none=True)

    if "email" in data:
        data["email"] = data["email"].strip().lower()
        existing = db.scalar(
            select(User).where(
                User.email == data["email"],
                User.id != user.id,
            )
        )
        if existing:
            return JSONResponse(
                status_code=409,
                content=error_response("Email sudah terdaftar."),
            )

    if data.get("password"):
        data["password_hash"] = hash_password(data.pop("password"))
    else:
        data.pop("password", None)

    for key, value in data.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=409,
            content=error_response("Email sudah terdaftar."),
        )

    return success_response("Profil berhasil diperbarui", public_user(user))


@router.post("", status_code=201)
def create_user(
    payload: AdminUserCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    email = payload.email.strip().lower()

    if db.scalar(select(User).where(User.email == email)):
        return JSONResponse(
            status_code=409,
            content=error_response("Email sudah terdaftar."),
        )

    user = User(
        nama=payload.nama,
        email=email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=409,
            content=error_response("Email sudah terdaftar."),
        )

    return success_response("Akun berhasil dibuat", public_user(user))
