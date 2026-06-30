<div style="text-align: center;">

**UNIVERSIDAD AUTÓNOMA GABRIEL RENÉ MORENO**

**Facultad de Ingeniería en Ciencias de la Computación y Telecomunicaciones**

**Carrera: Ingeniería Informática**

---

![Logo UAGRM](../../../../mobile/img/uagrm-logo.png)

---

# PERFIL DEL PROYECTO

## Wireless HeatMapper

### Sistema Inteligente de Análisis y Optimización de Cobertura WiFi mediante Mapas de Calor

**Variante:** Modalidad 100 % en línea
(sin persistencia local en el dispositivo móvil ni mecanismos de sincronización diferida)

---

**Grupo:** 24

**Autores:**

| Estudiante                         | Registro  |
| ---------------------------------- | --------- |
| Fernandez Ortega Jhasmany Jhunnior | 207025509 |
| Quiroga Flores Herland Borys       | 200104373 |

**Materia:** Ingeniería de Software II

**Docente:** Ing. Rolando Martínez Canedo, M.Sc.

**Cliente real:** Bulldog Tech.

**Santa Cruz de la Sierra — Bolivia**

**Abril de 2026**

</div>


# 1. Introducción

En la actualidad, la conectividad inalámbrica mediante redes WiFi se ha convertido en un componente esencial dentro de entornos empresariales, educativos y domésticos, permitiendo el acceso continuo a servicios digitales y sistemas de información. Sin embargo, la correcta planificación y el despliegue de estas redes en espacios interiores representan un desafío técnico significativo debido a factores como la atenuación de la señal, las interferencias electromagnéticas, los obstáculos físicos y la distribución irregular de los puntos de acceso. En muchos casos, el diseño de redes WiFi se basa en estimaciones teóricas proporcionadas por los fabricantes y en la experiencia empírica de los técnicos, lo cual no garantiza una cobertura óptima en condiciones reales, derivando en zonas de baja señal, interferencias entre canales, solapamientos innecesarios y deficiencias en la calidad del servicio que únicamente se detectan después de la implementación.

El presente proyecto, denominado **Wireless HeatMapper**, propone el desarrollo de un sistema **estrictamente en línea** compuesto por dos componentes integrados y un backend central: una **aplicación móvil Android** desarrollada en Flutter que opera como cliente delgado, encargada del relevamiento en campo y de transmitir en tiempo real cada medición al backend, sin almacenar datos de dominio de forma persistente en el dispositivo; un **backend REST** implementado con Python/FastAPI que aloja el módulo de inteligencia artificial responsable de sugerir ubicaciones óptimas para los puntos de acceso y que actúa como única fuente de verdad sobre PostgreSQL; y una **plataforma web** construida con React + TypeScript que cumple dos funciones esenciales: panel de administración para la gestión de cuentas de técnicos y de clientes, y portal de cliente que permite visualizar de forma interactiva los resultados de un proyecto mediante un enlace único de acceso.

La justificación del proyecto se apoya en su capacidad de transformar el proceso tradicional de diseño de redes —basado en estimaciones teóricas— en un proceso fundamentado en evidencia técnica medible y compartible en línea entre técnicos, administradores y clientes. La integración de inteligencia artificial para la recomendación de posicionamiento de puntos de acceso, junto con la operación 100 % en línea sobre una arquitectura cliente-servidor robusta (Docker Compose + Nginx + FastAPI + PostgreSQL), eleva la propuesta por encima de las herramientas existentes de site survey y la convierte en una solución de alto valor para empresas como **Bulldog Tech.**, cuyo trabajo cotidiano consiste en relevar, diagnosticar y optimizar redes inalámbricas en edificios corporativos. A largo plazo, el sistema sienta las bases para incorporar telemetría continua, comparación de escenarios proyectados y entrega digital de informes técnicos a los clientes finales.


# 2. Antecedentes

## 2.1 Revisión Literaria

### **_Diseño y Site Survey de Redes WLAN — Marco CWNA-107_**

La Certified Wireless Network Administrator (CWNA-107) constituye el marco de referencia técnica más extendido para el diseño y validación de redes inalámbricas IEEE 802.11. Esta especificación define los parámetros operativos clave que debe medir y reportar cualquier herramienta de site survey: la **intensidad de señal recibida (RSSI)**, la **relación señal-ruido (SNR)**, la **utilización de canal**, el **solapamiento por co-canal (CCI)** y la **interferencia por canal adyacente (ACI)**. Conforme al manual CWNA-107, una red bien diseñada debe garantizar **RSSI ≥ −70 dBm** en zonas de cobertura primaria, y considerar como **zona muerta** toda área donde el RSSI cae por debajo de **−90 dBm**. El estándar define adicionalmente la metodología de site survey en tres etapas —_passive survey_, _active survey_ y _predictive survey_— y recomienda densidades mínimas de muestreo por metro cuadrado para garantizar la fidelidad de los mapas de cobertura interpolados. Estos umbrales y procedimientos constituyen el fundamento técnico del módulo de captura, análisis e inteligencia artificial del Wireless HeatMapper.

### **_Métricas de Software — Marco de Pressman (Ingeniería del Software, 7.ª edición)_**

Roger S. Pressman formaliza, en su tratado de Ingeniería del Software, dos familias de métricas para la planificación temprana de proyectos: las **Métricas Orientadas al Tamaño (MoT)** —que se apoyan en líneas de código (KLDC), esfuerzo en personas-mes y densidad de defectos— y las **Métricas Orientadas a la Función (MoF)** propuestas originalmente por Albrecht, que cuantifican el sistema en **Puntos de Función (PF)** mediante la combinación de cinco parámetros (entradas, salidas, consultas, archivos lógicos internos e interfaces externas) ajustados por catorce factores de complejidad. Pressman complementa estas técnicas con el **modelo COCOMO II** y con la **Ecuación del Software de Putnam–Myers**, que permite estimar el tiempo mínimo de desarrollo a partir del tamaño del sistema y de la productividad esperada del equipo. El presente proyecto aplica integralmente este marco para dimensionar el esfuerzo de las nueve funciones principales (RP1–RP9) y para situar al Wireless HeatMapper en relación con tres herramientas de referencia analizadas en GitHub.

### **_Marco de Trabajo Scrum_**

Scrum es un marco de trabajo (no una metodología prescriptiva) que define eventos, roles y artefactos para el desarrollo iterativo e incremental de productos de software complejos. En este proyecto, Scrum se integra con las cuatro actividades obligatorias de la ingeniería de software (análisis, diseño, implementación y pruebas) y se formaliza mediante cinco eventos —**R-1 Definición Inicial**, **R-2 Sprint Planning**, **R-3 Ejecución** (con Daily Scrum), **R-4 Sprint Review** y **R-5 Sprint Retrospective**— junto con los artefactos **F3 Product Backlog**, **F4 Historias de Usuario** y **F5 Sprint Backlog**. Este marco es el adoptado por el equipo de desarrollo para gestionar la evolución incremental del Wireless HeatMapper a lo largo de seis Sprints de dos semanas.

## 2.2 Referencias de Aplicaciones

A continuación se describen tres aplicaciones de software libre que constituyen referentes funcionales y metodológicos para el Wireless HeatMapper. Las métricas extraídas (KLDC, esfuerzo, defectos, puntos de función) se utilizan en la sección de estimaciones del Anexo Técnico.

### **_WiFiAnalyzer_**

WiFiAnalyzer es una aplicación móvil nativa para Android desarrollada en Kotlin y orientada al análisis de redes inalámbricas en tiempo real. Permite visualizar la intensidad de señal (RSSI), identificar puntos de acceso (SSID, BSSID), detectar canales ocupados en las bandas de 2.4 GHz, 5 GHz y 6 GHz, estimar la distancia a cada AP y consultar la base de datos de fabricantes a partir de la dirección MAC. La aplicación se distribuye por Google Play y F-Droid bajo licencia GPL-3.0. Su relevancia como referencia radica en que comparte con el Wireless HeatMapper la plataforma de destino (Android), el tipo de datos capturados y la naturaleza de la interfaz orientada a la gestión de redes inalámbricas. Es el proyecto de mayor madurez de los tres analizados, con 4 700 estrellas y 728 forks en GitHub.

| Atributo                  | Valor                                           |
| ------------------------- | ----------------------------------------------- |
| Repositorio               | github.com/VREMSoftwareDevelopment/WiFiAnalyzer |
| Plataforma                | Android (Google Play / F-Droid)                 |
| Lenguaje principal        | Kotlin 97.4 %, Java 2.6 %                       |
| Licencia                  | GPL-3.0                                         |
| Estrellas / Bifurcaciones | 4 700 / 728                                     |
| Confirmaciones (commits)  | 2 013                                           |
| Issues abiertas           | 6                                               |
| KLDC estimado             | 25.0                                            |
| Esfuerzo estimado         | 71 personas-mes                                 |

> _Figura 1: Captura de la interfaz principal de WiFiAnalyzer mostrando la lista de redes detectadas con su RSSI y canal._

### **_WiFiSurveyor_**

WiFiSurveyor es una aplicación web de escritorio multiplataforma (Windows, macOS y Linux) que combina la recopilación de datos de señal WiFi con la visualización de mapas de calor sobre planos de edificios. Está desarrollada en TypeScript (frontend Vue.js) y C# (backend multiplataforma). De los tres proyectos analizados, **WiFiSurveyor es el que mayor similitud funcional presenta con el Wireless HeatMapper**: permite importar un plano como imagen de fondo, registrar puntos de medición sobre él con sus coordenadas y valores de señal, y generar un mapa de calor de cobertura. Su integración con SonarCloud para análisis de calidad de código también lo convierte en una referencia metodológica relevante.

| Atributo                  | Valor                                       |
| ------------------------- | ------------------------------------------- |
| Repositorio               | github.com/ecoAPM/WiFiSurveyor              |
| Plataforma                | Windows / macOS / Linux (web local)         |
| Lenguaje principal        | TypeScript 51.7 %, C# 30.9 %, Vue.js 15.5 % |
| Licencia                  | GPL-3.0                                     |
| Estrellas / Bifurcaciones | 68 / 10                                     |
| Confirmaciones (commits)  | 273                                         |
| Issues abiertas           | 8                                           |
| KLDC estimado             | 8.0                                         |
| Esfuerzo estimado         | 23 personas-mes                             |

> _Figura 2: Captura de WiFiSurveyor mostrando un mapa de calor superpuesto al plano de un edificio._

### **_python-wifi-survey-heatmap_**

python-wifi-survey-heatmap es una herramienta de escritorio para Linux que permite registrar mediciones de señal WiFi en puntos predefinidos sobre un plano importado como imagen y posteriormente generar mapas de calor mediante interpolación espacial. Incorpora pruebas activas de ancho de banda con `iperf3` y análisis de utilización de canales. Su implementación es completamente en Python (scipy, matplotlib y wxPython Phoenix). Aunque carece de módulo de IA y se limita a Linux, implementa el flujo central del Wireless HeatMapper: captura por punto, almacenamiento en JSON y generación de heatmap continuo sobre el plano.

| Atributo                  | Valor                                         |
| ------------------------- | --------------------------------------------- |
| Repositorio               | github.com/jantman/python-wifi-survey-heatmap |
| Plataforma                | Linux (escritorio)                            |
| Lenguaje principal        | Python 98.3 %                                 |
| Licencia                  | No especificada (código abierto)              |
| Estrellas / Bifurcaciones | 467 / 92                                      |
| Confirmaciones (commits)  | 141                                           |
| Issues abiertas           | 9                                             |
| KLDC estimado             | 2.5                                           |
| Esfuerzo estimado         | 7 personas-mes                                |

> _Figura 3: Heatmap generado por python-wifi-survey-heatmap a partir de mediciones puntuales._

### Cuadro comparativo

| Métrica                     | WiFiAnalyzer | WiFiSurveyor | python-wifi-survey-heatmap | **Wireless HeatMapper** |
| --------------------------- | -----------: | -----------: | -------------------------: | ----------------------: |
| KLDC estimado               |         25.0 |          8.0 |                        2.5 |                **18.5** |
| Esfuerzo estimado (PM)      |           71 |           23 |                          7 |                  **42** |
| Issues abiertas             |            6 |            8 |                          9 |                       — |
| Calidad (errores/KLDC)      |         0.24 |         1.00 |                       3.60 |                       — |
| Productividad (LOC/PM)      |          352 |          348 |                        357 |                     350 |
| Puntos de Función ajustados |          102 |           74 |                         60 |                 **238** |

## 2.3 Caso de Estudio

El cliente real del proyecto es **Bulldog Tech.**, empresa boliviana de servicios tecnológicos con sede en Santa Cruz de la Sierra, especializada en consultoría e implementación de redes corporativas, cableado estructurado y soluciones de conectividad inalámbrica para clientes finales del sector empresarial, educativo y de hospitalidad. Sus técnicos de campo realizan, como parte de su servicio cotidiano, _site surveys_ WiFi en edificios de oficinas, plantas industriales, hoteles y campus universitarios, con el objetivo de diagnosticar la calidad de cobertura existente o de planificar el despliegue de nuevas redes.

