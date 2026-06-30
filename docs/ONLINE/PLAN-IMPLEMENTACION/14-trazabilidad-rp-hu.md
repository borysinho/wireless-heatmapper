# 14 — Trazabilidad RP ↔ HU ↔ Sprint ↔ UC

> Matriz de cobertura entre los Requerimientos Principales activos del PAPS Online y los artefactos Scrum del plan de implementación. Registra también los RP/HU descartados por refinamiento de alcance.

---

## 1. Matriz principal — RP ↔ HU ↔ Sprint ↔ UC

> **Mapeo RP autoritativo:** [PAPS Online §7 (RP1..RP9)](../Wireless%20Heatmapper%20-%20PAPS%20-%20Modalidad%20Online.md). No usar la numeración del PAPS histórico (`docs/Wireless Heatmapper - PAPS.md`).

| RP  | Descripción (PAPS Online §7)                                   | HU activas          | Sprint(s) | UC asociados     |
| --- | -------------------------------------------------------------- | ------------------- | --------- | ---------------- |
| RP1 | Captura de señal WiFi (en línea, request por request)          | PB-03               | S3        | UC05             |
| RP2 | Mapeo sobre plano (importación, calibración y marcado)         | PB-02, PB-11, PB-04 | S2, S3    | UC02, UC03, UC04 |
| RP3 | Generación de mapa de calor (interpolación en backend)         | PB-20, PB-05        | S4        | UC06             |
| RP4 | Análisis automático de cobertura (diagnóstico persistido)       | —                   | —         | —                |
| RP5 | Optimización mediante IA como conjuntos AP derivados           | PB-07, PB-12        | S5        | UC08, UC09       |
| RP6 | Generación y exportación de reportes (PDF)                     | —                   | —         | —                |
| RP7 | Administración de usuarios y supervisión organizacional        | PB-13, PB-19, PB-18 | S1        | UC13, UC18, UC19 |
| RP8 | Persistencia centralizada en línea (auth + dominio en backend) | PB-09, PB-01, PB-10 | S1        | UC11, UC01, UC12 |
| RP9 | Portal de cliente (enlace único + vista web sin login)         | PB-15, PB-16, PB-17 | S6        | UC15, UC16, UC17 |

**Cobertura activa:** 7 / 9 RP con al menos 1 HU asignada. RP4 y RP6 quedan fuera de alcance por decisión de negocio vigente.

> RP8 es transversal: además de PB-09/PB-01/PB-10 (HU principales del Sprint 1), se materializa en cada endpoint REST que persiste dominio en PostgreSQL desde el Sprint 1 en adelante.

> **Refinamiento vigente de RP5 (27-jun-2026):** las propuestas IA se persisten como `conjunto_ap` de origen `ia`, derivadas desde un único conjunto técnico mediante `conjunto_origen_id`. Se eliminan `escenario_optimizado`, `recomendacion_ap` y `valor_proyectado_punto` como entidades de negocio.

> **Refinamiento de alcance (27-jun-2026):** el documento [18 — Reglas de Gobierno para Conjuntos de APs, Heatmaps e IA](18-reglas-gobernanza-conjuntos-ap-heatmaps.md) elimina diagnóstico persistido, estados de aprobación/publicación y reportes PDF. PB-06 y PB-08 quedan eliminadas; PB-15/PB-16/PB-17 se mantienen con publicación explícita por enlace.

> **Refinamiento de asignaciones (20-jun-2026):** PB-18 amplía la supervisión a un ABM completo de proyectos y PB-09 incorpora el registro del dispositivo Android para avisar mediante FCM cuando el administrador crea o reasigna un proyecto. El token push se persiste en PostgreSQL como dato técnico de sesión; no introduce almacenamiento local de dominio ni modifica la asignación RP7/RP8.

