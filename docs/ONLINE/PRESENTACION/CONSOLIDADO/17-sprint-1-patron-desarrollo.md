# 10.6 Patrón de desarrollo del Sprint 1

Esta sección documenta los modelos de diseño técnicos producidos durante la ejecución del Sprint 1 (R-3): la **arquitectura física** desplegada en contenedores, la **arquitectura lógica** organizada en cuatro capas y el **diseño de datos** en sus tres niveles (conceptual, lógico y físico).

## 10.6.1 Arquitectura Física — Diagrama de Despliegue

```plantuml
@startuml
title Arquitectura Física — Diagrama de Despliegue (UML 2.5)\nWireless HeatMapper (modalidad 100 % en línea)
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

> _Figura 15: Arquitectura física — Diagrama de Despliegue de los contenedores Docker en producción._

## 10.6.2 Arquitectura Lógica — Diagrama de Paquetes

```plantuml
@startuml
title Arquitectura Lógica — Diagrama de Paquetes (UML 2.5)\nWireless HeatMapper (modalidad 100 % en línea)
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

> _Figura 16: Arquitectura lógica — Diagrama de Paquetes en cuatro capas._

## 10.6.3 Diseño de Datos

### 10.6.3.1 Diagrama de Clases Conceptual (Sprint 1)

```plantuml
@startuml
title Modelo de Datos — Sprint 1 (entidades implementadas)\nWireless HeatMapper
skinparam classBackgroundColor #EBF5FB
skinparam classBorderColor #2980B9
skinparam classHeaderBackgroundColor #2980B9
skinparam classHeaderFontColor white
skinparam arrowColor #2980B9
skinparam noteBackgroundColor #FFFDE7
hide circle

enum RolUsuario {
  ADMIN
  TECNICO
}

enum EstadoProyecto {
  NUEVO
  EN_PROGRESO
  COMPLETADO
  ARCHIVADO
}

class Usuario {
  +id : Integer
  +email : String
  +passwordHash : String
  +nombre : String
  +rol : RolUsuario
  +activo : Boolean
  +createdAt : DateTime
  +ultimoAcceso : DateTime
}

class RefreshToken {
  +id : Integer
  +token : String
  +expiresAt : DateTime
  +createdAt : DateTime
}

class Cliente {
  +id : Integer
  +nombre : String
  +activo : Boolean
  +createdAt : DateTime
}

class Proyecto {
  +id : Integer
  +nombre : String
  +descripcion : String
  +estado : EstadoProyecto
  +ultimaActividad : DateTime
  +cantidadPuntos : Integer
  +createdAt : DateTime
}

Usuario "1" --> "0..*" RefreshToken : tiene >
Usuario "1" --> "0..*" Proyecto : gestiona >
Cliente "1" --> "0..*" Proyecto : tiene >

note bottom of RefreshToken
  Eliminado físicamente en logout (PB-09 CA4)
  JWT: 15 min access + 7 días refresh
end note

note right of Proyecto
  Aislamiento por tecnico_id:
  un técnico solo ve sus proyectos.
  El admin ve todos vía
  GET /api/admin/proyectos
end note
@enduml
```

> _Figura 17: Diagrama de Clases Conceptual del Sprint 1._

### 10.6.3.2 Modelo Lógico (Esquema Relacional)