**Problema concreto que enfrenta el cliente:** Bulldog Tech. realiza actualmente sus relevamientos con instrumentos heterogéneos (apps gratuitas de WiFi analyzer en celulares Android, hojas Excel de campo y planos impresos sobre los que se anotan a mano los valores de RSSI). Esta operativa genera tres problemas principales: (i) los datos quedan desconectados del plano, dificultando la generación posterior de mapas de calor que entreguen al cliente; (ii) los técnicos no cuentan con un único repositorio centralizado de proyectos consultable desde la oficina, lo que impide al gerente supervisar el avance del trabajo de campo; y (iii) no existe ningún mecanismo automatizado de recomendación de posicionamiento de APs, por lo que las propuestas de mejora dependen exclusivamente de la experiencia individual de cada técnico.

**Cómo el Wireless HeatMapper ayuda a Bulldog Tech.:** El sistema centraliza en línea todo el flujo del relevamiento (proyecto → plano calibrado → puntos de medición → heatmap → análisis de cobertura → recomendaciones de IA → reporte y portal de cliente), permite al administrador supervisar todos los proyectos de la organización desde el panel web y entrega al cliente final un enlace único para visualizar de forma interactiva el resultado del trabajo —elevando la calidad percibida del servicio y eliminando los retrabajos asociados a la operativa actual basada en planos y planillas en papel.

**Beneficiarios secundarios:**

- **Empresas integradoras de redes y consultoras IT** que ofrezcan servicios de site survey similares a Bulldog Tech.
- **Departamentos de TI internos** de universidades, hospitales, hoteles y centros comerciales que requieran auditar y planificar su propia red WiFi.
- **Investigadores en algoritmos de interpolación espacial e inteligencia artificial aplicada a propagación de señal**, al disponer de un repositorio de datasets reales de mediciones georreferenciadas.


# 3. Descripción del Problema

A continuación se describen las cinco dimensiones principales del problema identificadas en el dominio del _site survey_ WiFi y, en particular, en la operativa actual de Bulldog Tech.

**Falta de herramientas digitales integradas para el relevamiento WiFi en interiores.** Los técnicos de campo emplean hoy un mosaico de aplicaciones gratuitas de análisis WiFi para Android (orientadas exclusivamente a la lista de redes detectadas), planos del edificio impresos en papel sobre los que se anotan los valores de RSSI a mano y planillas Excel para consolidar los datos al regresar a la oficina. Esta fragmentación impide que los datos capturados queden geográficamente referenciados sobre el plano y obliga a tareas manuales de transcripción posteriores que introducen errores y retrasos.

**Imposibilidad de generar mapas de calor de cobertura como parte del relevamiento.** El producto entregable que el cliente final espera —un mapa de calor de la cobertura WiFi del edificio— no se produce directamente con las herramientas actuales. Cuando se entrega, es resultado de un proceso manual posterior, costoso en horas-hombre y con baja fidelidad respecto a las muestras reales tomadas. Esto reduce la calidad percibida del servicio y limita la capacidad de Bulldog Tech. para diferenciarse de competidores que ofrecen reportes visuales más profesionales.

**Ausencia de criterios objetivos para la propuesta de mejora de la red.** Cuando el técnico identifica zonas de mala cobertura, las recomendaciones que entrega al cliente —cantidad de puntos de acceso adicionales, ubicaciones óptimas, canales sugeridos— se apoyan en su experiencia personal y en estimaciones empíricas. No existe un mecanismo automatizado que, partiendo de las muestras reales de campo y de la geometría del plano, sugiera un plan de despliegue verificable contra umbrales técnicos (RSSI ≥ −70 dBm, no superposición de canales, etc.).

**Falta de centralización organizacional y trazabilidad de los proyectos.** Cada técnico gestiona sus relevamientos en sus propios archivos locales (planos en su laptop, planillas en su correo), lo que impide al administrador o gerente de Bulldog Tech. consultar de forma consolidada el estado de los proyectos en curso, su avance, los clientes asociados y los entregables pendientes. La supervisión depende hoy de comunicación informal y reportes ad-hoc.

**Imposibilidad de compartir resultados con el cliente final de forma interactiva.** Los entregables actuales son documentos PDF estáticos enviados por correo. El cliente no puede explorar interactivamente el heatmap, no puede comparar el escenario actual con el escenario propuesto y no dispone de un acceso seguro y auditable a sus propios datos. Esta limitación reduce la transparencia del servicio y dificulta la justificación técnica de la propuesta económica que se envía al cliente.


# 4. Situación Problemática

Los técnicos de campo de Bulldog Tech. carecen de un sistema integrado, en línea y multiplataforma para el relevamiento, análisis y entrega de proyectos de cobertura WiFi en interiores, lo que les obliga a operar con un mosaico fragmentado de aplicaciones móviles de análisis WiFi gratuitas, planos impresos en papel y planillas Excel desconectadas entre sí; esta operativa fragmentada genera transcripciones manuales propensas a error y retrabajo, impide referenciar geográficamente las muestras de RSSI sobre el plano del edificio y obliga a generar los mapas de calor de cobertura mediante un proceso manual y costoso posterior, lo que a su vez se traduce en entregables de baja fidelidad técnica, en propuestas de mejora basadas exclusivamente en la experiencia individual del técnico y no en criterios objetivos verificables (RSSI ≥ −70 dBm, no solapamiento de canales) y en ausencia total de centralización organizacional —por lo que el administrador no puede supervisar el avance de los proyectos en curso ni el cliente final puede acceder de forma segura e interactiva a los resultados de su propio relevamiento—, afectando finalmente la calidad percibida del servicio, la capacidad de Bulldog Tech. para diferenciarse competitivamente en el mercado boliviano de consultoría de redes y la rentabilidad operativa de la empresa al duplicar horas-hombre en consolidación manual de datos.


# 5. Situación Deseada

Una vez implementado el sistema Wireless HeatMapper en su modalidad 100 % en línea, los técnicos de campo de Bulldog Tech. logran ejecutar todo el ciclo de un proyecto de site survey desde una única aplicación móvil delgada conectada en tiempo real a un backend central que actúa como única fuente de verdad sobre PostgreSQL, desarrollando capacidades para crear y gestionar proyectos asociados a clientes catalogados, importar y calibrar planos de edificios, capturar señales WiFi (RSSI, SSID, BSSID, canal y frecuencia) y transmitirlas en línea por cada punto de medición, generar mapas de calor continuos por interpolación espacial ejecutada en el backend, recibir análisis automatizados de cobertura que identifican zonas muertas y solapamientos de canal, y obtener recomendaciones de posicionamiento óptimo de puntos de acceso producidas por un módulo de inteligencia artificial; lo que se traduce en reducción medible del tiempo de consolidación post-campo, en entregables visuales interactivos accesibles por el cliente final mediante un enlace único de portal web con autenticación por token y expiración configurable, en capacidad de supervisión organizacional por parte del administrador desde el panel web (gestión de cuentas de técnicos, catálogo de clientes y vista consolidada de todos los proyectos de la organización con su estado y actividad reciente), y en una propuesta de servicio diferenciada en el mercado boliviano sustentada en evidencia técnica medible, compartible y trazable end-to-end.


# 6. Objetivos del Proyecto

## 6.1 Objetivo General

Desarrollar un sistema integrado y estrictamente en línea, compuesto por una aplicación móvil para Android, un backend REST con módulo de inteligencia artificial y una plataforma web complementaria, que permita a los técnicos de **Bulldog Tech.** realizar el relevamiento, análisis y optimización de la cobertura de redes WiFi en espacios interiores mediante la generación de mapas de calor basados en mediciones reales transmitidas en tiempo real al backend y recomendaciones automáticas de posicionamiento de puntos de acceso apoyadas en algoritmos de aprendizaje automático; y que adicionalmente provea un panel de administración para la gestión organizacional de los técnicos y clientes y un portal de cliente para la visualización interactiva de los resultados entregados.

## 6.2 Objetivos Específicos

- **Analizar los requisitos del sistema** mediante el relevamiento del proceso actual de site survey de Bulldog Tech., la elaboración del Plan del Proyecto y la definición de los nueve requerimientos principales (RP1–RP9) que rigen el alcance funcional y no funcional del sistema.

- **Diseñar la arquitectura del sistema y la base de datos central** sobre los principios de cliente delgado en línea, separación clara en cuatro capas (presentación / aplicación / dominio / persistencia) y única fuente de verdad sobre PostgreSQL, materializada en los modelos UML de Contexto (casos de uso UC01–UC19), Arquitectura (paquetes y despliegue) y Datos (clases conceptuales, esquema lógico relacional y diseño físico).

- **Implementar el módulo de captura automática de parámetros de señal WiFi** (RSSI, SSID, BSSID, canal y frecuencia) durante el recorrido del espacio, transmitiendo cada muestra en línea al backend mediante endpoints REST autenticados con JWT, contemplando las restricciones de scan throttling impuestas por Android 8.0 y superiores.

- **Desarrollar la funcionalidad de importación y georreferenciación de planos** de edificios en formato PNG/JPG/PDF, almacenados de forma central en el backend, con calibración de escala mediante línea de referencia que permita asociar cada medición a una coordenada métrica sobre el plano.

- **Implementar algoritmos de interpolación espacial** ejecutados en el backend (interpolación de distancia inversa ponderada y/o kriging) para generar mapas de calor continuos sobre el plano del edificio.

- **Desarrollar el módulo de análisis automatizado de cobertura**, capaz de identificar zonas muertas (RSSI < −90 dBm), interferencias entre canales (CCI/ACI) y solapamientos entre puntos de acceso, conforme a los umbrales del marco CWNA-107.

- **Aplicar técnicas de inteligencia artificial** para la recomendación de posicionamiento óptimo de puntos de acceso garantizando cobertura objetivo ≥ −70 dBm, expuestas vía endpoint REST consumido tanto por la app móvil como por el portal de cliente.

- **Implementar la generación de reportes técnicos exportables** (PDF) que documenten la cobertura relevada, el análisis automático y el plan de implementación de APs propuesto.

- **Desarrollar el panel de administración web** que permita gestionar las cuentas de los técnicos (alta, baja y activación), administrar el catálogo de clientes y supervisar la totalidad de los proyectos de la organización con su estado y actividad reciente.

- **Desarrollar el portal de cliente web** que permita visualizar de forma interactiva los mapas de calor (actual y proyectado), el análisis de cobertura y el plan de APs recomendado, accesible mediante un enlace único generado por el técnico al cierre del proyecto.

- **Validar la efectividad del software** mediante pruebas unitarias y de integración (cobertura de código ≥ 80 % en backend), pruebas de aceptación con el Product Owner por cada Sprint, y pruebas de campo en instalaciones reales del cliente Bulldog Tech.


# 7. Alcance

A continuación se describen los módulos funcionales que componen el alcance del sistema, organizados por dominio y por requerimiento principal (RP) asociado.

**Módulo de captura de señal WiFi en línea (RP1).** La aplicación móvil escanea automáticamente las redes WiFi disponibles en cada punto del recorrido del técnico y registra los parámetros RSSI, SSID, BSSID, canal y frecuencia, asociándolos a la posición actual del usuario sobre el plano del edificio. Cada lote de muestras se transmite _en línea_ al backend mediante un endpoint REST autenticado con JWT, sin almacenamiento local persistente. Ante una pérdida temporal de conectividad la aplicación pausa explícitamente la captura, muestra al técnico un banner de estado de red y reanuda la operación cuando el backend confirma disponibilidad.

**Módulo de gestión de proyectos y planos (RP2).** El técnico crea proyectos asociados a un cliente del catálogo, sube el plano del edificio en formato PNG/JPG/PDF al backend y calibra su escala dibujando una línea de referencia con su longitud real conocida. El plano queda asociado al proyecto en la base de datos central PostgreSQL y se sirve al cliente móvil por URL bajo demanda. Toda operación es un request HTTPS contra el backend; no existe edición offline.

**Módulo de generación de mapa de calor (RP3).** A partir de los puntos de medición persistidos, el servicio de interpolación espacial del backend genera un mapa de calor continuo y lo devuelve al cliente para su visualización con escala de color graduada (verde para señal excelente, rojo para zona muerta o señal nula). El cliente móvil sólo solicita el heatmap actualizado y lo renderiza, liberándose de la carga computacional de la interpolación.

**Módulo de análisis automatizado de cobertura (RP4).** El backend analiza el heatmap generado para identificar zonas muertas (RSSI < −90 dBm), puntos de solapamiento excesivo entre APs e interferencias por canal (CCI/ACI), entregando los resultados al cliente como una colección estructurada de hallazgos categorizados por severidad y referenciados sobre el plano.

**Módulo de inteligencia artificial para optimización de APs (RP5).** A partir del análisis de cobertura, un modelo de aprendizaje automático hospedado en el backend sugiere la cantidad mínima de APs necesarios y sus posiciones óptimas sobre el plano para garantizar cobertura objetivo ≥ −70 dBm. El módulo entrega adicionalmente un mapa de calor _proyectado_ del escenario optimizado para comparación visual con el escenario actual.

