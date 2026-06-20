# Sprint 2 — Modelos Generados

## S2.2 Modelos del Sprint 2

### Modelo de contexto — Planos y calibración

```plantuml
@startuml Sprint2_CasosUso
title Sprint 2 — Casos de uso de importación y calibración de planos
skinparam backgroundColor #FAFAFA
skinparam actorBackgroundColor #EBF5FB
skinparam actorBorderColor #2980B9
skinparam usecaseBackgroundColor #EBF5FB
skinparam usecaseBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7
left to right direction

actor "Técnico" as Tecnico

rectangle "Wireless HeatMapper" {
  usecase "PB-02\nImportar plano" as UC02
  usecase "PB-11\nCalibrar escala" as UC11
  usecase "PB-01\nGestionar proyecto" as UC01
}

Tecnico --> UC02
Tecnico --> UC11
Tecnico --> UC01
UC11 ..> UC02 : <<requires>>
note right of UC11
  La calibración define
  metros por píxel
  antes de la captura.
end note
@enduml
```

_Figura 16. Casos de uso del Sprint 2 centrados en importación y calibración de planos._

### Diagrama de clases conceptual

```plantuml
@startuml Sprint2_Clases
title Sprint 2 — Modelo conceptual de Proyecto y Plano
skinparam backgroundColor #FAFAFA
skinparam classBackgroundColor #EBF5FB
skinparam classBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

class Proyecto {
  id : entero
  nombre : texto
  cliente : texto
  estado : texto
}

class Plano {
  id : entero
  nombre_archivo : texto
  formato : texto
  ancho_px : entero
  alto_px : entero
  escala_m_por_px : decimal
}

Proyecto "1" -- "0..*" Plano : contiene >

note right of Plano
  Un plano puede existir sin calibración.
  La escala se define luego de importar
  y validar una distancia real.
end note
@enduml
```

_Figura 17. Modelo conceptual del Sprint 2 con la entidad Plano asociada al proyecto._

### Diagrama de secuencia — Subida de plano

```plantuml
@startuml Sprint2_Secuencia_Subida
title Sprint 2 — Flujo de subida de plano
skinparam backgroundColor #FAFAFA
skinparam participantBackgroundColor #EBF5FB
skinparam participantBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

actor Tecnico
participant "PlanoEditorPage" as App
participant "ApiClient" as Api
participant "Backend /proyectos/{id}/planos" as Backend
participant "StorageService" as Storage
database PostgreSQL as DB

Tecnico -> App : seleccionar archivo
App -> Api : POST multipart/form-data
Api -> Backend : solicitud autenticada
Backend -> Storage : guardar archivo renderizado
Backend -> DB : insertar metadatos del plano
DB --> Backend : id y dimensiones
Backend --> App : 201 + URL firmada
App --> Tecnico : renderizar plano
@enduml
```

_Figura 18. Secuencia de importación de plano desde la app móvil hacia el backend._

### Diagrama de secuencia — Calibración de escala

```plantuml
@startuml Sprint2_Secuencia_Calibracion
title Sprint 2 — Flujo de calibración del plano
skinparam backgroundColor #FAFAFA
skinparam participantBackgroundColor #EBF5FB
skinparam participantBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

actor Tecnico
participant "PlanoEditorPage" as App
participant "PlanosCubit" as Cubit
participant "Backend /planos/{id}/calibracion" as Backend
database PostgreSQL as DB

Tecnico -> App : tocar dos puntos
App -> Tecnico : solicitar distancia real
Tecnico -> App : ingresar metros
App -> Cubit : confirmar calibración
Cubit -> Backend : PATCH calibracion
Backend -> DB : actualizar escala y puntos referencia
DB --> Backend : calibración persistida
Backend --> Cubit : plano calibrado
Cubit --> App : estado exitoso
App --> Tecnico : mostrar factor y regla
@enduml
```

_Figura 19. Secuencia de calibración del plano a partir de una distancia conocida._

**Tabla 15.** Diseño físico de datos de la tabla `planos`

| Columna | Tipo de dato | Descripción |
| ------- | ------------ | ----------- |
| `id` | INTEGER | Identificador del plano |
| `proyecto_id` | INTEGER | Referencia al proyecto propietario |
| `nombre_archivo` | VARCHAR(255) | Nombre original del archivo importado |
| `formato` | VARCHAR(10) | Formato admitido: PNG, JPG o PDF |
| `ruta_storage` | VARCHAR(500) | Ubicación lógica del archivo en storage |
| `ancho_px` | INTEGER | Ancho del plano en píxeles |
| `alto_px` | INTEGER | Alto del plano en píxeles |
| `escala_m_por_px` | DECIMAL(10,6) | Factor de conversión de metros por píxel |
| `x1_cal` | DECIMAL(10,2) | Coordenada X del primer punto de calibración |
| `y1_cal` | DECIMAL(10,2) | Coordenada Y del primer punto de calibración |
| `x2_cal` | DECIMAL(10,2) | Coordenada X del segundo punto de calibración |
| `y2_cal` | DECIMAL(10,2) | Coordenada Y del segundo punto de calibración |
| `distancia_real_m` | DECIMAL(10,2) | Distancia física declarada por el técnico |
| `creado_en` | TIMESTAMP WITH TIME ZONE | Fecha y hora de creación del registro |

---
