# Enfoque de Aplicación de Scrum como Marco de Trabajo para el Desarrollo de Software
**Versión 3.2**  
**Autor:** M.Sc. Ing. Rolando Martínez Canedo  
**Institución:** FICCT – UAGRM

---

## Tabla de Contenido

1. [Ciclo de Vida](#i-ciclo-de-vida)
2. [Actividades de Definición Inicial (R-1)](#ii-actividades-de-definición-inicial-r-1)
3. [Actividades a Realizar en Cada Sprint](#iii-actividades-a-realizar-en-cada-sprint)
   - [Sprint Planning (R-2)](#1-evento--tareas-para-realizar-el-sprint-planning-r-2)
   - [Ejecución del Sprint (R-3)](#2-evento--actividades-a-realizar-durante-la-ejecución-del-sprint-r-3)
   - [Scrum Diario (Daily Scrum)](#3-evento--scrum-diario-daily-scrum)
   - [Revisión de Sprint (R-4)](#4-evento--revisión-de-sprint-r-4)
   - [Retrospectiva de Sprint (R-5)](#5-evento--retrospectiva-de-sprint-r-5)
4. [Formularios y Plantillas](#iv-formularios-y-plantillas)

---

## I. Ciclo de Vida

### Ciclo de Vida del Software Basado en Scrum

El ciclo de vida del software en Scrum se estructura en una secuencia continua de Sprints, donde cada Sprint produce un incremento potencialmente entregable del producto. La estructura es la siguiente:

```
[ Sprint 1 ] ──► [ Sprint 2 ] ──► [ ... ] ──► [ Sprint n ]
```

Cada bloque (Sprint) representa una iteración completa del proceso Scrum. Los Sprints son contiguos, es decir, uno comienza inmediatamente después de que el anterior finaliza. El número de Sprints (n) varía según la complejidad y los requerimientos del proyecto.

---

### Marco de Trabajo Scrum (Diagrama General)

El siguiente esquema describe el flujo completo del Marco de Trabajo Scrum, con sus artefactos, eventos y roles, tal como se referencia en este enfoque:

```
                        ┌──────────────────────┐
                        │ Sprint Retrospective │  ◄── (R-5)
                        └──────────┬───────────┘
                                   │
          Product Goal             │
              │                    │
    ┌─────────▼──────────┐         │           ┌──────────────────┐
    │   Product Backlog  │         │           │   Daily Scrum    │
    │   Refinement       │         │           └──────────────────┘
    └─────────┬──────────┘         │                    │
              │                    │                    │
    ◄── (R-1) │                    │           ┌────────▼─────────┐     Definition
              │                    │           │                  │     of Done
    ┌─────────▼──────────┐  Sprint │           │   Scrum Team     │        │
    │  Product Backlog   │  Goal   │           │  ┌─────────────┐ │        │
    └─────────┬──────────┘    │    │           │  │ Dev  │  SM  │ │        │
              │               │    │           │  │      PO     │ │        │
    ┌─────────▼──────────┐    │    │           └────────┬─────────┘        │
    │   Sprint Planning  ├────►    │                    │             ┌────▼──────────┐
    └─────────┬──────────┘         │           ┌────────▼─────────┐   │ Sprint Review │
    ◄── (R-2) │                    │           │ Sprint Backlog   │   └───────────────┘
              │                    │           └──────────────────┘   ◄── (R-4)
              │                    │                    │
              └────────────────────┴────────────────────►  Increment
                                                      (R-3)
```

**Roles identificados en el Scrum Team:**
- **Dev** – Desarrolladores: responsables de crear el incremento.
- **SM** – Scrum Master: facilita el proceso y elimina impedimentos.
- **PO** – Product Owner: responsable del Product Backlog y el valor del producto.

**Artefactos del marco:**
- **Product Backlog** – Lista ordenada de todo lo que se necesita en el producto.
- **Sprint Backlog** – Conjunto de ítems seleccionados del Product Backlog para el Sprint, más el plan para entregarlos.
- **Increment** – Suma de todos los ítems completados del Product Backlog durante el Sprint, que cumplen la Definition of Done.

**Eventos referenciados en este enfoque (registros R):**
| Referencia | Evento/Actividad |
|---|---|
| R-1 | Definición inicial / Sprint 0 |
| R-2 | Sprint Planning |
| R-3 | Ejecución del Sprint |
| R-4 | Sprint Review |
| R-5 | Sprint Retrospective |

---

## II. Actividades de Definición Inicial (R-1)

El objetivo principal de la etapa de **"definición" o "Sprint 0"** es preparar el entorno y sentar las bases para el desarrollo del proyecto en los siguientes Sprints.

> **⚠️ Importante:** Esta etapa es **opcional**, pero se recomienda realizarla para: proyectos complejos, equipos nuevos, y/o cambios tecnológicos significativos.

### Definiciones Iniciales – Sprint 0 (Opcional)

| Id | Tarea |
|----|-------|
| a) | Definir el equipo Scrum, multifuncional y auto gestionado |
| b) | Definir el objetivo del producto |
| c) | Identificar los requerimientos iniciales |
| d) | Definir el tiempo de duración del Sprint (ideal el mismo tiempo para todos: **2 a 4 semanas**) |
| e) | Definir infraestructura tecnológica (hardware y software) para la gestión del proyecto (Jira, Azure DevOps y otros) como también para el proceso de desarrollo del software |
| f) | Definir prácticas de ingeniería que identifiquen actividades técnicas de desarrollo que serán realizadas durante el Sprint |
| g) | Esbozar modelos iniciales de: **Contexto**, **Datos** y **Arquitectura** |
| h) | Definir criterios de calidad |
| i) | Generar el **Product Backlog** (artefacto) – ver formato F3 |