**Módulo de generación de reportes (RP6).** El sistema permite la exportación de reportes técnicos en PDF que documentan el estado actual de la cobertura, las zonas problemáticas identificadas, las recomendaciones de la IA y el plan de implementación propuesto, en un formato adecuado para entregar al cliente como cierre del proyecto.

**Módulo de administración web (RP7).** El panel web provee al administrador de Bulldog Tech. cuatro funciones principales: (i) gestión de cuentas de técnicos (alta, baja y activación), (ii) administración del catálogo de clientes, (iii) listado consolidado de todos los proyectos de la organización con filtros por técnico, estado y rango de fechas, y (iv) operaciones administrativas sobre los proyectos (archivar, reasignar entre técnicos).

**Persistencia centralizada en línea (RP8).** Todas las entidades del dominio (proyectos, planos calibrados, puntos de medición, mediciones WiFi, análisis y heatmaps) residen exclusivamente en la base de datos central PostgreSQL. La aplicación móvil opera como cliente REST autenticado con JWT y no mantiene estado de dominio entre ejecuciones; al iniciar sesión, el técnico recupera del backend el listado de sus proyectos y todas las operaciones posteriores se realizan en línea.

**Portal de cliente web (RP9).** El técnico genera al cierre del proyecto un enlace único (token UUID firmado, expiración configurable, contador de accesos auditable) que permite al cliente acceder a un portal web sin instalar la aplicación móvil. El portal muestra el heatmap actual, el heatmap proyectado, el análisis de cobertura y el plan de APs recomendado de forma interactiva.

> **Nota sobre exclusiones del alcance:** El sistema **no implementa** un modo desconectado ni mecanismos de sincronización diferida (modalidad 100 % en línea por diseño); **no implementa** medición activa de ancho de banda con `iperf3` (a diferencia de python-wifi-survey-heatmap); **no implementa** posicionamiento automático del técnico por SLAM o triangulación inercial (la posición se marca manualmente sobre el plano); y **no contempla** despliegue multi-tenant con múltiples organizaciones (Bulldog Tech. es la única organización en la primera versión).


# 8. Tecnología

## 8.1 Estrategia

El proyecto adopta el **marco de trabajo Scrum**. Scrum se selecciona porque es un marco iterativo e incremental que se adapta a proyectos de cuatro a seis meses, permite entregar valor de forma temprana al cliente real (Bulldog Tech.) y está diseñado para equipos pequeños multifuncionales y autogestionados (en este caso, dos personas que cubren los roles de Scrum Master, Product Owner y Developer simultáneamente). La estrategia Scrum se complementa con las cuatro actividades obligatorias de la ingeniería de software (análisis, diseño, implementación y pruebas) y se materializa en cinco eventos —**R-1** Definición Inicial, **R-2** Sprint Planning, **R-3** Ejecución (con Daily Scrum), **R-4** Sprint Review y **R-5** Sprint Retrospective— y tres artefactos —**F3** Product Backlog, **F4** Historias de Usuario y **F5** Sprint Backlog—.

## 8.2 Métodos

- **Lenguaje de modelado:** UML 2.5+ con la herramienta **StarUML** y diagramas embebidos en formato **PlantUML** dentro de los documentos Markdown, para garantizar diagramas versionables en Git y renderizables tanto en VS Code como en la cadena de generación del Word final.
- **Modelado de Casos de Uso (UC01–UC19):** diagrama de Contexto del sistema, conforme al estándar UML.
- **Modelado de Arquitectura:** diagrama de Paquetes en cuatro capas y diagrama de Despliegue de los contenedores Docker.
- **Modelado de Datos:** diagrama de Clases conceptual, esquema lógico relacional y diseño físico PostgreSQL.
- **Modelado de Lógica:** diagramas de Secuencia y de Estados para las HU con flujo de negocio complejo.
- **Estimación de tamaño y esfuerzo:** Métricas de Pressman (KLDC, Puntos de Función), modelo COCOMO II y Ecuación del Software de Putnam–Myers; estimación de PHU mediante **Planning Poker** con escala de Fibonacci (1, 2, 3, 5, 8, 13, 21).
- **Algoritmos de IA y procesamiento de señal:** interpolación espacial (Inverse Distance Weighting / Kriging) en el backend, y modelo de aprendizaje supervisado para recomendación de posicionamiento de APs (entrenamiento con datasets sintéticos y reales de propagación de señal).
- **Fundamento técnico WiFi:** marco de referencia **CWNA-107**, con umbrales operativos RSSI ≥ −70 dBm para diseño objetivo y < −90 dBm para zona muerta.

## 8.3 Herramientas

### Herramientas de Software

| Categoría                   | Herramienta                                                                   |
| --------------------------- | ----------------------------------------------------------------------------- |
| Control de versiones        | Git, GitHub                                                                   |
| Gestión del Product Backlog | Notion (sincronizado con scripts Python), GitHub Projects                     |
| Modelado UML                | StarUML 6, PlantUML (embebido en Markdown)                                    |
| Diseño UI/UX                | Figma (prototipos), Material 3 Design Kit                                     |
| Lenguaje móvil              | Dart                                                                          |
| Framework móvil             | Flutter SDK 3.x · BLoC/Cubit · Dio · go_router · flutter_secure_storage       |
| Lenguaje backend            | Python 3.12                                                                   |
| Framework backend           | FastAPI · SQLAlchemy 2.x · Alembic · python-jose (JWT) · bcrypt               |
| Lenguaje web                | TypeScript 5.x                                                                |
| Framework web               | React 18 + Vite + TanStack Query + axios + react-router-dom + react-hook-form |
| Estilo web                  | CSS Modules + tokens de color/tipografía (Poppins, Inter)                     |
| Base de datos               | PostgreSQL 15+                                                                |
| Contenerización             | Docker · Docker Compose                                                       |
| Reverse proxy / TLS         | Nginx (`/api → backend`, `/admin → web`, `/ → portal cliente`)                |
| Calidad de código (backend) | ruff, ruff-format, pytest, pytest-cov                                         |
| Calidad de código (web)     | ESLint, Prettier, Vitest                                                      |
| Calidad de código (móvil)   | dart analyze, dart format, flutter test                                       |
| Pre-commit hooks            | pre-commit (ruff, prettier, eslint, dart format)                              |
| CI/CD                       | GitHub Actions (lint + tests + build de imagen Docker + push)                 |
| Editor / IDE                | Visual Studio Code · Android Studio · DataGrip                                |
| Documentación               | Markdown · Pandoc (generación del .docx final) · LaTeX (opcional)             |
| Modelo de IA                | scikit-learn · TensorFlow / ONNX Runtime (despliegue en backend)              |
| Servidor cloud              | VPS Linux (Render, Fly.io o equivalente)                                      |

### Herramientas de Hardware

- **Computadoras portátiles de desarrollo (×2):** equipos de los autores con Linux/macOS, mínimo 16 GB de RAM, para ejecutar Docker Compose, Android emulator y entornos de desarrollo simultáneos.
- **Smartphones Android (×2)** con API ≥ 26 (Android 8.0 Oreo) para pruebas en dispositivo físico (siempre en línea).
- **Enrutadores WiFi de prueba (×2)** para construir entornos controlados de validación del algoritmo de interpolación y del módulo de análisis de cobertura.
- **Impresora** para impresión de planos durante pruebas de campo en instalaciones reales de Bulldog Tech.


# 9. Cronograma

La planificación temporal del proyecto se organiza en **siete iteraciones** alineadas con el marco Scrum: un Sprint inicial de definición (Sprint 0, una semana), seis Sprints de desarrollo de dos semanas (Sprints 1 al 6) y una semana de cierre para pruebas integradas y entrega final. La **revisión conjunta del Sprint 0 + Sprint 1 se realiza el 27 de abril de 2026**, conforme al hito M0 del plan.

A continuación se presenta un Diagrama de Gantt por cada Sprint (vista general, Sprint 0 y Sprint 1; los Sprints 2 al 6 figuran en el Plan de Implementación vigente).

## 9.1 Diagrama de Gantt — Plan general


> _Figura 4: Diagrama de Gantt general — distribución de Sprints del Wireless HeatMapper, abril–julio 2026._

## 9.2 Diagrama de Gantt — Sprint 0 (Definición Inicial)


> _Figura 5: Diagrama de Gantt — Sprint 0 (Definición Inicial), 13–17 abril 2026._

## 9.3 Diagrama de Gantt — Sprint 1 (Fundación CRUD)


> _Figura 6: Diagrama de Gantt — Sprint 1 (Fundación CRUD), 20–26 abril 2026._

## 9.4 Sprints 2 al 6 (vista resumida)

| Sprint   | Período            | HU                  | PHU | Objetivo del Sprint                                                |
| -------- | ------------------ | ------------------- | --: | ------------------------------------------------------------------ |
| Sprint 2 | 28 abr – 11 may 26 | PB-02, PB-11        |  16 | Planos en línea (importar + calibrar)                              |
| Sprint 3 | 12 may – 25 may 26 | PB-03, PB-04        |  21 | Captura WiFi en línea con ingesta REST                             |
| Sprint 4 | 26 may – 8 jun 26  | PB-05, PB-06        |  26 | Heatmap (interpolación backend) + análisis automático de cobertura |
| Sprint 5 | 9 jun – 22 jun 26  | PB-07, PB-12, PB-08 |  42 | IA, comparación de escenarios y exportación de reportes            |
| Sprint 6 | 23 jun – 6 jul 26  | PB-15, PB-16, PB-17 |  26 | Portal de cliente y enlace único                                   |
| Cierre   | 7 jul – 11 jul 26  | RP6 + integración   |   — | Pruebas integradas, ajustes finales y entrega                      |

**Total Sprints 1–6 = 160 PHU**.


# 10. Proceso de Desarrollo SCRUM

## 10.1 Definiciones del Proceso de Desarrollo

### 10.1.1 Marco de trabajo

El proyecto adopta **Scrum** como marco de trabajo. Scrum es un **marco de trabajo**, no una metodología prescriptiva: define eventos, roles y artefactos pero no indica cómo se hace ingeniería. Para este proyecto, Scrum se integra con las cuatro actividades obligatorias de la ingeniería de software:

| #   | Actividad      | Cuándo ocurre                  | Responsable principal                     |
| --- | -------------- | ------------------------------ | ----------------------------------------- |
| 1   | Análisis       | Sprint Planning (R-2)          | Product Owner + equipo                    |
| 2   | Diseño         | Ejecución del Sprint (R-3)     | Equipo de desarrollo                      |
| 3   | Implementación | Ejecución del Sprint (R-3)     | Equipo de desarrollo                      |
| 4   | Pruebas        | Ejecución + Review (R-3 / R-4) | Dev (1.er filtro) · QA (2.do) · PO (3.er) |

El proceso es **incremental** (cada Sprint añade valor sobre el anterior) e **iterativo** (cada Sprint repite las cuatro actividades).

### 10.1.2 Ciclo de vida


> _Figura 7: Ciclo de vida Scrum aplicado a Wireless HeatMapper, integrado con las cuatro actividades obligatorias de ingeniería de software._

### 10.1.3 Eventos Scrum

| Evento                                | Cuándo                | Duración    | Resultado                                       |
| ------------------------------------- | --------------------- | ----------- | ----------------------------------------------- |
| **R-1 Definición Inicial (Sprint 0)** | Antes del Sprint 1    | 1 semana    | Modelos base + Product Backlog (F3) + infra     |
| **R-2 Sprint Planning**               | Inicio de cada Sprint | ≤ 4 horas   | Sprint Backlog (F5) + objetivo del Sprint       |
| **R-3 Ejecución del Sprint**          | Durante el Sprint     | 2 semanas   | Incremento operativo (deployable)               |
| **R-3.1 Daily Scrum**                 | Cada día del Sprint   | 15 minutos  | Sincronización + identificación de impedimentos |
| **R-4 Sprint Review**                 | Último día del Sprint | ≤ 2 horas   | Demo + Product Backlog actualizado              |
| **R-5 Sprint Retrospective**          | Después del Review    | ≤ 1.5 horas | Plan de mejora para el siguiente Sprint         |

### 10.1.4 Equipo SCRUM

| Persona                            | Rol                     | Descripción                                                             |
| ---------------------------------- | ----------------------- | ----------------------------------------------------------------------- |
| Herland Borys Quiroga Flores       | **Product Owner / Dev** | Gestión del Product Backlog, validación con cliente real, dev móvil/web |
| Jhasmany Jhunnior Fernandez Ortega | **Scrum Master / Dev**  | Facilitación de ceremonias, eliminación de impedimentos, dev backend/IA |
| Ambos                              | **Developers**          | Multifuncionales (backend, móvil, web, IA) y autogestionados            |

Adicionalmente:

- **Cliente real:** Bulldog Tech. — aceptación funcional de los incrementos.


