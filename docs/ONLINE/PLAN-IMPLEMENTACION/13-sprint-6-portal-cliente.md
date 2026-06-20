# 13 — Sprint 6: Portal del Cliente (web)

**Duración:** 2 semanas (10 días hábiles) · **23 jun – 6 jul 2026**
**PHU comprometidos:** 26
**Objetivo del Sprint:**

> Habilitar el portal web público para clientes de Bulldog Tech.: el técnico genera un enlace único, el cliente accede sin login a una vista interactiva con su heatmap, análisis y plan de APs. Cierra el alcance del producto en su modalidad 100 % en línea.

**HU incluidas:** PB-15, PB-16, PB-17

---

## 1. Diagrama de secuencia — Acceso del cliente al enlace público

```plantuml
@startuml
title PB-15/16/17 — Acceso del cliente al portal con token único
skinparam sequenceArrowColor #2980B9
skinparam participantBackgroundColor #EBF5FB

actor "Técnico" as tech
actor "Cliente" as cliente
participant "Web (admin)\nReact" as wadm
participant "Web (portal)\nReact" as wcli
participant "Backend\n/api/share/*" as be
database "PostgreSQL" as db

tech -> wadm : "Generar enlace de cliente"\n(seleccionar proyecto, expiración 7d)
wadm -> be : POST /api/share/proyectos/{id}/enlaces
be -> db : INSERT token_enlace (token=uuid4, expira_en, ...)
db --> be : token
be --> wadm : 201 {urlPublica}
wadm -> tech : copiar / compartir enlace

== El cliente abre el enlace ==
cliente -> wcli : GET https://heatmapper.app/portal/{token}
wcli -> be : GET /api/share/{token}
be -> db : SELECT token_enlace WHERE token=? AND expira_en > now() AND revocado=false
alt token inválido / expirado / revocado
  db --> be : null
  be --> wcli : 404
  wcli -> cliente : "Enlace no válido o expirado"
else token válido
  db --> be : enlace
  be -> db : UPDATE token_enlace SET accesos = accesos + 1, ultimo_acceso = now()
  be -> db : SELECT proyecto + plano + heatmap activo + análisis + escenarios
  db --> be : payload
  be --> wcli : 200 {proyecto, heatmap, analisis, escenarios}
  wcli -> cliente : renderiza vista interactiva
end
@enduml
```

---

## 2. Diagrama de componentes — Portal del cliente

```plantuml
@startuml
title Componentes del Portal del Cliente (web)
skinparam componentBackgroundColor #EBF5FB
skinparam componentBorderColor #2980B9
skinparam interfaceBackgroundColor #FDFEFE
skinparam arrowColor #2980B9

package "web/portal-cliente" {
  [PortalLayout] as L
  [TokenGuard] as TG
  [HeatmapInteractivo\n(Konva.js)] as HI
  [PanelAnalisis] as PA
  [VistaEscenarios] as VE
  [DescargaPDFButton] as DPDF
  [api/shareClient.ts] as API
}
package "web/shared" {
  [TanStack Query Provider] as TQ
  [axios + tokenInterceptor] as AX
}
[PortalLayout] --> [TokenGuard]
[TokenGuard] --> [API]
[HeatmapInteractivo] --> [API]
[PanelAnalisis] --> [API]
[VistaEscenarios] --> [API]
[DescargaPDFButton] --> [API]
[API] --> [AX]
[AX] ..> [TQ] : usa para caché

note bottom of TG
  Valida token en cada request.
  Si 404 redirige a página de error.
  No expone JWT ni datos sensibles.
end note
@enduml
```

---

## 3. Historias de Usuario del Sprint 6 (F4)

### PB-15 — Generar Enlace Único para Cliente

```
Historia de Usuario
─────────────────────────────────────────────────────────────────
Id: PB-15   Nombre: Generar enlace único para cliente   Prioridad: Alta   PHU: 5

Como     : Técnico de Bulldog Tech.
Quiero   : Generar un enlace único, seguro y con expiración configurable
           para compartir un proyecto con el cliente sin que requiera login
Para     : Entregar resultados rápidamente sin gestionar credenciales

Reglas de negocio:
  · Token: UUID v4 + HMAC firmado con secret del backend (256 bits).
  · Expiración configurable: 1 día, 7 días, 30 días o personalizada.
  · Endpoint: POST /api/share/proyectos/{id}/enlaces {expiraEnDias} → 201.
  · Lista de enlaces activos por proyecto: GET /api/share/proyectos/{id}/enlaces.
  · Revocación: PATCH /api/share/enlaces/{id} {revocado: true} → 200.
  · El backend mantiene `accesos`, `ultimo_acceso` y `ip_ultimo_acceso` por
    enlace (auditoría).
  · El enlace generado tiene formato `https://{host}/portal/{token}`.

