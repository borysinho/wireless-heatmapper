# Clase 21/04/2026 — Aspectos Generales del Proyecto

> **Contexto:** El docente recapitula y amplía los 12 puntos que cada grupo (empresa de software) debe entregar como proyecto de la materia. Cada grupo es tratado como una empresa de software real.

---

## Organización inicial de grupos

- Se completó la conformación de grupos según la hoja firmada entregada previamente.
- Los grupos deben estar compuestos preferentemente por **6 integrantes**.
- Quienes no tenían grupo fueron asignados a grupos incompletos.
- El registro de grupos quedó **cerrado** ese día.

---

## Puntos del Proyecto de la Materia

El docente recapitula que el proyecto tiene múltiples puntos que deben entregarse. A continuación se desarrolla cada uno:

---

### Punto 1 — PAPS

- Ya fue presentado y revisado.
- No se desarrolla nuevamente en esta clase.

---

### Punto 2 — Modelos de Desarrollo

- Se trabaja siguiendo **Scrum**.
- Hay **cuatro modelos obligatorios**:
  1. **Modelo de Contexto**
  2. **Modelo de Arquitectura**
  3. **Modelo de Datos**
  4. **Modelo de Lógica**
- Estos modelos deben estar completamente elaborados.

---

### Punto 3 — Plan/Manual de Garantía de Calidad del Software (SQA / QAP)

#### ¿Qué es?

Un documento orientado a garantizar que lo que se desarrolla tiene calidad. La idea es definir, mientras se desarrolla el software, qué acciones y políticas garantizan que el producto final sea de calidad.

#### Estándares posibles (elegir uno de tres)

| Estándar | Número / Referencia                                     |
| -------- | ------------------------------------------------------- |
| **ISO**  | ISO 9001 (genérico) + guía **ISO 9000-3** para software |
| **IEEE** | IEEE 730                                                |
| **CMMI** | 5 niveles (relaciona capacidad y madurez)               |

> **Nota sobre ISO 9001:** Es un modelo genérico aplicable a cualquier área. La guía específica para software es la **ISO 9000-3**, que indica cómo aplicar el 9001 en el ámbito del desarrollo de software.

> **Nota sobre CMMI:** Distingue entre _capacidad_ (saber hacer) y _madurez_ (hacerlo de forma repetible y consistente). Las empresas van escalando en los 5 niveles. Muchas empresas no logran superar el nivel 2.

#### Error común a evitar

> **NO** deben orientar el manual de calidad hacia el proyecto o software en particular.  
> **SÍ** deben orientarlo hacia la **empresa de software** (ya que cada grupo es una empresa).

#### Contenido esperado del manual (orientativo)

- Misión y visión de la empresa de software
- Política de calidad de la empresa
- Patrones o estándares de desarrollo adoptados
- Procedimientos y lo que hay que seguir haciendo para asegurar calidad

#### ¿Cuándo se entrega?

- El docente dictará primero una clase explicando el estándar seleccionado (**SQA**).
- En la **clase siguiente** a esa explicación, los grupos deben traer el **manual de calidad aplicado a su empresa**.
- Se recomienda **empezar a leer ISO 9000-3 desde ahora**, ya que el contenido es extenso.

---

### Punto 4 — Herramientas CASE

#### ¿Qué significa CASE?

> **CASE** = _Computer Aided Software Engineering_ = Ingeniería de Software Asistida por Computador

#### ¿Qué se debe demostrar?

- Que se usó una herramienta CASE **más allá de simplemente dibujar diagramas**.
- Que se aprovechó el propósito real de la herramienta: **mejorar y acelerar la productividad**.
- Se deben mostrar los modelos del Punto 2, esta vez elaborados dentro de la herramienta CASE, demostrando **navegabilidad entre modelos**.

#### Ejemplo de navegabilidad esperada (con una herramienta como ArgoUML u otra)

```
Diagrama de Paquetes
    └── doble clic en un paquete → Diagrama de Casos de Uso
            └── doble clic en un caso de uso → Diagrama de Comunicación / Secuencia
                    └── doble clic en un objeto → Diagrama de Clases
                            └── los mensajes que fluyen entre objetos → aparecen como métodos/operaciones de las clases
```

Esta **navegabilidad completa** es lo que se debe visualizar y demostrar.

#### Conocimientos requeridos

1. Comprensión conceptual de qué es una herramienta CASE y para qué sirve.
2. Saber **usar** la herramienta de manera avanzada (no solo dibujar).

#### Integración posible

- Se pueden integrar **varias herramientas CASE**.
- Se pueden integrar con el propio entorno de desarrollo (IDE).

---

### Punto 5 — Aspectos Legales para Apertura de Empresa de Software

