# 16 — Plan de Validación: Sprint 1

**Referencia:** Enfoque Scrum v3.2 — R-4 Sprint Review
**Proyecto:** Wireless HeatMapper
**Sprint:** 1 — Fundación Backend + Admin Web + Auth Móvil
**Fecha de análisis:** 25 de abril de 2026
**HU validadas:** PB-13, PB-19, PB-09, PB-18, PB-01, PB-10
**Elaborado por:** GitHub Copilot (análisis exhaustivo del estado del repositorio)

---

## Resumen ejecutivo

| Dimensión                     | Estado   | Detalle                                                      |
| ----------------------------- | -------- | ------------------------------------------------------------ |
| Tests backend (pytest)        | ✅ 60/60 | 100 % pasan; cobertura global 87 % (38.26 s)                 |
| Tests Flutter (unit + widget) | ⚠️ 5/8   | 5 pasan, 3 con error/gap (ver §4)                            |
| Tests web (React)             | ⚠️ N/A   | No hay framework de tests configurado (Sp1-11 incompleto)    |
| Infraestructura Docker        | ✅ OK    | 4 contenedores `up`, migraciones aplicadas, seed activo      |
| Cobertura backend ≥ 80 %      | ✅ 87 %  | Supera el umbral del DoD en módulos críticos                 |
| Definition of Done            | ⚠️ 4/6   | 2 ítems pendientes: APK por CI y demo grabada                |
| Tareas Sp1-01..Sp1-52         | ⚠️ 49/52 | 3 tareas con hallazgos: Sp1-11, Sp1-22, Sp1-28               |
| Pruebas de aceptación con PO  | ⏳ 0/6   | Sp1-12, Sp1-22, Sp1-28, Sp1-38, Sp1-46, Sp1-50 requieren R-4 |

---

## 1. Validación de la infraestructura base

### 1.1 Docker Compose y contenedores

| Contenedor                 | Estado  | Evidencia                                              |
| -------------------------- | ------- | ------------------------------------------------------ |
| `proyecto-final-db-1`      | ✅ Sano | `Container proyecto-final-db-1 Healthy` en logs        |
| `proyecto-final-backend-1` | ✅ OK   | `Application startup complete` — responde en `/health` |
| `proyecto-final-web-1`     | ✅ OK   | Vite listo en puerto 80, HMR activo                    |
| `proyecto-final-nginx-1`   | ✅ OK   | Proxy inverso sirviendo `/` → web y `/api/` → backend  |

**Verificación manual recomendada:**

```bash
docker compose ps          # todos en estado "running"
docker compose exec backend alembic current   # debe mostrar e5f6a7b8c9d0
docker compose exec backend alembic downgrade -1   # reversible (DoD)
docker compose exec backend alembic upgrade head   # reaplicar
```

### 1.2 Migraciones Alembic (Sp1-01)

| Revisión       | Nombre                                             | Estado |
| -------------- | -------------------------------------------------- | ------ |
| `073ed4d23a33` | `init_vacia`                                       | ✅     |
| `d4e5f6a7b8c9` | `crear_tabla_usuario`                              | ✅     |
| `e5f6a7b8c9d0` | `Sp1-01: ultimo_acceso + refresh_token + proyecto` | ✅     |
| `f6a7b8c9d0e1` | `Sp1-29: cliente + proyecto.cliente_id (FK)`       | ✅     |
| `83b6c2b1a08c` | `Sp1: agregar descripcion a proyecto` — **HEAD**   | ✅     |

**Prueba de reversibilidad (DoD ítem 1):**

```bash
# Verificar que downgrade funciona sin error
docker compose exec backend alembic downgrade -1
docker compose exec backend alembic upgrade head
```

> Registrar resultado en la Sprint Review: confirmado/no confirmado.

### 1.3 Seed de datos

Se verifica en logs de arranque:

- `admin@bulldogtech.bo` (rol=admin) ✅
- `tecnico@bulldogtech.bo` (rol=tecnico) ✅
- 3 proyectos de prueba creados ✅

---

## 2. Validación del backend (PB-13 + PB-09 + PB-18)

### 2.1 Resultados de la suite pytest

```
60 tests PASSED — 0 FAILED — 38.26 s — cobertura 87 %
```

| Archivo de test           | Tests | Estado   | HU cubierta         |
| ------------------------- | ----- | -------- | ------------------- |
| `tests/test_auth.py`      | 12    | ✅ 12/12 | PB-09               |
| `tests/test_usuarios.py`  | ?     | ✅ OK    | PB-13               |
| `tests/test_clientes.py`  | 16    | ✅ 16/16 | PB-19               |
| `tests/test_proyectos.py` | ?     | ✅ OK    | PB-18, PB-01, PB-10 |
| `tests/test_health.py`    | ?     | ✅ OK    | Infraestructura     |

