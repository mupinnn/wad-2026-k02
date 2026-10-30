"""Hook startup aplikasi."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.seed import seed


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Migrasi dijalankan manual: `alembic upgrade head` dari folder backend.
    seed()
    yield