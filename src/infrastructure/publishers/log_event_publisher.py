from src.application.ports.event_publisher import EventPublisher
from src.domain.events.dosimetria_calculada_event import DosimetriaCalculadaEvent


class LogEventPublisher(EventPublisher):
    def publicar(self, evento: DosimetriaCalculadaEvent) -> None:
        print(
            f"[EVENTO] DosimetriaCalculada | "
            f"ocorrido_em={evento.ocorrido_em.isoformat()} | "
            f"pena_definitiva={evento.resultado.pena_definitiva_formatada}"
        )
        