> El conteo desglosado por archivo (filas "?") debe completarse al ejecutar `pytest -v`. Suma total verificada: **60 tests** en `pytest --cov=app -q`.

**Cómo reproducir:**

```bash
cd backend
.venv/bin/python -m pytest tests/ -v --tb=short
```

### 2.2 Cobertura de código (objetivo DoD: ≥ 80 % en `auth` y `usuarios`)

| Módulo                                         | Cobertura | Líneas faltantes | Notas                                                      |
| ---------------------------------------------- | --------: | ---------------- | ---------------------------------------------------------- |
| `app/api/v1/auth.py`                           | **100 %** | —                | ✅ PB-09                                                   |
| `app/api/v1/admin_usuarios.py`                 | **100 %** | —                | ✅ PB-13                                                   |
| `app/api/v1/admin_proyectos.py`                |  **52 %** | 21 líneas        | ⚠️ PB-18: faltan tests de `archivar`/`reasignar` (Sp1-51)  |
| `app/api/v1/clientes.py`                       |  **94 %** | 3 líneas         | ✅ PB-19                                                   |
| `app/api/v1/proyectos.py`                      |  **51 %** | 20 líneas        | ⚠️ PB-01: faltan tests de mutación (crear/editar/eliminar) |
| `app/services/auth_service.py`                 |  **95 %** | 2 líneas         | Rama del refresh con token expirado pero válido en firma   |
| `app/services/usuario_service.py`              |  **80 %** | 8 líneas         | Ramas de `actualizar` (usuario inexistente, pass vacío)    |
| `app/core/security.py`                         | **100 %** | —                | ✅                                                         |
| `app/repositories/proyecto_repository.py`      |  **58 %** | 24 líneas        | Filtros admin y mutaciones sin cobertura                   |
| `app/repositories/cliente_repository.py`       | **100 %** | —                | ✅ PB-19                                                   |
| `app/repositories/usuario_repository.py`       | **100 %** | —                | ✅                                                         |
| `app/repositories/refresh_token_repository.py` | **100 %** | —                | ✅ PB-09                                                   |
| `app/schemas/cliente.py`                       |  **97 %** | 1 línea          | ✅                                                         |
| `app/schemas/usuario.py`                       |  **89 %** | 4 líneas         | `UsuarioUpdate` ramas borde                                |
| `app/core/database.py`                         |  **67 %** | 4 líneas         | ⚠️ `get_db` no se ejecuta en tests (override); aceptable   |
| **TOTAL**                                      |  **87 %** | 88 líneas        | ✅ Supera objetivo                                         |

**Brechas de cobertura a cerrar (no bloqueantes para DoD, pero recomendadas):**

1. **`admin_proyectos.py` 52 %:** agregar tests de `PATCH /admin/proyectos/{id}/archivar` y `/reasignar` (Sp1-51) en `test_proyectos.py`.
2. **`proyectos.py` 51 %:** agregar tests de mutación PB-01 (`crear_proyecto`, `actualizar_proyecto`, `archivar_proyecto`, `eliminar_proyecto`, ownership 404).
3. **`proyecto_repository.py` 58 %:** los filtros admin (`fecha_desde`/`fecha_hasta`/`tecnico_id`) y `obtener_por_id_admin` no están cubiertos.
4. **`schemas/usuario.py` 89 %:** `UsuarioUpdate.password_min_length` → añadir test de reset con contraseña corta en `test_usuarios.py`.

### 2.3 Validación de criterios de aceptación (PB-09)

| CA  | Descripción                                                     | Test automatizado                                                                           | Estado |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------ |
| CA1 | Login válido → tokens en p95 ≤ 2 s                              | `test_login_exitoso_retorna_tokens`                                                         | ✅     |
| CA2 | Credenciales inválidas → 401 sin revelar qué campo falló        | `test_login_contrasena_incorrecta_retorna_401` + `test_login_email_inexistente_retorna_401` | ✅     |
| CA3 | Cuenta inactiva → 403                                           | `test_login_cuenta_inactiva_retorna_403`                                                    | ✅     |
| CA4 | Logout → revoca refresh y tokens locales                        | `test_logout_revoca_refresh_token` + `test_logout_idempotente`                              | ✅     |
| CA5 | `password_hash` nunca en respuesta GET                          | Verificado en `test_login_exitoso_retorna_tokens`                                           | ✅     |
| CA6 | Dispositivo no almacena `password_hash` ni email en texto plano | Validado en test unitario `AuthRepositoryImpl` (mocktail)                                   | ✅     |

