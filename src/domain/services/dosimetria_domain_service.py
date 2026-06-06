from typing import List

from src.domain.entities.dosimetria import CircustanciaJudicial, AjusteLegal, AjusteFase3, ResultadoDosimetria, \
    TipoAjuste


class DosimetriaDomainService:
    def calcular(self, pena_minima_anos: float, pena_maxima_anos: float, circunstancias_desfavoraveis: List[CircustanciaJudicial], ajustes_fase2: List[AjusteLegal], ajustes_fase3: List[AjusteFase3],) -> ResultadoDosimetria:
        pena_minima_meses = int(pena_minima_anos * 12)
        pena_maxima_meses = int(pena_maxima_anos * 12)

        pena_base_meses = self._calcular_pena_base(
            pena_minima_meses,
            pena_maxima_meses,
            circunstancias_desfavoraveis,
        )

        pena_intermediaria_meses = self._calcular_pena_intermediaria(
            pena_base_meses,
            pena_minima_meses,
            pena_maxima_meses,
            ajustes_fase2,
        )

        pena_definitiva_meses = self._calcular_pena_definitiva(
            pena_intermediaria_meses,
            ajustes_fase3,
        )

        pena_definitiva_anos = pena_definitiva_meses / 12
        pena_definitiva_formatada = self._formatar_pena(pena_definitiva_meses)

        return ResultadoDosimetria(
            pena_minima_meses=pena_minima_meses,
            pena_maxima_meses=pena_maxima_meses,
            circunstancias_desfavoraveis=[c.value for c in circunstancias_desfavoraveis],
            pena_base_meses=pena_base_meses,
            ajustes_fase2=ajustes_fase2,
            pena_intermediaria_meses=pena_intermediaria_meses,
            ajustes_fase3=ajustes_fase3,
            pena_definitiva_meses=pena_definitiva_meses,
            pena_definitiva_anos=round(pena_definitiva_anos, 2),
            pena_definitiva_formatada=pena_definitiva_formatada,
        )

    def _calcular_pena_base(self, pena_minima_meses: int, pena_maxima_meses: int, circunstancias_desfavoraveis: List[CircustanciaJudicial]) -> int:
        diferenca = pena_maxima_meses - pena_minima_meses
        incremento_por_circunstancia = diferenca / 8
        total_incremento = incremento_por_circunstancia * len(circunstancias_desfavoraveis)
        return int(round(pena_minima_meses + total_incremento))

    def _calcular_pena_intermediaria(self, pena_base_meses: int, pena_minima_meses: int, pena_maxima_meses: int, ajustes: List[AjusteLegal]) -> int:
        pena = pena_base_meses
        for a in ajustes:
            variacao = pena_base_meses // 6
            if a.tipo == TipoAjuste.AGRAVANTE:
                pena += variacao
            else:
                pena -= variacao
        return max(pena_minima_meses, min(pena, pena_maxima_meses))

    def _calcular_pena_definitiva(self, pena_intermediaria_meses: int, ajustes: List[AjusteFase3]) -> int:
        pena = pena_intermediaria_meses
        for a in ajustes:
            variacao = int(pena * a.fracao_numerador / a.fracao_denominador)
            if a.aumentar:
                pena += variacao
            else:
                pena -= variacao
        return max(pena, 1)

    def _formatar_pena(self, meses: int) -> str:
        anos = meses // 12
        meses_restantes = meses % 12
        partes = []
        if anos > 0:
            partes.append(f"{anos} ano{'s' if anos > 1 else ''}")
        if meses_restantes > 0:
            partes.append(f"{meses_restantes} {'meses' if meses_restantes > 1 else 'mês'}")
        return " e ".join(partes) if partes else "0 meses"