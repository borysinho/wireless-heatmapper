# 9. Cronograma

La planificación temporal del proyecto se organiza en **siete iteraciones** alineadas con el marco Scrum: un Sprint inicial de definición (Sprint 0, una semana), seis Sprints de desarrollo de dos semanas (Sprints 1 al 6) y una semana de cierre para pruebas integradas y entrega final. La **revisión conjunta del Sprint 0 + Sprint 1 se realiza el 27 de abril de 2026**, conforme al hito M0 del plan.

A continuación se presenta un Diagrama de Gantt por cada Sprint (vista general, Sprint 0 y Sprint 1; los Sprints 2 al 6 figuran en el Plan de Implementación vigente).

## 9.1 Diagrama de Gantt — Plan general

```plantuml
@startgantt
title Plan general de Sprints — Wireless HeatMapper (modalidad 100 % en línea)
skinparam backgroundColor #FAFAFA
Project starts 2026-04-13
saturday are closed
sunday are closed

[Sprint 0 — Definición inicial] lasts 5 days
[Sprint 1 — Backend, Admin Web, Auth Móvil + CRUD] lasts 5 days
[Sprint 2 — Planos en línea] lasts 14 days
[Sprint 3 — Captura WiFi en línea] lasts 14 days
[Sprint 4 — Heatmap y Análisis] lasts 14 days
[Sprint 5 — IA, Comparación y Reportes] lasts 14 days
[Sprint 6 — Portal de Cliente] lasts 14 days
[Cierre — Pruebas integradas y entrega] lasts 5 days

[Sprint 1 — Backend, Admin Web, Auth Móvil + CRUD] starts at [Sprint 0 — Definición inicial]'s end
[Sprint 2 — Planos en línea] starts at [Sprint 1 — Backend, Admin Web, Auth Móvil + CRUD]'s end
[Sprint 3 — Captura WiFi en línea] starts at [Sprint 2 — Planos en línea]'s end
[Sprint 4 — Heatmap y Análisis] starts at [Sprint 3 — Captura WiFi en línea]'s end
[Sprint 5 — IA, Comparación y Reportes] starts at [Sprint 4 — Heatmap y Análisis]'s end
[Sprint 6 — Portal de Cliente] starts at [Sprint 5 — IA, Comparación y Reportes]'s end
[Cierre — Pruebas integradas y entrega] starts at [Sprint 6 — Portal de Cliente]'s end

-- Hitos --
[M0: Presentación conjunta S0+S1] happens 2026-04-27
[M1: Backend desplegado] happens at [Sprint 0 — Definición inicial]'s end
[M2: Login + CRUD Proyectos extremo a extremo] happens at [Sprint 1 — Backend, Admin Web, Auth Móvil + CRUD]'s end
@endgantt
```

> _Figura 4: Diagrama de Gantt general — distribución de Sprints del Wireless HeatMapper, abril–julio 2026._

## 9.2 Diagrama de Gantt — Sprint 0 (Definición Inicial)

```plantuml
@startgantt
title Sprint 0 — Definición Inicial (R-1)\n13 abr – 17 abr 2026
skinparam backgroundColor #FAFAFA
scale 1.5
Project starts 2026-04-13
saturday are closed
sunday are closed

[Sp0-01..05 Roles y backlog] lasts 1 day
[Sp0-06 Modelos UML] lasts 2 days
[Sp0-07..08 Repo + Docker] lasts 1 day
[Sp0-09..11 Backend + Alembic] lasts 1 day
[Sp0-12 Init Flutter] lasts 1 day
[Sp0-13 Init Web (Vite)] lasts 1 day
[Sp0-14 Nginx] lasts 1 day
[Sp0-15 CI/CD] lasts 1 day
[Sp0-16 Pre-commit] lasts 1 day
[Sp0-17 READMEs] lasts 1 day

[Sp0-06 Modelos UML] starts at [Sp0-01..05 Roles y backlog]'s end
[Sp0-07..08 Repo + Docker] starts at [Sp0-06 Modelos UML]'s end
[Sp0-09..11 Backend + Alembic] starts at [Sp0-07..08 Repo + Docker]'s end
[Sp0-12 Init Flutter] starts at [Sp0-09..11 Backend + Alembic]'s end
[Sp0-13 Init Web (Vite)] starts at [Sp0-09..11 Backend + Alembic]'s end
[Sp0-14 Nginx] starts at [Sp0-13 Init Web (Vite)]'s end
[Sp0-15 CI/CD] starts at [Sp0-14 Nginx]'s end
[Sp0-16 Pre-commit] starts at [Sp0-15 CI/CD]'s end
[Sp0-17 READMEs] starts at [Sp0-16 Pre-commit]'s end
@endgantt
```

> _Figura 5: Diagrama de Gantt — Sprint 0 (Definición Inicial), 13–17 abril 2026._

## 9.3 Diagrama de Gantt — Sprint 1 (Fundación CRUD)

```plantuml
@startgantt
title Sprint 1 — Backend + Admin Web + Auth Móvil + CRUD\n20 abr – 26 abr 2026
skinparam backgroundColor #FAFAFA
scale 1.5
Project starts 2026-04-20
saturday are closed
sunday are closed

[PB-13 Usuarios (web)] lasts 2 days
[PB-19 Clientes (web)] lasts 1 day
[PB-09 Auth (móvil)] lasts 2 days
[PB-18 Proyectos org] lasts 2 days
[PB-01 CRUD Proyecto] lasts 2 days
[PB-10 Historial proyectos] lasts 1 day
[R-4 Review + R-5 Retro] lasts 1 day

[PB-19 Clientes (web)] starts at [PB-13 Usuarios (web)]'s start
[PB-09 Auth (móvil)] starts at [PB-13 Usuarios (web)]'s end
[PB-18 Proyectos org] starts at [PB-13 Usuarios (web)]'s end
[PB-01 CRUD Proyecto] starts at [PB-09 Auth (móvil)]'s end
[PB-10 Historial proyectos] starts at [PB-01 CRUD Proyecto]'s end
[R-4 Review + R-5 Retro] starts at [PB-10 Historial proyectos]'s end
@endgantt
```

> _Figura 6: Diagrama de Gantt — Sprint 1 (Fundación CRUD), 20–26 abril 2026._

## 9.4 Sprints 2 al 6 (vista resumida)

| Sprint   | Período            | HU                  | PHU | Objetivo del Sprint                                                |
| -------- | ------------------ | ------------------- | --: | ------------------------------------------------------------------ |
| Sprint 2 | 28 abr – 11 may 26 | PB-02, PB-11        |  16 | Planos en línea (importar + calibrar)                              |
| Sprint 3 | 12 may – 25 may 26 | PB-03, PB-04        |  21 | Captura WiFi en línea con ingesta REST                             |
| Sprint 4 | 26 may – 8 jun 26  | PB-05, PB-06        |  26 | Heatmap (interpolación backend) + análisis automático de cobertura |
| Sprint 5 | 9 jun – 22 jun 26  | PB-07, PB-12, PB-08 |  42 | IA, comparación de escenarios y exportación de reportes            |
| Sprint 6 | 23 jun – 6 jul 26  | PB-15, PB-16, PB-17 |  26 | Portal de cliente y enlace único                                   |
| Cierre   | 7 jul – 11 jul 26  | RP6 + integración   |   — | Pruebas integradas, ajustes finales y entrega                      |

**Total Sprints 1–6 = 160 PHU**.
