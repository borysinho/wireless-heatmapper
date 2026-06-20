**UNIVERSIDAD AUTONOMA GABRIEL RENE MORENO**

Facultad de Ingeniería en Ciencias de la Computación y
Telecomunicaciones

![](media/image1.png){width="2.576388888888889in"
height="2.8666666666666667in"}\*\* \*\*

---

**Sistema Inteligente de Análisis y Optimización de Cobertura WiFi
mediante Mapas de Calor**

---

**Variante:** Modalidad 100 % en línea (sin persistencia local en el dispositivo móvil ni mecanismos de sincronización diferida)

---

**Docente:** Ing. Rolando Martínez

**Materia:** Ingeniería de Software II

**Grupo:** 24

**Estudiantes:**

- Fernandez Ortega Jhasmany Jhunnior - 207025509

<!-- -->

- Quiroga [Flores]{.underline} Herland Borys - 200104373

**Fecha:** 14/04/2026

**Santa Cruz -- Bolivia**

# 1. PAPS

## Introducción

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

# 2. Métricas

## 2.1 Software de referencia

Con el propósito de establecer una base comparativa que permita estimar
el tamaño, esfuerzo y complejidad del sistema propuesto, se analizaron
tres proyectos de software de código abierto con funciones similares a
las del Wireless HeatMapper. Los proyectos seleccionados poseen
repositorios públicos en GitHub, lo que facilita la extracción de
métricas objetivas de tamaño, productividad y calidad. A continuación se
describe cada uno de estos sistemas.

### 2.1.1 WiFiAnalyzer

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

### 2.1.2 WiFiSurveyor

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

### 2.1.3 python-wifi-survey-heatmap

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

## 2.2 Métricas Orientadas al Tamaño (MoT)

Las métricas orientadas al tamaño establecen medidas directas del
software producido, normalizadas por el volumen de código fuente.
Siguiendo el marco propuesto por Pressman (2010), las medidas directas
empleadas son: líneas de código en miles (KLDC), esfuerzo expresado en
personas-mes (PM), cantidad de desarrolladores, y número de errores y
defectos reportados. A partir de estas medidas se derivan las métricas
de calidad y productividad.

### Líneas de código (KLDC)

El recuento de líneas de código se expresó en miles (KLDC). Para los
proyectos de referencia, el valor fue estimado a partir del tamaño del
repositorio, el número de confirmaciones y la madurez funcional
observada, dado que no existe una medición publicada por los autores.

### Tiempo de desarrollo

Se tomó como referencia el período de actividad del repositorio (desde
la primera confirmación hasta la versión estable más reciente),
ponderado por el número de contribuidores para obtener una estimación
del esfuerzo acumulado en personas-mes.

### Cantidad de desarrolladores

Se consideró la cantidad de contribuidores activos registrados en el
repositorio. WiFiAnalyzer cuenta con una comunidad de más de 15
contribuidores; WiFiSurveyor fue desarrollado por un equipo de
aproximadamente 3 personas; python-wifi-survey-heatmap tiene un único
desarrollador principal.

### Errores y defectos

Como indicador de defectos conocidos se utilizó el número de incidencias
abiertas (issues) en GitHub al momento del análisis, que refleja los
problemas reportados por los usuarios y pendientes de resolución.

### Esfuerzo

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

## 2.3 Cálculo de métricas

A partir de los datos de la tabla anterior se calculan las métricas de
calidad y productividad definidas por Pressman (2010) para cada proyecto
de referencia.

### Calidad = (Errores + Defectos) / KLDC

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

### Productividad = (KLDC / Esfuerzo) × 1 000

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

# 3. Métricas Orientadas a la Función (MoF)

Las métricas orientadas a la función miden el software en términos de la
funcionalidad que entrega al usuario, con independencia del lenguaje de
programación utilizado. El método de Puntos de Función (PF), propuesto
por Albrecht y formalizado por Pressman (2010), cuantifica las
características del dominio de información del sistema mediante cinco
parámetros de medición, a los que se aplican factores de peso según su
complejidad.