> _Figura 8: Equipo Scrum del proyecto — distribución de roles y multifuncionalidad._

### 10.1.5 Objetivo del Producto

> **Objetivo del Producto:** Proveer a Bulldog Tech. y a sus clientes finales una solución integral, en línea y multiplataforma para el relevamiento, análisis y optimización de la cobertura WiFi en interiores, que sustituya el flujo manual actual (apps de WiFi analyzer + planos impresos + planillas Excel) por un proceso digital end-to-end con captura georreferenciada en tiempo real, generación automatizada de mapas de calor por interpolación espacial, análisis automático de cobertura y recomendaciones de posicionamiento de APs producidas por inteligencia artificial, accesible para los clientes finales mediante un portal web con enlace único.

### 10.1.6 Duración de los Sprints

| Sprint   | Inicio     | Fin        | Duración  |
| -------- | ---------- | ---------- | --------- |
| Sprint 0 | 13/04/2026 | 17/04/2026 | 1 semana  |
| Sprint 1 | 20/04/2026 | 26/04/2026 | 1 semana¹ |
| Sprint 2 | 28/04/2026 | 11/05/2026 | 2 semanas |
| Sprint 3 | 12/05/2026 | 25/05/2026 | 2 semanas |
| Sprint 4 | 26/05/2026 | 08/06/2026 | 2 semanas |
| Sprint 5 | 09/06/2026 | 22/06/2026 | 2 semanas |
| Sprint 6 | 23/06/2026 | 06/07/2026 | 2 semanas |
| Cierre   | 07/07/2026 | 11/07/2026 | 1 semana  |

¹ El Sprint 1 se ejecuta en una semana acelerada para coincidir con la revisión conjunta S0+S1 del 27 de abril de 2026 (hito M0). Los Sprints 2–6 mantienen la duración estándar de dos semanas.

### 10.1.7 Definition of Done (acordada en Sprint 0)

| Criterio                            | Verificación                                                     |
| ----------------------------------- | ---------------------------------------------------------------- |
| Código implementado en backend      | Endpoints REST documentados con OpenAPI/Swagger                  |
| Código implementado en cliente      | Móvil (Flutter) y/o web (React) consumiendo los endpoints        |
| Migraciones Alembic aplicadas       | Esquema PostgreSQL versionado y reversible                       |
| Pruebas unitarias                   | Cobertura ≥ 70 % en módulos nuevos del backend                   |
| Pruebas de integración              | Tests de endpoints contra BD efímera (pytest + httpx)            |
| Criterios de aceptación validados   | El PO ejecuta cada CA contra el incremento desplegado            |
| Code review aprobado                | Pull Request revisado por el otro miembro del equipo             |
| Mergeado a `main`                   | Squash-merge desde rama `feature/PB-XX-slug`                     |
| Despliegue automático               | Pipeline GitHub Actions construye imagen Docker                  |
| Sin almacenamiento local de dominio | El cliente móvil no persiste entidades de dominio entre sesiones |

### 10.1.8 Product Backlog (F3)

**Versión:** 2.0 (ajustada a modalidad 100 % en línea) · **Product Owner:** Herland Borys Quiroga Flores · **Fecha:** abril 2026.

**Cambios respecto al backlog original (modalidad offline):**

| Cambio                                      | Razón                                                                           |
| ------------------------------------------- | ------------------------------------------------------------------------------- |
| **PB-14 eliminado**                         | "Sincronizar proyecto al servidor" no aplica: toda operación ya es online       |
| **PB-13 (admin) reubicado al Sprint 1**     | El pre-aprovisionamiento de técnicos es prerrequisito de la autenticación móvil |
| **PB-01 y PB-10 adelantados al Sprint 1**   | El CRUD móvil de proyectos quedó implementado; se consolida la fundación CRUD   |
| **Estimaciones de PB-03 y PB-05 ajustadas** | El cliente delgado en línea reduce la carga de implementación móvil             |
| **PB-09 redefinido**                        | Autenticación contra backend con JWT (no contra SQLite local)                   |
| **PB-02 redefinido**                        | El plano se sube al backend; el cliente solo lo solicita por URL firmada        |

**Diagrama de estados del Product Backlog:**


> _Figura 9: Diagrama de estados de las Historias de Usuario en el Product Backlog del Wireless HeatMapper._

**Product Backlog completo.** Las prioridades se expresan como Alta, Media y Baja. Los PHU corresponden a Puntos de Historia en escala de Fibonacci (1, 2, 3, 5, 8, 13, 21). A continuación se presenta primero un cuadro resumen y luego el detalle de cada Historia en formato de formulario tabular.

**Cuadro resumen del Product Backlog:**

| Id        | Nombre corto                             | Prioridad | PHU | Sprint   | RP  | Estado    |
| --------- | ---------------------------------------- | --------- | --: | -------- | --- | --------- |
| PB-13     | Gestionar usuarios (admin web)           | Alta      |   8 | Sprint 1 | RP7 | Done      |
| PB-19     | Gestionar clientes (admin web)           | Alta      |   3 | Sprint 1 | RP7 | Done      |
| PB-09     | Autenticar usuario (móvil)               | Alta      |   5 | Sprint 1 | RP8 | Done      |
| PB-18     | Ver proyectos de la organización         | Baja      |   5 | Sprint 1 | RP7 | Done      |
| PB-01     | Gestionar proyecto de survey             | Alta      |   5 | Sprint 1 | RP8 | Done      |
| PB-10     | Ver historial de proyectos               | Media     |   3 | Sprint 1 | RP8 | Done      |
| PB-02     | Importar plano de edificio               | Alta      |   8 | Sprint 2 | RP2 | Estimada  |
| PB-11     | Calibrar escala del plano                | Alta      |   8 | Sprint 2 | RP2 | Estimada  |
| PB-03     | Capturar señales WiFi (en línea)         | Alta      |  13 | Sprint 3 | RP1 | Estimada  |
| PB-04     | Marcar puntos de medición                | Alta      |   8 | Sprint 3 | RP2 | Estimada  |
| PB-05     | Generar mapa de calor                    | Alta      |  13 | Sprint 4 | RP3 | Estimada  |
| PB-06     | Analizar cobertura automáticamente       | Alta      |  13 | Sprint 4 | RP4 | Estimada  |
| PB-07     | Obtener recomendaciones de APs por IA    | Alta      |  21 | Sprint 5 | RP5 | Estimada  |
| PB-12     | Comparar escenario actual vs propuesto   | Media     |   8 | Sprint 5 | RP5 | Estimada  |
| PB-08     | Exportar reporte técnico                 | Media     |  13 | Sprint 5 | RP6 | Estimada  |
| PB-15     | Generar enlace de cliente                | Media     |   5 | Sprint 6 | RP9 | Estimada  |
| PB-16     | Ver heatmap interactivo (portal cliente) | Media     |  13 | Sprint 6 | RP9 | Estimada  |
| PB-17     | Ver análisis y plan AP (portal cliente)  | Media     |   8 | Sprint 6 | RP9 | Estimada  |
| ~~PB-14~~ | ~~Sincronizar proyecto al servidor~~     | —         |   — | N/A      | —   | Eliminada |

**Detalle de cada Historia de Usuario (formato F4 — formulario):**

**PB-13 — Gestionar usuarios (admin web)**

| Campo           | Contenido                                                               |
| --------------- | ----------------------------------------------------------------------- |
| Prioridad / PHU | Alta · 8                                                                |
| Sprint / RP     | Sprint 1 · RP7                                                          |
| Estado          | Done                                                                    |
| Como            | Administrador                                                           |
| Quiero          | Crear, activar y desactivar cuentas de técnicos desde el panel web      |
| Para            | Controlar el acceso al sistema sin intervenir el código de la app móvil |

**PB-19 — Gestionar clientes (admin web)**

| Campo           | Contenido                                           |
| --------------- | --------------------------------------------------- |
| Prioridad / PHU | Alta · 3                                            |
| Sprint / RP     | Sprint 1 · RP7                                      |
| Estado          | Done                                                |
| Como            | Administrador                                       |
| Quiero          | Crear y gestionar clientes desde el panel web       |
| Para            | Que los técnicos los seleccionen al crear proyectos |

**PB-09 — Autenticar usuario (móvil)**

| Campo           | Contenido                                  |
| --------------- | ------------------------------------------ |
| Prioridad / PHU | Alta · 5                                   |
| Sprint / RP     | Sprint 1 · RP8                             |
| Estado          | Done                                       |
| Como            | Técnico de campo                           |
| Quiero          | Iniciar sesión en la app contra el backend |
| Para            | Acceder solo a mis proyectos               |

**PB-18 — Ver proyectos de la organización**

| Campo           | Contenido                                                                      |
| --------------- | ------------------------------------------------------------------------------ |
| Prioridad / PHU | Baja · 5                                                                       |
| Sprint / RP     | Sprint 1 · RP7                                                                 |
| Estado          | Done                                                                           |
| Como            | Administrador                                                                  |
| Quiero          | Ver todos los proyectos de todos los técnicos con su estado y última actividad |
| Para            | Supervisar el trabajo de campo                                                 |

**PB-01 — Gestionar proyecto de survey**

| Campo           | Contenido                                                  |
| --------------- | ---------------------------------------------------------- |
| Prioridad / PHU | Alta · 5                                                   |
| Sprint / RP     | Sprint 1 · RP8                                             |
| Estado          | Done                                                       |
| Como            | Técnico                                                    |
| Quiero          | Crear, editar, archivar y eliminar proyectos en el backend |
| Para            | Organizar mis mediciones por edificio o cliente            |

**PB-10 — Ver historial de proyectos**

| Campo           | Contenido                                       |
| --------------- | ----------------------------------------------- |
| Prioridad / PHU | Media · 3                                       |
| Sprint / RP     | Sprint 1 · RP8                                  |
| Estado          | Done                                            |
| Como            | Técnico                                         |
| Quiero          | Ver mis proyectos con estado y última actividad |
| Para            | Retomarlos o consultarlos rápidamente           |

**PB-02 — Importar plano de edificio**

| Campo           | Contenido                                                            |
| --------------- | -------------------------------------------------------------------- |
| Prioridad / PHU | Alta · 8                                                             |
| Sprint / RP     | Sprint 2 · RP2                                                       |
| Estado          | Estimada                                                             |
| Como            | Técnico                                                              |
| Quiero          | Subir un plano (PNG/JPG/PDF) al backend asociado a un proyecto       |
| Para            | Disponer de un soporte gráfico georreferenciable para las mediciones |

**PB-11 — Calibrar escala del plano**

| Campo           | Contenido                                                               |
| --------------- | ----------------------------------------------------------------------- |
| Prioridad / PHU | Alta · 8                                                                |
| Sprint / RP     | Sprint 2 · RP2                                                          |
| Estado          | Estimada                                                                |
| Como            | Técnico                                                                 |
| Quiero          | Definir la escala real del plano dibujando una línea de referencia      |
| Para            | Convertir distancias en píxeles a metros reales en cálculos posteriores |

**PB-03 — Capturar señales WiFi (en línea)**

| Campo           | Contenido                                                           |
| --------------- | ------------------------------------------------------------------- |
| Prioridad / PHU | Alta · 13                                                           |
| Sprint / RP     | Sprint 3 · RP1                                                      |
| Estado          | Estimada                                                            |
| Como            | Técnico                                                             |
| Quiero          | Que la app escanee redes WiFi y envíe cada lote en línea al backend |
| Para            | Persistir mediciones de RSSI georreferenciadas sin estado local     |

**PB-04 — Marcar puntos de medición**

| Campo           | Contenido                                                     |
| --------------- | ------------------------------------------------------------- |
| Prioridad / PHU | Alta · 8                                                      |
| Sprint / RP     | Sprint 3 · RP2                                                |
| Estado          | Estimada                                                      |
| Como            | Técnico                                                       |
| Quiero          | Marcar la posición de cada punto sobre el plano               |
| Para            | Asociar mediciones a coordenadas precisas dentro del edificio |

**PB-05 — Generar mapa de calor**

| Campo           | Contenido                                                            |
| --------------- | -------------------------------------------------------------------- |
| Prioridad / PHU | Alta · 13                                                            |
| Sprint / RP     | Sprint 4 · RP3                                                       |
| Estado          | Estimada                                                             |
| Como            | Técnico                                                              |
| Quiero          | Ver un mapa de calor continuo sobre el plano generado por el backend |
| Para            | Visualizar la cobertura WiFi de manera intuitiva                     |

**PB-06 — Analizar cobertura automáticamente**

| Campo           | Contenido                                                                     |
| --------------- | ----------------------------------------------------------------------------- |
| Prioridad / PHU | Alta · 13                                                                     |
| Sprint / RP     | Sprint 4 · RP4                                                                |
| Estado          | Estimada                                                                      |
| Como            | Técnico                                                                       |
| Quiero          | Que el backend identifique zonas muertas (< −90 dBm), solapamientos y CCI/ACI |
| Para            | Diagnosticar problemas de cobertura sin análisis manual                       |

