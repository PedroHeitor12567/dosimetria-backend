from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.controllers.dosimetria_controller import router as dosimetria_router

app = FastAPI(
    title="API de Dosimetria da Pena",
    description="Cálculo do sistema trifásico de dosimetria da pena conforme o Código Penal Brasileiro",
    version="2.0.0",
)

app.include_router(dosimetria_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health():
    return {"status": "ok"}