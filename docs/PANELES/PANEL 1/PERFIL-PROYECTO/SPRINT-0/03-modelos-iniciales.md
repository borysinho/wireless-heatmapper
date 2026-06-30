# Sprint 0 — Modelos Iniciales del Sistema

## S0.3 Modelos Iniciales

Como resultado de la ingeniería de requisitos del Sprint 0 se generaron los tres modelos iniciales que sirven como base para todos los sprints posteriores.

---

## S0.3.1 Modelo de Contexto — Diagrama de Casos de Uso

```plantuml
@startuml Modelo_Contexto_Sprint0
skinparam actorBackgroundColor #EBF5FB
skinparam usecaseBackgroundColor #EBF5FB
skinparam usecaseBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Modelo de Contexto — Wireless HeatMapper (Sprint 0)

left to right direction

actor Administrador as ADMIN
actor "Técnico\n(App Móvil)" as TEC
actor Cliente as CLI
actor "Sistema IA\n(Backend)" as IA <<system>>

rectangle "Wireless HeatMapper" {
  usecase "UC01 Gestionar usuarios" as UC01
  usecase "UC02 Autenticarse" as UC02
  usecase "UC09 Gestionar clientes" as UC09
  usecase "UC13 Gestionar proyectos" as UC13
  usecase "UC18 Ver listado de proyectos" as UC18
  usecase "UC19 Autenticarse en app móvil" as UC19
  usecase "UC03 Seleccionar proyecto" as UC03
  usecase "UC04 Realizar levantamiento Wi-Fi" as UC04
  usecase "UC05 Generar mapa de calor" as UC05
  usecase "UC06 Analizar cobertura con IA" as UC06
  usecase "UC07 Ver heatmap en panel web" as UC07
  usecase "UC08 Exportar reportes" as UC08
  usecase "UC10 Ver proyectos propios" as UC10
}

ADMIN --> UC01
ADMIN --> UC02
ADMIN --> UC09
ADMIN --> UC13
ADMIN --> UC18
ADMIN --> UC07
ADMIN --> UC08
TEC --> UC19
TEC --> UC03
TEC --> UC04
UC04 --> UC05 : <<include>>
UC05 --> UC06 : <<include>>
CLI --> UC10
CLI --> UC02
UC06 --> IA : <<extend>>
@enduml
```

_Figura 6. Modelo de contexto — Diagrama de casos de uso del sistema Wireless HeatMapper._

---

### Diagrama de Paquetes

```plantuml
@startuml Arquitectura_Paquetes_Sprint0
skinparam packageBackgroundColor #EBF5FB
skinparam packageBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Diagrama de Paquetes — Wireless HeatMapper

package "App Móvil\n(Flutter/Dart)" as MOBILE {
  package "presentation" {
    [screens]
    [widgets]
    [blocs]
  }
  package "domain" {
    [entities]
    [use_cases]
    [repositories]
  }
  package "data" {
    [datasources]
    [models]
    [repositories_impl]
  }
}

package "Backend\n(FastAPI/Python)" as BACKEND {
  package "api" {
    [routers]
    [schemas]
    [dependencies]
  }
  package "domain" {
    [models]
    [services]
  }
  package "infrastructure" {
    [database]
    [repositories]
    [ia_module]
  }
}

package "Web Admin\n(React/TypeScript)" as WEB {
  package "pages" {
    [admin]
    [auth]
    [client]
  }
  package "components" {
    [shared]
    [heatmap]
  }
  package "services" {
    [api_client]
    [state]
  }
}

package "Base de Datos\n(PostgreSQL 15)" as DB {
  [tablas]
  [migraciones]
}

MOBILE --> BACKEND : REST/HTTPS (Dio)
WEB --> BACKEND : REST/HTTPS (Axios)
BACKEND --> DB : SQLAlchemy/ORM
@enduml
```

_Figura 7. Diagrama de paquetes — Arquitectura por capas del sistema Wireless HeatMapper._

### Diagrama de Despliegue

```plantuml
@startuml Despliegue_Sprint0
skinparam nodeBackgroundColor #EBF5FB
skinparam nodeBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Diagrama de Despliegue — Wireless HeatMapper

node "Dispositivo Android\n(Técnico)" as ANDROID {
  artifact "App Flutter\n(APK)" as APK
}

node "Servidor de Producción\n(VPS / Docker)" as SERVER {
  node "Contenedor: Nginx\n(Reverse Proxy)" as NGINX
  node "Contenedor: FastAPI\n(Backend REST + IA)" as API
  node "Contenedor: React App\n(Panel Web)" as WEBAPP
  node "Contenedor: PostgreSQL\n(Base de Datos)" as DB

  NGINX --> API : /api/*
  NGINX --> WEBAPP : /*
  API --> DB : TCP 5432
}

ANDROID --> NGINX : HTTPS / REST

note right of SERVER
  Orquestación: Docker Compose
  CI/CD: GitHub Actions
end note
@enduml
```

_Figura 8. Diagrama de despliegue — Infraestructura Docker del sistema Wireless HeatMapper._

---

## S0.3.3 Modelo de Datos Inicial — Conceptual

```plantuml
@startuml Modelo_Datos_Conceptual_Sprint0
skinparam classBackgroundColor #EBF5FB
skinparam classBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Modelo Conceptual de Datos — Wireless HeatMapper

class Usuario {
  nombre
  apellido
  correo
  contrasena
  rol
  activo
}

class Organizacion {
  nombre
  direccion
  contacto
  activo
}

class Proyecto {
  nombre
  descripcion
  estado
  fechaInicio
  fechaFin
}

class Instalacion {
  nombre
  descripcion
}

class PlanoDePlanta {
  archivo
  escala
  anchoMetros
  altoMetros
}

class Medicion {
  rssi_dBm
  ssid
  bssid
  frecuencia_GHz
  canal
  coordenadaX
  coordenadaY
  fechaHora
}

class MapaDeCalor {
  imagenGenerada
  algoritmo
  fechaGeneracion
}

class ReporteIA {
  recomendaciones
  puntajeCobertura
  fechaEmision
}

Usuario "1" -- "0..*" Proyecto : gestiona
Organizacion "1" -- "1..*" Proyecto : solicita
Proyecto "1" -- "1..*" Instalacion : abarca
Instalacion "1" -- "1" PlanoDePlanta : tiene
Proyecto "1" -- "0..*" Medicion : contiene
Medicion "0..*" -- "1" MapaDeCalor : origina
MapaDeCalor "1" -- "0..1" ReporteIA : genera
@enduml
```

_Figura 9. Modelo conceptual de datos — Entidades principales del dominio de Wireless HeatMapper._

---
