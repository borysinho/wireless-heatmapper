# 14 — Trazabilidad RP ↔ HU ↔ Sprint ↔ UC

> Matriz de cobertura entre los 9 Requerimientos Principales del PAPS Online y los artefactos Scrum del plan de implementación. Garantiza que ningún RP queda sin entrega y que ninguna HU es huérfana.

---

## 1. Matriz principal — RP ↔ HU ↔ Sprint ↔ UC

> **Mapeo RP autoritativo:** [PAPS Online §7 (RP1..RP9)](../Wireless%20Heatmapper%20-%20PAPS%20-%20Modalidad%20Online.md). No usar la numeración del PAPS histórico (`docs/Wireless Heatmapper - PAPS.md`).

| RP  | Descripción (PAPS Online §7)                                   | HU activas          | Sprint(s) | UC asociados     |
| --- | -------------------------------------------------------------- | ------------------- | --------- | ---------------- |
| RP1 | Captura de señal WiFi (en línea, request por request)          | PB-03               | S3        | UC05             |
| RP2 | Mapeo sobre plano (importación, calibración y marcado)         | PB-02, PB-11, PB-04 | S2, S3    | UC02, UC03, UC04 |
| RP3 | Generación de mapa de calor (interpolación en backend)         | PB-20, PB-05        | S4        | UC06             |
| RP4 | Análisis automático de cobertura (zonas muertas, CCI/ACI)      | PB-06               | S4        | UC07             |
| RP5 | Optimización mediante IA (recomendaciones + comparación)       | PB-07, PB-12        | S5        | UC08, UC09       |
| RP6 | Generación y exportación de reportes (PDF)                     | PB-08               | S5        | UC10             |
| RP7 | Administración de usuarios y supervisión organizacional        | PB-13, PB-19, PB-18 | S1        | UC13, UC18, UC19 |
| RP8 | Persistencia centralizada en línea (auth + dominio en backend) | PB-09, PB-01, PB-10 | S1        | UC11, UC01, UC12 |
| RP9 | Portal de cliente (enlace único + vista web sin login)         | PB-15, PB-16, PB-17 | S6        | UC15, UC16, UC17 |

**Cobertura:** 9 / 9 RP con al menos 1 HU asignada (100 %).

> RP8 es transversal: además de PB-09/PB-01/PB-10 (HU principales del Sprint 1), se materializa en cada endpoint REST que persiste dominio en PostgreSQL desde el Sprint 1 en adelante.

> **Refinamiento aprobado de RP5 (20-jun-2026):** el paquete [17 — Especificación de Optimización RF por Escenarios](17-especificacion-optimizacion-rf/00-indice.md) amplía PB-07/PB-12 para distinguir AP físico, radio y BSSID; recomendar configuración por banda; y proyectar valores sin modificar mediciones reales. El ajuste de gobernanza móvil/web del 20-jun-2026 no altera los identificadores ni la asignación de Sprint de esta matriz.

> **Refinamiento de gobernanza móvil/web:** el documento [18 — Reglas de Gobernanza para Conjuntos de APs, Heatmaps e IA](18-reglas-gobernanza-conjuntos-ap-heatmaps.md) aclara que el móvil puede crear conjuntos manuales y visualizar heatmaps operativos, mientras que la generación IA queda restringida a backend/web y el cliente solo accede a contenido publicado por enlace. Impacta PB-20, PB-05, PB-06, PB-07, PB-12, PB-08, PB-15, PB-16 y PB-17 sin crear nuevas HU ni renombrar RP.

> **Refinamiento de asignaciones (20-jun-2026):** PB-18 amplía la supervisión a un ABM completo de proyectos y PB-09 incorpora el registro del dispositivo Android para avisar mediante FCM cuando el administrador crea o reasigna un proyecto. El token push se persiste en PostgreSQL como dato técnico de sesión; no introduce almacenamiento local de dominio ni modifica la asignación RP7/RP8.

---

## 2. Listado completo de HU del plan de implementación

