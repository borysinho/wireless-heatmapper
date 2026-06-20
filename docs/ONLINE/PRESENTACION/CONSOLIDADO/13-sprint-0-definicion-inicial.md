# 10.2 Sprint 0 — Definición Inicial (R-1)

**Referencia Scrum:** R-1 — Definición Inicial
**Duración:** 1 semana (5 días hábiles) · **13 abr – 17 abr 2026**
**Estado:** Implementado
**Objetivo del Sprint 0:** Dejar listo el entorno de desarrollo y operación para que el Sprint 1 pueda iniciar con un backend desplegable, base de datos inicializada, pipeline CI/CD funcionando y modelos UML aprobados.

## 10.2.1 Justificación del Sprint 0

El Sprint 0 fue **obligatorio** en este proyecto por tres razones:

- Es la primera vez que el equipo trabaja con la modalidad 100 % en línea: había que cablear la integración entre Docker Compose, Nginx, FastAPI y PostgreSQL antes de poder hablar de funcionalidad de negocio.
- Antes de hacer Sprint Planning era necesario tener un Product Backlog ordenado (F3) y un esqueleto de arquitectura validado por el PO.
- El cliente de tipos del frontend (`openapi-typescript`) depende del OpenAPI publicado por el backend, por lo que el backend "vacío pero corriendo" debía existir desde el día 1 del Sprint 1.

## 10.2.2 Tareas del Sprint 0

| Id        | Tarea                                                                               | Responsable |     Estim. | Estado       |
| --------- | ----------------------------------------------------------------------------------- | ----------- | ---------: | ------------ |
| Sp0-01    | Definir equipo Scrum, roles y formato de Daily                                      | Ambos       |     0.5 hr | Terminado |
| Sp0-02    | Confirmar objetivo del producto y del proyecto                                      | Borys (PO)  |       1 hr | Terminado |
| Sp0-03    | Refinar y aprobar el Product Backlog (F3) ajustado a modalidad online               | Borys (PO)  |      3 hrs | Terminado |
| Sp0-04    | Aprobar duración estándar de Sprint = 2 semanas                                     | Ambos       |     0.5 hr | Terminado |
| Sp0-05    | Definir Definition of Done                                                          | Ambos       |       1 hr | Terminado |
| Sp0-06    | Aprobar diagramas: Contexto, Arquitectura (paquetes + despliegue), Datos            | Ambos       |      4 hrs | Terminado |
| Sp0-07    | Crear repositorio GitHub con estructura de monorepo (`backend/`, `mobile/`, `web/`) | Jhasmany    |      2 hrs | Terminado |
| Sp0-08    | Crear `docker-compose.yml` con servicios `db`, `backend`, `web`, `nginx`            | Jhasmany    |      4 hrs | Terminado |
| Sp0-09    | Crear `Dockerfile` del backend (Python 3.12 + Uvicorn) y `pyproject.toml` mínimo    | Jhasmany    |      3 hrs | Terminado |
| Sp0-10    | Crear endpoint `GET /api/health` que retorna `{"status":"ok","db":"ok"}`            | Jhasmany    |      2 hrs | Terminado |
| Sp0-11    | Configurar Alembic con migración inicial vacía                                      | Jhasmany    |      2 hrs | Terminado |
| Sp0-12    | Inicializar proyecto Flutter `mobile/` con BLoC + Dio + go_router                   | Borys       |      2 hrs | Terminado |
| Sp0-13    | Inicializar proyecto Web `web/` (Vite + React + TS + TanStack Query + axios)        | Borys       |      2 hrs | Terminado |
| Sp0-14    | Configurar `nginx/nginx.conf` con `/api → backend:8000` y `/ → web`                 | Jhasmany    |      2 hrs | Terminado |
| Sp0-15    | Configurar GitHub Actions: lint + tests + build de imagen Docker                    | Jhasmany    |      4 hrs | Terminado |
| Sp0-16    | Configurar pre-commit (ruff + ruff-format, prettier, eslint)                        | Borys       |       1 hr | Terminado |
| Sp0-17    | Documentar guía de ejecución local en README de cada componente                     | Ambos       |      2 hrs | Terminado |
| **TOTAL** |                                                                                     |             | **36 hrs** |              |

## 10.2.3 Diagrama de actividades del Sprint 0