---

## III. Actividades a Realizar en Cada Sprint

### 1) Evento – Tareas para Realizar el Sprint Planning (R-2)

| Id | Tarea |
|----|-------|
| a) | El **Product Owner (PO)** propone cómo el producto podría aumentar su valor y utilidad en el Sprint actual, explicando las **Historias de Usuario (HU)** candidatas a desarrollar durante la ejecución del Sprint. Se utilizan las **3C**: **Card, Conversation, Confirmation**. *(Si se considera conveniente, se puede generar/actualizar el modelo de contexto —como el diagrama general de casos de uso— para tener una vista más abstracta de lo que aportan las HU. Ver formato F4.)* |
| b) | El equipo Scrum define el **objetivo del Sprint** |
| c) | Los desarrolladores estiman los **Puntos de Historia de Usuario** para cada HU, usando **Planning Poker**, para determinar con cuánto se pueden comprometer en el Sprint |
| d) | Los desarrolladores **seleccionan las HU** a desarrollar en el Sprint actual |
| e) | Los desarrolladores, si lo consideran conveniente, describen la solución desde el punto de vista del diseño de las HU seleccionadas en términos de: **Diseño de la arquitectura de software** y **Actualización del diseño de datos**. *(Esta actividad puede dejarse para ser completada y/o detallada durante la ejecución del Sprint —R-3— para cada HU seleccionada.)* |
| f) | Generar el **Sprint Backlog** (artefacto) – ver formato F5 |

---

### 2) Evento – Actividades a Realizar durante la Ejecución del Sprint (R-3)

El propósito de la ejecución del Sprint es que el equipo de desarrollo trabaje en las tareas del Sprint Backlog para cumplir con el objetivo del Sprint y entregar un **incremento de software potencialmente entregable**.

Durante esta fase, el equipo se enfoca en:
- Consolidar el diseño de la solución
- La implementación
- Las pruebas
- Refinar las funcionalidades comprometidas

Todo asegurando que se cumpla con los criterios de calidad y que esté listo para ser revisado en el Sprint Review.

#### 2.a) Cada Desarrollador Selecciona desde el Sprint Backlog qué Tareas Realizará

##### Actividad: Diseñar la Historia de Usuario Seleccionada

Los desarrolladores continúan incrementando los modelos de diseño que correspondan según la HU en proceso, enfocándose en lo necesario para cumplir los objetivos:

**a) Definir/Actualizar el diseño de la arquitectura de software** *(si corresponde)*

Modelos sugeridos (elegir una opción):
- **Opción 1 (UML):** Diagrama de paquetes + Diagrama de despliegue
- **Opción 2 (C4):** Niveles 1, 2 y 3

**b) Definir/Actualizar el proceso de diseño de datos** *(si corresponde)*

Modelo resultado:
- **Modelo conceptual:** Diagrama de clases en UML

**c) Diseñar reglas de la lógica de negocio** *(opcional)*

Modelos opcionales — realizar solo si es necesario y conveniente:
- Diagrama de secuencia
- Diagrama de estados
- Diagrama de tiempo

**d) Diseñar las interfaces de usuario**
- Definir y seguir un patrón de interfaces definido, ajustar si fuera necesario

---

##### Actividad: Implementar la Historia de Usuario Seleccionada

