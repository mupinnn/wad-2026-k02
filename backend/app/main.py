from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.response import error_response
from app.routers.auth import router as auth_router
from app.routers.consultations import router as consultations_router
from app.routers.users import router as users_router
from app.schemas import HealthResponse
from app.startup import lifespan

app = FastAPI(title="Jadwal Konsultasi Klinik", lifespan=lifespan)

# B5: izinkan hanya origin frontend. Jangan menambah origin lain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(consultations_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    message = exc.detail if isinstance(exc.detail, str) else "Permintaan ditolak."
    return JSONResponse(status_code=exc.status_code, content=error_response(message))


@app.get("/health", response_model=HealthResponse)
def get_health():
    return {"status": "ok"}
