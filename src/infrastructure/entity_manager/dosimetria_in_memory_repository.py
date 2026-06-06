import uuid
from typing import Dict, Optional, List

from src.domain.entities.dosimetria import ResultadoDosimetria
from src.domain.repositories.dosimetria_repository import DosimetriaRepository


class DosimetriaInMemoryRepository(DosimetriaRepository):
    def __init__(self):
        self._store: Dict[str, ResultadoDosimetria] = {}

    def salvar(self, resultado: ResultadoDosimetria) -> str:
        id_gerado = str(uuid.uuid4())
        self._store[id_gerado] = resultado
        return id_gerado

    def buscar_por_id(self, id: str) -> Optional[ResultadoDosimetria]:
        return self._store.get(id)

    def listar_todos(self) -> List[ResultadoDosimetria]:
        return list(self._store.values())
