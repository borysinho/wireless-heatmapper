# 03 — Modelo de Arquitectura (modalidad online)

**Notación:** UML 2.5 — Diagramas de Paquetes y de Despliegue
**Referencia:** PAPS Online §6, §11 · `docker-infra.instructions.md`

---

## 1. Visión general

La arquitectura del Wireless HeatMapper en modalidad 100 % en línea se compone de **tres aplicaciones cliente** y **un backend único** que actúa como fuente de verdad:

- **App móvil Android** (Flutter / Dart) — cliente delgado para el técnico de campo.
- **Plataforma web** (React + TypeScript) — panel de administración + portal de cliente.
- **Backend FastAPI** — REST + IA + autenticación + base de datos PostgreSQL.

Todo el tráfico atraviesa **Nginx** como reverse proxy con terminación TLS.

> **Convención de prefijos REST:** los routers FastAPI declaran rutas sin el prefijo `/api` (p. ej. `/auth/login`, `/admin/usuarios`, `/clientes`). Nginx anteceden el prefijo `/api` mediante `proxy_pass http://backend:8000/` (sin re-prefix), de modo que los clientes consumen `/api/auth/login`, `/api/admin/usuarios`, `/api/clientes`, etc. Los nombres mostrados en el diagrama incluyen el prefijo público para reflejar la URL final que ven los clientes.

> **Estado de implementación al cierre del Sprint 1:** están operativos los routers `auth`, `admin/usuarios`, `clientes`, `admin/proyectos` y `proyectos`; en el panel admin web están operativos `LoginAdmin`, `AdminLayout`, `GestionUsuarios`, `GestionClientes` y `ListadoProyectosOrg`. El resto de componentes del diagrama corresponde a sprints futuros.

---

## 2. Diagrama de paquetes

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
    [PlanoEditorPage]
    [CapturaPage]
    [HeatmapPage]
    [AnalisisPage]
    [RecomendacionesPage]
    [ReportePage]
    [BLoC / Cubit]
  }
  package "domain" as MOB_DOM {
    [UseCase: Login]
    [UseCase: ListarProyectos]
    [UseCase: CapturarMedicion]
    [UseCase: ObtenerHeatmap]
    [UseCase: SolicitarRecomendaciones]
  }
  package "data" as MOB_DATA {
    [ApiClient (Dio)]
    [AuthInterceptor (JWT)]
    [SecureStorage (token)]
    [WifiScanner (WifiManager)]
    [ConnectivityMonitor]
  }
  note bottom of MOB_DATA
    NO HAY persistencia de dominio.
    Solo SecureStorage para JWT y
    preferencias UI no críticas.
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
  package "portal-cliente" as WEB_CLIENTE {
    [VistaHeatmapInteractivo]
    [VistaAnalisisYPlanAP]
  }
  package "shared" as WEB_SHARED {
    [ApiClient (axios + TanStack Query)]
    [Tipos generados desde OpenAPI]
    [Router (React Router)]
  }
}

