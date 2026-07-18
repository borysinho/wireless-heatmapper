"""Modelo físico de propagación RF con calibración local por plano."""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class MuestraCalibracionRF:
    """Lectura real usada para ajustar el modelo al ambiente de un plano."""

    distancia_m: float
    banda: str
    rssi_dbm: float
    potencia_dbm: float | None = None
    ganancia_dbi: float = 2.14
    perdida_cable_db: float = 0.0


@dataclass(frozen=True)
class CorreccionEspacialRF:
    """Residuo local aprendido desde mediciones reales del plano."""

    x_px: float
    y_px: float
    banda: str
    error_db: float


@dataclass(frozen=True)
class ParametrosPropagacion:
    """Parámetros efectivos del modelo log-distance para una banda."""

    referencia_1m: float = -42.0
    perdida_por_doble_distancia: float = 6.0
    perdida_sistema_db: float = 52.0
    usa_potencia_tx: bool = False
    muestras: int = 0
    mae_db: float | None = None


class ModeloPropagacion:
    """Predicción RSSI determinística con degradación controlada a FSPL.

    Cuando existen mediciones reales vinculadas a APs con posición conocida, el
    modelo se calibra por plano ajustando el exponente log-distance y el nivel
    efectivo a 1 metro. Si no hay suficientes muestras, conserva el baseline de
    6 dB por duplicar distancia.
    """

    _PENALIZACION_BANDA = {"2.4": 0.0, "5": 6.4}

    def __init__(
        self,
        parametros_por_banda: dict[str, ParametrosPropagacion] | None = None,
        correcciones_espaciales: list[CorreccionEspacialRF] | None = None,
    ) -> None:
        self._parametros_por_banda = parametros_por_banda or {}
        self._correcciones_espaciales = correcciones_espaciales or []

    def fspl(self, *, rssi_referencia: float = -42.0, distancia_m: float) -> float:
        distancia = max(distancia_m, 1.0)
        perdida = 6.0 * math.log2(distancia)
        return round(max(-120.0, min(0.0, rssi_referencia - perdida)), 2)

    """Calibra desde muestras tomadas en campo"""
    @classmethod
    def calibrar_desde_muestras(
        cls,
        muestras: list[MuestraCalibracionRF],
    ) -> ModeloPropagacion:
        """Ajusta un modelo local por banda a partir de lecturas observadas."""
        por_banda: dict[str, list[MuestraCalibracionRF]] = defaultdict(list)
        for muestra in muestras:
            if muestra.rssi_dbm <= -120 or muestra.rssi_dbm >= 0:
                continue
            if muestra.distancia_m <= 0:
                continue
            por_banda[muestra.banda].append(muestra)

        parametros = {
            banda: cls._calibrar_banda(banda=banda, muestras=items)
            for banda, items in por_banda.items()
            if len(items) >= 3
        }
        return cls(parametros_por_banda=parametros)

    def predecir_rssi(
        self,
        *,
        distancia_px: float,
        metros_por_pixel: float,
        banda: str,
        punto_x: float | None = None,
        punto_y: float | None = None,
        penalizacion_material_db: float = 0.0,
        potencia_dbm: float | None = None,
        ganancia_dbi: float = 2.14,
        perdida_cable_db: float = 0.0,
        aplicar_correccion_espacial: bool = True,
    ) -> float:
        distancia_m = max(1.0, distancia_px * max(metros_por_pixel, 0.01))
        penalizacion_banda = self._penalizacion_banda(banda)
        parametros = self._parametros_por_banda.get(banda, ParametrosPropagacion())
        perdida = parametros.perdida_por_doble_distancia * math.log2(distancia_m)
        if potencia_dbm is None or (
            parametros.muestras >= 3 and not parametros.usa_potencia_tx
        ):
            referencia = parametros.referencia_1m
        else:
            eirp = potencia_dbm + ganancia_dbi - perdida_cable_db
            referencia = (
                eirp - parametros.perdida_sistema_db
                if parametros.usa_potencia_tx
                else eirp - 40.0 - 12.0
            )
        correccion_espacial = (
            self._correccion_espacial(banda=banda, x_px=punto_x, y_px=punto_y)
            if aplicar_correccion_espacial
            else 0.0
        )
        return round(
            max(
                -120.0,
                min(
                    0.0,
                    referencia
                    - perdida
                    - penalizacion_banda
                    - penalizacion_material_db
                    + correccion_espacial,
                ),
            ),
            2,
        )

    def con_correccion_espacial(
        self,
        correcciones: list[CorreccionEspacialRF],
    ) -> ModeloPropagacion:
        """Devuelve el mismo modelo físico con residuos locales acotados."""
        por_banda: dict[str, list[CorreccionEspacialRF]] = defaultdict(list)
        for correccion in correcciones:
            if not math.isfinite(correccion.error_db):
                continue
            if not math.isfinite(correccion.x_px) or not math.isfinite(correccion.y_px):
                continue
            por_banda[correccion.banda].append(
                CorreccionEspacialRF(
                    x_px=correccion.x_px,
                    y_px=correccion.y_px,
                    banda=correccion.banda,
                    error_db=max(-18.0, min(12.0, correccion.error_db)),
                )
            )
        validas = [
            item
            for items in por_banda.values()
            if len(items) >= 3
            for item in items
        ]
        return ModeloPropagacion(
            parametros_por_banda=self._parametros_por_banda,
            correcciones_espaciales=validas,
        )

    def resumen_calibracion(self) -> dict:
        """Devuelve metadatos serializables de la calibración aplicada."""
        por_banda = {
            banda: {
                "muestras": params.muestras,
                "referencia_1m_dbm": round(params.referencia_1m, 2),
                "perdida_por_doble_distancia_db": round(
                    params.perdida_por_doble_distancia,
                    2,
                ),
                "usa_potencia_tx": params.usa_potencia_tx,
                "mae_db": round(params.mae_db, 2)
                if params.mae_db is not None
                else None,
            }
            for banda, params in sorted(self._parametros_por_banda.items())
        }
        correccion_por_banda: dict[str, list[float]] = defaultdict(list)
        for correccion in self._correcciones_espaciales:
            correccion_por_banda[correccion.banda].append(correccion.error_db)
        resumen_espacial = {
            banda: {
                "muestras": len(valores),
                "correccion_promedio_db": round(sum(valores) / len(valores), 2),
                "correccion_min_db": round(min(valores), 2),
                "correccion_max_db": round(max(valores), 2),
            }
            for banda, valores in sorted(correccion_por_banda.items())
            if valores
        }
        if resumen_espacial:
            tipo = "calibracion_espacial_por_plano"
        elif por_banda:
            tipo = "calibracion_local_por_plano"
        else:
            tipo = "baseline_fspl"
        return {
            "tipo": tipo,
            "bandas": por_banda,
            "muestras": sum(item["muestras"] for item in por_banda.values()),
            "correccion_espacial": resumen_espacial,
        }

    @classmethod
    def _calibrar_banda(
        cls,
        *,
        banda: str,
        muestras: list[MuestraCalibracionRF],
    ) -> ParametrosPropagacion:
        penalizacion = cls._penalizacion_banda(banda)
        xs = [math.log2(max(1.0, muestra.distancia_m)) for muestra in muestras]
        ys = [muestra.rssi_dbm + penalizacion for muestra in muestras]
        referencia, perdida = cls._regresion_log_distance(xs=xs, ys=ys)

        muestras_con_potencia = [
            muestra for muestra in muestras if muestra.potencia_dbm is not None
        ]
        usa_potencia_tx = len(muestras_con_potencia) >= 3
        perdida_sistema = 52.0
        if usa_potencia_tx:
            perdidas = []
            for muestra in muestras_con_potencia:
                eirp = (
                    float(muestra.potencia_dbm)
                    + muestra.ganancia_dbi
                    - muestra.perdida_cable_db
                )
                distancia = math.log2(max(1.0, muestra.distancia_m))
                perdidas.append(
                    eirp - (muestra.rssi_dbm + penalizacion) - perdida * distancia
                )
            perdida_sistema = cls._promedio_recortado(
                perdidas,
                minimo=35.0,
                maximo=80.0,
            )

        errores = []
        for muestra in muestras:
            prediccion = referencia - perdida * math.log2(max(1.0, muestra.distancia_m))
            prediccion -= penalizacion
            errores.append(abs(prediccion - muestra.rssi_dbm))
        mae = sum(errores) / len(errores) if errores else None
        return ParametrosPropagacion(
            referencia_1m=referencia,
            perdida_por_doble_distancia=perdida,
            perdida_sistema_db=perdida_sistema,
            usa_potencia_tx=usa_potencia_tx,
            muestras=len(muestras),
            mae_db=mae,
        )

    @staticmethod
    def _regresion_log_distance(
        *,
        xs: list[float],
        ys: list[float],
    ) -> tuple[float, float]:
        promedio_x = sum(xs) / len(xs)
        promedio_y = sum(ys) / len(ys)
        var_x = sum((x - promedio_x) ** 2 for x in xs)
        if var_x <= 1e-9:
            return round(promedio_y, 2), 6.0
        cov = sum((x - promedio_x) * (y - promedio_y) for x, y in zip(xs, ys))
        pendiente = cov / var_x
        perdida = max(3.0, min(12.0, -pendiente))
        referencia = sum(y + perdida * x for x, y in zip(xs, ys)) / len(xs)
        return round(max(-90.0, min(-15.0, referencia)), 2), round(perdida, 2)

    @staticmethod
    def _promedio_recortado(
        valores: list[float],
        *,
        minimo: float,
        maximo: float,
    ) -> float:
        acotados = [max(minimo, min(maximo, valor)) for valor in valores]
        return round(sum(acotados) / len(acotados), 2)

    @classmethod
    def _penalizacion_banda(cls, banda: str) -> float:
        return cls._PENALIZACION_BANDA.get(banda, 6.4)

    def _correccion_espacial(
        self,
        *,
        banda: str,
        x_px: float | None,
        y_px: float | None,
    ) -> float:
        if x_px is None or y_px is None:
            return 0.0
        muestras = [
            muestra
            for muestra in self._correcciones_espaciales
            if muestra.banda == banda
        ]
        if len(muestras) < 3:
            return 0.0
        numerador = 0.0
        denominador = 0.0
        for muestra in muestras:
            dx = float(x_px) - muestra.x_px
            dy = float(y_px) - muestra.y_px
            distancia_cuadrado = dx * dx + dy * dy
            if distancia_cuadrado < 1e-9:
                return muestra.error_db
            peso = 1 / distancia_cuadrado
            numerador += peso * muestra.error_db
            denominador += peso
        if denominador <= 0:
            return 0.0
        return max(-18.0, min(12.0, numerador / denominador))


def generar_dataset_sintetico(seed: int = 24) -> list[dict]:
    """Dataset paramétrico reproducible para pruebas y reentrenamiento futuro."""
    filas: list[dict] = []
    bandas = ["2.4", "5"]
    materiales = [0.0, 3.0, 7.0, 12.0]
    modelo = ModeloPropagacion()
    for banda in bandas:
        for material in materiales:
            for distancia in range(1, 61):
                ruido = ((distancia * seed) % 7 - 3) * 0.35
                rssi = modelo.predecir_rssi(
                    distancia_px=float(distancia),
                    metros_por_pixel=1.0,
                    banda=banda,
                    penalizacion_material_db=material,
                )
                filas.append(
                    {
                        "distancia_m": distancia,
                        "banda": banda,
                        "perdida_material_db": material,
                        "rssi": round(rssi + ruido, 2),
                    }
                )
    return filas
