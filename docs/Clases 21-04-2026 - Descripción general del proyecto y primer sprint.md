# Clase 21-04-2026 — Descripción general del proyecto y primer sprint

> **Contexto:** Según el programa, esta clase estaba prevista para la presentación del primer sprint. Sin embargo, se optó por revisar primero algunos aspectos generales sobre la forma de encarar y documentar el proyecto. La clase siguiente se hará una revisión más rápida, y el **día martes** es la presentación formal para evaluación.

---

## 1. Marco de trabajo: Scrum

Scrum **no es una metodología de desarrollo**, sino un **marco de trabajo**. Esto implica que en un libro de Scrum no se explica qué hay que hacer ni cómo hacer el desarrollo de software como tal. Por eso, para la materia, se adoptó un esquema particular (el mismo usado en la materia SEPACO) que integra Scrum con las actividades de ingeniería de software.

Ese esquema aborda **tres puntos**:

1. **¿Cómo se insertan las actividades típicas de ingeniería dentro de Scrum?**
2. **¿Qué formatos se usan?** (e.g., cómo documentar una historia de usuario, un sprint backlog, etc.)
3. **¿Qué debe generar cada sprint?**

### Características del proceso

- **Incremental:** cada sprint es un incremento sobre el anterior.
- **Iterativo:** en cada sprint se repiten las mismas actividades de ingeniería.

Un **incremento** es, para esta materia, una **versión operativa de software**, es decir, software listo para producción que aporta valor real al cliente. Por ejemplo: un sprint que solo tuviera login no aporta valor por sí solo; en cambio, si además permite registrar productos o clientes, ya hay valor tangible.

> **Regla clave:** Cada sprint debe generar, al menos en el primero, un **mínimo de valor** para el cliente.

---

## 2. Actividades de ingeniería dentro de Scrum

Existen **cuatro actividades fundamentales** desde el punto de vista de ingeniería que deben estar presentes en todo proceso de desarrollo. No pueden faltar en ningún sprint:

| #   | Actividad          | Descripción                                                                                        |
| --- | ------------------ | -------------------------------------------------------------------------------------------------- |
| 1   | **Análisis**       | Entender el problema. Nadie dice que hace ingeniería si no dedica tiempo a comprender el problema. |
| 2   | **Diseño**         | Crear las soluciones más óptimas al problema identificado.                                         |
| 3   | **Implementación** | Escribir el código.                                                                                |
| 4   | **Pruebas**        | Asegurarse de que el software esté libre de fallos.                                                |

Estas cuatro actividades deben **insertarse** dentro del marco de trabajo Scrum.

---

## 3. Equipo Scrum

El equipo está conformado por **tres roles**:

### 3.1 Scrum Master

- Es el **facilitador** del equipo.
- No es un líder ni un jefe.
- Su responsabilidad central es asegurarse de que Scrum se aplique correctamente.
- El equipo es totalmente autogestionado; el Scrum Master facilita, no dirige.

### 3.2 Product Owner

- Es el **representante del cliente** dentro del equipo.
- También puede llamársele Ingeniero de Requisitos o Analista.
- Debe saber exactamente qué es lo que el software debe hacer.
- Tiene la responsabilidad de entender y gestionar los requerimientos.

### 3.3 Desarrolladores

Tienen dos características clave:

- **Autogestionados:** no necesitan que se les diga qué hacer en cada momento. Tienen la madurez para seleccionar sus tareas del Sprint Backlog de forma autónoma.
- **Multifuncionales:** pueden trabajar en distintas partes del proyecto (frontend, backend, mobile, base de datos, etc.), no están encerrados en un único rol.

---

## 4. Sprint 0 / Inicio del proyecto (Ingeniería de Requisitos inicial)

Antes de empezar con los sprints, hay un momento de **definición inicial del proyecto** (también llamado Sprint 0 o sprint de definición), donde:

- Se **organiza el equipo** (Scrum Master, Product Owner, Desarrolladores).
- El cliente y el equipo **conversan sobre los requerimientos** del sistema.
- Se generan los **primeros modelos** a partir de los ejercicios iniciales:
  - Modelo de datos
  - Modelo de arquitectura
  - Modelo de contexto

Este trabajo da origen al **Product Backlog inicial**.

---

## 5. Product Backlog

### ¿Cuándo se crea?

Se genera como resultado del trabajo de ingeniería de requisitos del Sprint 0 / inicio.

### ¿Cuándo se actualiza?