## 3.1 Parámetros de medición

Los parámetros utilizados para calcular los puntos de función sin
ajustar son los siguientes:

### Número de entradas (datos WiFi)

Representa el número de tipos de entrada distintos que el usuario o un
sistema externo proporciona a la aplicación. En el contexto de los
proyectos analizados, incluye formularios de configuración, parámetros
de escaneo, archivos de plano y datos de señal capturados
automáticamente y enviados en línea al backend.

### Número de salidas (mapas, reportes)

Corresponde a los tipos de salida que el sistema genera hacia el
usuario, incluyendo pantallas de visualización, mapas de calor, gráficas
de señal y documentos de reporte exportables.

### Número de consultas

Son las transacciones interactivas en las que el usuario solicita
información al sistema, como la consulta de historial de mediciones, el
filtrado de redes por SSID o frecuencia, y la búsqueda en la base de
datos de fabricantes.

### Archivos internos (datos de medición)

Corresponde a los grupos lógicos de datos mantenidos internamente por la
aplicación. En la modalidad 100 % en línea estos grupos residen
exclusivamente en la base de datos central PostgreSQL del backend
(proyectos, planos, mediciones, modelos de IA y configuraciones de
usuario); el cliente móvil no mantiene grupos lógicos persistentes
de dominio.

### Interfaces externas (APIs, sensores WiFi)

Son los archivos o servicios de datos que la aplicación comparte con
sistemas externos, como las APIs del sistema operativo para el acceso al
hardware WiFi, servicios en la nube y herramientas de terceros.

## 3.2 Cálculo de puntos de función

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

### Conteo total --- WiFiAnalyzer

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

### Conteo total --- WiFiSurveyor

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

### Conteo total --- python-wifi-survey-heatmap

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

### Factores de peso

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

### Complejidad del sistema

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

# 4. Complejidad del Software

La complejidad del Wireless HeatMapper es calificada como alta, en
concordancia con la naturaleza de sus componentes técnicos. La
evaluación se realiza sobre los seis factores principales del sistema:

## Procesamiento de datos

La aplicación debe capturar y transmitir en línea grandes volúmenes
de muestras de señal (RSSI, SSID, BSSID, canal y frecuencia) durante
el recorrido del espacio. La gestión eficiente de esta información
requiere un diseño cuidadoso de los endpoints REST de ingesta, del
control de concurrencia en el backend y del manejo de reintentos
controlados ante latencias o errores transitorios.

## Análisis de señal

El análisis incluye la identificación de zonas muertas, la detección de
solapamiento entre puntos de acceso y el reconocimiento de
interferencias por canal, procesos que implican comparaciones
multidimensionales sobre los datos capturados.

## Algoritmos de interpolación

La transformación de puntos de medición dispersos en un campo de
cobertura continuo se realiza mediante técnicas de interpolación
espacial (por ejemplo, interpolación de distancia inversa ponderada o
kriging). Estos algoritmos se ejecutan en el backend FastAPI, lo que
libera al cliente móvil de la carga computacional pero introduce
exigencias de rendimiento sobre el servidor y de eficiencia en la
serialización del campo continuo devuelto al cliente.

## Uso de inteligencia artificial

El módulo de recomendación de posicionamiento de puntos de acceso emplea
un modelo de aprendizaje automático entrenado con patrones de
propagación de señal, geometría de planos y características del entorno
físico. El modelo está hospedado en el backend y se consume vía API
REST tanto desde la app móvil como desde el portal de cliente, lo que
representa el componente de mayor complejidad técnica del proyecto.

## Interfaces móviles

