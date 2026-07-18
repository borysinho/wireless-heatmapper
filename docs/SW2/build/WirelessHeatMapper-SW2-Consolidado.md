---
title: "Documentación formal del proyecto y empresa"
subtitle: "Team 24 Software - Wireless HeatMapper"
author:
  - "Grupo 24 - Team 24 Software"
date: "Gestión 2026"
lang: es-BO
---

| Campo | Detalle |
| ----- | ------- |
| Universidad | Universidad Autonoma Gabriel Rene Moreno |
| Facultad | Facultad de Ingenieria en Ciencias de la Computacion y Telecomunicaciones |
| Materia | Ingenieria de Software II |
| Empresa de software | Team 24 Software |
| Proyecto | Sistema Inteligente de Analisis y Optimizacion de Cobertura WiFi mediante Mapas de Calor |
| Producto | Wireless HeatMapper |
| Cliente del caso | Bulldog Tech. |
| Grupo | 24 |
| Integrantes | Jhasmany Jhunnior Fernandez Ortega; Herland Borys Quiroga Flores |
| Ciudad | Santa Cruz de la Sierra, Bolivia |
| Gestion | 2026 |
| Modalidad del producto | 100 % en linea |

El presente documento es una presentacion formal, de investigacion y de desarrollo elaborada por Team 24 Software como startup academica de desarrollo de software. La documentacion no se limita al desarrollo puntual de Wireless HeatMapper: presenta a la empresa, su sistema de calidad, su presencia web, sus politicas, su infraestructura, su estrategia de mercado, sus mecanismos de puesta en marcha y la entrega del software como producto real.

La estructura principal sigue exactamente los doce puntos solicitados en la clase del 21/04/2026:

| # | Punto |
| - | ----- |
| 1 | PAPS |
| 2 | Modelos de Desarrollo |
| 3 | Manual de Garantia de Calidad del Software SQAP |
| 4 | Herramientas CASE |
| 5 | Aspectos Legales para Apertura de Empresa de Software |
| 6 | Infraestructura para la Produccion de Software |
| 7 | Sitio Web de la Empresa |
| 8 | Estudio de Mercado |
| 9 | Pruebas del Software |
| 10 | Marketing |
| 11 | Aspectos para la Puesta en Marcha |
| 12 | Software como Producto |


# 1. PAPS


### Introducción

En la actualidad, la conectividad inalámbrica mediante redes WiFi se ha
convertido en un componente esencial dentro de entornos empresariales,
educativos y domésticos, permitiendo el acceso continuo a servicios
digitales y sistemas de información. Sin embargo, la correcta
planificación y el despliegue de estas redes en espacios interiores
representan un desafío técnico significativo debido a factores como la
atenuación de la señal, las interferencias electromagnéticas, los
obstáculos físicos y la distribución irregular de los puntos de acceso.

En muchos casos, el diseño de redes WiFi se basa en estimaciones
teóricas proporcionadas por los fabricantes y en la experiencia empírica
de los técnicos, lo cual no garantiza una cobertura óptima en
condiciones reales. Esta situación puede derivar en zonas de baja señal,
interferencias entre canales, solapamientos innecesarios y deficiencias
en la calidad del servicio, problemas que únicamente se detectan después
de la implementación de la red, generando costos adicionales y
retrabajo.

Ante esta problemática, el presente proyecto propone el desarrollo de
un sistema **estrictamente en línea** compuesto por dos componentes
integrados: una **aplicación móvil Android** que opera como cliente
delgado, encargada del relevamiento en campo y de transmitir en
tiempo real cada medición al backend, sin almacenar datos de dominio
de forma persistente en el dispositivo; y una **plataforma web
complementaria** que cumple tres funciones esenciales: (i) panel de
administración para la gestión de cuentas de técnicos, (ii) portal de
cliente que permite visualizar de forma interactiva los resultados de
un proyecto mediante un enlace único, y (iii) backend REST que aloja
el módulo de inteligencia artificial responsable de sugerir
ubicaciones óptimas para los puntos de acceso y que actúa como única
fuente de verdad de todo el dominio (proyectos, planos, mediciones,
heatmaps y análisis). De esta manera, el proyecto busca transformar
el proceso tradicional de diseño de redes, pasando de un enfoque
basado en estimaciones a uno fundamentado en evidencia técnica
medible y compartible en línea entre técnicos, administradores y
clientes.

## Métricas

### Software de referencia

Con el propósito de establecer una base comparativa que permita estimar
el tamaño, esfuerzo y complejidad del sistema propuesto, se analizaron
tres proyectos de software de código abierto con funciones similares a
las del Wireless HeatMapper. Los proyectos seleccionados poseen
repositorios públicos en GitHub, lo que facilita la extracción de
métricas objetivas de tamaño, productividad y calidad. A continuación se
describe cada uno de estos sistemas.

#### WiFiAnalyzer

WiFiAnalyzer es una aplicación móvil nativa para la plataforma Android,
desarrollada en Kotlin, orientada al análisis de redes inalámbricas en
tiempo real. Permite visualizar la intensidad de señal (RSSI),
identificar puntos de acceso (SSID, BSSID), detectar canales ocupados en
las bandas de 2.4 GHz, 5 GHz y 6 GHz, estimar la distancia a cada AP y
consultar la base de datos de fabricantes a partir de la dirección MAC.
La aplicación se distribuye a través de Google Play y F-Droid bajo la
licencia GPL-3.0.

Su relevancia como proyecto de referencia radica en que comparte con el
Wireless HeatMapper la plataforma de destino (Android), el tipo de datos
capturados (RSSI, SSID, BSSID, canal, frecuencia) y la naturaleza de la
interfaz de usuario orientada a la gestión de redes inalámbricas. Es el
proyecto de mayor madurez de los tres analizados, con 4 700 estrellas y
728 bifurcaciones en GitHub.

---

             **Atributo**                                 **Valor**

---

              Repositorio              github.com/VREMSoftwareDevelopment/WiFiAnalyzer

              Plataforma                       Android (Google Play / F-Droid)

          Lenguaje principal                      Kotlin 97.4 %, Java 2.6 %

               Licencia                                    GPL-3.0

           Estrellas GitHub                                 4 700

             Bifurcaciones                                   728

       Confirmaciones (commits)                             2 013

     Incidencias abiertas (issues)                            6

             KLDC estimado                                  25.0

           Esfuerzo estimado                           71 personas-mes

---

#### WiFiSurveyor

WiFiSurveyor es una aplicación web de escritorio multiplataforma
(Windows, macOS y Linux) que combina la recopilación de datos de señal
WiFi con la visualización de mapas de calor sobre planos de edificios.
Desarrollada en TypeScript (frontend con Vue.js) y C# (backend
multiplataforma), su arquitectura se organiza en cuatro módulos: Core
(lógica compartida), implementaciones específicas por sistema operativo
(Windows, macOS, Linux) y la aplicación frontend. Los proyectos se
almacenan en formato JSON y pueden recargarse en sesiones posteriores.

De los tres proyectos analizados, WiFiSurveyor es el que mayor similitud
funcional presenta con el Wireless HeatMapper: permite importar un plano
como imagen de fondo, registrar puntos de medición sobre él con sus
coordenadas y valores de señal, y generar un mapa de calor de cobertura.
Su integración con SonarCloud para análisis de calidad de código también
lo convierte en una referencia metodológica relevante.

---

             **Atributo**                          **Valor**

---

              Repositorio               github.com/ecoAPM/WiFiSurveyor

              Plataforma              Windows / macOS / Linux (web local)

          Lenguaje principal             TypeScript 51.7 %, C# 30.9 %,
                                                 Vue.js 15.5 %

               Licencia                             GPL-3.0

           Estrellas GitHub                           68

             Bifurcaciones                            10

       Confirmaciones (commits)                       273

     Incidencias abiertas (issues)                     8

             KLDC estimado                            8.0

           Esfuerzo estimado                    23 personas-mes

---

#### python-wifi-survey-heatmap

python-wifi-survey-heatmap es una herramienta de escritorio para Linux
que permite al usuario registrar mediciones de señal WiFi en puntos
predefinidos sobre un plano importado como imagen, y posteriormente
generar mapas de calor mediante interpolación espacial. Además,
incorpora pruebas de ancho de banda activas mediante la herramienta
iperf3 y análisis de utilización de canales. Su implementación es
completamente en Python, apoyándose en las bibliotecas scipy y
matplotlib para el procesamiento y la visualización, y en wxPython
Phoenix para la interfaz gráfica.

Aunque está orientada a Linux y carece de módulo de inteligencia
artificial, su relevancia como referencia radica en que implementa el
flujo central del Wireless HeatMapper: captura de datos por punto de
medición, almacenamiento en JSON y generación de mapa de calor continuo
sobre el plano del edificio.

---

             **Atributo**                                **Valor**

---

              Repositorio              github.com/jantman/python-wifi-survey-heatmap

              Plataforma                            Linux (escritorio)

          Lenguaje principal                           Python 98.3 %

               Licencia                      No especificada (código abierto)

           Estrellas GitHub                                 467

             Bifurcaciones                                  92

       Confirmaciones (commits)                             141

     Incidencias abiertas (issues)                           9

             KLDC estimado                                  2.5

           Esfuerzo estimado                          7 personas-mes

---

### Métricas Orientadas al Tamaño (MoT)

Las métricas orientadas al tamaño establecen medidas directas del
software producido, normalizadas por el volumen de código fuente.
Siguiendo el marco propuesto por Pressman (2010), las medidas directas
empleadas son: líneas de código en miles (KLDC), esfuerzo expresado en
personas-mes (PM), cantidad de desarrolladores, y número de errores y
defectos reportados. A partir de estas medidas se derivan las métricas
de calidad y productividad.

#### Líneas de código (KLDC)

El recuento de líneas de código se expresó en miles (KLDC). Para los
proyectos de referencia, el valor fue estimado a partir del tamaño del
repositorio, el número de confirmaciones y la madurez funcional
observada, dado que no existe una medición publicada por los autores.

#### Tiempo de desarrollo

Se tomó como referencia el período de actividad del repositorio (desde
la primera confirmación hasta la versión estable más reciente),
ponderado por el número de contribuidores para obtener una estimación
del esfuerzo acumulado en personas-mes.

#### Cantidad de desarrolladores

Se consideró la cantidad de contribuidores activos registrados en el
repositorio. WiFiAnalyzer cuenta con una comunidad de más de 15
contribuidores; WiFiSurveyor fue desarrollado por un equipo de
aproximadamente 3 personas; python-wifi-survey-heatmap tiene un único
desarrollador principal.

#### Errores y defectos

Como indicador de defectos conocidos se utilizó el número de incidencias
abiertas (issues) en GitHub al momento del análisis, que refleja los
problemas reportados por los usuarios y pendientes de resolución.

#### Esfuerzo

El esfuerzo total se estimó dividiendo el KLDC estimado entre la
productividad promedio de la industria para proyectos de código abierto
(350 LOC/PM), valor coherente con los rangos documentados por Pressman
para sistemas de mediana complejidad.

La siguiente tabla consolida las métricas orientadas al tamaño de los
tres proyectos de referencia:

---

     **Métrica**     **WiFiAnalyzer**   **WiFiSurveyor**   **python-wifi-survey-heatmap**

---

    KLDC estimado          25.0               8.0                       2.5

Esfuerzo estimado 71 23 7
(PM)

Desarrolladores 15+ 3 1

Errores / issues 6 8 9
abiertos

       Commits            2 013               273                       141

---

### Cálculo de métricas

A partir de los datos de la tabla anterior se calculan las métricas de
calidad y productividad definidas por Pressman (2010) para cada proyecto
de referencia.

#### Calidad = (Errores + Defectos) / KLDC

La métrica de calidad expresa la densidad de defectos por cada mil
líneas de código. Un valor menor indica mayor madurez y limpieza del
código fuente.

---

          **Proyecto**            **Errores**        **KLDC**          **Calidad
                                                                    (errores/KLDC)**

---

          WiFiAnalyzer                 6               25.0               0.24

          WiFiSurveyor                 8                8.0               1.00

python-wifi-survey-heatmap 9 2.5 3.60

---

WiFiAnalyzer presenta la menor densidad de defectos (0.24 errores/KLDC),
lo que refleja su mayor madurez. python-wifi-survey-heatmap registra el
valor más alto (3.60 errores/KLDC), consistente con su estado declarado
de proyecto estable pero de mantenimiento reducido.

#### Productividad = (KLDC / Esfuerzo) × 1 000

La productividad mide la cantidad de líneas de código producidas por
persona-mes. Los tres proyectos convergen en torno a 350 LOC/PM, valor
representativo de proyectos de código abierto de complejidad media.

---

          **Proyecto**             **KLDC**      **Esfuerzo (PM)**  **Productividad
                                                                      (LOC/PM)**

---

          WiFiAnalyzer               25.0               71                352

          WiFiSurveyor                8.0               23                348

python-wifi-survey-heatmap 2.5 7 357

---

## Métricas Orientadas a la Función (MoF)

Las métricas orientadas a la función miden el software en términos de la
funcionalidad que entrega al usuario, con independencia del lenguaje de
programación utilizado. El método de Puntos de Función (PF), propuesto
por Albrecht y formalizado por Pressman (2010), cuantifica las
características del dominio de información del sistema mediante cinco
parámetros de medición, a los que se aplican factores de peso según su
complejidad.

### Parámetros de medición

Los parámetros utilizados para calcular los puntos de función sin
ajustar son los siguientes:

#### Número de entradas (datos WiFi)

Representa el número de tipos de entrada distintos que el usuario o un
sistema externo proporciona a la aplicación. En el contexto de los
proyectos analizados, incluye formularios de configuración, parámetros
de escaneo, archivos de plano y datos de señal capturados
automáticamente y enviados en línea al backend.

#### Número de salidas (mapas, reportes)

Corresponde a los tipos de salida que el sistema genera hacia el
usuario, incluyendo pantallas de visualización, mapas de calor, gráficas
de señal y documentos de reporte exportables.

#### Número de consultas

Son las transacciones interactivas en las que el usuario solicita
información al sistema, como la consulta de historial de mediciones, el
filtrado de redes por SSID o frecuencia, y la búsqueda en la base de
datos de fabricantes.

#### Archivos internos (datos de medición)

Corresponde a los grupos lógicos de datos mantenidos internamente por la
aplicación. En la modalidad 100 % en línea estos grupos residen
exclusivamente en la base de datos central PostgreSQL del backend
(proyectos, planos, mediciones, modelos de IA y configuraciones de
usuario); el cliente móvil no mantiene grupos lógicos persistentes
de dominio.

#### Interfaces externas (APIs, sensores WiFi)

Son los archivos o servicios de datos que la aplicación comparte con
sistemas externos, como las APIs del sistema operativo para el acceso al
hardware WiFi, servicios en la nube y herramientas de terceros.

### Cálculo de puntos de función

Para cada parámetro se asigna una complejidad (simple, medio o complejo)
y un factor de peso según la tabla establecida por Pressman (2010):

---

    **Parámetro**      **Simple**         **Medio**       **Complejo**

---

     Entradas de            3                 4                 6
       usuario

     Salidas de             4                 5                 7
       usuario

      Consultas             3                 4                 6

Archivos internos 7 10 15
lógicos

     Interfaces             5                 7                10
      externas

---

La fórmula de cálculo es:

**PF = Conteo total × \[0.65 + 0.01 × ΣFi\]**

Donde ΣFi es la suma de los 14 factores de ajuste de complejidad, cuyo
rango individual es de 0 a 5. El factor resultante oscila entre 0.65 y
1.35.

#### Conteo total --- WiFiAnalyzer

---

**Parámetro** **Cantidad** **Complejidad** **Peso** **Subtotal**

---

    Entradas de         3        Medio / Complejo       4-6             14
      usuario

    Salidas de          4        Medio / Complejo       5-7             26
      usuario

     Consultas          3         Simple / Medio        3-4             11

     Archivos           3         Simple / Medio        7-10            27
     internos
      lógicos

    Interfaces          2        Medio / Complejo       7-10            17
     externas

     Total sin                                                          95
      ajustar

---

ΣFi = 42 (complejidad media-alta, app Android con hardware WiFi,
persistencia de datos y visualizaciones complejas)

**PF = 95 × \[0.65 + 0.01 × 42\] = 95 × 1.07 ≈ 102 puntos de función**

#### Conteo total --- WiFiSurveyor

---

**Parámetro** **Cantidad** **Complejidad** **Peso** **Subtotal**

---

    Entradas de         3         Simple / Medio        3-4             11
      usuario

    Salidas de          3        Simple / Complejo      4-7             16
      usuario

     Consultas          2         Simple / Medio        3-4             7

     Archivos           2         Simple / Medio        7-10            17
     internos
      lógicos

    Interfaces          3              Medio             7              21
     externas

     Total sin                                                          72
      ajustar

---

ΣFi = 38 (complejidad moderada, aplicación multiplataforma con APIs WiFi
por cada sistema operativo)

**PF = 72 × \[0.65 + 0.01 × 38\] = 72 × 1.03 ≈ 74 puntos de función**

#### Conteo total --- python-wifi-survey-heatmap

---

**Parámetro** **Cantidad** **Complejidad** **Peso** **Subtotal**

---

    Entradas de         3         Simple / Medio        3-4             10
      usuario

    Salidas de          3        Medio / Complejo       5-7             19
      usuario

     Consultas          1             Simple             3              3

     Archivos           2             Simple             7              14
     internos
      lógicos

    Interfaces          2        Medio / Complejo       7-10            17
     externas

     Total sin                                                          63
      ajustar

---

ΣFi = 30 (complejidad baja-media, herramienta especializada de un único
desarrollador sin módulos avanzados)

**PF = 63 × \[0.65 + 0.01 × 30\] = 63 × 0.95 ≈ 60 puntos de función**

#### Factores de peso

La siguiente tabla resume los puntos de función calculados para cada
sistema de referencia y para el Wireless HeatMapper en su modalidad
100 % en línea:

---

          **Sistema**             **PF sin       **ΣFi**       **Factor**        **PF
                                 ajustar**                                    ajustado**

---

          WiFiAnalyzer               95             42            1.07           102

          WiFiSurveyor               72             38            1.03            74

python-wifi-survey-heatmap 63 30 0.95 60

      Wireless HeatMapper           203             52            1.17           238

---

#### Complejidad del sistema

El Wireless HeatMapper alcanza 238 puntos de función ajustados, valor
superior al de los tres proyectos de referencia, lo que refleja la
incorporación del módulo de inteligencia artificial, la gestión de
modelos entrenados, las salidas comparativas (escenario actual vs.
proyectado), la operación bajo una arquitectura cliente-servidor en
línea con base de datos central PostgreSQL, y la adición de una
plataforma web complementaria con panel de administración y portal
de cliente. Respecto a una variante con persistencia local móvil, el
conteo es ligeramente menor porque desaparece el grupo lógico de
datos de dominio en el dispositivo y porque las entradas no requieren
gestión de buffer persistente, sino transmisión en línea por request.
El desglose del conteo para el proyecto propio es el siguiente:

---

**Parámetro** **Cantidad** **Complejidad **Peso\*\* **Subtotal**
predominante\*\*

---

    Entradas de         6        Medio / Complejo      4-6             28
      usuario

    Salidas de          9            Complejo           7              63
      usuario

     Consultas          5        Medio / Complejo      4-6             25

     Archivos           5        Medio / Complejo     10-15            55
     internos
     lógicos

    Interfaces          4        Medio / Complejo      7-10            32
     externas

     Total sin                                                        203
      ajustar

---

**PF = 203 × \[0.65 + 0.01 × 52\] = 203 × 1.17 ≈ 238 puntos de función**

> Detalle del recuento de archivos internos lógicos (5): proyectos,
> planos, mediciones WiFi, modelos de IA y usuarios/credenciales.
> Todos residen exclusivamente en la base de datos central
> PostgreSQL del backend; no existe un sexto grupo lógico
> correspondiente a una base local en el dispositivo móvil.

## Complejidad del Software

La complejidad del Wireless HeatMapper es calificada como alta, en
concordancia con la naturaleza de sus componentes técnicos. La
evaluación se realiza sobre los seis factores principales del sistema:

### Procesamiento de datos

La aplicación debe capturar y transmitir en línea grandes volúmenes
de muestras de señal (RSSI, SSID, BSSID, canal y frecuencia) durante
el recorrido del espacio. La gestión eficiente de esta información
requiere un diseño cuidadoso de los endpoints REST de ingesta, del
control de concurrencia en el backend y del manejo de reintentos
controlados ante latencias o errores transitorios.

### Análisis de señal

El análisis incluye la identificación de zonas muertas, la detección de
solapamiento entre puntos de acceso y el reconocimiento de
interferencias por canal, procesos que implican comparaciones
multidimensionales sobre los datos capturados.

### Algoritmos de interpolación

La transformación de puntos de medición dispersos en un campo de
cobertura continuo se realiza mediante técnicas de interpolación
espacial (por ejemplo, interpolación de distancia inversa ponderada o
kriging). Estos algoritmos se ejecutan en el backend FastAPI, lo que
libera al cliente móvil de la carga computacional pero introduce
exigencias de rendimiento sobre el servidor y de eficiencia en la
serialización del campo continuo devuelto al cliente.

### Uso de inteligencia artificial

El módulo de recomendación de posicionamiento de puntos de acceso emplea
un modelo de aprendizaje automático entrenado con patrones de
propagación de señal, geometría de planos y características del entorno
físico. El modelo está hospedado en el backend y se consume vía API
REST tanto desde la app móvil como desde el portal de cliente, lo que
representa el componente de mayor complejidad técnica del proyecto.

### Interfaces móviles

La aplicación debe ofrecer una experiencia de usuario fluida en
pantallas de tamaño reducido, con visualizaciones de mapas de calor
interactivas que permitan zoom, desplazamiento y superposición de capas
informativas sobre el plano importado, manteniendo a la vez una
indicación clara del estado de conexión con el backend.

### Arquitectura cliente-servidor en línea

