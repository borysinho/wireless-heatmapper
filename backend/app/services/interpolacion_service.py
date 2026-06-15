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
    """Genera matrices RSSI mediante IDW o kriging ordinario determinístico."""

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
        if algoritmo_normalizado == "KRIGING":
            return self._kriging_ordinario(
                puntos=puntos,
                ancho_px=ancho_px,
                alto_px=alto_px,
                resolucion=resolucion,
            )
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

    def _kriging_ordinario(
        self,
        *,
        puntos: list[PuntoRSSI],
        ancho_px: int,
        alto_px: int,
        resolucion: int,
    ) -> list[list[float]]:
        if len(puntos) < 3:
            return self._idw(
                puntos=puntos,
                ancho_px=ancho_px,
                alto_px=alto_px,
                resolucion=resolucion,
            )

        valores = [p.rssi for p in puntos]
        media = sum(valores) / len(valores)
        varianza = sum((valor - media) ** 2 for valor in valores) / len(valores)
        sill = max(varianza, 1.0)
        alcance = max(ancho_px, alto_px) * 0.35
        nugget = sill * 0.02

        try:
            coeficientes = self._coeficientes_kriging(
                puntos=puntos,
                valores=valores,
                sill=sill,
                alcance=alcance,
                nugget=nugget,
            )
        except ValueError:
            return self._idw(
                puntos=puntos,
                ancho_px=ancho_px,
                alto_px=alto_px,
                resolucion=resolucion,
            )

        minimo = max(-120.0, min(valores) - 8.0)
        maximo = min(0.0, max(valores) + 8.0)
        matriz: list[list[float]] = []
        for fila in range(resolucion):
            y = ((fila + 0.5) / resolucion) * alto_px
            valores_fila: list[float] = []
            for col in range(resolucion):
                x = ((col + 0.5) / resolucion) * ancho_px
                valor = coeficientes[-1]
                for idx, punto in enumerate(puntos):
                    distancia = math.hypot(x - punto.x, y - punto.y)
                    valor += coeficientes[idx] * self._covarianza_exponencial(
                        distancia=distancia,
                        sill=sill,
                        alcance=alcance,
                    )
                valores_fila.append(round(max(minimo, min(maximo, valor)), 2))
            matriz.append(valores_fila)
        return matriz

    def _coeficientes_kriging(
        self,
        *,
        puntos: list[PuntoRSSI],
        valores: list[float],
        sill: float,
        alcance: float,
        nugget: float,
    ) -> list[float]:
        n = len(puntos)
        matriz = [[0.0 for _ in range(n + 1)] for _ in range(n + 1)]
        for i, punto_i in enumerate(puntos):
            for j, punto_j in enumerate(puntos):
                distancia = math.hypot(punto_i.x - punto_j.x, punto_i.y - punto_j.y)
                matriz[i][j] = self._covarianza_exponencial(
                    distancia=distancia,
                    sill=sill,
                    alcance=alcance,
                )
                if i == j:
                    matriz[i][j] += nugget
            matriz[i][n] = 1.0
            matriz[n][i] = 1.0

        rhs = [*valores, 0.0]
        return self._resolver_sistema_lineal(matriz, rhs)

    def _covarianza_exponencial(
        self,
        *,
        distancia: float,
        sill: float,
        alcance: float,
    ) -> float:
        return sill * math.exp(-distancia / max(alcance, 1e-9))

    def _resolver_sistema_lineal(
        self,
        matriz: list[list[float]],
        rhs: list[float],
    ) -> list[float]:
        n = len(rhs)
        a = [fila[:] for fila in matriz]
        b = rhs[:]
        epsilon = 1e-12

        for col in range(n):
            pivote = max(range(col, n), key=lambda fila: abs(a[fila][col]))
            if abs(a[pivote][col]) < epsilon:
                raise ValueError("Sistema singular para kriging.")
            if pivote != col:
                a[col], a[pivote] = a[pivote], a[col]
                b[col], b[pivote] = b[pivote], b[col]

            valor_pivote = a[col][col]
            for fila in range(col + 1, n):
                factor = a[fila][col] / valor_pivote
                if factor == 0:
                    continue
                a[fila][col] = 0.0
                for k in range(col + 1, n):
                    a[fila][k] -= factor * a[col][k]
                b[fila] -= factor * b[col]

        x = [0.0 for _ in range(n)]
        for fila in range(n - 1, -1, -1):
            suma = sum(a[fila][col] * x[col] for col in range(fila + 1, n))
            x[fila] = (b[fila] - suma) / a[fila][fila]
        return x


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