El Product Backlog es **dinámico**, puede actualizarse en cualquier momento. Sin embargo, la actualización formal ocurre durante la **Revisión del Sprint** (Sprint Review).

Hay **tres formas de actualizar el Product Backlog** durante la revisión:

1. **Marcar historias como "hechas":** historias completamente implementadas y aceptadas por el cliente.
2. **Regresar historias:** si lo presentado no es lo que el cliente quería, o hay algo que no está bien, la historia regresa al backlog para ser corregida o mejorada (sin marcarse como completada).
3. **Agregar nuevos requerimientos:** si en la revisión se identifican nuevas necesidades, se agregan al Product Backlog.

### Diferencia clave: Product Backlog vs. Sprint Backlog

|                  | Product Backlog                        | Sprint Backlog                           |
| ---------------- | -------------------------------------- | ---------------------------------------- |
| **Contiene**     | Requerimientos (historias de usuario)  | Tareas                                   |
| **¿Qué es?**     | Todo lo que el software debe hacer     | Lo que se hará durante el sprint actual  |
| **Granularidad** | Funcionalidades / historias de usuario | Tareas pequeñas (horas, máximo 1-3 días) |

> **Importante:** Las tareas del Sprint Backlog deben tener **granularidad mínima** (expresable en horas, máximo en días). Una tarea que dure una semana entera impide ver el avance real en el tablero Kanban.

---

## 6. Flujo de un Sprint

```
Product Backlog
      ↓
 Planificación del Sprint
      ↓
 Sprint Backlog
      ↓
 Ejecución del Sprint  →  Incremento (versión operativa)
      ↓
 Revisión del Sprint  →  Actualización del Product Backlog
```

---

## 7. Planificación del Sprint — Aquí ocurre el ANÁLISIS

La **planificación del sprint** es el evento donde se realiza el **análisis**. El Product Owner selecciona las historias a desarrollar y las explica al equipo.

### Las 3 C's de las Historias de Usuario

Durante la planificación aparecen las **3 C's**:

1. **Cards (Tarjetas):** cada requerimiento se documenta como una historia de usuario. Se escribe, se documenta.
2. **Conversación:** el equipo y el Product Owner conversan sobre la comprensión completa de cada requerimiento. Aquí es donde ocurre el **análisis real**, porque se discute y se entiende a fondo cada historia.
3. **Confirmación:** el Product Owner se asegura de que el equipo entendió correctamente la historia de usuario. Puede hacerlo mediante preguntas o, de forma más efectiva, a través del desarrollo de **prototipos**.

### Resultado del Análisis: Historias de Usuario

Cada historia de usuario, en su formato, incluye:

- Nombre del usuario
- Criterios / teoría
- Descripción del requerimiento
- (Opcional) Flujo de proceso / reglas de negocio — **solo cuando amerita**

> **Nota:** No todas las historias de usuario requieren un flujo de proceso. Una historia simple como "gestionar productos" (CRUD) probablemente no lo necesita. Pero una historia como "realizar retiro en caja bancaria" sí amerita describir el proceso detallado.

---

## 8. Ejecución del Sprint — Aquí ocurren DISEÑO, IMPLEMENTACIÓN y PRUEBAS

### 8.1 Diseño

El diseño se aborda desde **cuatro perspectivas**:

#### a) Diseño de Arquitectura

Se utilizan dos diagramas:

- **Diagrama de paquetes:** muestra la organización y estructura del software a nivel de módulos/paquetes.
- **Diagrama de despliegue:** permite visualizar:
  - Los **nodos** (servidores, dispositivos, etc.)
  - Qué **partes del software** van dentro de cada nodo
  - Los **sistemas de comunicación** utilizados (Bluetooth, Internet, red interna, etc.)

> **Alternativa C4:** Opcionalmente, se puede utilizar el modelo **C4** (especialmente diseñado para mostrar arquitectura de software) en lugar de UML. Los niveles 1, 2 y 3 de C4 son muy adecuados para mostrar la arquitectura.

