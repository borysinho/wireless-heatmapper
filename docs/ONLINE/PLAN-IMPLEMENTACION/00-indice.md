# Plan de Implementación SCRUM — Wireless HeatMapper (Modalidad 100 % en línea)

**Proyecto:** Sistema Inteligente de Análisis y Optimización de Cobertura WiFi mediante Mapas de Calor
**Modalidad:** 100 % en línea (sin persistencia local de dominio en el dispositivo móvil ni sincronización diferida)
**Marco de trabajo:** Scrum (Enfoque v3.2 — M.Sc. Ing. Rolando Martínez Canedo, FICCT-UAGRM)
**Materia:** Ingeniería de Software II — Grupo 24
**Equipo:** Jhasmany Jhunnior Fernandez Ortega · Herland Borys Quiroga Flores
**Versión:** 1.0 — Abril 2026

---

## Propósito de este plan

Este directorio contiene la documentación operativa del proceso Scrum aplicado al desarrollo del **Wireless HeatMapper en su modalidad 100 % en línea**, según se define en el [PAPS Online](../Wireless%20Heatmapper%20-%20PAPS%20-%20Modalidad%20Online.md). A diferencia del plan original en [docs/SCRUM/](../../SCRUM/00-indice.md), este plan:

- Elimina toda referencia a almacenamiento local de dominio en la app móvil (no SQLite/sqflite, no `drift`).
- Reemplaza la operación de **sincronización diferida** por **acceso transaccional en línea** desde el primer Sprint.
- Sitúa el **panel de administración web (RP7)** en el Sprint 1, dado que el aprovisionamiento previo de cuentas de técnicos es prerrequisito de la autenticación móvil (RP8/RP9).
- Reordena el resto del backlog de acuerdo a la ruta crítica del PAPS Online (A → J → C → D → F → G → M → I).

> Este plan es **únicamente documentación**. La implementación se ejecutará en un proceso posterior tomando estos documentos como insumo.

---

## Estructura del directorio

| #   | Archivo                                                                              | Contenido                                                                               |
| --- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| 00  | [00-indice.md](00-indice.md)                                                         | Índice del plan (este archivo)                                                          |
| 01  | [01-marco-scrum-online.md](01-marco-scrum-online.md)                                 | Marco Scrum, equipo, roles y Definition of Done                                         |
| 02  | [02-modelo-contexto.md](02-modelo-contexto.md)                                       | Modelo de contexto (UC01–UC18) en arquitectura cliente-servidor en línea                |
| 03  | [03-modelo-arquitectura.md](03-modelo-arquitectura.md)                               | Diagramas de paquetes y de despliegue (modalidad online)                                |
| 04  | [04-modelo-datos.md](04-modelo-datos.md)                                             | Diagrama de clases conceptual y modelo lógico — única fuente PostgreSQL                 |
| 05  | [05-product-backlog-online.md](05-product-backlog-online.md)                         | F3 — Product Backlog completo ajustado a modalidad online                               |
| 06  | [06-plan-de-sprints.md](06-plan-de-sprints.md)                                       | Gantt, PERT, objetivos por Sprint y velocidad esperada                                  |
| 07  | [07-sprint-0-definicion-inicial.md](07-sprint-0-definicion-inicial.md)               | R-1 · Sprint 0: equipo, infraestructura backend, contenedores y CI/CD                   |
| 08  | [08-sprint-1-fundacion-backend-y-admin.md](08-sprint-1-fundacion-backend-y-admin.md) | R-2/R-3 · Sprint 1: backend base, panel admin web, autenticación móvil                  |
| 09  | [09-sprint-2-proyectos-y-planos.md](09-sprint-2-proyectos-y-planos.md)               | Sprint 2: gestión de proyectos en línea, importación y calibración de planos            |
| 10  | [10-sprint-3-captura-online.md](10-sprint-3-captura-online.md)                       | Sprint 3: captura WiFi con ingesta REST y marcado de puntos                             |
| 11  | [11-sprint-4-heatmap-y-analisis.md](11-sprint-4-heatmap-y-analisis.md)               | Sprint 4: conjuntos de APs y motor de interpolación                                    |
| 12  | [12-sprint-5-ia-comparacion-y-reportes.md](12-sprint-5-ia-comparacion-y-reportes.md) | Sprint 5: módulo IA con conjuntos AP derivados                                         |
| 13  | [13-sprint-6-portal-cliente.md](13-sprint-6-portal-cliente.md)                       | Sprint 6: portal de cliente, enlace único y supervisión organizacional                  |
| 14  | [14-trazabilidad-rp-hu.md](14-trazabilidad-rp-hu.md)                                 | Matriz de trazabilidad RP ↔ HU ↔ Sprint ↔ UC                                            |
| 15  | [15-gestion-riesgos.md](15-gestion-riesgos.md)                                       | Riesgos del plan de implementación y plan de mitigación por sprint                      |
| 16  | [16-plan-validacion-sprint-1.md](16-plan-validacion-sprint-1.md)                     | Plan de validación exhaustivo del Sprint 1: tests, DoD, brechas y pruebas de aceptación |
| 17  | [17-especificacion-optimizacion-rf/](17-especificacion-optimizacion-rf/00-indice.md) | Especificación técnica de optimización RF, subordinada a las reglas 18 y al modelo 19   |
| 18  | [18-reglas-gobernanza-conjuntos-ap-heatmaps.md](18-reglas-gobernanza-conjuntos-ap-heatmaps.md) | Reglas de gobierno para conjuntos de APs, heatmaps, IA y publicación por enlace        |
| 19  | [19-modelo-base-datos-implementado.md](19-modelo-base-datos-implementado.md)         | Diagrama físico implementado de base de datos PostgreSQL con relaciones y flujos        |

