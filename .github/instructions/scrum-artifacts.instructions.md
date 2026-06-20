---
applyTo: "docs/{SCRUM,ONLINE/PLAN-IMPLEMENTACION}/**/*.md"
description: "Convenciones para crear o editar artefactos Scrum (F3 Product Backlog, F4 Historias de Usuario, F5 Sprint Backlog) y eventos R-1..R-5 del Enfoque Scrum v3.2 (FICCT-UAGRM). Aplica al plan vigente en docs/ONLINE/PLAN-IMPLEMENTACION/ y al histórico en docs/SCRUM/."
---

# Convenciones de artefactos SCRUM

Estos archivos siguen el **Enfoque Scrum v3.2** del M.Sc. Rolando Martínez (ver [docs/EnfoqueScrumV3.md](../../docs/EnfoqueScrumV3.md)). Respetar estrictamente la nomenclatura, los formatos F3/F4/F5 y la estructura de cada referencia R-x.

> **Plan vigente (modalidad 100 % en línea):** [docs/ONLINE/PLAN-IMPLEMENTACION/](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md).
> **Plan histórico (modalidad offline, no vigente):** [docs/SCRUM/](../../docs/SCRUM/00-indice.md). No editar salvo correcciones puntuales; cambios de alcance se aplican únicamente al plan vigente.

## Identificadores

| Tipo                     | Patrón     | Ejemplo  |
| ------------------------ | ---------- | -------- |
| Historia de Usuario (PB) | `PB-NN`    | `PB-09`  |
| Tarea del Sprint Backlog | `Sp{N}-NN` | `Sp3-12` |
| Caso de uso              | `UCNN`     | `UC05`   |
| Requerimiento principal  | `RPN`      | `RP4`    |
| Evento Scrum             | `R-N`      | `R-3`    |
| Formato/plantilla        | `FN`       | `F5`     |

**Nunca** renumerar IDs existentes. Para nuevos elementos, continuar la secuencia (siguiente número libre) y actualizar:

- El [Product Backlog vigente](../../docs/ONLINE/PLAN-IMPLEMENTACION/05-product-backlog-online.md) si es una HU nueva.
- El Sprint Backlog correspondiente del [Plan de Implementación Online](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md) si es una tarea nueva.
- El [índice del plan vigente](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md) si se agrega un archivo.
- La [matriz de trazabilidad](../../docs/ONLINE/PLAN-IMPLEMENTACION/14-trazabilidad-rp-hu.md) si la HU mapea a uno o más RP.

## Historias de Usuario (F4)

Formato canónico (preservar literalmente):

```
Como    :  <rol>
Quiero  :  <acción/funcionalidad>
Para    :  <beneficio/objetivo>
```

Cada HU debe incluir las secciones **Descripción**, **Conversación / Reglas de Negocio** y **Criterios de aceptación** (con formato `CA1: Dado que ... cuando ... entonces ...`).

## Estimación

- **PHU** (Puntos de Historia de Usuario): escala Fibonacci `1, 2, 3, 5, 8, 13, 21`. No usar otros valores.
- Tareas del Sprint Backlog: estimar en **horas** (`N hrs`).
- Estados válidos: `Por hacer`, `En proceso`, `Terminado`, `Bloqueado`.

## Diagramas PlantUML

Usar el bloque ` ```plantuml ` (no `mermaid`). Mantener la paleta del proyecto:

```
skinparam <X>BackgroundColor #EBF5FB
skinparam <X>BorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7
```

Para casos de uso usar `left to right direction`. Para diagramas de estado usar emojis discretos solo en estados terminales (`Done ✅`, `Regresada ↩`) siguiendo el estilo ya presente en el [Product Backlog vigente](../../docs/ONLINE/PLAN-IMPLEMENTACION/05-product-backlog-online.md).

## Cabecera de cada archivo

Todo archivo de planificación Scrum (`docs/SCRUM/` o `docs/ONLINE/PLAN-IMPLEMENTACION/`) debe iniciar con un bloque de metadatos así:

```markdown
# <Título>

**Referencia:** Enfoque Scrum v3.2 — <sección>
**Proyecto:** Wireless HeatMapper
**<otros campos según el formato>**
```

## Restricciones técnicas a citar

Cuando una HU o tarea toque captura/análisis WiFi, citar los umbrales del **CWNA-107** ya establecidos:

- Zona muerta: `RSSI < −90 dBm`
- Objetivo de diseño: `≥ −70 dBm`
- Throttling Android ≥ 8.0: `máx. 4 scans / 2 min` en background
- Potencia recomendada AP: `1/4 a 1/3 del máximo`

No reformular estos valores; copiarlos textualmente para mantener trazabilidad con el [PAPS Online](<../../docs/ONLINE/Wireless Heatmapper - PAPS - Modalidad Online.md>).

## Qué NO hacer

- No traducir términos Scrum estandarizados (Sprint, Backlog, Daily, Review, Retrospective, Definition of Done).
- No introducir nuevos formatos `Fx` ni nuevas referencias `R-x`: el marco está cerrado en v3.2.
- No reordenar las HU del Product Backlog vigente: el orden refleja prioridad y dependencias incrementales (Sprint 1 → 6).
- No agregar PHU a HU ya estimadas sin pasar por una sesión de Planning Poker (registrarlo como nota, no como cambio directo).
- No editar archivos del plan histórico ([docs/SCRUM/](../../docs/SCRUM/00-indice.md)) para reflejar cambios de alcance: aplicar siempre al plan vigente ([docs/ONLINE/PLAN-IMPLEMENTACION/](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md)).
- No reintroducir PB-14 (sincronización offline): está eliminada en la modalidad oficial 100 % en línea.
