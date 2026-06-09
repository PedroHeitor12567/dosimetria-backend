from typing import List

from src.domain.entities.dosimetria import CircustanciaJudicial, AjusteLegal, AjusteFase3, ResultadoDosimetria, \
    TipoAjuste

DIAS_POR_MES = 30

class DosimetriaDomainService:
    def calcular(self, pena_minima_anos: float, pena_maxima_anos: float, circunstancias_desfavoraveis: List[CircustanciaJudicial], ajustes_fase2: List[AjusteLegal], ajustes_fase3: List[AjusteFase3],) -> ResultadoDosimetria:
        pena_minima_dias = int(pena_minima_anos * 12 * DIAS_POR_MES)
        pena_maxima_dias = int(pena_maxima_anos * 12 * DIAS_POR_MES)

        pena_base_dias = self._calcular_pena_base(
            pena_minima_dias, pena_maxima_dias, circunstancias_desfavoraveis
        )

        pena_intermediaria_dias = self._calcular_pena_intermediaria(
            pena_base_dias, pena_minima_dias, pena_maxima_dias, ajustes_fase2
        )

        pena_definitiva_dias = self._calcular_pena_definitiva(
            pena_intermediaria_dias, ajustes_fase3
        )

        return ResultadoDosimetria(
            pena_minima_meses=pena_minima_dias // DIAS_POR_MES,
            pena_maxima_meses=pena_maxima_dias // DIAS_POR_MES,
            circunstancias_desfavoraveis=[c.value for c in circunstancias_desfavoraveis],
            pena_base_meses=pena_base_dias // DIAS_POR_MES,
            pena_base_dias=pena_base_dias,
            ajustes_fase2=ajustes_fase2,
            pena_intermediaria_meses=pena_intermediaria_dias // DIAS_POR_MES,
            pena_intermediaria_dias=pena_intermediaria_dias,
            ajustes_fase3=ajustes_fase3,
            pena_definitiva_meses=pena_definitiva_dias // DIAS_POR_MES,
            pena_definitiva_dias=pena_definitiva_dias,
            pena_definitiva_anos=round(pena_definitiva_dias / (12 * DIAS_POR_MES), 2),
            pena_definitiva_formatada=self._formatar_pena(pena_definitiva_dias),
        )

    def _calcular_pena_base(self, pena_minima_dias, pena_maxima_dias, circunstancias_desfavoraveis):
        diferenca = pena_maxima_dias - pena_minima_dias
        incremento = (diferenca / 8) * len(circunstancias_desfavoraveis)
        return int(round(pena_minima_dias + incremento))

    def _calcular_pena_intermediaria(self, pena_base_dias, pena_minima_dias, pena_maxima_dias, ajustes):
        pena = pena_base_dias
        for ajuste in ajustes:
            variacao = pena_base_dias // 6
            pena += variacao if ajuste.tipo == TipoAjuste.AGRAVANTE else -variacao
        return max(pena_minima_dias, min(pena, pena_maxima_dias))

    def _calcular_pena_definitiva(self, pena_intermediaria_dias, ajustes):
        pena = pena_intermediaria_dias
        for ajuste in ajustes:
            variacao = int(pena * ajuste.fracao_numerador / ajuste.fracao_denominador)
            pena += variacao if ajuste.aumentar else -variacao
        return max(pena, 1)

    def _formatar_pena(self, dias: int) -> str:
        anos = dias // 360
        resto = dias % 360
        meses = resto // 30
        dias_restantes = resto % 30
        partes = []
        if anos > 0:
            partes.append(f"{anos} ano{'s' if anos > 1 else ''}")
        if meses > 0:
            partes.append(f"{meses} {'meses' if meses > 1 else 'mês'}")
        if dias_restantes > 0:
            partes.append(f"{dias_restantes} dia{'s' if dias_restantes > 1 else ''}")
        return " e ".join(partes) if partes else "0 dias"
