"""Optimizador de APs Sprint 5 — PB-07."""

from __future__ import annotations

import math
from dataclasses import dataclass

from app.ai.modelo_propagacion import ModeloPropagacion
from app.services.interpolacion_service import PuntoRSSI


@dataclass(frozen=True)
class AlternativaOptimizada:
    nombre: str
    banda: str
    modelo_ap: str
    pct_cobertura_actual: float
    pct_cobertura: float
    costo_estimado: float
    cantidad_aps: int
    resumen: str
    metricas: dict
    recomendaciones: list[dict]
    matriz: list[list[float]]


class OptimizadorAPService:
    """Greedy + búsqueda local sobre una grilla del plano."""

    def __init__(self, modelo: ModeloPropagacion | None = None) -> None:
        self._modelo = modelo or ModeloPropagacion()

    def optimizar(
        self,
        *,
        puntos_actuales: list[PuntoRSSI],
        matriz_actual: list[list[float]],
        ancho_px: int,
        alto_px: int,
        metros_por_pixel: float,
        max_aps: int,
        presupuesto: float | None,
        banda: str,
        modelo_ap: str,
        costo_unitario: float,
        resolucion: int,
    ) -> list[AlternativaOptimizada]:
        if not puntos_actuales:
            raise ValueError("Se requieren puntos de medición para optimizar.")

        cantidad_max = max(1, max_aps)

        pct_actual = self._pct_cobertura(matriz_actual)
        candidatos = self._candidatos(
            puntos=puntos_actuales,
            ancho_px=ancho_px,
            alto_px=alto_px,
        )
        alternativas: list[AlternativaOptimizada] = []
        for cantidad in range(1, cantidad_max + 1):
            seleccionados = self._greedy(
                candidatos=candidatos,
                cantidad=cantidad,
                ancho_px=ancho_px,
                alto_px=alto_px,
                metros_por_pixel=metros_por_pixel,
                banda=banda,
                resolucion=resolucion,
            )
            seleccionados = self._busqueda_local(
                seleccionados=seleccionados,
                ancho_px=ancho_px,
                alto_px=alto_px,
                metros_por_pixel=metros_por_pixel,
                banda=banda,
                resolucion=resolucion,
            )
            matriz_proyectada = self._matriz_desde_aps(
                aps=seleccionados,
                ancho_px=ancho_px,
                alto_px=alto_px,
                metros_por_pixel=metros_por_pixel,
                banda=banda,
                resolucion=resolucion,
            )
            pct = self._pct_cobertura(matriz_proyectada)
            costo = 0.0
            recomendaciones = [
                self._recomendacion(
                    orden=idx,
                    x=x,
                    y=y,
                    banda=banda,
                    modelo_ap=modelo_ap,
                    costo_unitario=0,
                    puntos=puntos_actuales,
                    metros_por_pixel=metros_por_pixel,
                )
                for idx, (x, y) in enumerate(seleccionados, start=1)
            ]
            alternativas.append(
                AlternativaOptimizada(
                    nombre=f"Alternativa {cantidad}",
                    banda=banda,
                    modelo_ap="AP empresarial de potencia ajustable",
                    pct_cobertura_actual=pct_actual,
                    pct_cobertura=pct,
                    costo_estimado=costo,
                    cantidad_aps=cantidad,
                    resumen=(
                        f"Con {cantidad} AP(s) de potencia ajustable en banda "
                        f"{banda} GHz se proyecta {pct:.1f}% de cobertura >= -70 dBm."
                    ),
                    metricas={
                        "pct_cobertura_actual": pct_actual,
                        "pct_cobertura_proyectada": pct,
                        "mejora_pct": round(pct - pct_actual, 2),
                        "zonas_muertas_proyectadas": self._zonas_muertas(matriz_proyectada),
                    },
                    recomendaciones=recomendaciones,
                    matriz=matriz_proyectada,
                )
            )
        return sorted(
            alternativas,
            key=lambda item: (-item.pct_cobertura, item.cantidad_aps),
        )[:3]

    def _candidatos(
        self,
        *,
        puntos: list[PuntoRSSI],
        ancho_px: int,
        alto_px: int,
    ) -> list[tuple[float, float]]:
        criticos = sorted(puntos, key=lambda p: p.rssi)[: max(6, len(puntos) // 3)]
        candidatos = [(p.x, p.y) for p in criticos]
        for x_frac in (0.2, 0.5, 0.8):
            for y_frac in (0.2, 0.5, 0.8):
                candidatos.append((ancho_px * x_frac, alto_px * y_frac))
        unicos: list[tuple[float, float]] = []
        for x, y in candidatos:
            coord = (round(max(0, min(ancho_px, x)), 2), round(max(0, min(alto_px, y)), 2))
            if coord not in unicos:
                unicos.append(coord)
        return unicos

    def _greedy(
        self,
        *,
        candidatos: list[tuple[float, float]],
        cantidad: int,
        ancho_px: int,
        alto_px: int,
        metros_por_pixel: float,
        banda: str,
        resolucion: int,
    ) -> list[tuple[float, float]]:
        seleccionados: list[tuple[float, float]] = []
        restantes = candidatos[:]
        while len(seleccionados) < cantidad and restantes:
            mejor = max(
                restantes,
                key=lambda c: self._pct_cobertura(
                    self._matriz_desde_aps(
                        aps=[*seleccionados, c],
                        ancho_px=ancho_px,
                        alto_px=alto_px,
                        metros_por_pixel=metros_por_pixel,
                        banda=banda,
                        resolucion=resolucion,
                    )
                ),
            )
            seleccionados.append(mejor)
            restantes.remove(mejor)
        return seleccionados

    def _busqueda_local(
        self,
        *,
        seleccionados: list[tuple[float, float]],
        ancho_px: int,
        alto_px: int,
        metros_por_pixel: float,
        banda: str,
        resolucion: int,
    ) -> list[tuple[float, float]]:
        paso = max(20.0, min(ancho_px, alto_px) * 0.08)
        actuales = seleccionados[:]
        for idx, (x, y) in enumerate(actuales):
            vecinos = [
                (x, y),
                (x - paso, y),
                (x + paso, y),
                (x, y - paso),
                (x, y + paso),
            ]
            vecinos = [
                (round(max(0, min(ancho_px, vx)), 2), round(max(0, min(alto_px, vy)), 2))
                for vx, vy in vecinos
            ]
            actuales[idx] = max(
                vecinos,
                key=lambda c: self._pct_cobertura(
                    self._matriz_desde_aps(
                        aps=[*actuales[:idx], c, *actuales[idx + 1 :]],
                        ancho_px=ancho_px,
                        alto_px=alto_px,
                        metros_por_pixel=metros_por_pixel,
                        banda=banda,
                        resolucion=resolucion,
                    )
                ),
            )
        return actuales

    def _matriz_desde_aps(
        self,
        *,
        aps: list[tuple[float, float]],
        ancho_px: int,
        alto_px: int,
        metros_por_pixel: float,
        banda: str,
        resolucion: int,
    ) -> list[list[float]]:
        matriz: list[list[float]] = []
        for fila in range(resolucion):
            y = ((fila + 0.5) / resolucion) * alto_px
            valores_fila: list[float] = []
            for col in range(resolucion):
                x = ((col + 0.5) / resolucion) * ancho_px
                mejor = max(
                    self._modelo.predecir_rssi(
                        distancia_px=math.hypot(x - ap_x, y - ap_y),
                        metros_por_pixel=metros_por_pixel,
                        banda=banda,
                    )
                    for ap_x, ap_y in aps
                )
                valores_fila.append(mejor)
            matriz.append(valores_fila)
        return matriz

    def _recomendacion(
        self,
        *,
        orden: int,
        x: float,
        y: float,
        banda: str,
        modelo_ap: str,
        costo_unitario: float,
        puntos: list[PuntoRSSI],
        metros_por_pixel: float,
    ) -> dict:
        punto_critico = min(puntos, key=lambda p: math.hypot(p.x - x, p.y - y))
        distancia_m = math.hypot(punto_critico.x - x, punto_critico.y - y) * metros_por_pixel
        rssi = self._modelo.predecir_rssi(
            distancia_px=math.hypot(punto_critico.x - x, punto_critico.y - y),
            metros_por_pixel=metros_por_pixel,
            banda=banda,
        )
        return {
            "accion": "AGREGAR",
            "coord_x": round(x, 2),
            "coord_y": round(y, 2),
            "banda": banda,
            "modelo_ap": "AP empresarial de potencia ajustable",
            "costo_estimado": 0,
            "rssi_proyectado": rssi,
            "justificacion": (
                f"AP {orden}: ubicar un equipo con potencia TX ajustable y "
                f"capacidad para mantener RSSI proyectado {rssi:.1f} dBm "
                f"en una zona crítica a {distancia_m:.1f} m. Debe permitir "
                f"regular potencia para evitar solapamiento excesivo, operar "
                f"en banda {banda} GHz, usar antenas adecuadas al área y "
                f"soportar gestión centralizada. Objetivo de diseño: >= -70 dBm."
            ),
        }

    def _pct_cobertura(self, matriz: list[list[float]]) -> float:
        valores = [valor for fila in matriz for valor in fila]
        if not valores:
            return 0.0
        cubiertas = sum(1 for valor in valores if valor >= -70)
        return round(cubiertas * 100 / len(valores), 2)

    def _zonas_muertas(self, matriz: list[list[float]]) -> int:
        return sum(1 for fila in matriz for valor in fila if valor < -90)
