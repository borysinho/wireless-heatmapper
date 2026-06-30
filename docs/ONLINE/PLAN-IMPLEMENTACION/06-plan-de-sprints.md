# 06 — Plan de Sprints

**Referencia:** PAPS Online §14 (Gantt + PERT) y §13 (Ecuación del Software)
**Equipo:** 2 desarrolladores (multifuncionales y autogestionados)
**Duración estándar de Sprint:** 2 semanas (10 días hábiles)
**Capacidad por Sprint:** 80 hrs (2 devs × 4 hrs efectivas/día × 10 días) → ~72 hrs comprometidas + 10 % buffer

---

## 1. Diagrama de Gantt

```plantuml
@startgantt
title Plan de Sprints — Wireless HeatMapper (modalidad 100 % en línea)
skinparam backgroundColor #FAFAFA
Project starts 2026-04-13
saturday are closed
sunday are closed

[Sprint 0 — Definición inicial e infraestructura] lasts 5 days
[Sprint 1 — Backend, Admin Web, Auth Móvil + CRUD Proyectos] lasts 5 days
[Sprint 2 — Planos en línea (importar + calibrar)] lasts 14 days
[Sprint 3 — Captura WiFi en línea] lasts 14 days
[Sprint 4 — Conjuntos AP + Heatmap] lasts 14 days
[Sprint 5 — IA y Comparación] lasts 14 days
[Sprint 6 — Portal de Cliente] lasts 14 days
[Cierre — Pruebas integradas y entrega] lasts 5 days

[Sprint 1 — Backend, Admin Web, Auth Móvil + CRUD Proyectos] starts at [Sprint 0 — Definición inicial e infraestructura]'s end
[Sprint 2 — Planos en línea (importar + calibrar)] starts at [Sprint 1 — Backend, Admin Web, Auth Móvil + CRUD Proyectos]'s end
[Sprint 3 — Captura WiFi en línea] starts at [Sprint 2 — Planos en línea (importar + calibrar)]'s end
[Sprint 4 — Conjuntos AP + Heatmap] starts at [Sprint 3 — Captura WiFi en línea]'s end
[Sprint 5 — IA y Comparación] starts at [Sprint 4 — Conjuntos AP + Heatmap]'s end
[Sprint 6 — Portal de Cliente] starts at [Sprint 5 — IA y Comparación]'s end
[Cierre — Pruebas integradas y entrega] starts at [Sprint 6 — Portal de Cliente]'s end

-- Hitos --
[M0: Presentación conjunta S0+S1] happens 2026-04-27
[M1: Backend desplegado] happens at [Sprint 0 — Definición inicial e infraestructura]'s end
[M2: Login + CRUD Proyectos extremo a extremo] happens at [Sprint 1 — Backend, Admin Web, Auth Móvil + CRUD Proyectos]'s end
[M3: Mediciones persistidas en línea] happens at [Sprint 3 — Captura WiFi en línea]'s end
[M4: Heatmap visible en la app] happens at [Sprint 4 — Conjuntos AP + Heatmap]'s end
[M5: Propuesta IA comparable] happens at [Sprint 5 — IA y Comparación]'s end
[M6: Cliente accede al portal] happens at [Sprint 6 — Portal de Cliente]'s end
@endgantt
```

---

## 2. Diagrama PERT (dependencias entre sprints)

```plantuml
@startuml
title Diagrama PERT — Dependencias entre Sprints\nWireless HeatMapper (modalidad 100 % en línea)
skinparam activityBackgroundColor #EBF5FB
skinparam activityBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

start
:S0 · Infra (1 sem);
:S1 · Auth + Admin (1 sem);
:S2 · Proyectos + Planos (2 sem);
:S3 · Captura WiFi (2 sem);
:S4 · Conjuntos AP + Heatmap (2 sem);
:S5 · IA + Comparación (2 sem);
note right
  Ruta crítica: S0 → S1 → S2 → S3 → S4 → S5 → S6
  S0+S1 se presentan juntos el 27 abr 2026.
  Sprint 5 ajustado a 2 sem (antes 3).
end note
:S6 · Portal de Cliente (2 sem);
:Cierre (1 sem);
stop
@enduml
```

**Ruta crítica:** Sprint 0 → Sprint 1 → Sprint 2 → Sprint 3 → Sprint 4 → Sprint 5 → Sprint 6 → Cierre.