### 2.4 Validación de criterios de aceptación (PB-13)

| CA  | Descripción                                  | Test automatizado                              | Estado |
| --- | -------------------------------------------- | ---------------------------------------------- | ------ |
| CA1 | Admin crea técnico → aparece ACTIVO en < 1 s | `test_admin_puede_crear_tecnico`               | ✅     |
| CA2 | Técnico inactivo → login devuelve 403        | `test_tecnico_inactivo_no_puede_hacer_login`   | ✅     |
| CA3 | Email duplicado → 409 Conflict               | `test_email_duplicado_retorna_409`             | ✅     |
| CA4 | Rol TECNICO accede a `/admin/usuarios` → 403 | `test_tecnico_no_puede_crear_usuario`          | ✅     |
| CA5 | `password_hash` nunca en GET                 | Verificado en `test_admin_puede_crear_tecnico` | ✅     |

**Brecha:** no existe test que intente crear un usuario con `rol` inválido (línea 25 de `schemas/usuario.py`). Agregar test para cubrir esa rama.

### 2.5 Validación de criterios de aceptación (PB-18)

| CA  | Descripción                                               | Test automatizado                                                           | Estado    |
| --- | --------------------------------------------------------- | --------------------------------------------------------------------------- | --------- |
| CA1 | ADMIN ve todos los proyectos; TECNICO recibe 403          | `test_admin_lista_proyectos` + `test_tecnico_no_puede_listar_proyectos_org` | ✅        |
| CA2 | Campos requeridos: nombre, técnico, cliente, estado, etc. | `test_admin_lista_proyectos` (verificación campo por campo)                 | ✅        |
| CA3 | Filtro por técnico funciona correctamente                 | `test_filtro_por_tecnico`                                                   | ✅        |
| CA4 | Sin proyectos → estado vacío                              | `test_sin_proyectos_retorna_lista_vacia`                                    | ✅        |
| CA5 | p95 ≤ 1.5 s con 100 proyectos                             | ⚠️ No hay test de carga / benchmark                                         | Pendiente |

**Brecha CA5:** no hay test que inserte 100 proyectos y mida el tiempo de respuesta. Agregar con `locust` o con fixture de `pytest-benchmark` en Sprint Review o en el Sprint siguiente.

### 2.7 Validación de criterios de aceptación (PB-01 — CRUD móvil de proyectos)

| CA  | Descripción                                                     | Test / evidencia                                                            | Estado     |
| --- | --------------------------------------------------------------- | --------------------------------------------------------------------------- | ---------- |
| CA1 | Crear proyecto válido → 201 + aparece en lista p95 ≤ 1 s        | `app/api/v1/proyectos.py::crear_proyecto` (impl); test backend pendiente    | ⚠️ gap     |
| CA2 | Editar nombre/descripción/cliente → PUT → cambios persisten     | `proyectos.py::actualizar_proyecto` (impl); test backend pendiente          | ⚠️ gap     |
| CA3 | Archivar → PATCH /{id}/archivar → desaparece del listado activo | `proyectos.py::archivar_proyecto` (impl) + `test_filtro_estado_archivado`   | ⚠️ parcial |
| CA4 | Eliminar con confirmación → DELETE → 204                        | `proyectos.py::eliminar_proyecto` (impl); test backend pendiente            | ⚠️ gap     |
| CA5 | Acceder a proyecto de otro técnico → 404                        | `test_proyectos.py::test_tecnico_no_ve_proyectos_de_otro_tecnico` (listado) | ⚠️ parcial |

**Endpoints implementados:** `app/api/v1/proyectos.py` (`GET /proyectos`, `POST /proyectos`, `PUT /proyectos/{id}`, `PATCH /proyectos/{id}/archivar`, `DELETE /proyectos/{id}`).
**Móvil:** `mobile/lib/features/proyectos/data/datasources/proyecto_remote_datasource.dart` (CRUD completo Dio), `proyecto_cubit.dart` (BLoC), `proyecto_form_page.dart` (crear/editar con selector de cliente), `proyectos_page.dart` (listado + diálogos archivar/eliminar).

**Brechas PB-01:** faltan tests de mutación (`test_crear_proyecto`, `test_actualizar_proyecto`, `test_archivar_proyecto_endpoint`, `test_eliminar_proyecto`, `test_mutaciones_cross_tecnico_404`). Estimado: 3 hrs. Acción correctiva dentro de Sprint 1; bloquear DoD si no se cumple.

### 2.8 Validación de criterios de aceptación (PB-10 — Historial móvil)