package "Backend — FastAPI / Python" as BACKEND {
  package "api" as B_API {
    [auth_router (/api/auth)]
    [admin_usuarios_router (/api/admin/usuarios)]
    [clientes_router (/api/clientes, /api/admin/clientes)]
    [proyectos_router (/api/proyectos)]
    [admin_proyectos_router (/api/admin/proyectos)]
    [planos_router (/api/planos)]
    [mediciones_router (/api/mediciones)]
    [heatmap_router (/api/heatmap)]
    [analisis_router (/api/analisis)]
    [ia_router (/api/optimize-aps)]
    [reportes_router (/api/reportes)]
    [enlaces_router (/api/share-link)]
  }
  package "services" as B_SVC {
    [AuthService (JWT + bcrypt)]
    [UsuarioService]
    [ClienteService]
    [ProyectoService]
    [PlanoService]
    [MedicionService]
    [InterpolacionService (IDW/Kriging)]
    [AnalisisCoberturaService]
    [ReporteService (WeasyPrint)]
    [TokenEnlaceService]
  }
  package "ai" as B_AI {
    [OptimizadorAPs (modelo ML)]
    [PredictorCobertura]
  }
  package "repositories" as B_REPO {
    [UsuarioRepository]
    [RefreshTokenRepository]
    [ClienteRepository]
    [ProyectoRepository]
    [PlanoRepository]
    [PuntoMedicionRepository]
    [MedicionWifiRepository]
    [MapaCalorRepository]
    [AnalisisRepository]
    [EscenarioRepository]
    [ReporteRepository]
    [TokenEnlaceRepository]
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
WEB_CLIENTE --> WEB_SHARED
WEB_SHARED -down-> NGINX : HTTPS REST
NGINX -down-> B_API : /api/* (proxy_pass)
B_API --> B_SVC
B_SVC --> B_AI
B_SVC --> B_REPO
B_REPO --> B_MOD
B_MOD -down-> DB

note right of NGINX
  · /api/* → backend:8000
  · /admin/*, /cliente/* → web (SPA)
  · / → portal de cliente (SPA)
  · TLS (Let's Encrypt en producción)
end note
@enduml
```

---

## 3. Diagrama de despliegue

```plantuml
@startuml
title Modelo de Arquitectura — Diagrama de Despliegue (UML 2.5)\nWireless HeatMapper (modalidad 100 % en línea)
skinparam nodeBackgroundColor #EBF5FB
skinparam nodeBorderColor #2980B9
skinparam artifactBackgroundColor #FDFEFE
skinparam componentBackgroundColor #FDFEFE
skinparam databaseBackgroundColor #EAF7EA
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7

node "Dispositivo Android\n(Técnico de Campo)" as android {
  artifact "Wireless HeatMapper APK" as apk {
    component "UI Flutter" as ui_mob
    component "BLoC / Cubit" as bloc
    component "ApiClient (Dio + JWT)" as api_mob
    component "WifiScanner\n(WifiManager API)" as wifi_mob
    component "ConnectivityMonitor" as conn
    component "SecureStorage\n(solo JWT)" as ss
  }
}

node "Navegador Web\n(Admin / Cliente)" as browser {
  artifact "SPA React (panel admin / portal cliente)" as spa
}

node "VPS / Cloud — Servidor de Aplicación\n(Docker Compose)" as server {
  node "Contenedor: nginx" as cnt_nginx {
    component "Nginx 1.25\n(TLS, proxy)" as nginx
  }
  node "Contenedor: backend" as cnt_back {
    artifact "FastAPI app" as fastapi {
      component "Routers REST" as routers
      component "Services" as svcs
      component "AI Module\n(scikit-learn)" as ai
      component "Repositories\n(SQLAlchemy)" as repos
      component "Alembic" as alembic
    }
  }
  node "Contenedor: web" as cnt_web {
    artifact "Bundle React (estático)" as react_bundle
  }
  node "Contenedor: db" as cnt_db {
    database "PostgreSQL 15\n(volumen persistente)" as pg
  }
}

node "GitHub" as gh {
  artifact "Repositorio" as repo
  artifact "GitHub Actions\n(CI/CD)" as ci
}

android -down-> nginx : HTTPS\n(WiFi / 4G/5G)
browser -down-> nginx : HTTPS

nginx -down-> fastapi : /api/* → backend:8000
nginx -down-> react_bundle : / → bundle estático

fastapi -down-> pg : SQLAlchemy / asyncpg
ai -down-> pg : (lectura/cache de modelos)

ci ..> server : deploy (docker compose pull + up)
ci ..> gh : artefactos / imágenes
repo ..> ci : trigger en push/main

note right of android
  Restricciones (PAPS Online §10):
  · Sin SQLite local
  · Throttling Android ≥ 8.0:
    máx. 4 escaneos / 2 min
  · Pausa de captura ante caída de red
end note

note right of server
  Servicios:
  · nginx — :80 / :443
  · backend — :8000 (interno)
  · web — :80 (servido vía nginx)
  · db — :5432 (interno, no expuesto)

  Healthchecks:
  · backend GET /api/health
  · db pg_isready
  · web GET /
end note
@enduml
```

---

## 4. Estilo arquitectónico del backend (capas)

```
┌─────────────────────────────────────────────┐
│  api/        Routers FastAPI + dependencies │ ← entrada HTTP
├─────────────────────────────────────────────┤
│  services/   Lógica de negocio              │ ← orquestación
├─────────────────────────────────────────────┤
│  ai/         Modelos ML (sklearn / ONNX)    │ ← inferencia
├─────────────────────────────────────────────┤
│  repositories/  Acceso a BD (SQLAlchemy)    │ ← persistencia
├─────────────────────────────────────────────┤
│  models/     ORM + schemas Pydantic         │ ← contratos
└─────────────────────────────────────────────┘
                       ↓
                  PostgreSQL 15
```

Reglas:

- Las dependencias siempre apuntan **hacia abajo**.
- Los routers no acceden directamente a `repositories`; pasan por `services`.
- Los `services` reciben sesión SQLAlchemy por inyección (`Depends(get_db)`).
- Los modelos Pydantic (`schemas/`) son el contrato público; los ORM (`models/`) son internos.

---

## 5. Comunicación cliente-servidor

| Cliente            | Endpoint base               | Autenticación        | Formato                   |
| ------------------ | --------------------------- | -------------------- | ------------------------- |
| App móvil          | `https://<host>/api/`       | Bearer JWT (técnico) | JSON + multipart (planos) |
| Panel admin web    | `https://<host>/api/admin/` | Bearer JWT (admin)   | JSON                      |
| Portal cliente web | `https://<host>/api/share/` | Token de enlace UUID | JSON (lectura solamente)  |

Todos los clientes generan sus tipos a partir del **OpenAPI** publicado en `/api/openapi.json`:

- App móvil: `openapi-generator` → cliente Dart tipado
- Web: `openapi-typescript` → tipos TS + hooks de TanStack Query

---

## 6. Despliegue mediante Docker Compose

Servicios definidos en `docker-compose.yml` (referencia, no se implementan en este plan):

| Servicio  | Imagen base                      | Puerto interno | Volumen / Dependencia                      |
| --------- | -------------------------------- | -------------- | ------------------------------------------ |
| `db`      | `postgres:15-alpine`             | 5432           | `pgdata:/var/lib/postgresql/data`          |
| `backend` | `python:3.12-slim` + Uvicorn     | 8000           | depende de `db`; healthcheck `/api/health` |
| `web`     | `node:20` (build) → `nginx:1.25` | 80             | bundle estático servido por nginx          |
| `nginx`   | `nginx:1.25`                     | 80, 443        | depende de `backend` y `web`               |