---

## Mapa de sprints (resumen)

| Sprint       | Duración  | HU principales                           | Objetivo del Sprint                                                  | Valor entregado                                                                | Estado          |
| ------------ | --------- | ---------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------- |
| **Sprint 0** | 1 semana · 13–17 abr 2026 | —                                        | Definición inicial: equipo, infra, modelos base                      | Backend "hello world" con CI, contenedores levantados                          | ✅ Implementado |
| **Sprint 1** | 1 semana · 20–26 abr 2026 | PB-13, PB-19, PB-09, PB-18, PB-01, PB-10 | Fundación CRUD: backend + admin web + auth móvil + CRUD de proyectos | Admin gestiona técnicos y clientes; técnico hace login y CRUD de sus proyectos | ✅ Implementado |
| **Sprint 2** | 2 semanas · 28 abr–11 may 2026 | PB-02, PB-11                             | Planos en línea (importar + calibrar)                                | Técnico sube planos al backend y los calibra                                   | ✅ Implementado |
| **Sprint 3** | 2 semanas · 12–25 may 2026     | PB-03, PB-04                             | Captura de señal WiFi en línea con ingesta REST                      | Mediciones en vivo persistidas en PostgreSQL                                   | ✅ Implementado |
| **Sprint 4** | 2 semanas · 26 may–8 jun 2026  | PB-20, PB-05                             | Conjuntos de APs + heatmap backend                                  | Técnico genera heatmaps por propósito, AP individual o subconjunto             | ✅ Implementado |
| **Sprint 5** | 2 semanas · 9–22 jun 2026      | PB-07, PB-12                             | IA como conjuntos AP derivados                                      | Propuestas IA trazables desde conjuntos técnicos                               | ✅ Implementado |
| **Sprint 6** | 2 semanas · 23 jun–6 jul 2026  | PB-15, PB-16, PB-17                      | Portal de cliente + enlace único                                     | Cliente accede a conjuntos y heatmaps seleccionados por enlace                 | ⏳ Planificado  |

