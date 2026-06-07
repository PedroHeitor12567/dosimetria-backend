from fastapi import FastAPI
from src.infrastructure.controllers.dosimetria_controller import router as dosimetria_router

app = FastAPI(
    title="API de Dosimetria da Pena",
    description="Cálculo do sistema trifásico de dosimetria da pena conforme o Código Penal Brasileiro",
    version="2.0.0",
)

app.include_router(dosimetria_router)


@app.get("/health")
def health():
    return {"status": "ok"}