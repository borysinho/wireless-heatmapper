"""Servicios de interpolación y render de heatmaps.

Sprint 4 — PB-05.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from io import BytesIO

from PIL import Image


@dataclass(frozen=True)
class PuntoRSSI:
    punto_id: int
    x: float
    y: float
    rssi: float


ESCALA_CWNA = [
    {"desde": -50, "hasta": 0, "color": "#0B7A3B", "etiqueta": "Excelente"},
    {"desde": -70, "hasta": -51, "color": "#57B65A", "etiqueta": "Buena"},
    {"desde": -80, "hasta": -71, "color": "#F4D35E", "etiqueta": "Aceptable"},
    {"desde": -90, "hasta": -81, "color": "#F08A24", "etiqueta": "Débil"},
    {"desde": -120, "hasta": -91, "color": "#D7263D", "etiqueta": "Zona muerta"},
]


class InterpolacionService:
    """Genera matrices RSSI mediante IDW.

    Kriging queda expuesto como opción de contrato y usa IDW como baseline
    determinístico hasta integrar `pykrige` en un sprint técnico posterior.
    """

    def interpolar(
        self,
        *,
        puntos: list[PuntoRSSI],
        ancho_px: int,
        alto_px: int,
        resolucion: int,
        algoritmo: str,
    ) -> list[list[float]]:
        algoritmo_normalizado = algoritmo.upper()
        if algoritmo_normalizado not in {"IDW", "KRIGING"}:
            raise ValueError("Algoritmo no soportado.")
        return self._idw(
            puntos=puntos,
            ancho_px=ancho_px,
            alto_px=alto_px,
            resolucion=resolucion,
        )

    def _idw(
        self,
        *,
        puntos: list[PuntoRSSI],
        ancho_px: int,
        alto_px: int,
        resolucion: int,
    ) -> list[list[float]]:
        matriz: list[list[float]] = []
        potencia = 2.0
        epsilon = 1e-9

        for fila in range(resolucion):
            y = ((fila + 0.5) / resolucion) * alto_px
            valores_fila: list[float] = []
            for col in range(resolucion):
                x = ((col + 0.5) / resolucion) * ancho_px
                numerador = 0.0
                denominador = 0.0
                valor_directo: float | None = None
                for punto in puntos:
                    dist = math.hypot(x - punto.x, y - punto.y)
                    if dist < epsilon:
                        valor_directo = punto.rssi
                        break
                    peso = 1 / (dist**potencia)
                    numerador += peso * punto.rssi
                    denominador += peso
                valor = (
                    valor_directo
                    if valor_directo is not None
                    else numerador / denominador
                )
                valores_fila.append(round(max(-120.0, min(0.0, valor)), 2))
            matriz.append(valores_fila)
        return matriz


class HeatmapImageService:
    """Renderiza una matriz RSSI como PNG RGBA translúcido."""

    def render_png(self, matriz: list[list[float]], *, alpha: int = 153) -> bytes:
        alto = len(matriz)
        ancho = len(matriz[0]) if alto else 0
        image = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
        pix = image.load()
        for y, fila in enumerate(matriz):
            for x, rssi in enumerate(fila):
                r, g, b = self._color_para_rssi(rssi)
                pix[x, y] = (r, g, b, alpha)

        buffer = BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()

    def _color_para_rssi(self, rssi: float) -> tuple[int, int, int]:
        if rssi >= -50:
            return (11, 122, 59)
        if rssi >= -70:
            return (87, 182, 90)
        if rssi >= -80:
            return (244, 211, 94)
        if rssi >= -90:
            return (240, 138, 36)
        return (215, 38, 61)