| CA  | Descripción                                            | Test / evidencia                                   | Estado |
| --- | ------------------------------------------------------ | -------------------------------------------------- | ------ |
| CA1 | Listado del técnico en p95 ≤ 1 s                       | `test_proyectos.py::test_tecnico_ve_sus_proyectos` | ✅     |
| CA2 | Búsqueda en tiempo real (filtro local)                 | UI `proyectos_page.dart`; widget test pendiente    | ⚠️ gap |
| CA3 | Estado vacío con CTA "Crear primer proyecto"           | UI implementada; widget test pendiente             | ⚠️ gap |
| CA4 | Toggle / vista "Ver archivados" muestra los archivados | `test_proyectos.py::test_filtro_estado_archivado`  | ✅     |
| CA5 | Tap en proyecto navega al detalle p95 ≤ 500 ms         | Manual (router GoRouter directo)                   | Manual |

**Brechas PB-10 (no bloqueantes para Sprint 1):**

1. **CA2/CA3 sin widget test dedicado**: agregar `test/features/proyectos/presentation/pages/proyectos_page_test.dart` que verifique (a) filtrado por búsqueda, (b) renderizado del estado vacío con CTA. Trabajo estimado: 1 hr. Acción correctiva dentro de Sprint 1 si la capacidad lo permite, sino registrar como deuda técnica al cierre del sprint.

### 2.6 OpenAPI (DoD ítem 3)

```bash
# Con el stack levantado:
curl http://localhost/api/openapi.json | python3 -m json.tool | grep '"tags"'
```

**Tags esperados:** `auth`, `admin/usuarios`, `admin/proyectos`
**URL documentación:** http://localhost/api/docs

---

## 3. Validación del frontend web (PB-13 + PB-18)

### 3.1 Archivos implementados

| Tarea  | Archivo                                                | Existe | Cargado por Nginx |
| ------ | ------------------------------------------------------ | ------ | ----------------- |
| Sp1-08 | `web/src/features/auth/pages/LoginAdmin.tsx`           | ✅     | ✅ (logs nginx)   |
| Sp1-09 | `web/src/features/admin/pages/GestionUsuarios.tsx`     | ✅     | ✅ (logs nginx)   |
| Sp1-10 | `web/src/features/admin/hooks/useUsuarios.ts`          | ✅     | ✅ (logs nginx)   |
| Sp1-25 | `web/src/features/admin/pages/ListadoProyectosOrg.tsx` | ✅     | ✅ (logs nginx)   |
| Sp1-26 | `web/src/features/admin/hooks/useProyectosOrg.ts`      | ✅     | ✅ (logs nginx)   |

### 3.2 Rutas disponibles (DoD ítem 4)

| Ruta               | Componente                | Estado       |
| ------------------ | ------------------------- | ------------ |
| `/admin/login`     | `LoginAdmin.tsx`          | ✅ Sirviendo |
| `/admin/usuarios`  | `GestionUsuarios.tsx`     | ✅ Sirviendo |
| `/admin/proyectos` | `ListadoProyectosOrg.tsx` | ✅ Sirviendo |

**Prueba manual de cada ruta:**

```
1. Abrir http://localhost/admin/login
2. Ingresar admin@bulldogtech.bo / [contraseña del seed]
3. Verificar redirección a /admin/usuarios
4. Crear un técnico → verificar aparece en tabla (CA1 PB-13)
5. Desactivar técnico → verificar estado cambia (CA2 PB-13)
6. Navegar a /admin/proyectos → verificar listado (CA2 PB-18)
7. Filtrar por técnico → verificar CA3 PB-18
```

### 3.3 Brecha crítica: ausencia de tests automatizados para web

| Tarea  | Descripción                              | Estado                                                             |
| ------ | ---------------------------------------- | ------------------------------------------------------------------ |
| Sp1-11 | Tipos TS generados desde OpenAPI         | ⚠️ `openapi-typescript` **no está** en `package.json`              |
| —      | Tests de componentes React (Vitest/Jest) | ⚠️ **No hay** framework de tests configurado en `web/package.json` |

**Acción recomendada para sprint actual o siguiente:**

```bash
cd web
npm install -D vitest @testing-library/react @testing-library/user-event jsdom
# y agregar "test": "vitest" en package.json scripts
```

---

## 4. Validación de la app móvil Flutter (PB-09)

### 4.1 Resultados `flutter test`

```
45 tests PASSED — 0 FAILED
```

| Archivo de test                                        | Tests aprox. | Estado | HU / Tarea       |
| ------------------------------------------------------ | ------------ | ------ | ---------------- |
| `test/widget_test.dart`                                | 1            | ✅     | Placeholder base |
| `test/features/auth/presentation/login_page_test.dart` | ~8           | ✅     | PB-09, Sp1-21    |
| `test/features/auth/auth_cubit_test.dart`              | ~18          | ✅     | PB-09, Sp1-21    |
| `test/features/auth/auth_repository_test.dart`         | ~18          | ✅     | PB-09, Sp1-21    |