Criterios de aceptación:
  - CA1: Generar enlace → 201 con URL completa visible para el técnico.
  - CA2: Listar enlaces de un proyecto en la web admin con estado y métricas.
  - CA3: Revocar enlace → futuros accesos devuelven 404.
  - CA4: Token expirado devuelve 404 sin filtrar información del proyecto.
  - CA5: Botón "Copiar enlace" funciona en la web admin.
  - CA6: Validación: si la API recibe expiraEnDias > 365 → 422.

Desarrollador: Borys
```

### PB-16 — Ver Heatmap Interactivo en el Portal

```
Historia de Usuario
─────────────────────────────────────────────────────────────────
Id: PB-16   Nombre: Ver heatmap interactivo (web)   Prioridad: Alta   PHU: 13

Como     : Cliente de Bulldog Tech.
Quiero   : Abrir el enlace que me compartieron y ver el heatmap del edificio
           con zoom, pan, tooltips y leyenda
Para     : Entender visualmente la cobertura WiFi sin instalar nada

Reglas de negocio:
  · La vista carga sin pedir login (token en URL).
  · Render con Konva.js (canvas 2D performante).
  · Tooltip al hacer hover/tap muestra RSSI estimado y nivel CWNA-107.
  · Leyenda fija con los 5 niveles.
  · Botón "Cambiar algoritmo" oculto al cliente (solo admin).
  · La vista es responsive (móvil + desktop).
  · Performance: First Contentful Paint ≤ 2 s en 3G simulada con plano de
    1 MB; render del heatmap ≤ 2 s adicionales.

Criterios de aceptación:
  - CA1: Token válido → la página renderiza el plano + heatmap con leyenda.
  - CA2: Zoom (rueda/pinch) y pan (drag) funcionan en desktop y móvil.
  - CA3: Tooltip con RSSI estimado y nivel coloreado al hacer hover/tap.
  - CA4: Token inválido → página de error amigable sin filtrar datos.
  - CA5: Lighthouse ≥ 80 en Performance, ≥ 90 en Accessibility.
  - CA6: Sin warnings en consola en producción.

Desarrollador: Borys + Jhasmany
```

### PB-17 — Ver Análisis y Plan de APs en el Portal

```
Historia de Usuario
─────────────────────────────────────────────────────────────────
Id: PB-17   Nombre: Ver análisis y plan de APs (web)   Prioridad: Media   PHU: 8

Como     : Cliente de Bulldog Tech.
Quiero   : Ver el panel de análisis (cobertura, zonas muertas) y los
           escenarios propuestos con sus heatmaps proyectados, además de
           descargar el PDF
Para     : Tomar decisión informada sobre la inversión

Reglas de negocio:
  · El panel de análisis reusa la vista del Sprint 4 adaptada a web.
  · Carrusel/tabs de escenarios optimizados con preview del heatmap.
  · Botón "Descargar reporte PDF" → llama a un endpoint público que
    genera URL firmada del PDF asociada al token (no expone /api/reportes/{id}
    directamente).
  · Endpoint: GET /api/share/{token}/reporte → 302 a URL firmada del PDF
    o 404 si no hay reporte.

Criterios de aceptación:
  - CA1: Panel de análisis muestra: % cobertura, # zonas muertas, # solapamientos,
    # interferencias, lista de APs detectados.
  - CA2: Tabs de escenarios optimizados con costo, # APs y Δ cobertura.
  - CA3: Tap/click en un escenario muestra el heatmap proyectado a pantalla
    completa con leyenda.
  - CA4: Botón "Descargar PDF" descarga el reporte (si existe) o muestra
    "Reporte aún no disponible".
  - CA5: Sin información del técnico ni de otros proyectos visible.