Total: 5 + 5 + 14 + 14 + 14 + 14 + 14 + 5 = **85 días hábiles ≈ 4 meses** (S0+S1 presentados juntos el 27 abr 2026; desde abril hasta julio 2026).

---

## 3. Objetivos por Sprint

| Sprint   | Objetivo del Sprint                                                                                                                              | Demo en R-4                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Sprint 0 | Tener un backend "hello world" con Docker Compose, PostgreSQL inicializado, CI/CD funcionando y modelos UML aprobados                            | `curl /api/health` → 200 OK                                                        |
| Sprint 1 | El admin crea técnicos y clientes en el panel web; un técnico inicia sesión desde la app móvil y gestiona (CRUD) sus proyectos contra el backend | Crear usuario y cliente en web → loguearse en app → crear/editar/archivar proyecto |
| Sprint 2 | Un técnico sube un plano (PNG/PDF) y lo calibra sobre un proyecto existente; todo persiste en PostgreSQL                                         | Recorrido completo plano + calibración                                             |
| Sprint 3 | Un técnico marca puntos sobre el plano y captura mediciones WiFi que se persisten en línea en el backend                                         | Demo en vivo de captura → BD muestra registros                                     |
| Sprint 4 | El técnico organiza APs por propósito y genera heatmaps por AP/subconjunto/conjunto desde el backend                                              | Conjunto AP + heatmap renderizado en móvil                                         |
| Sprint 5 | El administrador genera propuestas IA como conjuntos AP derivados y compara mapas actuales/proyectados sin alterar mediciones reales              | Recomendación IA + comparación entre conjunto técnico y conjunto IA                |
| Sprint 6 | El técnico genera un enlace; el cliente lo abre en navegador y ve heatmap, análisis y plan AP                                                    | Demo del portal de cliente con token real                                          |

---

## 4. Asignación tentativa de horas por componente y Sprint

| Sprint   | Backend (Python) | App móvil (Flutter) | Web (React) | IA / ML | Total est. |
| -------- | ---------------: | ------------------: | ----------: | ------: | ---------: |
| Sprint 0 |               20 |                   8 |           4 |       — |         32 |
| Sprint 1 |               30 |                  20 |          22 |       — |         72 |
| Sprint 2 |               25 |                  35 |          10 |       — |         70 |
| Sprint 3 |               20 |                  45 |           5 |       — |         70 |
| Sprint 4 |               45 |                  32 |           6 |       — |       83\* |
| Sprint 5 |               25 |                  10 |          18 |      40 |       93\* |
| Sprint 6 |               15 |                  10 |          45 |       — |         70 |

\* Sprint 4 queda levemente excedido por incorporación de PB-20; Sprint 5 excede capacidad por IA y comparación, pero PB-08/PDF fue eliminado.

---

## 5. Velocidad esperada y burndown

```plantuml
@startuml
title Velocidad esperada por Sprint (PHU planificados)
skinparam defaultTextAlignment center
skinparam backgroundColor #FAFAFA

scale 1
concise "PHU comprometidos" as PHU

@PHU
0 is "Sprint 0: 0"
1 is "Sprint 1: 29"
2 is "Sprint 2: 16"
3 is "Sprint 3: 21"
4 is "Sprint 4: 21"
5 is "Sprint 5: 29"
6 is "Sprint 6: 26"
@enduml
```

> Si la velocidad real difiere en más de 20 % de la planificada durante **dos sprints consecutivos**, el equipo convoca reunión extraordinaria para re-priorizar el backlog (PAPS Online §18.2).

---

## 6. Hitos y entregables

| Hito  | Después de | Entregable verificable                                                                   |
| ----- | ---------- | ---------------------------------------------------------------------------------------- |
| M1    | Sprint 0   | `docker compose up` levanta `db + backend + web + nginx`; CI verde                       |
| M2    | Sprint 1   | Login extremo a extremo + CRUD de proyectos en móvil (admin web + técnico móvil) con JWT |
| M3    | Sprint 3   | Filas en `medicion_wifi` provenientes de la app durante una captura en vivo              |
| M4    | Sprint 4   | Conjunto AP + imagen heatmap devueltos por el backend y mostrados en app                 |
| M5    | Sprint 5   | Conjunto IA derivado + heatmap proyectado + comparación                                  |
| M6    | Sprint 6   | URL pública con token válido renderizando la vista de cliente completa                   |
| Final | Cierre     | Documentación + APK firmado + URL del backend + URL del panel admin                      |