La aplicación debe ofrecer una experiencia de usuario fluida en
pantallas de tamaño reducido, con visualizaciones de mapas de calor
interactivas que permitan zoom, desplazamiento y superposición de capas
informativas sobre el plano importado, manteniendo a la vez una
indicación clara del estado de conexión con el backend.

## Arquitectura cliente-servidor en línea

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

# 5. Estimaciones

## 5.1 Dimensiones del proyecto

### Tamaño: Alto

Según los proyectos de referencia analizados, el Wireless HeatMapper
en modalidad 100 % en línea se ubica en un rango de tamaño **alto**:
su conteo de 238 puntos de función ajustados supera ampliamente a los
tres sistemas comparados, y su estimación de KLDC (desarrollada en la
sección de métodos de estimación) se sitúa en el orden de los 18.5
KLDC, considerando los dos componentes del sistema: app móvil
Android (cliente delgado) y plataforma web con backend REST.

### Complejidad: Alta

La presencia de algoritmos de interpolación espacial, integración de
un modelo de inteligencia artificial, acceso al hardware WiFi de
Android, visualización interactiva de mapas de calor y la operación
bajo una arquitectura cliente-servidor estrictamente en línea entre
el cliente móvil y el servidor web sitúan al sistema en la categoría
de complejidad alta.

### Estabilidad: Media

Los requisitos funcionales principales están bien definidos a partir del
caso real de Bulldog Tech.; sin embargo, la especificación del módulo de
IA y los detalles del plan de implementación de APs pueden evolucionar
durante el desarrollo, lo que introduce una estabilidad media.

# 6. Ámbito del proyecto

## 6.1 Objetivo general

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

## 6.2 Objetivos específicos

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

# 7. Requerimientos principales

## RP1: Captura de señal WiFi

La aplicación debe escanear automáticamente las redes WiFi disponibles
en cada punto del recorrido y registrar los parámetros RSSI, SSID,
BSSID, canal y frecuencia, asociándolos a la posición actual del usuario
sobre el plano y transmitiéndolos en línea, request por request, al
backend para su persistencia en la base de datos central. El cliente
móvil no almacena las muestras entre sesiones: cada lote capturado se
envía en el momento y se descarta del estado en memoria una vez
confirmado por el servidor.

## RP2: Mapeo sobre plano

El sistema debe permitir la importación de planos de edificios en
formato PNG o PDF como imagen de referencia. Al importarse, el plano
se sube de inmediato al backend y se asocia al proyecto en curso; el
usuario puede entonces marcar puntos de medición o registrarlos de
forma continua durante el recorrido, viéndolos reflejados en línea
sobre el plano servido por el backend.

## RP3: Generación de heatmap

A partir de los puntos de medición registrados en el backend, el
servicio de interpolación espacial del backend debe generar un mapa
de calor continuo y devolverlo al cliente para su visualización,
utilizando una escala de color graduada (verde para señal excelente,
rojo para zona muerta o señal nula). El cliente móvil no ejecuta la
interpolación: solamente solicita el heatmap actualizado al backend
y lo renderiza.

## RP4: Análisis de cobertura

El sistema debe analizar automáticamente el mapa de calor generado para
identificar zonas muertas, puntos de solapamiento excesivo entre APs e
interferencias por canal, y presentar los resultados al usuario de forma
clara y estructurada.

## RP5: Optimización mediante IA

La aplicación debe incorporar un módulo de inteligencia artificial que,
a partir del análisis de cobertura y del inventario RF del sitio, sugiera
escenarios completos para instalaciones nuevas o redes existentes. Cada
escenario debe distinguir AP físico, radio y BSSID; recomendar cantidad,
posición, altura, modelo, antena, canal, ancho y potencia por radio; producir
resultados separados para 2,4 GHz y 5 GHz; y generar valores y mapas de calor
proyectados sin modificar las mediciones observadas. El detalle técnico
aprobado se define en la [Especificación de Optimización RF por Escenarios](PLAN-IMPLEMENTACION/17-especificacion-optimizacion-rf/00-indice.md).