El sistema opera bajo una arquitectura cliente-servidor estrictamente
en línea en la que el backend FastAPI con base de datos central
PostgreSQL constituye la única fuente de verdad. El cliente móvil
no almacena entidades de dominio entre sesiones: cada captura,
cada calibración de plano y cada solicitud de heatmap o análisis
se traduce en un request HTTPS contra el backend. Esta decisión
introduce una complejidad técnica centrada en el manejo de latencia,
en la atomicidad de cada request, en la indicación visible del
estado de red al técnico y en la pausa controlada de la captura
ante pérdidas de conectividad, en lugar de un protocolo de
sincronización diferida.

## Estimaciones

### Dimensiones del proyecto

#### Tamaño: Alto

Según los proyectos de referencia analizados, el Wireless HeatMapper
en modalidad 100 % en línea se ubica en un rango de tamaño **alto**:
su conteo de 238 puntos de función ajustados supera ampliamente a los
tres sistemas comparados, y su estimación de KLDC (desarrollada en la
sección de métodos de estimación) se sitúa en el orden de los 18.5
KLDC, considerando los dos componentes del sistema: app móvil
Android (cliente delgado) y plataforma web con backend REST.

#### Complejidad: Alta

La presencia de algoritmos de interpolación espacial, integración de
un modelo de inteligencia artificial, acceso al hardware WiFi de
Android, visualización interactiva de mapas de calor y la operación
bajo una arquitectura cliente-servidor estrictamente en línea entre
el cliente móvil y el servidor web sitúan al sistema en la categoría
de complejidad alta.

#### Estabilidad: Media

Los requisitos funcionales principales están bien definidos a partir del
caso real de Bulldog Tech.; sin embargo, la especificación del módulo de
IA y los detalles del plan de implementación de APs pueden evolucionar
durante el desarrollo, lo que introduce una estabilidad media.

## Ámbito del proyecto

### Objetivo general

Desarrollar un sistema integrado y estrictamente en línea, compuesto
por una aplicación móvil para Android y una plataforma web
complementaria, que permita a los técnicos de Bulldog Tech. realizar
el relevamiento, análisis y optimización de la cobertura de redes WiFi
en espacios interiores mediante la generación de mapas de calor
basados en mediciones reales transmitidas en tiempo real al backend
y recomendaciones automáticas de posicionamiento de puntos de acceso
apoyadas en inteligencia artificial; y que adicionalmente provea un
panel de administración para la gestión organizacional de los técnicos
y un portal de cliente para la visualización interactiva de los
resultados entregados.

### Objetivos específicos

- Implementar un módulo de captura automática de parámetros de señal
  WiFi (RSSI, SSID, BSSID, canal y frecuencia) durante el recorrido del
  espacio, transmitiendo cada muestra en línea al backend mediante
  endpoints REST.

- Desarrollar la funcionalidad de importación y georreferenciación de
  planos de edificios en formato PNG o PDF, permitiendo asociar cada
  medición a una coordenada sobre el plano almacenado de forma central
  en el backend.

- Implementar algoritmos de interpolación espacial, ejecutados en el
  backend, para generar mapas de calor continuos que representen la
  distribución de cobertura WiFi sobre el plano del edificio.

- Desarrollar el módulo de análisis de cobertura, capaz de identificar
  automáticamente zonas muertas, interferencias entre canales y
  solapamientos entre puntos de acceso.

- Integrar un módulo de inteligencia artificial que sugiera posiciones
  óptimas de puntos de acceso tanto para redes en producción
  (reubicación) como para proyectos nuevos (planificación).

- Implementar la generación de reportes técnicos exportables que
  documenten la cobertura relevada y el plan de implementación
  propuesto.

- Desarrollar un panel de administración web que permita gestionar las
  cuentas de los técnicos (alta, baja y activación) y supervisar la
  totalidad de los proyectos de la organización.

- Desarrollar un portal web de cliente que permita visualizar de forma
  interactiva los mapas de calor (actual y proyectado), el análisis de
  cobertura y el plan de APs recomendado, accesible mediante un enlace
  único generado por el técnico al cierre del proyecto.

## Requerimientos principales

### RP1: Captura de señal WiFi

La aplicación debe escanear automáticamente las redes WiFi disponibles
en cada punto del recorrido y registrar los parámetros RSSI, SSID,
BSSID, canal y frecuencia, asociándolos a la posición actual del usuario
sobre el plano y transmitiéndolos en línea, request por request, al
backend para su persistencia en la base de datos central. El cliente
móvil no almacena las muestras entre sesiones: cada lote capturado se
envía en el momento y se descarta del estado en memoria una vez
confirmado por el servidor.

### RP2: Mapeo sobre plano

El sistema debe permitir la importación de planos de edificios en
formato PNG o PDF como imagen de referencia. Al importarse, el plano
se sube de inmediato al backend y se asocia al proyecto en curso; el
usuario puede entonces marcar puntos de medición o registrarlos de
forma continua durante el recorrido, viéndolos reflejados en línea
sobre el plano servido por el backend.

### RP3: Generación de heatmap

A partir de los puntos de medición registrados en el backend, el
servicio de interpolación espacial del backend debe generar un mapa
de calor continuo y devolverlo al cliente para su visualización,
utilizando una escala de color graduada (verde para señal excelente,
rojo para zona muerta o señal nula). El cliente móvil no ejecuta la
interpolación: solamente solicita el heatmap actualizado al backend
y lo renderiza.

### RP4: Análisis de cobertura

El sistema debe analizar automáticamente el mapa de calor generado para
identificar zonas muertas, puntos de solapamiento excesivo entre APs e
interferencias por canal, y presentar los resultados al usuario de forma
clara y estructurada.

### RP5: Optimización mediante IA

La aplicación debe incorporar un módulo de inteligencia artificial que,
a partir del análisis de cobertura y del inventario RF del sitio, sugiera
escenarios completos para instalaciones nuevas o redes existentes. Cada
escenario debe distinguir AP físico, radio y BSSID; recomendar cantidad,
posición, altura, modelo, antena, canal, ancho y potencia por radio; producir
resultados separados para 2,4 GHz y 5 GHz; y generar valores y mapas de calor
proyectados sin modificar las mediciones observadas. El detalle técnico
aprobado se define en la [Especificación de Optimización RF por Escenarios](PLAN-IMPLEMENTACION/17-especificacion-optimizacion-rf/00-indice.md).

### RP6: Generación de reportes

El sistema debe permitir la exportación de reportes técnicos que
documenten el estado actual de la cobertura, las zonas problemáticas
identificadas y el plan de implementación propuesto, en un formato
adecuado para ser entregado al cliente como parte del cierre del
proyecto.

### RP7: Administración de usuarios

La plataforma web debe proveer un panel de administración con
autenticación basada en roles que permita crear, activar y desactivar
cuentas de técnicos, así como visualizar el listado completo de los
proyectos de la organización con su estado y actividad reciente. Esta
funcionalidad resuelve la dependencia de aprovisionamiento previo de
usuarios identificada en la historia de autenticación de la app móvil.

### RP8: Persistencia centralizada en línea

Todas las entidades del dominio del sistema —proyectos, planos
calibrados, puntos de medición, mediciones WiFi capturadas, análisis
de cobertura y mapas de calor generados— residen exclusivamente en
la base de datos central PostgreSQL del backend. La aplicación móvil
opera mediante sesiones REST autenticadas contra el backend y no
mantiene estado de dominio entre ejecuciones: al iniciar sesión, el
técnico recupera del backend el listado de sus proyectos y, al
trabajar en uno, todas las operaciones de lectura y escritura se
realizan directamente contra el servidor. No existen mecanismos de
sincronización diferida ni de reconciliación de estado, dado que no
hay un estado paralelo en el dispositivo.

### RP9: Portal de cliente

El sistema debe permitir al técnico generar, al cierre de un proyecto,
un enlace único de acceso para que el cliente visualice los resultados
en un portal web sin necesidad de instalar la aplicación móvil. El
portal debe presentar el mapa de calor actual, el mapa de calor
proyectado, el análisis de cobertura y el plan de implementación de
APs de forma interactiva, con autenticación por token de un solo
proyecto y expiración configurable.

## Rendimiento

### Tiempo de procesamiento de mapas

La generación del mapa de calor a partir de los puntos de medición no
debe superar los 5 segundos extremo a extremo (request del cliente,
interpolación en backend y entrega de la respuesta) para encuestas de
hasta 200 puntos de medición, garantizando una respuesta ágil durante
el trabajo en campo.

### Tiempo de respuesta de la aplicación

La interfaz de usuario debe responder a las interacciones del usuario
(zoom, desplazamiento, selección de puntos) en un tiempo inferior a 500
milisegundos sobre datos ya recibidos del backend, de modo que la
experiencia de uso en campo no se vea comprometida.

### Latencia de red end-to-end

Sobre una conexión móvil estable, el envío de un lote de scan WiFi al
backend debe completarse con un percentil 95 (p95) ≤ 1 segundo, y la
solicitud de un heatmap actualizado debe responderse con p95 ≤ 3
segundos. Estos objetivos se miden incluyendo el viaje de red en
ambas direcciones y son condición indispensable para la experiencia
en campo del técnico, dado que toda operación es en línea.

## Fiabilidad

### Precisión de medición

Los valores de RSSI registrados deben ser consistentes con los
reportados por el hardware WiFi del dispositivo, sin transformaciones
que introduzcan desviaciones. La precisión del posicionamiento sobre el
plano depende del método de localización empleado y debe ser documentada
en el manual de usuario.

### Consistencia del análisis

Dada la misma colección de datos de medición almacenados en el
backend, el sistema debe producir resultados idénticos en sucesivas
ejecuciones del análisis. El algoritmo de interpolación y el modelo
de IA deben operar de forma determinista o documentar explícitamente
cualquier componente estocástico.

## Restricciones

### Técnicas

#### Limitaciones de sensores móviles

Los sensores WiFi de los dispositivos Android acceden a la intensidad de
señal a través de la API del sistema operativo (WifiManager), que impone
restricciones en la frecuencia de escaneo (scan throttling) a partir de
Android 8.0. El diseño de la aplicación debe contemplar estas
limitaciones para no degradar la densidad de muestras recolectadas.

#### Precisión en interiores

La localización GPS pierde precisión en espacios interiores. La
aplicación deberá recurrir a métodos alternativos de posicionamiento
(marcado manual sobre el plano o posicionamiento relativo por
desplazamiento) cuya exactitud quedará acotada por la interacción del
usuario.

#### Conectividad obligatoria

Por diseño, el sistema no contempla un modo desconectado: todas las
operaciones funcionales del técnico (autenticación, apertura de
proyecto, importación de plano, captura de mediciones, solicitud de
heatmap, análisis y exportación de reportes) requieren conectividad
a internet activa con el backend. Ante una caída o degradación de la
red, la aplicación debe notificar al técnico, pausar de forma
explícita la captura en curso y reanudarla solamente cuando el
backend confirme nuevamente disponibilidad. No se mantiene un buffer
persistente de mediciones en el dispositivo: las muestras capturadas
durante una ventana sin conectividad se descartan o se reintentan
de forma acotada en memoria, según el patrón de reintento exponencial
acordado, sin pérdida silenciosa para el usuario.

#### Seguridad de la plataforma web

El portal de cliente debe implementar autenticación mediante token de
enlace único de un solo proyecto, con expiración configurable y
contador de accesos auditable. El panel de administración debe
operar bajo un esquema de roles diferenciados (Administrador y
Técnico) con autenticación basada en credenciales y manejo de sesión
sobre HTTPS. Las contraseñas deben almacenarse hasheadas (bcrypt) en
la base de datos central.

#### Compatibilidad de navegadores

La plataforma web debe ser funcional en las dos últimas versiones
estables de los navegadores Chrome, Firefox y Safari, sin requerir la
instalación de extensiones ni complementos adicionales por parte del
usuario.

### Recursos

#### Tiempo de desarrollo

El proyecto se desarrolla en el marco de un semestre académico, lo que
impone una restricción temporal de aproximadamente seis meses para la
entrega del prototipo funcional.

#### Herramientas disponibles

El equipo de desarrollo dispone de Android Studio y Flutter SDK como
entorno principal para la app móvil, Python (FastAPI) para el
desarrollo del backend y del modelo de inteligencia artificial,
React + TypeScript para la plataforma web, PostgreSQL como motor de
base de datos central, Docker para la contenerización del backend y
las herramientas de control de versiones y colaboración provistas
por GitHub.

## Interfaces externas

### Dispositivos móviles

La aplicación está dirigida a dispositivos Android con API nivel 26
(Android 8.0 Oreo) o superior, que dispongan de interfaz WiFi activa,
conectividad de datos hacia el backend y capacidad de procesamiento
suficiente para renderizar mapas de calor recibidos del servidor.

### Sensores WiFi

El acceso al hardware WiFi se realiza a través de la API WifiManager de
Android, que expone la información de las redes detectadas en cada
escaneo, incluyendo RSSI, SSID, BSSID, canal y frecuencia.

### Servicios en la nube

El sistema integra un servidor backend desplegado en la nube que cumple
tres funciones operadas estrictamente en línea: (i) ingesta y
persistencia central de proyectos, planos, mediciones, análisis y
heatmaps consumida por la app móvil durante todo el ciclo de vida
del proyecto, (ii) hospedaje del modelo de IA expuesto vía API REST,
y (iii) provisión de la base de datos central PostgreSQL que sustenta
tanto el panel de administración como el portal de cliente. El
backend constituye la única fuente de verdad del dominio.

### APIs de análisis

El módulo de inteligencia artificial está hospedado de forma
definitiva en el servidor backend (FastAPI) y expone endpoints REST
(`/optimize-aps`, `/predict-coverage`) que son consumidos tanto por la
app móvil para obtener recomendaciones en campo, como por el portal
de cliente para re-ejecutar la inferencia bajo demanda al visualizar
los resultados. Esta arquitectura libera al dispositivo móvil de la
carga computacional del modelo y centraliza el ciclo de actualización.

### Navegador web

La plataforma web es accesible desde cualquier navegador moderno sin
necesidad de instalación. El panel de administración requiere
autenticación con credenciales de Administrador o Técnico, mientras
que el portal de cliente se accede mediante un enlace único con token
de un solo proyecto.

## Métodos de estimación

Se aplicaron tres métodos de estimación complementarios para obtener
rangos de esfuerzo y tamaño consistentes: estimación basada en líneas de
código mediante la fórmula de tres puntos, el modelo COCOMO II con
puntos de objeto y la técnica de Planning Poker sobre las historias de
usuario principales.

### Estimación basada en líneas de código

#### Escenarios: optimista, probable, pesimista

Se definen tres escenarios de tamaño en KLDC tomando como referencia los
proyectos de menor complejidad (python-wifi-survey-heatmap, 2.5 KLDC) y
mayor complejidad (WiFiAnalyzer, 25 KLDC) del conjunto analizado, y
considerando el alcance funcional del Wireless HeatMapper en su
modalidad 100 % en línea, que comprende dos componentes (app móvil
cliente delgado + plataforma web con backend) sin código dedicado a
persistencia local ni a protocolos de sincronización:

---

       **Escenario**             **KLDC**            **Justificación**

---

         Optimista                  12              Solo funciones core
                                                  (RP1--RP3) más admin
                                                       web mínimo

         Probable                   18              Todas las funciones
                                                  (RP1--RP9): app móvil
                                                  como cliente REST
                                                  delgado + plataforma
                                                  web + backend

         Pesimista                  27            Funciones completas con
                                                    refactorizaciones,
                                                  pruebas extensas y
                                                  endurecimiento de
                                                       seguridad web

---

Aplicando la fórmula de valor esperado de Pressman (2010):

**KLDC esperado = (S_opt + 4 × S_m + S_pes) / 6**

KLDC esperado = (12 + 4 × 18 + 27) / 6 = 111 / 6 ≈ 18.5 KLDC

Con una productividad de referencia de 350 LOC/PM (derivada de los
proyectos analizados), el esfuerzo estimado es:

**Esfuerzo = 18 500 / 350 ≈ 53 personas-mes**

Para un equipo de dos personas: duración estimada ≈ 26 meses. Este
valor representa el esfuerzo total acumulado y sirve como cota
superior para la planificación con los demás métodos.

### Modelo COCOMO II

El modelo COCOMO II en su variante de composición de aplicación utiliza
puntos de objeto para estimar el esfuerzo en etapas tempranas. Los
elementos contabilizados son pantallas de interfaz, reportes y
componentes de software.

#### Pantallas

Se identificaron 19 pantallas principales: en la app móvil —inicio de
sesión, panel principal, nueva encuesta, importación de plano,
escaneo activo, visualización de mapa de calor, resultados de
análisis, detalle de zona, recomendaciones de IA, comparación de
escenarios, configuración de reporte, vista previa del reporte,
historial de proyectos, ajustes de la aplicación—; y en la plataforma
web —login web, dashboard de administración, gestión de usuarios,
listado de proyectos de la organización, vista interactiva del
portal de cliente (heatmap + análisis + plan AP).

#### Reportes

Se definieron 6 tipos de reporte: cobertura WiFi detallada, análisis
de interferencias, plan de implementación de APs, comparación de
escenarios (antes/después), resumen ejecutivo para el cliente y
reporte interactivo web exportable desde el portal de cliente.

#### Componentes

Se identificaron 32 componentes principales, entre ellos: escáner
WiFi, cliente HTTP autenticado, motor de interpolación espacial
(backend), renderizador de mapas de calor, analizador de cobertura,
módulo de posicionamiento interior, parser de planos, modelo de IA,
módulo de recomendaciones, generador de reportes, módulo de
autenticación web, gestor de tokens de enlace, controlador REST de
administración de usuarios, controlador REST de proyectos y
mediciones, módulo de roles y permisos, renderizador de heatmap web,
indicador de estado de conectividad, entre otros.

---

     **Tipo**     **Cantidad**   **Complejidad**     **Peso**     **Puntos de
                                                                    Objeto**

---

    Pantallas          19             Medio             2              38

     Reportes          6             Difícil            8              48

Componentes 32 Medio 2 64

    Total NOP                                                         150

---

Considerando que no existe reutilización de código de otros proyectos
(NOP = 150) y una tasa de productividad PROD = 7 NOP/PM correspondiente
a un equipo con experiencia media en el dominio, el esfuerzo estimado
es:

**Esfuerzo = NOP / PROD = 150 / 7 ≈ 21 personas-mes**

Para dos desarrolladores, esto equivale a una duración de
aproximadamente 10.5 meses.

### Planning Poker

#### Historias de usuario

Se estimaron los nueve requerimientos principales utilizando la
técnica de Planning Poker con la escala de Fibonacci. La estimación
refleja la complejidad relativa percibida por el equipo de
desarrollo, considerando que la operación es estrictamente en línea
y que el cliente móvil no implementa lógica de persistencia local
ni de sincronización diferida.

#### Estimación por puntos

---

**Requerimiento** **Descripción resumida** **Puntos de
historia**

---

          RP1            Captura automática de señal WiFi           13
                          (envío en línea al backend)

          RP2            Mapeo de mediciones sobre plano            21

          RP3            Generación de mapa de calor por            21
                            interpolación (en backend)

          RP4            Análisis automático de cobertura           13

          RP5         Módulo de IA para optimización de APs         34

          RP6          Generación y exportación de reportes         8

          RP7        Administración de usuarios (panel web)         8

          RP8         Persistencia centralizada en línea            5
                       (cliente REST tipado del backend)

          RP9        Portal de cliente con enlace único              13

         Total                                                     136

---

Con una velocidad de sprint de 20-25 puntos por iteración (sprints de
dos semanas), se estiman 6 sprints (12 semanas) para el desarrollo
de los requerimientos principales.

## Ecuación del Software

El modelo dinámico multivariable de Putnam y Myers, formalizado por
Pressman (2010) como la Ecuación del Software, permite estimar el tiempo
mínimo de desarrollo a partir del tamaño del sistema:

**t_mín = 8.14 × (LOC / P)\^0.43**

### Cálculo de esfuerzo

Para el Wireless HeatMapper en modalidad 100 % en línea se emplean los
siguientes parámetros:

---

     **Parámetro**         **Valor**             **Justificación**

---

      LOC estimado           18 500          Estimación de tres puntos
                                                   (sección 12.1)

P (productividad) 10 000 Software de telecomunicaciones
(Pressman, 2010)

      B (factor de            0.34         Proyecto de tamaño mediano-alto
       habilidad)                          con arquitectura cliente-servidor
                                            en línea (10 000 -- 70 000 LOC)

---

t_mín = 8.14 × (18 500 / 10 000)\^0.43 = 8.14 × 1.85\^0.43 ≈ 8.14 ×
1.30 ≈ 10.6 meses

**t_mín ≈ 11 meses**

### Parámetros de productividad

E = 180 × B × t³ (t en años, E en personas-mes)

E = 180 × 0.34 × (0.883)³ = 61.2 × 0.689 ≈ 42 personas-mes

### Estimación del equipo de trabajo

Para una duración objetivo de 11 meses con 2 desarrolladores, la
ecuación del software arroja un esfuerzo de 42 PM, valor que actúa
como cota superior conservadora para el sistema integrado en
modalidad en línea (app móvil cliente delgado + plataforma web). La
estimación COCOMO II (21 PM) y la estimación por Planning Poker
(12 semanas de sprint para los requerimientos principales) son más
representativas para el alcance inicial del prototipo funcional.

---

        **Método**         **Esfuerzo estimado**       **Duración (2
                                                        personas)**

---

     Estimación LOC (3             53 PM              26 meses (cota
          puntos)                                        superior)

     COCOMO II (puntos             21 PM                 10.5 meses
          objeto)

Ecuación del Software 42 PM 11 meses

      Planning Poker            6 sprints              12 semanas
         (sprints)                                       (\~3 meses)

---

El rango de estimación razonable para el prototipo funcional se sitúa
entre 12 semanas (Planning Poker, requerimientos principales) y
10.5 meses (COCOMO II, sistema completo). La diferencia refleja el
alcance incremental del desarrollo ágil adoptado y la simplificación
del cliente móvil al operar exclusivamente en línea.

## Planificación del tiempo

### Diagrama de Gantt

