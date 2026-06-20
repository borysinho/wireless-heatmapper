# Sprint 1 — Modelos Generados

## S1.2 Modelos del Sprint 1

---

## S1.2.1 Modelo de Contexto — Sprint 1

El diagrama de casos de uso muestra exclusivamente las funcionalidades abarcadas en el Sprint 1:

```plantuml
@startuml Contexto_Sprint1
skinparam actorBackgroundColor #EBF5FB
skinparam usecaseBackgroundColor #EBF5FB
skinparam usecaseBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Modelo de Contexto — Sprint 1 (Fundación)

left to right direction

actor Administrador as ADMIN
actor "Técnico\n(App Móvil)" as TEC

rectangle "Wireless HeatMapper — Sprint 1" {
  usecase "PB-10\nAutenticarse\nen panel web" as UC10
  usecase "PB-01\nGestionar\nusuarios" as UC01
  usecase "PB-09\nGestionar\nclientes" as UC09
  usecase "PB-13\nGestionar\nproyectos" as UC13
  usecase "PB-18\nVer proyectos\npor cliente" as UC18
  usecase "PB-19\nAutenticarse\nen app móvil" as UC19
}

ADMIN --> UC10
ADMIN --> UC01
ADMIN --> UC09
ADMIN --> UC13
ADMIN --> UC18
@enduml
```

_Figura 10. Modelo de contexto actualizado al Sprint 1 — Casos de uso implementados en la primera iteración._

---

### Diagrama de Paquetes (Sprint 1)

```plantuml
@startuml Paquetes_Sprint1
skinparam packageBackgroundColor #EBF5FB
skinparam packageBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Diagrama de Paquetes — Sprint 1

package "App Móvil (Flutter)" as MOBILE {
  package "presentation" {
    [LoginScreen]
    [DashboardScreen]
    [auth_bloc]
  }
  package "domain" {
    [AuthUseCase]
    [UserEntity]
  }
  package "data" {
    [AuthRemoteDataSource]
    [AuthRepository]
  }
}

package "Backend (FastAPI)" as BACKEND {
  package "api/v1" {
    [auth_router]
    [users_router]
    [organizations_router]
    [projects_router]
  }
  package "schemas" {
    [UserSchema]
    [OrganizationSchema]
    [ProjectSchema]
    [TokenSchema]
  }
  package "services" {
    [AuthService]
    [UserService]
    [OrganizationService]
    [ProjectService]
  }
  package "models" {
    [UserModel]
    [OrganizationModel]
    [ProjectModel]
  }
}

package "Web Admin (React)" as WEB {
  package "pages" {
    [LoginPage]
    [DashboardPage]
    [UsersPage]
    [OrganizationsPage]
    [ProjectsPage]
  }
  package "services" {
    [apiClient]
    [authService]
  }
}

package "Base de Datos\n(PostgreSQL)" as DB {
  [usuarios]
  [organizaciones]
  [proyectos]
}

MOBILE --> BACKEND : JWT / REST
WEB --> BACKEND : JWT / REST
BACKEND --> DB : SQLAlchemy
@enduml
```

_Figura 11. Diagrama de paquetes del Sprint 1 — Módulos implementados y sus dependencias._

### Diagrama de Despliegue (Sprint 1)

```plantuml
@startuml Despliegue_Sprint1
skinparam nodeBackgroundColor #EBF5FB
skinparam nodeBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Diagrama de Despliegue — Sprint 1

node "Dispositivo Android" as ANDROID {
  artifact "App Flutter" as APK
}

node "PC / Navegador Web" as BROWSER {
  artifact "Panel Admin React" as REACT_APP
}

node "Servidor (Docker Compose)" as SERVER {
  node "nginx:alpine" as NGINX {
    artifact "Reverse Proxy" as RP
  }
  node "backend:python" as API_NODE {
    artifact "FastAPI App" as API
  }
  node "db:postgres15" as DB_NODE {
    artifact "PostgreSQL" as DB
  }
}

ANDROID --> NGINX : HTTPS :443 /api
BROWSER --> NGINX : HTTPS :443
NGINX --> API : :8000 /api/v1
NGINX --> REACT_APP : :80 /*
API --> DB : :5432
@enduml
```

_Figura 12. Diagrama de despliegue del Sprint 1 — Configuración Docker de los contenedores en producción._

---

### Modelo Conceptual

