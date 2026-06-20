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

---
