# Carátula

**UNIVERSIDAD AUTÓNOMA GABRIEL RENÉ MORENO**
**FACULTAD DE INGENIERÍA EN CIENCIAS DE LA COMPUTACIÓN Y TELECOMUNICACIONES**
**CARRERA DE INGENIERÍA INFORMÁTICA**

# Wireless HeatMapper

**Sistema integrado de levantamiento y visualización de cobertura Wi-Fi**

**Proyecto de Desarrollo de Software**
**Ingeniería de Software II — Grupo 24**

**Integrantes:**

| Apellidos y Nombres                | Registro  |
| ---------------------------------- | --------- |
| Fernandez Ortega Jhasmany Jhunnior | 207025509 |
| Quiroga Flores Herland Borys       | 200104373 |

**Santa Cruz de la Sierra, Bolivia**
**Mayo de 2026**


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 2. Tabla de Contenidos

- [1. Carátula](#1-carátula)
- [2. Tabla de Contenidos](#2-tabla-de-contenidos)
- [3. Introducción](#3-introducción)
- [4. Antecedentes](#4-antecedentes)
  - [4.1 Fundamentación Teórica](#41-fundamentación-teórica)
  - [4.2 Comparación de Software Similar](#42-comparación-de-software-similar)
- [5. Descripción del Problema](#5-descripción-del-problema)
  - [5.1 Narrativa del Problema](#51-narrativa-del-problema)
  - [5.2 Diagrama Causa-Efecto (Ishikawa)](#52-diagrama-causa-efecto-ishikawa)
  - [5.3 Modelo de Dominio](#53-modelo-de-dominio)
- [6. Situación Problemática](#6-situación-problemática)
- [7. Situación Deseada](#7-situación-deseada)
- [8. Objetivos](#8-objetivos)
  - [8.1 Objetivo General](#81-objetivo-general)
  - [8.2 Objetivos Específicos](#82-objetivos-específicos)
- [9. Alcance](#9-alcance)
  - [9.1 Módulo de Autenticación y Usuarios](#91-módulo-de-autenticación-y-usuarios)
  - [9.2 Módulo de Gestión de Proyectos](#92-módulo-de-gestión-de-proyectos)
  - [9.3 Módulo de Levantamiento Wi-Fi](#93-módulo-de-levantamiento-wi-fi)
  - [9.4 Módulo de Heatmap](#94-módulo-de-heatmap)
  - [9.5 Módulo de Análisis con IA](#95-módulo-de-análisis-con-ia)
  - [9.6 Panel de Administración Web](#96-panel-de-administración-web)
- [10. Tecnología de Desarrollo](#10-tecnología-de-desarrollo)
  - [10.1 Stack Tecnológico](#101-stack-tecnológico)
  - [10.2 Proceso de Desarrollo](#102-proceso-de-desarrollo)
- [11. Bibliografía](#11-bibliografía)
- [12. Anexos](#12-anexos)
  - [12.1 Esquema Gráfico: Situación Actual vs. Situación Deseada](#121-esquema-gráfico-situación-actual-vs-situación-deseada)
  - [12.2 Datos del Caso de Estudio](#122-datos-del-caso-de-estudio)
  - [12.3 Currículum Vitae de los Integrantes](#123-currículum-vitae-de-los-integrantes)

---

## Parte 2 — Resultados del Proceso de Desarrollo

### Sprint 0 — Ingeniería de Requisitos Inicial

- [S0.1 Organización del Equipo](#s01-organización-del-equipo)
- [S0.2 Ingeniería de Requisitos](#s02-ingeniería-de-requisitos)
- [S0.3 Modelos Iniciales del Sistema](#s03-modelos-iniciales-del-sistema)

### Sprint 1 — Fundación Backend y Admin

- [S1.1 Historias de Usuario](#s11-historias-de-usuario)
- [S1.2 Modelos Generados](#s12-modelos-generados)
  - [S1.2.1 Modelo de Contexto](#s121-modelo-de-contexto)
  - [S1.2.2 Modelo de Arquitectura](#s122-modelo-de-arquitectura)
  - [S1.2.3 Modelo de Datos](#s123-modelo-de-datos)
  - [S1.2.4 Modelo de Lógica](#s124-modelo-de-lógica)
- [S1.3 Implementación](#s13-implementación)
- [S1.4 Pruebas](#s14-pruebas)


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 3. Introducción

Bulldog Tech. es una empresa tecnológica con sede en Santa Cruz de la Sierra, Bolivia, con trayectoria consolidada en servicios de soporte técnico, mantenimiento de equipos y consultoría en sistemas de información. Hace aproximadamente un año, la empresa amplió su cartera incorporando el área de infraestructura tecnológica de telecomunicaciones, que comprende la instalación, configuración y mantenimiento de redes de datos inalámbricas para clientes corporativos y pymes de la región.

En esa área, el proceso de trabajo que la empresa ha adoptado sigue el modelo tradicional del sector: el técnico especializado visita las instalaciones del cliente, evalúa el espacio con criterio propio y determina la ubicación de los puntos de acceso a partir de su experiencia directa. Es el técnico quien, en ese recorrido presencial, aporta el mayor valor para la toma de decisiones sobre posicionamiento, cantidad y configuración de los equipos. El resultado depende, en gran medida, de la calidad de ese juicio profesional y de la información que logra obtener durante la visita.

El **Wireless HeatMapper** surge como respuesta al límite natural de ese proceso. A medida que la empresa asume proyectos de mayor envergadura, la evaluación exclusivamente subjetiva resulta insuficiente para garantizar coberturas homogéneas, documentar las decisiones técnicas o demostrar objetivamente los resultados a los clientes. El sistema propuesto permite al técnico respaldar y enriquecer su criterio con datos de señal medidos en campo, generando mapas de calor sobre los planos reales de las instalaciones, identificando zonas problemáticas y produciendo reportes que acompañan cada proyecto de infraestructura.

Este documento fue elaborado por el equipo de desarrollo —Fernandez Ortega Jhasmany Jhunnior y Quiroga Flores Herland Borys— a partir del trabajo de análisis, diseño y planificación realizado directamente con el cliente, **Bulldog Tech.**

El documento se organiza en dos partes. La **Parte 1** contiene el Perfil del Proyecto: contexto del problema, objetivos, alcance y tecnologías seleccionadas. La **Parte 2** documenta los resultados de las dos primeras iteraciones: el Sprint 0 (ingeniería de requisitos inicial y modelos del sistema) y el Sprint 1 (primera entrega funcional con autenticación, gestión de usuarios, clientes y proyectos). A lo largo del texto el lector encontrará los fundamentos que justifican cada decisión tomada durante el desarrollo.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 4. Antecedentes

## 4.1 Fundamentación Teórica

La fundamentación teórica del proyecto descansa sobre tres pilares: el comportamiento físico de las señales de radiofrecuencia en espacios interiores, las métricas estándar de medición de cobertura Wi-Fi y la metodología profesional de *site survey*. La fuente técnica de referencia para esta sección es el libro *CWNA Certified Wireless Network Administrator Study Guide (Examen CWNA-107)*, que constituye el estándar de la industria para la certificación de administradores de redes inalámbricas.

### 4.1.1 Propagación de señal RF en espacios interiores

Las redes de área local inalámbrica (WLAN), estandarizadas bajo la familia IEEE 802.11, operan principalmente en las bandas de radiofrecuencia de 2.4 GHz y 5 GHz. A diferencia de los entornos exteriores, los espacios interiores presentan condiciones de propagación adversas que determinan directamente la calidad de la cobertura.

El modelo teórico base de pérdida de señal en el espacio libre es la **ecuación FSPL** (*Free Space Path Loss*):

> FSPL (dB) = 20 log(d) + 20 log(f) + 20 log(4π/c)

donde *d* es la distancia en metros y *f* es la frecuencia en Hz. En la práctica, la atenuación real supera siempre a la teórica porque los materiales de construcción absorben y reflejan la señal. La siguiente tabla resume los valores de atenuación empírica documentados en el estándar CWNA-107:

**Tabla 1.** Atenuación típica de materiales constructivos sobre señal Wi-Fi (fuente: CWNA-107, Cap. 3)

| Material                  | Atenuación aproximada (dB) |
| ------------------------- | -------------------------- |
| Tabique de yeso (drywall) | 3 a 5                      |
| Ventana de vidrio común   | 3 a 4                      |
| Vidrio con malla metálica | 6 a 10                     |
| Partición de madera       | 5 a 6                      |
| Ladrillo / bloque         | 6 a 10                     |
| Concreto armado           | 10 a 15                    |
| Lámina o panel metálico   | 12 a 35                    |

Adicionalmente, el fenómeno de **propagación multitrayecto** (*multipath*) ocurre cuando la señal llega al receptor por múltiples rutas —reflexión, difracción y dispersión— con distintos retardos de fase. Esto puede causar tanto interferencia constructiva (incremento de señal) como destructiva (*null*), produciendo zonas de señal nula incluso en áreas con aparente buena cobertura. La norma 802.11n y versiones posteriores mitigan este efecto mediante tecnología MIMO (*Multiple Input Multiple Output*).

Fuente: CWNA-107, Cap. 3 — *RF Signal Characteristics* y Cap. 4 — *Radio Frequency Components, Measurements, and Mathematics*.

### 4.1.2 Métricas de medición de cobertura Wi-Fi

La calidad de la señal Wi-Fi se cuantifica mediante dos métricas complementarias: el nivel de señal recibida y la relación señal a ruido.

**RSSI y dBm.** El indicador **RSSI** (*Received Signal Strength Indicator*) es, técnicamente, una escala propietaria de cada fabricante de chips Wi-Fi (típicamente de 0 a 255 o de 0 a 127) y no tiene unidades estandarizadas entre vendors. Para garantizar comparabilidad entre dispositivos, el valor de referencia universal en la industria es el nivel de señal expresado en **dBm** (decibelios relativos a 1 milivatio), que sí es una magnitud física absoluta. El CWNA-107 establece que toda herramienta de *site survey* profesional debe reportar el nivel de señal en dBm, no en unidades RSSI propietarias. Wireless HeatMapper adopta este criterio: almacena y visualiza únicamente valores en dBm.

Los umbrales de referencia para la clasificación de la cobertura, basados en la Tabla 13.1 del CWNA-107, son:

**Tabla 2.** Clasificación de calidad de señal Wi-Fi por nivel de señal (fuente: CWNA-107, Cap. 13, Tabla 13.1)

| Nivel de señal  | Clasificación            | Aplicaciones sostenibles                        |
| --------------- | ------------------------ | ----------------------------------------------- |
| −30 dBm         | Excepcional              | Máxima tasa de transferencia (MCS máximo)       |
| −55 dBm         | Muy buena                | Datos, voz y video sin restricción              |
| −65 dBm         | Excelente                | VoIP y aplicaciones de tiempo real              |
| −70 dBm         | Buena (objetivo diseño)  | Límite recomendado para nuevas instalaciones    |
| −71 a −80 dBm   | Aceptable con limitación | Solo datos básicos; tasa reducida por DRS       |
| −81 a −89 dBm   | Débil                    | Conexión marginal; alta probabilidad de errores |
| menor a −90 dBm | Zona muerta              | Sin conectividad funcional                      |

El fenómeno **DRS** (*Dynamic Rate Switching*) es directamente responsable de los problemas de rendimiento en zonas de señal débil: cuando el nivel de señal cae por debajo de los umbrales superiores de la tabla, el estándar 802.11 reduce automáticamente la tasa de modulación (MCS) para mantener la asociación, lo que puede degradar el throughput de cientos de Mbps a menos de 6 Mbps sin que el usuario lo perciba como una desconexión. El umbral de −70 dBm como objetivo de diseño no es arbitrario: garantiza un margen de desvanecimiento (*fade margin*) suficiente para mantener tasas de transferencia aceptables ante variaciones de señal debidas al movimiento de personas y objetos.

**SNR e interferencia.** La **relación señal a ruido** (SNR, *Signal-to-Noise Ratio*) es igualmente crítica: expresa, en dB, la diferencia entre el nivel de señal útil y el piso de ruido del ambiente. El CWNA-107 establece los siguientes requisitos mínimos de SNR para aplicaciones en entornos empresariales:

- Datos generales: SNR mayor o igual a 20 dB.
- Aplicaciones de voz (VoIP): SNR mayor o igual a 25 dB.
- SNR menor o igual a 10 dB: muy malo, conexión poco confiable.

En entornos con densidad alta de puntos de acceso coexisten dos tipos de interferencia. La **interferencia de canal adyacente** (ACI, *Adjacent Channel Interference*) ocurre cuando dos celdas vecinas operan en canales solapados en frecuencia (por ejemplo, canales 1 y 3 en la banda 2.4 GHz), produciendo corrupción de tramas a nivel de capa 2. La **interferencia de canal co-ubicado** (CCI, *Co-Channel Interference*) ocurre cuando varios puntos de acceso comparten el mismo canal y se escuchan mutuamente, reduciendo la eficiencia del medio al multiplicar los tiempos de diferimiento CSMA/CA. Para la banda 2.4 GHz, el CWNA-107 establece que únicamente los canales 1, 6 y 11 son no solapados, y su uso sistemático es el patrón mínimo requerido para evitar ACI.

Fuente: CWNA-107, Cap. 4 — *RF Components, Measurements, and Mathematics*; Cap. 13 — *WLAN Design Concepts*.

### 4.1.3 Metodología de site survey

Un **levantamiento de sitio** (*site survey*) es el proceso formal mediante el cual un ingeniero de redes inalámbricas caracteriza las condiciones RF de un espacio antes, durante o después de desplegar una WLAN. El CWNA-107 describe el método moderno predominante en la industria como **método híbrido**, compuesto de cuatro fases:

1. **Visita inicial al sitio** (*Initial Site Visit*): reconocimiento físico con planos de planta en mano, documentación fotográfica de la estructura y toma de nota de materiales de construcción, obstáculos y restricciones de montaje.

2. **Análisis de espectro** (*Spectrum Analysis*): medición de las fuentes de interferencia no Wi-Fi presentes en las bandas 2.4 GHz y 5 GHz. El CWNA-107 establece que si el ruido de fondo supera −85 dBm en cualquier banda, el rendimiento de la WLAN se degrada severamente.

3. **Medición de atenuación de materiales** (*Attenuation Spot Checks*): cuantificación empírica de la pérdida de señal a través de cada tipo de pared del edificio, para alimentar el modelo predictivo de cobertura con valores reales en lugar de valores predeterminados.

4. **Diseño predictivo** (*Predictive Design*): uso de software especializado para modelar la distribución de cobertura sobre el plano digital, iterando la ubicación y potencia de los puntos de acceso hasta cumplir los umbrales de diseño (primario: −65 dBm; secundario: −70 dBm).

El resultado del proceso es un reporte formal que incluye: análisis de espectro, mapa de calor de cobertura (*heatmap*), plano de ubicación de puntos de acceso con canales y potencias asignadas, análisis de capacidad y throughput, y listado de materiales. Wireless HeatMapper aborda precisamente la automatización de la fase de recolección de datos de campo y la generación de este reporte para entornos donde las herramientas comerciales (como Ekahau Site Survey, con costo de licencia superior a USD 3,000) resultan prohibitivas.

La **validación post-instalación** (*Validation Survey*) es otra fase documentada por el CWNA-107 frecuentemente omitida en instalaciones pequeñas: consiste en caminar todo el espacio instalado midiendo cobertura real y comparándola con el diseño previsto, antes de poner la red en servicio. Las métricas a validar incluyen: nivel de señal (dBm), SNR, pérdida de paquetes IP y retransmisiones de capa 2 (objetivo: menor al 5% para datos, menor al 2% para VoIP).

Fuente: CWNA-107, Cap. 14 — *Site Survey and Validation*.

### 4.1.4 Restricciones de plataforma móvil Android

En dispositivos Android 8.0 (Oreo) o posterior, el sistema operativo impone un límite de *throttling* en el escaneo de redes inalámbricas en segundo plano: el sistema permite como máximo 4 escaneos cada 2 minutos cuando la aplicación no está en primer plano. Esta restricción fue introducida por Google para reducir el consumo de batería y tiene implicaciones directas sobre la densidad de muestras que una aplicación de levantamiento de cobertura puede obtener. El diseño de Wireless HeatMapper debe compensar esta limitación mediante una experiencia de usuario orientada a mantener la aplicación activa en primer plano durante todo el proceso de levantamiento, además de implementar un indicador visual de frecuencia de escaneo efectiva.

Fuente: CWNA-107, Cap. 3 — *RF Signal Characteristics*, sección sobre comportamiento de cliente Android; documentación Android Developers API 26+.

### 4.1.5 Sistemas de información geoespacial y algoritmos de interpolación

El levantamiento de cobertura Wi-Fi es, en esencia, una actividad de recolección de datos geoespaciales: cada medición de señal (en dBm) se asocia a una coordenada dentro de un espacio físico representado sobre un plano de planta. A partir de un conjunto discreto de muestras, los algoritmos de interpolación espacial permiten construir una superficie continua de valores, que es lo que se visualiza como mapa de calor.

Los dos algoritmos más utilizados en el contexto de heatmapping Wi-Fi son:

- **IDW** (*Inverse Distance Weighting* — Ponderación por distancia inversa): asigna a cada punto sin medición un valor calculado como promedio ponderado de las muestras vecinas, donde el peso de cada muestra es inversamente proporcional a la distancia. Es el algoritmo más común por su simplicidad computacional.

- **Kriging**: método geoestadístico que modela la correlación espacial entre muestras mediante un variograma. Produce estimaciones de mayor fidelidad en entornos con variación espacial estructurada, pero a mayor costo computacional.

En el caso específico de señales Wi-Fi, la propagación RF no es isótropa (no decrece uniformemente con la distancia) debido a la atenuación por materiales. Para compensar esto, el módulo de inteligencia artificial puede incorporar modelos de propagación basados en la ecuación FSPL con factores de atenuación calibrados por tipo de material, generando así una interpolación físicamente informada que supera la calidad de IDW puro.

---

## 4.2 Comparación de Software Similar

A continuación se analizan tres proyectos de código abierto con funcionalidades similares a las que aborda Wireless HeatMapper:

---

### 4.2.1 WiFi Analyzer

- **Repositorio:** [github.com/VREMSoftwareDevelopment/WiFiAnalyzer](https://github.com/VREMSoftwareDevelopment/WiFiAnalyzer)
- **Plataforma:** Android (aplicación móvil nativa)
- **Descripción:** Aplicación de análisis de redes Wi-Fi en tiempo real. Permite visualizar canales, intensidad de señal y puntos de acceso cercanos mediante gráficos dinámicos.
- **Aspectos relevantes:**
  - Visualización en tiempo real de señal (RSSI) por red
  - Análisis de canales para detectar interferencias
  - Interfaz simple y accesible para usuarios técnicos
  - No genera mapas de calor ni permite levantamientos georreferenciados
  - No tiene componente web ni backend centralizado
- **Limitación frente a Wireless HeatMapper:** Opera exclusivamente en modo local y no persiste datos entre sesiones ni permite analizar la distribución espacial de la cobertura.

![Interfaz de WiFi Analyzer — análisis de canales y señal en tiempo real sobre Android](img/WIFIAnalyzer.png)

_Figura 1. Interfaz de WiFi Analyzer — visualización de intensidad de señal y canales Wi-Fi en dispositivo Android._

---

### 4.2.2 WiFi Surveyor

- **Repositorio:** [github.com/ecoAPM/WiFiSurveyor](https://github.com/ecoAPM/WiFiSurveyor)
- **Plataforma:** Multiplataforma (Linux/macOS/Windows)
- **Descripción:** Herramienta de escritorio para realizar levantamientos básicos de cobertura Wi-Fi con visualización de señal en tiempo real sobre un mapa de planta.
- **Aspectos relevantes:**
  - Permite importar un plano de planta como imagen de fondo
  - Registro manual de mediciones sobre el plano
  - Generación de mapas de calor básicos
  - No tiene aplicación móvil para levantamiento en campo
  - Sin backend centralizado ni módulo de análisis inteligente
- **Limitación frente a Wireless HeatMapper:** El levantamiento es manual y no existe integración con análisis automatizado ni acceso multiusuario a través de una plataforma web.

![Interfaz de WiFi Surveyor — levantamiento de cobertura sobre plano de planta](img/wifisurveyor.png)

_Figura 2. Interfaz de WiFi Surveyor — registro de mediciones sobre plano de planta en entorno de escritorio._

---

### 4.2.3 python-wifi-survey-heatmap

- **Repositorio:** [github.com/jantman/python-wifi-survey-heatmap](https://github.com/jantman/python-wifi-survey-heatmap)
- **Plataforma:** Linux (línea de comandos + interfaz gráfica básica)
- **Descripción:** Script Python para ejecutar un *site survey* Wi-Fi interactivo sobre un plano de planta, generando un mapa de calor de RSSI, velocidad de transmisión y otros parámetros.
- **Aspectos relevantes:**
  - Genera mapas de calor con múltiples métricas (RSSI, TX rate, calidad)
  - Visualización inmediata con matplotlib
  - Requiere conocimiento técnico para instalación y uso
  - Sin aplicación móvil; el levantamiento se hace con laptop en campo
  - Sin persistencia en base de datos ni historial de proyectos
  - Sin interfaz web ni módulo de IA
- **Limitación frente a Wireless HeatMapper:** Es una herramienta para usuarios altamente técnicos, orientada a uso puntual. No permite gestión de proyectos, acceso remoto ni análisis inteligente de resultados.

![Interfaz de python-wifi-survey-heatmap — mapa de calor generado con matplotlib en Linux](img/python-wifi-survey-heatmap.png)

_Figura 3. Interfaz de python-wifi-survey-heatmap — generación de mapa de calor de cobertura Wi-Fi sobre plano digital._

---

### Resumen comparativo

**Tabla 3.** Comparación de características entre herramientas de heatmapping existentes y Wireless HeatMapper

| Característica                        | WiFi Analyzer | WiFi Surveyor | python-wifi-survey | **Wireless HeatMapper** |
| ------------------------------------- | :-----------: | :-----------: | :----------------: | :---------------------: |
| Aplicación móvil Android              |      Sí       |      No       |        No          |           Sí            |
| Panel web de administración           |      No       |      No       |        No          |           Sí            |
| Backend centralizado con BD           |      No       |      No       |        No          |           Sí            |
| Generación de mapa de calor           |      No       |      Sí       |        Sí          |           Sí            |
| Levantamiento georreferenciado        |      No       |      Sí       |        Sí          |           Sí            |
| Análisis con Inteligencia Artificial  |      No       |      No       |        No          |           Sí            |
| Gestión de proyectos y clientes       |      No       |      No       |        No          |           Sí            |
| Multiusuario y acceso remoto          |      No       |      No       |        No          |           Sí            |


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 5. Descripción del Problema

## 5.1 Narrativa del Problema

Bulldog Tech. es una empresa tecnológica con sede en Santa Cruz de la Sierra, Bolivia, con experiencia consolidada en servicios de soporte técnico, mantenimiento de equipos y consultoría en sistemas de información. Hace aproximadamente un año, la empresa amplió su operación incorporando el área de infraestructura tecnológica de telecomunicaciones, orientada a la instalación, configuración y mantenimiento de redes de datos inalámbricas para clientes corporativos y pymes de la región.

En esta área, Bulldog Tech. aplica el proceso tradicional del sector: el técnico especializado visita las instalaciones del cliente, evalúa el espacio y determina la ubicación de los puntos de acceso (APs) a partir de su criterio y experiencia directa. Es el técnico quien, durante esa visita presencial, aporta el mayor valor para las decisiones de diseño de la red: cuántos APs instalar, dónde colocarlos y cómo configurarlos. El proyecto avanza desde esa evaluación subjetiva como único insumo técnico documentado.

Ese modelo funciona en instalaciones simples, pero presenta limitaciones estructurales conforme la empresa asume proyectos de mayor envergadura. La principal es que el proceso no genera evidencia objetiva: no se miden niveles de señal por zona, no se documenta la cobertura real alcanzada y no se deja una línea base que permita comparar el estado de la red antes y después de una intervención. La metodología profesional de *site survey*, documentada en el estándar de la industria CWNA-107, establece que el umbral mínimo de calidad de señal aceptable para una instalación nueva es de −70 dBm, y que cualquier zona con señal inferior a −90 dBm constituye una zona muerta donde la conectividad funcional no puede garantizarse. Sin instrumentos de medición, no existe forma de verificar si estos umbrales se cumplen en el trabajo que la empresa entrega a sus clientes.

Las consecuencias se manifiestan tanto hacia adentro como hacia los proyectos del cliente. En las instalaciones propias de Bulldog Tech., los técnicos reportan cortes intermitentes en el área de taller, el personal administrativo trabaja con velocidades insuficientes y los clientes que esperan en recepción perciben una señal débil. Ante cada reporte de falla, el diagnóstico es informal: se visita el lugar, se reinicia el equipo, se revisan cables, sin registro escrito, sin identificación de causa raíz y sin garantía de que el problema no reaparezca. En los proyectos de clientes, la empresa no puede demostrar objetivamente que la red entregada cumple con los parámetros técnicos acordados, lo que representa un riesgo creciente a medida que la cartera de clientes se expande.

La ausencia de una herramienta de levantamiento formal impide tomar decisiones basadas en datos para la reubicación o ampliación de puntos de acceso, y hace que el conocimiento técnico sobre cada instalación permanezca en la memoria del técnico que realizó la visita, sin sistematizarse. Este problema no es exclusivo de Bulldog Tech.: representa una limitación común en empresas que inician en el área de infraestructura de telecomunicaciones y no disponen del presupuesto para contratar herramientas comerciales de *site survey* (como Ekahau Site Survey o AirMagnet), cuyo costo de licencia puede superar los USD 3,000 anuales.

---

## 5.2 Diagrama Causa-Efecto (Ishikawa)

El siguiente diagrama identifica las causas raíz que originan la deficiente gestión de cobertura Wi-Fi en Bulldog Tech.:

![Diagrama 1](img/p1-01-ishikawa-causa-efecto!p1-01-ishikawa-causa-efecto_12.png)

_Figura 4. Diagrama de causa-efecto (Ishikawa) — Deficiente gestión de cobertura Wi-Fi en Bulldog Tech._

---

## 5.3 Modelo de Dominio

El modelo de dominio representa los conceptos clave del negocio involucrados en el problema. Cada clase es un concepto puro del negocio, no una tabla ni una clase de código:

![Modelo de Dominio — Wireless HeatMapper](img/p1-02-modelo-dominio!p1-02-modelo-dominio_13.png)

_Figura 5. Modelo de dominio — conceptos clave del problema de cobertura Wi-Fi en Bulldog Tech._


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 6. Situación Problemática

Desde que Bulldog Tech. incorporó el área de infraestructura de telecomunicaciones, hace aproximadamente un año, los proyectos de instalación de redes inalámbricas se han ejecutado siguiendo un proceso tradicional: el técnico asignado visita las instalaciones del cliente, recorre los espacios, identifica los ambientes a cubrir y determina, a partir de su experiencia y criterio profesional, cuántos puntos de acceso instalar y dónde ubicarlos. En ese modelo, el técnico es la fuente principal de información para la toma de decisiones. Lo que él observa durante la visita es, en la práctica, el único insumo técnico que sustenta el diseño de la red.

Este enfoque funciona dentro de ciertos límites. Para instalaciones pequeñas y simples, el juicio del técnico experimentado es suficiente para lograr una cobertura aceptable. Sin embargo, a medida que los proyectos crecen en tamaño y complejidad, la evaluación subjetiva empieza a mostrar sus restricciones: no permite cuantificar la calidad de la señal por zona, no genera documentación que respalde las decisiones tomadas, no deja un registro que sirva como línea base para comparar el estado antes y después de una intervención, y no es transferible si el técnico que realizó la visita no está disponible para el seguimiento del proyecto.

El resultado de ese proceso, aplicado también a la infraestructura propia de Bulldog Tech., es una red Wi-Fi que funciona de forma general, pero sin que nadie pueda afirmar con certeza qué zonas tienen cobertura suficiente, cuáles presentan degradación de señal y dónde existen puntos ciegos. Las consecuencias se perciben en el día a día: cortes intermitentes en el área de taller, velocidades insuficientes en administración y señal débil en recepción. Ante cada reporte de falla, la respuesta es reactiva: se visita el lugar, se reinicia el equipo, se revisa el cableado, sin dejar registro escrito ni identificar la causa raíz, lo que hace que los mismos problemas reaparezcan semanas después.

La empresa carece de métricas objetivas de cobertura, de un historial de mediciones y de criterios técnicos documentados para fundamentar decisiones de mejora. Las inversiones en infraestructura de red se aplican sin sustento verificable, con resultados que no se pueden demostrar objetivamente ni a la gerencia ni a los clientes.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 7. Situación Deseada

Con Wireless HeatMapper implementado, Bulldog Tech. tendrá la capacidad de complementar el criterio técnico del especialista con datos de señal medidos objetivamente en campo. El técnico que realiza la visita al cliente seguirá siendo quien aporta el juicio profesional sobre el diseño de la red, pero contará con un instrumento que le permite respaldar sus decisiones: medirá los niveles de señal por zona sobre el plano real de las instalaciones, identificará con precisión los puntos ciegos y las zonas de cobertura degradada, y producirá un mapa de calor que documenta el estado de la red en el momento del levantamiento.

Para cada proyecto, el sistema generará un historial de mediciones que permite comparar el estado antes y después de cada intervención técnica. El módulo de inteligencia artificial analizará los datos recolectados y producirá recomendaciones de reposicionamiento de puntos de acceso fundamentadas en los umbrales de cobertura establecidos por el estándar CWNA-107. Los reportes generados automáticamente podrán ser entregados al cliente como parte del servicio, lo que fortalece la propuesta de valor de la empresa frente a instaladores que operan únicamente con criterio empírico.

El resultado más significativo es la formalización del proceso. El conocimiento que hoy reside exclusivamente en la experiencia del técnico quedará sistematizado en el historial de cada proyecto: qué se midió, cuándo, dónde y con qué resultado. Eso no solo reduce la dependencia de personas específicas, sino que permite a Bulldog Tech. crecer en el área de infraestructura de telecomunicaciones con un proceso técnico documentado, reproducible y verificable, apropiado para la envergadura de los proyectos que la empresa busca asumir.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 8. Objetivos

## 8.1 Objetivo General

Desarrollar un sistema integrado de levantamiento y visualización de cobertura Wi-Fi, compuesto por una aplicación móvil Android, un backend REST con módulo de inteligencia artificial y una plataforma web de administración, que permita a Bulldog Tech. diagnosticar, documentar y optimizar la distribución de su red inalámbrica mediante mapas de calor georreferenciados y análisis automatizado.

---

## 8.2 Objetivos Específicos

1. **Diseñar e implementar el backend REST** con FastAPI y PostgreSQL que gestione la autenticación de usuarios, la administración de clientes y proyectos, y el almacenamiento centralizado de mediciones Wi-Fi.
   - *Entregable:* API REST funcional con endpoints documentados y base de datos relacional normalizada.

2. **Desarrollar la aplicación móvil Android** con Flutter que permita al técnico autenticarse, seleccionar un proyecto, y recolectar mediciones de RSSI georreferenciadas sobre el plano de planta de la instalación.
   - *Entregable:* Aplicación Flutter con módulos de autenticación y levantamiento de señal operativos.

3. **Construir el panel web de administración** con React y TypeScript que permita gestionar usuarios, clientes, proyectos y visualizar los mapas de calor generados.
   - *Entregable:* Aplicación web funcional con autenticación, CRUD de entidades principales y visualización de resultados.

4. **Integrar un módulo de inteligencia artificial** en el backend capaz de analizar los datos de cobertura recolectados y generar recomendaciones de optimización de la red.
   - *Entregable:* Módulo de IA con al menos un modelo de análisis validado y endpoint de recomendaciones funcional.

5. **Definir y documentar la arquitectura de despliegue** del sistema mediante Docker Compose y GitHub Actions, garantizando la reproducibilidad del entorno en producción.
   - *Entregable:* Archivo `docker-compose.yml` funcional con todos los servicios orquestados y pipeline de CI/CD configurado.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 9. Alcance

El sistema Wireless HeatMapper abarca las siguientes funcionalidades organizadas por módulos:

---

## 9.1 Módulo de Autenticación y Usuarios

Gestiona el acceso seguro al sistema para todos los perfiles de usuario. Incluye:

- Registro e inicio de sesión con autenticación JWT.
- Gestión de roles: Administrador, Técnico y Cliente.
- Recuperación de contraseña y gestión de perfil.
- Control de sesiones activas y cierre de sesión seguro.

---

## 9.2 Módulo de Gestión de Clientes y Proyectos

Permite la administración completa de los clientes (empresas) y sus proyectos de levantamiento Wi-Fi. Incluye:

- Alta, edición y desactivación de clientes (organizaciones).
- Creación y gestión de proyectos de levantamiento por instalación.
- Carga y administración del plano de planta de cada instalación.
- Asignación de técnicos a proyectos.
- Listado, filtrado y seguimiento del estado de proyectos.

---

## 9.3 Módulo de Levantamiento Wi-Fi (App Móvil)

Ejecutado desde la aplicación Android Flutter, permite al técnico recolectar datos de señal en campo. Incluye:

- Visualización del plano de planta del proyecto activo.
- Marcación de puntos de medición sobre el plano con posicionamiento táctil.
- Captura automática de valores RSSI, SSID, BSSID, frecuencia y canal de todas las redes detectadas en cada punto.
- Indicador visual del nivel de cobertura por punto medido.
- Envío inmediato de mediciones al backend (modalidad 100% en línea, sin almacenamiento local).
- Control de throttling Android (máx. 4 escaneos / 2 min en Android 8.0+).

---

## 9.4 Módulo de Generación de Heatmap

Procesa las mediciones recolectadas y genera la visualización de cobertura. Incluye:

- Interpolación de valores RSSI sobre el plano usando algoritmo IDW (*Inverse Distance Weighting*).
- Generación de mapa de calor con escala de colores por umbral (excelente, buena, aceptable, débil, zona muerta).
- Exportación del mapa de calor como imagen PNG y como reporte PDF.
- Historial de mapas por proyecto para comparativa temporal.

---

## 9.5 Módulo de Análisis con Inteligencia Artificial

Procesa los datos de cobertura y genera recomendaciones automatizadas. Incluye:

- Identificación de zonas muertas (RSSI ≤ −90 dBm) y zonas con cobertura insuficiente.
- Detección de solapamiento excesivo de canales entre APs.
- Generación de recomendaciones textuales: reubicación de APs, cambio de canal, potencia de transmisión.
- Puntaje global de calidad de cobertura por instalación.

---

## 9.6 Panel de Administración Web

Interfaz web accesible desde navegador para administradores y clientes. Incluye:

- Dashboard con resumen de proyectos activos y alertas de cobertura.
- CRUD completo de usuarios, clientes y proyectos.
- Visualización de mapas de calor y descarga de reportes.
- Historial de levantamientos y comparativa de evolución de cobertura.
- Gestión de configuración del sistema.

---

## Requerimientos fuera del alcance

Los siguientes aspectos quedan **explícitamente fuera del alcance** del proyecto:

- Soporte para tecnologías de red distintas a Wi-Fi (Bluetooth, LTE, Ethernet).
- Posicionamiento en interiores con GPS o trilateración (el posicionamiento es manual sobre plano).
- Módulo de facturación o cobro de servicios.
- Integración con sistemas ERP o CRM externos.
- Modo offline en la aplicación móvil (toda la persistencia ocurre en el backend).


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 10. Tecnología de Desarrollo

## 10.1 Stack Tecnológico

### Backend

**Tabla 11a.** Stack tecnológico — Backend

| Tecnología        | Uso                                           | Justificación                                                                                                                                                    |
| ----------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Python 3.11+**  | Lenguaje principal del backend                | Ecosistema maduro para ciencia de datos e IA; sintaxis clara; amplia disponibilidad de bibliotecas para procesamiento de señales y machine learning.              |
| **FastAPI**       | Framework REST API                            | Alto rendimiento (basado en Starlette/ASGI), validación automática con Pydantic, generación de documentación OpenAPI integrada y soporte nativo para async/await. |
| **PostgreSQL 15+**| Base de datos relacional central              | Motor robusto, open source, soporte de tipos espaciales (PostGIS para coordenadas), transacciones ACID y excelente integración con SQLAlchemy.                    |
| **SQLAlchemy**    | ORM y acceso a datos                          | Permite un control preciso del esquema y las consultas; facilita la migración con Alembic y desacopla el modelo de dominio del motor de BD.                       |
| **Alembic**       | Migraciones de base de datos                  | Control de versiones del esquema de base de datos alineado con el ciclo de desarrollo incremental de Scrum.                                                       |

### Aplicación Móvil

| Tecnología          | Uso                                           | Justificación                                                                                                                                               |
| ------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Flutter / Dart**  | App Android (cliente REST en línea)           | Un solo código base para múltiples plataformas, widgets Material 3, rendimiento nativo. Elimina la necesidad de BD local (modalidad 100% en línea).          |
| **BLoC / Cubit**    | Gestión de estado                             | Patrón declarativo, testeable y predecible; separa presentación de lógica de negocio conforme a la arquitectura por capas del proyecto.                     |
| **Dio**             | Cliente HTTP                                  | Interceptores de autenticación JWT, manejo de errores centralizado y soporte para *multipart* (carga de planos e imágenes).                                  |

### Frontend Web

| Tecnología              | Uso                                           | Justificación                                                                                                                                              |
| ----------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **React 18 + TypeScript** | Panel de administración web                 | Ecosistema maduro, tipado estático que reduce errores en tiempo de desarrollo, componentes reutilizables y amplio soporte de la comunidad.                  |
| **Vite**                | Bundler y servidor de desarrollo              | Compilación rápida en desarrollo, Hot Module Replacement eficiente, configuración mínima.                                                                  |
| **TanStack Query**      | Gestión de estado del servidor                | Caché automática, sincronización con el backend y manejo declarativo de estados de carga y error.                                                          |

### Infraestructura y Despliegue

| Tecnología           | Uso                                           | Justificación                                                                                                                                                  |
| -------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Docker Compose**   | Orquestación de servicios en local/producción | Reproducibilidad del entorno; todos los servicios (backend, BD, frontend, Nginx) se levantan con un único comando.                                             |
| **Nginx**            | Reverse proxy                                 | Gestión centralizada de rutas HTTP/HTTPS; separa el tráfico de la API del frontend estático.                                                                   |
| **GitHub Actions**   | CI/CD                                         | Integrado con el repositorio; automatiza linting, pruebas, construcción de imágenes Docker y despliegue al entorno de producción en cada merge a `main`.       |

### Herramientas CASE y Desarrollo Colaborativo

| Herramienta       | Uso                                                    |
| ----------------- | ------------------------------------------------------ |
| **StarUML**       | Modelado UML 2.5+: casos de uso, clases, secuencia, despliegue, paquetes |
| **PlantUML**      | Diagramas embebidos en documentación Markdown           |
| **GitHub**        | Control de versiones, gestión de issues y pull requests |
| **VS Code**       | IDE principal con extensiones para Flutter, Python y TypeScript |

---

## 10.2 Proceso de Desarrollo

El proyecto adopta **Scrum** como marco de trabajo ágil, combinando su ciclo iterativo e incremental con las cuatro actividades fundamentales de ingeniería de software: análisis, diseño, implementación y pruebas. Estas actividades se ejecutan dentro de cada sprint, lo que permite un desarrollo continuo con entregas verificables al final de cada iteración.

### Estructura del proceso

```
Sprint 0 (Inicio)
├── Organización del equipo (roles Scrum)
├── Ingeniería de Requisitos inicial (conversación con el cliente)
└── Modelos iniciales: contexto, arquitectura, datos → Product Backlog

Sprint N (1, 2, 3...)
├── Planificación del Sprint
│   ├── Selección de HU del Product Backlog
│   ├── Análisis: Las 3 C's (Cards, Conversación, Confirmación)
│   └── Sprint Backlog (tareas de granularidad mínima)
│
├── Ejecución del Sprint
│   ├── Diseño: arquitectura, datos, lógica, interfaces
│   ├── Implementación: código con estándar y refactoring
│   └── Pruebas: unitarias (dev), calidad (QA), aceptación (PO)
│
└── Revisión del Sprint
    ├── Demostración del incremento operativo al cliente
    └── Actualización del Product Backlog
```

### Roles del equipo

| Rol              | Integrante                         | Responsabilidad principal                                   |
| ---------------- | ---------------------------------- | ----------------------------------------------------------- |
| Scrum Master     | Fernandez Ortega Jhasmany Jhunnior | Facilitar el proceso Scrum; remover impedimentos             |
| Product Owner    | Quiroga Flores Herland Borys       | Gestionar el Product Backlog; representar al cliente         |
| Desarrolladores  | Ambos integrantes                  | Diseño, implementación y pruebas (equipo multifuncional)    |

### Duración de sprints

| Sprint          | Duración          | Fechas                        |
| --------------- | ----------------- | ----------------------------- |
| Sprint 0        | 1 semana (5 días) | 13 abr 2026 → 17 abr 2026    |
| Sprint 1        | 1 semana (5 días) | 20 abr 2026 → 24 abr 2026    |
| Sprint 2 al 6   | 2 semanas (14 días) | A partir del 27 abr 2026    |
| Cierre          | 1 semana (5 días) | Al finalizar Sprint 6         |

> **M0 — Presentación conjunta Sprint 0 + Sprint 1:** 27 de abril de 2026.

### Incremento

Cada sprint debe generar una **versión operativa de software** que aporte valor real al cliente. Las historias de usuario se consideran completas únicamente cuando pasan los tres filtros de prueba: unitarias (desarrollador), calidad (QA) y aceptación (Product Owner).

### Plan de Sprints — Gantt

![Plan general de Sprints — Wireless HeatMapper (modalidad 100 % en línea)](img/01-plan-general-sprints.png)

_Figura 15. Diagrama de Gantt — Cronograma de sprints del proyecto Wireless HeatMapper (abril–julio 2026)._

### Objetivos por Sprint

**Tabla 12.** Objetivos e hitos verificables por sprint

| Sprint   | Objetivo                                                                                                    | Hito verificable                                                |
| -------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Sprint 0 | Backend "hello world" con Docker Compose, PostgreSQL, CI/CD y modelos UML aprobados                        | `curl /api/health` → 200 OK                                     |
| Sprint 1 | Admin crea técnicos y clientes en panel web; técnico inicia sesión en app y gestiona proyectos             | Crear usuario/cliente en web → login en app → CRUD proyectos    |
| Sprint 2 | Técnico sube plano PNG/PDF y lo calibra sobre un proyecto; persiste en PostgreSQL                           | Recorrido completo plano + calibración                          |
| Sprint 3 | Técnico marca puntos sobre el plano y captura mediciones Wi-Fi persistidas en línea                        | Demo en vivo captura → BD muestra registros                     |
| Sprint 4 | Técnico solicita heatmap al backend y ve análisis automático (zonas muertas, CCI/ACI); el sistema aplica los umbrales CWNA-107 (−70 dBm objetivo, −90 dBm zona muerta) para clasificar las zonas | Heatmap renderizado + panel de análisis con clasificación por zonas                         |
| Sprint 5 | Técnico recibe recomendaciones de IA, compara escenarios y exporta reporte PDF                              | Recomendaciones IA + comparación + PDF descargable              |
| Sprint 6 | Técnico genera enlace; cliente lo abre en navegador y ve heatmap, análisis y plan AP                       | Portal de cliente con token real funcionando                    |



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 11. Bibliografía

Las siguientes referencias sustentan el desarrollo técnico y metodológico del proyecto Wireless HeatMapper, presentadas en formato APA 7.ª edición.

---

## Referencias

Coleman, D., Westcott, D. A., Harkins, B., & Jackman, S. (2021). *CWNA: Certified Wireless Network Administrator study guide (Examen CWNA-107)* (5.ª ed.). Sybex / Wiley.

Schwaber, K., & Sutherland, J. (2020). *La Guía Definitiva de Scrum: Las Reglas del Juego*. Scrum.org. https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-Spanish-Latin-South-American.pdf

IEEE. (2016). *IEEE Standard for Information Technology — Telecommunications and information exchange between systems — Local and metropolitan area networks — Specific requirements — Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications (IEEE Std 802.11-2016)*. Institute of Electrical and Electronics Engineers.

FastAPI. (2024). *FastAPI — Documentación oficial*. Tiangolo. https://fastapi.tiangolo.com/

Flutter. (2024). *Flutter — Documentación oficial*. Google. https://docs.flutter.dev/

PostgreSQL Global Development Group. (2024). *PostgreSQL 15 Documentation*. https://www.postgresql.org/docs/15/

VREM Software Development. (2024). *WiFi Analyzer* [Software de código abierto]. GitHub. https://github.com/VREMSoftwareDevelopment/WiFiAnalyzer

ecoAPM. (2023). *WiFi Surveyor* [Software de código abierto]. GitHub. https://github.com/ecoAPM/WiFiSurveyor

Antman, J. (2023). *python-wifi-survey-heatmap* [Software de código abierto]. GitHub. https://github.com/jantman/python-wifi-survey-heatmap

Object Management Group. (2017). *OMG® Unified Modeling Language® (OMG UML®) Version 2.5.1*. https://www.omg.org/spec/UML/2.5.1/

React. (2024). *React — Documentación oficial*. Meta Open Source. https://react.dev/

Docker Inc. (2024). *Docker Compose — Documentación oficial*. https://docs.docker.com/compose/


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 12. Anexos

## 12.1 Esquema Gráfico: Situación Actual vs. Situación Deseada

El siguiente diagrama ilustra el contraste entre el estado actual de gestión de cobertura Wi-Fi en Bulldog Tech. y el escenario que se alcanzará con la implementación de Wireless HeatMapper:

![Diagrama 3](img/p1-12-situacion-actual-deseada!p1-12-situacion-actual-deseada_14.png)

---

## 12.2 Datos del Caso de Estudio

| Campo               | Detalle                                                        |
| ------------------- | -------------------------------------------------------------- |
| **Empresa**         | Bulldog Tech.                                                  |
| **Rubro**           | Servicios tecnológicos: soporte, consultoría, redes           |
| **Ubicación**       | Santa Cruz de la Sierra, Bolivia                               |
| **Problemática**    | Deficiente gestión y diagnóstico de cobertura Wi-Fi interna    |
| **Áreas afectadas** | Taller técnico, área administrativa, sala de atención al cliente |
| **Necesidad clave** | Herramienta accesible de site survey y heatmapping Wi-Fi       |

---

## 12.3 Currículum Vitae de los Integrantes

### Fernandez Ortega Jhasmany Jhunnior

| Campo              | Detalle                                               |
| ------------------ | ----------------------------------------------------- |
| **Carrera**        | Ingeniería Informática — FICCT, UAGRM                |
| **Registro**       | 207025509                                             |
| **Rol en el proyecto** | Scrum Master / Desarrollador                      |
| **Áreas de enfoque** | Backend, infraestructura, DevOps                   |

---

### Quiroga Flores Herland Borys

| Campo              | Detalle                                               |
| ------------------ | ----------------------------------------------------- |
| **Carrera**        | Ingeniería Informática — FICCT, UAGRM                |
| **Registro**       | 200104373                                             |
| **Rol en el proyecto** | Product Owner / Desarrollador                    |
| **Áreas de enfoque** | Análisis de requisitos, frontend web, mobile       |

---

## Nota sobre la Carta de Formalización

La **Carta de Formalización** del acuerdo con el cliente Bulldog Tech. es un documento físico firmado que se adjunta de forma impresa al presente trabajo. Contiene el compromiso formal entre el equipo de desarrollo y el representante de Bulldog Tech. para la ejecución del proyecto Wireless HeatMapper bajo el marco de trabajo Scrum.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Sprint 0 — Organización del Equipo

## S0.1 Organización del Equipo Scrum

El Sprint 0 corresponde al momento de inicio del proyecto, previo al primer sprint de desarrollo. En esta etapa se definió la estructura del equipo, se establecieron los canales de comunicación y se acordaron las herramientas de trabajo colaborativo.

**Duración:** 1 semana (5 días hábiles)
**Fecha de inicio:** 13 de abril de 2026
**Fecha de fin:** 17 de abril de 2026
**Hito al finalizar (M1):** Backend "hello world" con Docker Compose, PostgreSQL y CI/CD funcionando.

### Cronograma del Sprint 0

![Sprint 0 — Definición Inicial (R-1) — 13 abr – 17 abr 2026](img/02-sprint-0-detalle.png)

_Figura 23. Diagrama de Gantt — Planificación detallada del Sprint 0 (13–17 abr 2026)._

---

### Roles asignados

| Rol              | Integrante                           | Responsabilidades                                                                                                           |
| ---------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **Scrum Master** | Fernandez Ortega Jhasmany Jhunnior   | Facilitar los eventos Scrum, remover impedimentos, asegurar el cumplimiento del marco de trabajo, gestionar el tablero Kanban |
| **Product Owner**| Quiroga Flores Herland Borys         | Definir y priorizar el Product Backlog, interlocutor con el cliente (Bulldog Tech.), validar criterios de aceptación         |
| **Desarrolladores** | Ambos integrantes               | Diseño, implementación y pruebas; el equipo es multifuncional y autogestionado                                               |

---

### Herramientas de trabajo colaborativo

| Herramienta        | Propósito                                              |
| ------------------ | ------------------------------------------------------ |
| GitHub             | Control de versiones, gestión de issues y pull requests |
| GitHub Projects    | Tablero Kanban para seguimiento del Sprint Backlog      |
| VS Code + extensiones | IDE principal con Live Share para trabajo colaborativo |
| WhatsApp / Discord | Comunicación informal del equipo                        |
| StarUML            | Modelado UML 2.5+                                       |

---

### Acuerdo de trabajo

- **Frecuencia de Daily Scrum:** diaria (asincrónica por chat cuando no coinciden horarios).
- **Duración de sprints:** Sprint 0 = 1 semana (13–17 abr 2026); Sprint 1 = 1 semana (20–24 abr 2026); Sprint 2 en adelante = 2 semanas.
- **M0 — Presentación conjunta Sprint 0 + Sprint 1:** 27 de abril de 2026.
- **Estándar de commits:** mensajes en español, con prefijo de tipo (`feat:`, `fix:`, `docs:`, `test:`).
- **Definición de Hecho (DoD):** código revisado por el compañero, pruebas unitarias pasando, funcionalidad demostrable en entorno local.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Sprint 0 — Ingeniería de Requisitos

## S0.2 Ingeniería de Requisitos Inicial

Durante el Sprint 0 se realizó la sesión inicial de levantamiento de requisitos con el representante de Bulldog Tech. El Product Owner condujo la entrevista siguiendo las 3 C's: documentar las historias (Cards), conversar con el cliente para comprenderlas (Conversación) y confirmar la comprensión mediante ejemplos concretos (Confirmación).

---

### Técnicas utilizadas

- **Entrevista semiestructurada** con el cliente para identificar problemas operativos concretos.
- **Modelo de dominio preliminar** para alinear el vocabulario del negocio con el equipo.
- **Brainstorming interno** para identificar actores, funcionalidades y restricciones.

---

### Requerimientos Principales identificados (RP)

**Tabla 3.** Requerimientos principales del sistema Wireless HeatMapper

| ID    | Requerimiento Principal                                                                      | Prioridad |
| ----- | -------------------------------------------------------------------------------------------- | :-------: |
| RP1   | Gestión de usuarios y autenticación segura (JWT, roles)                                      | Alta      |
| RP2   | Gestión de clientes (organizaciones) por parte del administrador                             | Alta      |
| RP3   | Gestión de proyectos de levantamiento Wi-Fi                                                  | Alta      |
| RP4   | Levantamiento de señal Wi-Fi desde app móvil (recolección de mediciones RSSI)               | Alta      |
| RP5   | Generación de mapa de calor georreferenciado sobre plano de planta                           | Alta      |
| RP6   | Análisis con IA y generación de recomendaciones de optimización                              | Media     |
| RP7   | Panel web de administración y visualización de resultados                                    | Alta      |
| RP8   | Generación y exportación de reportes (PDF/PNG)                                               | Media     |
| RP9   | Gestión de planos de planta (carga y administración)                                         | Media     |

---

### Product Backlog inicial — Historias de Usuario (resumen)

**Tabla 4.** Product Backlog inicial — Historias de usuario priorizadas

| ID     | Historia de Usuario                                                   | PHU | Sprint |
| ------ | --------------------------------------------------------------------- | :-: | :----: |
| PB-01  | Como administrador, quiero gestionar usuarios del sistema             |  3  |   1    |
| PB-09  | Como administrador, quiero gestionar clientes (organizaciones)        |  5  |   1    |
| PB-10  | Como usuario, quiero autenticarme con correo y contraseña             |  3  |   1    |
| PB-13  | Como administrador, quiero gestionar proyectos de levantamiento       |  5  |   1    |
| PB-18  | Como administrador, quiero ver el listado de proyectos por cliente    |  3  |   1    |
| PB-19  | Como técnico, quiero autenticarme desde la app móvil                  |  3  |   1    |
| PB-02  | Como técnico, quiero seleccionar un proyecto y ver su plano           |  5  |   2    |
| PB-03  | Como técnico, quiero marcar puntos de medición sobre el plano         |  8  |   2    |
| PB-04  | Como técnico, quiero que se capture el RSSI automáticamente al marcar |  5  |   2    |
| PB-05  | Como sistema, quiero generar el heatmap a partir de las mediciones    |  8  |   2    |
| PB-06  | Como administrador, quiero ver el heatmap en el panel web             |  5  |   3    |
| PB-07  | Como sistema, quiero analizar la cobertura con IA                     | 13  |   3    |
| PB-08  | Como administrador, quiero exportar reportes en PDF                   |  5  |   3    |
| PB-11  | Como técnico, quiero gestionar planos de planta desde la app          |  5  |   2    |
| PB-12  | Como administrador, quiero gestionar planos desde el panel web        |  3  |   2    |
| PB-15  | Como cliente, quiero ver mis proyectos en el panel web                |  3  |   3    |
| PB-16  | Como sistema, quiero enviar notificaciones de alerta de cobertura     |  5  |   3    |
| PB-17  | Como administrador, quiero gestionar configuración del sistema        |  3  |   3    |

> **Nota:** PB-14 (sincronización offline) fue **eliminada** en la modalidad 100% en línea. Toda la persistencia ocurre en el backend.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Sprint 0 — Modelos Iniciales del Sistema

## S0.3 Modelos Iniciales

Como resultado de la ingeniería de requisitos del Sprint 0 se generaron los tres modelos iniciales que sirven como base para todos los sprints posteriores.

---

## S0.3.1 Modelo de Contexto — Diagrama de Casos de Uso

![Modelo de Contexto — Wireless HeatMapper (Sprint 0)](img/p1-s0-01-casos-uso!p1-s0-01-casos-uso_3.png)

_Figura 6. Modelo de contexto — Diagrama de casos de uso del sistema Wireless HeatMapper._

---

### Diagrama de Paquetes



_Figura 7. Diagrama de paquetes — Arquitectura por capas del sistema Wireless HeatMapper._

### Diagrama de Despliegue

![Diagrama de Despliegue — Wireless HeatMapper](img/p1-s0-03-despliegue!p1-s0-03-despliegue_4.png)

_Figura 8. Diagrama de despliegue — Infraestructura Docker del sistema Wireless HeatMapper._

---

## S0.3.3 Modelo de Datos Inicial — Conceptual



_Figura 9. Modelo conceptual de datos — Entidades principales del dominio de Wireless HeatMapper._


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

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


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Sprint 1 — Modelos Generados

## S1.2 Modelos del Sprint 1

---

## S1.2.1 Modelo de Contexto — Sprint 1

El diagrama de casos de uso muestra exclusivamente las funcionalidades abarcadas en el Sprint 1:

![Modelo de Contexto — Sprint 1 (Fundación)](img/p1-s1-01-casos-uso!p1-s1-01-casos-uso_8.png)

_Figura 10. Modelo de contexto actualizado al Sprint 1 — Casos de uso implementados en la primera iteración._

---

### Diagrama de Paquetes (Sprint 1)



_Figura 11. Diagrama de paquetes del Sprint 1 — Módulos implementados y sus dependencias._

### Diagrama de Despliegue (Sprint 1)

![Diagrama de Despliegue — Sprint 1](img/p1-s1-03-despliegue!p1-s1-03-despliegue_9.png)

_Figura 12. Diagrama de despliegue del Sprint 1 — Configuración Docker de los contenedores en producción._

---

### Modelo Conceptual

![Modelo Conceptual de Datos — Sprint 1](img/p1-s1-04-datos-conceptual!p1-s1-04-datos-conceptual_10.png)

_Figura 13. Modelo conceptual de datos del Sprint 1 — Entidades de usuario, organización y proyecto._

### Modelo Lógico (Esquema Relacional)

```
usuarios (
  id          PK  SERIAL
  nombre          VARCHAR(100)  NOT NULL
  apellido        VARCHAR(100)  NOT NULL
  correo          VARCHAR(255)  NOT NULL  UNIQUE
  contrasena_hash VARCHAR(255)  NOT NULL
  rol             VARCHAR(20)   NOT NULL  CHECK (rol IN ('admin','tecnico','cliente'))
  activo          BOOLEAN       NOT NULL  DEFAULT TRUE
  fecha_creacion  TIMESTAMP     NOT NULL  DEFAULT NOW()
)

organizaciones (
  id             PK  SERIAL
  nombre             VARCHAR(200)  NOT NULL  UNIQUE
  direccion          VARCHAR(300)
  contacto           VARCHAR(200)
  activo             BOOLEAN       NOT NULL  DEFAULT TRUE
  fecha_creacion     TIMESTAMP     NOT NULL  DEFAULT NOW()
)

proyectos (
  id               PK  SERIAL
  nombre               VARCHAR(200)  NOT NULL
  descripcion          TEXT
  estado               VARCHAR(20)   NOT NULL  DEFAULT 'activo'
                         CHECK (estado IN ('activo','pausado','completado','cancelado'))
  fecha_inicio         DATE
  fecha_fin            DATE
  fecha_creacion       TIMESTAMP     NOT NULL  DEFAULT NOW()
  organizacion_id  FK  INTEGER       NOT NULL  REFERENCES organizaciones(id)
  usuario_id       FK  INTEGER                 REFERENCES usuarios(id)
)
```

### Normalización aplicada

- **1FN:** Todos los atributos son atómicos; no hay grupos repetitivos.
- **2FN:** No hay dependencias parciales (todas las tablas tienen clave primaria simple).
- **3FN:** No hay dependencias transitivas; `rol` y `estado` usan CHECK constraint en lugar de tabla de lookup para simplicidad en este sprint.

---

## S1.2.4 Modelo de Lógica — Flujo de Autenticación (PB-10 / PB-19)

El flujo de autenticación es el proceso más relevante del Sprint 1 por involucrar múltiples componentes. Se documenta mediante diagrama de secuencia:

![Flujo de Autenticación — PB-10 / PB-19](img/p1-s1-05-secuencia-autenticacion!p1-s1-05-secuencia-autenticacion!p1-s1-05-secuencia-autenticacion_11.png)

_Figura 14. Diagrama de secuencia — Flujo de autenticación mediante JWT (PB-10 / PB-19)._


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Sprint 1 — Implementación

## S1.3 Avance de Implementación

### Estándar de codificación adoptado

- **Backend (Python):** PEP 8, nombres en `snake_case`, docstrings en funciones públicas, tipado estático con `mypy`.
- **Frontend (TypeScript):** ESLint + Prettier, componentes funcionales con hooks, nombres de archivos en `PascalCase` para componentes y `camelCase` para utilidades.
- **Mobile (Dart):** Guía de estilo oficial de Flutter (`dart format`), BLoC separado por funcionalidad, repositorios con interfaz en dominio e implementación en data.

### Estilo arquitectónico

- **Backend:** Arquitectura por capas (presentación → servicios → repositorios → base de datos).
- **Frontend web:** Componentes con separación de lógica (`hooks`) y presentación (`JSX`).
- **App móvil:** Clean Architecture de tres capas (presentation / domain / data) con BLoC/Cubit.

### Gestión de base de datos

Se utiliza **SQLAlchemy ORM** con **Alembic** para migraciones. Esta decisión otorga:
- Desacoplamiento del modelo de dominio del motor de BD.
- Control de versiones del esquema en cada sprint.
- Facilidad de pruebas con base de datos en memoria (SQLite) en CI.

---

### Descripción de componentes implementados

#### Backend — FastAPI

| Componente                         | Descripción                                                                 |
| ---------------------------------- | --------------------------------------------------------------------------- |
| `POST /api/v1/auth/login`          | Autenticación con correo/contraseña, retorna JWT firmado (HS256)            |
| `GET/POST /api/v1/users`           | CRUD de usuarios del sistema (solo administrador)                           |
| `GET/POST /api/v1/organizations`   | CRUD de organizaciones/clientes                                             |
| `GET/POST /api/v1/projects`        | CRUD de proyectos de levantamiento                                          |
| `GET /api/v1/projects?org_id=X`    | Listado de proyectos filtrado por organización                              |
| Middleware JWT                     | Verificación de token en cada endpoint protegido; extracción de rol         |
| Alembic migration `001_initial`    | Creación de tablas `usuarios`, `organizaciones`, `proyectos`                |

#### Frontend Web — React + TypeScript

| Componente                | Descripción                                                              |
| ------------------------- | ------------------------------------------------------------------------ |
| `LoginPage`               | Formulario de autenticación con validación y manejo de errores           |
| `DashboardPage`           | Vista principal con resumen de proyectos activos                         |
| `UsersPage`               | Listado, creación y edición de usuarios                                  |
| `OrganizationsPage`       | CRUD de organizaciones con tabla paginada                                |
| `ProjectsPage`            | Listado y filtro de proyectos por organización; creación y edición       |
| `apiClient` (Axios)       | Instancia centralizada con interceptor para agregar token JWT al header  |
| Contexto de autenticación | Gestión global del estado de sesión (usuario, token, rol)                |

#### App Móvil — Flutter

| Componente              | Descripción                                                                    |
| ----------------------- | ------------------------------------------------------------------------------ |
| `LoginScreen`           | Pantalla de inicio de sesión con Material 3, Poppins/Inter, manejo de errores |
| `DashboardScreen`       | Pantalla principal post-login con listado de proyectos asignados               |
| `AuthCubit`             | Gestión de estado de autenticación (inicial, cargando, autenticado, error)     |
| `AuthRemoteDataSource`  | Cliente Dio para `POST /auth/login`; almacenamiento de token con FlutterSecureStorage |
| `AuthRepository`        | Abstracción de dominio que desacopla la UI de la fuente de datos               |

---

### Infraestructura

| Componente                   | Estado        |
| ----------------------------- | ------------- |
| `docker-compose.yml`          | Implementado  |
| Servicio `db` (PostgreSQL 15) | Implementado  |
| Servicio `backend` (FastAPI)  | Implementado  |
| Servicio `web` (React/Nginx)  | Implementado  |
| Servicio `nginx` (proxy)      | Implementado  |
| GitHub Actions (CI lint+test) | Implementado  |


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Sprint 1 — Pruebas

## S1.4 Pruebas Realizadas

Las pruebas del Sprint 1 siguen tres filtros de verificación complementarios que cubren la perspectiva del desarrollador, del equipo de calidad y del responsable del producto.

---

## Filtro 1 — Pruebas Unitarias (Desarrollador)

Cada desarrollador entregó código con pruebas unitarias que verifican la lógica de negocio de forma aislada, sin depender de la base de datos real ni de la red.

### Backend (pytest)

**Tabla 5.** Pruebas unitarias del backend (pytest) — Sprint 1

| ID Prueba   | Módulo                  | Caso probado                                                         | Resultado |
| ----------- | ----------------------- | -------------------------------------------------------------------- | :-------: |
| UT-BE-01    | `AuthService`           | Autenticación exitosa con credenciales válidas retorna token JWT     | Aprobada  |
| UT-BE-02    | `AuthService`           | Autenticación con contraseña incorrecta lanza `HTTPException 401`    | Aprobada  |
| UT-BE-03    | `AuthService`           | Autenticación de usuario inactivo lanza `HTTPException 401`          | Aprobada  |
| UT-BE-04    | `UserService`           | Creación de usuario con correo duplicado lanza `HTTPException 409`   | Aprobada  |
| UT-BE-05    | `UserService`           | Creación de usuario con datos válidos retorna usuario creado         | Aprobada  |
| UT-BE-06    | `OrganizationService`   | Creación de organización con nombre duplicado lanza `HTTPException 409` | Aprobada |
| UT-BE-07    | `OrganizationService`   | Desactivación de organización actualiza campo `activo = False`       | Aprobada  |
| UT-BE-08    | `ProjectService`        | Creación de proyecto con organización inexistente lanza `HTTPException 404` | Aprobada |
| UT-BE-09    | `ProjectService`        | Listado de proyectos filtrado por `organizacion_id` retorna solo los correspondientes | Aprobada |
| UT-BE-10    | Middleware JWT           | Token expirado en endpoint protegido retorna `HTTPException 401`     | Aprobada  |

### App Móvil (flutter_test)

**Tabla 6.** Pruebas unitarias de la app móvil (flutter_test) — Sprint 1

| ID Prueba   | Módulo                  | Caso probado                                                         | Resultado |
| ----------- | ----------------------- | -------------------------------------------------------------------- | :-------: |
| UT-FL-01    | `AuthCubit`             | Estado inicial es `AuthInitial`                                      | Aprobada  |
| UT-FL-02    | `AuthCubit`             | Login exitoso emite `AuthLoading` → `AuthAuthenticated`              | Aprobada  |
| UT-FL-03    | `AuthCubit`             | Login fallido emite `AuthLoading` → `AuthError` con mensaje          | Aprobada  |
| UT-FL-04    | `AuthRepository`        | `login()` llama al datasource con correo y contraseña correctos      | Aprobada  |
| UT-FL-05    | `LoginScreen` widget    | Botón de login deshabilitado si campos vacíos                        | Aprobada  |

---

## Filtro 2 — Pruebas de Calidad (QA)

El segundo integrante actuó como QA verificando funcionalidad, rendimiento y seguridad de los módulos entregados.

### Pruebas funcionales

**Tabla 7.** Pruebas funcionales de calidad — Sprint 1

| ID Prueba   | Funcionalidad                         | Escenario probado                                          | Resultado |
| ----------- | ------------------------------------- | ---------------------------------------------------------- | :-------: |
| QA-F-01     | Login panel web                       | Flujo completo de login con usuario administrador          | Aprobada  |
| QA-F-02     | Login panel web                       | Login con contraseña errónea muestra mensaje sin revelar campo | Aprobada |
| QA-F-03     | Gestión de usuarios                   | CRUD completo desde panel web                              | Aprobada  |
| QA-F-04     | Gestión de organizaciones             | CRUD completo; intento de nombre duplicado muestra error   | Aprobada  |
| QA-F-05     | Gestión de proyectos                  | Crear proyecto, filtrar por cliente, editar estado         | Aprobada  |
| QA-F-06     | Login app móvil                       | Flujo completo de autenticación en dispositivo Android     | Aprobada  |

### Pruebas de rendimiento

**Tabla 8.** Pruebas de rendimiento de endpoints críticos — Sprint 1

| ID Prueba   | Endpoint                         | Métrica                        | Resultado  |
| ----------- | -------------------------------- | ------------------------------ | :--------: |
| QA-P-01     | `POST /auth/login`               | Tiempo de respuesta < 500 ms   | 180 ms  |
| QA-P-02     | `GET /projects?org_id=1`         | Tiempo de respuesta < 300 ms   | 95 ms   |
| QA-P-03     | `GET /users` (100 registros)     | Tiempo de respuesta < 500 ms   | 210 ms  |

### Pruebas de seguridad

**Tabla 9.** Pruebas de seguridad de autenticación y autorización — Sprint 1

| ID Prueba   | Escenario                                                    | Resultado |
| ----------- | ------------------------------------------------------------ | :-------: |
| QA-S-01     | Acceso a `/users` sin token retorna 401                      | Aprobada  |
| QA-S-02     | Acceso a `/users` con token de rol `tecnico` retorna 403     | Aprobada  |
| QA-S-03     | Token manipulado (firma inválida) retorna 401                | Aprobada  |

---

## Filtro 3 — Pruebas de Aceptación (Product Owner)

El Product Owner verificó que cada historia de usuario cumple con sus criterios de aceptación definidos en la planificación del sprint.

**Tabla 10.** Pruebas de aceptación — Verificación por historia de usuario

| HU     | Criterios verificados                                                  | Aceptada |
| ------ | ---------------------------------------------------------------------- | :------: |
| PB-01  | CRUD de usuarios; no permite correo duplicado; desactivación funciona  | Sí    |
| PB-09  | CRUD de organizaciones; nombre duplicado muestra error; desactivación  | Sí    |
| PB-10  | Login web; JWT persiste en sesión; logout funciona; error sin revelar campo | Sí |
| PB-13  | CRUD de proyectos; asociación con cliente; estados correctos           | Sí    |
| PB-18  | Listado filtrado por cliente; navegación al detalle funciona           | Sí    |
| PB-19  | Login app móvil; token almacenado; sesión persiste; logout funciona    | Sí    |

**Resultado del Sprint 1:** Todas las historias de usuario comprometidas fueron aceptadas por el Product Owner. El incremento es una versión operativa que aporta valor: el sistema cuenta con autenticación segura, gestión completa de la estructura organizacional (usuarios, clientes, proyectos) y acceso desde la app móvil.