#### ¿Qué se debe hacer?

Definir todos los **requisitos y trámites legales** que deben cumplirse para abrir una empresa de desarrollo de software en Bolivia.

#### Pasos orientativos (a investigar y documentar)

1. **Obtener el NIT** (Número de Identificación Tributaria) — incluir los pasos requeridos.
2. **Registrarse en FUNDEMPRESA** (registro de empresas en Bolivia).
3. **Obtener la Patente Municipal** del municipio correspondiente.
4. **Registrar Derechos de Autor** del software — saber en qué institución se registra.

#### Observaciones del docente

- Todo esto se puede investigar **sin salir de casa**, a través de las páginas web oficiales de cada institución.
- Para mayor detalle, se puede consultar con:
  - Un **profesional del área administrativa**
  - Un **contador**
  - Un **tramitador**
- **No van a abrir la empresa de verdad**, pero deben saber exactamente qué hay que hacer.

#### Reflexión sobre el equipo de una empresa de software

El docente puntualiza que una empresa de software no puede estar conformada solo por ingenieros. Se necesita también:

- **Expertos financieros** → para manejar correctamente el dinero que se mueve.
- **Expertos en impuestos** → porque los impuestos en Bolivia son significativos. Ejemplo de desglose al emitir una factura:

| Impuesto                                                                 | Porcentaje     |
| ------------------------------------------------------------------------ | -------------- |
| IVA                                                                      | 13%            |
| Impuesto a las Transacciones (IT)                                        | 3%             |
| Impuesto a las Utilidades de las Empresas (IUE, anual)                   | 25%            |
| Otros (comisiones de tiendas: App Store, Google Play, pasarelas de pago) | Variable (~5%) |
| **Total aproximado**                                                     | **~41%** o más |

> El propósito del punto 5 es que los estudiantes **se informen de todo esto** para que, cuando lo hagan de verdad, no sean sorprendidos.

---

### Punto 6 — Infraestructura para la Producción de Software

#### ¿Qué se debe mostrar?

Toda la **infraestructura tecnológica** que el equipo usa o usará para desarrollar el proyecto. Incluye herramientas en varias categorías:

| Categoría                                 | Ejemplos                                                                           |
| ----------------------------------------- | ---------------------------------------------------------------------------------- |
| **Gestión del proyecto**                  | Jira, Trello, Chotrack                                                             |
| **Desarrollo colaborativo**               | Herramientas de trabajo en equipo sobre código                                     |
| **Control de versiones**                  | Git (con ramas individuales por desarrollador + rama `main`/`master`)              |
| **Gestión de configuración del software** | Control de cambios, control de versiones (más allá del simple Git)                 |
| **Despliegue automatizado**               | Docker (microservicios), Kubernetes (orquestación si hay múltiples microservicios) |
| **Herramientas de IA integradas al IDE**  | GitHub Copilot, Gemini (Google), u otras herramientas de IA para desarrollo        |

#### Observación sobre IA en el desarrollo

> Hoy en día es completamente natural y conveniente usar herramientas de IA integradas al IDE. El docente menciona la herramienta de **Google (Gemini)** como particularmente buena porque:
>
> - Está pensada en la generación de **distintos agentes**.
> - Puede trabajar **simultáneamente** en cada aspecto del proyecto.
> - No es solo un generador de código, sino que trabaja desde la misma comunicación del proyecto.

La idea es que **todo sea lo más automatizado posible**.

---

### Punto 7 — Sitio Web de la Empresa

#### Requisitos

- Debe estar **100% publicado y en línea** (no se aceptan prototipos o localhost).
- Debe representar a la **empresa de software** (no al producto en sí).

#### Contenido mínimo del sitio web

- **Quiénes somos** (información de la empresa)
- **Productos/Servicios**
- **Descargas** (si aplica)
- **Soporte**
- **Contacto** con botones de: WhatsApp, redes sociales, envío de emails
- **Chatbot** integrado y bien entrenado

#### Sobre el chatbot

> **No** debe ser simplemente un botón de WhatsApp.  
> Debe ser un **chatbot propio**, con contenido específico y entrenado acorde a:
>
> - Las características de la empresa
> - El proyecto que desarrollan
> - El tipo de usuario al que atienden

---

### Punto 8 — Estudio de Mercado

#### ¿Por qué es necesario?

Ningún emprendimiento real existe sin un estudio de mercado. Aunque muchos grupos están resolviendo problemas reales (talleres de grado), deben hacer este ejercicio con fines prácticos.

#### Contenido esperado

- **Cuantificación del mercado**: determinar el tamaño del mercado objetivo.
- **Segmentación del mercado**: identificar los tipos de usuarios o clientes.
- **Tipos de monetización**: definir **cómo van a generar dinero** con el software.
  - Hay muchas formas de monetización (freemium, suscripción, licencia, comisiones, etc.).

