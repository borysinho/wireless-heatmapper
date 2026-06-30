# 11 — Sprint 4: Conjuntos AP y Heatmap (backend)

**Duración:** 2 semanas (10 días hábiles) · **26 may – 8 jun 2026**
**PHU comprometidos:** 21
**Objetivo del Sprint:**

> Implementar conjuntos persistentes de APs por plano con propósito explícito, y sobre cada conjunto generar mapas de calor mediante interpolación espacial IDW en el backend FastAPI. Dentro de un conjunto, el técnico puede generar heatmaps para un AP individual, un subconjunto de APs o el conjunto completo. Al cierre, un técnico organiza los APs detectados por propósito y genera el heatmap requerido sobre el plano de su proyecto.

**HU incluidas:** PB-20, PB-05  
**HU eliminada por refinamiento:** PB-06 (sin diagnóstico persistido)  
**Restricciones:** latencia p95 del heatmap ≤ 3 s para hasta 200 puntos · cobertura objetivo ≥ −70 dBm · zona muerta < −90 dBm.

---

## 1. Diagrama de secuencia — Solicitud de heatmap

```plantuml
@startuml
title PB-05 — Generación de heatmap (interpolación en backend)
skinparam sequenceArrowColor #2980B9
skinparam participantBackgroundColor #EBF5FB

actor "Técnico" as tech
participant "App Móvil\n(HeatmapPage)" as app
participant "ApiClient" as api
participant "Backend\n/api/planos/{id}/heatmap" as be
participant "InterpolacionService\n(IDW)" as svc
database "PostgreSQL" as db
participant "ImageService\n(matplotlib + PIL)" as img

tech -> app : ingresar a un conjunto de APs\nseleccionar AP individual/subconjunto/todo
app -> api : POST /conjuntos-ap/{id}/heatmaps\n{modo, bssids, algoritmo, resolucion}
api -> be : HTTPS
be -> db : validar conjunto + SELECT puntos\nmejor RSSI de APs seleccionados por punto
db --> be : List<Punto + RSSI>
be -> svc : interpolar(puntos, ancho_px, alto_px, resolucion)
svc --> be : Matriz NxM de RSSI estimado
be -> img : render PNG colorizado (verde→rojo)
img --> be : bytes PNG
be -> db : INSERT mapa_calor (datos JSONB + ref imagen)
be --> app : 200 {urlImagen, matriz, escala}
app -> tech : superpone heatmap traslúcido sobre el plano
@enduml
```

---

## 2. Diagrama de componentes — Backend del heatmap

```plantuml
@startuml
title Componentes del módulo de Heatmap (backend)
skinparam componentBackgroundColor #EBF5FB
skinparam componentBorderColor #2980B9
skinparam interfaceBackgroundColor #FDFEFE
skinparam arrowColor #2980B9

[heatmap_router] as R
[InterpolacionService] as IS
[ImageService] as IMG
[MedicionRepository] as MR
[MapaCalorRepository] as MCR
database "PostgreSQL" as DB

R --> IS
IS --> MR
IS --> IMG
IS --> MCR
MR --> DB
MCR --> DB

note bottom of IS
  Algoritmos:
  - IDW (algoritmo oficial único)
  Resolución configurable (64/128/256).
end note

@enduml
```

---

## 3. Historias de Usuario del Sprint 4 (F4)

### PB-20 — Gestionar Conjuntos de APs por Plano

```
Historia de Usuario
─────────────────────────────────────────────────────────────────
Id: PB-20   Nombre: Gestionar conjuntos de APs por plano   Prioridad: Alta   PHU: 8

Como     : Técnico de campo
Quiero   : Crear conjuntos de APs con un propósito específico dentro de cada plano
Para     : Generar heatmaps focalizados sin rehacer la selección manual cada vez

Descripción:
  Cada plano puede tener múltiples APs detectados a partir de sus capturas. El
  técnico organiza esos APs en conjuntos persistentes, por ejemplo "Red
  corporativa principal", "APs de invitados", "APs críticos para roaming" o
  "AP sospechoso". Al ingresar a un conjunto, puede generar heatmaps para un
  AP individual, un subconjunto de ese conjunto o todo el conjunto.

Reglas de negocio:
  · Cada conjunto pertenece a un solo plano y a los proyectos del técnico autenticado.
  · El conjunto tiene nombre obligatorio y propósito obligatorio.
  · Un conjunto debe incluir al menos 1 AP detectado en las mediciones del plano.
  · No se puede agregar un BSSID que no exista en las mediciones del plano.
  · El sistema ofrece un conjunto virtual "Todos los APs detectados" cuando el
    plano tiene mediciones, pero los conjuntos creados por el técnico se
    persisten en PostgreSQL.
  · El propósito del conjunto se conserva para trazabilidad en los mapas de
    calor y propuestas IA posteriores.
  · Al modificarse las mediciones del plano, los conjuntos se mantienen, pero
    el backend valida de nuevo los BSSID antes de generar un heatmap.

Criterios de aceptación:
  - CA1: Crear conjunto con nombre, propósito y 1+ BSSID válidos → 201 y aparece
    en la lista del plano.
  - CA2: Crear conjunto sin propósito o sin APs → 422 con mensaje claro.
  - CA3: Intentar agregar un BSSID inexistente para el plano → 422.
  - CA4: Editar nombre, propósito o miembros → 200 y se preserva la trazabilidad
    de heatmaps ya generados.
  - CA5: El técnico ve la lista de conjuntos del plano con cantidad de APs y
    fecha de actualización.
  - CA6: Desde un conjunto puede elegir AP individual, subconjunto o conjunto
    completo antes de solicitar el heatmap.

Desarrollador: Borys (backend) + Jhasmany (móvil)
```