## RP6: Generación de reportes

El sistema debe permitir la exportación de reportes técnicos que
documenten el estado actual de la cobertura, las zonas problemáticas
identificadas y el plan de implementación propuesto, en un formato
adecuado para ser entregado al cliente como parte del cierre del
proyecto.

## RP7: Administración de usuarios

La plataforma web debe proveer un panel de administración con
autenticación basada en roles que permita crear, activar y desactivar
cuentas de técnicos, así como visualizar el listado completo de los
proyectos de la organización con su estado y actividad reciente. Esta
funcionalidad resuelve la dependencia de aprovisionamiento previo de
usuarios identificada en la historia de autenticación de la app móvil.

## RP8: Persistencia centralizada en línea

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

## RP9: Portal de cliente

El sistema debe permitir al técnico generar, al cierre de un proyecto,
un enlace único de acceso para que el cliente visualice los resultados
en un portal web sin necesidad de instalar la aplicación móvil. El
portal debe presentar el mapa de calor actual, el mapa de calor
proyectado, el análisis de cobertura y el plan de implementación de
APs de forma interactiva, con autenticación por token de un solo
proyecto y expiración configurable.

# 8. Rendimiento

## Tiempo de procesamiento de mapas

La generación del mapa de calor a partir de los puntos de medición no
debe superar los 5 segundos extremo a extremo (request del cliente,
interpolación en backend y entrega de la respuesta) para encuestas de
hasta 200 puntos de medición, garantizando una respuesta ágil durante
el trabajo en campo.

## Tiempo de respuesta de la aplicación

La interfaz de usuario debe responder a las interacciones del usuario
(zoom, desplazamiento, selección de puntos) en un tiempo inferior a 500
milisegundos sobre datos ya recibidos del backend, de modo que la
experiencia de uso en campo no se vea comprometida.

## Latencia de red end-to-end

Sobre una conexión móvil estable, el envío de un lote de scan WiFi al
backend debe completarse con un percentil 95 (p95) ≤ 1 segundo, y la
solicitud de un heatmap actualizado debe responderse con p95 ≤ 3
segundos. Estos objetivos se miden incluyendo el viaje de red en
ambas direcciones y son condición indispensable para la experiencia
en campo del técnico, dado que toda operación es en línea.

# 9. Fiabilidad

## Precisión de medición

Los valores de RSSI registrados deben ser consistentes con los
reportados por el hardware WiFi del dispositivo, sin transformaciones
que introduzcan desviaciones. La precisión del posicionamiento sobre el
plano depende del método de localización empleado y debe ser documentada
en el manual de usuario.

## Consistencia del análisis

Dada la misma colección de datos de medición almacenados en el
backend, el sistema debe producir resultados idénticos en sucesivas
ejecuciones del análisis. El algoritmo de interpolación y el modelo
de IA deben operar de forma determinista o documentar explícitamente
cualquier componente estocástico.

# 10. Restricciones

## 10.1 Técnicas

### Limitaciones de sensores móviles

Los sensores WiFi de los dispositivos Android acceden a la intensidad de
señal a través de la API del sistema operativo (WifiManager), que impone
restricciones en la frecuencia de escaneo (scan throttling) a partir de
Android 8.0. El diseño de la aplicación debe contemplar estas
limitaciones para no degradar la densidad de muestras recolectadas.

### Precisión en interiores

La localización GPS pierde precisión en espacios interiores. La
aplicación deberá recurrir a métodos alternativos de posicionamiento
(marcado manual sobre el plano o posicionamiento relativo por
desplazamiento) cuya exactitud quedará acotada por la interacción del
usuario.

### Conectividad obligatoria

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

### Seguridad de la plataforma web

