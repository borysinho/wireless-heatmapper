# Sprint 1 — Pruebas

## S1.4 Pruebas Realizadas

Las pruebas del Sprint 1 siguen tres filtros de verificación complementarios que cubren la perspectiva del desarrollador, del equipo de calidad y del responsable del producto.

---

## Filtro 1 — Pruebas Unitarias (Desarrollador)

Cada desarrollador entregó código con pruebas unitarias que verifican la lógica de negocio de forma aislada, sin depender de la base de datos real ni de la red.

### Backend (pytest)

**Tabla 5.** Pruebas unitarias del backend (pytest) — Sprint 1

| ID Prueba   | Módulo                  | Caso probado                                                         | Resultado |
| ----------- | ----------------------- | -------------------------------------------------------------------- | :-------: |
| UT-BE-01    | `AuthService`           | Autenticación exitosa con credenciales válidas retorna token JWT     | Aprobada  |
| UT-BE-02    | `AuthService`           | Autenticación con contraseña incorrecta lanza `HTTPException 401`    | Aprobada  |
| UT-BE-03    | `AuthService`           | Autenticación de usuario inactivo lanza `HTTPException 401`          | Aprobada  |
| UT-BE-04    | `UserService`           | Creación de usuario con correo duplicado lanza `HTTPException 409`   | Aprobada  |
| UT-BE-05    | `UserService`           | Creación de usuario con datos válidos retorna usuario creado         | Aprobada  |
| UT-BE-06    | `OrganizationService`   | Creación de organización con nombre duplicado lanza `HTTPException 409` | Aprobada |
| UT-BE-07    | `OrganizationService`   | Desactivación de organización actualiza campo `activo = False`       | Aprobada  |
| UT-BE-08    | `ProjectService`        | Creación de proyecto con organización inexistente lanza `HTTPException 404` | Aprobada |
| UT-BE-09    | `ProjectService`        | Listado de proyectos filtrado por `organizacion_id` retorna solo los correspondientes | Aprobada |
| UT-BE-10    | Middleware JWT           | Token expirado en endpoint protegido retorna `HTTPException 401`     | Aprobada  |

### App Móvil (flutter_test)

**Tabla 6.** Pruebas unitarias de la app móvil (flutter_test) — Sprint 1

| ID Prueba   | Módulo                  | Caso probado                                                         | Resultado |
| ----------- | ----------------------- | -------------------------------------------------------------------- | :-------: |
| UT-FL-01    | `AuthCubit`             | Estado inicial es `AuthInitial`                                      | Aprobada  |
| UT-FL-02    | `AuthCubit`             | Login exitoso emite `AuthLoading` → `AuthAuthenticated`              | Aprobada  |
| UT-FL-03    | `AuthCubit`             | Login fallido emite `AuthLoading` → `AuthError` con mensaje          | Aprobada  |
| UT-FL-04    | `AuthRepository`        | `login()` llama al datasource con correo y contraseña correctos      | Aprobada  |
| UT-FL-05    | `LoginScreen` widget    | Botón de login deshabilitado si campos vacíos                        | Aprobada  |

---

## Filtro 2 — Pruebas de Calidad (QA)

El segundo integrante actuó como QA verificando funcionalidad, rendimiento y seguridad de los módulos entregados.

### Pruebas funcionales

**Tabla 7.** Pruebas funcionales de calidad — Sprint 1

| ID Prueba   | Funcionalidad                         | Escenario probado                                          | Resultado |
| ----------- | ------------------------------------- | ---------------------------------------------------------- | :-------: |
| QA-F-01     | Login panel web                       | Flujo completo de login con usuario administrador          | Aprobada  |
| QA-F-02     | Login panel web                       | Login con contraseña errónea muestra mensaje sin revelar campo | Aprobada |
| QA-F-03     | Gestión de usuarios                   | CRUD completo desde panel web                              | Aprobada  |
| QA-F-04     | Gestión de organizaciones             | CRUD completo; intento de nombre duplicado muestra error   | Aprobada  |
| QA-F-05     | Gestión de proyectos                  | Crear proyecto, filtrar por cliente, editar estado         | Aprobada  |
| QA-F-06     | Login app móvil                       | Flujo completo de autenticación en dispositivo Android     | Aprobada  |

### Pruebas de rendimiento

**Tabla 8.** Pruebas de rendimiento de endpoints críticos — Sprint 1

| ID Prueba   | Endpoint                         | Métrica                        | Resultado  |
| ----------- | -------------------------------- | ------------------------------ | :--------: |
| QA-P-01     | `POST /auth/login`               | Tiempo de respuesta < 500 ms   | 180 ms  |
| QA-P-02     | `GET /projects?org_id=1`         | Tiempo de respuesta < 300 ms   | 95 ms   |
| QA-P-03     | `GET /users` (100 registros)     | Tiempo de respuesta < 500 ms   | 210 ms  |

### Pruebas de seguridad

**Tabla 9.** Pruebas de seguridad de autenticación y autorización — Sprint 1

| ID Prueba   | Escenario                                                    | Resultado |
| ----------- | ------------------------------------------------------------ | :-------: |
| QA-S-01     | Acceso a `/users` sin token retorna 401                      | Aprobada  |
| QA-S-02     | Acceso a `/users` con token de rol `tecnico` retorna 403     | Aprobada  |
| QA-S-03     | Token manipulado (firma inválida) retorna 401                | Aprobada  |

---

## Filtro 3 — Pruebas de Aceptación (Product Owner)

El Product Owner verificó que cada historia de usuario cumple con sus criterios de aceptación definidos en la planificación del sprint.

**Tabla 10.** Pruebas de aceptación — Verificación por historia de usuario

| HU     | Criterios verificados                                                  | Aceptada |
| ------ | ---------------------------------------------------------------------- | :------: |
| PB-01  | CRUD de usuarios; no permite correo duplicado; desactivación funciona  | Sí    |
| PB-09  | CRUD de organizaciones; nombre duplicado muestra error; desactivación  | Sí    |
| PB-10  | Login web; JWT persiste en sesión; logout funciona; error sin revelar campo | Sí |
| PB-13  | CRUD de proyectos; asociación con cliente; estados correctos           | Sí    |
| PB-18  | Listado filtrado por cliente; navegación al detalle funciona           | Sí    |
| PB-19  | Login app móvil; token almacenado; sesión persiste; logout funciona    | Sí    |

**Resultado del Sprint 1:** Todas las historias de usuario comprometidas fueron aceptadas por el Product Owner. El incremento es una versión operativa que aporta valor: el sistema cuenta con autenticación segura, gestión completa de la estructura organizacional (usuarios, clientes, proyectos) y acceso desde la app móvil.

---