### PB-05 — Generar Mapa de Calor

```
Historia de Usuario
─────────────────────────────────────────────────────────────────
Id: PB-05   Nombre: Generar mapa de calor   Prioridad: Alta   PHU: 13

Como     : Técnico de campo
Quiero   : Ver un mapa de calor continuo (verde→rojo) sobre el plano,
           generado por el backend a partir de mis mediciones
Para     : Visualizar la distribución de cobertura WiFi del edificio

Reglas de negocio:
  · Antes de generar el mapa, el técnico ingresa a un conjunto de APs del plano
    y selecciona el modo de generación: AP individual, subconjunto o conjunto
    completo.
  · El mapa conserva `conjunto_ap_id`, modo de generación y BSSID usados para
    que el portal cliente explique el propósito del heatmap.
  · El heatmap se calcula con las mediciones de los APs seleccionados, tomando
    por punto la mejor señal disponible entre esos APs; no usa un agregado global
    de todas las redes.
  · La ubicación de los APs sobre el plano es referencial para visualización y
    análisis; no se usa como muestra RSSI sintética para interpolar.
  · Dentro de un conjunto, la app permite alternar entre vista de todo el
    conjunto, subconjunto temporal y AP individual, regenerando el mapa con los
    BSSID correspondientes sin modificar el conjunto persistente.
  · La respuesta incluye los puntos de lectura usados, RSSI mínimo/promedio/máximo
    y advertencias cuando la densidad de muestras puede producir un mapa uniforme.
  · Algoritmo disponible: IDW (oficial único).
  · Resoluciones: 64×64, 128×128, 256×256 (default 128).
  · Escala visual de calidad RSSI:
      ≥ −60 dBm → verde oscuro (Excelente)
      −61 a −67 → verde claro (Muy buena)
      −68 a −70 → verde lima (Buena, límite de diseño)
      −71 a −75 → amarillo (Advertencia operativa)
      −76 a −80 → naranja (Débil)
      −81 a −90 → rojizo (Muy débil)
      < −90    → rojo (Zona muerta oficial)
  · Mínimo de 5 puntos para generar heatmap; menos → 422.
  · Cada generación crea un nuevo registro en `mapa_calor`; el último por
    plano se considera "activo".
  · Latencia objetivo: p95 ≤ 3 s para 200 puntos.
  · El backend cachea el heatmap por (plano_id, conjunto_ap_id, modo, BSSID,
    algoritmo, resolución, firma de mediciones) y lo invalida cuando cambian
    las mediciones relevantes.

Criterios de aceptación:
  - CA1: Generar desde un conjunto con 5+ puntos de lectura → 200 con URL de
    imagen, matriz, puntos usados, métricas RSSI, conjunto_ap_id y modo.
  - CA2: Selección con < 5 puntos de lectura → 422 con mensaje
    "Se requieren al menos 5 puntos de los APs seleccionados".
  - CA3: Latencia p95 ≤ 3 s con 200 puntos (medida con `pytest-benchmark`).
  - CA4: La app superpone el heatmap sobre el plano con transparencia 60 %,
    leyenda de escala, puntos de lectura y métricas RSSI.
  - CA5: Cambiar resolución regenera el heatmap.
  - CA6: Tras añadir un punto nuevo para ese AP, el heatmap cacheado se invalida
    y el siguiente GET devuelve un mapa actualizado.
  - CA7: Seleccionar AP individual dentro del conjunto genera un heatmap solo
    para ese BSSID sin eliminar los demás APs del conjunto.
  - CA8: Seleccionar un subconjunto temporal genera un heatmap solo con esos
    BSSID y mantiene intacto el conjunto persistente.

Desarrollador: Borys (backend) + Jhasmany (móvil)
```

### PB-06 — Analizar Cobertura Automáticamente

**Estado:** eliminada por refinamiento vigente.  
**Justificación:** no se persiste diagnóstico separado (`analisis_cobertura`/`ap_detectado`). Las métricas visuales se derivan de `mapa_calor`, `lectura_rssi` y conjuntos AP cuando la UI las necesita.