El portal de cliente debe implementar autenticación mediante token de
enlace único de un solo proyecto, con expiración configurable y
contador de accesos auditable. El panel de administración debe
operar bajo un esquema de roles diferenciados (Administrador y
Técnico) con autenticación basada en credenciales y manejo de sesión
sobre HTTPS. Las contraseñas deben almacenarse hasheadas (bcrypt) en
la base de datos central.

### Compatibilidad de navegadores

La plataforma web debe ser funcional en las dos últimas versiones
estables de los navegadores Chrome, Firefox y Safari, sin requerir la
instalación de extensiones ni complementos adicionales por parte del
usuario.

## 10.2 Recursos

### Tiempo de desarrollo

El proyecto se desarrolla en el marco de un semestre académico, lo que
impone una restricción temporal de aproximadamente seis meses para la
entrega del prototipo funcional.

### Herramientas disponibles

El equipo de desarrollo dispone de Android Studio y Flutter SDK como
entorno principal para la app móvil, Python (FastAPI) para el
desarrollo del backend y del modelo de inteligencia artificial,
React + TypeScript para la plataforma web, PostgreSQL como motor de
base de datos central, Docker para la contenerización del backend y
las herramientas de control de versiones y colaboración provistas
por GitHub.

# 11. Interfaces externas

## Dispositivos móviles

La aplicación está dirigida a dispositivos Android con API nivel 26
(Android 8.0 Oreo) o superior, que dispongan de interfaz WiFi activa,
conectividad de datos hacia el backend y capacidad de procesamiento
suficiente para renderizar mapas de calor recibidos del servidor.

## Sensores WiFi

El acceso al hardware WiFi se realiza a través de la API WifiManager de
Android, que expone la información de las redes detectadas en cada
escaneo, incluyendo RSSI, SSID, BSSID, canal y frecuencia.

## Servicios en la nube

El sistema integra un servidor backend desplegado en la nube que cumple
tres funciones operadas estrictamente en línea: (i) ingesta y
persistencia central de proyectos, planos, mediciones, análisis y
heatmaps consumida por la app móvil durante todo el ciclo de vida
del proyecto, (ii) hospedaje del modelo de IA expuesto vía API REST,
y (iii) provisión de la base de datos central PostgreSQL que sustenta
tanto el panel de administración como el portal de cliente. El
backend constituye la única fuente de verdad del dominio.

## APIs de análisis

El módulo de inteligencia artificial está hospedado de forma
definitiva en el servidor backend (FastAPI) y expone endpoints REST
(`/optimize-aps`, `/predict-coverage`) que son consumidos tanto por la
app móvil para obtener recomendaciones en campo, como por el portal
de cliente para re-ejecutar la inferencia bajo demanda al visualizar
los resultados. Esta arquitectura libera al dispositivo móvil de la
carga computacional del modelo y centraliza el ciclo de actualización.

## Navegador web

La plataforma web es accesible desde cualquier navegador moderno sin
necesidad de instalación. El panel de administración requiere
autenticación con credenciales de Administrador o Técnico, mientras
que el portal de cliente se accede mediante un enlace único con token
de un solo proyecto.

# 12. Métodos de estimación

Se aplicaron tres métodos de estimación complementarios para obtener
rangos de esfuerzo y tamaño consistentes: estimación basada en líneas de
código mediante la fórmula de tres puntos, el modelo COCOMO II con
puntos de objeto y la técnica de Planning Poker sobre las historias de
usuario principales.

## 12.1 Estimación basada en líneas de código

### Escenarios: optimista, probable, pesimista

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

## 12.2 Modelo COCOMO II

El modelo COCOMO II en su variante de composición de aplicación utiliza
puntos de objeto para estimar el esfuerzo en etapas tempranas. Los
elementos contabilizados son pantallas de interfaz, reportes y
componentes de software.

### Pantallas

