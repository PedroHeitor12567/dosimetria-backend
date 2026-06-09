from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.application.use_cases.calcular_dosimetria_use_case import CalcularDosimetriaUseCase
from src.domain.entities.dosimetria import TipoAjuste, CircustanciaJudicial, AjusteLegal, AjusteFase3
from src.infrastructure.container import container

router = APIRouter(prefix="/dosimetria", tags=["Dosimetria"])

def get_calcular_dosimetria_use_case() -> CalcularDosimetriaUseCase:
    return container.calcular_dosimetria_use_case()

class AjusteLegalRequest(BaseModel):
    tipo: TipoAjuste
    descricao: str

class AjusteFase3Request(BaseModel):
    descricao: str
    fracao_numerador: int = Field(gt=0)
    fracao_denominador: int = Field(gt=0)
    aumentar: bool

class DosimetriaRequest(BaseModel):
    pena_minima_anos: float = Field(gt=0)
    pena_maxima_anos: float = Field(gt=0)
    circunstancias_desfavoraveis: List[CircustanciaJudicial] = Field(default=[])
    ajustes_fase2: List[AjusteLegalRequest] = Field(default=[])
    ajustes_fase3: List[AjusteFase3Request] = Field(default=[])

class DosimetriaResponse(BaseModel):
    pena_minima_meses: int
    pena_maxima_meses: int
    circunstancias_desfavoraveis: List[str]
    pena_base_meses: int
    pena_base_dias: int
    pena_intermediaria_meses: int
    pena_intermediaria_dias: int
    pena_definitiva_meses: int
    pena_definitiva_dias: int
    pena_definitiva_anos: float
    pena_definitiva_formatada: str

@router.post("/calcular", response_model=DosimetriaResponse)
def calcular_dosimetria(
        request: DosimetriaRequest,
        use_case: CalcularDosimetriaUseCase = Depends(get_calcular_dosimetria_use_case),
):
    if request.pena_maxima_anos <= request.pena_minima_anos:
        raise HTTPException(
            status_code=422,
            detail="pena_maxima_anos deve ser maior que pena_minima_anos",
        )

    ajustes_fase2 = [
        AjusteLegal(tipo=a.tipo, descricao=a.descricao)
        for a in request.ajustes_fase2
    ]

    ajustes_fase3 = [
        AjusteFase3(
            descricao=a.descricao,
            fracao_numerador=a.fracao_numerador,
            fracao_denominador=a.fracao_denominador,
            aumentar=a.aumentar,
        )
        for a in request.ajustes_fase3
    ]

    resultado = use_case.executar(
        pena_minima_anos=request.pena_minima_anos,
        pena_maxima_anos=request.pena_maxima_anos,
        circunstancias_desfavoraveis=request.circunstancias_desfavoraveis,
        ajustes_fase2=ajustes_fase2,
        ajustes_fase3=ajustes_fase3,
    )

    return DosimetriaResponse(
        pena_minima_meses=resultado.pena_minima_meses,
        pena_maxima_meses=resultado.pena_maxima_meses,
        circunstancias_desfavoraveis=resultado.circunstancias_desfavoraveis,
        pena_base_meses=resultado.pena_base_meses,
        pena_intermediaria_meses=resultado.pena_intermediaria_meses,
        pena_definitiva_meses=resultado.pena_definitiva_meses,
        pena_base_dias=resultado.pena_base_dias,
        pena_intermediaria_dias=resultado.pena_intermediaria_dias,
        pena_definitiva_dias=resultado.pena_definitiva_dias,
        pena_definitiva_anos=resultado.pena_definitiva_anos,
        pena_definitiva_formatada=resultado.pena_definitiva_formatada,
    )