from src.application.ports.event_publisher import EventPublisher
from src.application.use_cases.calcular_dosimetria_use_case import CalcularDosimetriaUseCase
from src.domain.repositories.dosimetria_repository import DosimetriaRepository
from src.domain.services.dosimetria_domain_service import DosimetriaDomainService
from src.infrastructure.entity_manager.dosimetria_in_memory_repository import DosimetriaInMemoryRepository
from src.infrastructure.publishers.log_event_publisher import LogEventPublisher


class Container:
    def __init__(self):
        self._repository: DosimetriaRepository = DosimetriaInMemoryRepository()
        self._event_publisher: EventPublisher = LogEventPublisher()
        self._domain_service:DosimetriaDomainService = DosimetriaDomainService()

    def calcular_dosimetria_use_case(self) -> CalcularDosimetriaUseCase:
        return CalcularDosimetriaUseCase(
            domain_service=self._domain_service,
            repository=self._repository,
            event_publisher=self._event_publisher,
        )

container = Container()