**PB-07 — Obtener recomendaciones de APs por IA**

| Campo           | Contenido                                                                                |
| --------------- | ---------------------------------------------------------------------------------------- |
| Prioridad / PHU | Alta · 21                                                                                |
| Sprint / RP     | Sprint 5 · RP5                                                                           |
| Estado          | Estimada                                                                                 |
| Como            | Técnico                                                                                  |
| Quiero          | Que el backend (IA) sugiera posiciones óptimas para APs garantizando cobertura ≥ −70 dBm |
| Para            | Optimizar la red WiFi del cliente con criterios técnicos objetivos                       |

**PB-12 — Comparar escenario actual vs propuesto**

| Campo           | Contenido                                                                           |
| --------------- | ----------------------------------------------------------------------------------- |
| Prioridad / PHU | Media · 8                                                                           |
| Sprint / RP     | Sprint 5 · RP5                                                                      |
| Estado          | Estimada                                                                            |
| Como            | Técnico                                                                             |
| Quiero          | Ver el heatmap actual junto al heatmap proyectado del escenario optimizado de la IA |
| Para            | Cuantificar la mejora esperada antes de ejecutar cambios físicos                    |

**PB-08 — Exportar reporte técnico**

| Campo           | Contenido                                                                |
| --------------- | ------------------------------------------------------------------------ |
| Prioridad / PHU | Media · 13                                                               |
| Sprint / RP     | Sprint 5 · RP6                                                           |
| Estado          | Estimada                                                                 |
| Como            | Técnico                                                                  |
| Quiero          | Exportar un reporte PDF con heatmap actual, análisis y plan AP propuesto |
| Para            | Entregar un documento profesional al cliente                             |

**PB-15 — Generar enlace de cliente**

| Campo           | Contenido                                                                              |
| --------------- | -------------------------------------------------------------------------------------- |
| Prioridad / PHU | Media · 5                                                                              |
| Sprint / RP     | Sprint 6 · RP9                                                                         |
| Estado          | Estimada                                                                               |
| Como            | Técnico                                                                                |
| Quiero          | Generar un enlace único (token + expiración) para compartir un proyecto con el cliente |
| Para            | Permitir el acceso seguro al portal de cliente sin crear cuentas formales              |

**PB-16 — Ver heatmap interactivo (portal cliente)**

| Campo           | Contenido                                                                      |
| --------------- | ------------------------------------------------------------------------------ |
| Prioridad / PHU | Media · 13                                                                     |
| Sprint / RP     | Sprint 6 · RP9                                                                 |
| Estado          | Estimada                                                                       |
| Como            | Cliente                                                                        |
| Quiero          | Acceder por enlace único a una vista web con el heatmap actual y el proyectado |
| Para            | Comprender la cobertura WiFi de mi propio edificio                             |

**PB-17 — Ver análisis y plan AP (portal cliente)**

| Campo           | Contenido                                                                          |
| --------------- | ---------------------------------------------------------------------------------- |
| Prioridad / PHU | Media · 8                                                                          |
| Sprint / RP     | Sprint 6 · RP9                                                                     |
| Estado          | Estimada                                                                           |
| Como            | Cliente                                                                            |
| Quiero          | Ver el análisis de cobertura y las posiciones recomendadas de APs en el portal web |
| Para            | Tomar decisiones informadas sobre la inversión en infraestructura WiFi             |

**PB-14 — Sincronizar proyecto al servidor (eliminada)**

| Campo         | Contenido                                                                                                              |
| ------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Estado        | Eliminada en modalidad online                                                                                          |
| Justificación | Todas las operaciones ya se realizan contra el backend en línea; la sincronización diferida deja de aplicar por diseño |

**Resumen por Sprint:**

| Sprint    | HU                                       | PHU         | Objetivo del Sprint                                                |
| --------- | ---------------------------------------- | ----------- | ------------------------------------------------------------------ |
| Sprint 1  | PB-13, PB-19, PB-09, PB-18, PB-01, PB-10 | 29          | Backend base + admin web + auth móvil + CRUD proyectos móvil       |
| Sprint 2  | PB-02, PB-11                             | 16          | Planos en línea (importar + calibrar)                              |
| Sprint 3  | PB-03, PB-04                             | 21          | Captura WiFi en línea con ingesta REST                             |
| Sprint 4  | PB-05, PB-06                             | 26          | Heatmap (interpolación backend) + análisis automático de cobertura |
| Sprint 5  | PB-07, PB-12, PB-08                      | 42          | IA, comparación de escenarios y exportación de reportes            |
| Sprint 6  | PB-15, PB-16, PB-17                      | 26          | Portal de cliente y enlace único                                   |
| **TOTAL** |                                          | **160 PHU** |                                                                    |


# 10.2 Sprint 0 — Definición Inicial (R-1)

**Referencia Scrum:** R-1 — Definición Inicial
**Duración:** 1 semana (5 días hábiles) · **13 abr – 17 abr 2026**
**Estado:** Implementado
**Objetivo del Sprint 0:** Dejar listo el entorno de desarrollo y operación para que el Sprint 1 pueda iniciar con un backend desplegable, base de datos inicializada, pipeline CI/CD funcionando y modelos UML aprobados.

## 10.2.1 Justificación del Sprint 0

El Sprint 0 fue **obligatorio** en este proyecto por tres razones:

- Es la primera vez que el equipo trabaja con la modalidad 100 % en línea: había que cablear la integración entre Docker Compose, Nginx, FastAPI y PostgreSQL antes de poder hablar de funcionalidad de negocio.
- Antes de hacer Sprint Planning era necesario tener un Product Backlog ordenado (F3) y un esqueleto de arquitectura validado por el PO.
- El cliente de tipos del frontend (`openapi-typescript`) depende del OpenAPI publicado por el backend, por lo que el backend "vacío pero corriendo" debía existir desde el día 1 del Sprint 1.

## 10.2.2 Tareas del Sprint 0

| Id        | Tarea                                                                               | Responsable |     Estim. | Estado       |
| --------- | ----------------------------------------------------------------------------------- | ----------- | ---------: | ------------ |
| Sp0-01    | Definir equipo Scrum, roles y formato de Daily                                      | Ambos       |     0.5 hr | Terminado |
| Sp0-02    | Confirmar objetivo del producto y del proyecto                                      | Borys (PO)  |       1 hr | Terminado |
| Sp0-03    | Refinar y aprobar el Product Backlog (F3) ajustado a modalidad online               | Borys (PO)  |      3 hrs | Terminado |
| Sp0-04    | Aprobar duración estándar de Sprint = 2 semanas                                     | Ambos       |     0.5 hr | Terminado |
| Sp0-05    | Definir Definition of Done                                                          | Ambos       |       1 hr | Terminado |
| Sp0-06    | Aprobar diagramas: Contexto, Arquitectura (paquetes + despliegue), Datos            | Ambos       |      4 hrs | Terminado |
| Sp0-07    | Crear repositorio GitHub con estructura de monorepo (`backend/`, `mobile/`, `web/`) | Jhasmany    |      2 hrs | Terminado |
| Sp0-08    | Crear `docker-compose.yml` con servicios `db`, `backend`, `web`, `nginx`            | Jhasmany    |      4 hrs | Terminado |
| Sp0-09    | Crear `Dockerfile` del backend (Python 3.12 + Uvicorn) y `pyproject.toml` mínimo    | Jhasmany    |      3 hrs | Terminado |
| Sp0-10    | Crear endpoint `GET /api/health` que retorna `{"status":"ok","db":"ok"}`            | Jhasmany    |      2 hrs | Terminado |
| Sp0-11    | Configurar Alembic con migración inicial vacía                                      | Jhasmany    |      2 hrs | Terminado |
| Sp0-12    | Inicializar proyecto Flutter `mobile/` con BLoC + Dio + go_router                   | Borys       |      2 hrs | Terminado |
| Sp0-13    | Inicializar proyecto Web `web/` (Vite + React + TS + TanStack Query + axios)        | Borys       |      2 hrs | Terminado |
| Sp0-14    | Configurar `nginx/nginx.conf` con `/api → backend:8000` y `/ → web`                 | Jhasmany    |      2 hrs | Terminado |
| Sp0-15    | Configurar GitHub Actions: lint + tests + build de imagen Docker                    | Jhasmany    |      4 hrs | Terminado |
| Sp0-16    | Configurar pre-commit (ruff + ruff-format, prettier, eslint)                        | Borys       |       1 hr | Terminado |
| Sp0-17    | Documentar guía de ejecución local en README de cada componente                     | Ambos       |      2 hrs | Terminado |
| **TOTAL** |                                                                                     |             | **36 hrs** |              |

## 10.2.3 Diagrama de actividades del Sprint 0


> _Figura 10: Diagrama de actividades del Sprint 0 — Definición Inicial._

## 10.2.4 Modelos UML aprobados en el Sprint 0

### 10.2.4.1 Modelo de Contexto (Casos de Uso)


> _Figura 11: Modelo de Contexto del sistema (Diagrama de Casos de Uso UML 2.5) — UC01 a UC19, con desglose por Sprint._

### 10.2.4.2 Modelo de Arquitectura — Diagrama de Paquetes


> _Figura 12: Modelo de Arquitectura — Diagrama de Paquetes en cuatro capas._

### 10.2.4.3 Modelo de Arquitectura — Diagrama de Despliegue


> _Figura 13: Modelo de Arquitectura — Diagrama de Despliegue de los contenedores Docker._

### 10.2.4.4 Modelo de Datos (vista conceptual de Sprint 1)

El diagrama de Clases de la base de datos correspondiente al estado al cierre del Sprint 0/Sprint 1 se presenta en el bloque de Diseño de Datos del Sprint 1 (sección 10.3.4). Las entidades incluidas en la versión inicial del esquema son **Usuario**, **RefreshToken**, **Cliente** y **Proyecto**, con sus respectivas tablas, restricciones y claves foráneas.

## 10.2.5 Definition of Ready para el Sprint 1 (verificada al cierre del Sprint 0)

| Criterio                                                        | Estado |
| --------------------------------------------------------------- | ------ |
| Repositorio GitHub creado y accesible para ambos miembros       | Sí |
| `docker compose up` levanta los 4 servicios sin errores         | Sí |
| `curl http://localhost/api/health` → `200 OK`                   | Sí |
| Migración inicial Alembic aplicada en `db`                      | Sí |
| Pipeline CI verde en `main`                                     | Sí |
| Modelos UML (contexto, arquitectura, datos) aprobados por el PO | Sí |
| Product Backlog (F3) aprobado y ordenado por el PO              | Sí |


# 10.3 Sprint 1 — Sprint Planning (R-2)

**Evento:** R-2 Sprint Planning
**Sprint:** 1 — Fundación Backend + Admin Web + Auth Móvil + CRUD Proyectos
**Fecha de inicio:** 20 de abril de 2026
**Fecha de fin:** 26 de abril de 2026
**Capacidad:** ~80 hrs (2 devs × 4 hrs/día × 5 días hábiles × 2)
**PHU comprometidos:** 29

## 10.3.1 Objetivo del Sprint 1

> **Objetivo del Sprint 1:** Disponer de un backend que autentica usuarios con JWT, un panel web donde el administrador crea técnicos y clientes y supervisa los proyectos de la organización, una pantalla de login móvil que valida credenciales contra el backend en línea, y un CRUD completo de proyectos en la app móvil para que el técnico pueda crear, listar, editar, archivar y eliminar proyectos asociados a un cliente. Al cierre, un técnico recién creado puede iniciar sesión desde la app, gestionar sus proyectos y dejarlos listos para recibir planos en el Sprint 2.

## 10.3.2 Historias de Usuario seleccionadas (Planning Poker)

| HU        | Nombre                               | PHU    | Técnica de estimación |
| --------- | ------------------------------------ | ------ | --------------------- |
| PB-13     | Gestionar usuarios (admin web)       | 8      | Planning Poker        |
| PB-19     | Gestionar clientes (admin web)       | 3      | Planning Poker        |
| PB-09     | Autenticar usuario (móvil)           | 5      | Planning Poker        |
| PB-18     | Ver proyectos de la organización     | 5      | Planning Poker        |
| PB-01     | Gestionar proyecto de survey (móvil) | 5      | Planning Poker        |
| PB-10     | Ver historial de proyectos           | 3      | Planning Poker        |
| **Total** |                                      | **29** |                       |

## 10.3.3 Diagrama de relación entre HU del Sprint 1


> _Figura 14: Diagrama de relación entre las Historias de Usuario del Sprint 1._


# 10.4 Historias de Usuario del Sprint 1 (F4)

A continuación se presenta el detalle de las seis Historias de Usuario que conforman el Sprint 1 en el formato F4 adoptado por el equipo (Como/Quiero/Para + descripción + reglas de negocio + criterios de aceptación), expresadas como formularios tabulares para facilitar la lectura.

## 10.4.1 HU PB-13 — Gestionar Usuarios (panel web)

