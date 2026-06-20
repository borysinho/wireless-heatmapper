## 2.5 Mapas de Calor y Técnicas de Interpolación Espacial

### 2.5.1 El mapa de calor como instrumento de diagnóstico de cobertura

Un **mapa de calor de cobertura Wi-Fi** (Wi-Fi heatmap) es una representación gráfica superpuesta sobre el plano de un edificio que traduce los valores de RSSI medidos en cada punto del relevamiento a una escala de color continua e intuitiva: convencionalmente, el verde o el azul para zonas de señal fuerte (RSSI ≥ −70 dBm), el amarillo o el naranja para zonas de señal aceptable (−70 a −85 dBm) y el rojo para zonas de señal débil o muerta (RSSI < −90 dBm).

La utilidad del mapa de calor radica en que convierte miles de valores numéricos aislados —las muestras de RSSI tomadas en distintos puntos del recorrido— en una imagen comprensible tanto para el técnico experto como para el cliente final sin conocimientos de telecomunicaciones. Esta accesibilidad es uno de los fundamentos del producto entregado por el Wireless HeatMapper al cierre de cada proyecto (RP3, RP6, RP9).

Para generarlo, sin embargo, se enfrenta un problema fundamental: los puntos de medición son **discretos y distribuidos irregularmente** sobre el plano, mientras que el mapa de calor debe representar una **función continua** sobre toda la superficie del edificio. La solución a este problema es la **interpolación espacial**: el proceso de estimar el valor de RSSI en los puntos no medidos a partir de los valores medidos en los puntos vecinos.

### 2.5.2 Interpolación por Distancia Inversa Ponderada (IDW)

La **Inverse Distance Weighting (IDW)** es la técnica de interpolación espacial más empleada en la práctica de site survey Wi-Fi por su simplicidad de implementación y su bajo costo computacional. El principio del IDW es que el valor estimado en un punto no medido $p_0$ es un promedio ponderado de los valores medidos en los puntos vecinos $\{p_1, p_2, \ldots, p_n\}$, donde el peso de cada vecino es inversamente proporcional a su distancia a $p_0$:

$$\hat{z}(p_0) = \frac{\displaystyle\sum_{i=1}^{n} \frac{z(p_i)}{d(p_0, p_i)^k}}{\displaystyle\sum_{i=1}^{n} \frac{1}{d(p_0, p_i)^k}}$$

donde:

- $\hat{z}(p_0)$ es el valor de RSSI estimado en el punto $p_0$,
- $z(p_i)$ es el valor de RSSI medido en el punto vecino $p_i$,
- $d(p_0, p_i)$ es la distancia euclidiana entre $p_0$ y $p_i$,
- $k$ es el exponente de potencia que controla la tasa de decaimiento del peso con la distancia (típicamente $k = 2$).

**Propiedades del IDW relevantes para el proyecto:**

- Es un interpolador exacto: en los puntos de medición, el valor estimado coincide exactamente con el valor medido.
- Con $k = 2$, los puntos lejanos tienen una influencia mucho menor que los cercanos, lo que produce transiciones suaves pero conserva bien las discontinuidades locales.
- No hace suposiciones sobre la distribución estadística de los datos, lo que lo hace adecuado para RSSI en entornos con muchos obstáculos.
- Su principal limitación es el **efecto isla** (_bull's eye_): en zonas de alta densidad de puntos con valores similares, puede generar contornos artificialmente circulares.

### 2.5.3 Kriging

El **Kriging** es una familia de técnicas de interpolación geoestadística desarrolladas originalmente en la minería (Krige, 1951) y ampliamente adoptadas en ciencias ambientales y geoespaciales. A diferencia del IDW, el Kriging es un **estimador óptimo no sesgado**: incorpora información sobre la estructura espacial de la correlación entre los datos (capturada en el **variograma** o semivariograma experimental) para calcular pesos óptimos en el sentido de mínima varianza.

El variograma $\gamma(h)$ describe cómo varía la similitud entre pares de puntos en función de su separación $h$:

$$\gamma(h) = \frac{1}{2N(h)} \sum_{i=1}^{N(h)} [z(p_i + h) - z(p_i)]^2$$

donde $N(h)$ es el número de pares de puntos separados por la distancia $h$.

El Kriging Ordinario —la variante más común— estima el valor en un punto no medido $p_0$ como:

$$\hat{z}(p_0) = \sum_{i=1}^{n} \lambda_i \cdot z(p_i)$$

donde los pesos $\lambda_i$ se calculan resolviendo el sistema de ecuaciones de Kriging, que minimiza la varianza del error de estimación condicionada a la restricción de que la estimación sea no sesgada ($\sum \lambda_i = 1$).

**Ventajas del Kriging sobre IDW para heatmaps Wi-Fi:**

- Proporciona, además del valor estimado, una **varianza de la estimación** en cada punto, lo que permite identificar zonas del plano donde la estimación es poco confiable por escasez de puntos de medición.
- Genera transiciones más suaves y consistentes con la estructura espacial real de la señal.
- Puede incorporar tendencias globales del campo de señal (Kriging Universal).

**Desventaja:** mayor complejidad computacional y necesidad de estimar el variograma experimental con un número suficiente de puntos de medición (recomendado: ≥ 30 puntos). En proyectos con pocos puntos de medición, el IDW es preferible por su robustez.

El módulo de generación de heatmap del Wireless HeatMapper (RP3) implementa ambas técnicas —IDW como método predeterminado y Kriging como alternativa opcional para proyectos con alta densidad de puntos— ejecutadas en el backend Python/FastAPI mediante la librería `scipy.interpolate` y el módulo `pykrige`.

### 2.5.4 Renderización del heatmap sobre el plano

El proceso de generación del mapa de calor en el Wireless HeatMapper sigue los siguientes pasos:

1. **Normalización de coordenadas:** los puntos de medición marcados sobre el plano digital (en píxeles) se convierten a coordenadas métricas reales usando el factor de escala calibrado durante la importación del plano (RP2).
2. **Creación del grid de interpolación:** se genera una grilla regular de resolución configurable (por defecto, una celda por cada 0.5 m²) que cubre toda la extensión del plano.
3. **Interpolación:** se aplica IDW (o Kriging) para estimar el RSSI en cada celda de la grilla.
4. **Mapeo de color:** los valores de RSSI estimados se mapean a una paleta de colores (verde → amarillo → naranja → rojo) usando los umbrales de la Tabla 13.1 del CWNA-107.
5. **Composición visual:** el heatmap coloreado se superpone con transparencia sobre el plano del edificio y se sirve al cliente móvil y al portal web como imagen PNG.