```plantuml
@startuml
title Sprint 0 — Actividades de Definición Inicial (R-1)\nWireless HeatMapper (modalidad 100 % en línea)
skinparam activityBackgroundColor #EBF5FB
skinparam activityBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

start

:Definir equipo Scrum y roles;
note right: SM: Jhasmany · PO: Borys

:Confirmar objetivo del producto y del proyecto;

:Refinar y aprobar Product Backlog (F3) — modalidad online;
note right: Eliminar PB-14, reubicar PB-13 al Sprint 1

:Aprobar Definition of Done;

fork
  :Modelo de Contexto\n(UC01–UC19);
fork again
  :Modelo de Arquitectura\n(paquetes + despliegue);
fork again
  :Modelo de Datos\n(clases + lógico + Alembic plan);
end fork

:Configurar repositorio GitHub (monorepo);

fork
  :Backend FastAPI mínimo\n+ /api/health\n+ Alembic;
fork again
  :App móvil Flutter inicializada\n(BLoC + Dio + go_router);
fork again
  :Web React + Vite + TS\n+ TanStack Query;
fork again
  :Nginx + Docker Compose\n(db + backend + web + nginx);
end fork

:Pipeline CI/CD GitHub Actions\n(lint + tests + build + push imagen);

:Pre-commit hooks\n(ruff/ruff-format/prettier/eslint);

:Documentar guía de ejecución local\nen README de cada componente;

:Sprint 0 completado;
note right: El equipo está listo para R-2 del Sprint 1

stop
@enduml
```

> _Figura 10: Diagrama de actividades del Sprint 0 — Definición Inicial._

## 10.2.4 Modelos UML aprobados en el Sprint 0

### 10.2.4.1 Modelo de Contexto (Casos de Uso)

```plantuml
@startuml
title Modelo de Contexto — Wireless HeatMapper (modalidad 100 % en línea)\nDiagrama de Casos de Uso (UML 2.5)
left to right direction
skinparam packageStyle rectangle
skinparam actorBackgroundColor #EBF5FB
skinparam actorBorderColor #2980B9
skinparam usecaseBackgroundColor #FDFEFE
skinparam usecaseBorderColor #2980B9
skinparam rectangleBackgroundColor #FAFAFA
skinparam rectangleBorderColor #BDC3C7
skinparam arrowColor #5D6D7E
skinparam noteBackgroundColor #FFFDE7

actor "Técnico\nde Campo" as tech #LightBlue
actor "Administrador\n(Bulldog Tech.)" as admin #LightSteelBlue
actor "Cliente /\nStakeholder" as client #LightCoral
actor "Android\nWifiManager API" as wifi #LightGreen
actor "Servicio IA\n(backend)" as ia #LightYellow

rectangle "Wireless HeatMapper (Backend FastAPI + App móvil + Web)" {
  ' ── Sprint 1 — IMPLEMENTADO ──────────────────────────────────────────────
  usecase "UC11\nAutenticar\nUsuario" as UC11
  usecase "UC13\nGestionar Usuarios\n(Admin Web)" as UC13
  usecase "UC19\nGestionar Clientes\n(Admin Web)" as UC19
  usecase "UC18\nVer Proyectos de\nla Organización" as UC18
  usecase "UC01\nGestionar Proyecto\nde Survey" as UC01
  usecase "UC12\nVer Historial\nde Proyectos" as UC12

  ' ── Sprint 2 — Pendiente ──────────────────────────────────────────────────
  usecase "UC02\nImportar Plano\n(subida al backend)" as UC02
  usecase "UC03\nCalibrar Escala\ndel Plano" as UC03

  ' ── Sprint 3 — Pendiente ──────────────────────────────────────────────────
  usecase "UC04\nMarcar Punto\nde Medición" as UC04
  usecase "UC05\nCapturar Señales WiFi\n(envío en línea)" as UC05

  ' ── Sprint 4 — Pendiente ──────────────────────────────────────────────────
  usecase "UC06\nGenerar Mapa de Calor\n(interpolación en backend)" as UC06
  usecase "UC07\nAnalizar Cobertura\n(zonas muertas, CCI/ACI)" as UC07

  ' ── Sprint 5 — Pendiente ──────────────────────────────────────────────────
  usecase "UC08\nObtener Recomendaciones\nde APs (IA)" as UC08
  usecase "UC09\nComparar Escenario\nActual vs Propuesto" as UC09
  usecase "UC10\nExportar Reporte\nTécnico (PDF)" as UC10

  ' ── Sprint 6 — Pendiente ──────────────────────────────────────────────────
  usecase "UC15\nGenerar Enlace\nde Cliente" as UC15
  usecase "UC16\nVer Heatmap\nInteractivo (Web)" as UC16
  usecase "UC17\nVer Análisis y\nPlan AP (Web)" as UC17
}

tech --> UC11
tech --> UC01
tech --> UC02
tech --> UC03
tech --> UC04
tech --> UC06
tech --> UC07
tech --> UC08
tech --> UC09
tech --> UC10
tech --> UC12
tech --> UC15

admin --> UC11
admin --> UC13
admin --> UC18
admin --> UC19

client --> UC16
client --> UC17

UC01 ..> UC19 : <<include>>
UC04 ..> UC05 : <<include>>
UC05 -- wifi
UC08 -- ia
UC09 ..> UC08 : <<extend>>
UC15 ..> UC16 : <<include>>

note bottom of UC13
  Sprint 1 — implementado
end note

note bottom of UC19
  Sprint 1 — implementado
end note
@enduml
```