La planificación se organiza en siete fases iterativas alineadas con la
metodología Scrum, distribuidas a lo largo de un período de **4 meses
de desarrollo (abril – julio 2026)**, conforme a la velocidad estimada
mediante Planning Poker (6 sprints de 2 semanas = 12 semanas; §13).
Sprint 0 y Sprint 1 se ejecutan en las primeras 2 semanas y se
presentan conjuntamente el **27 de abril de 2026**. Las fases del
componente web se ejecutan en paralelo y de forma incremental,
comenzando con la infraestructura del backend en el Sprint 1; el
cliente HTTP autenticado del móvil (RP8) se construye de forma
transversal desde el primer sprint y no requiere una fase dedicada:

---

      **Fase**         **Actividad        **Fecha inicio**    **Fecha fin**
                       principal**

---

          1            S0+S1: Análisis,   13 abr 2026         27 abr 2026
                      diseño e infra
                      + fundación CRUD
                    (RP7 y RP8 incluidos
                     en este sprint)

          2            S2+S3: RP1+RP2:   28 abr 2026          25 may 2026
                    Captura de señal
                  (envío en línea) y
                  mapeo sobre plano

          3            S4: RP3+RP4:      26 may 2026           8 jun 2026
                  Heatmap (backend) y
                       análisis de
                        cobertura

          4         S5: RP5: Módulo      9 jun 2026           22 jun 2026
                    de IA y
                  recomendaciones
                  (backend FastAPI)

          5         S6: RP9: Portal      23 jun 2026           6 jul 2026
                    de cliente (web)

          6              RP6 +            7 jul 2026          11 jul 2026
                      integración +
                    pruebas + entrega

---

### Diagrama de PERT

Las dependencias entre actividades identificadas para el diagrama PERT
son las siguientes. Nótese que en la modalidad 100 % en línea no
existe una actividad dedicada a sincronización app↔servidor: el
cliente HTTP del móvil consume directamente los endpoints del backend
desde el primer sprint y queda absorbido en las actividades B, C, D
y E:

---

**Actividad** **Descripción** **Precedencia**

---

         A           Análisis de requisitos y diseño           ---

         B        Implementación del escáner WiFi y             A, J
                  cliente REST de ingesta (RP1)

         C         Importación y georreferenciación de          A, J
                              planos (RP2)

         D        Algoritmo de interpolación y heatmap        B, C
                          en backend (RP3)

         E        Módulo de análisis de cobertura (RP4)         D

         F           Entrenamiento del modelo de IA             D

         G         Integración del módulo de IA (RP5)         E, F

         J        Backend FastAPI: infraestructura,             A
                  base de datos PostgreSQL y endpoints
                          REST de dominio

         K        Panel de administración web (RP7)            J

         M        Portal de cliente web (RP9)                   G

         H            Generación de reportes (RP6)              G

         I          Pruebas de integración y ajustes        H, K, M
                                 finales

---

La ruta crítica del proyecto es: A → J → C → D → F → G → M → I,
correspondiente a las actividades con mayor tiempo estimado y sin
holgura, donde el portal de cliente se mantiene como actividad
crítica posterior a la integración del módulo de IA. La eliminación
de la actividad de sincronización acorta la ruta crítica respecto a
una variante con persistencia local móvil.

## Gestión de riesgos

### Riesgos técnicos

---

     **Riesgo**      **Probabilidad**   **Impacto**        **Estrategia de
                                                            mitigación**

---

Limitaciones de Alta Medio Implementar mecanismo de
scan throttling muestreo adaptativo;
en Android 8+ documentar densidad
mínima recomendada.

      Precisión           Media             Alto       Definir densidad mínima

insuficiente del de muestras por metro
algoritmo de cuadrado; validar con
interpolación con datos reales de Bulldog
baja densidad de Tech.
muestras

Rendimiento del Media Alto El modelo se ejecuta
modelo de IA sobre exclusivamente en backend;
hardware limitado dimensionar el servidor
y aplicar caché de
inferencias por proyecto.

Seguridad del Media Alto Token UUID v4 firmado,
enlace de cliente expiración configurable,
(token reutilizable contador de accesos
o expuesto) auditable; revocación
manual desde la app.

Pérdida de Alta Alto Indicador visible del
conectividad en estado de red, reintento
campo (modo en exponencial acotado por
línea exclusivo) request, pausa explícita
de la captura ante caída
de red y reanudación
controlada al recuperar
conexión.

---

### Riesgos de desarrollo

---

    **Riesgo**      **Probabilidad**     **Impacto**      **Estrategia de
                                                           mitigación**

---

Subestimación Alta Alto Priorizar el
del esfuerzo entrenamiento del
requerido para modelo en las
el módulo de IA primeras
iteraciones;
ajustar alcance si
es necesario.

Cambios en los Media Medio Mantener el módulo
requisitos del de IA desacoplado
módulo de IA mediante una
durante el interfaz estable;
desarrollo usar Feature Flags
para activarlo
progresivamente.

---

### Riesgos de entorno

---

      **Riesgo**      **Probabilidad**     **Impacto**     **Estrategia de
                                                            mitigación**

---

    Restricciones           Alta              Medio        Planificar con
    académicas que                                            margen de

limiten las horas holgura;
de desarrollo priorizar los
requerimientos de
mayor valor (RP3,
RP5).

Indisponibilidad Media Medio Construir un
de instalaciones conjunto de datos
de Bulldog Tech. de prueba
para pruebas en sintético para
campo validación
temprana del
algoritmo.

Costo de Alta Medio Usar tier gratuito de
infraestructura proveedor cloud (Render,
cloud para etapa Fly.io o similar);
académica desplegar contenedor
único Docker.

---

## Tabla de recursos

### Hardware

---

        **Recurso**            **Cantidad**               **Uso**

---

Computadora portátil de 2 Desarrollo de la
desarrollo aplicación y
entrenamiento del
modelo de IA

Smartphone Android (API 2 Pruebas unitarias, de
26+) integración y pruebas
en campo (siempre en
línea con el backend)

    Enrutadores WiFi de              2            Generación de entornos
          prueba                                     controlados para
                                                      validación del
                                                         algoritmo

---

### Software

---

            **Herramienta**                         **Uso**

---

            Android Studio                Entorno de desarrollo de la
                                              aplicación Android

             Python 3.10+               Desarrollo y entrenamiento del
                                                 modelo de IA

        TensorFlow / ONNX Runtime       Despliegue del modelo en el
                                              backend FastAPI

             Git / GitHub             Control de versiones y gestión del
                                                  repositorio

                 Figma                Diseño de prototipos de interfaz de
                                                    usuario

        Microsoft Word / LaTeX            Documentación del proyecto

           Flutter SDK / Dart           Desarrollo de la aplicación
                                       móvil Android (cliente REST)

        FastAPI (Python 3.10+)         Backend REST: dominio, IA y
                                       administración de usuarios

         React + TypeScript            Plataforma web (panel de
                                       administración y portal de cliente)

               Node.js / npm           Toolchain de construcción del
                                                  frontend web

              PostgreSQL 15+            Base de datos central del servidor
                                       backend (única fuente de verdad)

                  Docker                Contenerización y despliegue del
                                                 servidor backend

                  Nginx                 Servidor web reverse-proxy y
                                              hospedaje del bundle React

---

> Nota: en esta modalidad 100 % en línea no se utiliza ninguna base
> de datos local en el dispositivo móvil; la totalidad del estado de
> dominio se gestiona en PostgreSQL a través del backend.

### Recursos humanos

---

          **Rol**               **Nombre**          **Responsabilidad**

---

      Desarrollador /        Fernandez Ortega     Backend Android, módulo
       Investigador          Jhasmany Jhunnior      WiFi, cliente REST y
                                                  experiencia en línea

      Desarrollador /     Quiroga Flores Herland       Módulo de IA,
       Investigador                Borys               algoritmos de
                                                      interpolación,
                                                  generación de reportes

       Docente tutor       Ing. Rolando Martínez  Supervisión académica y
                                                    revisión de avances

---

### Infraestructura

---

              **Recurso**                           **Uso**

---

          Repositorio GitHub            Alojamiento del código fuente y
                                            gestión de incidencias

Servidor backend en la nube Hospedaje de la API REST,
del modelo de IA y de la
base de datos PostgreSQL
central

    Instalaciones de Bulldog Tech.    Pruebas en campo en entornos reales

---

## Organización interna

### Estructura del equipo

El equipo está conformado por dos desarrolladores-investigadores con
dedicación compartida entre el desarrollo del sistema y la investigación
sobre los algoritmos de interpolación e inteligencia artificial. Ambos
miembros participan en todas las fases del proyecto, con una
distribución de responsabilidades por componente según se detalla en la
tabla de recursos humanos.

### Roles

---

                **Rol**                      **Responsabilidades**

---

      Product Owner (compartido)         Definición y priorización del
                                        backlog; validación con Bulldog
                                                     Tech.

        Scrum Master (rotativo)        Facilitación de ceremonias Scrum;
                                          eliminación de impedimentos

         Desarrollador Android         Implementación de RP1, RP2, RP3,
                                       RP6 y cliente REST en línea

        Ingeniero de IA / Datos           Implementación de RP4, RP5,
                                       entrenamiento y ajuste del modelo

---

## Mecanismos de seguimiento y control

### Reuniones Scrum

#### Daily

Reunión diaria de 15 minutos para sincronizar el avance, identificar
impedimentos y ajustar el plan del día. Se realiza de forma presencial o
mediante videollamada según la disponibilidad del equipo.

#### Sprint Review

Al final de cada sprint (cada dos semanas), el equipo presenta las
funcionalidades completadas al docente tutor y, cuando sea posible, a un
representante de Bulldog Tech. El resultado de esta revisión alimenta el
backlog de la siguiente iteración.

#### Sprint Retrospective

Reunión interna al término de cada sprint para analizar los procesos de
trabajo, identificar oportunidades de mejora y acordar acciones
concretas para el siguiente ciclo.

### Control del proyecto

#### Seguimiento de tareas

Las tareas se gestionan mediante el tablero Kanban del repositorio en
GitHub (GitHub Projects), con columnas de estado: Pendiente, En
progreso, En revisión y Completado. Cada tarea está asociada a un
requerimiento principal y a un sprint.

#### Evaluación del progreso

Al inicio de cada sprint se actualiza el gráfico de avance (burndown
chart) con los puntos de historia completados frente a los planificados.
Si la velocidad real difiere en más de un 20 % de la planificada durante
dos sprints consecutivos, el equipo convoca una reunión extraordinaria
para revisar el alcance o redistribuir tareas.


# 2. Modelos de Desarrollo


El proyecto Wireless HeatMapper utiliza modelos UML 2.5+ como soporte tecnico del proceso Scrum. Estos modelos permiten representar el sistema desde cuatro perspectivas obligatorias: contexto, arquitectura, datos y logica. Cada perspectiva tiene un proposito distinto y se vincula con diagramas PlantUML versionados en `docs/SW2/diagramas/`, de forma que el documento academico, la herramienta CASE y el repositorio mantengan la misma fuente de verdad.

Los modelos se aplican sobre la modalidad 100 % en linea del producto: la aplicacion movil actua como cliente delgado, el backend FastAPI concentra la logica de negocio, PostgreSQL es la unica fuente persistente de datos de dominio y la plataforma web cubre la administracion y el portal de cliente.

### Modelo de contexto

El modelo de contexto delimita la frontera funcional de Wireless HeatMapper y muestra como interactuan los actores humanos y sistemas externos con el producto. Su objetivo es aclarar que responsabilidades pertenecen al sistema y que responsabilidades quedan fuera de el.

En este proyecto, el contexto distingue al tecnico de campo, administrador, cliente, Android WifiManager API y servicio interno de IA. Tambien resume los casos de uso principales relacionados con autenticacion, proyectos, planos, captura WiFi, heatmaps, administracion, propuestas IA y consulta por enlace.

| Diagrama | Tipo UML | Bloque PlantUML |
| -------- | -------- | --------------- |
| Modelo de Contexto - Wireless HeatMapper | Casos de uso | [01-modelo-contexto.puml](../diagramas/01-modelo-contexto.puml) |

### Modelo de arquitectura

El modelo de arquitectura describe la organizacion tecnica del sistema y las responsabilidades de cada componente. Sirve para verificar que la solucion respeta el stack acordado: Flutter/Dart para la app movil, React/TypeScript para la web, FastAPI para el backend, PostgreSQL como base central, Docker Compose y Nginx para despliegue.

La arquitectura se representa con dos vistas complementarias. La vista de paquetes muestra la separacion por capas y modulos de software. La vista de despliegue muestra los nodos de ejecucion, contenedores, artefactos y enlaces de comunicacion entre dispositivo Android, navegador, servidor cloud, backend, web, base de datos y GitHub Actions.

| Diagrama | Tipo UML | Bloque PlantUML |
| -------- | -------- | --------------- |
| Modelo de Arquitectura - Diagrama de Paquetes | Paquetes | [02-arquitectura-paquetes.puml](../diagramas/02-arquitectura-paquetes.puml) |
| Modelo de Arquitectura - Diagrama de Despliegue | Despliegue | [03-arquitectura-despliegue.puml](../diagramas/03-arquitectura-despliegue.puml) |

### Modelo de datos

El modelo de datos representa las entidades de negocio, sus atributos principales y relaciones. Su funcion es asegurar que la persistencia centralizada cubre los datos necesarios para ejecutar los flujos del producto sin almacenamiento local de dominio en la app movil.

El modelo conceptual incluye usuarios, clientes, proyectos, planos, puntos de medicion, lecturas RSSI, conjuntos AP, items de conjuntos, mapas de calor y tokens de enlace cliente. Tambien explicita relaciones de composicion y multiplicidad para reflejar que un proyecto contiene planos, mediciones, heatmaps y enlaces publicados.

| Diagrama | Tipo UML | Bloque PlantUML |
| -------- | -------- | --------------- |
| Modelo de Datos Conceptual - Wireless HeatMapper | Clases | [04-modelo-datos-conceptual.puml](../diagramas/04-modelo-datos-conceptual.puml) |

### Modelo de logica

El modelo de logica describe el comportamiento dinamico del sistema. A diferencia del modelo de datos, que muestra estructura, este modelo muestra secuencias de mensajes, cambios de estado y reglas de ejecucion observables durante los casos de uso principales.

Para SW2 se priorizan tres diagramas. El primero cubre la captura WiFi en linea y generacion de heatmap. El segundo cubre la publicacion de resultados y acceso del cliente mediante token. El tercero resume el ciclo de vida de un proyecto desde su creacion hasta archivo o reactivacion.

| Diagrama | Tipo UML | Bloque PlantUML |
| -------- | -------- | --------------- |
| Modelo de Logica - Captura WiFi y Generacion de Heatmap | Secuencia | [05-logica-captura-heatmap.puml](../diagramas/05-logica-captura-heatmap.puml) |
| Modelo de Logica - Publicacion y Portal Cliente | Secuencia | [06-logica-portal-cliente.puml](../diagramas/06-logica-portal-cliente.puml) |
| Modelo de Logica - Estados del Proyecto | Estados | [07-estados-proyecto.puml](../diagramas/07-estados-proyecto.puml) |

### Diagramas complementarios

Ademas de los cuatro modelos obligatorios, el paquete documental incluye diagramas de apoyo para demostrar trazabilidad con herramientas CASE y planificacion de pruebas. No reemplazan los modelos principales; sirven como evidencia academica de navegabilidad, validacion y control de calidad.

| Diagrama | Proposito | Bloque PlantUML |
| -------- | --------- | --------------- |
| Herramientas CASE - Navegabilidad entre modelos | Evidenciar trazas entre casos de uso, secuencias, clases, datos y pruebas. | [08-case-navegabilidad.puml](../diagramas/08-case-navegabilidad.puml) |
| Flujo de Trabajo de Pruebas - Proceso Unificado | Representar el flujo general de planificacion, ejecucion, correccion y validacion de pruebas. | [09-flujo-pruebas-rup.puml](../diagramas/09-flujo-pruebas-rup.puml) |

### Trazabilidad entre modelos

| Elemento funcional | Modelo de contexto | Modelo de arquitectura | Modelo de datos | Modelo de logica |
| ------------------ | ------------------ | ---------------------- | --------------- | ---------------- |
| Captura WiFi | UC05 Capturar senales WiFi | App movil, WifiScanner, backend, PostgreSQL | PuntoMedicion, LecturaRSSI | Secuencia captura WiFi y heatmap |
| Gestion de proyectos | UC01 Gestionar proyecto | App movil, web admin, backend | Proyecto, Usuario, Cliente | Estados del proyecto |
| Planos | UC02 Importar plano, UC03 Calibrar plano | App movil, backend, repositorios | Plano, PuntoMedicion | Secuencia captura WiFi y heatmap |
| Heatmaps | UC06 Generar mapa de calor | InterpolacionService, backend, PostgreSQL | MapaCalor, ConjuntoAP | Secuencia captura WiFi y heatmap |
| IA | UC08 Generar propuesta IA, UC09 Comparar propuesta | Modulo IA backend, OptimizadorAPService | ConjuntoAP, ConjuntoAPItem, MapaCalor | Comparacion derivada desde conjuntos AP |
| Portal cliente | UC15 Generar enlace cliente, UC16 Consultar heatmap, UC17 Ver conjuntos AP | Web portal, Nginx, backend share | TokenEnlaceCliente, MapaCalor, ConjuntoAP | Secuencia publicacion y portal cliente |
| Administracion | UC13 Gestionar usuarios, UC18 Ver proyectos organizacion, UC19 Gestionar clientes | Web admin, backend, PostgreSQL | Usuario, Cliente, Proyecto | Flujos CRUD administrativos |

### Criterios formales UML

- Los casos de uso separan actores humanos, sistemas externos y frontera del sistema.
- Los paquetes muestran responsabilidades por capa y dependencias dirigidas.
- El despliegue distingue nodos, contenedores, artefactos y canales de comunicacion.
- Las clases expresan atributos, multiplicidades, composicion y asociaciones relevantes.
- Las secuencias muestran participantes, mensajes sincronos, validaciones y persistencia.
- El diagrama de estados mantiene transiciones compatibles con los estados del proyecto.
- Todos los diagramas se mantienen como PlantUML para facilitar regeneracion, revision y uso en herramientas CASE.


## Evidencias de los cuatro modelos obligatorios


### modelo contexto

![modelo contexto](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/01-modelo-contexto.png)


### arquitectura paquetes

![arquitectura paquetes](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/02-arquitectura-paquetes.png)


### arquitectura despliegue

![arquitectura despliegue](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/03-arquitectura-despliegue.png)


### modelo datos conceptual

![modelo datos conceptual](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/04-modelo-datos-conceptual.png)


### logica captura heatmap

![logica captura heatmap](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/05-logica-captura-heatmap.png)


### logica portal cliente

![logica portal cliente](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/06-logica-portal-cliente.png)


### estados proyecto

![estados proyecto](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/07-estados-proyecto.png)



# 3. Manual de Garantía de Calidad del Software SQAP


**Organización:** Team 24 Software
**Eslogan:** Software medible, verificable y alineado al cliente
**Uso:** Manual institucional aplicable a todos los proyectos de software
**Código del documento:** SQAP-T24-001
**Versión:** 1.0
**Fecha:** 8 de junio de 2026
**Norma guía:** ISO/IEC 90003:2014, adopción IEEE Std 90003-2015

![Logotipo corporativo Team 24 Software](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SQAP/assets/team-24-software-logo.png)

---

### Control del documento

| Campo | Detalle |
| ----- | ------- |
| Tipo de documento | Plan de Aseguramiento de la Calidad del Software / Manual de Calidad |
| Emitido por | Dirección de Calidad — Team 24 Software |
| Elaborado por | Equipo de Gestión de Calidad |
| Organización aplicable | Team 24 Software |
| Alcance de aplicación | Todos los proyectos de software desarrollados, mantenidos o entregados por Team 24 Software |
| Uso previsto | Marco institucional de calidad y base para la presentación formal de cada proyecto |
| Estado | Versión vigente para aplicación institucional |
| Ubicación | `docs/SQAP/Manual de Calidad - SQAP.md` |

### Historial de cambios

| Versión | Fecha | Responsable | Descripción |
| ------- | ----- | ----------- | ----------- |
| 1.0 | 8 jun 2026 | Team 24 Software | Emisión inicial del manual de calidad institucional, alineado a ISO/IEC 90003 |

### Aprobación

| Rol | Responsable | Firma / constancia |
| --- | ----------- | ------------------ |
| Representante de calidad | Responsable designado por Team 24 Software | Pendiente de aprobación |
| Dirección técnica | Responsable designado por Team 24 Software | Pendiente de aprobación |
| Dirección general | Representante autorizado de Team 24 Software | Pendiente de aprobación |

---

### Propósito

El presente Manual de Calidad del Software establece el sistema institucional de aseguramiento de la calidad de Team 24 Software para la adquisición, desarrollo, verificación, validación, entrega, operación y mantenimiento de productos de software. Su propósito es definir criterios, responsabilidades, procesos, registros y controles que permitan producir software conforme a requisitos del cliente, requisitos técnicos, compromisos contractuales y estándares profesionales.

Este documento se elabora tomando como guía ISO/IEC 90003:2014, que orienta la aplicación de ISO 9001:2008 al software. No declara certificación ISO 9001 ni reemplaza requisitos contractuales específicos; establece el marco de trabajo que todo proyecto de la organización debe seguir y adaptar mediante su plan de calidad particular.

### Alcance

Este manual aplica a todos los proyectos de software ejecutados por Team 24 Software, sean internos, experimentales, comerciales, de mantenimiento, de integración o desarrollados para clientes externos. Cubre las siguientes actividades:

- Gestión del sistema de calidad y de su documentación.
- Planificación de proyectos, planificación de la calidad y definición del ciclo de vida.
- Gestión de requisitos, trazabilidad y comunicación con cliente.
- Diseño, desarrollo, integración, pruebas, liberación y mantenimiento.
- Gestión de configuración, cambios, dependencias y entregables.
- Control de no conformidades, acciones correctivas, acciones preventivas y mejora continua.
- Medición de calidad de proceso, producto, servicio y satisfacción del cliente.
- Control de propiedad del cliente, preservación del producto software y herramientas de medición aplicables.

Cada proyecto desarrollado por la empresa debe preparar una **Ficha de Aplicación del Manual de Calidad** o un **Plan de Calidad del Proyecto**, donde se indique cómo se aplican estos procesos al contexto específico del cliente, alcance, tecnología, riesgos, entregables y criterios de aceptación. Dicha ficha no reemplaza este manual; lo particulariza para un proyecto concreto.

