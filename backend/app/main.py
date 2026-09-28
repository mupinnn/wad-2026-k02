from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import Consultation, ConsultationCreate
from app.services import create_consultation

app = FastAPI(title="Jadwal Konsultasi Klinik")

# B5: izinkan hanya origin frontend. Jangan menambah origin lain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.post("/consultations", response_model=Consultation, status_code=status.HTTP_201_CREATED)
def post_consultation(payload: ConsultationCreate):
    return create_consultation(payload)