> **Sobre UML:** Asegurarse de utilizar la **versión 2.5 o superior** de UML. Las notaciones anteriores a 2.5 están obsoletas. Para ver las últimas novedades de UML, consultar el sitio oficial de la **OMG (Object Management Group)**: [www.omg.org](https://www.omg.org)

#### b) Diseño de Datos _(OBLIGATORIO)_

Proceso estándar de diseño de base de datos relacional:

1. **Modelo conceptual** — diagrama de clases representando entidades y relaciones
2. **Modelo lógico** — resultado del mapeo del modelo conceptual a un esquema relacional
3. **Normalización** — aplicar reglas de normalización para asegurar consistencia
4. **Diseño físico** — tablas con sus columnas y tipos de datos, listo para implementar

#### c) Diseño de Lógica _(OPCIONAL)_

Solo se realiza para historias de usuario que involucren procesos complejos. Diagramas disponibles:

- **Diagrama de secuencia** — conveniente para mostrar el flujo de mensajes entre objetos
- **Diagrama de actividad** — para flujos de proceso
- **Diagrama de estados** — para flujos con estados bien definidos

> No se hace para todas las historias de usuario; solo donde valga la pena y agregue valor a la documentación.

#### d) Diseño de Interfaces

- Definir patrones de UI homogéneos
- Definir una **identidad visual consistente** en todas las interfaces
- Aplicar criterios de **experiencia de usuario (UX)** e **interacción humano-computadora (HCI)**

---

### 8.2 Implementación

Al escribir código, se deben tomar decisiones y seguir estándares:

- Seguir un **estándar de codificación** establecido por el equipo
- Código **completamente comentado** y bien **refactorizado**
- Decidir el **estilo arquitectónico** (monolítico, por capas, basado en dominio, microservicios, etc.)
- Decidir cómo **gestionar la base de datos**: ORM vs. SQL directo

> **ORM vs. SQL directo:**
>
> - **ORM** (e.g., JPA/Hibernate en Spring Boot, SQLAlchemy en Python): gestiona automáticamente ciertos controles, pero puede restar flexibilidad.
> - **SQL directo:** mayor control y flexibilidad, pero toda la responsabilidad del manejo de transacciones recae en el desarrollador.
> - Cada opción tiene sus ventajas; el desarrollador debe evaluar cuál es más apropiada según el contexto.

---

### 8.3 Pruebas — Tres filtros obligatorios

| Filtro         | Responsable        | ¿Qué hace?                                                                                                                                                                                    |
| -------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1er filtro** | Desarrollador      | **Pruebas unitarias.** El desarrollador debe entregar código completamente probado. No puede decir "que lo pruebe QA"; lo que entrega ya debe estar probado por él.                           |
| **2do filtro** | QA (Cuba / Tester) | **Pruebas de calidad.** Busca romper el software. Verifica: funcionalidad, rendimiento (tiempos de respuesta), seguridad (vulnerabilidades). Si no lo hace QA, lo hará el usuario final.      |
| **3er filtro** | Product Owner      | **Pruebas de aceptación.** Verifica que el software cumple con los requerimientos del negocio. Su punto de partida son los **criterios de aceptación** definidos en cada historia de usuario. |

---

## 9. Modelos que deben generarse por sprint

| Modelo                     | Tipo                                                             | Obligatorio |
| -------------------------- | ---------------------------------------------------------------- | ----------- |
| **Modelo de Contexto**     | Diagrama de Casos de Uso                                         | ✅ Sí       |
| **Modelo de Arquitectura** | Diagrama de Paquetes + Diagrama de Despliegue (o C4 niveles 1-3) | ✅ Sí       |
| **Modelo de Datos**        | Diagrama de Clases conceptual → modelo lógico → físico           | ✅ Sí       |
| **Modelo de Lógica**       | Diagrama de Secuencia / Actividad / Estados (solo donde amerite) | ⚪ Opcional |

### Sobre el Modelo de Contexto

El diagrama de casos de uso es el instrumento ideal porque muestra:

- Las **funcionalidades** del software (casos de uso)
- Los **actores** que interactúan con el sistema (no necesariamente personas; también sistemas externos)
- Los **actores externos** (e.g., un sistema SAP con el que se integra)

> Un **actor** es cualquier entidad externa que interactúa con el sistema, ya sea enviando datos, recibiendo datos, o ambas cosas.

---

## 10. Sobre el uso de IA para generar diagramas

Se puede usar IA para generar diagramas, pero hay **dos problemas importantes** a tener en cuenta:

1. **No siempre cumple la notación UML correctamente.** La IA puede generar un diagrama visualmente entendible pero que no sigue el estándar UML. Si se afirma que se usa UML, debe cumplirse en su totalidad.
2. **Los diagramas generados por IA pueden estar desconectados entre sí.** Por ejemplo, el diagrama de paquetes puede no tener relación con el diagrama de clases ni con el de secuencia.

### Recomendación para usar IA con herramientas CASE (e.g., StarUML, Enterprise Architect):

- Proporcionar una **especificación muy detallada** a la IA
- Pedirle que genere el diagrama en formato **PlantUML** o **XMI**
- Importar ese código a la herramienta CASE
- Desde ahí, integrar y relacionar correctamente todos los diagramas

> De esta forma, los diagramas quedan vinculados en la herramienta (por ejemplo, hacer doble click en un paquete abre el diagrama de casos de uso; hacer doble click en un caso de uso abre el diagrama de secuencia correspondiente).

---

## 11. Los tres objetivos del proyecto

Es importante distinguir claramente los **tres tipos de objetivos**:

| Objetivo                  | ¿Cambia?                   | Descripción                                                                                                                                                                          |
| ------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Objetivo del Proyecto** | No (fijo)                  | Por qué existe el proyecto. Empieza con "Desarrollar...". Responde a la necesidad de crear el software.                                                                              |
| **Objetivo del Producto** | No (fijo)                  | Qué valor obtendrá el cliente con el software funcionando en su negocio. ¿Qué busca lograr el cliente? (mejorar tiempo de atención, aumentar utilidades, etc.)                       |
| **Objetivo del Sprint**   | Sí (cambia en cada sprint) | El propósito específico de cada sprint. Cada sprint atiende aspectos distintos (e.g., Sprint 1: gestión de personas y base; Sprint 2: core del sistema; Sprint 3: aplicación móvil). |

---

## 12. Descripción del problema en el Perfil del Proyecto

Para documentar la descripción del problema, se puede usar una **narración detallada** o combinar varios instrumentos:

1. **Narrativa descriptiva:** texto que, al leerlo completo, da un panorama detallado del negocio y su problemática. Es la parte más larga del documento.
2. **Modelo de negocio:** diagrama de actividad que muestra el flujo de los procesos del negocio.
3. **Modelo tipo SIPOC u otros:** para describir el proceso.
4. **Modelo de dominio:** diagrama de clases donde **cada clase representa un concepto del negocio** (no es ni la base de datos ni el código). Muestra el alcance conceptual del dominio.

> **Nota sobre el Modelo de Dominio:** El término "dominio" viene de matemáticas (el conjunto de valores posibles de una función). En el modelo de dominio, cada clase es un concepto puro del negocio; no representa una tabla ni una clase de código.

---

## 13. Entregables para el Primer Sprint (presentación el martes)

### Contenido del documento (a subir desde la mañana del martes):

**Parte 1 — Perfil del Proyecto:**

- Descripción detallada del proyecto (objetivo del proyecto, objetivo del producto)
- Descripción del problema (narrativa + modelos de negocio/dominio si aplica)
- Proceso de desarrollo (cómo se ha formalizado el uso de Scrum)

**Parte 2 — Resultado del Primer Sprint:**

- Historias de usuario del sprint
- Modelos generados (contexto, arquitectura, datos, lógica donde aplique)
- Avance de implementación (software demostrable)
- Pruebas unitarias realizadas (se deben detallar en el documento)

**Anexos obligatorios:**

1. **Representación gráfica** de la situación actual (problemática) vs. situación deseada
2. **Carta de formalización** del acuerdo con el cliente / proceso de desarrollo
3. **Diapositivas impresas** de la presentación (para que quede registrado en el docente)

### Presentación oral:

- Máximo **10 minutos**
- Debe incluir demostración del **software funcional** (avance de implementación)
- Puede tener **2 o 3 historias de usuario completamente terminadas** para el primer sprint (no es necesario un avance masivo, pero lo que se presente debe estar 100% funcional)

---

## 14. Formato del documento

El documento debe seguir las normas formales de un trabajo académico:

- **Normas APA** para citas y referencias
- Seguir las indicaciones del libro de **Metodología de Investigación** de la institución
- Referencia opcional: **"Manual para elaboración del perfil de proyecto"** — Saúl Escalera (disponible en biblioteca)

Aspectos formales: tipografía, márgenes, espaciado, pies de página, portada, etc.

---

## 15. Cronograma

| Fecha                | Actividad                                              |
| -------------------- | ------------------------------------------------------ |
| Jueves (esta semana) | Revisión rápida de avances (quien tenga algo ya listo) |
| **Martes próximo**   | **Presentación formal — Evaluación del Primer Sprint** |

> La presentación del martes se hará en orden, empezando por los grupos que tengan todo más definido. Los grupos con mayor atraso presentarán al final o en la siguiente oportunidad.

---

_Apuntes tomados de la grabación de clase del 21 de abril de 2026._
