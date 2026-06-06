from abc import ABC, abstractmethod

from src.domain.events.dosimetria_calculada_event import DosimetriaCalculadaEvent


class EventPublisher(ABC):
    @abstractmethod
    def publicar(self, evento: DosimetriaCalculadaEvent) -> None:
        pass
