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
