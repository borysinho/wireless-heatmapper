"""Servicios de interpolación y render de heatmaps.

Sprint 4 — PB-05.
"""

from __future__ import annotations

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
    {"desde": -60, "hasta": 0, "color": "#0B7A3B", "etiqueta": "Excelente"},
    {"desde": -67, "hasta": -61, "color": "#57B65A", "etiqueta": "Muy buena"},
    {"desde": -70, "hasta": -68, "color": "#F4D35E", "etiqueta": "Objetivo mínimo"},
    {"desde": -75, "hasta": -71, "color": "#F08A24", "etiqueta": "Inestable"},
    {"desde": -80, "hasta": -76, "color": "#D95D39", "etiqueta": "Débil"},
    {"desde": -90, "hasta": -81, "color": "#B91C1C", "etiqueta": "Muy débil"},
    {"desde": -120, "hasta": -91, "color": "#D7263D", "etiqueta": "Zona muerta"},
]


class InterpolacionService:
    """Genera matrices RSSI mediante IDW."""

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
        if algoritmo_normalizado != "IDW":
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
        epsilon_cuadrado = 1e-18
        puntos_base = [(punto.x, punto.y, punto.rssi) for punto in puntos]

        for fila in range(resolucion):
            y = ((fila + 0.5) / resolucion) * alto_px
            valores_fila: list[float] = []
            for col in range(resolucion):
                x = ((col + 0.5) / resolucion) * ancho_px
                numerador = 0.0
                denominador = 0.0
                valor_directo: float | None = None
                for punto_x, punto_y, punto_rssi in puntos_base:
                    dx = x - punto_x
                    dy = y - punto_y
                    distancia_cuadrado = dx * dx + dy * dy
                    if distancia_cuadrado < epsilon_cuadrado:
                        valor_directo = punto_rssi
                        break
                    peso = 1 / distancia_cuadrado
                    numerador += peso * punto_rssi
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

    def render_png(
        self,
        matriz: list[list[float]],
        *,
        alpha: int = 153,
        mascara: list[list[bool]] | None = None,
    ) -> bytes:
        alto = len(matriz)
        ancho = len(matriz[0]) if alto else 0
        image = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
        pix = image.load()
        for y, fila in enumerate(matriz):
            for x, rssi in enumerate(fila):
                if mascara is not None and not mascara[y][x]:
                    pix[x, y] = (0, 0, 0, 0)
                    continue
                r, g, b = self._color_para_rssi(rssi)
                pix[x, y] = (r, g, b, alpha)

        buffer = BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()

    def render_diferencia_png(
        self,
        matriz: list[list[float]],
        *,
        alpha: int = 180,
    ) -> bytes:
        """Renderiza deltas RSSI con paleta divergente rojo-blanco-verde."""
        alto = len(matriz)
        ancho = len(matriz[0]) if alto else 0
        image = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
        pix = image.load()
        for y, fila in enumerate(matriz):
            for x, delta in enumerate(fila):
                intensidad = min(1.0, abs(delta) / 20.0)
                if delta >= 0:
                    base = (255, 255, 255)
                    destino = (11, 122, 59)
                else:
                    base = (255, 255, 255)
                    destino = (215, 38, 61)
                color = tuple(
                    round(base[canal] + (destino[canal] - base[canal]) * intensidad)
                    for canal in range(3)
                )
                pix[x, y] = (*color, alpha)

        buffer = BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()

    def _color_para_rssi(self, rssi: float) -> tuple[int, int, int]:
        if rssi >= -60:
            return (11, 122, 59)
        if rssi >= -67:
            return (87, 182, 90)
        if rssi >= -70:
            return (244, 211, 94)
        if rssi >= -75:
            return (240, 138, 36)
        if rssi >= -80:
            return (217, 93, 57)
        if rssi >= -90:
            return (185, 28, 28)
        return (215, 38, 61)