| HU    | Nombre                                   | Sprint | PHU | RP  | Estado de implementación        |
| ----- | ---------------------------------------- | ------ | --: | --- | ------------------------------- |
| PB-13 | Gestionar usuarios (admin web)           | S1     |   8 | RP7 | ✅ Implementada                 |
| PB-19 | Gestionar clientes (admin web)           | S1     |   3 | RP7 | ✅ Implementada                 |
| PB-09 | Autenticar usuario (móvil)               | S1     |   5 | RP8 | ✅ Implementada                 |
| PB-18 | Ver proyectos de la organización         | S1     |   5 | RP7 | ✅ Implementada                 |
| PB-01 | Gestionar proyecto de survey             | S1     |   5 | RP8 | ✅ Implementada                 |
| PB-10 | Ver historial de proyectos               | S1     |   3 | RP8 | ✅ Implementada                 |
| PB-02 | Importar plano de edificio               | S2     |   8 | RP2 | ✅ Implementada                 |
| PB-11 | Calibrar escala del plano                | S2     |   8 | RP2 | ✅ Implementada                 |
| PB-03 | Capturar señales WiFi (en línea)         | S3     |  13 | RP1 | ✅ Implementada                 |
| PB-04 | Marcar puntos de medición                | S3     |   8 | RP2 | ✅ Implementada                 |
| PB-20 | Gestionar conjuntos de APs por plano     | S4     |   8 | RP3 | ✅ Implementada                 |
| PB-05 | Generar mapa de calor                    | S4     |  13 | RP3 | ✅ Implementada                 |
| PB-06 | Analizar cobertura automáticamente       | S4     |  13 | RP4 | ✅ Implementada                 |
| PB-07 | Recomendaciones IA de APs                | S5     |  21 | RP5 | ✅ Implementada                 |
| PB-12 | Comparar escenarios                      | S5     |   8 | RP5 | ✅ Implementada                 |
| PB-08 | Exportar reporte PDF                     | S5     |  13 | RP6 | ✅ Implementada                 |
| PB-15 | Generar enlace único para cliente        | S6     |   5 | RP9 | ✅ Implementada                 |
| PB-16 | Ver heatmap interactivo (web)            | S6     |  13 | RP9 | ✅ Implementada                 |
| PB-17 | Ver análisis y plan de APs (web)         | S6     |   8 | RP9 | ✅ Implementada                 |
| PB-14 | Sincronizar mediciones offline → backend | —      |   — | —   | ❌ Eliminada (modalidad online) |

**Total PHU activos:** 8 + 3 + 5 + 5 + 5 + 3 + 8 + 8 + 13 + 8 + 8 + 13 + 13 + 21 + 8 + 13 + 5 + 13 + 8 = **168 PHU** (19 HU activas)

> El total de 168 PHU se actualizó al añadir PB-20 (8 PHU) como refinamiento obligatorio del Sprint 4: los heatmaps se generan desde conjuntos de APs con propósito trazable, no desde una selección ad hoc sin contexto.

---

## 3. Cobertura por sprint

| Sprint | PHU comprometidos | HU                                       | RP cubiertos           | Estado          |
| ------ | ----------------: | ---------------------------------------- | ---------------------- | --------------- |
| S0     |         — (setup) | (sin HU funcional — ver Sprint 0)        | habilitadores de infra | ✅ Implementado |
| S1     |                29 | PB-13, PB-19, PB-09, PB-18, PB-01, PB-10 | RP7, RP8               | ✅ Implementado |
| S2     |                16 | PB-02, PB-11                             | RP2                    | ✅ Implementado |
| S3     |                21 | PB-03, PB-04                             | RP1, RP2               | ✅ Implementado |
| S4     |                34 | PB-20, PB-05, PB-06                      | RP3, RP4               | ✅ Implementado |
| S5     |                42 | PB-07, PB-12, PB-08                      | RP5, RP6               | ✅ Implementado |
| S6     |                26 | PB-15, PB-16, PB-17                      | RP9                    | ✅ Implementado |
| **Σ**  |           **168** | 19 HU activas                            | 9 / 9 RP               |                 |

---

## 4. Cobertura por UC del modelo de contexto

> Identificadores UC alineados con [02-modelo-contexto.md §3](02-modelo-contexto.md). UC14 fue eliminado por modalidad online (no hay sincronización diferida).