> **Nota sobre PB-14:** la Historia de Usuario "Sincronizar proyecto al servidor" del backlog original **se elimina** en esta modalidad, dado que toda operación de dominio ya se ejecuta en línea contra el backend desde el Sprint 1. El cierre del proyecto y la generación del enlace público se cubren con PB-15 en el Sprint 6.

> **Nota de presentación:** Sprint 0 y Sprint 1 se presentan juntos el **lunes 27 de abril de 2026** (Sprint Review conjunto). Cada sprint tiene 2 semanas de duración (Sprint 0 = semana 1, Sprint 1 = semana 2). Sprint 2 inicia el martes 28 de abril. El cierre del proyecto está previsto para el **11 de julio de 2026**.

> **Nota sobre PB-19, PB-01 y PB-10 (Sprint 1):** PB-19 (gestión de clientes) se sumó al alcance del Sprint 1 como prerrequisito del selector de cliente al crear proyectos. PB-01 y PB-10 (CRUD e historial móvil de proyectos) se adelantaron desde el Sprint 2 al Sprint 1 para consolidar la fundación CRUD `Usuario` / `Cliente` / `Proyecto` en una sola entrega.

---

## Trazabilidad rápida

> Mapeo conforme [PAPS Online §7](../Wireless%20Heatmapper%20-%20PAPS%20-%20Modalidad%20Online.md). Detalle completo en [14-trazabilidad-rp-hu.md](14-trazabilidad-rp-hu.md).

- **RP1 — Captura de señal WiFi (en línea):** Sprint 3 (PB-03)
- **RP2 — Mapeo sobre plano:** Sprint 2 (PB-02, PB-11) + Sprint 3 (PB-04)
- **RP3 — Generación de heatmap (en backend):** Sprint 4 (PB-20, PB-05)
- **RP4 — Análisis de cobertura:** fuera de alcance vigente (PB-06 eliminada)
- **RP5 — Optimización IA:** Sprint 5 (PB-07, PB-12), como conjuntos AP derivados
- **RP6 — Generación de reportes:** fuera de alcance vigente (PB-08 eliminada)
- **RP7 — Administración de usuarios:** Sprint 1 (PB-13, PB-19, PB-18)
- **RP8 — Persistencia centralizada en línea:** Sprint 1 (PB-09, PB-01, PB-10) y transversal en sprints siguientes
- **RP9 — Portal de cliente:** Sprint 6 (PB-15, PB-16, PB-17)

Detalle completo en [14-trazabilidad-rp-hu.md](14-trazabilidad-rp-hu.md).

> **Nota de gobierno móvil/web:** las reglas para conjuntos técnicos en móvil, heatmaps operativos, IA restringida a backend/web y publicación por enlace están registradas en [18-reglas-gobernanza-conjuntos-ap-heatmaps.md](18-reglas-gobernanza-conjuntos-ap-heatmaps.md).

---

## Convenciones

- **Identificadores estables:** `RP1..RP9` (PAPS), `PB-01..PB-19` (Product Backlog), `Sp{N}-NN` (tareas), `UC01..UC19` (casos de uso, UC14 eliminado), `R-1..R-5` (eventos Scrum).
- **Formatos:** F3 (Product Backlog), F4 (Historia de Usuario), F5 (Sprint Backlog).
- **Diagramas:** PlantUML embebido en bloques ` ```plantuml ` (compatible con StarUML 2.5+ y extensiones de VS Code). Paleta visual: `#EBF5FB` (fondo), `#2980B9` (bordes), `#FFFDE7` (notas).
- **Idioma:** español (es-BO) en toda la documentación, identificadores de negocio y comentarios.
- **Umbrales técnicos CWNA-107 preservados:**
  - RSSI < −90 dBm = zona muerta
  - Objetivo de diseño ≥ −70 dBm
  - Throttling Android ≥ 8.0 = 4 escaneos cada 2 minutos
  - Potencia recomendada de AP = 1/4 a 1/3 de su máximo