Se identificaron 19 pantallas principales: en la app móvil —inicio de
sesión, panel principal, nueva encuesta, importación de plano,
escaneo activo, visualización de mapa de calor, resultados de
análisis, detalle de zona, recomendaciones de IA, comparación de
escenarios, configuración de reporte, vista previa del reporte,
historial de proyectos, ajustes de la aplicación—; y en la plataforma
web —login web, dashboard de administración, gestión de usuarios,
listado de proyectos de la organización, vista interactiva del
portal de cliente (heatmap + análisis + plan AP).

### Reportes

Se definieron 6 tipos de reporte: cobertura WiFi detallada, análisis
de interferencias, plan de implementación de APs, comparación de
escenarios (antes/después), resumen ejecutivo para el cliente y
reporte interactivo web exportable desde el portal de cliente.

### Componentes

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

## 12.3 Planning Poker

### Historias de usuario

Se estimaron los nueve requerimientos principales utilizando la
técnica de Planning Poker con la escala de Fibonacci. La estimación
refleja la complejidad relativa percibida por el equipo de
desarrollo, considerando que la operación es estrictamente en línea
y que el cliente móvil no implementa lógica de persistencia local
ni de sincronización diferida.

### Estimación por puntos

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

# 13. Ecuación del Software

El modelo dinámico multivariable de Putnam y Myers, formalizado por
Pressman (2010) como la Ecuación del Software, permite estimar el tiempo
mínimo de desarrollo a partir del tamaño del sistema:

**t_mín = 8.14 × (LOC / P)\^0.43**

## Cálculo de esfuerzo

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

## Parámetros de productividad

E = 180 × B × t³ (t en años, E en personas-mes)

E = 180 × 0.34 × (0.883)³ = 61.2 × 0.689 ≈ 42 personas-mes

## Estimación del equipo de trabajo

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

# 14. Planificación del tiempo

## 14.1 Diagrama de Gantt

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

## 14.2 Diagrama de PERT

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

# 15. Gestión de riesgos

## Riesgos técnicos

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

## Riesgos de desarrollo

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

## Riesgos de entorno

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

# 16. Tabla de recursos

## Hardware

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

## Software

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

## Recursos humanos

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

## Infraestructura

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

# 17. Organización interna

## Estructura del equipo

El equipo está conformado por dos desarrolladores-investigadores con
dedicación compartida entre el desarrollo del sistema y la investigación
sobre los algoritmos de interpolación e inteligencia artificial. Ambos
miembros participan en todas las fases del proyecto, con una
distribución de responsabilidades por componente según se detalla en la
tabla de recursos humanos.

## Roles

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

# 18. Mecanismos de seguimiento y control

## 18.1 Reuniones Scrum

### Daily

Reunión diaria de 15 minutos para sincronizar el avance, identificar
impedimentos y ajustar el plan del día. Se realiza de forma presencial o
mediante videollamada según la disponibilidad del equipo.

### Sprint Review

Al final de cada sprint (cada dos semanas), el equipo presenta las
funcionalidades completadas al docente tutor y, cuando sea posible, a un
representante de Bulldog Tech. El resultado de esta revisión alimenta el
backlog de la siguiente iteración.

### Sprint Retrospective

Reunión interna al término de cada sprint para analizar los procesos de
trabajo, identificar oportunidades de mejora y acordar acciones
concretas para el siguiente ciclo.

## 18.2 Control del proyecto

### Seguimiento de tareas

Las tareas se gestionan mediante el tablero Kanban del repositorio en
GitHub (GitHub Projects), con columnas de estado: Pendiente, En
progreso, En revisión y Completado. Cada tarea está asociada a un
requerimiento principal y a un sprint.

### Evaluación del progreso

Al inicio de cada sprint se actualiza el gráfico de avance (burndown
chart) con los puntos de historia completados frente a los planificados.
Si la velocidad real difiere en más de un 20 % de la planificada durante
dos sprints consecutivos, el equipo convoca una reunión extraordinaria
para revisar el alcance o redistribuir tareas.