#### Observación clave

> **Todo debe estar basado en números.** Nada de suposiciones sin respaldo cuantitativo. Si no hay datos, no es un estudio de mercado.

Si los grupos necesitan apoyo, pueden consultar con especialistas del área de administración de empresas o mercadotecnia.

---

### Punto 9 — Pruebas del Software

> Este punto demanda **más esfuerzo** que muchos de los otros, porque el software debe estar **completamente probado** antes de entregarse.

#### Concepto clave

Si el cliente solicita una **boleta de garantía** del software, el equipo no puede negarse. Para emitirla, deben estar seguros de que lo que entregan es de calidad.

#### Niveles de prueba obligatorios

##### Nivel 1 — Pruebas de Unidad (por el programador)

- Cada programador prueba su propio código **antes de entregarlo**.
- No puede entregar esperando que otro encuentre sus errores.
- Se usan **frameworks de pruebas de unidad** (JUnit, Jest, pytest, etc.) integrados al entorno de desarrollo.

##### Nivel 2 — QA (Aseguramiento de Calidad)

- El QA tiene la responsabilidad de **intentar quebrar el software**.
- Prueba más allá de la lógica funcional:
  - **Rendimiento** (tiempo de respuesta)
  - **Vulnerabilidades de seguridad**
  - Otros aspectos no funcionales
- Se deben usar **herramientas y servicios especializados** (por ejemplo, escáneres de vulnerabilidades que reciben una URL y detectan todos los posibles fallos).

##### Nivel 3 — Product Owner (validación del negocio)

- Valida que el software haga **funcionalmente lo que debe hacer**.
- Más allá de que técnicamente esté bien, verifica que cumpla con los **requerimientos del negocio**.

#### Técnicas a aplicar

##### Técnica de Caja Blanca — Método del Camino Básico

- **Propósito:** No prueba la funcionalidad, sino la **lógica interna** del código.
- **Aplicación:** Elegir al menos **4 métodos / casos de uso / historias de usuario** del software.
- **Criterio de selección:** Aplicar donde la **complejidad ciclomática sea ≥ 3**.
  - La complejidad ciclomática mide el número de caminos independientes en el código (similar a las funciones O(n), O(n²), etc. en algoritmos).
- **Resultado esperado:** Demostrar que se probaron todos los caminos posibles en la lógica de esos métodos.

##### Listas de Comprobación (Checklists)

- Son listados de verificación con ítems que deben cumplirse **antes de publicar** una aplicación.
- Ejemplo análogo: en cirugías hay checklists obligatorios; en aviación, antes de despegar se verifica ítem por ítem.
- En software: existen recomendaciones genéricas de ingeniería de software que deben cumplirse para que una publicación sea correcta.
- Se obtienen de los **libros de ingeniería de software**.

##### Herramientas de Prueba

- Para probar **tiempo de respuesta**: se debe poblar la base de datos con una **gran cantidad de registros** y ejecutar las operaciones midiendo el tiempo real.
- Deben usar herramientas especializadas para:
  - Poblado de bases de datos
  - Medición de rendimiento (benchmarking)
  - Detección de vulnerabilidades

#### Documentación de pruebas

El docente indica que:

1. Deben leer y aplicar el **flujo de trabajo de pruebas del Proceso Unificado** (del libro del proceso de desarrollo — buscar el capítulo/tema de "Prueba" o "Flujo de Trabajo de Prueba"). Debe aplicarse **completo**.
2. Aplicar técnicas de **caja blanca** (camino básico) para los métodos seleccionados.
3. Incluir **listas de comprobación** obtenidas de literatura de ingeniería de software.
4. Demostrar el uso de **herramientas de prueba** con resultados reales.

Todo esto debe aparecer en el **documento de pruebas** del proyecto.

---

### Punto 10 — Marketing

#### ¿Qué se debe hacer?

Definir y documentar todos los **mecanismos de promoción** que la empresa usaría para dar a conocer su producto.

#### Ejemplos de estrategias de marketing

- Publicaciones en **redes sociales**
- **Lanzamientos** del producto
- Asistencia a **ferias tecnológicas**
- Participación en **convenciones** del sector
- Elaborar el **material correspondiente** para cada estrategia (flyers, posts, demos, etc.)

> El propósito es identificar las oportunidades concretas para dar a conocer lo que han desarrollado.

---

### Punto 11 — Aspectos para la Puesta en Marcha

#### Infraestructura Cloud

Se deben evaluar y comparar **tres plataformas cloud** obligatorias:

| Plataforma       | Proveedor |
| ---------------- | --------- |
| **AWS**          | Amazon    |
| **Google Cloud** | Google    |
| **Azure**        | Microsoft |

Para cada una, se deben hacer **proyecciones de costos** utilizando las calculadoras de precios que proveen (pago por consumo).

> No es obligatorio **desplegar** las aplicaciones móviles en las tiendas (App Store, Google Play), pero **sí** es obligatorio presentar todos los **requisitos y características** necesarios para abrir una cuenta de desarrollador en dichas tiendas.

**Diferencias importantes a considerar** al abrir cuentas de publicación:

- Cuenta **personal** vs. cuenta de **empresa** (diferente proceso y costos)
- Cuenta de **organización educativa** o **social** (requisitos distintos)

Según el tipo de proyecto desarrollado, deberán definir qué tipo de cuenta corresponde.

#### Tipos de Licencia del Software

Deben especificar **cómo van a otorgar licencias** de su software. Opciones:

- **SaaS** (Software as a Service) — modelo de suscripción en la nube
- **On-Premise** — instalación local en el cliente
- Otros modelos de licenciamiento

#### Términos y Condiciones / Políticas de Privacidad

- Toda aplicación debe incluir **Términos y Condiciones** que el usuario acepta al registrarse o instalar.
- Toda aplicación debe incluir una **Política de Privacidad** clara.
- Ambos documentos deben estar elaborados y enlazados desde la aplicación.

#### Mecanismos de adopción por parte del usuario

El docente pregunta cómo harían para que los usuarios usen el software correctamente. Los estudiantes responden: manuales, tutoriales, videos. El docente señala que hay algo más efectivo:

> **Un agente de IA** que esté permanentemente monitoreando lo que el usuario hace, de modo que cuando necesite ayuda, el agente ya tenga todo el contexto y pueda asistir sin necesidad de que el usuario explique desde cero.

Esto conecta con el punto del chatbot (Punto 7) y el desarrollo dirigido por especificación.

---

### Punto 12 — Software como Producto (Entregable Final)

- Definido desde Software 1: el software desarrollado se entrega como un **producto real**.
- Se debe entregar el software con **todas sus características** definidas y funcionando correctamente.
- Incluye todo lo construido a lo largo del semestre.

---

## Fechas y Dinámica de Entrega

- **Fecha máxima** de entrega de todos los puntos: **dos semanas antes del último día de clases**.
- Los puntos pueden entregarse de forma incremental a lo largo del semestre.
- **Sprint de Scrum**: los grupos llevan ~3 semanas en el proyecto. Un sprint dura máximo 2 semanas, por lo que ya deberían haber completado al menos un sprint.
  - El docente **no avisará** cuándo revisar el sprint: se supone que el equipo gestiona su propio Scrum y el tablero debe reflejar el estado actual en todo momento.
  - Habrá una **fecha final** inamovible de todas formas.

---

## Actividad del día (21/04/2026)

- **No hay presentación** de proyectos ese día.
- La actividad del día es hacer **revisiones con Scrum** (revisión del estado del tablero/sprint de cada grupo).
- El docente hace énfasis en que los desarrolladores deben usar la IA de manera **responsable**, bajo el enfoque de **Desarrollo Dirigido por Especificación**.

---

## Resumen de los 12 Puntos del Proyecto

| #   | Punto                               | Descripción breve                                              |
| --- | ----------------------------------- | -------------------------------------------------------------- |
| 1   | **PAPS**                            | Ya presentado                                                  |
| 2   | **Modelos de Desarrollo**           | Contexto, Arquitectura, Datos, Lógica (con Scrum)              |
| 3   | **Manual de Garantía de Calidad**   | ISO 9001 / IEEE 730 / CMMI — aplicado a la empresa             |
| 4   | **Herramientas CASE**               | Demostrar navegabilidad y uso real de herramientas CASE        |
| 5   | **Aspectos Legales**                | Trámites para apertura de empresa de software en Bolivia       |
| 6   | **Infraestructura para producción** | Gestión, CI/CD, Docker, Kubernetes, IA, control de versiones   |
| 7   | **Sitio Web**                       | Publicado, con chatbot propio entrenado                        |
| 8   | **Estudio de Mercado**              | Cuantificación, segmentación, monetización — todo en números   |
| 9   | **Pruebas**                         | Unitarias, QA, PO; caja blanca, checklists, herramientas       |
| 10  | **Marketing**                       | Estrategias y materiales para dar a conocer el producto        |
| 11  | **Puesta en Marcha**                | Cloud (AWS/GCP/Azure), licencias, T&C, políticas de privacidad |
| 12  | **Software como Producto**          | Entrega final del software completo y funcional                |