| Campo                 | Contenido                                                                                                                                                                                                                                                                                                                                                         |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Id**                | PB-13                                                                                                                                                                                                                                                                                                                                                             |
| **Nombre**            | Gestionar usuarios (admin web)                                                                                                                                                                                                                                                                                                                                    |
| **Prioridad**         | Alta                                                                                                                                                                                                                                                                                                                                                              |
| **PHU**               | 8                                                                                                                                                                                                                                                                                                                                                                 |
| **Como**              | Administrador de Bulldog Tech.                                                                                                                                                                                                                                                                                                                                    |
| **Quiero**            | Crear, activar y desactivar cuentas de técnicos desde el panel web.                                                                                                                                                                                                                                                                                               |
| **Para**              | Controlar el acceso al sistema sin intervenir el código de la app móvil.                                                                                                                                                                                                                                                                                          |
| **Descripción**       | El administrador accede al panel web mediante credenciales y, en la sección "Usuarios", puede crear nuevas cuentas de técnico (email, nombre completo, contraseña inicial), activarlas o desactivarlas, y reestablecer la contraseña. Las cuentas creadas pueden iniciar sesión inmediatamente desde la app móvil.                                                |
| **Reglas de negocio** | (a) Solo usuarios con rol ADMIN acceden a `/admin/usuarios`. (b) El email es único en la tabla `usuario`. (c) La contraseña inicial debe tener ≥ 8 caracteres y se almacena hasheada (bcrypt). (d) Desactivar un usuario invalida sus tokens activos en el siguiente request. (e) No se puede eliminar un usuario que tenga proyectos creados; sólo desactivarlo. |
| **CA1**               | Dado un admin autenticado, cuando completa el formulario de "Nuevo técnico" con datos válidos, entonces la cuenta aparece en la lista en estado ACTIVO en menos de 1 s.                                                                                                                                                                                           |
| **CA2**               | Dado un técnico inactivo, cuando intenta iniciar sesión, entonces el backend responde 403 con mensaje "Cuenta desactivada".                                                                                                                                                                                                                                       |
| **CA3**               | Email duplicado al crear devuelve 409 Conflict con mensaje claro.                                                                                                                                                                                                                                                                                                 |
| **CA4**               | Solo el rol ADMIN ve la sección `/admin/usuarios`; el TECNICO recibe 403.                                                                                                                                                                                                                                                                                         |
| **CA5**               | La contraseña nunca viaja en texto plano fuera del request HTTPS de creación; en GET no se devuelve `password_hash`.                                                                                                                                                                                                                                              |
| **Desarrollador**     | Borys (web) + Jhasmany (backend)                                                                                                                                                                                                                                                                                                                                  |

## 10.4.2 HU PB-19 — Gestionar Clientes (panel web)

| Campo                 | Contenido                                                                                                                                                                                                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Id**                | PB-19                                                                                                                                                                                                                                                                                                                                                |
| **Nombre**            | Gestionar clientes (admin web)                                                                                                                                                                                                                                                                                                                       |
| **Prioridad**         | Alta                                                                                                                                                                                                                                                                                                                                                 |
| **PHU**               | 3                                                                                                                                                                                                                                                                                                                                                    |
| **Como**              | Administrador de Bulldog Tech.                                                                                                                                                                                                                                                                                                                       |
| **Quiero**            | Crear y gestionar el catálogo de clientes desde el panel web.                                                                                                                                                                                                                                                                                        |
| **Para**              | Que los técnicos seleccionen el cliente correcto al crear proyectos, evitando ingresar nombres a mano con posibles inconsistencias.                                                                                                                                                                                                                  |
| **Descripción**       | El administrador accede a la sección "Clientes" del panel web y puede crear nuevos clientes (nombre), listar los existentes y desactivar los que ya no estén activos. Cuando un técnico crea un proyecto, el campo "Cliente" es un selector que consume `GET /api/clientes`.                                                                         |
| **Reglas de negocio** | (a) Solo usuarios con rol ADMIN pueden crear/desactivar clientes. (b) Todo usuario autenticado puede listar clientes activos. (c) El nombre del cliente es único (UNIQUE) y no puede estar vacío. (d) Un cliente desactivado no aparece en el selector de proyectos. (e) No se puede eliminar un cliente con proyectos asociados; solo desactivarlo. |
| **CA1**               | Admin crea un cliente con nombre válido y aparece en la lista en estado ACTIVO en menos de 1 s.                                                                                                                                                                                                                                                      |
| **CA2**               | Nombre duplicado devuelve 409 Conflict con mensaje claro.                                                                                                                                                                                                                                                                                            |
| **CA3**               | Técnico autenticado puede listar clientes activos (`GET /api/clientes`) pero recibe 403 al intentar crear (`POST /api/admin/clientes`).                                                                                                                                                                                                              |
| **CA4**               | Cliente desactivado no aparece en el selector de proyectos de la app.                                                                                                                                                                                                                                                                                |
| **CA5**               | Los proyectos existentes con ese cliente siguen mostrando el nombre aunque el cliente esté desactivado.                                                                                                                                                                                                                                              |
| **Desarrollador**     | Borys (web) + Jhasmany (backend)                                                                                                                                                                                                                                                                                                                     |

## 10.4.3 HU PB-09 — Autenticar Usuario (móvil contra backend)

| Campo                 | Contenido                                                                                                                                                                                                                                                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Id**                | PB-09                                                                                                                                                                                                                                                                                                                                                                                                |
| **Nombre**            | Autenticar usuario (móvil)                                                                                                                                                                                                                                                                                                                                                                           |
| **Prioridad**         | Alta                                                                                                                                                                                                                                                                                                                                                                                                 |
| **PHU**               | 5                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Como**              | Técnico de campo de Bulldog Tech.                                                                                                                                                                                                                                                                                                                                                                    |
| **Quiero**            | Iniciar sesión en la app móvil usando mi email y contraseña validados contra el backend en línea.                                                                                                                                                                                                                                                                                                    |
| **Para**              | Acceder solamente a mis proyectos y proteger los datos del cliente.                                                                                                                                                                                                                                                                                                                                  |
| **Descripción**       | La app móvil presenta una pantalla de Login al abrirse. Al ingresar credenciales válidas, la app llama a `POST /api/auth/login` y recibe un `access_token` + `refresh_token`. Los tokens se guardan en `flutter_secure_storage`. La app navega a la lista de proyectos. NO se almacena el `password_hash` ni ninguna entidad de dominio en el dispositivo.                                           |
| **Reglas de negocio** | (a) Toda llamada a `/api/*` requiere `Authorization: Bearer <access_token>`. (b) Cuando el access_token expira (401), el AuthInterceptor intenta refrescar automáticamente con el refresh_token. (c) Sin conexión con el backend, la pantalla de Login muestra banner "Sin conexión" y deshabilita el botón de inicio. (d) La sesión se considera "iniciada" únicamente si el backend respondió 200. |
| **CA1**               | Login con credenciales válidas navega a "Mis Proyectos" en p95 ≤ 2 s.                                                                                                                                                                                                                                                                                                                                |
| **CA2**               | Credenciales inválidas muestran mensaje "Credenciales inválidas" sin revelar cuál campo es incorrecto.                                                                                                                                                                                                                                                                                               |
| **CA3**               | Cuenta inactiva muestra mensaje "Cuenta desactivada. Contacte al administrador".                                                                                                                                                                                                                                                                                                                     |
| **CA4**               | Cierre de sesión llama `POST /api/auth/logout` (revoca refresh), borra tokens locales y vuelve al Login.                                                                                                                                                                                                                                                                                             |
| **CA5**               | Sin conexión, la app muestra "Sin conexión" y el botón queda deshabilitado; ningún intento de login local.                                                                                                                                                                                                                                                                                           |
| **CA6**               | El dispositivo no almacena `password_hash` ni email en texto plano fuera de SecureStorage.                                                                                                                                                                                                                                                                                                           |
| **Desarrollador**     | Jhasmany                                                                                                                                                                                                                                                                                                                                                                                             |

## 10.4.4 HU PB-18 — Ver Proyectos de la Organización (panel web)

| Campo                 | Contenido                                                                                                                                                                                                                                                |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Id**                | PB-18                                                                                                                                                                                                                                                    |
| **Nombre**            | Ver proyectos de la organización                                                                                                                                                                                                                         |
| **Prioridad**         | Baja                                                                                                                                                                                                                                                     |
| **PHU**               | 5                                                                                                                                                                                                                                                        |
| **Como**              | Administrador de Bulldog Tech.                                                                                                                                                                                                                           |
| **Quiero**            | Ver la lista de todos los proyectos de todos los técnicos de la organización con su estado y última actividad.                                                                                                                                           |
| **Para**              | Supervisar el trabajo de campo sin interrumpir a los técnicos.                                                                                                                                                                                           |
| **Descripción**       | En el dashboard del admin, una sección "Proyectos" lista todos los proyectos de la organización: nombre, técnico responsable, cliente, estado, fecha de última actividad y cantidad de mediciones. Soporta filtro por técnico, estado y rango de fechas. |
| **Reglas de negocio** | (a) Solo el rol ADMIN accede a esta vista. (b) Paginación: 20 ítems por página. (c) Orden por defecto: última actividad descendente.                                                                                                                     |
| **CA1**               | ADMIN ve todos los proyectos; TECNICO recibe 403.                                                                                                                                                                                                        |
| **CA2**               | La lista muestra: nombre, técnico, cliente, estado, fecha de última actividad, cantidad de puntos.                                                                                                                                                       |
| **CA3**               | Filtro por técnico funciona correctamente.                                                                                                                                                                                                               |
| **CA4**               | Si no hay proyectos, se muestra estado vacío "No hay proyectos registrados aún".                                                                                                                                                                         |
| **CA5**               | La carga inicial responde en p95 ≤ 1.5 s con 100 proyectos en BD.                                                                                                                                                                                        |
| **Desarrollador**     | Borys                                                                                                                                                                                                                                                    |

## 10.4.5 HU PB-01 — Gestionar Proyecto de Survey (móvil)

| Campo                 | Contenido                                                                                                                                                                                                                                                                                                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Id**                | PB-01                                                                                                                                                                                                                                                                                                                                                                         |
| **Nombre**            | Gestionar proyecto de survey                                                                                                                                                                                                                                                                                                                                                  |
| **Prioridad**         | Alta                                                                                                                                                                                                                                                                                                                                                                          |
| **PHU**               | 5                                                                                                                                                                                                                                                                                                                                                                             |
| **Como**              | Técnico de campo de Bulldog Tech.                                                                                                                                                                                                                                                                                                                                             |
| **Quiero**            | Crear, editar, archivar y eliminar proyectos en el backend desde la app móvil.                                                                                                                                                                                                                                                                                                |
| **Para**              | Organizar mis mediciones por edificio o cliente.                                                                                                                                                                                                                                                                                                                              |
| **Descripción**       | Desde la pantalla "Mis Proyectos" de la app móvil, el técnico autenticado puede crear un proyecto nuevo (nombre obligatorio, cliente del catálogo PB-19, descripción opcional), editarlo, archivarlo o eliminarlo (cascada sobre planos, puntos, mediciones cuando existan en sprints posteriores). Toda operación es un request al backend; no hay edición offline.          |
| **Reglas de negocio** | (a) El técnico autenticado solo ve y modifica proyectos donde `tecnico_id` coincide con su id (validación en backend). (b) Estados válidos: nuevo, en_progreso, completado, archivado. (c) El selector de cliente consume `GET /api/clientes` (solo activos). (d) Archivar = estado = archivado; no elimina datos. (e) Eliminar pide confirmación explícita en diálogo modal. |
| **CA1**               | Crear proyecto válido (`POST /api/proyectos`) responde 201 y aparece en la lista del técnico en p95 ≤ 1 s.                                                                                                                                                                                                                                                                    |
| **CA2**               | Editar nombre/descripción/cliente (`PUT /api/proyectos/{id}`) refleja cambios en el siguiente fetch.                                                                                                                                                                                                                                                                          |
| **CA3**               | Archivar (`PATCH /api/proyectos/{id}/archivar`) hace que el proyecto desaparezca del listado por defecto.                                                                                                                                                                                                                                                                     |
| **CA4**               | Eliminar con confirmación (`DELETE`) responde 204 y el proyecto desaparece de la lista.                                                                                                                                                                                                                                                                                       |
| **CA5**               | Intentar acceder a un proyecto de otro técnico responde 404 (no se revela existencia).                                                                                                                                                                                                                                                                                        |
| **Desarrollador**     | Jhasmany (móvil) + Borys (backend)                                                                                                                                                                                                                                                                                                                                            |

## 10.4.6 HU PB-10 — Ver Historial de Proyectos (móvil)

