"""Generación de reportes PDF Sprint 5 — PB-08."""

from __future__ import annotations

import hashlib
import textwrap
from dataclasses import dataclass
from datetime import datetime

import fitz

from app.models.escenario import EscenarioOptimizado
from app.models.proyecto import Proyecto


@dataclass(frozen=True)
class ReporteGenerado:
    contenido: bytes
    sha256: str
    tamanio_bytes: int


class ReporteService:
    """Construye un PDF profesional mínimo con secciones obligatorias."""

    def generar(
        self,
        *,
        proyecto: Proyecto,
        escenarios: list[EscenarioOptimizado],
        escenario_seleccionado: EscenarioOptimizado | None = None,
        cantidad_mediciones: int = 0,
    ) -> ReporteGenerado:
        doc = fitz.open()
        self._portada(doc, proyecto=proyecto)
        self._resumen(doc, proyecto=proyecto, escenarios=escenarios)
        self._analisis(doc, escenarios=escenarios)
        for escenario in escenarios:
            self._escenario(doc, escenario=escenario)
        self._anexo(
            doc,
            proyecto=proyecto,
            escenario=escenario_seleccionado,
            cantidad_mediciones=cantidad_mediciones,
        )
        contenido = doc.tobytes(deflate=True)
        doc.close()
        sha = hashlib.sha256(contenido).hexdigest()
        return ReporteGenerado(
            contenido=contenido,
            sha256=sha,
            tamanio_bytes=len(contenido),
        )

    def _portada(self, doc: fitz.Document, *, proyecto: Proyecto) -> None:
        page = doc.new_page(width=595, height=842)
        self._texto(page, 72, 96, "Bulldog Tech.", 28, bold=True)
        self._texto(page, 72, 140, "Reporte tecnico de cobertura WiFi", 20, bold=True)
        self._texto(page, 72, 190, f"Proyecto: {proyecto.nombre}", 14)
        cliente = proyecto.cliente.nombre if proyecto.cliente else "Sin cliente asignado"
        self._texto(page, 72, 216, f"Cliente: {cliente}", 12)
        tecnico = proyecto.tecnico.nombre if proyecto.tecnico else "Tecnico asignado"
        self._texto(page, 72, 242, f"Tecnico: {tecnico}", 12)
        self._texto(page, 72, 268, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 12)
        self._texto(
            page,
            72,
            720,
            "Sistema Wireless HeatMapper - Modalidad 100% en linea",
            10,
        )

    def _resumen(
        self,
        doc: fitz.Document,
        *,
        proyecto: Proyecto,
        escenarios: list[EscenarioOptimizado],
    ) -> None:
        page = doc.new_page(width=595, height=842)
        self._titulo(page, "Resumen ejecutivo")
        mejor = max(escenarios, key=lambda e: e.pct_cobertura, default=None)
        lineas = [
            f"Proyecto evaluado: {proyecto.nombre}.",
            f"Cantidad de escenarios propuestos: {len(escenarios)}.",
        ]
        if mejor is not None:
            lineas.append(
                "Mejor escenario: "
                f"{mejor.nombre} con {mejor.pct_cobertura:.1f}% de cobertura "
                f">= -70 dBm y costo estimado {mejor.costo_estimado:.2f}."
            )
        lineas.append(
            "El objetivo tecnico preservado es cobertura de diseno >= -70 dBm "
            "y deteccion de zonas muertas RSSI < -90 dBm."
        )
        self._parrafo(page, 72, 120, "\n".join(lineas))

    def _analisis(self, doc: fitz.Document, *, escenarios: list[EscenarioOptimizado]) -> None:
        page = doc.new_page(width=595, height=842)
        self._titulo(page, "Analisis de cobertura")
        y = 120
        for escenario in escenarios[:6]:
            self._texto(
                page,
                72,
                y,
                (
                    f"{escenario.nombre}: actual {escenario.pct_cobertura_actual:.1f}% "
                    f"-> proyectado {escenario.pct_cobertura:.1f}% | "
                    f"APs {escenario.cantidad_aps} | costo {escenario.costo_estimado:.2f}"
                ),
                11,
            )
            y += 28
        if not escenarios:
            self._texto(page, 72, y, "No existen escenarios optimizados registrados.", 11)

    def _escenario(self, doc: fitz.Document, *, escenario: EscenarioOptimizado) -> None:
        page = doc.new_page(width=595, height=842)
        self._titulo(page, f"Escenario propuesto: {escenario.nombre}")
        self._parrafo(page, 72, 116, escenario.resumen)
        y = 190
        self._texto(page, 72, y, "Recomendaciones AP", 13, bold=True)
        y += 28
        for rec in escenario.recomendaciones:
            texto = (
                f"{rec.orden}. {rec.accion} {rec.modelo_ap} en "
                f"({rec.coord_x:.1f}, {rec.coord_y:.1f}) banda {rec.banda} GHz. "
                f"{rec.justificacion}"
            )
            y = self._parrafo(page, 90, y, texto, size=10, ancho=82) + 12

    def _anexo(
        self,
        doc: fitz.Document,
        *,
        proyecto: Proyecto,
        escenario: EscenarioOptimizado | None,
        cantidad_mediciones: int,
    ) -> None:
        page = doc.new_page(width=595, height=842)
        self._titulo(page, "Anexo tecnico")
        lineas = [
            f"Proyecto ID: {proyecto.id}",
            f"Estado: {proyecto.estado}",
            f"Cantidad de puntos registrada: {proyecto.cantidad_puntos}",
            f"Cantidad de mediciones incluidas: {cantidad_mediciones}",
            f"Escenario seleccionado: {escenario.nombre if escenario else 'No especificado'}",
            "Integridad: este PDF se registra con hash SHA-256 en el backend.",
        ]
        self._parrafo(page, 72, 120, "\n".join(lineas))

    def _titulo(self, page: fitz.Page, texto: str) -> None:
        self._texto(page, 72, 72, texto, 20, bold=True)

    def _parrafo(
        self,
        page: fitz.Page,
        x: float,
        y: float,
        texto: str,
        *,
        size: int = 11,
        ancho: int = 88,
    ) -> float:
        actual = y
        for linea in texto.splitlines():
            for parte in textwrap.wrap(linea, width=ancho) or [""]:
                self._texto(page, x, actual, parte, size)
                actual += size + 6
        return actual

    def _texto(
        self,
        page: fitz.Page,
        x: float,
        y: float,
        texto: str,
        size: int,
        *,
        bold: bool = False,
    ) -> None:
        fontname = "helv"
        page.insert_text((x, y), texto, fontsize=size, fontname=fontname, fill=(0.08, 0.12, 0.16))
