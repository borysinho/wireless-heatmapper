# Sprint 3 — Modelos Generados

## S3.2 Modelos del Sprint 3

### Modelo de contexto — Captura y marcado de puntos

```plantuml
@startuml Sprint3_CasosUso
title Sprint 3 — Casos de uso de captura WiFi en línea
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
  usecase "PB-03\nCapturar señales WiFi" as UC03
  usecase "PB-04\nMarcar puntos de medición" as UC04
  usecase "PB-11\nPlano calibrado" as UC11
}

Tecnico --> UC03
Tecnico --> UC04
UC03 ..> UC11 : <<requires>>
UC04 ..> UC03 : <<include>>
@enduml
```

_Figura 20. Casos de uso del Sprint 3 para captura en línea y marcado de puntos._

### Diagrama de secuencia — Captura WiFi en línea

```plantuml
@startuml Sprint3_Secuencia_Captura
title Sprint 3 — Captura WiFi y persistencia en línea
skinparam backgroundColor #FAFAFA
skinparam participantBackgroundColor #EBF5FB
skinparam participantBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

actor Tecnico
participant "CapturaPage" as App
participant "WifiScanner" as Scanner
participant "CapturaCubit" as Cubit
participant "Backend /mediciones" as Backend
database PostgreSQL as DB

Tecnico -> App : tocar punto en plano
App -> Scanner : iniciar escaneo
Scanner --> App : resultados WiFi
App -> Cubit : enviar lote
Cubit -> Backend : POST /api/mediciones
Backend -> DB : insertar punto y mediciones
DB --> Backend : ids y nivel
Backend --> Cubit : 201 Created
Cubit --> App : actualizar plano
App --> Tecnico : mostrar badge por nivel
@enduml
```

_Figura 21. Secuencia de captura y envío de mediciones WiFi hacia el backend._

### Diagrama de estados — Sesión de captura

```plantuml
@startuml Sprint3_Estados
title Sprint 3 — Estados del CapturaCubit
skinparam backgroundColor #FAFAFA
skinparam stateBackgroundColor #EBF5FB
skinparam stateBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

[*] --> Inactiva
Inactiva --> Loading : iniciarSesion
Loading --> Activa : puntos cargados
Activa --> Enviando : marcarPunto
Enviando --> Activa : lote persistido
Activa --> Throttling : limite alcanzado
Throttling --> Activa : tiempo liberado
Activa --> Pausada : sin conectividad
Pausada --> Activa : reanudar
Activa --> PuntoDetalle : abrirDetallePunto
PuntoDetalle --> Activa : cerrarDetalle
Enviando --> Error : fallo de envio
Error --> Activa : reintentar
Activa --> Inactiva : detenerSesion
@enduml
```

_Figura 22. Estados operativos del `CapturaCubit` durante una sesión de medición._

**Tabla 20.** Diseño físico de datos de `punto_medicion` y `medicion_wifi`

| Tabla | Columna | Tipo de dato | Descripción |
| ----- | ------- | ------------ | ----------- |
| `punto_medicion` | `id` | INTEGER | Identificador del punto |
| `punto_medicion` | `plano_id` | INTEGER | Referencia al plano calibrado |
| `punto_medicion` | `x_px` | DECIMAL(10,2) | Coordenada X del punto sobre el plano |
| `punto_medicion` | `y_px` | DECIMAL(10,2) | Coordenada Y del punto sobre el plano |
| `punto_medicion` | `nivel` | VARCHAR(20) | Nivel agregado del punto según peor RSSI |
| `punto_medicion` | `creado_en` | TIMESTAMP WITH TIME ZONE | Fecha de creación del punto |
| `medicion_wifi` | `id` | INTEGER | Identificador de la medición |
| `medicion_wifi` | `punto_id` | INTEGER | Referencia al punto de medición |
| `medicion_wifi` | `ssid` | VARCHAR(255) | Nombre de la red detectada |
| `medicion_wifi` | `bssid` | VARCHAR(17) | Dirección MAC del AP detectado |
| `medicion_wifi` | `rssi` | INTEGER | Intensidad de señal en dBm |
| `medicion_wifi` | `frecuencia` | INTEGER | Frecuencia de operación en MHz |
| `medicion_wifi` | `canal` | INTEGER | Canal observado |
| `medicion_wifi` | `numero_lectura` | INTEGER | Ciclo de escaneo dentro del mismo punto |
| `medicion_wifi` | `creado_en` | TIMESTAMP WITH TIME ZONE | Fecha de registro de la lectura |

**Tabla 21.** Clasificación CWNA-107 aplicada en backend

| Rango dBm | Nivel documentado | Uso interpretativo |
| --------- | ----------------- | ------------------ |
| `>= -70` | EXCELENTE | Cobertura objetivo |
| `-71 a -80` | BUENA | Cobertura funcional |
| `-81 a -85` | ACEPTABLE | Cobertura degradada |
| `-86 a -90` | DEBIL | Riesgo de pérdida de calidad |
| `< -90` | ZONA_MUERTA | Sin cobertura útil |

---
