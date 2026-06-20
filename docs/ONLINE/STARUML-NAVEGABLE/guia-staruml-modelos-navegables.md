# Guía — Modelos Navegables en StarUML 7.1

## Wireless HeatMapper · Sprint 0 + Sprint 1

**Basado en:** `docs/ONLINE/PRESENTACION/presentacion-scrum-s0-s1.md`  
**Herramienta:** StarUML 7.1  
**Fecha:** abril 2026

---

## Tabla de Contenido

1. [Conceptos clave para navegabilidad](#1-conceptos-clave-para-navegabilidad)
2. [Inventario de diagramas](#2-inventario-de-diagramas)
3. [Estructura del proyecto StarUML](#3-estructura-del-proyecto-staruml)
4. [Paso a paso — Crear el proyecto](#4-paso-a-paso--crear-el-proyecto)
5. [Crear cada modelo y sus diagramas](#5-crear-cada-modelo-y-sus-diagramas)
6. [Hacer los diagramas navegables (Sub-diagramas)](#6-hacer-los-diagramas-navegables-sub-diagramas)
7. [Paleta de colores y estilo](#7-paleta-de-colores-y-estilo)
8. [Tabla de referencia rápida](#8-tabla-de-referencia-rápida)

---

## 1. Conceptos clave para navegabilidad

### Modelo vs Vista (Model vs View)

En StarUML un **Model Element** (modelo) es la entidad con datos (nombre, tipo, atributos). Una **View Element** (vista) es la representación visual en un diagrama. El mismo modelo puede aparecer en varios diagramas sin duplicar información — si cambia el nombre en el modelo, todos los diagramas se actualizan solos.

> **Regla práctica:** Crear el elemento una sola vez en el Model Explorer; arrastrarlo a los distintos diagramas para crear las vistas adicionales.

### Sub-diagramas (el mecanismo de navegación)

Un Sub-diagrama es un diagrama anidado **dentro de un elemento del modelo** (paquete, clase, caso de uso, nodo de despliegue, etc.). Esto crea una jerarquía navegable:

```
Diagrama de nivel alto
  └── Elemento (clic derecho → Open Sub-Diagram)
        └── Diagrama de detalle
              └── Elemento de detalle (clic derecho → Open Sub-Diagram)
                    └── Diagrama más detallado
```

**Atajos de navegación en StarUML 7.1:**

| Acción                                       | Atajo          |
| -------------------------------------------- | -------------- |
| Abrir sub-diagrama del elemento seleccionado | `Ctrl+Shift+D` |
| Seleccionar elemento en el Model Explorer    | `Ctrl+E`       |
| Abrir diagrama desde el Model Explorer       | Doble clic     |
| Ir al diagrama siguiente (Working Diagrams)  | `Ctrl+Shift+]` |
| Ir al diagrama anterior                      | `Ctrl+Shift+[` |
| Cerrar diagrama activo                       | `F4`           |

### Plantilla recomendada

Al crear el proyecto seleccionar: **File → New From Template → UMLConventional**

Esto genera los modelos base: Use-Case Model, Analysis Model, Design Model, Implementation Model, Deployment Model. Se usarán como contenedores de los diagramas del proyecto.

---

## 2. Inventario de diagramas

Los siguientes diagramas están definidos en el documento de presentación. La columna **Tipo StarUML** indica el diagrama equivalente a crear.

| #   | Sección en doc | Nombre del diagrama                          | Tipo PlantUML     | Tipo StarUML            | Modelo StarUML sugerido |
| --- | -------------- | -------------------------------------------- | ----------------- | ----------------------- | ----------------------- |
| 1   | §1             | Ciclo de Vida Scrum                          | Activity          | Activity Diagram        | Analysis Model          |
| 2   | §2             | Equipo Scrum                                 | Class             | Class Diagram           | Analysis Model          |
| 3   | §3.3           | Sprint 0 — Actividades de Definición Inicial | Activity          | Activity Diagram        | Analysis Model          |
| 4   | §4.2           | Estado de las HU en el Product Backlog       | StateMachine      | Statechart Diagram      | Analysis Model          |
| 5   | §5             | HU del Sprint 1 (relaciones entre HU)        | UseCase           | Use Case Diagram        | Use-Case Model          |
| 6   | §8.1           | Login del Técnico — extremo a extremo        | Sequence          | Sequence Diagram        | Design Model            |
| 7   | §8.2           | Navegación App Móvil Flutter (Sprint 1)      | Activity          | Activity Diagram        | Implementation Model    |
| 8   | §9.1           | Modelo de Contexto — Casos de Uso            | UseCase           | Use Case Diagram        | Use-Case Model          |
| 9   | §9.2           | Arquitectura — Diagrama de Paquetes          | Package/Component | Package Diagram         | Implementation Model    |
| 10  | §9.2.b         | Arquitectura — Diagrama de Despliegue        | Deployment        | Deployment Diagram      | Deployment Model        |
| 11  | §9.3           | Modelo de Datos — Clases (Sprint 1)          | Class             | Class Diagram           | Design Model            |
| 12  | §9.3.b         | Modelo Lógico — Esquema Relacional           | Class (Tabla)     | Class Diagram (ERD)     | Design Model            |
| 13  | §9.3.c         | Diseño Físico — Tablas PostgreSQL            | (sin PlantUML)    | Nota / Referencia†      | Design Model            |
| 14  | §9.4           | Plan de Sprints — Gantt                      | Gantt (no UML)    | Nota libre / se omite\* | —                       |
| 15  | §9.5           | Crear Proyecto de Survey (PB-01)             | Sequence          | Sequence Diagram        | Design Model            |

> \* El Gantt de PlantUML no tiene equivalente UML estándar en StarUML. Se puede representar como nota de texto o imagen embebida en el documento. Opción alternativa: usar la extensión **Gantt Chart** si está disponible en el registry de StarUML.

> † El §9.3.c es documentación de referencia (tablas Markdown) del esquema físico PostgreSQL. En StarUML se representa como una **Note** adjunta al diagrama 12, o como un comentario HTML en el campo `documentation` de cada clase `<<Table>>`.

---

## 3. Estructura del proyecto StarUML

El archivo se guardará como `WirelessHeatMapper.mdj`. La plantilla UMLConventional genera **5 modelos**. Su correspondencia con los modelos obligatorios del docente (clase 21-04-2026 y EnfoqueScrumV3) es:

| Modelo StarUML           | Corresponde a (docente)                              | Diagramas asignados |
| ------------------------ | ---------------------------------------------------- | ------------------- |
| **Use-Case Model**       | Modelo de Contexto                                   | #5, #8              |
| **Analysis Model**       | Marco Scrum / proceso (no es un modelo del producto) | #1, #2, #3, #4      |
| **Design Model**         | Modelo de Datos + Modelo de Lógica                   | #6, #11, #12, #15   |
| **Implementation Model** | Modelo de Arquitectura — _estructura del código_     | #7, #9              |
| **Deployment Model**     | Modelo de Arquitectura — _despliegue físico_         | #10                 |

> **¿Por qué el Implementation Model contiene el diagrama de paquetes?**  
> La clase del 21-04-2026 (§8.1.a) define el _Diagrama de Paquetes_ como instrumento para mostrar "la organización y estructura del software a nivel de módulos/paquetes". En UML 4+1, el **Implementation Model** es el contenedor estándar para diagramas que representan _cómo está organizado el código fuente_ (paquetes, capas, módulos de las tres plataformas). El **Deployment Model** cubre la parte física (nodos Docker, protocolos de red). Ambos juntos cubren el "Modelo de Arquitectura" del docente. El **Design Model** queda reservado para el diseño lógico: clases, esquema relacional y diagramas de secuencia.

La jerarquía en el **Model Explorer** es:

```
WirelessHeatMapper  (Project)
│
├── Use-Case Model                                    ← Actores y casos de uso
│   ├── «actor» TecnicoDeCampo
│   ├── «actor» Administrador
│   ├── «actor» ClienteStakeholder
│   ├── «actor» AndroidWifiManagerAPI
│   ├── «actor» ServicioIA
│   ├── UC01 Gestionar Proyecto de Survey
│   │     └── 📊 §9.5 PB-01 — Crear Proyecto de Survey (secuencia)       [#15 — Sequence Diagram]
│   ├── UC02 Importar Plano (subida al backend)
│   ├── UC03 Calibrar Escala del Plano
│   ├── UC04 Marcar Punto de Medición
│   ├── UC05 Capturar Señales WiFi (envío en línea)
│   ├── UC06 Generar Mapa de Calor (interpolación en backend)
│   ├── UC07 Analizar Cobertura (zonas muertas, CCI/ACI)
│   ├── UC08 Obtener Recomendaciones de APs (IA)
│   ├── UC09 Comparar Escenario Actual vs Propuesto
│   ├── UC10 Exportar Reporte Técnico (PDF)
│   ├── UC11 Autenticar Usuario
│   │     └── 📊 §8.1 PB-09 — Login del Técnico (secuencia extremo a extremo)  [#6 — Sequence Diagram]
│   ├── UC12 Ver Historial de Proyectos
│   ├── UC13 Gestionar Usuarios (Admin Web)
│   ├── UC15 Generar Enlace de Cliente
│   ├── UC16 Ver Heatmap Interactivo (Web)
│   ├── UC17 Ver Análisis y Plan AP (Web)
│   ├── UC18 Ver Proyectos de la Organización
│   ├── UC19 Gestionar Clientes (Admin Web)
│   ├── Package: Sprint1-HU                          ← HU del Sprint 1
│   │   ├── «usecase» PB-01 Gestionar Proyecto (móvil — CRUD)         [traza → UC01]
│   │   ├── «usecase» PB-09 Autenticar Usuario (móvil contra backend)  [traza → UC11]
│   │   ├── «usecase» PB-10 Ver Historial de Proyectos                 [traza → UC12]
│   │   ├── «usecase» PB-13 Gestionar Usuarios (panel web)             [traza → UC13]
│   │   ├── «usecase» PB-18 Ver Proyectos de la Organización           [traza → UC18]
│   │   ├── «usecase» PB-19 Gestionar Clientes (panel web)             [traza → UC19]
│   │   └── 📊 §5   HU del Sprint 1 (relaciones entre HU)  [#5 — Use Case Diagram]
│   └── 📊 §9.1 Modelo de Contexto — Casos de Uso          [#8 — Use Case Diagram]
│
├── Analysis Model                                    ← Marco de trabajo Scrum (proceso, no producto)
│   ├── Package: ProcesoScrum
│   │   ├── «class» EquipoScrum
│   │   ├── «class» ScrumMaster
│   │   ├── «class» ProductOwner
│   │   ├── «class» Desarrollador
│   │   ├── 📊 §1   Ciclo de Vida Scrum                [#1 — Activity Diagram]
│   │   ├── 📊 §2   Equipo Scrum                       [#2 — Class Diagram]
│   │   └── 📊 §3.3 Sprint 0 — Actividades de Definición Inicial  [#3 — Activity Diagram]
│   └── Package: ProductBacklog
│       ├── «state» Pendiente de Estimación
│       ├── «state» Estimada y Priorizada
│       ├── «state» Seleccionada para Sprint
│       ├── «state» En Desarrollo
│       ├── «state» Done
│       ├── «state» Regresada
│       ├── «state» Eliminada / No aplica
│       └── 📊 §4.2 Estado de las HU en el Product Backlog        [#4 — Statechart Diagram]
│
├── Design Model                                      ← Diseño lógico: clases de dominio
│   ├── «enumeration» RolUsuario  {ADMIN, TECNICO}
│   ├── «enumeration» EstadoProyecto  {NUEVO, EN_PROGRESO, COMPLETADO, ARCHIVADO}
│   ├── «class» Usuario
│   ├── «class» RefreshToken  
│   ├── «class» Cliente
│   ├── «class» Proyecto
│   └── 📊 §9.3   Modelo de Datos — Sprint 1 (entidades implementadas)  [#11 — Class Diagram]
│         └── 📊 §9.3.b Modelo Lógico (Esquema Relacional) — Sprint 1   [#12 — Class Diagram ERD]
│
├── Implementation Model                              ← Arquitectura: organización del código fuente
│   ├── Package: AppMovil-Flutter
│   │   ├── Package: presentation
│   │   ├── Package: domain
│   │   ├── Package: data
│   │   └── 📊 §8.2 Diseño de navegación — App Móvil Flutter (Sprint 1)  [#7 — Activity Diagram]
│   ├── Package: Backend-FastAPI
│   │   ├── Package: api
│   │   ├── Package: services
│   │   ├── Package: ai
│   │   ├── Package: repositories
│   │   ├── Package: models
│   │   └── 📊 §9.3 Modelo de Datos — Sprint 1 (sub-diagrama de clases)  [#11 — Class Diagram]
│   ├── Package: Web-React
│   │   ├── Package: panel-admin
│   │   └── Package: shared
│   └── 📊 §9.2 Arquitectura — Diagrama de Paquetes (UML 2.5)             [#9 — Package Diagram]
│
└── Deployment Model                                  ← Arquitectura: despliegue físico (nodos Docker)
    ├── «artifact» nginx.conf
    ├── «artifact» dist/
    ├── «artifact» app/
    ├── «artifact» alembic/
    ├── «artifact» heatmapper.apk
    ├── «node» ServidorProduccion (Linux / VPS)
    │   ├── «node» Contenedor: nginx
    │   ├── «node» Contenedor: web
    │   ├── «node» Contenedor: backend
    │   └── «node» Contenedor: db
    ├── «node» Dispositivo Móvil Android
    ├── «node» Navegador Web
    ├── «node» Servicio CI/CD (GitHub Actions)
    └── 📊 §9.2.b Arquitectura — Diagrama de Despliegue (Docker Compose + Nginx)  [#10 — Deployment Diagram]
```

---

## 4. Paso a paso — Crear el proyecto

### 4.1 Crear el proyecto desde plantilla

1. Abrir StarUML 7.1.
2. Seleccionar **File → New From Template → UMLConventional**.
3. Se crean automáticamente: _Use-Case Model_, _Analysis Model_, _Design Model_, _Implementation Model_, _Deployment Model_.
4. Guardar con **Ctrl+Shift+S** como `WirelessHeatMapper.mdj`.

### 4.2 Renombrar y limpiar modelos

En el **Model Explorer** (panel izquierdo):

1. Clic derecho sobre el nodo raíz del proyecto → **Rename** → `WirelessHeatMapper`.
2. En _Analysis Model_: clic derecho → **Add → Package** → nombrar `ProcesoScrum`.
3. En _Analysis Model_: clic derecho → **Add → Package** → nombrar `ProductBacklog`.
4. En _Implementation Model_: clic derecho → **Add → Package** → nombrar `AppMovil-Flutter`.
5. Repetir dentro de _Implementation Model_ para `Backend-FastAPI` y `Web-React`.

> **No eliminar el Implementation Model.** Contiene los diagramas de la estructura de código del proyecto (ver tabla de correspondencia en §3).

---

## 5. Crear cada modelo y sus diagramas

### Diagrama 1 — Ciclo de Vida Scrum (Activity Diagram)

**Ubicación:** `Analysis Model / ProcesoScrum`

**Pasos:**

1. En Model Explorer, seleccionar `ProcesoScrum`.
2. **Model → Add Diagram → UML Activity Diagram**.
3. Renombrar a `Ciclo de Vida Scrum`.
4. En la Toolbox usar: **InitialNode**, **ActivityNode** (para los estados), **ForkNode** / **JoinNode** (para la bifurcación condicional), **DecisionNode**, **FinalNode**.
5. Crear los nodos de actividad principales:
   - `[R-1] Sprint 0 — Definición Inicial`
   - `[R-2] Sprint Planning`
   - `[R-3] Ejecución del Sprint`
   - `Generar Incremento`
   - `[R-4] Sprint Review`
   - `[R-5] Sprint Retrospective`
6. Conectar con **ControlFlow** (`→`).
7. Para el ciclo `while (¿Quedan Sprints?)`: usar un **DecisionNode** con guardas `[Sí]` y `[No]`.

> **Sub-diagrama navegable:** Hacer clic derecho sobre el nodo `[R-3] Ejecución del Sprint` → **Add → UML Activity Diagram** → nombrar `R-3 Detalle Ejecución`. Esto permite navegar con `Ctrl+Shift+D` al detalle.

---

### Diagrama 2 — Equipo Scrum (Class Diagram)

**Ubicación:** `Analysis Model / ProcesoScrum`

**Pasos:**

1. Seleccionar `ProcesoScrum` en Model Explorer.
2. **Model → Add Diagram → UML Class Diagram** → renombrar `Equipo Scrum`.
3. Agregar clases con la Toolbox → **Class**:
   - `EquipoScrum` con atributos: `tamaño: Integer = 2`, `modalidad: String`, `duracionSprint: String`
   - `ScrumMaster` con operaciones: `facilitar()`, `removerImpedimentos()`
   - `ProductOwner` con operaciones: `gestionarBacklog()`, `validarConCliente()`
   - `Desarrollador` con atributos: `autogestionado: Boolean`, `multifuncional: Boolean`
4. Agregar relaciones con Toolbox:
   - `EquipoScrum` → `ScrumMaster`: **Association** (composición `*--`)
   - `EquipoScrum` → `ProductOwner`: **Association** (composición)
   - `EquipoScrum` → `Desarrollador`: **Association** (multiplicidad `2`)
   - `ScrumMaster` → `Desarrollador`: **Generalization** (`--|>`)
   - `ProductOwner` → `Desarrollador`: **Generalization**
5. Agregar nota (Toolbox → **Note**) + **NoteLink** al elemento `Desarrollador`.

---

### Diagrama 3 — Sprint 0 Actividades (Activity Diagram)

**Ubicación:** `Analysis Model / ProcesoScrum`

**Pasos:**

1. Seleccionar `ProcesoScrum` → **Model → Add Diagram → UML Activity Diagram** → `Sprint 0 - Actividades`.
2. Seguir la misma lógica que el Diagrama 1.
3. Usar **ForkNode** / **JoinNode** para los bloques `fork…end fork` del PlantUML:
   - Primer fork: Modelo de Contexto / Modelo de Arquitectura / Modelo de Datos (paralelo).
   - Segundo fork: Backend FastAPI / App Móvil / Web React / Nginx+Docker (paralelo).

> **Sub-diagrama navegable:** Clic derecho en el nodo `Configurar repositorio GitHub (monorepo)` → **Add → UML Activity Diagram** → `Sp0-07 Detalle`. Útil para mostrar el monorepo `backend/`, `mobile/`, `web/`.

---

### Diagrama 4 — Estados de HU en el Product Backlog (Statechart Diagram)

**Ubicación:** `Analysis Model / ProductBacklog`

**Pasos:**

1. Seleccionar `ProductBacklog` → **Model → Add Diagram → UML Statechart Diagram** → `Estados del Product Backlog`.
2. Usar Toolbox → **State** para cada estado:
   - `Pendiente de Estimación`
   - `Estimada y Priorizada`
   - `Seleccionada para Sprint`
   - `En Desarrollo`
   - `Done`
   - `Regresada`
   - `Eliminada / No aplica`
3. Usar Toolbox → **InitialPseudostate** (punto negro inicial).
4. Conectar con **Transition** (flechas) y completar la propiedad `guard` en el panel de propiedades con los textos de guardia (ej: `Planning Poker`, `R-2 Sprint Planning`).

---

### Diagrama 5 — HU del Sprint 1 (Use Case Diagram)

**Ubicación:** `Use-Case Model`

**Pasos:**

1. Seleccionar `Use-Case Model` → **Model → Add Diagram → UML Use Case Diagram** → `HU Sprint 1`.
2. Desde Toolbox agregar **Actor** (2 actores): `Administrador`, `Técnico de Campo`.
3. Agregar **UseCase** (6 casos de uso): `PB-13`, `PB-19`, `PB-09`, `PB-18`, `PB-01`, `PB-10`.
4. Conectar actores con sus casos de uso usando **Association** (línea simple actor→UC).
5. Para las relaciones entre UC (prerrequisitos):
   - Toolbox → **Dependency** o **Include/Extend** (según aplique).
   - Toolbox → **Include** para `<<include>>`; Toolbox → **Extend** para `<<extend>>`.
6. Agregar **Note** al caso de uso `PB-13` indicando `Sin cuentas pre-aprovisionadas...`.

> **Sub-diagrama navegable:** Clic derecho sobre el UC `PB-09 Autenticar Usuario` → **Add → UML Sequence Diagram** → `PB-09 Login Secuencia`. Esto conecta directamente el caso de uso con su diagrama de secuencia (Diagrama 6).

---

### Diagrama 6 — Login Extremo a Extremo (Sequence Diagram)

**Ubicación:** Sub-diagrama de `UC11 Autenticar Usuario` en `Use-Case Model`  
_(también accesible desde `Design Model`)_

**Pasos:**

1. Seleccionar el elemento `UC11 Autenticar Usuario` en Model Explorer.
2. **Model → Add Diagram → UML Sequence Diagram** → `PB-09 Login del Técnico`.
3. En la Toolbox agregar **Lifeline** (columnas) para cada participante:
   - `Técnico`, `App Móvil (LoginPage)`, `ApiClient (Dio+JWT)`, `Nginx`, `Backend (/api/auth/login)`, `PostgreSQL`, `SecureStorage`
4. Agregar mensajes con Toolbox → **Message** (flecha horizontal sólida para sincrónico):
   - `ingresa email + contraseña`
   - `POST /api/auth/login`
   - etc.
5. Para el bloque `alt`: Toolbox → **CombinedFragment** → propiedad `interactionOperator = alt`.
   - Crear dos operandos: `credenciales válidas y usuario activo` / `credenciales inválidas`.

---

### Diagrama 7 — Navegación App Móvil Flutter (Activity Diagram)

**Ubicación:** `Implementation Model / AppMovil-Flutter`

**Pasos:**

1. Seleccionar `AppMovil-Flutter` → **Add Diagram → UML Activity Diagram** → `Navegación App Móvil Sprint 1`.
2. Crear actividades: `Splash`, `LoginPage`, `ProyectosPage`, `ProyectoFormPage`.
3. Usar **DecisionNode** para cada bifurcación condicional (`¿token válido?`, `¿credenciales OK?`, `¿acción del usuario?`).
4. Etiquetar las guardas en cada **ControlFlow** (propiedad `guard`).

---

### Diagrama 8 — Modelo de Contexto (Use Case Diagram)

**Ubicación:** `Use-Case Model`

**Pasos:**

1. Seleccionar `Use-Case Model` → **Add Diagram → UML Use Case Diagram** → `Modelo de Contexto`.
2. Agregar **Actor** para cada actor del diagrama:
   - `Técnico de Campo`, `Administrador (Bulldog Tech.)`, `Cliente / Stakeholder`, `Android WifiManager API`, `Servicio IA (backend)`
3. Agregar **UseCase** (UC01 a UC19, sin UC14):
   - Arrastrar desde Model Explorer si ya existen los elementos; de lo contrario, crearlos desde Toolbox.
4. Usar Toolbox → **SystemBoundary** para el rectángulo del sistema.
5. Conectar actores y casos de uso con **Association**.
6. Agregar relaciones entre UC con **Include** o **Dependency** según corresponda.
7. Agregar **Note** a UC13 y UC19 indicando `Sprint 1 — implementado ✅`.

> **Sub-diagrama navegable:** Clic derecho sobre el UC `UC09 Comparar Escenario` → **Add → UML Sequence Diagram** → `UC09 Comparación Escenario Detalle`. Hacer lo mismo para los UCs más complejos (UC05, UC06, UC07, UC08).

---

### Diagrama 9 — Arquitectura de Paquetes (Package Diagram / Component Diagram)

**Ubicación:** `Implementation Model`

**Pasos:**

1. Seleccionar `Design Model` → **Add Diagram → UML Package Diagram** → `Arquitectura de Paquetes`.
2. Agregar **Package** para cada capa:
   - `App Móvil — Flutter / Dart`
   - `Plataforma Web — React + TypeScript + Vite`
   - `Backend — FastAPI / Python`
3. Dentro de cada **Package** agregar sub-paquetes con Toolbox → **Package**:
   - App Móvil: `presentation`, `domain`, `data`
   - Web: `panel-admin`, `shared`
   - Backend: `api`, `services`, `repositories`, `models`
4. Dentro de cada sub-paquete agregar **Component** para los módulos individuales.
5. Agregar nodos adicionales: **Database** (`PostgreSQL 15`), **Node** (`Nginx`).
6. Conectar con **Dependency** (flecha punteada) los flujos de datos.

> **Sub-diagrama navegable:** Clic derecho sobre el Package `App Móvil` → **Add → UML Activity Diagram** → navega al Diagrama 7. Clic derecho sobre el Package `Backend-FastAPI` → **Add → UML Class Diagram** → navega al Diagrama 11.

---

### Diagrama 10 — Despliegue (Deployment Diagram)

**Ubicación:** `Deployment Model`

**Pasos:**

1. Seleccionar `Deployment Model` → **Add Diagram → UML Deployment Diagram** → `Diagrama de Despliegue`.
2. Usar Toolbox → **Node** para cada nodo:
   - `Servidor de Producción (Linux / VPS)` — nodo contenedor
   - Dentro: `Contenedor: nginx`, `Contenedor: web`, `Contenedor: backend`, `Contenedor: db`
   - Exteriores: `Dispositivo Móvil Android`, `Navegador Web`, `Servicio CI/CD`
3. Para nodos dentro de nodos: seleccionar el nodo padre → arrastrar nuevo nodo dentro de él.
4. Usar Toolbox → **Artifact** para los artefactos: `nginx.conf`, `dist/`, `app/`, `alembic/`, `heatmapper.apk`.
5. Conectar nodos con **CommunicationPath** (línea con estereotipo): indicar el protocolo en la propiedad `name` (ej: `HTTPS :443`).
6. Agregar **Note** a los nodos clave (`Dispositivo Móvil Android`, `Contenedor: db`).

---

### Diagrama 11 — Modelo de Datos Sprint 1 (Class Diagram)

**Ubicación:** `Design Model`

**Pasos:**

1. Seleccionar `Design Model` → **Add Diagram → UML Class Diagram** → `Modelo de Datos — Sprint 1`.
2. Agregar **Enumeration** (Toolbox → Enumeration):
   - `RolUsuario` con literales: `ADMIN`, `TECNICO`
   - `EstadoProyecto` con literales: `NUEVO`, `EN_PROGRESO`, `COMPLETADO`, `ARCHIVADO`
3. Agregar **Class** para cada entidad:
   - `Usuario` con atributos: `id: Long`, `email: String`, `passwordHash: String`, etc.
   - `RefreshToken` con atributos: `id: Long`, `token: String`, `expiresAt: DateTime`, `revocado: Boolean`
   - `Cliente` con atributos: `id: Long`, `nombre: String`, `activo: Boolean`, `fechaCreacion: DateTime`
   - `Proyecto` con atributos: `id: Long`, `nombre: String`, `descripcion: String`, `estado: EstadoProyecto`, etc.
4. Agregar relaciones con Toolbox → **Association**:
   - `Usuario` `1` → `0..*` `RefreshToken` (composición: tiene >)
   - `Usuario` `1` → `0..*` `Proyecto` (asociación: gestiona >)
   - `Cliente` `1` → `0..*` `Proyecto` (asociación: tiene >)
5. En cada asociación, configurar las multiplicidades en el Property Editor.
6. Agregar **Note** a `RefreshToken` y a `Proyecto`.

> **Sub-diagrama navegable:** Clic derecho sobre la clase `Usuario` o sobre el diagrama raíz → **Add → UML Class Diagram** → `Esquema Relacional Sprint 1` → navega al Diagrama 12.

---

### Diagrama 12 — Modelo Lógico / Esquema Relacional (Class Diagram ERD)

**Ubicación:** Sub-diagrama del Diagrama 11 (`Design Model`)
**Sección de referencia:** §9.3.b del documento de presentación

**Pasos:**

1. Con el Diagrama 11 abierto, hacer clic derecho sobre el área del diagrama (o sobre la clase `Usuario` como ancla) → **Add → UML Class Diagram** → renombrar `Modelo Lógico — Esquema Relacional Sprint 1`.
2. Agregar **Class** con estereotipo `<<Table>>` para cada tabla:
   - `usuario` con columnas: `PK id: BIGSERIAL`, `email: VARCHAR(255) UNIQUE NOT NULL`, `password_hash: VARCHAR(255) NOT NULL`, `nombre_completo: VARCHAR(255) NOT NULL`, `rol: rol_usuario NOT NULL`, `activo: BOOLEAN DEFAULT TRUE`, `fecha_creacion: TIMESTAMPTZ`, `ultimo_acceso: TIMESTAMPTZ`
   - `refresh_token` con columnas: `PK id: BIGSERIAL`, `token: VARCHAR(512) UNIQUE NOT NULL`, `expires_at: TIMESTAMPTZ NOT NULL`, `revocado: BOOLEAN DEFAULT FALSE`, `FK usuario_id: BIGINT NOT NULL`
   - `cliente` con columnas: `PK id: BIGSERIAL`, `nombre: VARCHAR(255) UNIQUE NOT NULL`, `activo: BOOLEAN DEFAULT TRUE`, `fecha_creacion: TIMESTAMPTZ`
   - `proyecto` con columnas: `PK id: BIGSERIAL`, `nombre: VARCHAR(255) NOT NULL`, `descripcion: TEXT`, `fecha_creacion: TIMESTAMPTZ`, `fecha_ultima_actividad: TIMESTAMPTZ`, `estado: estado_proyecto DEFAULT 'en_progreso'`, `FK tecnico_id: BIGINT NOT NULL`, `FK cliente_id: BIGINT NOT NULL`
3. Para asignar el estereotipo `<<Table>>` a cada clase:
   - Seleccionar la clase → en el Property Editor, campo `stereotype` → escribir `Table`.
4. Separar visualmente los atributos PK y FK del resto con una línea divisoria (`--`): agregar el texto `--` como el primer atributo de la sección de FKs en el nombre del atributo, o usar una **Constraint** de StarUML para resaltar la clave primaria.
5. Conectar las tablas con **Association** (dirección FK → PK):
   - `refresh_token.usuario_id` → `usuario.id` (rol del extremo: `usuario_id`)
   - `proyecto.tecnico_id` → `usuario.id`
   - `proyecto.cliente_id` → `cliente.id`
6. En el Property Editor de cada asociación, escribir el nombre del campo FK en la propiedad `name` del extremo origen.

> **Diferencia con el Diagrama 11:** El Diagrama 11 usa tipos de dominio (`String`, `Long`, `Boolean`) y refleja el modelo ORM (Python/SQLAlchemy). El Diagrama 12 usa tipos PostgreSQL (`VARCHAR`, `BIGSERIAL`, `TIMESTAMPTZ`) y refleja el esquema físico de la BD. Mantener ambos para mostrar la trazabilidad ORM → SQL.

> **Diseño Físico (§9.3.c):** El §9.3.c del documento de presentación contiene las tablas Markdown con restricciones detalladas (`ON DELETE CASCADE`, índices, etc.). En StarUML agregar esta información en el campo `documentation` de cada clase `<<Table>>` (clic sobre la clase → panel Documentation en la parte inferior).

---

### Diagrama 13 — Plan de Sprints Gantt _(referencia)_

> El `@startgantt` de PlantUML no tiene representación UML nativa en StarUML. Opciones:
>
> - Incluirlo como imagen exportada desde PlantUML embebida en una **Note** del modelo.
> - Usar la extensión **Gantt Chart** del Extension Registry de StarUML si está disponible.
> - Referenciar el archivo PlantUML original desde el campo `documentation` del nodo raíz del proyecto.

---

### Diagrama 14 — Crear Proyecto de Survey — PB-01 (Sequence Diagram)

**Ubicación:** Sub-diagrama de `UC01 Gestionar Proyecto de Survey` en `Use-Case Model`  
_(también accesible desde `Design Model`)_
**Sección de referencia:** §9.5 del documento de presentación

**Pasos:**

1. Seleccionar el elemento `UC01 Gestionar Proyecto de Survey` en Model Explorer.
2. **Model → Add Diagram → UML Sequence Diagram** → renombrar `PB-01 Crear Proyecto de Survey`.
3. En la Toolbox agregar **Lifeline** para cada participante:
   - `Técnico`, `App Móvil (ProyectoFormPage)`, `ApiClient (Dio+JWT)`, `Nginx`, `Backend (/api/proyectos)`, `PostgreSQL`
4. Agregar los mensajes con Toolbox → **Message** (sincrónico):
   - `Técnico → App`: `completa nombre, selecciona cliente, descripción (opcional)`
   - `App → ApiClient`: `POST /api/proyectos {nombre, cliente_id, descripcion}`
   - `ApiClient → Nginx`: `HTTPS (Bearer token en header)`
   - `Nginx → Backend`: `proxy_pass /api/proyectos`
   - `Backend → Backend`: `verificar JWT y extraer tecnico_id` (auto-mensaje: flecha sobre la misma lifeline)
   - `Backend → PostgreSQL`: `INSERT INTO proyecto (nombre, cliente_id, tecnico_id, ...)`
   - `PostgreSQL → Backend` (retorno): `proyecto creado (id, estado='en_progreso')` — usar **Message** tipo Return (flecha punteada)
   - `Backend → App` (retorno): `201 {id, nombre, estado, cliente, fecha_creacion}`
   - `App → Técnico`: `navegar a ProyectosPage con nuevo proyecto visible`
5. No hay bloque `alt` en este diagrama (flujo feliz directo); si se desea agregar el caso de error de validación, usar **CombinedFragment** con `interactionOperator = alt`.

> **Vinculación navegable:** Este diagrama es el par del Diagrama 6 (Login). Ambos son sub-diagramas de sus respectivos casos de uso: UC11 → Login, UC01 → Crear Proyecto. Al navegar el Diagrama 5 (HU Sprint 1), hacer clic derecho sobre el UC `PB-01` → `Ctrl+Shift+D` abre este diagrama directamente.

---

## 6. Hacer los diagramas navegables (Sub-diagramas)

### Mapa de navegación recomendado

El siguiente mapa define los puntos de entrada y las rutas de drill-down que crean la experiencia navegable:

```
[Diagrama 8: Modelo de Contexto]  ← Punto de entrada principal
    │
    ├── UC01 Gestionar Proyecto
    │     ├── Ctrl+Shift+D → [Diagrama 14: Secuencia Crear Proyecto PB-01]
    │     └── (referencia cruzada) → [Diagrama 11: Modelo de Datos]
    │
    ├── UC11 Autenticar Usuario
    │     └── Ctrl+Shift+D → [Diagrama 6: Secuencia Login]
    │
    ├── UC13/UC19 (admin) → anotados "Sprint 1 ✅"
    │     └── Ctrl+Shift+D → [Diagrama 5: HU Sprint 1]
    │
    └── Sistema completo
          └── Ctrl+Shift+D → [Diagrama 9: Arquitectura de Paquetes]
                              │
                              ├── Package: AppMovil-Flutter
                              │     └── Ctrl+Shift+D → [Diagrama 7: Navegación Móvil]
                              │
                              ├── Package: Backend-FastAPI
                              │     └── Ctrl+Shift+D → [Diagrama 11: Modelo de Datos]
                              │                         └── Ctrl+Shift+D → [Diagrama 12: Esquema Relacional]
                              │
                              └── Node: Nginx + Docker
                                    └── Ctrl+Shift+D → [Diagrama 10: Despliegue]

[Diagrama 5: HU Sprint 1]
    ├── UC PB-01 Gestionar Proyecto
    │     └── Ctrl+Shift+D → [Diagrama 14: Secuencia Crear Proyecto]
    └── UC PB-09 Autenticar Usuario
          └── Ctrl+Shift+D → [Diagrama 6: Secuencia Login]

[Diagrama 1: Ciclo de Vida Scrum]
    ├── Nodo: [R-3] Ejecución del Sprint
    │     └── Ctrl+Shift+D → [Diagrama 3: Sprint 0 Actividades]
    └── Nodo: [R-2] Sprint Planning
          └── Ctrl+Shift+D → [Diagrama 5: HU Sprint 1]
```

### Procedimiento para crear un sub-diagrama navegable

1. En un diagrama abierto, hacer **clic derecho** sobre el elemento que será punto de navegación (paquete, clase, caso de uso, nodo, actividad).
2. Seleccionar **Add → [tipo de diagrama destino]**.
3. StarUML crea el diagrama vacío como hijo del elemento seleccionado — aparece en el Model Explorer bajo ese elemento.
4. Poblar el diagrama hijo con los elementos correspondientes.
5. **Para navegar en tiempo de presentación:** seleccionar el elemento padre en cualquier diagrama → presionar `Ctrl+Shift+D` → se abre el diagrama hijo directamente.

> **Consejo para presentación:** Antes de presentar, abrir todos los diagramas en el panel _Working Diagrams_ y navegar entre ellos con `Ctrl+Shift+]` / `Ctrl+Shift+[`. El presentador puede hacer `Ctrl+Shift+D` sobre un elemento para "sumergirse" en el detalle y `Ctrl+Shift+[` para volver al diagrama anterior.

---

## 7. Paleta de colores y estilo

Para mantener coherencia con los diagramas PlantUML del proyecto, aplicar el siguiente estilo en cada elemento del diagrama. Las propiedades se editan en el **Style Editor** (clic derecho → Edit Style, o en el panel inferior de propiedades).

| Elemento                          | Fill Color | Line Color | Font Color |
| --------------------------------- | ---------- | ---------- | ---------- |
| Clases / Paquetes / Nodos (fondo) | `#EBF5FB`  | `#2980B9`  | Negro      |
| Cabecera de clase (header)        | `#2980B9`  | `#2980B9`  | Blanco     |
| Notas / Anotaciones               | `#FFFDE7`  | `#BDC3C7`  | Negro      |
| Actores                           | `#EBF5FB`  | `#2980B9`  | Negro      |
| Casos de uso                      | `#FDFEFE`  | `#2980B9`  | Negro      |
| Flechas / CommunicationPath       | `#2980B9`  | —          | —          |
| Flechas de Secuencia              | `#2980B9`  | —          | Negro      |

### Aplicar estilo masivo

Para aplicar el mismo estilo a todos los elementos de un tipo:

1. Seleccionar todos los elementos del mismo tipo con `Ctrl+A` y luego deseleccionar los que no apliquen con `Shift+clic`.
2. Abrir **Format → Fill Color** (`Ctrl+Shift+I`) → introducir el código hexadecimal.
3. Repetir para **Format → Line Color** (`Ctrl+Shift+L`).

---

## 8. Tabla de referencia rápida

| Elemento PlantUML      | Herramienta en StarUML Toolbox   | Atajo de creación          |
| ---------------------- | -------------------------------- | -------------------------- | ------------------------ |
| `start` / `stop`       | InitialNode / ActivityFinalNode  | Arrastrar desde Toolbox    |
| `:Actividad;`          | Action (Activity Diagram)        | Arrastrar desde Toolbox    |
| `if/else/endif`        | DecisionNode + ControlFlow       | Arrastrar + editar guard   |
| `fork…end fork`        | ForkNode / JoinNode              | Arrastrar desde Toolbox    |
| `[*] --> Estado`       | InitialPseudostate + Transition  | Arrastrar desde Toolbox    |
| `state "Nombre"`       | State                            | Arrastrar desde Toolbox    |
| `actor "Nombre"`       | Actor                            | Arrastrar desde Toolbox    |
| `usecase "Nombre"`     | UseCase                          | Arrastrar desde Toolbox    |
| `..> <<include>>`      | Include (dependency con stereo)  | Toolbox → Include          |
| `..> <<extend>>`       | Extend                           | Toolbox → Extend           |
| `participant "Nombre"` | Lifeline                         | Arrastrar desde Toolbox    |
| `->` / `-->`           | Message (sync) / Message (async) | Arrastrar entre lifelines  |
| `alt ... else ... end` | CombinedFragment (interactionOp) | Toolbox → CombinedFragment |
| `class Nombre`         | Class                            | Arrastrar desde Toolbox    |
| `enum Nombre`          | Enumeration                      | Toolbox → Enumeration      |
| `--                    | >`                               | Generalization             | Toolbox → Generalization |
| `"1" --> "0..*"`       | Association + multiplicidades    | Toolbox → Association      |
| `*--`                  | Composition                      | Toolbox → Composition      |
| `package "Nombre"`     | Package                          | Toolbox → Package          |
| `node "Nombre"`        | Node (Deployment)                | Toolbox → Node             |
| `artifact "Nombre"`    | Artifact                         | Toolbox → Artifact         |
| `database "Nombre"`    | Database                         | Toolbox → Component/Node   |
| `note right of X`      | Note + NoteLink                  | Toolbox → Note             |

---

## Orden de construcción recomendado

Para evitar referencias rotas, crear los elementos en este orden:

```
1.  Crear proyecto con plantilla UMLConventional
2.  Crear los actores en Use-Case Model (se reusarán)
3.  Crear los casos de uso UC01..UC19 en Use-Case Model
4.  Diagrama 8  — Modelo de Contexto (usa actores + UC ya creados)
5.  Diagrama 11 — Modelo de Datos — Clases (entidades ORM base)
6.  Diagrama 12 — Modelo Lógico Esquema Relacional
             (sub-diagrama del Diagrama 11 o de la clase Usuario)
7.  Diagrama 9  — Arquitectura de Paquetes (referencia entidades)
8.  Diagrama 10 — Despliegue (referencia paquetes ya creados)
9.  Diagrama 6  — Secuencia Login PB-09 (como sub-diagrama de UC11)
10. Diagrama 14 — Secuencia Crear Proyecto PB-01 (sub-diagrama de UC01)
11. Diagrama 5  — HU Sprint 1 (reusa actores y UCs ya creados)
12. Diagrama 2  — Equipo Scrum
13. Diagrama 1  — Ciclo de Vida Scrum
14. Diagrama 3  — Sprint 0 Actividades (sub-diagrama del Diagrama 1)
15. Diagrama 4  — Estados del Product Backlog
16. Diagrama 7  — Navegación App Móvil (sub-diagrama de Package AppMovil)
17. Conectar todos los sub-diagramas según el mapa de navegación de la §6
```

---

_Guía generada para StarUML 7.1 — Wireless HeatMapper · FICCT-UAGRM · Ingeniería de Software II Grupo 24_
