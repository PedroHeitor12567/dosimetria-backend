from dataclasses import dataclass
from enum import Enum
from typing import List

class CircustanciaJudicial(str, Enum):
    CULPABILIDADE = "culpabilidade"
    ANTECENDENTES = "antecedentes"
    CONDUTA_SOCIAL = "conduta_social"
    PERSONALIDADE = "personalidade"
    MOTIVOS = "motivos"
    CIRCUNSTANCIAS = "circunstancias"
    CONSEQUENCIAS = "consequencias"
    COMPORTAMENTO_VITIMA = "comportamento_vitima"

class TipoAjuste(str, Enum):
    AGRAVANTE = "agravante"
    ATENUANTE = "atenuante"

@dataclass
class AjusteLegal:
    tipo: TipoAjuste
    descricao: str

@dataclass
class AjusteFase3:
    descricao: str
    fracao_numerador: int
    fracao_denominador: int
    aumentar: bool

@dataclass
class ResultadoDosimetria:
    pena_minima_meses: int
    pena_maxima_meses: int
    circunstancias_desfavoraveis: List[str]
    pena_base_meses: int
    pena_base_dias: int
    ajustes_fase2: List[AjusteLegal]
    pena_intermediaria_meses: int
    pena_intermediaria_dias: int
    ajustes_fase3: List[AjusteFase3]
    pena_definitiva_meses: int
    pena_definitiva_dias: int
    pena_definitiva_anos: float
    pena_definitiva_formatada: str