# 10.5 Sprint Backlog del Sprint 1 (F5)

**Sprint Backlog**
**Sprint número:** 1
**Tiempo programado:** 1 semana (5 días hábiles)
**Fecha de inicio del Sprint:** 20 de abril de 2026
**Fecha de finalización del Sprint:** 26 de abril de 2026

## 10.5.1 HU PB-13 (8 PHU) — Backend + Web

| Id     | Tarea                                                                       | Resp.    | Estim. | Estado       |
| ------ | --------------------------------------------------------------------------- | -------- | -----: | ------------ |
| Sp1-01 | Migración Alembic `0001_inicial_usuarios` (tabla `usuario`)                 | Jhasmany |   1 hr | Terminado |
| Sp1-02 | Modelo SQLAlchemy + schemas Pydantic `Usuario`/`UsuarioCreate`/`UsuarioOut` | Jhasmany |  2 hrs | Terminado |
| Sp1-03 | `UsuarioRepository` (CRUD básico + filtro por activo)                       | Jhasmany |  2 hrs | Terminado |
| Sp1-04 | `AuthService` con bcrypt (hash, verify) + emisión de JWT (python-jose)      | Jhasmany |  3 hrs | Terminado |
| Sp1-05 | Endpoint `POST /api/admin/usuarios` (crear) protegido por rol ADMIN         | Jhasmany |  2 hrs | Terminado |
| Sp1-06 | Endpoints `PATCH /usuarios/{id}` (activar/desactivar/reset password)        | Jhasmany |  2 hrs | Terminado |
| Sp1-07 | Tests pytest: creación, duplicado, activar/desactivar                       | Jhasmany |  3 hrs | Terminado |
| Sp1-08 | Pantalla `LoginAdmin.tsx` (React + react-hook-form)                         | Borys    |  2 hrs | Terminado |
| Sp1-09 | Pantalla `GestionUsuarios.tsx` con tabla + modal de creación                | Borys    |  4 hrs | Terminado |
| Sp1-10 | Hook `useUsuarios` (TanStack Query: list, create, toggle)                   | Borys    |  2 hrs | Terminado |
| Sp1-11 | Tipos TS generados desde OpenAPI (`openapi-typescript`)                     | Borys    |   1 hr | Terminado |
| Sp1-12 | Prueba de aceptación PB-13 con PO                                           | Ambos    |   1 hr | ⏳ R-4       |

## 10.5.2 HU PB-09 (5 PHU) — Backend + Móvil

| Id     | Tarea                                                                         | Resp.    | Estim. | Estado       |
| ------ | ----------------------------------------------------------------------------- | -------- | -----: | ------------ |
| Sp1-13 | Endpoint `POST /api/auth/login` (OAuth2 password flow)                        | Jhasmany |  2 hrs | Terminado |
| Sp1-14 | Endpoint `POST /api/auth/refresh`                                             | Jhasmany |  2 hrs | Terminado |
| Sp1-15 | Endpoint `POST /api/auth/logout` (revoca refresh)                             | Jhasmany |   1 hr | Terminado |
| Sp1-16 | Tests pytest del flujo auth (login OK, login KO, refresh, logout)             | Jhasmany |  2 hrs | Terminado |
| Sp1-17 | `LoginPage` Flutter con `flutter_form_builder` + validaciones                 | Jhasmany |  3 hrs | Terminado |
| Sp1-18 | `AuthRepository` (Dio) y `AuthCubit` (BLoC) con persistencia en SecureStorage | Jhasmany |  3 hrs | Terminado |
| Sp1-19 | `AuthInterceptor` Dio: refresh automático al recibir 401                      | Jhasmany |  3 hrs | Terminado |
| Sp1-20 | `ConnectivityMonitor` + banner "Sin conexión" en `LoginPage`                  | Jhasmany |  2 hrs | Terminado |
| Sp1-21 | Widget tests de `LoginPage` y unit tests de `AuthCubit`                       | Jhasmany |  2 hrs | Terminado |
| Sp1-22 | Prueba de aceptación PB-09 con PO (crear admin → crear técnico → loguearse)   | Ambos    |   1 hr | ⏳ R-4       |

## 10.5.3 HU PB-18 (5 PHU) — Backend + Web

| Id     | Tarea                                                                         | Resp.    | Estim. | Estado       |
| ------ | ----------------------------------------------------------------------------- | -------- | -----: | ------------ |
| Sp1-23 | Endpoint `GET /api/admin/proyectos` (paginado, filtros)                       | Jhasmany |  3 hrs | Terminado |
| Sp1-24 | Tests pytest del listado con seed data                                        | Jhasmany |  2 hrs | Terminado |
| Sp1-25 | Pantalla `ListadoProyectosOrg.tsx` (tabla + filtros)                          | Borys    |  4 hrs | Terminado |
| Sp1-26 | Hook `useProyectosOrg` con paginación TanStack Query                          | Borys    |  2 hrs | Terminado |
| Sp1-27 | Estado vacío y skeleton de carga                                              | Borys    |   1 hr | Terminado |
| Sp1-28 | Prueba de aceptación PB-18 con PO                                             | Ambos    |   1 hr | ⏳ R-4       |
| Sp1-51 | Endpoints admin `PATCH /admin/proyectos/{id}/archivar` y `/{id}/reasignar`    | Borys    |  2 hrs | Terminado |
| Sp1-52 | Botones "Archivar" y "Reasignar" en `ListadoProyectosOrg.tsx` + modal + hooks | Borys    |  3 hrs | Terminado |