| Campo                 | Contenido                                                                                                                                                                                                                                                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Id**                | PB-10                                                                                                                                                                                                                                                                                                                                                               |
| **Nombre**            | Ver historial de proyectos                                                                                                                                                                                                                                                                                                                                          |
| **Prioridad**         | Media                                                                                                                                                                                                                                                                                                                                                               |
| **PHU**               | 3                                                                                                                                                                                                                                                                                                                                                                   |
| **Como**              | Técnico de campo.                                                                                                                                                                                                                                                                                                                                                   |
| **Quiero**            | Ver mis proyectos con estado, última actividad y conteo de puntos.                                                                                                                                                                                                                                                                                                  |
| **Para**              | Retomarlos rápidamente o consultarlos sin perder contexto.                                                                                                                                                                                                                                                                                                          |
| **Descripción**       | Desde la pantalla "Mis Proyectos" de la app móvil, el técnico autenticado accede a la lista de sus proyectos activos ordenada por última actividad. Puede buscar por nombre o cliente, navegar al detalle de un proyecto y activar un toggle para ver también los proyectos archivados. No hay carga de datos local; cada vista realiza un GET al backend en línea. |
| **Reglas de negocio** | (a) Endpoint `GET /api/proyectos` (sin filtro = activos del técnico). (b) `GET /api/proyectos?estado=archivado` para los archivados. (c) Orden por `fecha_ultima_actividad` DESC. (d) Búsqueda case-insensitive en nombre y cliente.                                                                                                                                |
| **CA1**               | Listado del técnico responde en p95 ≤ 1 s.                                                                                                                                                                                                                                                                                                                          |
| **CA2**               | Búsqueda en tiempo real (filtro local sobre el listado cargado).                                                                                                                                                                                                                                                                                                    |
| **CA3**               | Estado vacío con CTA "Crear primer proyecto" si no hay proyectos.                                                                                                                                                                                                                                                                                                   |
| **CA4**               | Toggle "Ver archivados" muestra los proyectos archivados.                                                                                                                                                                                                                                                                                                           |
| **CA5**               | Tap en un proyecto navega al detalle en p95 ≤ 500 ms.                                                                                                                                                                                                                                                                                                               |
| **Desarrollador**     | Jhasmany (móvil) + Borys (backend)                                                                                                                                                                                                                                                                                                                                  |


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


# 10.6 Patrón de desarrollo del Sprint 1

Esta sección documenta los modelos de diseño técnicos producidos durante la ejecución del Sprint 1 (R-3): la **arquitectura física** desplegada en contenedores, la **arquitectura lógica** organizada en cuatro capas y el **diseño de datos** en sus tres niveles (conceptual, lógico y físico).

## 10.6.1 Arquitectura Física — Diagrama de Despliegue


> _Figura 15: Arquitectura física — Diagrama de Despliegue de los contenedores Docker en producción._

## 10.6.2 Arquitectura Lógica — Diagrama de Paquetes


> _Figura 16: Arquitectura lógica — Diagrama de Paquetes en cuatro capas._

## 10.6.3 Diseño de Datos

### 10.6.3.1 Diagrama de Clases Conceptual (Sprint 1)


> _Figura 17: Diagrama de Clases Conceptual del Sprint 1._

### 10.6.3.2 Modelo Lógico (Esquema Relacional)


> _Figura 18: Modelo lógico (esquema relacional) del Sprint 1._

### 10.6.3.3 Diseño Físico (Tablas PostgreSQL)

**Tabla: `usuario`**

| Columna       | Tipo PostgreSQL | Restricciones              |
| ------------- | --------------- | -------------------------- |
| id            | SERIAL          | PRIMARY KEY                |
| nombre        | VARCHAR(120)    | NOT NULL                   |
| email         | VARCHAR(255)    | UNIQUE, NOT NULL           |
| password_hash | VARCHAR(255)    | NOT NULL                   |
| rol           | VARCHAR(30)     | NOT NULL DEFAULT 'tecnico' |
| activo        | BOOLEAN         | NOT NULL DEFAULT TRUE      |
| ultimo_acceso | TIMESTAMPTZ     | NULLABLE                   |
| created_at    | TIMESTAMPTZ     | NOT NULL DEFAULT now()     |

**Tabla: `refresh_token`**

| Columna    | Tipo PostgreSQL | Restricciones                                |
| ---------- | --------------- | -------------------------------------------- |
| id         | SERIAL          | PRIMARY KEY                                  |
| token      | VARCHAR(64)     | UNIQUE, NOT NULL                             |
| usuario_id | INTEGER         | NOT NULL, FK → usuario(id) ON DELETE CASCADE |
| expires_at | TIMESTAMPTZ     | NOT NULL                                     |
| created_at | TIMESTAMPTZ     | NOT NULL DEFAULT now()                       |

**Tabla: `cliente`**

| Columna    | Tipo PostgreSQL | Restricciones          |
| ---------- | --------------- | ---------------------- |
| id         | SERIAL          | PRIMARY KEY            |
| nombre     | VARCHAR(100)    | UNIQUE, NOT NULL       |
| activo     | BOOLEAN         | NOT NULL DEFAULT TRUE  |
| created_at | TIMESTAMPTZ     | NOT NULL DEFAULT now() |

**Tabla: `proyecto`**

| Columna          | Tipo PostgreSQL        | Restricciones                          |
| ---------------- | ---------------------- | -------------------------------------- |
| id               | SERIAL                 | PRIMARY KEY                            |
| nombre           | VARCHAR(200)           | NOT NULL                               |
| descripcion      | VARCHAR(500)           | NULLABLE                               |
| cliente_id       | INTEGER                | NULLABLE, FK → cliente(id)             |
| estado           | estado_proyecto (ENUM) | NOT NULL DEFAULT 'nuevo'               |
| tecnico_id       | INTEGER                | NOT NULL, FK → usuario(id)             |
| ultima_actividad | TIMESTAMPTZ            | NOT NULL DEFAULT now() ON UPDATE now() |
| cantidad_puntos  | INTEGER                | NOT NULL DEFAULT 0                     |
| created_at       | TIMESTAMPTZ            | NOT NULL DEFAULT now()                 |


# 10.7 Sprint 1 — Ejecución (R-3)

## 10.7.1 Diagrama de secuencia — Login extremo a extremo (PB-09)


> _Figura 19: Diagrama de secuencia — Login extremo a extremo (PB-09)._

## 10.7.2 Diagrama de secuencia — Crear Proyecto (PB-01)


> _Figura 20: Diagrama de secuencia — Crear proyecto de survey (PB-01)._

## 10.7.3 Diseño de interfaces de usuario

Siguiendo la actividad R-3 del marco Scrum adoptado por el equipo, para cada HU seleccionada se definió el diseño de la interfaz antes de implementarla. La app móvil sigue **Material 3** con paleta clara/oscura y tokens de diseño (`AppPalette`, `AppSpacing`, `AppRadius`); la plataforma web usa CSS Modules con variables de color, tipografía Poppins/Inter y un sistema consistente de badges, tablas y modales.

**Pantallas diseñadas e implementadas en Sprint 1:**

| Plataforma | Pantalla                  | Componentes de diseño clave                                             |
| ---------- | ------------------------- | ----------------------------------------------------------------------- |
| Móvil      | `LoginPage`               | Card centrada, campos email/contraseña, banner rojo "Sin conexión", CTA |
| Móvil      | `ProyectosPage`           | AppBar, SearchBar, ListView con tarjetas de proyecto, FAB "+ Nuevo"     |
| Móvil      | `ProyectoFormPage`        | Form scrollable, DropdownSearch clientes, TextFields, Guardar/Cancelar  |
| Web Admin  | `LoginAdmin.tsx`          | Layout centrado, card login, validación inline con react-hook-form      |
| Web Admin  | `GestionUsuarios.tsx`     | Sidebar + tabla paginada, modal "Nuevo técnico", toggle activo/inactivo |
| Web Admin  | `GestionClientes.tsx`     | Tabla, badge estado activo/inactivo, modal crear cliente                |
| Web Admin  | `ListadoProyectosOrg.tsx` | Tabla con filtros (técnico, estado), paginación, acciones contextuales  |

### 10.7.3.1 Flujo de navegación — App Móvil (Sprint 1)


> _Figura 21: Flujo de navegación de la app móvil en el Sprint 1._

## 10.7.4 Resultados de pruebas — backend (pytest)

| Suite de tests            | Tests  | Estado   | HU cubierta         |
| ------------------------- | ------ | -------- | ------------------- |
| `tests/test_auth.py`      | 12     | 12/12 | PB-09               |
| `tests/test_usuarios.py`  | OK     | Sí | PB-13               |
| `tests/test_clientes.py`  | 16     | 16/16 | PB-19               |
| `tests/test_proyectos.py` | OK     | Sí | PB-18, PB-01, PB-10 |
| `tests/test_health.py`    | OK     | Sí | Infraestructura     |
| **TOTAL**                 | **60** | 60/60 | Cobertura **87 %**  |

## 10.7.5 Daily Scrum (R-3.1)

El equipo realizó el **Daily Scrum de 15 minutos** cada día hábil durante el Sprint 1 (20–26 abr 2026), respondiendo las tres preguntas estándar:

| #   | Pregunta                                                             | Propósito                                                |
| --- | -------------------------------------------------------------------- | -------------------------------------------------------- |
| 1   | ¿Qué hice **ayer** para contribuir al Sprint?                        | Sincronizar avances y detectar solapamiento de trabajo   |
| 2   | ¿Qué voy a hacer **hoy** para contribuir al Sprint?                  | Planear el día y señalar dependencias entre miembros     |
| 3   | ¿Veo algún **impedimento** que impida lograr el objetivo del Sprint? | Identificar bloqueos para que el SM los elimine o escale |

**Impedimentos detectados y resoluciones durante el Sprint 1:**

| Fecha       | Impedimento detectado                                         | Resolución (SM)                                                  |
| ----------- | ------------------------------------------------------------- | ---------------------------------------------------------------- |
| 21 abr 2026 | Mock de `ConnectivityMonitor` en Flutter tests falla          | Registrado como deuda técnica; postergado al inicio del Sprint 2 |
| 22 abr 2026 | 99 hrs estimadas superan capacidad real (~80 hrs disponibles) | PO re-priorizó; se mantienen las 6 HU sin agregar tareas nuevas  |
| 23 abr 2026 | CI/CD no genera APK Android automáticamente                   | Construcción manual para Sprint 1; tarea nueva para Sprint 2     |
| 24 abr 2026 | Framework de pruebas web (Vitest) no configurado              | PO decidió posponer configuración al inicio del Sprint 2         |

## 10.7.6 Definition of Done — Sprint 1

| Criterio DoD                                                                                  | Estado  |
| --------------------------------------------------------------------------------------------- | ------- |
| Migración `0001` aplicada y reversible                                                        | Sí |
| Migración `0002_cliente_y_proyecto` aplicada y reversible                                     | Sí |
| Coverage backend ≥ 80 % en módulos auth, usuarios, clientes, proyectos                        | 87 % |
| OpenAPI publicado con tags `auth`, `admin/usuarios`, `clientes`, `proyectos`                  | Sí |
| Bundle web sirviendo `/admin/login`, `/admin/usuarios`, `/admin/clientes`, `/admin/proyectos` | Sí |
| APK de la app móvil con login funcional + CRUD proyectos                                      | Sí |
| Widget tests de `ProyectosPage` y `ProyectoFormPage` pasando                                  | Parcial 5/8  |
| Demo grabada del flujo completo                                                               | ⏳      |


# 10.8 Sprint 1 — Sprint Review (R-4)

**Formato:** F1 — Revisión de Sprint
**Evento:** R-4 Sprint Review (presentación conjunta S0+S1)
**Proyecto:** Wireless HeatMapper — Sprint 0 + Sprint 1
**Número de revisión:** 1
**Objetivo de la revisión:** Validar el incremento del Sprint 1 ante el Product Owner y los interesados
**Lugar, fecha, hora:** 27 de abril de 2026, 08:00 hrs

## 10.8.1 Participantes

| Nombre                             | Rol               |
| ---------------------------------- | ----------------- |
| Jhasmany Jhunnior Fernandez Ortega | Scrum Master/Dev  |
| Herland Borys Quiroga Flores       | Product Owner/Dev |

## 10.8.2 Presentación del incremento

| Función presentada                                              | HU           |
| --------------------------------------------------------------- | ------------ |
| Docker Compose: 4 contenedores corriendo + `/api/health` 200 OK | Sprint 0     |
| Admin crea técnico y cliente en el panel web                    | PB-13, PB-19 |
| Técnico inicia sesión en la app móvil con JWT                   | PB-09        |
| Técnico crea, edita, archiva y elimina proyectos en la app      | PB-01        |
| Admin ve todos los proyectos de la organización con filtros     | PB-18        |
| Técnico busca y navega su historial de proyectos                | PB-10        |

## 10.8.3 Flujo de demo (extremo a extremo)