Los desarrolladores continúan incrementando las funcionalidades del software. Las siguientes tareas son un ejemplo y dependen del proceso de implementación definido para el proyecto:

| Id | Tarea de implementación |
|----|------------------------|
| a) | Implementar **Back-end** (servicios APIs RESTful o GraphQL, otros) |
| b) | Implementar **Front-end** (WEB / MÓVIL) |
| c) | Generar consultas SQL o adoptar ORM para interactuar con la BD; scripts de migración para actualizar el esquema de la BD |
| d) | Implementar operaciones CRUD, sistemas de autenticación, roles, permisos y otros |
| e) | Trabajar sobre **ramas individuales** para facilitar colaboración, versionamiento e integración para poner en producción; usar repositorios de código (GitHub) |
| f) | Seguir **estándares de codificación** |

---

##### Actividad: Testear la Historia de Usuario Seleccionada

Los desarrolladores deben asegurar que la funcionalidad implementada esté testeada de forma individual y al integrarse con el resto de las funcionalidades:

| Id | Tarea de pruebas |
|----|-----------------|
| a) | Aplicar **pruebas de unidad**, **caja negra** y otras técnicas de prueba según la aplicación |
| b) | Revisar los **criterios de aceptación** definidos para cada Historia de Usuario |
| c) | Considerar herramientas como: **JUnit**, **Postman**, **JMeter**, **OWASP ZAP**, **Firebase Test Lab**, entre otras |

---

#### 2.b) Generación del Incremento y Despliegue

Al finalizar la ejecución del Sprint se debe generar el **incremento** (artefacto) correspondiente, integrando el resultado con los incrementos anteriores para asegurar que funcionan correctamente juntos.

Consideraciones:
- El incremento debe cumplir con el criterio de **"Definition of Done" (DoD)**
- Asegurarse de que todas las ramas de código estén integradas en la rama principal (**main** o **master**)
- Asegurarse de que el código siga las mejores prácticas de estilo y estándares del equipo
- Preparar/monitorear el entorno de producción
- Considerar el uso de:
  - **Contenedores** (Docker)
  - **Automatización del despliegue**
  - **Pipelines CI/CD** (integración continua / despliegue continuo): GitHub Actions, Jenkins, GitLab, entre otros

---

### 3) Evento – Scrum Diario (Daily Scrum)

Durante la ejecución del Sprint (R-3), el equipo se reúne **15 minutos** cada día para sincronizar actividades y crear un plan para las siguientes 24 horas.

**Intervención de cada integrante del equipo basada en:**
1. ¿Qué hice **ayer** para contribuir al Sprint?
2. ¿Qué voy a hacer **hoy** para contribuir al Sprint?
3. ¿Veo algún **impedimento** que impida lograr el objetivo del Sprint?

**Otras actividades opcionales sugeridas:**
- Actualizar el **tablero tipo Kanban**
- Actualizar el **gráfico de trabajo pendiente (Burndown chart)**

---

### 4) Evento – Revisión de Sprint (R-4)

El propósito de la revisión del Sprint es **inspeccionar el resultado del Sprint y determinar futuras adaptaciones**. El equipo Scrum presenta los resultados a las partes interesadas clave y se discute el progreso hacia el Objetivo de Producto. *(Validación)*

Actividades:
- El **Dueño de Producto** explica qué elementos del Product Backlog se han terminado en cumplimiento con el objetivo definido para el Sprint
- Los **Desarrolladores** presentan el incremento para facilitar la retroalimentación
- Recoger **feedback** de todos los invitados a la revisión
- **Actualizar el Product Backlog**: marcar con "done" lo concluido y colaborar para determinar qué podría ser lo siguiente a desarrollar
- Revisión del valor que podría aportar el siguiente incremento, según los cambios del mercado

> **Resultado:** Al finalizar el Sprint Review, el equipo Scrum tendrá un Product Backlog revisado y actualizado para el siguiente Sprint.

#### Formato F1 – Ejemplo de Revisión de Sprint

```
Revisión de Sprint
─────────────────────────────────────────────────────
Nombre del proyecto y número de revisión:
Objetivo de la revisión:
Lugar, fecha, hora:

Participantes
┌──────────────────┬──────────────────┐
│ Nombre           │ Rol              │
├──────────────────┼──────────────────┤
│                  │                  │
└──────────────────┴──────────────────┘

Presentación del incremento
┌──────────────────────────────────────┐
│ Función presentada                   │
│ [Elemento de trabajo a presentar]    │
└──────────────────────────────────────┘

Retroalimentación
[Preguntas y comentarios]

Tareas completadas
[Marque los elementos de trabajo como "Terminado" que cumplieron con los 
criterios de aceptación. Para los elementos que necesitan más trabajo, 
determine si pasarán al siguiente Sprint o volverán al Product Backlog]

Para lo que viene
[Agregar elementos de acción para actualizar el Product Backlog y futuros 
Sprints en relación al entorno del negocio]
```