---

## 4. Sprint Backlog (F5) — Sprint 4

### HU PB-20 (8 PHU)

| Id     | Tarea                                                                                         | Resp.    | Estim. |
| ------ | --------------------------------------------------------------------------------------------- | -------- | -----: |
| Sp4-00 | Migración Alembic `0009_conjuntos_ap` (`conjunto_ap`, `conjunto_ap_item`)                     | Borys    |  2 hrs |
| Sp4-24 | Modelos + schemas + repositorio de conjuntos de APs                                           | Borys    |  3 hrs |
| Sp4-25 | Endpoints CRUD `GET/POST/PATCH/DELETE /api/planos/{id}/conjuntos-ap` y `/api/conjuntos-ap`    | Borys    |  4 hrs |
| Sp4-26 | Endpoint `POST /api/conjuntos-ap/{id}/heatmaps` con modo INDIVIDUAL/SUBCONJUNTO/COMPLETO     | Borys    |  4 hrs |
| Sp4-27 | Pantalla móvil de lista de conjuntos y formulario de creación/edición                         | Jhasmany |  5 hrs |
| Sp4-28 | Detalle móvil de conjunto con selección individual/subconjunto/todo                           | Jhasmany |  5 hrs |
| Sp4-29 | Tests backend y widget/cubit para conjuntos de APs                                            | Ambos    |  5 hrs |

### HU PB-05 (13 PHU)

| Id     | Tarea                                                                                            | Resp.    | Estim. |
| ------ | ------------------------------------------------------------------------------------------------ | -------- | -----: |
| Sp4-01 | Migración Alembic de `mapa_calor` y metadatos de generación por conjunto AP             | Borys    |  2 hrs |
| Sp4-02 | Modelos + schemas de `MapaCalor`                                                                 | Borys    |   1 hr |
| Sp4-03 | `InterpolacionService.idw()` con caching por (plano, algoritmo, resolución)                      | Borys    |  5 hrs |
| Sp4-04 | Decisión técnica: IDW como algoritmo único para evitar mapas divergentes ante el cliente          | Borys    |  4 hrs |
| Sp4-05 | `ImageService` con matplotlib (colormap personalizado por umbrales CWNA-107)                     | Borys    |  3 hrs |
| Sp4-06 | Endpoint `GET /api/planos/{id}/heatmap` compatible + generación desde `POST /conjuntos-ap/{id}/heatmaps` | Borys    |  3 hrs |
| Sp4-07 | Invalidación de caché al INSERT/DELETE en `punto_medicion`                                       | Borys    |  2 hrs |
| Sp4-08 | Tests pytest: dataset sintético, validación de matriz, validación visual del PNG                 | Borys    |  4 hrs |
| Sp4-09 | Benchmark p95 con `pytest-benchmark` (200 puntos)                                                | Borys    |  2 hrs |
| Sp4-10 | Pantalla `HeatmapPage` Flutter: superposición de imagen sobre plano                              | Jhasmany |  4 hrs |
| Sp4-11 | Selector de resolución; refetch al cambiar                                                       | Jhasmany |  2 hrs |
| Sp4-12 | Leyenda de escala de color visible en pantalla                                                   | Jhasmany |   1 hr |
| Sp4-13 | Aceptación con PO                                                                                | Ambos    |   1 hr |

### HU PB-06 (0 PHU) — Eliminada

| Id     | Tarea                                      | Resp. | Estim. |
| ------ | ------------------------------------------ | ----- | -----: |
| Sp4-14 | Documentar eliminación de diagnóstico persistido | Ambos |   1 hr |

### Resumen Sprint 4

| Concepto          |   Valor |
| ----------------- | ------: |
| Total de tareas   |      22 |
| Horas estimadas   |  ~83 hrs |
| Horas disponibles | ~80 hrs |
| Buffer            |  ~-3 hrs |
| PHU comprometidos |      21 |

> **Nota de replanificación PO (19-jun-2026):** PB-20 se incorpora a Sprint 4 como ajuste de alcance porque la generación de heatmaps requiere propósito trazable por conjunto de APs. La capacidad queda ajustada al eliminar PB-06 como diagnóstico persistido.

---

## 5. DoD específica del Sprint 4

- [x] Migración `e6f7a8b9c0d1_sp4_heatmap_y_analisis` aplicada y reversible
- [x] Migración de conjuntos de APs aplicada y reversible
- [x] Prueba automatizada de p95 local ≤ 3 s para heatmap con 200 puntos (`tests/test_heatmaps.py`)
- [x] El técnico crea un conjunto de APs con propósito y genera heatmap de AP individual, subconjunto o conjunto completo
- [x] App muestra leyenda CWNA-107 con los 5 niveles
- [x] Tests del módulo `interpolacion` cubren dataset sintético, cache y generación de mapas
- [x] Demo implementada: técnico abre proyecto de Sprint 3 → crea conjunto AP → ve heatmap