```plantuml
@startuml Datos_Conceptual_Sprint1
skinparam classBackgroundColor #EBF5FB
skinparam classBorderColor #2980B9
skinparam arrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Modelo Conceptual de Datos — Sprint 1

class Usuario {
  nombre : string
  apellido : string
  correo : string
  contrasena_hash : string
  rol : enum
  activo : bool
  fecha_creacion : datetime
}

class Organizacion {
  nombre : string
  direccion : string
  contacto : string
  activo : bool
  fecha_creacion : datetime
}

class Proyecto {
  nombre : string
  descripcion : string
  estado : enum
  fecha_inicio : date
  fecha_fin : date
  fecha_creacion : datetime
}

Usuario "1" -- "0..*" Proyecto : gestiona >
Organizacion "1" -- "0..*" Proyecto : tiene >
@enduml
```

_Figura 13. Modelo conceptual de datos del Sprint 1 — Entidades de usuario, organización y proyecto._

### Modelo Lógico (Esquema Relacional)

```
usuarios (
  id          PK  SERIAL
  nombre          VARCHAR(100)  NOT NULL
  apellido        VARCHAR(100)  NOT NULL
  correo          VARCHAR(255)  NOT NULL  UNIQUE
  contrasena_hash VARCHAR(255)  NOT NULL
  rol             VARCHAR(20)   NOT NULL  CHECK (rol IN ('admin','tecnico','cliente'))
  activo          BOOLEAN       NOT NULL  DEFAULT TRUE
  fecha_creacion  TIMESTAMP     NOT NULL  DEFAULT NOW()
)

organizaciones (
  id             PK  SERIAL
  nombre             VARCHAR(200)  NOT NULL  UNIQUE
  direccion          VARCHAR(300)
  contacto           VARCHAR(200)
  activo             BOOLEAN       NOT NULL  DEFAULT TRUE
  fecha_creacion     TIMESTAMP     NOT NULL  DEFAULT NOW()
)

proyectos (
  id               PK  SERIAL
  nombre               VARCHAR(200)  NOT NULL
  descripcion          TEXT
  estado               VARCHAR(20)   NOT NULL  DEFAULT 'activo'
                         CHECK (estado IN ('activo','pausado','completado','cancelado'))
  fecha_inicio         DATE
  fecha_fin            DATE
  fecha_creacion       TIMESTAMP     NOT NULL  DEFAULT NOW()
  organizacion_id  FK  INTEGER       NOT NULL  REFERENCES organizaciones(id)
  usuario_id       FK  INTEGER                 REFERENCES usuarios(id)
)
```

### Normalización aplicada

- **1FN:** Todos los atributos son atómicos; no hay grupos repetitivos.
- **2FN:** No hay dependencias parciales (todas las tablas tienen clave primaria simple).
- **3FN:** No hay dependencias transitivas; `rol` y `estado` usan CHECK constraint en lugar de tabla de lookup para simplicidad en este sprint.

---

## S1.2.4 Modelo de Lógica — Flujo de Autenticación (PB-10 / PB-19)

El flujo de autenticación es el proceso más relevante del Sprint 1 por involucrar múltiples componentes. Se documenta mediante diagrama de secuencia:

```plantuml
@startuml Secuencia_Autenticacion_Sprint1
skinparam sequenceParticipantBackgroundColor #EBF5FB
skinparam sequenceParticipantBorderColor #2980B9
skinparam sequenceArrowColor #2980B9
skinparam backgroundColor #FAFAFA

title Flujo de Autenticación — PB-10 / PB-19

actor Usuario as USR
participant "Frontend\n(Web o App)" as FE
participant "FastAPI\n/auth/login" as API
participant "AuthService" as SVC
database "PostgreSQL\nusuarios" as DB

USR -> FE : Ingresa correo + contraseña
FE -> API : POST /api/v1/auth/login\n{email, password}
API -> SVC : autenticar(email, password)
SVC -> DB : SELECT * FROM usuarios\nWHERE correo = email AND activo = TRUE
DB --> SVC : registro del usuario
SVC -> SVC : verificar bcrypt(password, hash)

alt Credenciales válidas
  SVC --> API : usuario autenticado
  API -> API : generar JWT\n(sub=user_id, rol, exp)
  API --> FE : 200 OK {access_token, token_type}
  FE -> FE : almacenar token\n(SecureStorage / Context)
  FE --> USR : Redirige al dashboard
else Credenciales inválidas
  SVC --> API : fallo de autenticación
  API --> FE : 401 Unauthorized\n{detail: "Credenciales incorrectas"}
  FE --> USR : Muestra mensaje de error
end
@enduml
```

_Figura 14. Diagrama de secuencia — Flujo de autenticación mediante JWT (PB-10 / PB-19)._

---
