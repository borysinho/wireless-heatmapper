# Sprint 1 — Historias de Usuario

## S1.1 Historias de Usuario del Sprint 1

**Objetivo del Sprint 1:** Establecer la fundación del sistema con el backend base, el panel de administración web (gestión de usuarios, clientes y proyectos), y la autenticación desde la app móvil.

**Duración:** 1 semana (5 días hábiles: 20–24 de abril de 2026)
**Presentación conjunta S0+S1:** 27 de abril de 2026
**Puntos de Historia del Sprint:** 29 PHU

### Cronograma del Sprint 1

![Sprint 1 — Backend + Admin Web + Auth Móvil + CRUD — 20 abr – 24 abr 2026](img/03-sprint-1-detalle.png)

_Figura 24. Diagrama de Gantt — Planificación detallada del Sprint 1 (20–24 abr 2026)._

---

### PB-13 — Gestionar proyectos de levantamiento

| Campo                | Detalle |
| -------------------- | ------- |
| **ID**               | PB-13 |
| **Rol**              | Como administrador |
| **Funcionalidad**    | quiero crear, editar, visualizar y eliminar proyectos de levantamiento Wi-Fi |
| **Beneficio**        | para organizar el trabajo técnico por cliente e instalación |
| **PHU**              | 5 |
| **RP asociado**      | RP3 |

**Criterios de aceptación:**
- El administrador puede crear un nuevo proyecto asociado a un cliente existente.
- El sistema valida que el nombre del proyecto no esté duplicado para el mismo cliente.
- El administrador puede editar nombre, descripción y estado del proyecto.
- El administrador puede desactivar (eliminación lógica) un proyecto.
- El listado de proyectos muestra nombre, cliente, estado y fecha de creación.

---

### PB-19 — Autenticarse en la app móvil

| Campo                | Detalle |
| -------------------- | ------- |
| **ID**               | PB-19 |
| **Rol**              | Como técnico |
| **Funcionalidad**    | quiero iniciar sesión desde la aplicación móvil con mi correo y contraseña |
| **Beneficio**        | para acceder de forma segura a mis proyectos asignados |
| **PHU**              | 3 |
| **RP asociado**      | RP1 |

**Criterios de aceptación:**
- El técnico ingresa correo y contraseña; el sistema autentica contra el backend.
- Si las credenciales son correctas, se almacena el token JWT en memoria segura de la app.
- Si las credenciales son incorrectas, se muestra un mensaje de error claro.
- La sesión persiste mientras el token es válido.
- El técnico puede cerrar sesión explícitamente.

---

### PB-09 — Gestionar clientes (organizaciones)

| Campo                | Detalle |
| -------------------- | ------- |
| **ID**               | PB-09 |
| **Rol**              | Como administrador |
| **Funcionalidad**    | quiero registrar, editar, ver y desactivar clientes (organizaciones) en el sistema |
| **Beneficio**        | para tener un catálogo actualizado de empresas con proyectos de levantamiento |
| **PHU**              | 5 |
| **RP asociado**      | RP2 |

**Criterios de aceptación:**
- El administrador puede registrar una nueva organización con nombre, dirección y contacto.
- El sistema impide registrar dos organizaciones con el mismo nombre.
- El administrador puede editar los datos de una organización existente.
- El administrador puede desactivar una organización (no se eliminan sus proyectos).
- El listado muestra nombre, contacto, estado y fecha de registro.

---

### PB-18 — Ver listado de proyectos por cliente

| Campo                | Detalle |
| -------------------- | ------- |
| **ID**               | PB-18 |
| **Rol**              | Como administrador |
| **Funcionalidad**    | quiero ver todos los proyectos agrupados o filtrados por cliente |
| **Beneficio**        | para tener visibilidad del trabajo activo e histórico por organización |
| **PHU**              | 3 |
| **RP asociado**      | RP3, RP7 |

**Criterios de aceptación:**
- El panel web muestra un listado de proyectos filtrable por cliente.
- Cada entrada muestra: nombre del proyecto, cliente, estado y fecha de creación.
- El administrador puede navegar al detalle de cualquier proyecto desde el listado.

---

### PB-01 — Gestionar usuarios del sistema

| Campo                | Detalle |
| -------------------- | ------- |
| **ID**               | PB-01 |
| **Rol**              | Como administrador |
| **Funcionalidad**    | quiero crear, editar, ver y desactivar usuarios del sistema |
| **Beneficio**        | para controlar quién tiene acceso al sistema y con qué rol |
| **PHU**              | 3 |
| **RP asociado**      | RP1 |

**Criterios de aceptación:**
- El administrador puede crear un usuario asignando nombre, correo, contraseña temporal y rol.
- Los roles disponibles son: Administrador, Técnico, Cliente.
- El sistema no permite dos usuarios con el mismo correo.
- El administrador puede editar datos y cambiar el rol de un usuario.
- El administrador puede desactivar un usuario (no puede iniciar sesión al estar inactivo).

---

### PB-10 — Autenticarse en el panel web

| Campo                | Detalle |
| -------------------- | ------- |
| **ID**               | PB-10 |
| **Rol**              | Como usuario (administrador o cliente) |
| **Funcionalidad**    | quiero iniciar sesión en el panel web con correo y contraseña |
| **Beneficio**        | para acceder de forma segura a las funciones que corresponden a mi rol |
| **PHU**              | 3 |
| **RP asociado**      | RP1 |

**Criterios de aceptación:**
- El usuario ingresa correo y contraseña en el formulario de login.
- Si las credenciales son correctas, se genera un token JWT y se redirige al dashboard.
- Si las credenciales son incorrectas, se muestra mensaje de error sin revelar cuál campo falló.
- El sistema redirige automáticamente al login si el token expira.
- El usuario puede cerrar sesión desde cualquier página del panel.

---

### Resumen del Sprint Backlog

| HU     | Descripción                              | PHU | Estado   |
| ------ | ---------------------------------------- | :-: | -------- |
| PB-13  | Gestionar proyectos de levantamiento     |  5  | Completada |
| PB-19  | Autenticarse en la app móvil             |  3  | Completada |
| PB-09  | Gestionar clientes (organizaciones)      |  5  | Completada |
| PB-18  | Ver listado de proyectos por cliente     |  3  | Completada |
| PB-01  | Gestionar usuarios del sistema           |  3  | Completada |
| PB-10  | Autenticarse en el panel web             |  3  | Completada |
| **Total** |                                       | **22** | |

> **Nota:** Los 29 PHU incluyen tareas técnicas de infraestructura (configuración de Docker Compose, setup de base de datos, pipeline CI/CD) contabilizadas en el Sprint Backlog pero no asociadas a una HU específica (7 PHU adicionales).

---