> **Refinamiento de publicación a cliente (23-jun-2026):** PB-15 usa el cliente registrado en PB-19 como destinatario del enlace público, tomando su correo de referencia del catálogo de clientes. Se elimina el ingreso manual de correos en la pantalla de publicación para preservar trazabilidad y reducir errores de envío.

> **Refinamiento de área operativa (23-jun-2026):** PB-04 incorpora el trazado de un polígono de interés en la captura móvil; PB-05 y PB-07 usan ese polígono para recortar heatmaps y restringir recomendaciones IA al área operativa definida.

> **Refinamiento de generación masiva de heatmaps (29-jun-2026):** la previsualización web de conjuntos AP genera o actualiza únicamente el mapa global del conjunto y un mapa individual por cada AP. Esta regla aplica por igual a conjuntos técnicos (`manual_movil` / `manual_web`) y conjuntos propuestos por IA (`ia`), sin crear combinaciones intermedias.

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
| PB-06 | Analizar cobertura automáticamente       | —      |   — | RP4 | ❌ Eliminada (sin diagnóstico persistido) |
| PB-07 | Recomendaciones IA de APs                | S5     |  21 | RP5 | ✅ Implementada                 |
| PB-12 | Comparar escenarios                      | S5     |   8 | RP5 | ✅ Implementada                 |
| PB-08 | Exportar reporte PDF                     | —      |   — | RP6 | ❌ Eliminada (sin exportación PDF) |
| PB-15 | Generar enlace único para cliente        | S6     |   5 | RP9 | ✅ Implementada                 |
| PB-16 | Ver heatmap interactivo (web)            | S6     |  13 | RP9 | ✅ Implementada                 |
| PB-17 | Ver análisis y plan de APs (web)         | S6     |   8 | RP9 | ✅ Implementada                 |
| PB-14 | Sincronizar mediciones offline → backend | —      |   — | —   | ❌ Eliminada (modalidad online) |

**Total PHU activos:** 8 + 3 + 5 + 5 + 5 + 3 + 8 + 8 + 13 + 8 + 8 + 13 + 21 + 8 + 5 + 13 + 8 = **142 PHU** (17 HU activas)

> El total histórico de 168 PHU quedó reducido a 142 PHU por la eliminación de PB-06 (13 PHU) y PB-08 (13 PHU). PB-20 (8 PHU) permanece activa como refinamiento obligatorio del Sprint 4.

---

## 3. Cobertura por sprint

| Sprint | PHU comprometidos | HU                                       | RP cubiertos           | Estado          |
| ------ | ----------------: | ---------------------------------------- | ---------------------- | --------------- |
| S0     |         — (setup) | (sin HU funcional — ver Sprint 0)        | habilitadores de infra | ✅ Implementado |
| S1     |                29 | PB-13, PB-19, PB-09, PB-18, PB-01, PB-10 | RP7, RP8               | ✅ Implementado |
| S2     |                16 | PB-02, PB-11                             | RP2                    | ✅ Implementado |
| S3     |                21 | PB-03, PB-04                             | RP1, RP2               | ✅ Implementado |
| S4     |                21 | PB-20, PB-05                             | RP3                    | ✅ Implementado |
| S5     |                29 | PB-07, PB-12                             | RP5                    | ✅ Implementado |
| S6     |                26 | PB-15, PB-16, PB-17                      | RP9                    | ✅ Implementado |
| **Σ**  |           **142** | 17 HU activas                            | 7 / 9 RP activos       |                 |

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
| UC07 | (eliminado — diagnóstico persistido)           | —           | —      |
| UC08 | Obtener recomendaciones de APs (IA)           | PB-07       | S5     |
| UC09 | Comparar escenario actual vs propuesto        | PB-12       | S5     |
| UC10 | (eliminado — reporte PDF)                     | —           | —      |
| UC11 | Autenticar usuario                            | PB-09       | S1     |
| UC12 | Ver historial de proyectos                    | PB-10       | S1     |
| UC13 | Gestionar usuarios (admin web)                | PB-13       | S1     |
| UC14 | (eliminado — sincronización offline)          | —           | —      |
| UC15 | Generar enlace de cliente                     | PB-15       | S6     |
| UC16 | Ver heatmap interactivo (web)                 | PB-16       | S6     |
| UC17 | Ver plan AP y heatmaps compartidos (web)      | PB-17       | S6     |
| UC18 | Ver proyectos de la organización              | PB-18       | S1     |
| UC19 | Gestionar clientes (admin web)                | PB-19       | S1     |

