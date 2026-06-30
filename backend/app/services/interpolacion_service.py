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
    {"desde": -70, "hasta": 0, "color": "#A7E84A", "etiqueta": "Óptimo"},
    {"desde": -80, "hasta": -71, "color": "#F1E64A", "etiqueta": "Aceptable"},
    {"desde": -85, "hasta": -81, "color": "#C7B84B", "etiqueta": "Pobre"},
    {"desde": -90, "hasta": -86, "color": "#7E8173", "etiqueta": "Muy pobre"},
    {"desde": -120, "hasta": -91, "color": "#1C1C1C", "etiqueta": "Zona muerta"},
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
        distancia_celda = max(ancho_px / resolucion, alto_px / resolucion)

        for fila in range(resolucion):
            y = ((fila + 0.5) / resolucion) * alto_px
            valores_fila: list[float] = []
            for col in range(resolucion):
                x = ((col + 0.5) / resolucion) * ancho_px
                numerador = 0.0
                denominador = 0.0
                valor_directo: float | None = None
                vecinos: list[tuple[float, float]] = []
                for punto_x, punto_y, punto_rssi in puntos_base:
                    dx = x - punto_x
                    dy = y - punto_y
                    distancia_cuadrado = dx * dx + dy * dy
                    vecinos.append((distancia_cuadrado, punto_rssi))
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
                if valor_directo is None:
                    valor = self._aplicar_soporte_local(
                        valor=valor,
                        vecinos=vecinos,
                        distancia_celda=distancia_celda,
                    )
                valores_fila.append(round(max(-120.0, min(0.0, valor)), 2))
            matriz.append(valores_fila)
        return matriz

    def _aplicar_soporte_local(
        self,
        *,
        valor: float,
        vecinos: list[tuple[float, float]],
        distancia_celda: float,
    ) -> float:
        """Evita islas optimistas causadas por un único punto bueno aislado."""
        if len(vecinos) < 3:
            return valor
        vecinos_ordenados = sorted(vecinos, key=lambda item: item[0])[:4]
        distancia_mas_cercana = vecinos_ordenados[0][0] ** 0.5
        if distancia_mas_cercana <= distancia_celda * 1.5:
            return valor

        reglas = [
            (-70.0, -71.0),
            (-80.0, -81.0),
            (-85.0, -86.0),
        ]
        ajustado = valor
        for umbral, limite in reglas:
            if ajustado >= umbral:
                soporte = sum(1 for _, rssi in vecinos_ordenados if rssi >= umbral)
                if soporte < 2:
                    ajustado = min(ajustado, limite)
        return ajustado


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
                    destino = (167, 232, 74)
                else:
                    base = (255, 255, 255)
                    destino = (126, 129, 115)
                color = tuple(
                    round(base[canal] + (destino[canal] - base[canal]) * intensidad)
                    for canal in range(3)
                )
                pix[x, y] = (*color, alpha)

        buffer = BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()

    def _color_para_rssi(self, rssi: float) -> tuple[int, int, int]:
        if rssi >= -70:
            return (167, 232, 74)
        if rssi >= -80:
            return (241, 230, 74)
        if rssi >= -85:
            return (199, 184, 75)
        if rssi >= -90:
            return (126, 129, 115)
        return (28, 28, 28)