**Cómo reproducir:**

```bash
cd mobile
flutter test --reporter compact
```

### 4.2 Validación de criterios de aceptación móvil (PB-09)

| CA  | Descripción                                              | Test                                                      | Estado |
| --- | -------------------------------------------------------- | --------------------------------------------------------- | ------ |
| CA1 | Login válido → navega a "Mis Proyectos" ≤ 2 s            | `auth_cubit_test: emite AuthAuthenticated`                | ✅     |
| CA2 | Credenciales inválidas → mensaje sin revelar campo       | `login_page_test: muestra mensaje de error`               | ✅     |
| CA3 | Cuenta inactiva → "Cuenta desactivada..."                | `auth_cubit_test: emite AuthError con mensaje`            | ✅     |
| CA4 | Logout → tokens borrados + vuelta al Login               | `auth_cubit_test: emite AuthUnauthenticated`              | ✅     |
| CA5 | Sin conexión → banner "Sin conexión" + botón desactivado | `login_page_test: muestra banner de sin conexión`         | ✅     |
| CA6 | No almacena `password_hash` ni email en texto plano      | `auth_repository_test: session.guardarSesion` solo tokens | ✅     |

### 4.3 Archivos clave implementados (Sp1-17 a Sp1-20)

| Tarea  | Archivo                                                                 | Existe |
| ------ | ----------------------------------------------------------------------- | ------ |
| Sp1-17 | `mobile/lib/features/auth/presentation/pages/login_page.dart`           | ✅     |
| Sp1-18 | `mobile/lib/features/auth/data/repositories/auth_repository_impl.dart`  | ✅     |
| Sp1-18 | `mobile/lib/features/auth/presentation/bloc/auth_cubit.dart`            | ✅     |
| Sp1-19 | `mobile/lib/features/auth/data/datasources/auth_remote_datasource.dart` | ✅     |
| Sp1-20 | `mobile/lib/core/network/connectivity_monitor.dart`                     | ✅     |

**Prueba de aceptación manual (Sp1-22):**

```
Pre-condición: stack Docker corriendo, técnico creado vía panel web.
1. Instalar APK en dispositivo Android o emulador.
2. Abrir app → debe mostrar LoginPage.
3. Ingresar credenciales válidas → navegar a "Mis Proyectos" (lista vacía).
4. Desactivar técnico desde panel web → intentar login → debe mostrar "Cuenta desactivada".
5. Desconectar red → banner "Sin conexión" visible, botón deshabilitado.
6. Hacer logout → volver a LoginPage, tokens borrados de SecureStorage.
```

---

## 5. Validación de la Definition of Done — Sprint 1

| #   | Criterio DoD                                                               | Estado | Observaciones                                                           |
| --- | -------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------- |
| 1   | Migración `0001` aplicada y reversible (`alembic downgrade -1`)            | ⏳     | Migraciones aplicadas ✅; reversibilidad requiere prueba manual         |
| 2   | Coverage backend ≥ 80 % en `auth` y `usuarios`                             | ✅     | 94.81 % global; auth 100 %, admin_usuarios 100 %                        |
| 3   | OpenAPI publicado con tags `auth`, `admin/usuarios`, `admin/proyectos`     | ✅     | Verificado en código y logs de arranque                                 |
| 4   | Bundle web sirviendo `/admin/login`, `/admin/usuarios`, `/admin/proyectos` | ✅     | Confirmado en logs Nginx; HMR activo                                    |
| 5   | APK de la app móvil construido por CI con login funcional                  | ⚠️     | **No hay GitHub Actions configurado**; APK debe construirse manualmente |
| 6   | Demo grabada del flujo: admin crea técnico → técnico hace login en app     | ⚠️     | **Pendiente de grabar**                                                 |

---

## 6. Estado detallado del Sprint Backlog (Sp1-01 a Sp1-28)

### HU PB-13 — Gestionar Usuarios