Desarrollador: Borys + Jhasmany
```

---

## 4. Sprint Backlog (F5) — Sprint 6

### HU PB-15 (5 PHU)

| Id     | Tarea                                                                         | Resp. | Estim. |
| ------ | ----------------------------------------------------------------------------- | ----- | -----: |
| Sp6-01 | Migración Alembic `0007_token_enlace`                                         | Borys |   1 hr |
| Sp6-02 | Modelo + schemas + servicio de generación con HMAC                            | Borys |  3 hrs |
| Sp6-03 | Endpoints CRUD de enlaces + revocación + auditoría                            | Borys |  3 hrs |
| Sp6-04 | Tests pytest (generación, expiración, revocación, ownership)                  | Borys |  3 hrs |
| Sp6-05 | Vista admin "Enlaces del proyecto" con tabla + botones generar/revocar/copiar | Borys |  4 hrs |
| Sp6-06 | Aceptación con PO                                                             | Ambos |   1 hr |

### HU PB-16 (13 PHU)

| Id     | Tarea                                                                   | Resp.    | Estim. |
| ------ | ----------------------------------------------------------------------- | -------- | -----: |
| Sp6-07 | Endpoint `GET /api/share/{token}` (payload completo del proyecto)       | Borys    |  3 hrs |
| Sp6-08 | Tests pytest (token válido, inválido, expirado, revocado, contadores)   | Borys    |  3 hrs |
| Sp6-09 | Setup React Router con ruta `/portal/:token` + TokenGuard               | Jhasmany |  3 hrs |
| Sp6-10 | `api/shareClient.ts` (axios + react-query) generado desde OpenAPI       | Jhasmany |  2 hrs |
| Sp6-11 | Componente `HeatmapInteractivo` con Konva.js                            | Jhasmany |  8 hrs |
| Sp6-12 | Tooltip con RSSI estimado en posición del cursor                        | Jhasmany |  4 hrs |
| Sp6-13 | Leyenda + diseño responsive (Tailwind o CSS modules)                    | Jhasmany |  3 hrs |
| Sp6-14 | Página de error para token inválido/expirado                            | Jhasmany |  2 hrs |
| Sp6-15 | Optimización de performance (lazy load, code split, image optimization) | Jhasmany |  3 hrs |
| Sp6-16 | Lighthouse audit + ajustes de accesibilidad                             | Jhasmany |  3 hrs |
| Sp6-17 | Tests con Vitest + React Testing Library                                | Jhasmany |  4 hrs |
| Sp6-18 | Aceptación con PO                                                       | Ambos    |   1 hr |

### HU PB-17 (8 PHU)

| Id     | Tarea                                                                    | Resp.    | Estim. |
| ------ | ------------------------------------------------------------------------ | -------- | -----: |
| Sp6-19 | Endpoint `GET /api/share/{token}/reporte` con redirect 302 a URL firmada | Borys    |  2 hrs |
| Sp6-20 | Tests pytest del endpoint (con/sin reporte, token revocado)              | Borys    |  2 hrs |
| Sp6-21 | Componente `PanelAnalisis` (web)                                         | Jhasmany |  3 hrs |
| Sp6-22 | Componente `VistaEscenarios` con tabs                                    | Jhasmany |  4 hrs |
| Sp6-23 | Render del heatmap proyectado a pantalla completa                        | Jhasmany |  3 hrs |
| Sp6-24 | `DescargaPDFButton` con manejo de error                                  | Jhasmany |  2 hrs |
| Sp6-25 | Tests E2E con Playwright (flujo completo: token → vista → PDF)           | Jhasmany |  4 hrs |
| Sp6-26 | Aceptación con PO + sesión con cliente piloto                            | Ambos    |  2 hrs |

### Resumen Sprint 6

| Concepto          |   Valor |
| ----------------- | ------: |
| Total de tareas   |      26 |
| Horas estimadas   | ~80 hrs |
| Horas disponibles | ~80 hrs |
| Buffer            |   0 hrs |
| PHU comprometidos |      26 |

> **Nota de capacidad:** este sprint queda al 100 % de la capacidad. Si surge desviación, la primera HU candidata a recortar es PB-17 (carrusel de escenarios) manteniendo PB-15 y PB-16 como mínimo viable.

---

## 5. DoD específica del Sprint 6

- [ ] Migración `0007` aplicada y reversible
- [ ] Web portal desplegado en su propio container o ruta de Nginx (`/portal/*`)
- [ ] Tests E2E con Playwright pasan en CI/CD
- [ ] Lighthouse Performance ≥ 80 + Accessibility ≥ 90
- [ ] OWASP top 10 revisado: ningún endpoint público expone datos del técnico ni de otros proyectos
- [ ] Demo final: técnico genera enlace → comparte → cliente lo abre desde su navegador → revisa heatmap interactivo → descarga PDF