### Exclusiones y límites

El manual no cubre fabricación de hardware, instalación física de redes, certificaciones de seguridad eléctrica, cumplimiento legal especializado ni soporte operativo 24/7, salvo que un contrato de proyecto lo incorpore expresamente.

En proyectos de software con componentes de hardware, medición física, inteligencia artificial, datos externos o servicios de terceros, el manual exige registrar las condiciones de uso, supuestos, límites y validez de los datos o instrumentos empleados, pero no certifica dispositivos externos ni sustituye normas técnicas propias del dominio del cliente.

### Referencias

#### Referencias normativas y metodológicas

| Referencia | Uso en este manual |
| ---------- | ------------------ |
| ISO/IEC 90003:2014 / IEEE Std 90003-2015 | Guía principal para aplicar ISO 9001 al software |
| ISO 9001:2008 | Base conceptual de sistema de gestión de calidad referida por ISO/IEC 90003 |
| ISO/IEC 12207 | Referencia de procesos de ciclo de vida del software citada por ISO/IEC 90003 |
| ISO/IEC 25010 | Referencia de características de calidad de producto software |
| ISO/IEC 15939 | Referencia para procesos de medición de software |
| ISO/IEC 14764 | Referencia para mantenimiento de software |
| Guía interna de proceso Scrum de Team 24 Software | Marco operativo usado para integrar Scrum con actividades de ingeniería |

#### Documentos de aplicación por proyecto

Los documentos técnicos o metodológicos de un proyecto específico, como planes de proyecto, backlogs, matrices de trazabilidad, referencias técnicas del dominio o actas de revisión, se registran en la Ficha de Aplicación del Manual de Calidad de ese proyecto. No forman parte del alcance permanente del manual institucional, aunque pueden usarse como evidencia de aplicación.

### Identidad organizacional

#### Nombre institucional

La organización adopta el nombre **Team 24 Software** como denominación corporativa oficial para este Manual de Calidad. Bajo este nombre la empresa define, ejecuta, controla y mejora su sistema de gestión de calidad aplicado al desarrollo de software.

#### Eslogan

**Software medible, verificable y alineado al cliente.**

El eslogan resume tres compromisos operativos: todo producto debe poder medirse, toda entrega debe poder verificarse y toda decisión debe responder a una necesidad validada con el cliente.

#### Misión

Desarrollar soluciones de software confiables, verificables y mantenibles, aplicando prácticas de ingeniería, aseguramiento de calidad y mejora continua para resolver necesidades reales de clientes mediante productos funcionales, documentados y técnicamente sustentados.

#### Visión

Consolidarse como una empresa de desarrollo capaz de ejecutar proyectos de software con disciplina profesional, trazabilidad completa, evidencia de calidad y entregas incrementales que puedan ser revisadas por clientes, auditores, pares técnicos y partes interesadas autorizadas.

#### Valores de calidad

| Valor | Conducta esperada |
| ----- | ----------------- |
| Enfoque al cliente | Los requisitos se levantan, revisan y aceptan con participación del cliente o su representante |
| Evidencia | Ningún avance se considera terminado sin registros verificables |
| Trazabilidad | Cada requisito debe poder vincularse con diseño, implementación, pruebas y entrega |
| Simplicidad técnica | Se eligen soluciones comprensibles, mantenibles y adecuadas al alcance |
| Mejora continua | Cada sprint o proyecto debe cerrar con lecciones y acciones de mejora |
| Responsabilidad profesional | Los hallazgos, defectos y riesgos se reportan sin ocultamiento |

### Política de calidad

Team 24 Software se compromete a desarrollar productos de software que satisfagan requisitos acordados con el cliente, cumplan criterios técnicos verificables y mantengan evidencia documental suficiente para demostrar conformidad. Para ello adopta un sistema de calidad basado en planificación, trazabilidad, revisión técnica, pruebas por niveles, control de cambios, gestión de riesgos, control de no conformidades y mejora continua.

La calidad se gestiona desde el inicio del proyecto y no como una actividad final. Cada incremento debe pasar por análisis, diseño, implementación y pruebas, con participación del Product Owner, revisión del equipo y aceptación del cliente cuando corresponda.

### Objetivos de calidad

Los objetivos de calidad se revisan al inicio de cada proyecto, durante los hitos de seguimiento y antes de cada liberación. Cuando el proyecto no defina valores propios, se aplican los siguientes mínimos institucionales:

| Objetivo | Métrica | Meta mínima | Evidencia esperada | Responsable |
| -------- | ------- | ----------- | ------------------ | ----------- |
| Conformidad de requisitos | Requisitos con criterios de aceptación definidos | 100 % antes de ingresar a ejecución | Backlog, caso de uso o especificación aprobada | Product Owner |
| Trazabilidad | Requisitos vinculados a diseño, implementación y prueba | 100 % en requisitos implementados | Matriz de trazabilidad actualizada | Representante de calidad |
| Calidad de código | Cambios revisados por un responsable distinto al autor | 100 % antes de integrar a la línea base | Registro de revisión o aprobación técnica | Equipo técnico |
| Pruebas relevantes | Pruebas definidas según riesgo ejecutadas | 100 % de pruebas obligatorias del plan de calidad | Reporte de pruebas, evidencia de CI o acta QA | QA / Equipo técnico |
| Defectos críticos | Defectos críticos abiertos al liberar | 0 | Registro de defectos filtrado por severidad | Representante de calidad |
| Documentación | Artefactos afectados actualizados | 100 % antes de cierre de sprint o hito | Documentos versionados y registro de cambios | Equipo técnico |
| Satisfacción del cliente | Entregables aceptados sin observaciones bloqueantes | ≥ 90 % del alcance comprometido, salvo cambio aprobado | Acta de aceptación o revisión del cliente | Product Owner |
| Mejora continua | Acciones de mejora registradas y seguidas | Al menos 1 acción por iteración o hito | Registro de retrospectiva o plan de mejora | Scrum Master / Facilitador |

Cuando un proyecto defina metas técnicas adicionales, estas deben registrarse en su Plan de Calidad del Proyecto con métricas, responsables, umbrales de aceptación y evidencia requerida. Las metas particulares no modifican este manual; lo complementan.

### Sistema de gestión de calidad

#### Enfoque por procesos

El sistema de calidad se organiza en procesos interrelacionados. Cada proceso tiene entradas, actividades, salidas, responsables, registros y controles.

| Proceso | Entradas | Salidas | Control principal | Registros mínimos |
| ------- | -------- | ------- | ----------------- | ----------------- |
| Gestión de requisitos | Necesidad del cliente, acuerdos, entrevistas | Backlog, requisitos, criterios de aceptación | Revisión y aprobación del Product Owner | Actas, backlog, matriz de trazabilidad |
| Planificación | Backlog priorizado, capacidad, riesgos | Plan de iteración, objetivo, plan de calidad | Revisión de capacidad, riesgos y dependencias | Plan de calidad, cronograma, matriz de riesgos |
| Diseño | Requisitos aceptados, arquitectura base | Modelos, decisiones técnicas, contratos, prototipos | Revisión técnica de diseño | Modelos UML 2.5+, ADR, especificaciones, prototipos |
| Implementación | Diseño aprobado, estándares de código | Código, configuración, migraciones o artefactos técnicos | Revisión técnica antes de integración | Registro de cambios, revisión de código, bitácora técnica |
| Verificación | Código integrado, criterios técnicos | Resultados de pruebas y hallazgos | Ejecución de pruebas según riesgo | Reportes de prueba, cobertura, evidencias CI |
| Validación | Incremento verificable, criterios de aceptación | Aceptación, rechazo u observaciones | Validación del Product Owner o cliente | Acta de revisión, checklist de aceptación |
| Liberación | Incremento validado, checklist de release | Versión entregable | Autorización formal de liberación | Registro de release, versión, evidencia de entrega |
| Medición y mejora | Métricas, defectos, retroalimentación | Acciones correctivas, preventivas y mejoras | Revisión por dirección o comité de calidad | Retrospectivas, no conformidades, auditorías |

#### Ciclo de vida de software

La organización adopta un ciclo de vida iterativo e incremental basado en Scrum. Cada sprint integra cuatro actividades obligatorias de ingeniería:

1. **Análisis:** comprensión de historias de usuario, reglas de negocio y criterios de aceptación.
2. **Diseño:** arquitectura, datos, lógica e interfaces según necesidad.
3. **Implementación:** codificación, integración, migraciones y configuración.
4. **Pruebas:** verificación por desarrollador, QA rotativo y aceptación por Product Owner.

El ciclo se adapta a proyectos futuros, siempre que mantenga evidencia de planificación, ejecución, revisión y mejora.

#### Correspondencia con ISO/IEC 90003

| Cláusula ISO/IEC 90003 | Aplicación en Team 24 Software |
| ---------------------- | -------------------------------- |
| 4. Sistema de gestión de calidad | Manual, procesos, control documental, registros y trazabilidad |
| 5. Responsabilidad de la dirección | Política, objetivos, roles, revisión gerencial y comunicación interna |
| 6. Gestión de recursos | Competencias, herramientas, infraestructura y ambiente de trabajo |
| 7. Realización del producto | Planificación, requisitos, diseño, desarrollo, compras, liberación y configuración |
| 8. Medición, análisis y mejora | Satisfacción, auditoría, métricas, no conformidades, acciones correctivas y preventivas |

#### Manual institucional y plan de calidad por proyecto

Este manual define el marco permanente de calidad de la empresa. Cada proyecto debe derivar de él un Plan de Calidad del Proyecto o una Ficha de Aplicación que especifique:

- Cliente, partes interesadas y responsable de aceptación.
- Alcance funcional y no funcional del producto.
- Ciclo de vida y calendario de entregas.
- Roles asignados y autoridad para aprobar cambios.
- Requisitos de calidad aplicables y métricas objetivo.
- Herramientas, tecnologías, dependencias y restricciones.
- Controles de verificación, validación, liberación y mantenimiento.
- Riesgos, propiedad del cliente, datos sensibles y registros requeridos.
- Criterios de cierre, entrega y soporte posterior.

La ficha de aplicación es obligatoria para presentar formalmente un proyecto bajo el sistema de calidad de Team 24 Software.

### Responsabilidad de la dirección

#### Compromiso directivo

La dirección técnica y el representante de calidad son responsables de:

- Comunicar la importancia de cumplir requisitos del cliente, requisitos normativos, compromisos contractuales y estándares profesionales.
- Mantener vigente este manual y sus registros.
- Revisar objetivos de calidad y resultados de medición.
- Asignar recursos razonables para pruebas, documentación, revisión y mejora.
- Evitar que la presión por entregar elimine controles mínimos de calidad.

#### Enfoque al cliente

El cliente o su representante participa en la definición de requisitos, revisión de incrementos y aceptación funcional. Cuando existan partes interesadas adicionales, su participación debe quedar registrada en el Plan de Calidad del Proyecto sin reemplazar la autoridad de aceptación definida con el cliente.

Los requisitos del cliente deben transformarse en historias de usuario, criterios de aceptación, reglas de negocio y casos de prueba. Cualquier ambigüedad debe resolverse antes de comprometer la historia en un sprint.

#### Roles y responsabilidades

| Rol de calidad | Responsable en la organización | Responsabilidades |
| -------------- | ------------------------------ | ----------------- |
| Dirección técnica | Product Owner + Scrum Master | Aprobar política, objetivos, cambios mayores y releases |
| Representante de calidad | Scrum Master, con rotación si el proyecto lo requiere | Mantener SQAP, controlar registros, coordinar auditorías internas |
| Product Owner | Responsable designado por proyecto | Priorizar requisitos, validar criterios de aceptación, representar al cliente |
| Scrum Master / Facilitador | Responsable designado por proyecto | Facilitar proceso, remover impedimentos, proteger controles de calidad |
| Desarrolladores | Equipo técnico del proyecto | Diseñar, implementar, probar y documentar |
| QA rotativo | Integrante distinto al autor principal del cambio | Ejecutar pruebas de calidad y buscar fallos funcionales, seguridad y rendimiento |
| Cliente / usuario representante | Organización contratante o representante designado | Validar que el producto resuelve la necesidad real |

#### Comunicación interna

La comunicación se formaliza mediante:

- Sprint Planning para análisis y compromiso.
- Daily Scrum para coordinación e impedimentos.
- Revisiones técnicas de cambios para control de calidad del código y artefactos.
- Sprint Review para validación con PO/cliente.
- Retrospective para mejora del proceso.
- Documentación versionada para decisiones, modelos y evidencias.

Las decisiones que afecten alcance, arquitectura, seguridad, datos o calidad deben registrarse en un documento del proyecto, solicitud de cambio, revisión técnica o registro de decisión arquitectónica.

#### Revisión por la dirección

Al cierre de cada sprint o fase se realiza una revisión de gestión con los siguientes insumos:

- Estado de historias, tareas y entregables.
- Resultados de pruebas y cobertura.
- No conformidades abiertas y cerradas.
- Riesgos activos y cambios de severidad.
- Retroalimentación del cliente, usuarios clave, auditoría o partes interesadas autorizadas.
- Cumplimiento de objetivos de calidad.
- Necesidades de recursos o capacitación.

La salida de la revisión debe incluir decisiones, acciones correctivas, acciones preventivas y ajustes al plan.

### Gestión de recursos

#### Competencia

Cada integrante debe mantener competencia suficiente para cumplir su rol. La competencia se evidencia mediante tareas completadas, revisiones aprobadas, pruebas ejecutadas, documentación producida y participación en ceremonias.

| Área | Competencias mínimas |
| ---- | -------------------- |
| Requisitos | Historias de usuario, criterios de aceptación, trazabilidad |
| Diseño | UML 2.5 o superior, arquitectura por capas, modelos de datos, prototipos |
| Backend | Diseño de API, servicios, persistencia, seguridad, validación de datos y pruebas de integración |
| Móvil | Desarrollo de clientes móviles, consumo de servicios, manejo de permisos, UX y pruebas en dispositivo |
| Web | Desarrollo frontend, tipado, consumo de API, accesibilidad básica, rendimiento y pruebas de interfaz |
| Calidad | Pruebas unitarias, integración, aceptación, seguridad básica, revisión de código |
| DevOps | Automatización de entornos, integración continua, entrega controlada, monitoreo básico y gestión de configuración |

#### Conciencia y capacitación

Cuando una tecnología, norma o dominio técnico sea nuevo para el equipo, se debe registrar una actividad de capacitación o investigación. La evidencia puede ser una nota técnica, prototipo, prueba de concepto, checklist o referencia bibliográfica.

#### Infraestructura

La infraestructura mínima de proyecto debe incluir:

- Repositorio de control de versiones con ramas, revisiones y versiones identificables.
- Entorno reproducible mediante contenedores, máquinas virtuales, scripts de provisión o mecanismo equivalente.
- Base de datos versionada mediante migraciones.
- Pipeline de integración continua cuando el alcance lo permita.
- Herramientas de modelado y documentación.
- Gestión de secretos fuera del repositorio.

La infraestructura específica, versiones, servicios, entornos y restricciones tecnológicas se documentan en el Plan de Calidad del Proyecto y en los documentos técnicos de arquitectura.

#### Ambiente de trabajo

El ambiente de trabajo debe favorecer concentración, revisión técnica, comunicación clara y respaldo de la información. Las decisiones críticas no deben depender de memoria personal; deben quedar registradas.

### Control de documentación y registros

#### Documentos controlados

Son documentos controlados:

- Manual de Calidad / SQAP.
- Planes de proyecto y planes de calidad por proyecto.
- Product Backlog, historias de usuario y Sprint Backlog.
- Modelos UML 2.5 o superior generados con herramientas CASE.
- Planes de prueba y reportes de validación.
- Matriz de trazabilidad, riesgos, retrospectivas y actas.
- Guías técnicas, guías de despliegue y documentación de servicios.

#### Reglas de control documental

| Regla | Aplicación |
| ----- | ---------- |
| Identificación | Cada documento debe tener título, propósito, ubicación y versión cuando corresponda |
| Versionado | Todo documento vive en un repositorio o sistema de control documental y se modifica mediante registros rastreables |
| Revisión | Cambios relevantes se revisan por al menos otro integrante o por el PO |
| Aprobación | Documentos base del proyecto se aprueban en revisión de sprint, revisión técnica o comité de calidad |
| Obsolescencia | Documentos históricos se conservan indicando que no son fuente vigente |
| Trazabilidad | Cambios en requisitos deben reflejarse en la matriz de trazabilidad correspondiente |

#### Control de registros

Los registros son evidencias de que el sistema de calidad opera. Deben ser legibles, recuperables y estar protegidos contra pérdida.

| Registro | Responsable | Retención mínima |
| -------- | ----------- | ---------------- |
| Product Backlog y Sprint Backlog | Product Owner | Vida del proyecto + periodo de retención definido |
| Actas de Review y Retrospective | Scrum Master | Vida del proyecto + periodo de retención definido |
| Resultados de pruebas | QA rotativo / Dev | Vida del proyecto |
| Revisiones técnicas de cambios | Equipo de desarrollo | Vida del repositorio |
| Reportes de defectos | QA rotativo | Vida del proyecto |
| No conformidades | Representante de calidad | Vida del proyecto + periodo de retención definido |
| Releases y changelog | Dirección técnica | Vida del producto |

### Patrón de desarrollo institucional

#### Marco metodológico

Team 24 Software adopta Scrum como marco de trabajo, integrado con actividades de ingeniería de software. El patrón institucional se resume así:

```text
Definición inicial
  → Product Backlog
  → Sprint Planning
  → Análisis de HU
  → Diseño técnico
  → Implementación
  → Pruebas por niveles
  → Sprint Review
  → Retrospective
  → Mejora del proceso
```

#### Estándares de trabajo

| Área | Estándar adoptado |
| ---- | ----------------- |
| Requisitos | Historias de usuario con 3 C: Card, Conversación, Confirmación |
| Planificación | Scrum, estimación por PHU, Sprint Backlog con tareas pequeñas |
| Modelado | UML 2.5 o superior mediante herramientas CASE |
| Arquitectura | Capas, separación de responsabilidades y contratos explícitos |
| Código | Revisión técnica, estilo consistente, nombres de dominio en español cuando aplique |
| API | Contratos de servicio documentados, validación de entrada y errores normalizados |
| Datos | Modelo relacional, migraciones versionadas y reversibles cuando sea viable |
| Pruebas | Unitarias, integración, aceptación, seguridad y rendimiento según riesgo |
| Despliegue | Entornos reproducibles, configuración externa y entrega automatizable |
| Documentación | Documentación versionada y evidencia vinculada a requisitos |

#### Definition of Done institucional

Una historia se considera terminada solo si:

- Sus criterios de aceptación están implementados.
- Existe evidencia de pruebas proporcionales al riesgo.
- El código fue revisado por otro integrante.
- La documentación afectada fue actualizada.
- La trazabilidad requisito-diseño-prueba-entrega está registrada.
- No quedan defectos críticos o bloqueantes asociados.
- El Product Owner acepta la historia o registra observaciones.

Para proyectos con restricciones especiales, la Definition of Done debe ampliarse en el Plan de Calidad del Proyecto. Las restricciones particulares deben redactarse como criterios verificables y asociarse a evidencia objetiva.

### Gestión de requisitos y comunicación con cliente

#### Determinación de requisitos

Los requisitos se levantan a partir de entrevistas, documentos, observación del proceso, necesidades del cliente, restricciones técnicas, normativas aplicables y decisiones de negocio aprobadas. Deben clasificarse como funcionales, no funcionales, técnicos, de seguridad, de operación o de documentación.

#### Revisión de requisitos

Antes de comprometer un requisito, el equipo verifica:

- Claridad de la necesidad y del usuario afectado.
- Criterios de aceptación verificables.
- Dependencias técnicas y de negocio.
- Riesgos asociados.
- Consistencia con alcance vigente.
- Factibilidad dentro del sprint o fase.
- Impacto en arquitectura, datos, seguridad y pruebas.

#### Trazabilidad

Todo requisito implementado debe poder relacionarse con:

- Requerimiento principal o necesidad del cliente.
- Historia de usuario.
- Tareas del sprint.
- Modelos o decisiones de diseño.
- Código o componente afectado.
- Pruebas ejecutadas.
- Evidencia de aceptación.

Cada proyecto define su propia matriz de trazabilidad. Como mínimo, debe permitir ubicar qué requisito originó cada entrega y qué prueba demuestra su conformidad.

#### Cambios de requisitos

Los cambios deben registrarse, evaluar impacto y aprobarse antes de implementarse. Un cambio aceptado debe actualizar backlog, trazabilidad, riesgos, estimaciones y documentación relacionada.

Los cambios urgentes se pueden atender dentro del sprint solo si no comprometen la calidad del incremento o si el Product Owner aprueba el intercambio de alcance.

| Tipo de cambio | Evaluación requerida | Aprobación mínima | Registro obligatorio |
| -------------- | -------------------- | ----------------- | -------------------- |
| Menor | No altera alcance, arquitectura, costo ni fecha comprometida | Product Owner | Backlog o registro de cambio |
| Funcional | Agrega, elimina o modifica comportamiento observable del producto | Product Owner + dirección técnica | Solicitud de cambio, impacto y criterio de aceptación |
| Técnico | Afecta arquitectura, datos, seguridad, rendimiento o infraestructura | Dirección técnica + representante de calidad | Análisis técnico, riesgos y plan de pruebas |
| Contractual | Afecta alcance formal, costo, fecha, entregable o responsabilidad del cliente | Dirección técnica + cliente | Acta, anexo contractual o aprobación escrita |
| Correctivo urgente | Atiende defecto crítico o incidente operativo | Dirección técnica | Registro de incidente, corrección y verificación posterior |

### Diseño y desarrollo

#### Planificación del diseño y desarrollo

Cada proyecto debe definir:

- Ciclo de vida aplicable.
- Responsables e interfaces entre roles.
- Actividades de análisis, diseño, codificación, integración y pruebas.
- Entregables por fase o sprint.
- Herramientas y estándares.
- Criterios de revisión, verificación, validación y liberación.

#### Entradas de diseño

Las entradas mínimas de diseño son:

- Historias de usuario y criterios de aceptación.
- Reglas de negocio.
- Requisitos no funcionales.
- Restricciones tecnológicas.
- Modelos previos aprobados.
- Riesgos activos.
- Requisitos de seguridad, datos y operación.

#### Salidas de diseño

Las salidas deben ser suficientes para implementar y verificar el producto. Pueden incluir:

- Diagrama de contexto o casos de uso.
- Diagrama de paquetes, despliegue o C4.
- Modelo conceptual, lógico y físico de datos.
- Diagramas de secuencia, actividad o estado cuando el proceso lo amerite.
- Contratos API.
- Prototipos o diseños de interfaz.
- ADR para decisiones relevantes.

#### Revisión de diseño

El diseño se revisa antes o durante la implementación según complejidad. La revisión verifica:

- Correspondencia con requisitos.
- Consistencia con arquitectura vigente.
- Viabilidad técnica.
- Impacto en seguridad y datos.
- Pruebas necesarias.
- Mantenibilidad y simplicidad.

#### Verificación

La verificación responde a la pregunta: **¿el producto fue construido correctamente según las especificaciones?** Incluye revisión de código, pruebas unitarias, pruebas de integración, análisis estático, validación de migraciones, revisión de contratos API y ejecución de pipelines.

#### Validación

La validación responde a la pregunta: **¿el producto resuelve la necesidad del usuario?** Se ejecuta mediante Sprint Review, pruebas de aceptación, demostraciones, escenarios de uso y confirmación del Product Owner o cliente.

#### Control de cambios de diseño y desarrollo

Todo cambio relevante debe:

1. Identificar motivo y alcance.
2. Evaluar impacto en requisitos, diseño, datos, pruebas y documentación.
3. Registrar aprobación.
4. Implementarse mediante un cambio trazable en el sistema de control de versiones.
5. Verificarse mediante pruebas.
6. Actualizar documentación y trazabilidad.

### Compras, componentes externos y software de terceros

Team 24 Software utiliza bibliotecas, frameworks y herramientas open source. Antes de incorporar un componente externo se evalúa:

- Licencia y compatibilidad con el proyecto.
- Mantenimiento y comunidad.
- Riesgos de seguridad conocidos.
- Compatibilidad técnica.
- Impacto en despliegue y operación.
- Alternativas disponibles.

Los componentes deben fijar versiones cuando sea necesario para reproducibilidad. Las dependencias críticas deben revisarse antes de una liberación.

### Gestión de configuración

#### Elementos de configuración

Son elementos de configuración:

- Código fuente.
- Migraciones de base de datos.
- Archivos de infraestructura.
- Documentación controlada.
- Diagramas y modelos.
- Scripts de build, test y deploy.
- Configuraciones de integración, construcción y despliegue automatizable.
- Artefactos liberados.

#### Reglas de versionado

| Elemento | Regla |
| -------- | ----- |
| Código | Control de versiones, cambios pequeños y revisión técnica |
| Releases | Tags o marcas de versión con changelog |
| Base de datos | Migraciones incrementales y documentadas |
| Configuración | Variables de entorno; secretos fuera del repositorio |
| Documentación | Commits asociados a cambios de alcance o diseño |
| Diagramas | Modelos UML y artefactos CASE versionados junto al documento |

#### Liberación

Una liberación solo procede cuando:

- El incremento compila y se ejecuta en entorno definido.
- Las pruebas mínimas pasan.
- No existen defectos críticos abiertos.
- La documentación de uso o instalación está actualizada.
- El Product Owner o responsable designado autoriza la entrega.

#### Propiedad del cliente

Se considera propiedad del cliente cualquier información, archivo, credencial, imagen, base de datos, plano, documento, marca, configuración, muestra, dataset o acceso entregado por el cliente para el desarrollo, prueba, operación o mantenimiento del producto.

El equipo debe:

- Identificar la propiedad del cliente al recibirla.
- Registrar su ubicación, responsable y finalidad de uso.
- Protegerla contra pérdida, acceso no autorizado, corrupción o divulgación.
- Notificar al cliente si se pierde, daña o detecta uso no autorizado.
- Devolverla, eliminarla o conservarla según acuerdo formal al cierre del proyecto.

#### Preservación del producto software

El producto software debe preservarse durante desarrollo, almacenamiento, entrega y mantenimiento. Esta preservación incluye:

- Repositorios con historial y control de acceso.
- Versiones etiquetadas y artefactos de release identificables.
- Backups o exportaciones de datos cuando el proyecto lo requiera.
- Integridad de paquetes, imágenes, instaladores, contenedores y scripts.
- Documentación de instalación, configuración y recuperación.
- Protección de credenciales, llaves y variables sensibles fuera del repositorio.

#### Control de herramientas de seguimiento y medición

Cuando la conformidad del producto dependa de herramientas de medición, análisis, simulación, pruebas, monitoreo o generación de reportes, el proyecto debe registrar:

- Herramienta utilizada, versión y configuración relevante.
- Métrica o resultado que produce.
- Criterio de aceptación asociado.
- Método de verificación o calibración cuando aplique.
- Limitaciones conocidas y efecto posible sobre la validez del resultado.

En software, este control aplica a suites de prueba, analizadores estáticos, herramientas de cobertura, monitores de rendimiento, herramientas de seguridad, scripts de benchmark, modelos de IA, sensores, emuladores y cualquier instrumento que produzca evidencia de conformidad.

### Pruebas y aseguramiento de calidad

#### Tres filtros de prueba

| Filtro | Responsable | Propósito |
| ------ | ----------- | --------- |
| 1er filtro: pruebas del desarrollador | Autor del cambio | Comprobar que la unidad desarrollada cumple su especificación |
| 2do filtro: QA rotativo | Integrante distinto al autor principal | Buscar fallos funcionales, de seguridad, rendimiento, usabilidad y datos |
| 3er filtro: aceptación | Product Owner / cliente | Confirmar que la historia cumple los criterios de aceptación |

#### Tipos de prueba

| Tipo | Aplicación | Evidencia mínima | Momento de ejecución |
| ---- | ---------- | ---------------- | -------------------- |
| Unitarias | Funciones, servicios, validadores y lógica de dominio | Reporte de ejecución o salida de herramienta de pruebas | Durante implementación y antes de integrar |
| Integración | Contratos entre capas, servicios, persistencia y componentes externos | Reporte de integración, logs o evidencia de entorno de prueba | Antes de validar la historia o requisito |
| Interfaz de usuario | Componentes críticos de interacción web, móvil o escritorio | Capturas, pruebas automatizadas o checklist de UI | Antes de demo o revisión con cliente |
| End-to-end | Flujos principales del usuario cuando el riesgo lo amerite | Escenario ejecutado, resultado esperado y evidencia | Antes de liberación de incremento |
| Seguridad | Autenticación, autorización, validación de entrada y exposición de datos | Checklist de seguridad, hallazgos y correcciones | Antes de liberar funciones expuestas |
| Rendimiento | Operaciones con umbrales de latencia, carga o disponibilidad | Resultado de benchmark o monitoreo definido | Antes de liberar funciones críticas |
| Regresión | Funcionalidades afectadas por cambios o defectos corregidos | Suite o checklist de regresión ejecutado | Antes de cerrar correcciones |
| Aceptación | Criterios acordados con Product Owner o cliente | Acta, checklist o aprobación documentada | Al cierre de historia, sprint o hito |

#### Criterios de severidad de defectos

| Severidad | Definición | Criterio de liberación |
| --------- | ---------- | ---------------------- |
| Crítica | Bloquea operación principal, compromete datos o seguridad | No se libera |
| Alta | Afecta una función importante sin alternativa razonable | Requiere corrección o aprobación formal de excepción |
| Media | Afecta flujo secundario o tiene solución temporal | Puede liberarse con registro y fecha de corrección |
| Baja | Defecto menor visual, texto o mejora no funcional | Puede registrarse como deuda técnica |

#### Calidad específica para IA y datos

Cuando el proyecto incorpore modelos de IA o análisis de datos, se debe registrar:

- Fuente y calidad del dataset.
- Supuestos y limitaciones del modelo.
- Métrica de evaluación.
- Validación contra baseline.
- Riesgos de sesgo, sobreajuste o uso indebido.
- Mensajes claros cuando la recomendación sea orientativa.

Si el resultado de IA se usa para apoyar una decisión del cliente, la salida debe presentarse con su alcance, limitaciones y nivel de confianza esperado. Ninguna recomendación generada por IA debe sustituir una validación profesional cuando el dominio requiera juicio experto.

### Control de producto no conforme

Un producto, incremento, documento o componente es no conforme cuando no cumple un requisito, criterio de aceptación, estándar técnico, restricción de arquitectura, política de seguridad o definición de terminado.

#### Tratamiento

Toda no conformidad debe:

1. Registrarse con identificador.
2. Clasificarse por severidad.
3. Asignar responsable.
4. Definir corrección o disposición.
5. Verificar cierre.
6. Registrar lección o acción preventiva si corresponde.

#### Disposiciones posibles

| Disposición | Uso |
| ----------- | --- |
| Corrección inmediata | Defecto corregible dentro del sprint |
| Rechazo de entrega | Incumplimiento crítico o historia no aceptable |
| Aceptación bajo concesión | Se entrega con defecto conocido aprobado por PO/cliente |
| Replanificación | Se devuelve al backlog con prioridad ajustada |
| Eliminación de alcance | Se descarta formalmente por cambio aprobado |

### Medición, análisis y mejora

#### Métricas de proceso

| Métrica | Fuente | Frecuencia | Responsable | Uso |
| ------- | ------ | ---------- | ----------- | --- |
| Avance real vs. planificado | Plan de iteración y tablero de trabajo | Cada sprint o hito | Scrum Master / Facilitador | Ajustar compromiso, capacidad y prioridades |
| Entregables aceptados / comprometidos | Acta de revisión y backlog | Cada sprint o hito | Product Owner | Evaluar confiabilidad de planificación |
| Defectos por severidad | Registro de defectos | Semanal o por hito | Representante de calidad | Identificar áreas de riesgo y priorizar correcciones |
| Tiempo de ciclo de cambios | Registro de cambios o revisiones técnicas | Cada sprint o hito | Dirección técnica | Mejorar flujo de revisión e integración |
| Acciones de mejora cerradas | Retrospectiva o plan de mejora | Cada sprint o hito | Representante de calidad | Medir eficacia de la mejora continua |

#### Métricas de producto

| Métrica | Fuente | Umbral base | Uso |
| ------- | ------ | ----------- | --- |
| Cobertura de pruebas | Reporte de herramienta de pruebas | Definido por proyecto; mínimo institucional en módulos críticos | Estimar confianza técnica |
| Densidad de defectos | Registro de defectos y tamaño del producto | Tendencia decreciente o justificación documentada | Evaluar estabilidad del producto |
| Rendimiento de operaciones críticas | Pruebas de rendimiento o monitoreo | Umbral definido en el Plan de Calidad del Proyecto | Validar experiencia de uso y capacidad técnica |
| Disponibilidad del servicio | Monitoreo o bitácora operativa | Umbral definido por contrato o proyecto | Controlar continuidad operativa |
| Vulnerabilidades abiertas | Revisión de seguridad o dependencias | Cero críticas sin tratamiento antes de liberar | Reducir riesgo de seguridad |
| Trazabilidad completa | Matriz de trazabilidad | 100 % en requisitos liberados | Evidenciar conformidad requisito-entrega |

#### Satisfacción del cliente

La satisfacción se mide mediante aceptación de historias, observaciones en Review, cambios solicitados, defectos reportados por usuario y cumplimiento del valor esperado.

#### Análisis de datos

El equipo revisa tendencias para tomar decisiones. Si una métrica se degrada durante dos sprints consecutivos, se debe definir acción correctiva o preventiva.

#### Mejora continua

La mejora continua se gestiona mediante retrospectivas, auditorías internas, análisis de defectos y actualización de estándares. Toda acción debe tener responsable, fecha objetivo y criterio de cierre.

### Auditoría interna

#### Frecuencia

Se realiza auditoría interna al menos una vez por proyecto y, en proyectos con varios sprints, al cierre de sprints significativos o antes de entregas formales al cliente.

#### Criterios de auditoría

La auditoría verifica:

- Cumplimiento de este manual.
- Evidencia de requisitos, diseño, pruebas y aceptación.
- Trazabilidad completa.
- Control de documentos y registros.
- Gestión de riesgos y no conformidades.
- Cumplimiento de restricciones del proyecto.

La auditoría debe producir un resultado documentado con hallazgos clasificados. Los hallazgos se gestionan según la siguiente escala:

| Tipo de hallazgo | Descripción | Tratamiento requerido |
| ---------------- | ----------- | --------------------- |
| Conformidad | El proceso o artefacto cumple lo establecido | Registrar evidencia |
| Observación | Existe oportunidad de mejora sin incumplimiento directo | Evaluar acción preventiva |
| No conformidad menor | Incumplimiento parcial sin impacto crítico inmediato | Definir corrección y fecha de cierre |
| No conformidad mayor | Incumplimiento que afecta calidad, seguridad, entrega o trazabilidad | Bloquear liberación o exigir concesión formal |

#### Independencia

Cuando el tamaño del equipo lo permita, el auditor no debe auditar su propio trabajo. En equipos de dos personas, el integrante que no fue autor principal del artefacto asume la revisión y deja constancia de la limitación de independencia.

### Acciones correctivas y preventivas

#### Acción correctiva

Se aplica cuando existe una no conformidad real. Debe identificar causa raíz, acción tomada, responsable, fecha y verificación de eficacia.

El flujo mínimo de una acción correctiva es:

1. Registrar la no conformidad o defecto.
2. Contener el efecto inmediato cuando exista riesgo para el cliente o la entrega.
3. Analizar causa raíz.
4. Definir acción correctiva, responsable y fecha objetivo.
5. Ejecutar la acción y registrar evidencia.
6. Verificar eficacia.
7. Cerrar o reabrir la acción si la causa persiste.

#### Acción preventiva

Se aplica ante una no conformidad potencial. Puede originarse en riesgos, tendencias de métricas, cambios técnicos, incidentes externos o lecciones aprendidas.

La acción preventiva debe ser proporcional al riesgo identificado. No se exige eliminar todo riesgo, pero sí demostrar que el equipo evaluó su probabilidad, impacto, responsable y respuesta prevista.

#### Registro mínimo

| Campo | Descripción |
| ----- | ----------- |
| ID | Identificador correlativo |
| Tipo | Correctiva o preventiva |
| Origen | Defecto, auditoría, riesgo, Review, cliente, comité de calidad |
| Descripción | Problema o riesgo observado |
| Causa raíz | Motivo principal identificado |
| Acción | Medida definida |
| Responsable | Persona asignada |
| Fecha objetivo | Compromiso de cierre |
| Evidencia | Revisión técnica, prueba, documento, acta o captura |
| Estado | Abierta, en curso, cerrada, descartada |

### Ficha de aplicación del manual por proyecto

Todo proyecto presentado por Team 24 Software debe incorporar una ficha que demuestre cómo se aplica este manual a su contexto particular. Esta ficha permite mantener el manual como documento institucional y, al mismo tiempo, documentar las decisiones específicas de cada producto.

#### Información general del proyecto

| Campo | Descripción |
| ----- | ----------- |
| Nombre del proyecto | Denominación oficial del producto o servicio |
| Cliente / solicitante | Organización o persona que solicita el proyecto |
| Responsable de aceptación | Persona o rol autorizado para aceptar entregables |
| Tipo de proyecto | Nuevo desarrollo, mantenimiento, evolución, integración, prototipo u otro |
| Alcance resumido | Objetivo y límites funcionales del producto |
| Fecha de inicio / cierre | Fechas planificadas y reales |
| Versión de la ficha | Control de versión del plan de calidad del proyecto |

#### Aplicación de procesos de calidad

| Proceso del manual | Definición en el proyecto |
| ------------------ | ------------------------- |
| Requisitos | Fuente de requisitos, formato de historias/casos, responsable de aprobación |
| Planificación | Ciclo de vida, iteraciones, hitos, capacidad y cronograma |
| Diseño | Modelos, arquitectura, decisiones técnicas y revisión requerida |
| Implementación | Repositorio, ramas, estándares de codificación y revisión |
| Verificación | Pruebas unitarias, integración, seguridad, rendimiento y evidencia |
| Validación | Criterios de aceptación, responsable de validación y acta de entrega |
| Configuración | Elementos versionados, releases, artefactos y gestión de cambios |
| Medición | Métricas de calidad, umbrales y frecuencia de revisión |
| Mejora | Retrospectivas, acciones correctivas, preventivas y lecciones aprendidas |

#### Controles específicos del proyecto

Cada ficha debe declarar controles específicos cuando existan restricciones particulares, por ejemplo:

- Requisitos regulatorios, contractuales o de negocio.
- Datos sensibles, propiedad del cliente o confidencialidad.
- Dependencias de terceros, licencias o componentes COTS.
- Tecnologías obligatorias o prohibidas.
- Restricciones de conectividad, seguridad, disponibilidad o rendimiento.
- Uso de inteligencia artificial, modelos predictivos, datasets o sensores.
- Herramientas de medición, calibración o monitoreo.
- Criterios de soporte, mantenimiento y cierre.

Estos controles se aprueban antes de iniciar la ejecución y se revisan en cada hito relevante del proyecto.

### Checklist institucional de liberación

El checklist institucional de liberación es una plantilla que debe completarse antes de entregar una versión del producto al cliente o ponerla disponible para uso operativo. La columna **Estado** no representa una evaluación previa del manual; debe llenarse para cada liberación concreta con uno de los siguientes valores: **Cumple**, **No cumple**, **No aplica** o **Pendiente**. Cuando un criterio quede como **No cumple** o **Pendiente**, la liberación debe ser bloqueada o aprobada bajo concesión formal por la dirección técnica y el cliente, según el riesgo.

| # | Criterio de liberación | Verificación requerida | Evidencia mínima esperada | Responsable | Estado |
| - | ---------------------- | ---------------------- | ------------------------- | ----------- | ------ |
| 1 | Requisitos comprometidos implementados o replanificados formalmente | Comparar alcance comprometido contra backlog, contrato o plan de calidad del proyecto | Backlog actualizado, acta de cambio o registro de replanificación | Product Owner | Pendiente |
| 2 | Criterios de aceptación ejecutados | Revisar que cada historia, requisito o caso de uso tenga validación registrada | Checklist de aceptación, acta de revisión o resultado de pruebas de aceptación | Product Owner / Cliente | Pendiente |
| 3 | Pruebas relevantes ejecutadas y aprobadas | Ejecutar pruebas unitarias, integración, regresión, seguridad o rendimiento según el riesgo del proyecto | Reporte de pruebas, salida de CI, evidencia de cobertura o reporte de QA | QA / Equipo técnico | Pendiente |
| 4 | Defectos críticos y altos controlados | Revisar incidencias abiertas y confirmar que no existan defectos críticos sin tratamiento | Registro de defectos, matriz de severidad o acta de concesión aprobada | Representante de calidad | Pendiente |
| 5 | Documentación afectada actualizada | Confirmar que manuales, guías, API, modelos y documentos de usuario reflejan la versión a liberar | Documentos versionados, enlaces a repositorio o registro de cambios | Equipo técnico | Pendiente |
| 6 | Trazabilidad actualizada | Verificar relación entre requisitos, diseño, implementación, pruebas y entrega | Matriz de trazabilidad o registro equivalente del proyecto | Representante de calidad | Pendiente |
| 7 | Riesgos y no conformidades revisados | Revisar riesgos abiertos, acciones correctivas, acciones preventivas y no conformidades pendientes | Matriz de riesgos, registro de no conformidades y plan de acción | Dirección técnica | Pendiente |
| 8 | Build, paquete o despliegue reproducible verificado | Confirmar que la versión puede construirse, instalarse, desplegarse o recuperarse en el entorno definido | Tag de versión, artefacto de release, pipeline exitoso o acta de despliegue | DevOps / Equipo técnico | Pendiente |
| 9 | Propiedad del cliente y datos sensibles controlados | Confirmar protección, devolución, eliminación o conservación autorizada de datos y activos del cliente | Registro de activos, respaldo, acta de devolución o evidencia de eliminación | Representante de calidad | Pendiente |
| 10 | Autorización formal de liberación registrada | Obtener aprobación de la autoridad definida en el Plan de Calidad del Proyecto | Acta de liberación, correo de aprobación, firma o registro de release | Dirección técnica / Cliente | Pendiente |

### Formato de registro de no conformidad

```text
ID:
Fecha:
Proyecto:
Detectado por:
Origen:
Severidad:
Descripción:
Requisito / estándar afectado:
Causa raíz:
Acción inmediata:
Acción correctiva:
Responsable:
Fecha objetivo:
Evidencia de verificación:
Estado:
```

### Formato de revisión de sprint

```text
Sprint:
Fecha:
Historias comprometidas:
Historias aceptadas:
Historias rechazadas o replanificadas:
Defectos críticos:
Evidencia de pruebas:
Observaciones del PO / cliente:
Cambios al Product Backlog:
Acciones correctivas:
Acciones preventivas:
Decisión de release:
```

### Bibliografía

- Institute of Electrical and Electronics Engineers. (2015). *IEEE Std 90003-2015: IEEE Standard Adoption of ISO/IEC 90003:2014, Software Engineering — Guidelines for the Application of ISO 9001:2008 to Computer Software*. IEEE.
- International Organization for Standardization. (2014). *ISO/IEC 90003:2014: Software engineering — Guidelines for the application of ISO 9001:2008 to computer software*. ISO/IEC.
- International Organization for Standardization. (2008). *ISO 9001:2008: Quality management systems — Requirements*. ISO.
- International Organization for Standardization. (2006). *ISO/IEC 14764:2006: Software Engineering — Software Life Cycle Processes — Maintenance*. ISO/IEC.
- International Organization for Standardization. (2007). *ISO/IEC 15939:2007: Systems and Software Engineering — Measurement Process*. ISO/IEC.

---

### Anexo A. Matriz rápida ISO/IEC 90003 vs. evidencias institucionales

