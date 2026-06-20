## 2.2 Propagación de Señales RF en Entornos Interiores

La calidad de la cobertura Wi-Fi en un edificio no depende únicamente de la potencia del transmisor ni de la distancia entre el AP y el cliente. En entornos interiores, la señal RF interactúa de forma compleja con los materiales constructivos del edificio mediante cinco mecanismos físicos fundamentales: absorción, reflexión, dispersión (scattering), refracción y difracción. La comprensión y cuantificación de estos mecanismos es la base teórica que justifica la necesidad de un relevamiento de campo real —en lugar de modelos teóricos de cobertura— y que da sustento al algoritmo de interpolación espacial del módulo RP3 del Wireless HeatMapper (Coleman & Westcott, 2018).

### 2.2.1 Pérdida en Espacio Libre (FSPL)

En ausencia de obstáculos, la potencia de la señal recibida disminuye a medida que aumenta la distancia al transmisor. Este fenómeno, denominado **Free Space Path Loss (FSPL)**, sigue una relación logarítmica con la distancia y con la frecuencia:

$$FSPL_{dB} = 20 \log_{10}(d) + 20 \log_{10}(f) + 20 \log_{10}\!\left(\frac{4\pi}{c}\right)$$

donde $d$ es la distancia en metros, $f$ es la frecuencia en Hz y $c$ es la velocidad de la luz. Para las frecuencias Wi-Fi, la versión práctica de la fórmula es:

$$FSPL_{dB} \approx 20 \log_{10}(d) + 20 \log_{10}(f_{GHz}) + 92.4$$

El FSPL explica por qué las señales de 5 GHz tienen mayor pérdida de propagación que las de 2.4 GHz a la misma distancia —consecuencia directa del término de frecuencia—, lo que se traduce en menor cobertura pero también en menor interferencia entre celdas adyacentes (Coleman & Westcott, 2018).

### 2.2.2 Absorción

La absorción es el fenómeno por el cual la energía de la onda RF se convierte en calor al atravesar un material. Es el mecanismo dominante de pérdida de señal en entornos interiores. La magnitud de la absorción depende de la composición del material: el agua absorbe fuertemente la RF, lo que implica que paredes de cartón humedecido, bloques de concreto (que retienen humedad), follaje y los propios cuerpos humanos (compuestos en un 50–65 % de agua) son absorbentes significativos de la señal.

La siguiente tabla resume los valores de atenuación típicos a 2.4 GHz por tipo de material constructivo, según el manual CWNA-107:

| Material                                | Atenuación típica a 2.4 GHz |
| --------------------------------------- | --------------------------- |
| Hueco de ascensor (metal)               | −30 dB                      |
| Pared de concreto                       | −12 dB                      |
| Puerta de madera sólida                 | −3 dB                       |
| Ventana sin tintado                     | −3 dB                       |
| Drywall (yeso)                          | −3 dB                       |
| Drywall hueco                           | −2 dB                       |
| Pared de cubículo (tela/madera delgada) | −1 dB                       |

> **Implicación para el Wireless HeatMapper:** estos valores pueden emplearse como _a priori_ en el motor de IA (RP5) cuando el técnico dibuja los muros sobre el plano calibrado del edificio. La atenuación diferencial entre materiales justifica que dos puntos a igual distancia del AP puedan tener valores de RSSI muy distintos, lo que a su vez justifica la necesidad de un relevamiento de campo real punto a punto (Coleman & Westcott, 2018).

### 2.2.3 Reflexión

La reflexión ocurre cuando la onda RF incide sobre una superficie lisa cuyas dimensiones son significativamente mayores que la longitud de onda de la señal. En entornos interiores, el metal (puertas metálicas, archivadores, estructuras de acero), el vidrio y el concreto pulido son los principales reflectores. Las reflexiones generan múltiples copias de la señal original que llegan al receptor con distintos retardos y fases, fenómeno conocido como **multipath**.

El multipath puede ser destructivo (las copias se cancelan entre sí) o constructivo (se suman). Los estándares modernos 802.11n y 802.11ac explotan el multipath de forma constructiva mediante técnicas MIMO (Multiple Input Multiple Output) con recombinación MRC (Maximal Ratio Combining), convirtiendo un fenómeno históricamente problemático en una ventaja para la capacidad de transmisión (Coleman & Westcott, 2018).

### 2.2.4 Dispersión (Scattering)

La dispersión ocurre cuando la onda RF incide sobre superficies irregulares o partículas cuyo tamaño es comparable o menor que la longitud de onda. Mallas metálicas, cercas de eslabón, paredes de estuco con malla, superficies rugosas y follaje denso son causantes de dispersión. El efecto es la fragmentación de la onda incidente en múltiples ondas dispersadas de menor amplitud, lo que produce una pérdida neta de la potencia de la señal en la dirección de propagación original.

### 2.2.5 Difracción

La difracción es el doblado y dispersión de la señal alrededor de un obstáculo sólido. Detrás del obstáculo se forma una **sombra RF** —zona en la que la señal directa no llega— que puede manifestarse como zona muerta (dead zone) o zona de señal muy degradada en el mapa de calor. Vigas estructurales, columnas de concreto y grandes equipos industriales son fuentes típicas de difracción en entornos de oficinas y plantas industriales (Coleman & Westcott, 2018).

El Wireless HeatMapper no modela explícitamente la difracción, pero el relevamiento de campo captura su efecto neto en los valores de RSSI medidos: si una columna genera una sombra RF, los puntos de medición tomados en esa zona reflejarán la caída de señal, que el algoritmo de interpolación y el módulo de análisis (RP4) identificarán automáticamente como zona problemática.

### 2.2.6 Comportamiento general: señal vs. distancia en entornos interiores

La combinación de los cinco mecanismos anteriores produce un perfil de propagación que **no sigue una relación lineal con la distancia** —como sí ocurre con el FSPL en espacio libre— sino que es irregular, asimétrico y dependiente de la planta del edificio. Esto tiene dos consecuencias directas para el proyecto:

1. **Justificación del relevamiento de campo:** un modelo de cobertura puramente teórico (calculado solo con FSPL y las especificaciones del fabricante del AP) no puede predecir con fiabilidad la cobertura real en un edificio con paredes, mobiliario y personas.
2. **Justificación del algoritmo de interpolación espacial:** los algoritmos IDW y Kriging (sección 2.5) son apropiados precisamente porque estiman el valor de RSSI en puntos no medidos a partir de los vecinos más cercanos, capturando implícitamente las irregularidades del entorno sin necesidad de modelar explícitamente cada obstáculo.