> _Figura 11: Modelo de Contexto del sistema (Diagrama de Casos de Uso UML 2.5) — UC01 a UC19, con desglose por Sprint._

### 10.2.4.2 Modelo de Arquitectura — Diagrama de Paquetes

```plantuml
@startuml
title Modelo de Arquitectura — Diagrama de Paquetes (UML 2.5)\nWireless HeatMapper (modalidad 100 % en línea)
skinparam packageStyle rectangle
skinparam packageBackgroundColor #EBF5FB
skinparam packageBorderColor #2980B9
skinparam componentBackgroundColor #FDFEFE
skinparam componentBorderColor #5D6D7E
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

package "App Móvil — Flutter / Dart" as MOBILE {
  package "presentation" as MOB_PRES {
    [LoginPage]
    [ProyectosPage]
    [ProyectoFormPage]
    [BLoC / Cubit]
  }
  package "domain" as MOB_DOM {
    [UseCase: Login]
    [UseCase: ListarProyectos]
    [UseCase: GestionarProyecto]
  }
  package "data" as MOB_DATA {
    [ApiClient (Dio)]
    [AuthInterceptor (JWT)]
    [SecureStorage (token)]
    [ConnectivityMonitor]
  }
  note bottom of MOB_DATA
    NO HAY persistencia de dominio.
    Solo SecureStorage para JWT.
  end note
}

package "Plataforma Web — React + TypeScript + Vite" as WEB {
  package "panel-admin" as WEB_ADMIN {
    [LoginAdmin]
    [AdminLayout]
    [GestionUsuarios]
    [GestionClientes]
    [ListadoProyectosOrg]
  }
  package "shared" as WEB_SHARED {
    [ApiClient (axios + TanStack Query)]
    [Router (React Router)]
  }
  package "types" as WEB_TYPES {
    [Tipos TypeScript del dominio\n(features/*/types — manual)]
  }
}

package "Backend — FastAPI / Python" as BACKEND {
  package "api" as B_API {
    [auth_router (/api/auth)]
    [admin_usuarios_router (/api/admin/usuarios)]
    [clientes_router (/api/clientes)]
    [proyectos_router (/api/proyectos)]
    [admin_proyectos_router (/api/admin/proyectos)]
  }
  package "services" as B_SVC {
    [AuthService (JWT + bcrypt)]
    [UsuarioService]
  }
  package "repositories" as B_REPO {
    [UsuarioRepository]
    [RefreshTokenRepository]
    [ClienteRepository]
    [ProyectoRepository]
  }
  package "models" as B_MOD {
    [SQLAlchemy ORM models]
    [Pydantic schemas]
    [Alembic migrations]
  }
}

database "PostgreSQL 15" as DB
node "Nginx (reverse proxy + TLS)" as NGINX

MOB_PRES --> MOB_DOM
MOB_DOM --> MOB_DATA
MOB_DATA -down-> NGINX : HTTPS REST
WEB_ADMIN --> WEB_SHARED
WEB_SHARED -down-> NGINX : HTTPS REST
NGINX -down-> B_API : /api/* (proxy_pass)
B_API --> B_SVC
B_SVC --> B_REPO
B_REPO --> B_MOD
B_MOD -down-> DB

note right of NGINX
  · /api/* → backend:8000
  · /admin/* → web (SPA)
  · / → portal de cliente
end note
@enduml
```