| UC   | Nombre                                        | HU asociada | Sprint |
| ---- | --------------------------------------------- | ----------- | ------ |
| UC01 | Gestionar proyecto de survey                  | PB-01       | S1     |
| UC02 | Importar plano (subida al backend)            | PB-02       | S2     |
| UC03 | Calibrar escala del plano                     | PB-11       | S2     |
| UC04 | Marcar punto de medición                      | PB-04       | S3     |
| UC05 | Capturar señales WiFi (envío en línea)        | PB-03       | S3     |
| UC06 | Generar mapa de calor (interpolación backend) | PB-20, PB-05 | S4     |
| UC07 | Analizar cobertura (zonas muertas, CCI/ACI)   | PB-06       | S4     |
| UC08 | Obtener recomendaciones de APs (IA)           | PB-07       | S5     |
| UC09 | Comparar escenario actual vs propuesto        | PB-12       | S5     |
| UC10 | Exportar reporte técnico (PDF)                | PB-08       | S5     |
| UC11 | Autenticar usuario                            | PB-09       | S1     |
| UC12 | Ver historial de proyectos                    | PB-10       | S1     |
| UC13 | Gestionar usuarios (admin web)                | PB-13       | S1     |
| UC14 | (eliminado — sincronización offline)          | —           | —      |
| UC15 | Generar enlace de cliente                     | PB-15       | S6     |
| UC16 | Ver heatmap interactivo (web)                 | PB-16       | S6     |
| UC17 | Ver análisis y plan AP (web)                  | PB-17       | S6     |
| UC18 | Ver proyectos de la organización              | PB-18       | S1     |
| UC19 | Gestionar clientes (admin web)                | PB-19       | S1     |

**Cobertura UC:** 18 / 18 UC activos cubiertos (100 %, UC14 eliminado).

---

## 5. Validaciones de huérfanos

- **HU sin RP**: ninguna. Todas las HU activas están asociadas a un RP del PAPS Online. PB-13, PB-19 y PB-18 cubren RP7; PB-09, PB-01 y PB-10 cubren RP8. ✔
- **RP sin HU**: ninguno. ✔
- **HU sin sprint**: ninguna. ✔
- **HU sin UC**: ninguna (PB-19 ↔ UC19, añadido al modelo de contexto). ✔
- **UC sin HU**: ninguno (UC14 eliminado por modalidad online conforme PAPS Online §10.1). ✔

---

## 6. Cobertura de restricciones CWNA-107

| Restricción CWNA-107                          | Aplicada en HU      | Verificada en sprint |
| --------------------------------------------- | ------------------- | -------------------- |
| RSSI < −90 dBm = zona muerta                  | PB-03, PB-06        | S3, S4               |
| Objetivo de diseño ≥ −70 dBm                  | PB-05, PB-06, PB-07 | S4, S5               |
| Umbral operativo < −75 dBm = zona problemática | PB-05, PB-06        | S4                   |
| Throttling Android ≥ 8.0 = 4 escaneos / 2 min | PB-03               | S3                   |
| FSPL / log-distance (6 dB por duplicar distancia) | PB-07 (modelo IA) | S5                   |
| Calibración local del predictor por plano finalizado | PB-07, PB-12 | S5                   |
| Tabla 3.1 — atenuación de materiales a 2,4 GHz | PB-07 (modelo IA) | S5                   |
| Heatmap por APs de interés (BSSID; ubicación AP referencial; puntos de lectura como fuente de interpolación) | PB-20, PB-05, PB-06 | S4                   |
| CCI / ACI (canales 2.4 GHz Δ ≤ 4)             | PB-06               | S4                   |
| Solapamiento de áreas con RSSI ≥ −70 dBm      | PB-06               | S4                   |
| Configuración y predicción separadas para 2,4/5 GHz | PB-07, PB-12 | S5 · aprobado / ajuste gobernanza |
| Medición observada inmutable vs valor proyectado | PB-07, PB-12 | S5 · aprobado / ajuste gobernanza |

---

## 7. Resumen de validación

✅ **9 / 9 RP** con cobertura de HU (mapeo conforme PAPS Online §7)
✅ **18 / 18 UC** activos cubiertos por HU (UC14 eliminado por modalidad online)
✅ **19 / 19 HU** activas asignadas a sprint
✅ **Restricciones CWNA-107 listadas** trazadas a HU
✅ **0 huérfanos** detectados

> Esta matriz se debe revisar al inicio de cada Sprint Planning (R-2) y al cierre de cada Sprint Review (R-4) según el skill `validar-trazabilidad-rp` referenciado en [AGENTS.md](../../../AGENTS.md).
