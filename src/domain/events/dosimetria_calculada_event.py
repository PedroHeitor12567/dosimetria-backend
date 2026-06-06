from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.dosimetria import ResultadoDosimetria


@dataclass
class DosimetriaCalculadaEvent:
    ocorrido_em: datetime
    resultado: ResultadoDosimetria
