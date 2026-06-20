## Métricas de Calidad de Señal en Redes Wi-Fi

### RSSI — Received Signal Strength Indicator

El **RSSI** (Received Signal Strength Indicator), también denominado RSL (Received Signal Level) en la nomenclatura del CWNA-107, es la métrica primaria para evaluar la calidad de una señal Wi-Fi desde la perspectiva del cliente receptor. Se expresa en **dBm** (decibelios relativos a 1 miliWatt), con valores que en la práctica oscilan entre aproximadamente −30 dBm (señal muy fuerte, cliente a pocos metros del AP) y −100 dBm (señal al límite del piso de ruido) (Coleman & Westcott, 2018).

El dBm es una unidad logarítmica de potencia absoluta. Su definición es:

$$P_{dBm} = 10 \log_{10}\!\left(\frac{P_{mW}}{1\,mW}\right)$$

La escala logarítmica es fundamental para interpretar correctamente los valores de RSSI: una diferencia de 3 dBm representa aproximadamente el doble o la mitad de la potencia recibida; una diferencia de 10 dBm representa diez veces más o menos potencia. En consecuencia, pasar de −70 dBm a −80 dBm no es una reducción de ~14 % —como parecería en la escala lineal— sino una reducción al 10 % de la potencia original (Coleman & Westcott, 2018).

#### Tabla de calidad de señal recibida (CWNA-107, Tabla 13.1)

El estándar CWNA-107 define la siguiente clasificación de calidad de señal, que el módulo de análisis de cobertura del Wireless HeatMapper adopta íntegramente (Coleman & Westcott, 2018):

| Calidad                              | Rango RSSI  |
| ------------------------------------ | ----------- |
| Muy fuerte                           | ≥ −60 dBm   |
| **Fuerte (objetivo de diseño)**      | **−70 dBm** |
| Aceptable                            | −80 dBm     |
| Débil                                | −90 dBm     |
| Muy débil (límite del piso de ruido) | ≤ −95 dBm   |

> **Criterio de diseño del Wireless HeatMapper (RP3, RP4, RP5):** toda zona del plano donde el RSSI sea ≥ −70 dBm se considera cobertura adecuada; toda zona con RSSI < −90 dBm se clasifica como **zona muerta**. Estas definiciones provienen directamente del marco técnico CWNA-107 y se aplican tanto al mapa de calor generado como al análisis automatizado de cobertura.

#### Limitaciones técnicas del RSSI reportado por Android

Es importante señalar que el RSSI reportado por una NIC 802.11 estándar (como la del smartphone Android que utiliza el técnico de campo) no es una medición de potencia en sentido estricto. Los chips Wi-Fi integran el nivel de señal mediante algoritmos propietarios que no están estandarizados entre fabricantes. Adicionalmente, Android impone restricciones de _scan throttling_ a partir de la versión 8.0 (Oreo): en modo pasivo, el sistema limita los escaneos a no más de 4 por cada 2 minutos para conservar batería, lo que reduce la densidad temporal de muestras que la aplicación puede capturar durante el recorrido (Coleman & Westcott, 2018). El diseño del módulo RP1 del Wireless HeatMapper contempla esta limitación.

### SNR — Signal-to-Noise Ratio

El **SNR** (relación señal a ruido) es la diferencia en dB entre el nivel de señal recibida (RSSI) y el piso de ruido del canal. Es la métrica que determina la capacidad del receptor para decodificar correctamente los bits transmitidos:

$$SNR_{dB} = RSSI_{dBm} - Noise\,Floor_{dBm}$$

Los valores mínimos recomendados por el CWNA-107 para distintas aplicaciones son:

| Aplicación                              | SNR mínimo recomendado |
| --------------------------------------- | ---------------------- |
| Datos generales                         | 20 dB                  |
| Voz sobre Wi-Fi (VoWiFi)                | 25 dB                  |
| 802.11ac con 256-QAM (máxima velocidad) | 29 dB                  |
| 802.11ax con 1024-QAM                   | 35 dB                  |

Un piso de ruido típico en la banda 2.4 GHz en entornos de oficina es de aproximadamente −100 dBm (Coleman & Westcott, 2018). Por lo tanto, un RSSI de −70 dBm sobre un piso de ruido de −100 dBm produce un SNR de 30 dB, suficiente para operar a las tasas más altas del 802.11n/ac.

### CCI — Interferencia Co-Canal (Co-Channel Interference)

La **CCI** ocurre cuando dos o más APs que utilizan el mismo canal están dentro del rango de escucha de un mismo cliente. Dado que 802.11 es una red de acceso al medio compartido (CSMA/CA), la CCI obliga a los APs a esperar antes de transmitir cada vez que detectan otro AP en el mismo canal transmitiendo, lo que reduce directamente el throughput disponible. En una red mal diseñada con APs 2.4 GHz todos configurados en canal 6, la CCI puede reducir el throughput efectivo a menos del 30 % del valor teórico.

### ACI — Interferencia por Canal Adyacente (Adjacent Channel Interference)

La **ACI** ocurre cuando dos APs utilizan canales distintos pero solapados espectralmente (por ejemplo, canal 1 y canal 3 en la banda 2.4 GHz). Los filtros de los receptores 802.11 no atenúan completamente las señales de canales adyacentes, por lo que parte de la energía del canal vecino "derrama" sobre el canal en uso. La ACI es más difícil de diagnosticar que la CCI porque los APs en canales no planificados (canales 2, 3, 4, etc.) son frecuentemente producto de redes vecinas fuera del control del administrador.

El módulo de análisis de cobertura del Wireless HeatMapper (RP4) detecta automáticamente los APs activos en cada punto de medición —incluidos sus canales— y cruza esta información para identificar situaciones de CCI y ACI, entregando el resultado como hallazgos categorizados por severidad en el reporte final.

### Dynamic Rate Switching (DRS)

Un concepto estrechamente ligado al RSSI es el **Dynamic Rate Switching**: a medida que un cliente se aleja del AP y el RSSI disminuye, el estándar 802.11 negocia tasas de datos progresivamente menores (modulaciones más robustas pero menos eficientes en espectro). Esto implica que un cliente a −80 dBm puede seguir conectado pero consumirá mucho más tiempo de canal para transmitir la misma cantidad de datos que a −60 dBm, perjudicando a todos los demás clientes en la misma celda (Coleman & Westcott, 2018). Este efecto es uno de los fundamentos técnicos que justifica el umbral de diseño de −70 dBm como objetivo del Wireless HeatMapper.
