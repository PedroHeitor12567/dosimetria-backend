from datetime import datetime
from typing import List

from src.application.ports.event_publisher import EventPublisher
from src.domain.entities.dosimetria import ResultadoDosimetria, CircustanciaJudicial, AjusteLegal, AjusteFase3
from src.domain.events.dosimetria_calculada_event import DosimetriaCalculadaEvent
from src.domain.repositories.dosimetria_repository import DosimetriaRepository
from src.domain.services.dosimetria_domain_service import DosimetriaDomainService


class CalcularDosimetriaUseCase:
    def __init__(self, domain_service: DosimetriaDomainService, repository: DosimetriaRepository, event_publisher: EventPublisher,) -> None:
        self._domain_service = domain_service
        self._repository = repository
        self._event_publisher = event_publisher

    def executar(self, pena_minima_anos: float, pena_maxima_anos: float, circunstancias_desfavoraveis: List[CircustanciaJudicial], ajustes_fase2: List[AjusteLegal], ajustes_fase3: List[AjusteFase3]) -> ResultadoDosimetria:
        resultado = self._domain_service.calcular(
            pena_minima_anos=pena_minima_anos,
            pena_maxima_anos=pena_maxima_anos,
            circunstancias_desfavoraveis=circunstancias_desfavoraveis,
            ajustes_fase2=ajustes_fase2,
            ajustes_fase3=ajustes_fase3,
        )

        self._repository.salvar(resultado)

        self._event_publisher.publicar(
            DosimetriaCalculadaEvent(
                ocorrido_em=datetime.now(),
                resultado=resultado,
            )
        )

        return resultado