| ISO/IEC 90003 | Evidencia institucional esperada | Sección del manual |
| ------------- | -------------------------------- | ------------------ |
| 4.1 Sistema de gestión de calidad | Procesos identificados, secuencia, controles, medición y mejora | 8 |
| 4.2 Manual de calidad | Alcance, exclusiones, procesos y control documental | 1, 2, 3, 11 |
| 4.2 Control de documentos | Reglas de identificación, versión, revisión y obsolescencia | 11.2 |
| 4.2 Control de registros | Registros definidos, responsables y retención mínima | 11.3 |
| 5.1 Compromiso de dirección | Responsabilidad directiva y protección de controles de calidad | 9.1 |
| 5.2 Enfoque al cliente | Participación del cliente y validación de requisitos | 9.2, 13 |
| 5.3 Política de calidad | Política formal de la empresa | 6 |
| 5.4 Objetivos de calidad | Objetivos y métricas mínimas de calidad | 7 |
| 5.5 Responsabilidad y comunicación | Roles, autoridad y comunicación interna | 9.3, 9.4 |
| 5.6 Revisión por dirección | Insumos y salidas de revisión | 9.5 |
| 6 Gestión de recursos | Competencia, capacitación, infraestructura y ambiente | 10 |
| 7.1 Planificación del producto | Plan de calidad por proyecto y criterios de aceptación | 8.4, 22 |
| 7.2 Procesos relacionados con cliente | Determinación, revisión y comunicación de requisitos | 13 |
| 7.3 Diseño y desarrollo | Entradas, salidas, revisión, verificación, validación y cambios | 14 |
| 7.4 Compras | Evaluación de componentes externos y software de terceros | 15 |
| 7.5 Producción y servicio | Configuración, liberación, propiedad del cliente y preservación | 16 |
| 7.6 Seguimiento y medición | Control de herramientas de medición y evidencia | 16.6 |
| 8.2 Seguimiento y medición | Pruebas, auditoría, satisfacción y métricas | 17, 19, 20 |
| 8.3 Producto no conforme | Identificación, tratamiento y disposición | 18 |
| 8.4 Análisis de datos | Métricas, tendencias y decisiones de mejora | 19 |
| 8.5 Mejora | Acciones correctivas, preventivas y mejora continua | 19.5, 21 |


# 4. Herramientas CASE


### Concepto

CASE significa Computer Aided Software Engineering, es decir, ingenieria de software asistida por computador. En este proyecto la herramienta CASE no se utiliza solamente para dibujar, sino para organizar modelos, navegar entre artefactos, mantener consistencia semantica y respaldar decisiones de diseno.

### Herramientas adoptadas

| Herramienta | Uso |
| ----------- | --- |
| StarUML | Organizacion de modelos UML 2.5+, paquetes, clases, casos de uso y diagramas dinamicos. |
| PlantUML | Representacion textual versionable de diagramas UML. |
| Visual Studio Code | Edicion, vista previa, trazabilidad con repositorio y revision Markdown. |
| GitHub | Versionado, control de cambios, revision y publicacion de evidencia. |

### Navegabilidad esperada

La demostracion CASE debe permitir recorrer la arquitectura desde niveles generales hacia detalles tecnicos:

1. Diagrama de paquetes del sistema.
2. Paquete de aplicacion movil, backend o web.
3. Casos de uso asociados al paquete.
4. Diagrama de secuencia del caso de uso.
5. Clases, servicios o repositorios que participan en la secuencia.
6. Entidades de datos persistidas.
7. Pruebas vinculadas al comportamiento esperado.

El recorrido replica la navegabilidad solicitada en clase: desde un diagrama de paquetes se ingresa al caso de uso, luego al diagrama de comunicacion o secuencia, despues a las clases participantes, y los mensajes observados en la interaccion se verifican como metodos u operaciones de esas clases.

La figura UML de navegabilidad CASE representa este recorrido y demuestra la relacion entre modelos, clases, datos y pruebas.

### Evidencia de uso real

| Evidencia | Descripcion |
| --------- | ----------- |
| Modelo de contexto | Actores, casos de uso y frontera del sistema. |
| Modelo de arquitectura | Paquetes y despliegue con componentes reales. |
| Modelo de datos | Clases conceptuales y relaciones de persistencia. |
| Modelo de logica | Secuencias de captura, heatmap y portal cliente. |
| Trazabilidad | Relacion entre requerimientos, casos de uso, entidades y pruebas. |
| Exportacion | Diagramas renderizados a imagen para documento Word. |

### Beneficio para productividad

El enfoque CASE reduce retrabajo porque los diagramas se versionan como texto, se revisan junto con el codigo y pueden regenerarse automaticamente. Tambien facilita explicar el sistema al docente, al Product Owner y al equipo tecnico, manteniendo una relacion clara entre lo solicitado, lo disenado, lo implementado y lo probado.

### Criterios de aceptacion de la demostracion

- Se visualizan al menos los cuatro modelos obligatorios.
- Se demuestra navegabilidad entre caso de uso, secuencia, clase y dato.
- Los diagramas usan notacion UML 2.5+.
- El modelo no contradice la modalidad 100 % en linea.
- Las entidades y componentes corresponden al producto implementado.


## Evidencia de navegabilidad CASE


### case navegabilidad

![case navegabilidad](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/08-case-navegabilidad.png)



# 5. Aspectos Legales para Apertura de Empresa de Software


### Enfoque

Team 24 Software se plantea como una empresa de desarrollo de software que opera en Bolivia y presta servicios tecnologicos a clientes empresariales. Para fines academicos no se ejecuta la apertura real de la empresa, pero se documentan los pasos que deberian cumplirse para constituirla y operar formalmente.

### Tipo de organizacion recomendado

Para una empresa con dos o mas socios se recomienda una Sociedad de Responsabilidad Limitada (S.R.L.), porque separa el patrimonio de la empresa del patrimonio personal de los socios y permite formalizar participaciones. Para un emprendimiento individual podria utilizarse empresa unipersonal, aunque con menor separacion patrimonial.

### Registro de comercio

El registro de comercio en Bolivia es administrado por el Servicio Plurinacional de Registro de Comercio (SEPREC). Aunque en clases se mencione FUNDEMPRESA como referencia historica, la entidad vigente para los tramites de registro comercial es SEPREC.

Pasos generales:

1. Definir razon social, tipo societario, actividad economica y domicilio.
2. Elaborar escritura de constitucion, estatutos y poderes cuando corresponda.
3. Ingresar al portal de tramites de SEPREC.
4. Llenar el formulario virtual de inscripcion.
5. Realizar el pago correspondiente.
6. Atender observaciones si existieran.
7. Obtener la matricula de comercio con codigo de validacion.

Para empresa unipersonal, SEPREC informa que el tramite utiliza formulario virtual, pago en plataforma, analisis legal y emision de Matricula de Comercio, con costo referencial de Bs 130 y plazo de 24 horas desde el siguiente dia habil al pago, sujeto a validacion de la entidad.

### NIT y obligaciones tributarias

El Numero de Identificacion Tributaria identifica a la empresa ante el Servicio de Impuestos Nacionales. Para sociedades registradas en SEPREC, el NIT coincide con la matricula de comercio y la razon social debe coincidir entre SEPREC y SIN.

Obligaciones tributarias principales:

| Concepto | Aplicacion |
| -------- | ---------- |
| IVA | Impuesto al Valor Agregado por operaciones facturadas. |
| IT | Impuesto a las Transacciones. |
| IUE | Impuesto a las Utilidades de las Empresas. |
| Facturacion | Emision de factura segun regimen aplicable. |
| Registros contables | Libros, balances y declaraciones segun normativa tributaria. |

La empresa debe contar con apoyo contable para clasificar actividades, registrar obligaciones periodicas y evitar contingencias por facturacion o impuestos.

### Patente municipal

La actividad economica requiere registro o empadronamiento municipal segun jurisdiccion. En Santa Cruz de la Sierra existen tramites para empadronamiento de patente municipal a la actividad economica para contribuyente natural y juridico. La empresa debe verificar requisitos vigentes del Gobierno Autonomo Municipal correspondiente, domicilio legal, actividad declarada y condiciones de funcionamiento.

### Derechos de autor del software

El software puede registrarse ante el Servicio Nacional de Propiedad Intelectual (SENAPI), en la Direccion de Derecho de Autor y Derechos Conexos. SENAPI reconoce programas de computacion como obras registrables y solicita, entre otros requisitos, carta o memorial, cedulas de identidad, formulario, comprobantes de pago y soporte material del programa. Para aplicaciones web se puede adjuntar video demostrativo y descripcion del programa.

El registro es declarativo y fortalece la seguridad juridica sobre autoria y titularidad, aunque la obra nace protegida desde su creacion.

### Contratos y documentos legales operativos

Team 24 Software debe preparar:

- Contrato de prestacion de servicios o licencia SaaS.
- Acuerdo de niveles de servicio si existe compromiso operativo.
- Terminos y condiciones de uso.
- Politica de privacidad.
- Acuerdos de confidencialidad con clientes.
- Contratos laborales o de prestacion de servicios para colaboradores.
- Politica de propiedad intelectual sobre codigo, documentacion y modelos.

### Equipo administrativo requerido

Una empresa de software no se sostiene solo con desarrolladores. Debe contar con apoyo financiero, contable, tributario y legal para manejar facturacion, impuestos, contratos, propiedad intelectual, costos cloud, licencias y obligaciones laborales.

### Fuentes institucionales consultadas

- Servicio Plurinacional de Registro de Comercio (SEPREC): registro de comercio y tramites empresariales.
- Servicio de Impuestos Nacionales (SIN): NIT y requisitos tributarios.
- Servicio Nacional de Propiedad Intelectual (SENAPI): derecho de autor y registro de programas de computacion.
- Gobierno Autonomo Municipal de Santa Cruz de la Sierra: patente municipal para actividad economica.



# 6. Infraestructura para la Producción de Software


### Vision general

La infraestructura de Team 24 Software integra herramientas de gestion, desarrollo colaborativo, control de versiones, automatizacion, contenedores, despliegue, seguridad e inteligencia artificial aplicada al ciclo de desarrollo. El objetivo es producir software repetible, verificable y desplegable.

### Gestion del proyecto

El proyecto se gestiona con Scrum. El Product Backlog organiza historias de usuario; el Sprint Backlog descompone tareas; la Sprint Review valida incrementos; y la Retrospective captura mejoras. El tablero debe reflejar el estado real del sprint sin depender de avisos del docente.

Las herramientas aceptables para demostrar la gestion incluyen Jira, Trello, GitHub Projects o Chotrack. Para esta entrega se documenta el flujo Scrum y se conserva evidencia versionada del backlog, sprint, tareas y trazabilidad.

### Desarrollo colaborativo

| Area | Herramienta o practica |
| ---- | ---------------------- |
| Repositorio | GitHub. |
| Versionado | Git con ramas por funcionalidad y rama principal protegida. |
| Revision | Pull requests o revision cruzada antes de integrar. |
| Convenciones | Commits descriptivos, trazabilidad con HU y criterios de aceptacion. |
| Documentacion | Markdown, PlantUML y documentos consolidados. |

### Control de configuracion

Los elementos bajo control incluyen:

- Codigo fuente backend, web y movil.
- Migraciones de base de datos.
- Configuracion Docker.
- Nginx y reglas de reverse proxy.
- Variables de entorno documentadas.
- Diagramas y documentos versionados.
- Releases moviles y artefactos de despliegue.

### Automatizacion CI/CD

El pipeline de integracion continua debe ejecutar:

- Pruebas backend con pytest.
- Analisis estatico backend con ruff.
- Lint y build del frontend.
- Analisis y pruebas de Flutter.
- Construccion de imagenes Docker.
- Publicacion controlada de artefactos.
- Despliegue a servidor productivo cuando el cambio sea aprobado.

### Contenedores y despliegue

El despliegue productivo se organiza con Docker Compose:

- `nginx`: terminacion TLS y reverse proxy.
- `backend`: API FastAPI y modulo IA.
- `web`: bundle React estatico.
- `db`: PostgreSQL con volumen persistente.

Nginx publica la API bajo `/api`, el panel web, el portal de cliente y los recursos estaticos. El backend no expone directamente la base de datos al exterior.

Kubernetes se considera una alternativa de orquestacion para una etapa posterior con multiples microservicios, escalamiento horizontal o alta disponibilidad. No se adopta como tecnologia principal de esta entrega porque el alcance operativo inicial se cubre con Docker Compose, Nginx y una unica base PostgreSQL centralizada.

### Seguridad operativa

| Control | Aplicacion |
| ------- | ---------- |
| TLS | Trafico cifrado entre clientes y servidor. |
| JWT | Autenticacion de usuarios. |
| Roles | Administrador, tecnico y acceso publico controlado por token. |
| Ownership | Validacion de propiedad de proyectos y recursos. |
| Secretos | Variables de entorno y secretos de CI/CD. |
| Backups | Copias periodicas de PostgreSQL y archivos subidos. |
| Auditoria | Registro de accesos relevantes y releases. |

### Inteligencia artificial integrada al desarrollo

El equipo puede utilizar asistentes de IA en IDE para acelerar tareas de analisis, generacion de pruebas, refactorizacion, documentacion y revision. Su uso debe ser responsable: todo resultado generado por IA se revisa, prueba y adapta al criterio del equipo. La IA no reemplaza la validacion tecnica ni la responsabilidad profesional.

Ejemplos de herramientas aplicables son GitHub Copilot, Gemini, Codex u otros asistentes integrados al IDE. Su evidencia debe mostrarse como apoyo al desarrollo y a la especificacion, no como sustituto de pruebas, revisiones o aceptacion del Product Owner.

### Ambientes

| Ambiente | Uso | Reglas |
| -------- | --- | ------ |
| Local | Desarrollo individual | Datos de prueba y secretos locales. |
| Integracion | Validacion de ramas | Tests automatizados y base efimera. |
| Produccion | Acceso real del producto | TLS, backups, monitoreo y cambios aprobados. |


# 7. Sitio Web de la Empresa


### Proposito

El sitio web publico representa a **Team 24 Software** como empresa de desarrollo de software y servicios tecnologicos. Su funcion no se limita a promocionar Wireless HeatMapper: tambien comunica la identidad institucional, el catalogo de servicios, los canales de soporte, las descargas disponibles, las politicas publicas y el acceso a informacion confiable para clientes, docentes, usuarios tecnicos y visitantes externos.

El sitio se considera parte de la presencia digital de la empresa y debe mantenerse publicado en linea, disponible por HTTPS y alineado con la documentacion oficial del proyecto.

### URL publica

La publicacion en linea del producto y sitio institucional se encuentra en:

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/>

Para presentaciones academicas, entregas documentales y demostraciones, esta URL puede acompanarse con codigo QR en anexos o material promocional. La URL no debe depender de `localhost`, tuneles temporales ni servidores personales apagables durante la evaluacion.

La pagina oficial de la empresa en Facebook se encuentra en:

<https://www.facebook.com/profile.php?id=61591962512748>

Este enlace se incorpora como canal publico de difusion y debe acompanarse con codigo QR en anexos o material promocional. No se publican enlaces a otras redes sociales porque no forman parte de los canales oficiales vigentes.

### Objetivos del sitio

| Objetivo | Descripcion |
| -------- | ----------- |
| Presencia institucional | Presentar a Team 24 Software como proveedor responsable de soluciones de software. |
| Difusion comercial | Mostrar servicios ofrecidos, producto principal y beneficios para clientes potenciales. |
| Acceso al producto | Dirigir al usuario hacia Wireless HeatMapper, portal web, manuales y descargas moviles. |
| Soporte operativo | Centralizar preguntas frecuentes, canales de ayuda y reporte de incidentes. |
| Confianza y transparencia | Publicar politicas basicas de privacidad, terminos de uso, mantenimiento y contacto. |
| Atencion asistida | Incorporar un chatbot entrenado con informacion de empresa, producto y soporte. |

### Publico objetivo

| Publico | Necesidad principal dentro del sitio |
| ------- | ------------------------------------ |
| Clientes empresariales | Entender que problema resuelve Wireless HeatMapper y como solicitar una demostracion. |
| Tecnicos de redes | Conocer el flujo de trabajo, descargas moviles, manuales y soporte tecnico. |
| Administradores de organizaciones | Revisar beneficios, seguridad, gestion de usuarios y portal de cliente. |
| Docentes y evaluadores | Ver evidencia de publicacion, alcance del producto y documentacion asociada. |
| Visitantes generales | Identificar a la empresa, servicios ofrecidos y formas de contacto. |

### Mapa de secciones publicas

| Seccion | Contenido esperado | Resultado para el visitante |
| ------- | ------------------ | --------------------------- |
| Inicio | Mensaje principal de Team 24 Software, acceso a Wireless HeatMapper, llamada a demo y accesos rapidos. | Comprende en segundos que ofrece la empresa y donde ingresar. |
| Empresa | Quienes somos, mision, vision, valores, equipo Grupo 24 y enfoque de trabajo. | Reconoce la identidad institucional y responsabilidad del proveedor. |
| Servicios | Desarrollo web, aplicaciones moviles, backend/API, consultoria WiFi, analitica, IA aplicada y mantenimiento. | Identifica servicios contratables mas alla del producto principal. |
| Producto | Presentacion de Wireless HeatMapper, problema, usuarios, arquitectura general, beneficios y flujo de uso. | Entiende el valor del producto y su modalidad 100 % en linea. |
| Descargas | APK Android, manual de usuario, documentacion publica, notas de version y enlaces autorizados. | Obtiene recursos oficiales sin recurrir a archivos sueltos o enlaces informales. |
| Soporte | Preguntas frecuentes, guia para reportar incidentes, horarios de atencion, severidades y tiempos de respuesta. | Sabe como pedir ayuda y que informacion debe enviar. |
| Contacto | Formulario web, correo institucional del proyecto, telefono/WhatsApp autorizado y ubicacion referencial en Santa Cruz de la Sierra. | Puede solicitar informacion, soporte o una demostracion. |
| Chatbot | Asistente conversacional entrenado con informacion aprobada de empresa, producto, soporte y WiFi basico. | Recibe respuestas inmediatas y consistentes antes de escalar a soporte humano. |
| Politicas | Privacidad, terminos de uso, licenciamiento, cookies si aplican y mantenimiento de contenido. | Conoce reglas de uso, tratamiento de datos y alcance del servicio. |

### Seccion Empresa

La seccion de empresa debe diferenciar claramente a **Team 24 Software** del cliente del caso **Bulldog Tech.**. Team 24 Software es la empresa desarrolladora del producto; Bulldog Tech. es el cliente real utilizado para contextualizar el problema de cobertura WiFi.

Contenido minimo:

- Nombre institucional: Team 24 Software.
- Equipo: Grupo 24 de Ingenieria de Software II.
- Ubicacion referencial: Santa Cruz de la Sierra, Bolivia.
- Mision: desarrollar soluciones digitales verificables, mantenibles y orientadas a necesidades reales de clientes.
- Vision: consolidarse como equipo proveedor de software tecnico para redes, analitica y procesos empresariales.
- Valores: calidad, trazabilidad, responsabilidad, seguridad, aprendizaje continuo y comunicacion clara.
- Perfil del equipo: desarrollo web, movil, backend, documentacion, pruebas y despliegue.

### Seccion Servicios

La seccion de servicios presenta capacidades de Team 24 Software de forma comercial y verificable. No debe prometer servicios que no puedan explicarse o demostrarse.

| Servicio | Alcance |
| -------- | ------- |
| Desarrollo de software web | Sistemas administrativos, portales de cliente, dashboards y aplicaciones SPA. |
| Desarrollo movil | Aplicaciones Android con cliente delgado, consumo REST y experiencia orientada a campo. |
| Backend y APIs | APIs REST, autenticacion JWT, persistencia centralizada y documentacion OpenAPI. |
| Consultoria WiFi | Herramientas para relevamiento, interpretacion de RSSI, mapas de calor y evidencia tecnica. |
| Analitica e IA aplicada | Procesamiento de datos, recomendaciones asistidas y automatizacion de decisiones tecnicas. |
| DevOps basico | Contenedores, despliegue con Docker Compose, Nginx, HTTPS y CI/CD. |
| Mantenimiento y soporte | Correcciones, actualizaciones, respaldos, monitoreo y atencion de incidentes. |

Cada servicio debe incluir una descripcion breve, beneficios, ejemplos de entregables y un llamado a contacto.

### Seccion Producto: Wireless HeatMapper

Wireless HeatMapper es el producto destacado del sitio. Debe presentarse como una solucion integrada para relevar, procesar y publicar resultados de cobertura WiFi en interiores mediante mapas de calor.

Contenido minimo:

- Problema que resuelve: mediciones WiFi fragmentadas, uso de planos impresos, transcripcion manual y baja trazabilidad.
- Usuarios principales: administrador, tecnico de campo y cliente final.
- Componentes: app movil Android, backend FastAPI, PostgreSQL, panel web, portal de cliente e IA backend.
- Modalidad: 100 % en linea, sin persistencia local de dominio ni sincronizacion diferida.
- Beneficios: evidencia centralizada, mapas de calor, comparacion de escenarios, portal por enlace y supervision organizacional.
- Criterios tecnicos visibles: objetivo de diseno RSSI >= -70 dBm y zona muerta RSSI < -90 dBm.

La seccion debe incluir enlaces hacia login, portal, manual de usuario, API/documentacion tecnica cuando corresponda y canal de soporte.

### Seccion Descargas

La seccion de descargas debe publicar solamente recursos oficiales, versionados y revisados.

| Recurso | Contenido | Regla de publicacion |
| ------- | --------- | -------------------- |
| APK Android | Instalador de la app movil para tecnicos. | Publicar solo builds generados desde release o entrega aprobada. |
| Manual de usuario | Guia de uso para administrador, tecnico y cliente. | Mantener sincronizado con el incremento desplegado. |
| Notas de version | Cambios principales, correcciones y advertencias. | Una entrada por version liberada. |
| Documentacion publica | Enlaces a documentos aprobados para consulta externa. | No exponer secretos, credenciales ni datos privados. |
| Politicas | Terminos, privacidad, soporte y mantenimiento. | Revisar ante cada cambio de operacion o tratamiento de datos. |

Los enlaces rotos, archivos duplicados o versiones obsoletas deben retirarse o marcarse claramente como historicas.

### Seccion Soporte

La seccion de soporte debe orientar al usuario antes de escalar a contacto humano. Debe contener:

- Preguntas frecuentes sobre acceso, roles, carga de planos, mediciones, heatmaps y portal cliente.
- Guia para reportar incidentes.
- Horario de atencion definido para el contexto academico o productivo.
- Clasificacion de severidad.
- Datos minimos que debe enviar el usuario.
- Flujo de escalamiento desde chatbot hacia soporte humano.

#### Clasificacion de incidentes

| Severidad | Ejemplo | Tiempo objetivo de primera respuesta |
| --------- | ------- | ------------------------------------ |
| Alta | Sistema publicado inaccesible, login general caido, perdida de acceso al portal. | 4 horas habiles. |
| Media | Error en carga de planos, falla en generacion de heatmap o descarga no disponible. | 1 dia habil. |
| Baja | Consulta funcional, ajuste de texto, duda de uso o solicitud de mejora. | 2 dias habiles. |

#### Datos requeridos para soporte

- Nombre y rol del usuario.
- Organizacion o cliente relacionado.
- URL o pantalla donde ocurre el problema.
- Pasos para reproducir el incidente.
- Fecha y hora aproximada.
- Captura de pantalla si corresponde.
- Version de APK o navegador utilizado.

### Seccion Contacto

La seccion de contacto debe ofrecer canales claros y evitar informacion ambigua.

| Canal | Uso recomendado |
| ----- | --------------- |
| Formulario web | Solicitudes comerciales, demostraciones, soporte general y mensajes academicos. |
| Correo institucional | Comunicacion formal, seguimiento de incidentes y entrega de evidencias. |
| WhatsApp autorizado | Coordinacion rapida de demostraciones o soporte de baja complejidad. |
| Facebook oficial | Difusion institucional, marketing y anuncios publicos mediante la pagina <https://www.facebook.com/profile.php?id=61591962512748>. |
| Ubicacion referencial | Identificar la ciudad base de operacion sin publicar domicilios privados. |

El formulario debe pedir solo datos necesarios: nombre, correo, organizacion, motivo, mensaje y consentimiento para tratamiento de datos. No debe solicitar contrasenas, tokens, credenciales ni informacion sensible de redes internas.

### Chatbot entrenado

El sitio debe incluir un chatbot propio o integrado que responda con informacion especifica de Team 24 Software y Wireless HeatMapper. No debe limitarse a redirigir a WhatsApp ni responder con texto generico sin contexto.

#### Objetivo del chatbot

Atender consultas frecuentes, reducir carga de soporte inicial y guiar al visitante hacia la seccion correcta del sitio. Cuando la consulta supere su alcance, debe escalar al formulario de contacto o al canal de soporte humano.

#### Base de conocimiento

| Tema | Contenido entrenado o documentado |
| ---- | --------------------------------- |
| Empresa | Identidad de Team 24 Software, equipo, servicios, ubicacion referencial y contacto. |
| Producto | Componentes de Wireless HeatMapper, roles, modalidad online, beneficios y limites. |
| Uso | Inicio de sesion, creacion de proyectos, carga de planos, mediciones, heatmaps y portal cliente. |
| Soporte | Como reportar incidentes, severidades, datos requeridos y tiempos de respuesta. |
| WiFi basico | RSSI, mapas de calor, objetivo >= -70 dBm, zona muerta < -90 dBm e interpretacion general. |
| Privacidad | Datos tratados, finalidad, roles de acceso y recomendaciones de seguridad. |
| Descargas | Donde obtener APK, manuales, notas de version y documentacion autorizada. |

#### Preguntas que debe responder

- Que es Team 24 Software?
- Que problema resuelve Wireless HeatMapper?
- Como ingreso al sistema publicado?
- Cual es la diferencia entre administrador, tecnico y cliente?
- Como se reporta un problema?
- Donde descargo la app movil?
- Que significa RSSI >= -70 dBm?
- Que significa RSSI < -90 dBm?
- Como se comparte un proyecto con un cliente?
- Que datos trata el sistema?

#### Limites y seguridad del chatbot

El chatbot debe aplicar las siguientes reglas:

- No inventar precios, contratos, credenciales ni compromisos comerciales no aprobados.
- No solicitar contrasenas, tokens, claves WiFi reales ni secretos de infraestructura.
- No entregar datos privados de clientes, usuarios, planos o proyectos.
- No reemplazar soporte humano en incidentes criticos.
- Indicar cuando una respuesta requiere validacion del equipo.
- Usar lenguaje claro, breve y profesional.
- Basar respuestas en documentacion aprobada, no en suposiciones.

#### Mantenimiento del entrenamiento

La base del chatbot se actualiza cuando cambian:

- servicios publicados;
- politicas de privacidad o terminos de uso;
- URL productiva;
- flujo de autenticacion;
- version de APK;
- manual de usuario;
- roles o permisos;
- procedimientos de soporte;
- criterios tecnicos visibles para usuarios.

Cada actualizacion debe registrar fecha, responsable, fuente documental usada y alcance del cambio.

### Politicas publicas del sitio

El sitio debe enlazar politicas basicas en lenguaje comprensible:

| Politica | Contenido minimo |
| -------- | ---------------- |
| Privacidad | Datos recolectados, finalidad, responsables, conservacion, seguridad y contacto. |
| Terminos de uso | Reglas de acceso, uso permitido, restricciones, disponibilidad y responsabilidades. |
| Licenciamiento | Titularidad del software, uso de terceros y condiciones de distribucion del APK. |
| Cookies o analitica | Herramientas usadas, finalidad y opciones del usuario, si corresponde. |
| Soporte | Canales, horarios, severidades, tiempos de respuesta y alcance del servicio. |
| Mantenimiento de contenido | Responsables, frecuencia, versionado y criterios para retirar informacion obsoleta. |

Estas politicas deben estar visibles desde el pie de pagina y desde la seccion de soporte o contacto.

### Politicas de mantenimiento del contenido

El contenido del sitio debe tratarse como informacion oficial de la empresa. Cualquier cambio debe ser revisado antes de publicarse, especialmente si afecta producto, soporte, politicas o descargas.

#### Responsabilidades

| Rol | Responsabilidad |
| --- | --------------- |
| Product Owner | Aprueba contenido de producto, beneficios, alcance y mensajes orientados al cliente. |
| Scrum Master | Coordina revision, evidencia de publicacion y cumplimiento de fechas. |
| Responsable tecnico | Valida URLs, descargas, version de APK, estado del despliegue y enlaces a documentacion. |
| Responsable de calidad | Revisa claridad, consistencia, ortografia, trazabilidad y ausencia de datos sensibles. |

#### Frecuencia de revision

| Frecuencia | Actividad |
| ---------- | --------- |
| En cada release | Validar enlaces, descargas, notas de version, manuales y capturas visibles. |
| Mensual | Revisar textos institucionales, servicios, contacto, preguntas frecuentes y chatbot. |
| Antes de una demo | Confirmar disponibilidad HTTPS, login, portal, QR, descargas y formulario de contacto. |
| Ante incidente critico | Publicar aviso, actualizar soporte y retirar informacion temporal incorrecta si aplica. |
| Ante cambio legal o de datos | Revisar privacidad, terminos de uso y consentimiento del formulario. |

#### Flujo de cambio de contenido

1. Identificar necesidad de cambio.
2. Registrar fuente del cambio: release, incidente, feedback de usuario, decision del PO o ajuste legal.
3. Editar contenido en rama o cambio controlado.
4. Revisar ortografia, enlaces, consistencia y datos sensibles.
5. Validar despliegue en ambiente publicado.
6. Registrar fecha, responsable y descripcion breve del cambio.

#### Criterios de retiro de contenido

Se debe retirar, corregir o marcar como historico cualquier contenido que:

- apunte a descargas no vigentes;
- mencione funcionalidades no disponibles;
- contradiga la modalidad 100 % en linea;
- exponga datos internos, credenciales o informacion de clientes;
- tenga enlaces rotos;
- use capturas desactualizadas;
- prometa tiempos, precios o garantias no aprobadas;
- confunda a Team 24 Software con Bulldog Tech.

### Criterios de aceptacion del sitio publicado

| Criterio | Verificacion |
| -------- | ------------ |
| Acceso publico | La URL abre por HTTPS desde navegador externo. |
| Identidad clara | Se distingue Team 24 Software, Wireless HeatMapper y Bulldog Tech. |
| Secciones completas | Empresa, servicios, producto, descargas, soporte, contacto, chatbot y politicas estan visibles. |
| Enlaces funcionales | Login, manuales, descargas, politicas y contacto no devuelven error. |
| Chatbot entrenado | Responde preguntas especificas de empresa, producto, soporte y WiFi basico. |
| Seguridad de informacion | No se publican secretos, credenciales, datos privados ni enlaces internos sensibles. |
| Contenido vigente | Textos, descargas y manuales coinciden con la version desplegada. |
| Mantenimiento definido | Existe responsable, frecuencia y flujo de actualizacion documentado. |

### Evidencias recomendadas

Para demostrar que el sitio esta publicado y mantenido, se recomienda conservar:

- captura de la pagina principal con URL visible;
- captura de cada seccion publica;
- captura de una conversacion valida con el chatbot;
- captura de la seccion de descargas;
- captura de politicas enlazadas;
- registro de verificacion de enlaces;
- QR de acceso usado en presentaciones;
- commit o version donde se actualizo el contenido.

### Relacion con otros documentos

Este documento se complementa con:

- `01-resumen-ejecutivo.md`, para la vision general del producto y empresa.
- `04-manual-calidad.md`, para politicas institucionales de calidad.
- `06-aspectos-legales.md`, para obligaciones de empresa de software en Bolivia.
- `07-infraestructura-produccion.md`, para despliegue, ambientes, seguridad y CI/CD.
- `11-marketing.md`, para canales de promocion y posicionamiento.
- `12-puesta-marcha.md`, para operacion del producto desplegado.
- `13-software-producto.md`, para ficha tecnica de Wireless HeatMapper.


## Evidencias públicas del sitio web


### Sitio empresarial Team 24 Software

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/>

![QR Sitio empresarial Team 24 Software](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-sitio-empresa.png)


### Facebook oficial Team 24 Software

<https://www.facebook.com/profile.php?id=61591962512748>

![QR Facebook oficial Team 24 Software](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-facebook.png)



# 8. Estudio de Mercado


### Objetivo

Evaluar la oportunidad comercial de Wireless HeatMapper para empresas que instalan, diagnostican o mantienen redes WiFi en interiores, con enfasis inicial en Bolivia y posibilidad de expansion regional.

### Mercado objetivo

El producto atiende a organizaciones que necesitan relevar cobertura WiFi y entregar evidencia tecnica:

- Empresas de telecomunicaciones e integradores de redes.
- Consultoras de infraestructura TI.
- Proveedores de servicios administrados.
- Universidades, colegios, clinicas, hoteles y edificios corporativos.
- Empresas con multiples sedes que requieren estandarizar auditorias WiFi.

### Segmentacion

| Segmento | Necesidad | Disposicion probable |
| -------- | --------- | -------------------- |
| Integradores pequenos | Reducir costo frente a herramientas profesionales caras. | Alta si el precio mensual es accesible. |
| Empresas medianas de TI | Estandarizar reportes y supervisar tecnicos. | Alta con portal cliente y control organizacional. |
| Instituciones educativas | Mejorar cobertura en aulas y laboratorios. | Media, depende de presupuesto anual. |
| Hoteles y comercios | Resolver quejas de conectividad. | Media, compra por proyecto. |
| Consultores independientes | Generar entregables mas profesionales. | Alta con plan economico. |

### Competencia y sustitutos

| Alternativa | Fortalezas | Limitaciones para el mercado objetivo |
| ----------- | ---------- | ------------------------------------- |
| Herramientas profesionales de site survey | Alta precision, reportes avanzados, hardware especializado. | Costo elevado, curva de aprendizaje y menor accesibilidad para equipos pequenos. |
| Apps moviles gratuitas | Bajo costo y disponibilidad inmediata. | No integran plano, portal cliente, gestion organizacional ni trazabilidad. |
| Planillas y mapas manuales | No requieren software especializado. | Alto error manual, poco profesional y dificil de auditar. |
| Desarrollo interno | Ajuste exacto a procesos propios. | Costo alto, mantenimiento permanente y riesgo tecnico. |

Como referencia de problema economico, herramientas comerciales de site survey pueden superar USD 3.000 anuales por licencia, lo que crea espacio para una solucion SaaS local o regional de menor costo.

### Supuestos cuantitativos iniciales

Los siguientes numeros son supuestos de planificacion que deben validarse con entrevistas y cotizaciones reales antes de una decision comercial definitiva:

| Variable | Supuesto base |
| -------- | ------------- |
| Clientes potenciales iniciales en Santa Cruz | 30 empresas o consultores TI con actividad en redes. |
| Tasa de conversion primer ano | 10 % del universo inicial. |
| Clientes pagos primer ano | 3 clientes empresariales. |
| Precio SaaS mensual base | USD 49 por organizacion. |
| Precio SaaS profesional | USD 99 por organizacion. |
| Ticket por implementacion/capacitacion | USD 150 por cliente. |
| Churn anual estimado | 15 %. |

### Modelo de monetizacion

Se recomienda modelo SaaS con planes:

| Plan | Precio referencial | Incluye |
| ---- | ------------------ | ------- |
| Base | USD 49/mes | 1 administrador, 2 tecnicos, proyectos limitados. |
| Profesional | USD 99/mes | Mas tecnicos, portal cliente y mayor volumen. |
| Proyecto unico | USD 120 por proyecto | Uso puntual para consultores o auditorias. |
| Servicios | Desde USD 150 | Capacitacion, carga inicial y soporte especializado. |

### Proyeccion simple de ingresos

| Escenario | Clientes promedio | Ingreso mensual SaaS | Ingreso anual SaaS |
| --------- | ----------------- | -------------------- | ------------------ |
| Conservador | 3 clientes a USD 49 | USD 147 | USD 1.764 |
| Base | 5 clientes a USD 99 | USD 495 | USD 5.940 |
| Optimista | 12 clientes a USD 99 | USD 1.188 | USD 14.256 |

Ingresos por capacitacion pueden agregar entre USD 450 y USD 1.800 durante el primer ano, segun cantidad de clientes y servicios contratados.

### Costos comerciales y operativos iniciales

| Concepto | Estimacion mensual |
| -------- | ------------------ |
| Hosting cloud inicial | USD 40 a USD 80 |
| Dominio y certificados | USD 1 a USD 2 prorrateado si se usa dominio propio |
| Marketing digital basico | USD 50 a USD 100 |
| Soporte y operacion | 10 a 20 horas mensuales |
| Herramientas complementarias | USD 0 a USD 30 |

### Indicadores de mercado

- Costo de adquisicion por cliente.
- Tasa de conversion desde demostraciones.
- Tiempo promedio para configurar un proyecto.
- Numero de proyectos por cliente al mes.
- Retencion mensual.
- Satisfaccion de clientes y tecnicos.

### Conclusion comercial

Wireless HeatMapper es viable como producto SaaS especializado si se posiciona en el espacio entre apps gratuitas insuficientes y suites profesionales costosas. El mercado inicial no debe asumirse masivo; debe trabajarse por nicho, con demostraciones tecnicas, pilotos controlados y validacion de disposicion de pago.



# 9. Pruebas del Software


### Proposito

El plan de pruebas asegura que Wireless HeatMapper cumpla requisitos funcionales, no funcionales y de negocio antes de su entrega como producto. Integra pruebas de desarrollador, QA y Product Owner, ademas de tecnicas de caja blanca, checklists, rendimiento y seguridad.

### Flujo de trabajo de pruebas del Proceso Unificado

| Actividad | Aplicacion en el proyecto |
| --------- | ------------------------- |
| Planificar pruebas | Definir alcance, riesgos, niveles, herramientas y criterios de aceptacion. |
| Disenar pruebas | Derivar casos desde historias, casos de uso, reglas de negocio y riesgos. |
| Implementar pruebas | Automatizar pruebas unitarias, integracion y fixtures. |
| Ejecutar pruebas | Correr suites backend, web, movil y pruebas manuales. |
| Evaluar resultados | Comparar contra criterios de aceptacion, cobertura y defectos. |
| Registrar defectos | Clasificar severidad, responsable y accion correctiva. |
| Verificar correcciones | Reejecutar pruebas afectadas y validar no regresion. |
| Cerrar pruebas | Emitir reporte y autorizacion de liberacion. |

El flujo se resume en una figura UML de actividad incluida en el consolidado.

### Niveles obligatorios

| Nivel | Responsable | Objetivo | Evidencia |
| ----- | ----------- | -------- | --------- |
| 1. Unidad | Programador | Probar su propio codigo antes de entregar. | pytest, Flutter test, pruebas de servicios. |
| 2. QA | QA rotativo | Intentar quebrar el software, revisar rendimiento y seguridad. | Casos negativos, OWASP, latencia, checklist. |
| 3. Product Owner | PO | Validar valor funcional y cumplimiento de negocio. | Acta de aceptacion o rechazo. |

### Herramientas

| Area | Herramientas |
| ---- | ------------ |
| Backend | pytest, pytest-asyncio, pytest-cov, httpx/TestClient. |
| Web | ESLint, build Vite, pruebas UI planificadas con Vitest. |
| Movil | flutter analyze, flutter test. |
| Rendimiento | pytest-benchmark, Locust o k6. |
| Seguridad | OWASP ZAP, revision de dependencias, validacion de configuracion TLS. |
| Datos | Seed controlado y cargas sinteticas. |

### Tecnica de caja blanca: camino basico

Se seleccionan metodos con complejidad ciclomatica >= 3 por contener decisiones relevantes. Para cada metodo se identifican caminos independientes y pruebas minimas.

#### Metodo 1: autenticacion de usuario

**Decision logica:** usuario existente, activo, password valido, token emitido.  
**Complejidad estimada:** 4.

| Camino | Condicion | Resultado esperado |
| ------ | --------- | ------------------ |
| C1 | Email inexistente | Error de credenciales. |
| C2 | Usuario inactivo | Rechazo por estado. |
| C3 | Password invalido | Error de credenciales. |
| C4 | Datos validos | Access token y refresh token emitidos. |

#### Metodo 2: carga y validacion de plano

**Decision logica:** formato, tamano, proyecto propio, conversion de archivo.  
**Complejidad estimada:** 5.

| Camino | Condicion | Resultado esperado |
| ------ | --------- | ------------------ |
| C1 | Proyecto ajeno | 403 o rechazo equivalente. |
| C2 | Formato no permitido | Error de validacion. |
| C3 | Archivo excede limite | Error por tamano. |
| C4 | PDF multipagina no permitido | Error controlado. |
| C5 | Archivo valido | Plano almacenado y metadatos registrados. |

#### Metodo 3: registro de mediciones WiFi

**Decision logica:** plano calibrado, punto valido, RSSI en rango, lote no vacio, propiedad.  
**Complejidad estimada:** 6.

| Camino | Condicion | Resultado esperado |
| ------ | --------- | ------------------ |
| C1 | Plano no calibrado | Rechazo por precondicion. |
| C2 | Punto fuera del plano | Error de validacion. |
| C3 | RSSI fuera de rango | Error de validacion. |
| C4 | Lote vacio | Error de validacion. |
| C5 | Proyecto ajeno | Rechazo por propiedad. |
| C6 | Lote valido | Lecturas persistidas y clasificadas. |

#### Metodo 4: generacion de heatmap

**Decision logica:** puntos minimos, algoritmo soportado, conjunto AP valido, matriz generada, permisos.  
**Complejidad estimada:** 5.

| Camino | Condicion | Resultado esperado |
| ------ | --------- | ------------------ |
| C1 | Menos de 5 puntos | Rechazo por datos insuficientes. |
| C2 | Algoritmo no soportado | Error controlado. |
| C3 | Conjunto AP inexistente | Error de referencia. |
| C4 | Usuario sin permiso | Rechazo por autorizacion. |
| C5 | Datos validos | Mapa de calor generado y persistido. |

### Checklists

#### Checklist previo a release

- [ ] Todas las pruebas automatizadas obligatorias pasan.
- [ ] No existen defectos criticos abiertos.
- [ ] Migraciones aplican correctamente.
- [ ] Variables de entorno productivas estan definidas.
- [ ] TLS y reverse proxy estan operativos.
- [ ] Backups estan configurados.
- [ ] Portal cliente no expone proyectos no publicados.
- [ ] Releases moviles incluyen version y changelog.
- [ ] Terminos y politica de privacidad estan disponibles.

#### Checklist de seguridad

- [ ] JWT expira y refresh token se invalida al cerrar sesion.
- [ ] Roles impiden acceso cruzado.
- [ ] Validacion de ownership en proyectos, planos, mediciones y heatmaps.
- [ ] Entradas del usuario se validan con schemas.
- [ ] Passwords se almacenan con hash seguro.
- [ ] Secretos no estan versionados.
- [ ] API no expone trazas internas en produccion.

### Pruebas de rendimiento

| Operacion | Carga objetivo | Meta |
| --------- | -------------- | ---- |
| Login | 50 usuarios concurrentes | p95 <= 1 s |
| Listado de proyectos | 1.000 proyectos semilla | p95 <= 1 s |
| Registro de mediciones | Lotes de 10 a 50 lecturas | p95 <= 1 s |
| Generacion heatmap | 200 puntos | p95 <= 3 s |
| Portal cliente | 100 accesos concurrentes | p95 <= 2 s |

### Pruebas de vulnerabilidades

Se propone ejecutar OWASP ZAP contra la URL publica y revisar:

- Inyeccion.
- Autenticacion rota.
- Exposicion de datos sensibles.
- Control de acceso roto.
- Configuracion insegura.
- Componentes vulnerables.

### Criterios de cierre

El software se considera apto para entrega cuando las pruebas obligatorias pasan, no existen defectos criticos, los hallazgos medios tienen plan de mitigacion, el Product Owner acepta el alcance y la evidencia queda registrada.


## Evidencia del flujo de trabajo de pruebas


### flujo pruebas rup

![flujo pruebas rup](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/09-flujo-pruebas-rup.png)



# 10. Marketing


### Objetivo general

Dar a conocer Team 24 Software y posicionar Wireless HeatMapper como una solucion accesible, tecnica y verificable para relevamiento de cobertura WiFi en interiores.