---

### 5) Evento – Retrospectiva de Sprint (R-5)

El propósito de la Retrospectiva del Sprint es **planificar formas de aumentar la calidad y la eficacia**. El Equipo Scrum se inspecciona a sí mismo, reflexiona sobre su forma de trabajo y crea un plan de mejoras para el siguiente Sprint, revisando: personas, interacciones, procesos, herramientas y su definición de "done". *(Verificación)*

**Pregunta central:** ¿Qué ha fallado y qué se puede mejorar?

Pasos:
1. **Recolectar información:** Construir una imagen conjunta de lo que ha sido el Sprint
2. **Generación de ideas:** Identificar acciones que ayuden a mejorar el rendimiento del equipo durante el siguiente Sprint
3. **Decidir qué hacer:** Proponer acciones concretas que el equipo pueda implementar en el próximo Sprint

#### Formato F2 – Ejemplo de Retrospectiva de Sprint

```
Retrospectiva de Sprint
─────────────────────────────────────────────────────
Nombre del proyecto y número de retrospectiva:
Objetivos de la retrospectiva:
Lugar, Fecha y hora:
Participantes:

Discusión
┌────────────────┬────────────────┬───────────────────────┬──────────────────────┐
│ ¿Qué salió     │ ¿Qué no salió  │ ¿Qué problemas se     │ ¿Qué debemos         │
│ bien?          │ bien?          │ encontró y cómo       │ cambiar para         │
│                │                │ fueron (o no)         │ mejorar?             │
│                │                │ resueltos?            │                      │
├────────────────┼────────────────┼───────────────────────┼──────────────────────┤
│                │                │                       │                      │
└────────────────┴────────────────┴───────────────────────┴──────────────────────┘
```

---

## IV. Formularios y Plantillas

### Formato F3 – Product Backlog

```
Product Backlog
─────────────────────────────────────────────────────────────────────────────────
Proyecto:
Product Owner:
Versión:                    Fecha:

┌──────┬──────────────────────┬────────────────────────────────────────────────────────────┬──────────┐
│  id  │ Nombre corto del     │ Descripción del requerimiento funcional                    │Prioridad │
│      │ requerimiento        │ usando: "Como <rol> quiero <acción> para <beneficio>"      │          │
├──────┼──────────────────────┼────────────────────────────────────────────────────────────┼──────────┤
│ Pb-1 │ Registrar eventos    │ Como organizador, quiero registrar eventos para realizar   │  Alta    │
│      │                      │ el seguimiento y control                                   │          │
├──────┼──────────────────────┼────────────────────────────────────────────────────────────┼──────────┤
│ Pb-2 │ Retirar dinero de    │ Como cliente, quiero retirar dinero de mi cuenta para      │  Baja    │
│      │ cuenta               │ proceder a realizar pagos                                  │          │
└──────┴──────────────────────┴────────────────────────────────────────────────────────────┴──────────┘
```

> **Nota sobre el formato de descripción:** Siempre seguir la estructura:  
> `Como <rol>, quiero <acción/funcionalidad>, para <beneficio/objetivo>`

---

### Formato F4 – Historia de Usuario

```
Historia de Usuario
─────────────────────────────────────────────────────────────────────────────────
Id:                 Nombre corto de HU:               Prioridad:    PHU:

Como    :  [Rol del usuario]
Quiero  :  [Funcionalidad que desea]
Para    :  [Beneficio o valor que obtendrá]

Descripción:
  [Descripción detallada de la historia]

Conversación / Reglas (opcional):
  [Reglas de negocio, aclaraciones o restricciones surgidas de la conversación]

Prototipo / Mockup (opcional):
  [Imagen o referencia del prototipo de interfaz]

Criterios de aceptación:
  [Lista de condiciones que deben cumplirse para que la historia se considere terminada]
  - Criterio 1:
  - Criterio 2:
  - Criterio n:

Desarrollador:  [Nombre del desarrollador asignado]
```

> **Nota sobre las 3C (Card, Conversation, Confirmation):**
> - **Card:** La historia de usuario escrita en la tarjeta con el formato "Como / Quiero / Para"
> - **Conversation:** El diálogo entre el PO y el equipo para clarificar la HU (campo "Conversación/Reglas")
> - **Confirmation:** Los criterios de aceptación que confirman que la HU está completa

