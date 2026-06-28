"""Servicio de generación asistida de polígonos de interés con Azure OpenAI."""

from __future__ import annotations

import base64
import json
import math
import urllib.error
import urllib.request
from collections import deque
from dataclasses import dataclass
from io import BytesIO
from typing import Any

from PIL import Image, ImageDraw, ImageFilter, ImageOps

from app.core.config import settings


class PoligonoIAConfigError(RuntimeError):
    """La integración de IA no está configurada."""


class PoligonoIAGenerationError(RuntimeError):
    """El modelo no pudo generar una respuesta utilizable."""


@dataclass(frozen=True)
class ImagenModelo:
    bytes_png: bytes
    ancho: int
    alto: int
    crop_x: int
    crop_y: int
    crop_ancho: int
    crop_alto: int


class PoligonoIAService:
    """Genera un polígono operativo desde la imagen del plano.

    El modelo trabaja sobre una imagen reducida para controlar costo y latencia.
    Los puntos se devuelven reescalados a las coordenadas reales del plano.
    """

    api_version = "2025-04-01-preview"

    def generar_desde_imagen(
        self,
        *,
        imagen_bytes: bytes,
        ancho_original: int,
        alto_original: int,
    ) -> list[dict[str, float]]:
        self._validar_configuracion()
        poligono_exterior = self._generar_poligono_exterior(
            imagen_bytes=imagen_bytes,
            ancho_original=ancho_original,
            alto_original=alto_original,
        )
        imagen_modelo = self._preparar_imagen(imagen_bytes)
        payload = self._payload(
            imagen_png=imagen_modelo.bytes_png,
            ancho_modelo=imagen_modelo.ancho,
            alto_modelo=imagen_modelo.alto,
        )
        data = self._post_responses(payload)
        contenido = self._extraer_texto(data)
        puntos_modelo = self._parsear_puntos(contenido)
        poligono_modelo = self._reescalar_puntos(
            puntos=puntos_modelo,
            imagen_modelo=imagen_modelo,
            ancho_original=ancho_original,
            alto_original=alto_original,
        )
        return self._elegir_poligono_exterior(
            poligono_modelo=poligono_modelo,
            poligono_exterior=poligono_exterior,
        )

    def _validar_configuracion(self) -> None:
        if not settings.azure_openai_api_key.strip():
            raise PoligonoIAConfigError("Falta AZURE_OPENAI_API_KEY.")
        if not settings.azure_openai_endpoint.strip():
            raise PoligonoIAConfigError("Falta AZURE_OPENAI_ENDPOINT.")
        if not settings.azure_openai_poligono_deployment.strip():
            raise PoligonoIAConfigError("Falta AZURE_OPENAI_POLIGONO_DEPLOYMENT.")

    def _preparar_imagen(self, imagen_bytes: bytes) -> ImagenModelo:
        max_px = max(256, settings.azure_openai_poligono_max_px)
        with Image.open(BytesIO(imagen_bytes)) as imagen:
            imagen = imagen.convert("RGB")
            crop_box = self._detectar_bbox_contenido(imagen)
            crop = imagen.crop(crop_box)
            crop_ancho, crop_alto = crop.size
            crop.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
            self._anotar_imagen_modelo(crop)
            salida = BytesIO()
            crop.save(salida, format="PNG", optimize=True)
            return ImagenModelo(
                bytes_png=salida.getvalue(),
                ancho=crop.width,
                alto=crop.height,
                crop_x=crop_box[0],
                crop_y=crop_box[1],
                crop_ancho=crop_ancho,
                crop_alto=crop_alto,
            )

    def _detectar_bbox_contenido(self, imagen: Image.Image) -> tuple[int, int, int, int]:
        """Recorta márgenes claros para que la IA no genere el marco del lienzo."""

        ancho, alto = imagen.size
        pixeles = imagen.load()
        xs: list[int] = []
        ys: list[int] = []
        for y in range(alto):
            for x in range(ancho):
                r, g, b = pixeles[x, y]
                es_muro_o_tinta = r < 235 or g < 235 or b < 235
                es_fondo_azulado_suave = b > 210 and r > 190 and g > 205
                if es_muro_o_tinta and not es_fondo_azulado_suave:
                    xs.append(x)
                    ys.append(y)
        if not xs or not ys:
            return (0, 0, ancho, alto)

        x0, x1 = min(xs), max(xs)
        y0, y1 = min(ys), max(ys)
        margen = max(8, int(min(ancho, alto) * 0.025))
        return (
            max(0, x0 - margen),
            max(0, y0 - margen),
            min(ancho, x1 + margen + 1),
            min(alto, y1 + margen + 1),
        )

    def _anotar_imagen_modelo(self, imagen: Image.Image) -> None:
        draw = ImageDraw.Draw(imagen)
        color = (220, 0, 0)
        for inset in range(3):
            draw.rectangle(
                (
                    inset,
                    inset,
                    imagen.width - 1 - inset,
                    imagen.height - 1 - inset,
                ),
                outline=color,
            )

    def _generar_poligono_exterior(
        self,
        *,
        imagen_bytes: bytes,
        ancho_original: int,
        alto_original: int,
    ) -> list[dict[str, float]]:
        with Image.open(BytesIO(imagen_bytes)) as imagen_original:
            imagen_original = imagen_original.convert("RGB")
            crop_box = self._detectar_bbox_contenido(imagen_original)
            crop = imagen_original.crop(crop_box)
            factor = 1.0
            max_px = 900
            if max(crop.size) > max_px:
                factor = max_px / max(crop.size)
                crop = crop.resize(
                    (
                        max(1, int(crop.width * factor)),
                        max(1, int(crop.height * factor)),
                    ),
                    Image.Resampling.LANCZOS,
                )

            mascara = self._mascara_huella_edificio(crop)
            puntos_crop = self._poligono_desde_mascara(mascara)
            if len(puntos_crop) < 3:
                return []

            inv_factor = 1 / factor
            return [
                {
                    "x": round(
                        max(
                            0.0,
                            min(ancho_original, crop_box[0] + punto[0] * inv_factor),
                        ),
                        2,
                    ),
                    "y": round(
                        max(
                            0.0,
                            min(alto_original, crop_box[1] + punto[1] * inv_factor),
                        ),
                        2,
                    ),
                }
                for punto in puntos_crop
            ]

    def _mascara_huella_edificio(self, imagen: Image.Image) -> Image.Image:
        gris = ImageOps.grayscale(imagen)
        tinta = gris.point(lambda px: 255 if px < 225 else 0, mode="L")
        filtro = self._kernel_morfologico(imagen.size)
        barrera = tinta.filter(ImageFilter.MaxFilter(filtro))
        barrera = barrera.filter(ImageFilter.MinFilter(filtro))
        barrera = barrera.filter(ImageFilter.MaxFilter(filtro))

        ancho, alto = barrera.size
        datos = barrera.load()
        exterior = bytearray(ancho * alto)
        cola: deque[tuple[int, int]] = deque()

        def agregar(x: int, y: int) -> None:
            idx = y * ancho + x
            if exterior[idx] or datos[x, y] != 0:
                return
            exterior[idx] = 1
            cola.append((x, y))

        for x in range(ancho):
            agregar(x, 0)
            agregar(x, alto - 1)
        for y in range(alto):
            agregar(0, y)
            agregar(ancho - 1, y)

        while cola:
            x, y = cola.popleft()
            if x > 0:
                agregar(x - 1, y)
            if x < ancho - 1:
                agregar(x + 1, y)
            if y > 0:
                agregar(x, y - 1)
            if y < alto - 1:
                agregar(x, y + 1)

        salida = Image.new("L", (ancho, alto), 0)
        salida_px = salida.load()
        area = 0
        for y in range(alto):
            for x in range(ancho):
                if exterior[y * ancho + x] == 0:
                    salida_px[x, y] = 255
                    area += 1

        ratio = area / max(1, ancho * alto)
        if ratio < 0.18 or ratio > 0.92:
            salida = barrera.filter(ImageFilter.MaxFilter(filtro))
        return self._mayor_componente(salida)

    def _kernel_morfologico(self, size: tuple[int, int]) -> int:
        base = max(5, int(min(size) * 0.035))
        return base + 1 if base % 2 == 0 else base

    def _mayor_componente(self, mascara: Image.Image) -> Image.Image:
        ancho, alto = mascara.size
        datos = mascara.load()
        visitado = bytearray(ancho * alto)
        mejor: list[tuple[int, int]] = []
        vecinos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

        for y in range(alto):
            for x in range(ancho):
                idx = y * ancho + x
                if visitado[idx] or datos[x, y] == 0:
                    continue
                actual: list[tuple[int, int]] = []
                cola: deque[tuple[int, int]] = deque([(x, y)])
                visitado[idx] = 1
                while cola:
                    cx, cy = cola.popleft()
                    actual.append((cx, cy))
                    for dx, dy in vecinos:
                        nx, ny = cx + dx, cy + dy
                        if nx < 0 or ny < 0 or nx >= ancho or ny >= alto:
                            continue
                        nidx = ny * ancho + nx
                        if visitado[nidx] or datos[nx, ny] == 0:
                            continue
                        visitado[nidx] = 1
                        cola.append((nx, ny))
                if len(actual) > len(mejor):
                    mejor = actual

        salida = Image.new("L", (ancho, alto), 0)
        salida_px = salida.load()
        for x, y in mejor:
            salida_px[x, y] = 255
        return salida

    def _poligono_desde_mascara(self, mascara: Image.Image) -> list[tuple[float, float]]:
        ancho, alto = mascara.size
        datos = mascara.load()
        frontera: list[tuple[int, int]] = []
        relleno: list[tuple[int, int]] = []
        for y in range(1, alto - 1):
            for x in range(1, ancho - 1):
                if datos[x, y] == 0:
                    continue
                relleno.append((x, y))
                if (
                    datos[x - 1, y] == 0
                    or datos[x + 1, y] == 0
                    or datos[x, y - 1] == 0
                    or datos[x, y + 1] == 0
                ):
                    frontera.append((x, y))
        if len(frontera) < 3 or not relleno:
            return []

        cx = sum(x for x, _ in relleno) / len(relleno)
        cy = sum(y for _, y in relleno) / len(relleno)
        bins = 128
        radial: list[tuple[float, int, int] | None] = [None] * bins
        for x, y in frontera:
            angulo = math.atan2(y - cy, x - cx)
            idx = int(((angulo + math.pi) / (2 * math.pi)) * bins) % bins
            dist = (x - cx) ** 2 + (y - cy) ** 2
            if radial[idx] is None or dist > radial[idx][0]:
                radial[idx] = (dist, x, y)

        puntos = [(float(item[1]), float(item[2])) for item in radial if item]
        if len(puntos) < 3:
            return []
        puntos = self._simplificar_cerrado(
            puntos,
            tolerancia=max(4.0, min(ancho, alto) * 0.018),
        )
        return self._limitar_vertices(puntos, max_vertices=18)

    def _simplificar_cerrado(
        self,
        puntos: list[tuple[float, float]],
        *,
        tolerancia: float,
    ) -> list[tuple[float, float]]:
        if len(puntos) <= 3:
            return puntos
        abiertos = puntos + [puntos[0]]
        simplificados = self._rdp(abiertos, tolerancia)[:-1]
        return simplificados if len(simplificados) >= 3 else puntos

    def _rdp(
        self,
        puntos: list[tuple[float, float]],
        tolerancia: float,
    ) -> list[tuple[float, float]]:
        if len(puntos) < 3:
            return puntos
        inicio, fin = puntos[0], puntos[-1]
        max_dist = -1.0
        max_idx = 0
        for idx in range(1, len(puntos) - 1):
            dist = self._distancia_linea(puntos[idx], inicio, fin)
            if dist > max_dist:
                max_dist = dist
                max_idx = idx
        if max_dist <= tolerancia:
            return [inicio, fin]
        izquierda = self._rdp(puntos[: max_idx + 1], tolerancia)
        derecha = self._rdp(puntos[max_idx:], tolerancia)
        return izquierda[:-1] + derecha

    def _distancia_linea(
        self,
        punto: tuple[float, float],
        inicio: tuple[float, float],
        fin: tuple[float, float],
    ) -> float:
        px, py = punto
        x1, y1 = inicio
        x2, y2 = fin
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)
        return abs(dy * px - dx * py + x2 * y1 - y2 * x1) / math.hypot(dx, dy)

    def _limitar_vertices(
        self,
        puntos: list[tuple[float, float]],
        *,
        max_vertices: int,
    ) -> list[tuple[float, float]]:
        if len(puntos) <= max_vertices:
            return puntos
        paso = len(puntos) / max_vertices
        return [puntos[int(idx * paso) % len(puntos)] for idx in range(max_vertices)]

    def _elegir_poligono_exterior(
        self,
        *,
        poligono_modelo: list[dict[str, float]],
        poligono_exterior: list[dict[str, float]],
    ) -> list[dict[str, float]]:
        if len(poligono_exterior) < 3:
            return poligono_modelo
        if len(poligono_modelo) < 3:
            return poligono_exterior
        area_modelo = abs(self._area(poligono_modelo))
        area_exterior = abs(self._area(poligono_exterior))
        if area_modelo < area_exterior * 0.92:
            return poligono_exterior

        bbox_modelo = self._bbox(poligono_modelo)
        bbox_exterior = self._bbox(poligono_exterior)
        ancho_exterior = max(1.0, bbox_exterior[2] - bbox_exterior[0])
        alto_exterior = max(1.0, bbox_exterior[3] - bbox_exterior[1])
        margen_x = ancho_exterior * 0.08
        margen_y = alto_exterior * 0.08
        cubre_bbox = (
            bbox_modelo[0] <= bbox_exterior[0] + margen_x
            and bbox_modelo[1] <= bbox_exterior[1] + margen_y
            and bbox_modelo[2] >= bbox_exterior[2] - margen_x
            and bbox_modelo[3] >= bbox_exterior[3] - margen_y
        )
        return poligono_modelo if cubre_bbox else poligono_exterior

    def _area(self, puntos: list[dict[str, float]]) -> float:
        area = 0.0
        for idx, punto in enumerate(puntos):
            siguiente = puntos[(idx + 1) % len(puntos)]
            area += punto["x"] * siguiente["y"] - siguiente["x"] * punto["y"]
        return area / 2

    def _bbox(self, puntos: list[dict[str, float]]) -> tuple[float, float, float, float]:
        xs = [punto["x"] for punto in puntos]
        ys = [punto["y"] for punto in puntos]
        return (min(xs), min(ys), max(xs), max(ys))

    def _payload(
        self,
        *,
        imagen_png: bytes,
        ancho_modelo: int,
        alto_modelo: int,
    ) -> dict[str, Any]:
        imagen_b64 = base64.b64encode(imagen_png).decode("ascii")
        instrucciones = (
            "Analiza el plano arquitectónico recortado y delimita el área "
            "interior útil donde se generarán heatmaps WiFi. Devuelve "
            "únicamente un JSON válido. Usa coordenadas en píxeles de la "
            "imagen recibida, con "
            f"origen arriba a la izquierda, ancho {ancho_modelo} y alto "
            f"{alto_modelo}. La imagen tiene un borde rojo artificial: NO lo "
            "uses como límite del polígono. No generes un rectángulo de "
            "bounding box. Sigue el contorno de los muros perimetrales oscuros "
            "del edificio, incluyendo entrantes y salientes visibles. Excluye "
            "márgenes blancos, cajetines, leyendas, textos fuera del edificio, "
            "calles, patios externos y fondo. Los vértices deben quedar sobre "
            "o ligeramente dentro del muro exterior, no pegados al borde rojo "
            "salvo que un muro toque realmente ese borde. Si hay duda, prefiere "
            "un polígono conservador dentro del edificio antes que cubrir zonas "
            "vacías. Usa entre 6 y 16 vértices, sin repetir el primer punto al "
            "final."
        )
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "puntos": {
                    "type": "array",
                    "minItems": 6,
                    "maxItems": 16,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                        },
                        "required": ["x", "y"],
                    },
                },
                "confianza": {"type": "number"},
                "razon": {"type": "string"},
            },
            "required": ["puntos", "confianza", "razon"],
        }
        return {
            "model": settings.azure_openai_poligono_deployment,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Eres un asistente de visión para planos WiFi.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": instrucciones},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{imagen_b64}",
                        },
                    ],
                },
            ],
            "max_output_tokens": 1200,
            "reasoning": {"effort": "minimal"},
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "poligono_interes",
                    "strict": True,
                    "schema": schema,
                }
            },
        }

    def _post_responses(self, payload: dict[str, Any]) -> dict[str, Any]:
        endpoint = settings.azure_openai_endpoint.rstrip("/")
        url = f"{endpoint}/openai/responses?api-version={self.api_version}"
        request = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "api-key": settings.azure_openai_api_key,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=settings.azure_openai_poligono_timeout_seconds,
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detalle = exc.read().decode("utf-8", errors="ignore")
            raise PoligonoIAGenerationError(
                f"Azure OpenAI rechazó la solicitud: {detalle[:300]}"
            ) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise PoligonoIAGenerationError(
                "No se pudo conectar con Azure OpenAI."
            ) from exc

    def _extraer_texto(self, data: dict[str, Any]) -> str:
        textos: list[str] = []
        for salida in data.get("output", []):
            for contenido in salida.get("content", []):
                if contenido.get("type") == "output_text":
                    textos.append(str(contenido.get("text", "")))
        texto = "\n".join(t for t in textos if t.strip()).strip()
        if not texto:
            raise PoligonoIAGenerationError("El modelo no devolvió texto.")
        return texto

    def _parsear_puntos(self, contenido: str) -> list[dict[str, float]]:
        try:
            payload = json.loads(contenido)
        except json.JSONDecodeError as exc:
            raise PoligonoIAGenerationError("El modelo devolvió JSON inválido.") from exc
        puntos = payload.get("puntos")
        if not isinstance(puntos, list) or len(puntos) < 3:
            raise PoligonoIAGenerationError(
                "El modelo no devolvió al menos 3 vértices."
            )
        normalizados: list[dict[str, float]] = []
        for punto in puntos:
            if not isinstance(punto, dict):
                raise PoligonoIAGenerationError("Un vértice no tiene formato válido.")
            normalizados.append({"x": float(punto["x"]), "y": float(punto["y"])})
        return normalizados

    def _reescalar_puntos(
        self,
        *,
        puntos: list[dict[str, float]],
        imagen_modelo: ImagenModelo,
        ancho_original: int,
        alto_original: int,
    ) -> list[dict[str, float]]:
        escala_x = imagen_modelo.crop_ancho / imagen_modelo.ancho
        escala_y = imagen_modelo.crop_alto / imagen_modelo.alto
        return [
            {
                "x": round(
                    max(
                        0.0,
                        min(
                            ancho_original,
                            imagen_modelo.crop_x + punto["x"] * escala_x,
                        ),
                    ),
                    2,
                ),
                "y": round(
                    max(
                        0.0,
                        min(
                            alto_original,
                            imagen_modelo.crop_y + punto["y"] * escala_y,
                        ),
                    ),
                    2,
                ),
            }
            for punto in puntos
        ]