```plantuml
@startuml
title Modelo Lógico (Esquema Relacional) — Sprint 1\nWireless HeatMapper
skinparam classBackgroundColor #EBF5FB
skinparam classBorderColor #2980B9
skinparam classHeaderBackgroundColor #2980B9
skinparam classHeaderFontColor white
skinparam arrowColor #2980B9
hide circle

class "usuario" <<Table>> {
  PK id : SERIAL
  --
  email : VARCHAR(255) UNIQUE NOT NULL
  password_hash : VARCHAR(255) NOT NULL
  nombre : VARCHAR(120) NOT NULL
  rol : VARCHAR(30) NOT NULL DEFAULT 'tecnico'
  activo : BOOLEAN NOT NULL DEFAULT TRUE
  ultimo_acceso : TIMESTAMPTZ
  created_at : TIMESTAMPTZ DEFAULT now()
}

class "refresh_token" <<Table>> {
  PK id : SERIAL
  --
  token : VARCHAR(64) UNIQUE NOT NULL
  expires_at : TIMESTAMPTZ NOT NULL
  created_at : TIMESTAMPTZ DEFAULT now()
  FK usuario_id : INTEGER NOT NULL ON DELETE CASCADE
}

class "cliente" <<Table>> {
  PK id : SERIAL
  --
  nombre : VARCHAR(100) UNIQUE NOT NULL
  activo : BOOLEAN NOT NULL DEFAULT TRUE
  created_at : TIMESTAMPTZ DEFAULT now()
}

class "proyecto" <<Table>> {
  PK id : SERIAL
  --
  nombre : VARCHAR(200) NOT NULL
  descripcion : VARCHAR(500)
  estado : estado_proyecto NOT NULL DEFAULT 'nuevo'
  ultima_actividad : TIMESTAMPTZ DEFAULT now()
  cantidad_puntos : INTEGER NOT NULL DEFAULT 0
  created_at : TIMESTAMPTZ DEFAULT now()
  FK tecnico_id : INTEGER NOT NULL
  FK cliente_id : INTEGER
}

"usuario" "1" --> "0..*" "refresh_token" : usuario_id
"usuario" "1" --> "0..*" "proyecto" : tecnico_id
"cliente" "1" --> "0..*" "proyecto" : cliente_id
@enduml
```

> _Figura 18: Modelo lógico (esquema relacional) del Sprint 1._

### 10.6.3.3 Diseño Físico (Tablas PostgreSQL)

**Tabla: `usuario`**

| Columna       | Tipo PostgreSQL | Restricciones              |
| ------------- | --------------- | -------------------------- |
| id            | SERIAL          | PRIMARY KEY                |
| nombre        | VARCHAR(120)    | NOT NULL                   |
| email         | VARCHAR(255)    | UNIQUE, NOT NULL           |
| password_hash | VARCHAR(255)    | NOT NULL                   |
| rol           | VARCHAR(30)     | NOT NULL DEFAULT 'tecnico' |
| activo        | BOOLEAN         | NOT NULL DEFAULT TRUE      |
| ultimo_acceso | TIMESTAMPTZ     | NULLABLE                   |
| created_at    | TIMESTAMPTZ     | NOT NULL DEFAULT now()     |

**Tabla: `refresh_token`**

| Columna    | Tipo PostgreSQL | Restricciones                                |
| ---------- | --------------- | -------------------------------------------- |
| id         | SERIAL          | PRIMARY KEY                                  |
| token      | VARCHAR(64)     | UNIQUE, NOT NULL                             |
| usuario_id | INTEGER         | NOT NULL, FK → usuario(id) ON DELETE CASCADE |
| expires_at | TIMESTAMPTZ     | NOT NULL                                     |
| created_at | TIMESTAMPTZ     | NOT NULL DEFAULT now()                       |

**Tabla: `cliente`**

| Columna    | Tipo PostgreSQL | Restricciones          |
| ---------- | --------------- | ---------------------- |
| id         | SERIAL          | PRIMARY KEY            |
| nombre     | VARCHAR(100)    | UNIQUE, NOT NULL       |
| activo     | BOOLEAN         | NOT NULL DEFAULT TRUE  |
| created_at | TIMESTAMPTZ     | NOT NULL DEFAULT now() |

**Tabla: `proyecto`**

| Columna          | Tipo PostgreSQL        | Restricciones                          |
| ---------------- | ---------------------- | -------------------------------------- |
| id               | SERIAL                 | PRIMARY KEY                            |
| nombre           | VARCHAR(200)           | NOT NULL                               |
| descripcion      | VARCHAR(500)           | NULLABLE                               |
| cliente_id       | INTEGER                | NULLABLE, FK → cliente(id)             |
| estado           | estado_proyecto (ENUM) | NOT NULL DEFAULT 'nuevo'               |
| tecnico_id       | INTEGER                | NOT NULL, FK → usuario(id)             |
| ultima_actividad | TIMESTAMPTZ            | NOT NULL DEFAULT now() ON UPDATE now() |
| cantidad_puntos  | INTEGER                | NOT NULL DEFAULT 0                     |
| created_at       | TIMESTAMPTZ            | NOT NULL DEFAULT now()                 |
