from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.dosimetria import ResultadoDosimetria


class DosimetriaRepository(ABC):
    @abstractmethod
    def salvar(self, resultado: ResultadoDosimetria) -> str:
        pass

    @abstractmethod
    def buscar_por_id(self, id: str) -> Optional[ResultadoDosimetria]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[ResultadoDosimetria]:
        pass