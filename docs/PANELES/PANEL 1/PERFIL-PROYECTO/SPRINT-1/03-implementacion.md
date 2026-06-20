# Sprint 1 — Implementación

## S1.3 Avance de Implementación

### Estándar de codificación adoptado

- **Backend (Python):** PEP 8, nombres en `snake_case`, docstrings en funciones públicas, tipado estático con `mypy`.
- **Frontend (TypeScript):** ESLint + Prettier, componentes funcionales con hooks, nombres de archivos en `PascalCase` para componentes y `camelCase` para utilidades.
- **Mobile (Dart):** Guía de estilo oficial de Flutter (`dart format`), BLoC separado por funcionalidad, repositorios con interfaz en dominio e implementación en data.

### Estilo arquitectónico

- **Backend:** Arquitectura por capas (presentación → servicios → repositorios → base de datos).
- **Frontend web:** Componentes con separación de lógica (`hooks`) y presentación (`JSX`).
- **App móvil:** Clean Architecture de tres capas (presentation / domain / data) con BLoC/Cubit.

### Gestión de base de datos

Se utiliza **SQLAlchemy ORM** con **Alembic** para migraciones. Esta decisión otorga:
- Desacoplamiento del modelo de dominio del motor de BD.
- Control de versiones del esquema en cada sprint.
- Facilidad de pruebas con base de datos en memoria (SQLite) en CI.

---

### Descripción de componentes implementados

#### Backend — FastAPI

| Componente                         | Descripción                                                                 |
| ---------------------------------- | --------------------------------------------------------------------------- |
| `POST /api/v1/auth/login`          | Autenticación con correo/contraseña, retorna JWT firmado (HS256)            |
| `GET/POST /api/v1/users`           | CRUD de usuarios del sistema (solo administrador)                           |
| `GET/POST /api/v1/organizations`   | CRUD de organizaciones/clientes                                             |
| `GET/POST /api/v1/projects`        | CRUD de proyectos de levantamiento                                          |
| `GET /api/v1/projects?org_id=X`    | Listado de proyectos filtrado por organización                              |
| Middleware JWT                     | Verificación de token en cada endpoint protegido; extracción de rol         |
| Alembic migration `001_initial`    | Creación de tablas `usuarios`, `organizaciones`, `proyectos`                |

#### Frontend Web — React + TypeScript

| Componente                | Descripción                                                              |
| ------------------------- | ------------------------------------------------------------------------ |
| `LoginPage`               | Formulario de autenticación con validación y manejo de errores           |
| `DashboardPage`           | Vista principal con resumen de proyectos activos                         |
| `UsersPage`               | Listado, creación y edición de usuarios                                  |
| `OrganizationsPage`       | CRUD de organizaciones con tabla paginada                                |
| `ProjectsPage`            | Listado y filtro de proyectos por organización; creación y edición       |
| `apiClient` (Axios)       | Instancia centralizada con interceptor para agregar token JWT al header  |
| Contexto de autenticación | Gestión global del estado de sesión (usuario, token, rol)                |

#### App Móvil — Flutter

| Componente              | Descripción                                                                    |
| ----------------------- | ------------------------------------------------------------------------------ |
| `LoginScreen`           | Pantalla de inicio de sesión con Material 3, Poppins/Inter, manejo de errores |
| `DashboardScreen`       | Pantalla principal post-login con listado de proyectos asignados               |
| `AuthCubit`             | Gestión de estado de autenticación (inicial, cargando, autenticado, error)     |
| `AuthRemoteDataSource`  | Cliente Dio para `POST /auth/login`; almacenamiento de token con FlutterSecureStorage |
| `AuthRepository`        | Abstracción de dominio que desacopla la UI de la fuente de datos               |

---

### Infraestructura

| Componente                   | Estado        |
| ----------------------------- | ------------- |
| `docker-compose.yml`          | Implementado  |
| Servicio `db` (PostgreSQL 15) | Implementado  |
| Servicio `backend` (FastAPI)  | Implementado  |
| Servicio `web` (React/Nginx)  | Implementado  |
| Servicio `nginx` (proxy)      | Implementado  |
| GitHub Actions (CI lint+test) | Implementado  |

---