### Publicos objetivo

| Publico | Mensaje principal |
| ------- | ----------------- |
| Integradores de redes | Entregue mapas de calor profesionales sin pagar suites costosas. |
| Empresas con sedes fisicas | Detecte zonas muertas y mejore la experiencia de usuarios WiFi. |
| Consultores TI | Profesionalice sus diagnosticos con evidencia visual e interactiva. |
| Instituciones educativas | Planifique cobertura por aulas, laboratorios y oficinas. |
| Hoteles y comercios | Reduzca quejas por mala senal y documente mejoras. |

### Posicionamiento

Wireless HeatMapper se posiciona como una solucion SaaS local, ligera y especializada para equipos que necesitan mapas de calor WiFi, portal cliente y trazabilidad, pero no justifican el costo de herramientas empresariales de alta gama.

### Canales

| Canal | Uso |
| ----- | --- |
| Sitio web | Presentacion institucional, demo, contacto y soporte. |
| Facebook oficial | Alcance local, demostraciones visuales y anuncios publicos en <https://www.facebook.com/profile.php?id=61591962512748>. |
| WhatsApp Business | Contacto comercial y soporte inicial. |
| Ferias tecnologicas | Demostracion presencial con mapas de calor. |
| Convenios academicos | Validacion y difusion en entornos educativos. |
| Repositorio GitHub | Transparencia tecnica y evidencia del producto. |

### Material promocional

- Flyer digital de problema/solucion.
- Video demo de 60 a 90 segundos.
- Caso de uso con plano, mediciones y heatmap.
- Presentacion comercial corta.
- Publicaciones comparativas: app gratuita vs. Wireless HeatMapper.
- QR hacia demo web, Facebook oficial, repositorio y releases moviles.

### Calendario inicial

| Semana | Actividad |
| ------ | --------- |
| 1 | Publicar landing institucional y demo tecnica. |
| 2 | Publicar video corto de captura y heatmap. |
| 3 | Contactar 10 integradores o consultores TI. |
| 4 | Ejecutar 2 demostraciones guiadas. |
| 5 | Publicar caso de estudio Bulldog Tech. |
| 6 | Ajustar propuesta comercial segun retroalimentacion. |

### Presupuesto referencial

| Concepto | Monto mensual |
| -------- | ------------- |
| Diseno de piezas basicas | USD 30 |
| Publicidad digital local | USD 50 a USD 100 |
| Dominio o correo institucional | USD 1 a USD 5 prorrateado |
| Demo y soporte comercial | 10 horas de equipo |

### Metricas

- Visitantes al sitio.
- Clics en QR o enlaces publicos.
- Contactos recibidos.
- Demos agendadas.
- Pilotos iniciados.
- Conversion a plan pago.
- Costo por lead.
- Retencion posterior al primer mes.


# 11. Aspectos para la Puesta en Marcha


### Objetivo

Definir las condiciones necesarias para operar Wireless HeatMapper como producto real: infraestructura cloud, costos, licenciamiento, cuentas de publicacion movil, terminos legales, privacidad y adopcion asistida por IA.

### Comparacion cloud

La arquitectura requiere un servidor de aplicacion, base de datos PostgreSQL, reverse proxy, almacenamiento de planos, backups y monitoreo. Para un inicio controlado se compara AWS, Google Cloud y Azure.

| Criterio | AWS | Google Cloud | Azure |
| -------- | --- | ------------ | ----- |
| Computo | EC2 o ECS. | Compute Engine o Cloud Run. | Virtual Machine, App Service o Container Apps. |
| Base de datos | RDS PostgreSQL o PostgreSQL en VM. | Cloud SQL PostgreSQL o PostgreSQL en VM. | Azure Database for PostgreSQL o PostgreSQL en VM. |
| Costeo | AWS Pricing Calculator. | Google Cloud Pricing Calculator. | Azure Pricing Calculator. |
| Ventaja | Ecosistema maduro y amplio. | Buen soporte de analitica y servicios gestionados. | Integracion directa con entorno Microsoft y VM actual del proyecto. |
| Riesgo | Complejidad inicial. | Costos variables si no se controla egress. | Costos de servicios gestionados pueden subir al escalar. |

### Proyeccion de costos iniciales

Los montos son referenciales y deben recalcularse con las calculadoras oficiales antes de compra o despliegue final.

| Escenario | Infraestructura | Costo mensual estimado |
| --------- | --------------- | ---------------------- |
| Economico | Una VM con Docker Compose, PostgreSQL local, backups manuales. | USD 20 a USD 50 |
| Base | VM 2 vCPU/4 GB, disco persistente, backups automatizados. | USD 40 a USD 90 |
| Gestionado | App service/containers + PostgreSQL gestionado + storage. | USD 80 a USD 180 |
| Escalable | Contenedores gestionados, base gestionada, monitoreo y CDN. | USD 180+ |

Para la entrega academica se utiliza Azure por disponibilidad actual del frontend publicado. Para operacion comercial, se recomienda mantener el escenario base hasta validar clientes pagos.

### Cuentas de tiendas moviles

#### Google Play

Google Play Console requiere cuenta de Google, aceptacion del Developer Distribution Agreement, verificacion de identidad, seleccion de tipo de cuenta personal u organizacion y pago unico de registro de USD 25. Las cuentas personales nuevas tienen requisitos adicionales de pruebas antes de distribucion publica.

#### Apple Developer

Apple Developer Program tiene membresia anual de USD 99 para distribucion en App Store. La inscripcion puede ser individual u organizacion. Las organizaciones deben verificar identidad, contar con D-U-N-S Number y acreditar autoridad para vincular legalmente a la entidad.

### Tipo de licencia

Se recomienda licenciamiento SaaS:

- El cliente paga suscripcion por organizacion.
- Team 24 Software opera backend, web, seguridad y backups.
- La app movil se distribuye como cliente delgado.
- Los datos del cliente se mantienen segregados por organizacion/proyecto.

Tambien puede ofrecerse licencia por proyecto unico para consultores o clientes con baja recurrencia. No se recomienda on-premise en la primera etapa porque incrementa soporte, instalacion y complejidad operativa.

### Terminos y condiciones

Los terminos deben cubrir:

- Descripcion del servicio.
- Roles de usuario.
- Uso permitido y prohibido.
- Responsabilidad sobre datos cargados.
- Disponibilidad y mantenimiento.
- Limitaciones de responsabilidad.
- Propiedad intelectual.
- Suspension de cuentas.
- Soporte y canales oficiales.
- Cambios al servicio.

### Politica de privacidad

La politica debe explicar:

- Datos personales tratados: nombre, email, rol y actividad.
- Datos tecnicos: proyectos, planos, mediciones WiFi, tokens y logs.
- Finalidad: operar el servicio, generar heatmaps, soporte y seguridad.
- Conservacion: mientras exista relacion contractual o necesidad legal.
- Seguridad: autenticacion, control de acceso, cifrado en transito y backups.
- Derechos del usuario: acceso, correccion, eliminacion cuando corresponda.

### Adopcion asistida por IA

Se propone un agente de ayuda integrado que observe contexto de pantalla, rol y flujo actual para responder preguntas sin que el usuario explique desde cero. Ejemplos:

- Si el tecnico esta calibrando plano, explicar como marcar distancia real.
- Si esta capturando WiFi, advertir sobre throttling Android.
- Si el administrador publica enlace, explicar vencimiento y contenido visible.
- Si el cliente consulta portal, explicar interpretacion de colores y RSSI.

### Fuentes oficiales de costos y cuentas

- AWS Pricing Calculator.
- Google Cloud Pricing Calculator.
- Azure Pricing Calculator.
- Google Play Console Help.
- Apple Developer Program.



# 12. Software como Producto (Entregable Final)


### Identificacion del producto

**Nombre:** Wireless HeatMapper  
**Proveedor:** Team 24 Software  
**Cliente inicial:** Bulldog Tech.  
**Modalidad:** SaaS 100 % en linea con app movil Android, backend REST y plataforma web.
**Fuente de verdad:** PostgreSQL central, sin base de datos local de dominio en el dispositivo movil.
**Version movil base:** 1.0.0+1.

Wireless HeatMapper se entrega como un producto integrado para relevamiento, analisis y publicacion de cobertura WiFi. La aplicacion movil funciona como cliente delgado para tecnicos de campo; el backend concentra autenticacion, reglas de negocio, persistencia, generacion de mapas de calor e inteligencia artificial; y la plataforma web permite administracion organizacional, revision tecnica y acceso controlado del cliente final.

### URLs y artefactos publicos

| Recurso | URL | Uso |
| ------- | --- | --- |
| Repositorio GitHub | <https://github.com/borysinho/wireless-heatmapper> | Codigo fuente, documentacion, historial, workflows y trazabilidad tecnica. |
| Sitio empresarial Team 24 Software | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/> | Entrada publica institucional, acceso a producto, descargas, soporte y contacto. |
| Panel administrador | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/admin/login> | Acceso para administradores y usuarios autorizados. |
| Portal cliente | `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/portal/{token}` | Acceso por enlace unico generado desde el panel web. |
| API REST | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/> | Base publica de endpoints consumidos por web y movil. |
| Swagger / OpenAPI | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/docs> | Documentacion interactiva de endpoints. |
| Esquema OpenAPI | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/openapi.json> | Contrato tecnico consumible por herramientas. |
| Manual de usuario | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/> | Guia publica de operacion funcional. |
| Releases moviles | <https://github.com/borysinho/wireless-heatmapper/releases> | APK Android generado por GitHub Actions. |

Estas URLs son las referencias publicas para entrega academica, demostracion y continuidad. En anexos se incorporan codigos QR hacia repositorio, sitio empresarial, documentacion OpenAPI, manual de usuario y releases moviles.

### Componentes entregables

| Componente | Descripcion |
| ---------- | ----------- |
| Backend REST + IA | API FastAPI con autenticacion, roles, servicios de dominio, almacenamiento, mapas de calor, propuestas IA y publicacion para cliente. |
| Base de datos | PostgreSQL con migraciones y entidades para usuarios, clientes, proyectos, planos, mediciones, conjuntos AP, mapas de calor y enlaces. |
| Web admin | Plataforma React/TypeScript para gestionar usuarios, clientes, proyectos RF, datos de campo, escenarios IA y publicacion. |
| Portal cliente | Vista web por token para consultar resultados publicados sin cuenta interna. |
| App movil Android | Cliente Flutter para tecnicos de campo: login, proyectos, planos, captura WiFi y consulta de heatmaps. |
| Infraestructura | Docker Compose, Nginx, TLS, GitHub Actions, despliegue cloud y publicacion de APK. |
| Manual y documentacion | Manual de usuario, modelos, pruebas, puesta en marcha, bibliografia y anexos con evidencias. |

### Componentes backend

| Area | Entrega |
| ---- | ------- |
| API | Servicio REST documentado con OpenAPI y healthcheck operativo. |
| Autenticacion | Login, JWT, refresh token, roles y control de acceso por usuario. |
| Administracion | Gestion de usuarios tecnicos, clientes y proyectos organizacionales. |
| Proyectos | CRUD de proyectos, asociacion con cliente y control de ownership. |
| Planos | Carga, almacenamiento, URLs firmadas, consulta y calibracion. |
| Captura WiFi | Persistencia de puntos de medicion y lecturas RSSI enviadas desde Android. |
| Heatmaps | Generacion de mapas de calor desde datos persistidos. |
| Conjuntos AP | Gestion de conjuntos tecnicos, AP disponibles y mapas asociados. |
| IA | Propuestas de optimizacion como conjuntos derivados y trazables. |
| Portal | Generacion y validacion de enlaces unicos para cliente. |
| Notificaciones | Base tecnica para dispositivos push y notificaciones operativas. |

### Componentes web

| Modulo | Entrega |
| ------ | ------- |
| Login administrador | Autenticacion web y carga de sesion. |
| Dashboard | Vista inicial de administracion. |
| Usuarios | Alta, edicion, consulta y administracion de tecnicos. |
| Clientes | Alta, edicion y consulta de clientes organizacionales. |
| Proyectos RF | Listado organizacional y navegacion al detalle tecnico. |
| Datos de campo | Visualizacion de conjuntos AP, mapas e informacion capturada. |
| Escenarios IA | Consulta de propuestas IA y comparacion con datos de campo. |
| Publicacion | Generacion y administracion del enlace unico para cliente. |
| Portal cliente | Visualizacion publica por token de resultados autorizados. |

### Componentes moviles

| Modulo | Entrega |
| ------ | ------- |
| Autenticacion | Login de tecnico contra backend y manejo seguro de sesion. |
| Proyectos | Listado, creacion, edicion, archivo y eliminacion logica segun permisos. |
| Clientes | Consulta remota de clientes para asociar proyectos. |
| Planos | Listado, carga, visualizacion, calibracion y renovacion de URL firmada. |
| Captura WiFi | Escaneo WiFi Android, seleccion de punto sobre plano y envio de mediciones. |
| Heatmap | Consulta de AP disponibles, conjuntos AP, escala y mapas generados en backend. |
| Conectividad | Avisos cuando la operacion en linea no esta disponible. |
| Notificaciones | Integracion base con Firebase Messaging y notificaciones locales. |
| Configuracion productiva | APK release apuntando a `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api`. |

La app movil conserva solamente credenciales de sesion y preferencias minimas necesarias. No almacena datos de dominio entre sesiones ni implementa sincronizacion diferida.

### Funcionalidades principales por actor

| Actor | Funcionalidades entregadas |
| ----- | -------------------------- |
| Administrador | Iniciar sesion, gestionar usuarios, gestionar clientes, consultar proyectos organizacionales, revisar datos RF, consultar escenarios IA y publicar resultados por enlace. |
| Tecnico de campo | Iniciar sesion en Android, gestionar sus proyectos, cargar y calibrar planos, capturar mediciones WiFi, consultar heatmaps y operar siempre contra el backend. |
| Cliente final | Abrir enlace unico, visualizar proyecto publicado, revisar datos de campo, heatmaps y resultados seleccionados por el administrador. |
| Sistema backend | Persistir dominio, aplicar reglas de acceso, generar heatmaps, gestionar conjuntos AP, producir propuestas IA trazables y servir contratos API. |
| Operacion DevOps | Validar cambios por CI, desplegar contenedores, publicar APK, mantener variables productivas y verificar salud de servicios. |

### Flujo de valor extremo a extremo

1. El administrador crea clientes, tecnicos y revisa proyectos desde la web.
2. El tecnico ingresa a la app movil y crea o selecciona un proyecto asignado.
3. El tecnico sube el plano al backend y calibra la escala del plano.
4. El tecnico captura lecturas WiFi sobre puntos del plano desde Android.
5. El backend persiste puntos, lecturas y datos de APs en PostgreSQL.
6. El tecnico o administrador genera conjuntos AP y mapas de calor.
7. El backend genera propuestas IA como conjuntos derivados y comparables.
8. El administrador selecciona resultados publicables y genera un enlace de cliente.
9. El cliente abre el portal por token y consulta los resultados publicados.

Este flujo demuestra la modalidad 100 % en linea: todas las operaciones de dominio dependen del backend y de la base central.

### Releases moviles

El release movil Android se administra con GitHub Actions.

| Elemento | Definicion |
| -------- | ---------- |
| Disparador automatico | Push de tags `mobile-v*`. |
| Disparador manual | Ejecucion manual con tag opcional y bandera de pre-release. |
| Validaciones previas | Instalacion de dependencias, analisis estatico y pruebas Flutter. |
| Build | APK Android en modo release con variables productivas. |
| Nombre de APK | `WirelessHeatMapper-{TAG}.apk`. |
| Destino | GitHub Releases del repositorio. |
| Retencion adicional | Artefacto temporal de GitHub Actions por 14 dias. |
| Backend configurado | `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api`. |

Cada release movil debe quedar asociado a un tag, un commit de origen, notas de release y APK descargable. El patron recomendado de tag conserva el formato `mobile-v{version}` o `mobile-v{version}-{run}` cuando se genera desde ejecucion manual.

### Repositorio y trazabilidad tecnica

| Recurso | Criterio de control |
| ------- | ------------------- |
| Rama productiva | `main` representa la version desplegable. |
| Rama de integracion | `develop` concentra integracion antes de promocion. |
| Ramas de trabajo | Ramas cortas por historia, correccion, infraestructura o documentacion. |
| Commits | Mensajes claros, preferentemente Conventional Commits en espanol. |
| Pull requests | Cambios funcionales pasan por validaciones aplicables antes de integrarse. |
| Workflows | CI, despliegue cloud y release movil quedan versionados en GitHub. |
| Evidencia historica | Git, GitHub Actions, GitHub Releases, OpenAPI y capturas de demostracion. |

### Criterios de producto terminado

| Criterio | Condicion |
| -------- | --------- |
| Funcional | Flujos principales de administracion, captura, heatmap, IA y portal cliente operan de extremo a extremo. |
| Modalidad online | La app movil no reintroduce base local de dominio ni sincronizacion diferida. |
| Integracion | Backend, web, movil, PostgreSQL, Nginx y workflows estan integrados segun la arquitectura documentada. |
| Seguridad | Roles, ownership, JWT, refresh token, URLs firmadas y tokens de portal se aplican en puntos criticos. |
| Calidad | Pruebas razonables del release ejecutadas sin defectos criticos abiertos. |
| Operacion | Plataforma web publica, API documentada, manual publicado y APK disponible en releases. |
| Documentacion | PAPS, modelos, pruebas, manual, puesta en marcha, bibliografia y anexos se encuentran completos. |
| Evidencia | Existen capturas, video o demostracion guiada de los flujos principales y enlaces publicos. |

### Soporte inicial

El soporte se organiza por niveles para separar dudas de uso, incidentes reproducibles y cambios estructurales.

| Nivel | Responsable | Alcance | Tiempo objetivo inicial |
| ----- | ----------- | ------- | ----------------------- |
| N1 | Product Owner / soporte funcional | Accesos, dudas de uso, navegacion, datos de demo y acompanamiento al cliente. | 1 dia habil |
| N2 | Equipo tecnico | Errores reproducibles, fallas de integracion, problemas de configuracion y revision de logs. | 2 dias habiles |
| N3 | Arquitectura / desarrollo | Defectos complejos, seguridad, migraciones, infraestructura, IA y cambios de diseno. | 3 a 5 dias habiles |

Canales minimos recomendados:

- Correo de soporte institucional.
- Registro de incidencias en GitHub Issues o tablero equivalente.
- Evidencia obligatoria por incidencia: usuario afectado, fecha, pasos, captura, URL o proyecto relacionado.
- Clasificacion por severidad: critica, alta, media o baja.

### Versionado

| Artefacto | Regla de versionado |
| --------- | ------------------- |
| Codigo fuente | Historial Git con commits atomicos y tags para releases relevantes. |
| Backend | Version expuesta por healthcheck y metadatos de la API. |
| Web | Version asociada al commit desplegado y a la imagen Docker publicada. |
| Movil | Version declarada en Flutter y tag `mobile-v*`. |
| Imagenes Docker | Tags `latest` y `COMMIT_SHA` en el registro de contenedores. |
| Documentacion | Control por Git y actualizacion junto al release. |
| Base de datos | Migraciones versionadas junto al cambio de modelo. |

Cada release debe incluir:

- Numero o tag de version.
- Fecha de publicacion.
- Commit o hash de referencia.
- Cambios principales.
- Correcciones incluidas.
- Riesgos conocidos o limitaciones.
- Artefactos publicados: APK, imagenes Docker, URL productiva o documentacion.
- Evidencias de pruebas ejecutadas.

### Evidencias de funcionamiento

| Evidencia | Forma esperada |
| --------- | -------------- |
| Repositorio accesible | URL publica de GitHub y hash del commit entregado. |
| Pipeline CI | Ejecucion de GitHub Actions sin fallos criticos en backend, web y manual. |
| Despliegue productivo | Plataforma web abierta en el dominio Azure y healthcheck backend operativo. |
| OpenAPI | Swagger disponible en `/api/docs` y esquema en `/api/openapi.json`. |
| APK Android | Archivo publicado en GitHub Releases con notas de release. |
| Login administrador | Captura o video del acceso a `/admin/login`. |
| Gestion de usuarios/clientes | Captura o video de alta, edicion o consulta. |
| Proyecto y plano | Captura o video de creacion de proyecto, carga y calibracion de plano. |
| Captura WiFi movil | Captura o video de punto medido y lectura enviada al backend. |
| Heatmap | Captura o video del mapa de calor generado desde datos persistidos. |
| Escenario IA | Captura o video de propuesta IA como conjunto derivado. |
| Portal cliente | URL con token de demo y captura de resultados publicados. |
| Manual de usuario | Sitio `/manual/` accesible con guia funcional. |
| Consolidado final | Documento academico en Word con diagramas y codigos QR. |

Para la entrega final, las evidencias deben vincularse al mismo commit o release que se presenta. Si una evidencia corresponde a un ambiente de demo, se registra la fecha, usuario de prueba, proyecto usado y limitaciones conocidas.

### Cierre de producto

Wireless HeatMapper queda definido como un producto integrado compuesto por:

- Backend FastAPI con persistencia PostgreSQL, reglas de negocio, generacion de heatmaps e IA.
- Plataforma web React/Vite para administracion, revision RF, escenarios IA y portal cliente.
- App Android Flutter para tecnicos de campo, operando como cliente delgado en linea.
- Infraestructura productiva reproducible con Docker Compose, Nginx, TLS y GitHub Actions.
- Repositorio, releases moviles, documentacion, manual y evidencias suficientes para demostracion y continuidad.

El producto final cumple la orientacion del proyecto: captura, analisis y entrega de resultados WiFi sin persistencia local de dominio en el dispositivo movil y con PostgreSQL como fuente central de verdad.


## Evidencias públicas del producto


### Repositorio GitHub

<https://github.com/borysinho/wireless-heatmapper>

![QR Repositorio GitHub](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-repositorio.png)


### Documentación Swagger / OpenAPI

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/docs>

![QR Documentación Swagger / OpenAPI](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-api-docs.png)


### Manual de usuario

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/>

![QR Manual de usuario](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-manual.png)


### Releases móviles

<https://github.com/borysinho/wireless-heatmapper/releases>

![QR Releases móviles](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-releases.png)

