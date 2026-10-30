"""Hash kata sandi dan token akses JWT."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import get_settings

ALGORITHM = "HS256"


def _secret_key() -> str:
    key = get_settings().secret_key
    if not key:
        raise RuntimeError("SECRET_KEY belum diisi di .env")
    return key


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"), password_hash.encode("utf-8")
        )
    except ValueError:
        # kata sandi > 72 byte, atau hash tersimpan tidak valid
        return False


def create_access_token(user_id: int) -> str:
    expire_minutes = get_settings().access_token_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, _secret_key(), algorithm=ALGORITHM)


def decode_token(token: str) -> int:
    """Kembalikan id pengguna. Melempar jwt.InvalidTokenError bila token tidak sah."""
    payload = jwt.decode(
        token,
        _secret_key(),
        algorithms=[ALGORITHM],
        options={"require": ["exp", "sub"]},
    )
    try:
        return int(payload["sub"])
    except ValueError:
        raise jwt.InvalidTokenError("sub bukan id yang valid") from None