"""Utilidades geométricas para áreas de interés sobre planos."""

from __future__ import annotations

from collections.abc import Iterable

PuntoPoligono = dict[str, float]


def normalizar_poligono(puntos: Iterable[dict]) -> list[PuntoPoligono]:
    """Devuelve vértices `{x, y}` sin duplicar el cierre explícito."""

    normalizados = [
        {"x": round(float(punto["x"]), 4), "y": round(float(punto["y"]), 4)}
        for punto in puntos
    ]
    if len(normalizados) > 1 and normalizados[0] == normalizados[-1]:
        normalizados.pop()
    return normalizados


def area_poligono(puntos: list[PuntoPoligono]) -> float:
    if len(puntos) < 3:
        return 0.0
    suma = 0.0
    for idx, punto in enumerate(puntos):
        siguiente = puntos[(idx + 1) % len(puntos)]
        suma += punto["x"] * siguiente["y"] - siguiente["x"] * punto["y"]
    return abs(suma) / 2


def punto_en_poligono(x: float, y: float, poligono: list[PuntoPoligono]) -> bool:
    """Ray casting con bordes incluidos para coordenadas de plano."""

    if len(poligono) < 3:
        return True
    dentro = False
    j = len(poligono) - 1
    for i, punto_i in enumerate(poligono):
        punto_j = poligono[j]
        xi, yi = punto_i["x"], punto_i["y"]
        xj, yj = punto_j["x"], punto_j["y"]
        if _punto_en_segmento(x, y, xi, yi, xj, yj):
            return True
        cruza = (yi > y) != (yj > y)
        if cruza:
            x_interseccion = (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi
            if x <= x_interseccion:
                dentro = not dentro
        j = i
    return dentro


def mascara_poligono(
    *,
    poligono: list[PuntoPoligono] | None,
    ancho_px: int,
    alto_px: int,
    resolucion: int,
) -> list[list[bool]] | None:
    if not poligono or len(poligono) < 3:
        return None
    mascara: list[list[bool]] = []
    for fila in range(resolucion):
        y = ((fila + 0.5) / resolucion) * alto_px
        valores_fila: list[bool] = []
        for col in range(resolucion):
            x = ((col + 0.5) / resolucion) * ancho_px
            valores_fila.append(punto_en_poligono(x, y, poligono))
        mascara.append(valores_fila)
    return mascara


def _punto_en_segmento(
    px: float,
    py: float,
    ax: float,
    ay: float,
    bx: float,
    by: float,
) -> bool:
    cruz = (py - ay) * (bx - ax) - (px - ax) * (by - ay)
    if abs(cruz) > 1e-7:
        return False
    dot = (px - ax) * (bx - ax) + (py - ay) * (by - ay)
    if dot < 0:
        return False
    largo_sq = (bx - ax) ** 2 + (by - ay) ** 2
    return dot <= largo_sq
