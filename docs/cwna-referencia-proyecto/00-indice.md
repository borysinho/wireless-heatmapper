# Extracción CWNA-107 → Wireless Heatmapper (PAPS)

Esta carpeta contiene los puntos extraídos del libro **CWNA Certified Wireless Network Administrator Study Guide (CWNA-107)** que son relevantes para el proyecto **Wireless Heatmapper** definido en [Wireless Heatmapper - Plan Aplicado a Proyecto de Software PAPS.md](../Wireless%20Heatmapper%20-%20Plan%20Aplicado%20a%20Proyecto%20de%20Software%20PAPS.md).

Cada archivo extraído indica explícitamente el **capítulo, sección y número de página** del libro original (CWNA-107.md) para facilitar la trazabilidad y la consulta de la fuente.

## Mapeo Requerimientos del Proyecto ↔ Archivos

| Requerimiento PAPS                                                                            | Tema clave                                                            | Archivo                                                                                                        |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| RP1 — Captura de señales WiFi (RSSI, SSID, BSSID, canal, frecuencia)                          | Métricas RSSI, dBm, SNR, sensibilidad de recepción                    | [02-rssi-y-mediciones.md](02-rssi-y-mediciones.md)                                                             |
| RP3 — Generación de heatmap por interpolación                                                 | FSPL, comportamientos RF (absorción, reflexión, multipath)            | [01-fundamentos-rf.md](01-fundamentos-rf.md)                                                                   |
| RP4 — Análisis de cobertura (zonas muertas, interferencia entre canales, solapamiento de APs) | Diseño de cobertura, ACI/CCI, reuso de canales 2.4/5 GHz              | [04-diseno-wlan.md](04-diseno-wlan.md)                                                                         |
| RP5 — Optimización por IA del posicionamiento de APs                                          | Diseño predictivo, antenas direccionales/omnidireccionales, capacidad | [03-antenas.md](03-antenas.md), [04-diseno-wlan.md](04-diseno-wlan.md), [05-site-survey.md](05-site-survey.md) |
| RP6 — Reporte técnico exportable                                                              | Estructura de un reporte de site survey y entregables                 | [05-site-survey.md](05-site-survey.md)                                                                         |
| Restricciones (throttling Android, posicionamiento indoor)                                    | Validación de cobertura, herramientas de medición                     | [05-site-survey.md](05-site-survey.md)                                                                         |

## Archivos

1. [01-fundamentos-rf.md](01-fundamentos-rf.md) — Comportamientos RF: absorción, reflexión, scattering, refracción, difracción, FSPL y multipath. (CWNA-107 Cap. 3)
2. [02-rssi-y-mediciones.md](02-rssi-y-mediciones.md) — Unidades de potencia (mW, dBm), dB/dBi/dBd, ruido, SNR/SINR, sensibilidad de recepción y métricas RSSI por fabricante. (CWNA-107 Cap. 4)
3. [03-antenas.md](03-antenas.md) — Patrones de radiación, ancho de haz, tipos de antenas y orientación. (CWNA-107 Cap. 5 y 13)
4. [04-diseno-wlan.md](04-diseno-wlan.md) — Diseño de cobertura, umbrales de señal, reuso de canales 2.4/5 GHz, ACI/CCI, capacidad y airtime. (CWNA-107 Cap. 13)
5. [05-site-survey.md](05-site-survey.md) — Site survey, análisis de espectro, análisis de cobertura, diseño predictivo, validación, herramientas y reportes. (CWNA-107 Cap. 14)

## Convención de citas

Cada bloque relevante usa el formato:

> **Fuente:** CWNA-107.md, Cap. N — _Título de Sección_ (pág. P, líneas L1–L2)

donde `pág. P` corresponde a la paginación impresa del libro y `líneas L1–L2` al rango aproximado dentro del archivo Markdown convertido [CWNA-107.md](../CWNA-107.md).