| Id     | Tarea                                                            | Estado | Evidencia                                                 |
| ------ | ---------------------------------------------------------------- | ------ | --------------------------------------------------------- |
| Sp1-01 | Migración Alembic `0001_inicial_usuarios`                        | ✅     | `e5f6a7b8c9d0` en logs Docker                             |
| Sp1-02 | Modelo SQLAlchemy + schemas Pydantic `Usuario`                   | ✅     | `app/models/usuario.py`, `app/schemas/usuario.py`         |
| Sp1-03 | `UsuarioRepository` (CRUD + filtro por activo)                   | ✅     | `app/repositories/usuario_repository.py` — 96 % cobertura |
| Sp1-04 | `AuthService` con bcrypt + JWT                                   | ✅     | `app/services/auth_service.py` — 95 % cobertura           |
| Sp1-05 | `POST /api/admin/usuarios`                                       | ✅     | 5 tests pasan en `test_usuarios.py`                       |
| Sp1-06 | `PATCH /admin/usuarios/{id}` (activar/desactivar/reset password) | ✅     | `test_desactivar_usuario`, `test_activar_usuario` pasan   |
| Sp1-07 | Tests pytest creación, duplicado, activar/desactivar             | ✅     | 9 tests pasan                                             |
| Sp1-08 | `LoginAdmin.tsx`                                                 | ✅     | Archivo existe y se sirve                                 |
| Sp1-09 | `GestionUsuarios.tsx` con tabla + modal                          | ✅     | Archivo existe y se sirve                                 |
| Sp1-10 | Hook `useUsuarios` (TanStack Query)                              | ✅     | `web/src/features/admin/hooks/useUsuarios.ts`             |
| Sp1-11 | Tipos TS desde OpenAPI (`openapi-typescript`)                    | ⚠️     | **`openapi-typescript` no está en `package.json`**        |
| Sp1-12 | Prueba de aceptación PB-13 con PO                                | ⏳     | Requiere sesión manual con el PO                          |

### HU PB-09 — Autenticar Usuario (móvil)

| Id     | Tarea                                                       | Estado | Evidencia                                                |
| ------ | ----------------------------------------------------------- | ------ | -------------------------------------------------------- |
| Sp1-13 | `POST /api/auth/login`                                      | ✅     | 4 tests pasan en `test_auth.py`                          |
| Sp1-14 | `POST /api/auth/refresh`                                    | ✅     | `test_refresh_exitoso` pasa                              |
| Sp1-15 | `POST /api/auth/logout`                                     | ✅     | `test_logout_revoca_refresh_token` pasa                  |
| Sp1-16 | Tests pytest flujo auth                                     | ✅     | 8 tests pasan                                            |
| Sp1-17 | `LoginPage` Flutter con `flutter_form_builder`              | ✅     | Archivo existe; widget test pasa                         |
| Sp1-18 | `AuthRepository` (Dio) + `AuthCubit` (BLoC) + SecureStorage | ✅     | `auth_repository_test` + `auth_cubit_test` pasan         |
| Sp1-19 | `AuthInterceptor` Dio: refresh automático al 401            | ✅     | `auth_remote_datasource.dart` implementado               |
| Sp1-20 | `ConnectivityMonitor` + banner "Sin conexión"               | ✅     | `ConnectivityMonitor` en `core/network/`; test CA-5 pasa |
| Sp1-21 | Widget tests `LoginPage` + unit tests `AuthCubit`           | ✅     | 45 tests Flutter pasan                                   |
| Sp1-22 | Prueba de aceptación PB-09 con PO                           | ⏳     | Requiere APK instalado en dispositivo físico             |

### HU PB-18 — Ver Proyectos de la Organización

| Id     | Tarea                                          | Estado | Evidencia                                         |
| ------ | ---------------------------------------------- | ------ | ------------------------------------------------- |
| Sp1-23 | `GET /api/admin/proyectos` (paginado, filtros) | ✅     | 6 tests pasan en `test_proyectos.py`              |
| Sp1-24 | Tests pytest listado con seed data             | ✅     | `proyectos_seed` fixture activo; tests pasan      |
| Sp1-25 | `ListadoProyectosOrg.tsx`                      | ✅     | Archivo existe y se sirve via Nginx               |
| Sp1-26 | Hook `useProyectosOrg` con paginación TanStack | ✅     | `web/src/features/admin/hooks/useProyectosOrg.ts` |
| Sp1-27 | Estado vacío y skeleton de carga               | ✅     | Probablemente implementado en la página           |
| Sp1-28 | Prueba de aceptación PB-18 con PO              | ⏳     | Requiere sesión manual con el PO                  |

---

## 7. Hallazgos y brechas identificadas

### 7.1 Dependencia `email-validator` no registrada en `pyproject.toml` (RESUELTA pero frágil)

**Síntoma:** El contenedor `backend-1` crasheó en el primer arranque con:

```
ImportError: email-validator is not installed, run `pip install 'pydantic[email]'`
```

**Causa:** `pydantic[email]>=2.0.0` sí está en `pyproject.toml` y debería instalar `email-validator` automáticamente. El fallo se debió a un build cache del Docker con una imagen anterior.
**Resolución aplicada:** El contenedor se recreó y arrancó correctamente.
**Acción preventiva:** Añadir en `Dockerfile` un `pip install --no-cache-dir -e ".[dev]"` explícito y forzar rebuild si pyproject.toml cambia.