| Paso | Actor               | Acción demostrada                                                         | Resultado verificable                              |
| ---: | ------------------- | ------------------------------------------------------------------------- | -------------------------------------------------- |
|    1 | Administrador (web) | Crea el cliente "Bulldog Tech." y el técnico "Jhasmany"                   | Ambos registros aparecen ACTIVOS en el panel admin |
|    2 | Técnico (app móvil) | Inicia sesión con las credenciales recién creadas                         | Navega a la pantalla "Mis Proyectos" (lista vacía) |
|    3 | Técnico (app móvil) | Crea el proyecto "Edificio Central" seleccionando el cliente del catálogo | El proyecto aparece en la lista del técnico        |
|    4 | Técnico (app móvil) | Edita la descripción del proyecto y luego lo archiva                      | El proyecto pasa a la pestaña "Archivados"         |
|    5 | Administrador (web) | Accede a `/admin/proyectos` y filtra por técnico "Jhasmany"               | Visualiza el proyecto creado en el paso 3          |

## 10.8.4 Retroalimentación

| Pregunta / Comentario                                                                           | Respuesta del equipo                                                                              |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| ¿Los 29 PHU son una velocidad sostenible para un equipo de 2 personas en el primer Sprint real? | SM: sí, es conservadora; se considera 25–30 PHU como rango cómodo para Sprints futuros.           |
| ¿El modelo JWT con refresh de 7 días es adecuado para un sistema de campo en línea?             | PO: es suficiente para el alcance del producto y cubre el requisito RP8 del Plan del Proyecto.    |
| ¿El administrador podría ver el detalle de cada proyecto además del listado general?            | PO: se registra como ítem de mejora para Sprint 2 (extensión de PB-18).                           |
| Los 3 widget tests fallidos en Flutter, ¿representan riesgo para la entrega del Sprint 2?       | SM: riesgo bajo; el código funciona en dispositivo; el fix de mocks está planificado en Sprint 2. |

## 10.8.5 Tareas completadas

| HU        | Estado | PHU        |
| --------- | ------ | ---------- |
| PB-13     | Done   | 8          |
| PB-19     | Done   | 3          |
| PB-09     | Done   | 5          |
| PB-18     | Done   | 5          |
| PB-01     | Done   | 5          |
| PB-10     | Done   | 3          |
| **Total** |        | **29 PHU** |

## 10.8.6 Para lo que viene — Sprint 2

- **PB-02:** Importar plano (PNG/JPG/PDF) al backend asociado a un proyecto.
- **PB-11:** Calibrar escala del plano dibujando línea de referencia.


# 10.9 Sprint 1 — Sprint Retrospective (R-5)

**Formato:** F2 — Retrospectiva de Sprint
**Evento:** R-5 Sprint Retrospective
**Proyecto:** Wireless HeatMapper — Sprint 1
**Objetivo de la retrospectiva:** Identificar lo que funcionó bien, lo que no funcionó y las mejoras para el Sprint 2
**Lugar, fecha, hora:** 27 de abril de 2026, 10:00 hrs
**Participantes:** Jhasmany Fernandez (SM) · Herland Borys Quiroga (PO)

| ¿Qué salió bien?                                                 | ¿Qué no salió bien?                                       | ¿Problemas encontrados y cómo se resolvieron?                         | ¿Qué debemos cambiar para mejorar?                              |
| ---------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------- |
| 60/60 tests pytest en verde con 87 % de cobertura                | Widget tests Flutter: 3 con error (5/8 pasan)             | Tests Flutter fallaron por mock de ConnectivityMonitor; pendiente fix | Agregar mocks correctos para ConnectivityMonitor en el Sprint 2 |
| Docker Compose funcional con 4 contenedores desde el día 1       | No se configuró framework de tests web (Vitest)           | Sp1-11 incompleto; se decidió posponer al Sprint 2                    | Configurar Vitest para web al inicio del Sprint 2               |
| Backend con arquitectura limpia en 4 capas (api→svc→repo→models) | Capacidad excedida: 99 hrs estimadas vs 80 disponibles    | Se priorizó funcionalidad core; código ya estaba implementado         | Ser más conservadores en comprometer PHU en Planning Poker      |
| Migraciones Alembic versionadas y reversibles                    | Pruebas de aceptación con PO (6 tareas Sp1-xx) pendientes | Se realizarán en la presentación R-4 del 27 abr                       | Hacer mini-reviews al cierre de cada HU dentro del Sprint       |
| Funcionalidad completa: admin web + auth móvil + CRUD proyectos  | APK no generado por CI/CD                                 | Se construye manualmente; CI build imagen Docker sí funciona          | Configurar step de build APK en GitHub Actions para el Sprint 2 |


# 11. Bibliografía

## Libros y normas

- Pressman, R. S. (2010). _Software Engineering: A Practitioner's Approach_ (7.ª ed.). McGraw-Hill.
- Coleman, D. D. & Westcott, D. A. (2018). _CWNA Certified Wireless Network Administrator Study Guide — Exam CWNA-107_ (5.ª ed.). Sybex / Wiley.
- Schwaber, K. & Sutherland, J. (2020). _The Scrum Guide — The Definitive Guide to Scrum: The Rules of the Game_. ScrumGuides.org.
- Object Management Group (2017). _OMG Unified Modeling Language (OMG UML), Version 2.5.1_. OMG Document formal/2017-12-05.
- Boehm, B. W. (1981). _Software Engineering Economics_. Prentice Hall (referencia base del modelo COCOMO empleado para estimación inicial del proyecto).

## Documentos internos del proyecto

- Quiroga Flores, H. B. & Fernandez Ortega, J. J. (2026). _Wireless HeatMapper — Plan del Proyecto (Modalidad Online)_. Equipo de desarrollo Wireless HeatMapper.

## Documentación técnica oficial (frameworks y herramientas)

- FastAPI — Documentación oficial: <https://fastapi.tiangolo.com/>
- Flutter — Documentación oficial: <https://docs.flutter.dev/>
- React — Documentación oficial: <https://react.dev/>
- TypeScript — Documentación oficial: <https://www.typescriptlang.org/docs/>
- PostgreSQL 15 — Documentación oficial: <https://www.postgresql.org/docs/15/>
- SQLAlchemy 2.x — Documentación oficial: <https://docs.sqlalchemy.org/>
- Alembic — Documentación oficial: <https://alembic.sqlalchemy.org/>
- Pydantic v2 — Documentación oficial: <https://docs.pydantic.dev/>
- Docker Compose — Documentación oficial: <https://docs.docker.com/compose/>
- Nginx — Documentación oficial: <https://nginx.org/en/docs/>
- TanStack Query — Documentación oficial: <https://tanstack.com/query>
- Vite — Documentación oficial: <https://vitejs.dev/>
- StarUML 5.x — Documentación oficial: <https://docs.staruml.io/>
- PlantUML — Documentación oficial: <https://plantuml.com/>

## Aplicaciones de referencia analizadas (estado del arte)

- VREM Software Development. _WiFiAnalyzer (Open Source)_. Repositorio GitHub: <https://github.com/VREMSoftwareDevelopment/WifiAnalyzer> (última consulta: abril 2026).
- Kismet Wireless. _Kismet — Wireless network and device detector_. <https://www.kismetwireless.net/>
- _python-wifi-survey-heatmap_ — herramienta de site survey y generación de heatmaps en Python. Repositorio GitHub público (última consulta: abril 2026).
- Inocybe Technologies / Tamosoft. _TamoGraph Site Survey_ (referencia comercial de comparación). <https://www.tamos.com/products/wifi-site-survey/>

## Estándares aplicables

- IEEE 802.11 Working Group. _IEEE Standard for Information Technology — Telecommunications and Information Exchange Between Systems — Local and Metropolitan Area Networks — Specific Requirements — Part 11: Wireless LAN MAC and PHY Specifications_. IEEE.
- RFC 7519 (Jones, M., Bradley, J. & Sakimura, N., 2015). _JSON Web Token (JWT)_. Internet Engineering Task Force.
- OWASP Foundation (2021). _OWASP Top 10 — The Ten Most Critical Web Application Security Risks_. <https://owasp.org/Top10/>


# 12. Anexos

## Anexo A — Gráficos comparativos: situación actual vs. situación deseada

| Dimensión                            | Situación actual (sin Wireless HeatMapper)                                | Situación deseada (con Wireless HeatMapper)                                                 |
| ------------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Captura de mediciones                | Apps WiFi analyzer + planilla Excel + transcripción manual                | App móvil delgada con envío en línea por punto al backend                                   |
| Georreferenciación sobre plano       | Marcas a mano sobre plano impreso                                         | Marcado interactivo sobre plano digital calibrado, persistido en backend                    |
| Generación del mapa de calor         | Edición manual posterior en software de imagen                            | Interpolación espacial automática (IDW/Kriging) ejecutada en el backend                     |
| Análisis de cobertura                | Criterio subjetivo del técnico                                            | Detección automática de zonas muertas (< −90 dBm) y CCI/ACI                                 |
| Recomendación de posicionamiento APs | Experiencia individual del técnico, sin justificación cuantitativa        | Recomendaciones generadas por módulo de IA con objetivo ≥ −70 dBm                           |
| Centralización organizacional        | Cada técnico mantiene sus propios archivos locales                        | Backend único (PostgreSQL) — el admin ve todos los proyectos de la organización             |
| Entrega al cliente                   | PDF estático armado a mano, enviado por correo                            | Portal web con enlace único + token + expiración configurable                               |
| Trazabilidad                         | Inexistente — no se puede reconstruir cuándo ni cómo se tomó una medición | End-to-end: cada medición tiene timestamp, técnico, plano, escala y coordenadas almacenadas |

## Anexo B — Carta de aceptación del cliente (Bulldog Tech.)

Documento institucional de Bulldog Tech. en el que la empresa acepta participar como cliente real del proyecto Wireless HeatMapper, recibir presentaciones de los incrementos al cierre de cada Sprint y validar funcionalmente los entregables. La carta original firmada se incluye como adjunto en la entrega física del Plan del Proyecto.

## Anexo C — Diapositivas de la presentación

Material de soporte usado durante la presentación oral de la revisión conjunta del Sprint 0 + Sprint 1. Contiene la línea narrativa del proyecto: introducción al problema, situación actual y deseada, alcance, marco Scrum, resumen del Sprint 0 y demo del Sprint 1. Las diapositivas se entregan en formato PDF como adjunto al Plan del Proyecto.

---

# 13. Apéndices

## Apéndice A — Stack tecnológico implementado

| Componente       | Tecnología                                          | Estado Sprint 1 |
| ---------------- | --------------------------------------------------- | --------------- |
| App móvil        | Flutter / Dart · BLoC/Cubit · Dio · go_router       | Operativo       |
| Backend REST     | Python 3.12 / FastAPI · SQLAlchemy · Alembic · JWT  | Operativo       |
| Base de datos    | PostgreSQL 15 (Docker)                              | Operativo       |
| Web (admin)      | React + TypeScript + Vite + TanStack Query          | Operativo       |
| Infraestructura  | Docker Compose + Nginx (reverse proxy)              | Operativo       |
| CI/CD            | GitHub Actions (lint + tests + build imagen Docker) | Operativo       |
| Pre-commit hooks | ruff · ruff-format · prettier · eslint              | Operativo       |

## Apéndice B — Definition of Done (acordada en Sprint 0)

| Criterio                               | Verificación                                                     |
| -------------------------------------- | ---------------------------------------------------------------- |
| Sí Código implementado en backend      | Endpoints REST documentados con OpenAPI/Swagger                  |
| Sí Código implementado en cliente      | Móvil (Flutter) y/o web (React) consumiendo los endpoints        |
| Sí Migraciones Alembic aplicadas       | Esquema PostgreSQL versionado y reversible                       |
| Sí Pruebas unitarias                   | Cobertura ≥ 70 % en módulos nuevos del backend                   |
| Sí Pruebas de integración              | Tests de endpoints contra BD efímera (pytest + httpx)            |
| Sí Criterios de aceptación validados   | El PO ejecuta cada CA contra el incremento desplegado            |
| Sí Code review aprobado                | Pull Request revisado por el otro miembro del equipo             |
| Sí Mergeado a `main`                   | Squash-merge desde rama `feature/PB-XX-slug`                     |
| Sí Despliegue automático               | Pipeline GitHub Actions construye imagen Docker                  |
| Sí Sin almacenamiento local de dominio | El cliente móvil no persiste entidades de dominio entre sesiones |

## Apéndice C — Trazabilidad HU ↔ RP (Sprint 1)

| HU    | Nombre                               | RP  | UC   |
| ----- | ------------------------------------ | --- | ---- |
| PB-13 | Gestionar usuarios (admin web)       | RP7 | UC13 |
| PB-19 | Gestionar clientes (admin web)       | RP7 | UC19 |
| PB-09 | Autenticar usuario (móvil)           | RP8 | UC11 |
| PB-18 | Ver proyectos de la organización     | RP7 | UC18 |
| PB-01 | Gestionar proyecto de survey (móvil) | RP8 | UC01 |
| PB-10 | Ver historial de proyectos           | RP8 | UC12 |

**RP7:** Gestión de acceso y pre-aprovisionamiento de técnicos por el administrador.
**RP8:** Operaciones CRUD del técnico autenticado contra el backend (sin persistencia local).

---

_Documento generado conforme al marco de trabajo Scrum adoptado por el equipo del proyecto._
_Última actualización: 27 de abril de 2026._