## 10.5.4 HU PB-19 (3 PHU) — Backend + Web

| Id     | Tarea                                                                              | Resp.    | Estim. | Estado       |
| ------ | ---------------------------------------------------------------------------------- | -------- | -----: | ------------ |
| Sp1-29 | Modelo SQLAlchemy `Cliente` + migración `0002_cliente_y_proyecto`                  | Jhasmany |  3 hrs | Terminado |
| Sp1-30 | Schemas Pydantic `ClienteCreate`/`ClienteOut`/`ClienteBasicoOut`/`ClienteUpdate`   | Jhasmany |   1 hr | Terminado |
| Sp1-31 | `ClienteRepository` (listar, crear, actualizar, desactivar)                        | Jhasmany |  2 hrs | Terminado |
| Sp1-32 | Endpoint `GET /api/clientes` (público para autenticados, lista activos)            | Jhasmany |   1 hr | Terminado |
| Sp1-33 | Endpoint `POST /api/admin/clientes` (solo ADMIN)                                   | Jhasmany |   1 hr | Terminado |
| Sp1-34 | Endpoints `PUT /api/admin/clientes/{id}` + `PATCH .../{id}/desactivar`             | Jhasmany |   1 hr | Terminado |
| Sp1-35 | Tests pytest: crear, duplicado, listar, desactivar, 403 para TECNICO               | Jhasmany |  2 hrs | Terminado |
| Sp1-36 | Página `GestionClientesPage.tsx` (tabla + modal crear/desactivar)                  | Borys    |  3 hrs | Terminado |
| Sp1-37 | Hook `useClientes` + integrar selector de clientes en formulario de proyecto (web) | Borys    |  2 hrs | Terminado |
| Sp1-38 | Prueba de aceptación PB-19 con PO                                                  | Ambos    |   1 hr | ⏳ R-4       |

## 10.5.5 HU PB-01 (5 PHU) — Backend + Móvil

| Id     | Tarea                                                                                   | Resp.    | Estim. | Estado       |
| ------ | --------------------------------------------------------------------------------------- | -------- | -----: | ------------ |
| Sp1-39 | Modelo SQLAlchemy `Proyecto` + migración incluida en `0002_cliente_y_proyecto`          | Jhasmany |  2 hrs | Terminado |
| Sp1-40 | Schemas Pydantic `ProyectoIn`/`ProyectoTecnicoOut` + `ProyectoRepository` con ownership | Jhasmany |  2 hrs | Terminado |
| Sp1-41 | Endpoints REST `GET/POST/PUT /api/proyectos`, `PATCH /{id}/archivar`, `DELETE /{id}`    | Jhasmany |  3 hrs | Terminado |
| Sp1-42 | Tests pytest CRUD: crear, editar, archivar, eliminar, ownership 404 cross-técnico       | Jhasmany |  3 hrs | Terminado |
| Sp1-43 | `ProyectoRemoteDatasource` (Dio) + `ProyectoRepositoryImpl` + `ProyectoCubit` (BLoC)    | Jhasmany |  3 hrs | Terminado |
| Sp1-44 | `ProyectoFormPage` (Flutter) con selector de cliente (`ClienteRemoteDatasource`)        | Jhasmany |  3 hrs | Terminado |
| Sp1-45 | Diálogos de confirmación para archivar y eliminar en `ProyectosPage`                    | Jhasmany |   1 hr | Terminado |
| Sp1-46 | Prueba de aceptación PB-01 con PO (login → crear → editar → archivar → eliminar)        | Ambos    |   1 hr | ⏳ R-4       |

## 10.5.6 HU PB-10 (3 PHU) — Backend + Móvil

| Id     | Tarea                                                                        | Resp.    | Estim. | Estado       |
| ------ | ---------------------------------------------------------------------------- | -------- | -----: | ------------ |
| Sp1-47 | Endpoint `GET /api/proyectos` con filtro de estado (activos / archivados)    | Jhasmany |   1 hr | Terminado |
| Sp1-48 | Widget de búsqueda local + ordenamiento por última actividad                 | Jhasmany |  2 hrs | Terminado |
| Sp1-49 | Estado vacío con CTA "Crear primer proyecto" + skeleton de carga             | Jhasmany |   1 hr | Terminado |
| Sp1-50 | Prueba de aceptación PB-10 con PO (listar, buscar, archivar, ver archivados) | Ambos    |   1 hr | ⏳ R-4       |

## 10.5.7 Resumen Sprint 1

| Concepto          |   Valor |
| ----------------- | ------: |
| Total de tareas   |      52 |
| Horas estimadas   | ~99 hrs |
| PHU comprometidos |      29 |

> **Estados posibles:** Por hacer · En proceso · Terminado · Bloqueado
