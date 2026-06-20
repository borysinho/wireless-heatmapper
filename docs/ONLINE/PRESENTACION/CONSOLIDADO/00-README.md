# CONSOLIDADO — Wireless HeatMapper · Perfil de Proyecto (Sprint 0 + Sprint 1)

Esta carpeta contiene los documentos Markdown numerados que componen el **Perfil de Proyecto** consolidado del sistema **Wireless HeatMapper**, modalidad 100 % en línea, gestionado mediante el marco de trabajo Scrum.

## Propósito

Los archivos de esta carpeta están diseñados para ser **concatenados de forma consecutiva** (orden lexicográfico de nombre) y convertidos automáticamente a un único documento Word (`.docx`) mediante una herramienta de procesamiento (p. ej. `pandoc`). Por ello:

- Cada archivo representa una sección o subsección coherente.
- No se repiten encabezados de portada en archivos intermedios.
- Las referencias a diagramas PlantUML se mantienen como bloques ` ```plantuml ` para permitir su renderización por la cadena de conversión.
- Las imágenes y diagramas externos se referencian con rutas relativas válidas desde esta carpeta.

## Orden de concatenación

| #   | Archivo                             | Sección de la estructura oficial          |
| --- | ----------------------------------- | ----------------------------------------- |
| 01  | `01-portada.md`                     | Portada                                   |
| 02  | `02-indice.md`                      | Índice (marcador para generación)         |
| 03  | `03-introduccion.md`                | Introducción                              |
| 04  | `04-antecedentes.md`                | Antecedentes (revisión, apps, caso)       |
| 05  | `05-descripcion-problema.md`        | Descripción del problema                  |
| 06  | `06-situacion-problematica.md`      | Situación problemática                    |
| 07  | `07-situacion-deseada.md`           | Situación deseada                         |
| 08  | `08-objetivos.md`                   | Objetivos del proyecto                    |
| 09  | `09-alcance.md`                     | Alcance                                   |
| 10  | `10-tecnologia.md`                  | Tecnología (estrategia, métodos, tools)   |
| 11  | `11-cronograma.md`                  | Cronograma                                |
| 12  | `12-proceso-scrum-definiciones.md`  | 12.1 Definiciones del proceso (Scrum)     |
| 13  | `13-sprint-0-definicion-inicial.md` | R-1 — Sprint 0                            |
| 14  | `14-sprint-1-planning.md`           | 12.2 Sprint 1 — Planning                  |
| 15  | `15-sprint-1-historias-usuario.md`  | 12.2 Sprint 1 — Historias de Usuario (F4) |
| 16  | `16-sprint-1-sprint-backlog.md`     | 12.2 Sprint 1 — Sprint Backlog (F5)       |
| 17  | `17-sprint-1-patron-desarrollo.md`  | 12.2 Sprint 1 — Patrón de Desarrollo      |
| 18  | `18-sprint-1-ejecucion.md`          | R-3 — Ejecución del Sprint 1              |
| 19  | `19-sprint-1-review.md`             | R-4 — Sprint Review                       |
| 20  | `20-sprint-1-retrospective.md`      | R-5 — Sprint Retrospective                |
| 21  | `21-bibliografia.md`                | Bibliografía                              |
| 22  | `22-anexos.md`                      | Anexos A, B, C                            |

## Comando sugerido para conversión a Word

```bash
cd docs/ONLINE/PRESENTACION/CONSOLIDADO
pandoc $(ls *.md | grep -v '^00-') -o WirelessHeatMapper-PerfilProyecto-S0-S1.docx \
  --from=markdown+yaml_metadata_block \
  --reference-doc=../plantilla-word.dotx \
  --toc --toc-depth=3
```

> **Nota:** Los bloques PlantUML deben procesarse previamente (p. ej. con el filtro `pandoc-plantuml-filter`) o reemplazarse por imágenes pre-renderizadas antes del paso final.

## Trazabilidad

Toda la información contenida en estos documentos proviene de:

- [docs/ONLINE/Wireless Heatmapper - PAPS - Modalidad Online.md](../../Wireless%20Heatmapper%20-%20PAPS%20-%20Modalidad%20Online.md) — fuente normativa del Plan del Proyecto.
- [docs/ONLINE/PRESENTACION/presentacion-scrum-s0-s1.md](../presentacion-scrum-s0-s1.md) — proceso Scrum consolidado de Sprint 0 y Sprint 1.
- [docs/ONLINE/PRESENTACION/diagramas-diseno-sprint-1/](../diagramas-diseno-sprint-1/) — diagramas UML de diseño del Sprint 1.
- [docs/ONLINE/PLAN-IMPLEMENTACION/](../../PLAN-IMPLEMENTACION/) — plan de Sprints vigente.

Última actualización: 27 de abril de 2026.