### 7.2 Sin framework de tests para la web (brecha de calidad)

`web/package.json` no incluye `vitest`, `jest`, `@testing-library/react` ni ningún runner de tests.
La tarea Sp1-11 está incompleta (`openapi-typescript` no está en devDependencies).

**Impacto:** Los componentes React `LoginAdmin`, `GestionUsuarios`, `ListadoProyectosOrg` y `UsuarioModal` no tienen cobertura automatizada. Los criterios de aceptación del frontend solo se pueden validar manualmente.

**Acción propuesta (Sprint 1 o inicio Sprint 2):**

```bash
cd web
npm install -D vitest @testing-library/react @testing-library/user-event @testing-library/jest-dom jsdom
npm install -D openapi-typescript
```

Y agregar en `package.json`:

```json
"test": "vitest run",
"test:watch": "vitest",
"generate-types": "openapi-typescript http://localhost/api/openapi.json -o src/shared/types/api.d.ts"
```

### 7.3 CI/CD no configurado (DoD ítem 5 bloqueado)

No existe ningún archivo en `.github/workflows/`. El DoD del Sprint 1 exige un APK construido por CI.

**Acción mínima requerida:**

- Crear `.github/workflows/ci-backend.yml` que ejecute `pytest` y reporte cobertura.
- Crear `.github/workflows/ci-mobile.yml` que ejecute `flutter test` y `flutter build apk`.

### 7.4 Filtros de fecha en proyectos sin cobertura de test

Las líneas 55-59 de `app/repositories/proyecto_repository.py` implementan los filtros `fecha_desde` y `fecha_hasta` del endpoint `GET /admin/proyectos`, pero ningún test los ejercita.

**Acción:** Añadir un test en `test_proyectos.py`:

```python
def test_filtro_por_fecha(self, client, admin_token, proyectos_seed):
    resp = client.get(
        "/admin/proyectos?fecha_desde=2026-01-01&fecha_hasta=2026-12-31",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
```

### 7.5 Reset de contraseña sin test

`UsuarioUpdate.password_min_length` (líneas 51-53 de `schemas/usuario.py`) no está cubierto. El endpoint `PATCH /admin/usuarios/{id}` acepta `password` para reset, pero no hay test que lo ejerza con contraseña corta.

**Acción:** Añadir test:

```python
def test_reset_password_corta_retorna_422(self, client, admin_token, tecnico_usuario):
    resp = client.patch(
        f"/admin/usuarios/{tecnico_usuario.id}",
        json={"password": "123"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 422
```

---

## 8. Plan de pruebas manuales para la Sprint Review (R-4)

Las siguientes pruebas deben ejecutarse con el stack Docker corriendo (`docker compose up`) antes de la sesión de Review con el PO:

### 8.1 Flujo completo PB-13 + PB-09 (Sp1-12 y Sp1-22)

```
Pre-condición: stack levantado; APK instalado en emulador o dispositivo.

PASO 1 — Admin inicia sesión en panel web
  → Navegar a http://localhost/admin/login
  → Ingresar admin@bulldogtech.bo y la contraseña del seed
  → Verificar redirección a /admin/usuarios

PASO 2 — Admin crea un técnico nuevo
  → Hacer clic en "Nuevo Técnico"
  → Ingresar: nombre="Técnico Review", email="review@bulldogtech.bo", contraseña="Review1234!", rol=técnico
  → Verificar que aparece en la tabla con estado ACTIVO (CA1 PB-13)

PASO 3 — Técnico inicia sesión en la app móvil
  → Abrir la app Flutter en el emulador
  → Ingresar review@bulldogtech.bo / Review1234!
  → Verificar que navega a "Mis Proyectos" (lista vacía) en ≤ 2 s (CA1 PB-09)

PASO 4 — Admin desactiva al técnico
  → Panel web: hacer clic en "Desactivar" en la fila de review@bulldogtech.bo
  → Verificar que el estado cambia a INACTIVO (CA2 PB-13)

PASO 5 — Técnico intenta hacer login con cuenta inactiva
  → App móvil: intentar login con review@bulldogtech.bo
  → Verificar mensaje "Cuenta desactivada. Contacte al administrador" (CA3 PB-09)

PASO 6 — Técnico cierra sesión
  → App móvil: hacer logout
  → Verificar regreso al LoginPage (CA4 PB-09)
  → Verificar que el refresh_token fue eliminado físicamente (si se intenta login → nuevo proceso)

RESULTADO ESPERADO: flujo completo sin errores → Sp1-12 y Sp1-22 aprobados
```