> _Figura 12: Modelo de Arquitectura — Diagrama de Paquetes en cuatro capas._

### 10.2.4.3 Modelo de Arquitectura — Diagrama de Despliegue

```plantuml
@startuml
title Modelo de Arquitectura — Diagrama de Despliegue (UML 2.5)\nWireless HeatMapper (modalidad 100 % en línea)
skinparam nodeBackgroundColor #EBF5FB
skinparam nodeBorderColor #2980B9
skinparam artifactBackgroundColor #FDFEFE
skinparam artifactBorderColor #5D6D7E
skinparam componentBackgroundColor #FDFEFE
skinparam componentBorderColor #5D6D7E
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

node "Servidor de Producción\n(Linux / VPS o Docker Host)" as HOST {

  node "Contenedor: nginx\n(reverse proxy, puerto 80/443)" as CTR_NGINX {
    artifact "nginx.conf\n(SPA + proxy /api/*)" as CONF_NGINX
  }

  node "Contenedor: web\n(Nginx + bundle React, puerto 80 interno)" as CTR_WEB {
    artifact "dist/ — bundle React\n(admin panel + portal cliente)\nservido por nginx:1.27-alpine" as ART_WEB
  }

  node "Contenedor: backend\n(FastAPI + Uvicorn, puerto 8000 interno)" as CTR_BACKEND {
    artifact "app/ — FastAPI\n(routers, services, repositories)" as ART_BACKEND
    artifact "alembic/versions/\n(migraciones PostgreSQL)" as ART_MIGR
  }

  node "Contenedor: db\n(PostgreSQL 15, puerto 5432 interno)" as CTR_DB {
    artifact "heatmapper_db\n(esquema: usuarios, clientes,\nproyectos, refresh_tokens)" as ART_DB
  }
}

node "Dispositivo Móvil Android\n(Flutter APK, Android 8+)" as MOBILE {
  artifact "heatmapper.apk\n(Flutter Release Build)" as ART_APK
}

node "Navegador Web\n(Chrome / Firefox)" as BROWSER {
  artifact "React SPA\n(cargada desde nginx)" as ART_SPA
}

node "Servicio CI/CD\n(GitHub Actions)" as CI {
  artifact "workflow: ci.yml\n(pytest, build, docker push)" as ART_CI
}

MOBILE -down-> CTR_NGINX : HTTPS :443\n(REST /api/*)
BROWSER -down-> CTR_NGINX : HTTPS :443\n(HTTP GET /*\n+ REST /api/*)
CTR_NGINX -right-> CTR_WEB : proxy_pass :80\n(/admin/*, /)
CTR_NGINX -down-> CTR_BACKEND : proxy_pass :8000\n(/api/*)
CTR_BACKEND -down-> CTR_DB : TCP :5432\n(SQLAlchemy ORM)
CI -right-> HOST : docker compose up\n(deploy automático)

note bottom of CTR_DB
  Datos persistidos en volumen Docker.
  Única fuente de verdad (sin BD local en móvil).
end note

note bottom of MOBILE
  flutter_secure_storage: solo almacena JWT.
  No hay persistencia de dominio local (modalidad 100 % en línea).
end note
@enduml
```

> _Figura 13: Modelo de Arquitectura — Diagrama de Despliegue de los contenedores Docker._

### 10.2.4.4 Modelo de Datos (vista conceptual de Sprint 1)

El diagrama de Clases de la base de datos correspondiente al estado al cierre del Sprint 0/Sprint 1 se presenta en el bloque de Diseño de Datos del Sprint 1 (sección 10.3.4). Las entidades incluidas en la versión inicial del esquema son **Usuario**, **RefreshToken**, **Cliente** y **Proyecto**, con sus respectivas tablas, restricciones y claves foráneas.

## 10.2.5 Definition of Ready para el Sprint 1 (verificada al cierre del Sprint 0)

| Criterio                                                        | Estado |
| --------------------------------------------------------------- | ------ |
| Repositorio GitHub creado y accesible para ambos miembros       | Sí |
| `docker compose up` levanta los 4 servicios sin errores         | Sí |
| `curl http://localhost/api/health` → `200 OK`                   | Sí |
| Migración inicial Alembic aplicada en `db`                      | Sí |
| Pipeline CI verde en `main`                                     | Sí |
| Modelos UML (contexto, arquitectura, datos) aprobados por el PO | Sí |
| Product Backlog (F3) aprobado y ordenado por el PO              | Sí |