---

### Formato F5 – Sprint Backlog

```
Sprint Backlog
─────────────────────────────────────────────────────────────────────────────────
Sprint número:                  Tiempo programado:
Fecha de inicio del Sprint:     Fecha de finalización del Sprint:

┌──────┬────────────────────────────────────────────┬────────────┬─────────────┬────────────┐
│  Id  │ Tarea                                      │ Estimación │ Responsable │  Estado    │
├──────┼────────────────────────────────────────────┼────────────┼─────────────┼────────────┤
│ Sp-1 │ Instalar y configurar framework Laravel    │  4 hrs     │ Juan        │ En proceso │
├──────┼────────────────────────────────────────────┼────────────┼─────────────┼────────────┤
│ Sp-2 │ Diseñar formulario de registro de cliente  │  2 hrs     │ Pedro       │ Por hacer  │
├──────┼────────────────────────────────────────────┼────────────┼─────────────┼────────────┤
│ Sp-3 │ Implementar API de registro de cliente     │  5 hrs     │ Maria       │ Por hacer  │
└──────┴────────────────────────────────────────────┴────────────┴─────────────┴────────────┘

Estados posibles: Por hacer | En proceso | Terminado
```

---

## Resumen del Flujo Completo por Sprint

A continuación se presenta el flujo consolidado de actividades que ocurren en cada Sprint:

```
INICIO DEL PROYECTO
       │
       ▼
[R-1] SPRINT 0 – Definición Inicial (opcional)
  • Formar equipo Scrum
  • Definir objetivo del producto
  • Identificar requerimientos iniciales
  • Definir duración del Sprint (2-4 semanas)
  • Definir infraestructura tecnológica
  • Definir prácticas de ingeniería
  • Esbozar modelos: Contexto, Datos, Arquitectura
  • Definir criterios de calidad
  • Generar Product Backlog (F3)
       │
       ▼
┌──────────────────────────────────────────────────────┐
│                  CICLO DE SPRINT                     │
│                                                      │
│  [R-2] SPRINT PLANNING                               │
│    • PO explica HU candidatas (3C)                   │
│    • Equipo define objetivo del Sprint               │
│    • Estimación con Planning Poker (PHU)             │
│    • Selección de HU para el Sprint                  │
│    • Diseño preliminar (arquitectura / datos)        │
│    • Generar Sprint Backlog (F5)                     │
│                    │                                 │
│                    ▼                                 │
│  [R-3] EJECUCIÓN DEL SPRINT                          │
│    Por cada HU seleccionada:                         │
│      1. DISEÑAR (arquitectura, datos, UI, lógica)    │
│      2. IMPLEMENTAR (back-end, front-end, BD, CRUD)  │
│      3. TESTEAR (unidad, integración, aceptación)    │
│    Al finalizar:                                     │
│      • Integrar ramas → rama principal               │
│      • Verificar Definition of Done                  │
│      • Desplegar (Docker, CI/CD)                     │
│    Diariamente → DAILY SCRUM (15 min):               │
│      • ¿Qué hice ayer?                               │
│      • ¿Qué haré hoy?                                │
│      • ¿Hay impedimentos?                            │
│                    │                                 │
│                    ▼                                 │
│  [R-4] SPRINT REVIEW (Validación)                    │
│    • PO explica ítems completados                    │
│    • Demo del incremento a stakeholders              │
│    • Recoger feedback                                │
│    • Actualizar Product Backlog (marcar "done")      │
│    • Formato F1                                      │
│                    │                                 │
│                    ▼                                 │
│  [R-5] SPRINT RETROSPECTIVE (Verificación)           │
│    • ¿Qué salió bien?                                │
│    • ¿Qué no salió bien?                             │
│    • ¿Qué problemas hubo y cómo se resolvieron?      │
│    • ¿Qué debemos cambiar para mejorar?              │
│    • Formato F2                                      │
│                    │                                 │
└────────────────────┼─────────────────────────────────┘
                     │
                     ▼
              ¿Hay más Sprints?
              /              \
            SÍ               NO
             │                │
             ▼                ▼
     [Volver a R-2]    FIN DEL PROYECTO
```

---

*Documento generado a partir de: "Un enfoque de aplicación de Scrum como marco de trabajo para el desarrollo de software (Ver. 3.2)" – M.Sc. Ing. Rolando Martínez Canedo, FICCT-UAGRM.*