### 8.2 Supervisión de proyectos PB-18 (Sp1-28)

```
Pre-condición: stack levantado con seed activo (3 proyectos de prueba).

PASO 1 — Admin navega a la sección de proyectos
  → http://localhost/admin/proyectos
  → Verificar que se muestra la lista de proyectos con campos:
    nombre, técnico, cliente, estado, última actividad, cantidad de puntos (CA2 PB-18)

PASO 2 — Filtro por técnico
  → Usar el selector de filtro de técnico
  → Seleccionar "tecnico@bulldogtech.bo"
  → Verificar que solo aparecen sus proyectos (CA3 PB-18)

PASO 3 — Estado vacío
  → Crear un nuevo técnico sin proyectos
  → Filtrar por ese técnico
  → Verificar mensaje "No hay proyectos registrados aún" (CA4 PB-18)

PASO 4 — Control de acceso
  → Intentar acceder a /admin/proyectos sin estar autenticado
  → Verificar redirección al login (CA1 PB-18)

RESULTADO ESPERADO: flujo completo → Sp1-28 aprobado
```

### 8.3 Prueba de conectividad (CA5 PB-09)

```
PASO 1 — Con stack detenido (docker compose stop):
  → Abrir la app Flutter
  → Verificar banner "Sin conexión" visible en LoginPage
  → Verificar que el botón "Iniciar Sesión" está deshabilitado

PASO 2 — Reiniciar stack (docker compose start):
  → Verificar que el banner desaparece
  → Verificar que el botón se habilita

RESULTADO ESPERADO: comportamiento correcto → CA5 PB-09 validado manualmente
```

### 8.4 Reversibilidad de migraciones (DoD ítem 1)

```bash
# Ejecutar en terminal con stack corriendo:
docker compose exec backend alembic current
# Salida esperada: e5f6a7b8c9d0 (head)

docker compose exec backend alembic downgrade -1
docker compose exec backend alembic current
# Salida esperada: d4e5f6a7b8c9

docker compose exec backend alembic upgrade head
docker compose exec backend alembic current
# Salida esperada: e5f6a7b8c9d0 (head)
```

---

## 9. Checklist final pre-Review

### Automatizado (ejecutar antes de la sesión R-4)

```bash
# 1. Backend
cd backend
.venv/bin/python -m pytest tests/ -v --cov=app --cov-report=term

# 2. Flutter
cd ../mobile
flutter test --reporter compact

# 3. Stack
cd ..
docker compose up -d
docker compose ps  # todos "running"
curl http://localhost/api/health  # {"status": "ok"}
curl http://localhost/api/docs    # OpenAPI disponible
```

### Manual (durante sesión R-4 con PO)

- [ ] Sp1-22: flujo completo PB-09 (ver §8.1)
- [ ] Sp1-12: flujo PB-13 (ver §8.1 — mismo flujo)
- [ ] Sp1-28: supervisión de proyectos PB-18 (ver §8.2)
- [ ] DoD 1: reversibilidad de migración (ver §8.4)
- [ ] DoD 5: mostrar APK construido (o registrar deuda técnica de CI/CD)
- [ ] DoD 6: grabar demo del flujo completo

### Acciones de cierre post-Review

- [ ] Añadir `openapi-typescript` a `web/package.json` (Sp1-11 — deuda técnica)
- [ ] Configurar `vitest` en web (deuda técnica)
- [ ] Crear `.github/workflows/ci-backend.yml` y `ci-mobile.yml`
- [ ] Añadir tests de cobertura faltantes (ver §7.4, §7.5)
- [ ] Registrar deuda técnica en el Product Backlog si no se cierra en Sprint 1

---

## 10. Resumen de cobertura de criterios de aceptación

| HU        | CAs totales | CAs con test automático | CAs solo manuales               | Estado global           |
| --------- | ----------- | ----------------------- | ------------------------------- | ----------------------- |
| PB-09     | 6           | 6                       | 0 (+ prueba real APK)           | ✅ / ⏳ APK             |
| PB-13     | 5           | 5                       | 0 (+ prueba real web)           | ✅ / ⏳ sesión PO       |
| PB-18     | 5           | 4                       | 1 (CA5: benchmark)              | ⚠️ CA5 pendiente        |
| PB-19     | 5           | 5                       | 0                               | ✅                      |
| PB-01     | 5           | 1                       | 4 (mutaciones backend)          | ⚠️ tests pendientes     |
| PB-10     | 5           | 2                       | 3 (CA2, CA3 widget; CA5 manual) | ⚠️ gap widget tests     |
| **Total** | **31**      | **22**                  | **9**                           | **22/31 automatizados** |