**Cobertura UC:** 16 / 16 UC activos cubiertos (100 %, UC07, UC10 y UC14 eliminados).

---

## 5. Validaciones de huérfanos

- **HU sin RP**: ninguna. Todas las HU activas están asociadas a un RP del PAPS Online. PB-13, PB-19 y PB-18 cubren RP7; PB-09, PB-01 y PB-10 cubren RP8. ✔
- **RP sin HU activo**: RP4 y RP6 quedan sin HU por refinamiento aprobado de alcance. ✔
- **HU sin sprint**: ninguna. ✔
- **HU sin UC**: ninguna (PB-19 ↔ UC19, añadido al modelo de contexto). ✔
- **UC sin HU**: ninguno (UC14 eliminado por modalidad online conforme PAPS Online §10.1). ✔

---

## 6. Cobertura de restricciones CWNA-107

| Restricción CWNA-107                          | Aplicada en HU      | Verificada en sprint |
| --------------------------------------------- | ------------------- | -------------------- |
| RSSI < −90 dBm = zona muerta                  | PB-03, PB-05, PB-16 | S3, S4, S6           |
| Objetivo de diseño ≥ −70 dBm                  | PB-05, PB-07, PB-16 | S4, S5, S6           |
| Umbral operativo < −75 dBm = zona problemática | PB-05               | S4                   |
| Throttling Android ≥ 8.0 = 4 escaneos / 2 min | PB-03               | S3                   |
| FSPL / log-distance (regla de 6 dB)           | PB-07 (modelo IA)   | S5                   |
| Calibración local del predictor por plano     | PB-07, PB-12        | S5                   |
| Heatmap por APs de interés (BSSID; ubicación AP referencial; puntos de lectura como fuente de interpolación) | PB-20, PB-05 | S4 |
| CCI / ACI en 2,4 GHz por separación de canales | PB-05, PB-07        | S4, S5               |
| Configuración y predicción separadas para 2,4/5 GHz | PB-07, PB-12 | S5 · aprobado / ajuste gobernanza |
| Medición observada inmutable vs valor proyectado | PB-07, PB-12 | S5 · aprobado / ajuste gobernanza |

> Referencias locales del libro: `02-rf-fundamentals.md` (dB/dBm), `03-spread-spectrum-technology.md` (canales 2,4 GHz y solapamiento), `05-antennas-and-accessories.md` (FSPL/regla de 6 dB) y `11-site-survey-fundamentals.md` (site survey, cobertura, dead spots e interferencias) dentro de [Certified Wireless Network Administrator - Official Study Guide Markdown](../../Certified%20Wireless%20Network%20Administrator%20-%20Official%20Study%20Guide%20Markdown/index.md).

---

## 7. Resumen de validación

✅ **7 / 9 RP** con cobertura de HU activa (RP4 y RP6 eliminados por refinamiento de alcance)
✅ **16 / 16 UC** activos cubiertos por HU (UC07, UC10 y UC14 eliminados)
✅ **17 / 17 HU** activas asignadas a sprint
✅ **Restricciones técnicas listadas** trazadas a HU y referencias CWNA locales
✅ **0 huérfanos** detectados

> Esta matriz se debe revisar al inicio de cada Sprint Planning (R-2) y al cierre de cada Sprint Review (R-4), conforme al EnfoqueScrumV3.
