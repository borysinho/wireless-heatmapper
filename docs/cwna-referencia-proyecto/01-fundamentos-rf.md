# 01 — Fundamentos RF: Propagación, Pérdidas y Multipath

> **Fuente principal:** [CWNA-107.md](../CWNA-107.md), **Capítulo 3 — Radio Frequency Fundamentals**, sección _Radio Frequency Behaviors_ (págs. 80–96, líneas ~4830–5180).

Esta extracción agrupa los comportamientos físicos de las señales RF que **afectan directamente la calidad del heatmap** (RP3) y la **detección de zonas muertas / interferencia** (RP4). Sin estos conceptos no es posible interpretar correctamente la atenuación medida ni elegir un modelo de interpolación adecuado.

---

## 1. Wave Propagation (Propagación de la onda)

> **Fuente:** Cap. 3 — _Wave Propagation_ (pág. 81, líneas ~4842–4862).

La forma en que una señal RF se mueve depende del medio: el drywall (yeso) afecta la onda muy diferente al concreto o al metal. Las ondas se ensanchan a medida que se alejan de la antena (analogía del epicentro de un terremoto): cerca del AP la señal es fuerte y concentrada; lejos del AP se atenúa y debilita.

**Implicación para el proyecto:** las muestras RSSI capturadas por el dispositivo Android no decaen linealmente respecto a la distancia. El algoritmo de interpolación (RP3) debe considerar atenuación logarítmica + obstáculos.

---

## 2. Absorción

> **Fuente:** Cap. 3 — _Absorption_ (pág. 82, líneas ~4870–4890).

- Si la señal no rebota, no rodea ni atraviesa el objeto, hay 100% absorción.
- A 2.4 GHz una pared de concreto deja la señal en **1/16** de su potencia original; el drywall reduce a aproximadamente **1/2**.
- El **agua** absorbe fuertemente la RF: papel, cartón, peceras y los **cuerpos humanos** (50–65% agua) son absorbentes.

**Caso "User Density"** (Cap. 3, pág. 82): un site survey hecho con la sala vacía dio cobertura aceptable; durante una tormenta con la terminal aeroportuaria llena de personas, la calidad cayó por absorción humana. **Para Heatmapper:** capturar muestras en condiciones reales de ocupación y considerar que la cobertura puede degradarse en horarios pico.

### Tabla 3.1 — Atenuación a 2.4 GHz por material

> **Fuente:** Cap. 3, pág. 88, líneas ~5158–5170.

| Material           | Atenuación @ 2.4 GHz |
| ------------------ | -------------------- |
| Hueco de ascensor  | −30 dB               |
| Pared de concreto  | −12 dB               |
| Puerta de madera   | −3 dB                |
| Ventana sin tintar | −3 dB                |
| Drywall            | −3 dB                |
| Drywall hueco      | −2 dB                |
| Pared de cubículo  | −1 dB                |

**Aplicación:** estos valores pueden alimentar el motor de IA (RP5) como _priors_ del modelo de propagación al colocar APs sobre el plano.

---

## 3. Reflexión

> **Fuente:** Cap. 3 — _Reflection_ (págs. 82–84, líneas ~4906–4940).

- Cuando la onda choca con una superficie lisa más grande que la longitud de onda, rebota.
- En entornos indoor, microondas se reflejan en puertas, paredes lisas, archivadores; el metal **siempre** refleja; vidrio y concreto pueden reflejar.
- Múltiples reflexiones llegan al receptor → fenómeno **multipath**.
- 802.11n/ac (MIMO) **aprovechan** el multipath con MRC (Maximal Ratio Combining); equipos legacy a/b/g lo sufrían.

---

## 4. Scattering (Dispersión)

> **Fuente:** Cap. 3 — _Scattering_ (págs. 84–85, líneas ~4948–4972).

Reflexiones múltiples cuando la longitud de onda es mayor que las partículas/superficies irregulares: **mallas metálicas, cercas de eslabón, paredes de estuco con malla, follaje, terreno rocoso**. La señal principal se descompone en muchas señales reflejadas más débiles, lo cual puede provocar pérdida significativa de la señal recibida.

---

## 5. Refracción

> **Fuente:** Cap. 3 — _Refraction_ (págs. 85–86, líneas ~4978–5002).

Doblado de la señal al pasar por un medio de distinta densidad. Causas: vapor de agua, cambios de temperatura/presión, cierto vidrio. Importante en enlaces outdoor (k-factor); poco frecuente indoor pero puede ocurrir con vidrios especiales.

---

## 6. Difracción

> **Fuente:** Cap. 3 — _Diffraction_ (págs. 86–87, líneas ~5008–5030).

Doblado y dispersión de la señal alrededor de un obstáculo (colina, edificio, viga). Detrás del obstáculo se forma una **RF shadow** (sombra RF) que puede ser zona muerta o de señal degradada.

**Para Heatmapper (RP4):** las zonas muertas no siempre coinciden con el área "por detrás" del AP — una viga estructural cercana puede generar una sombra perceptible en el heatmap.

---

## 7. Loss / Attenuation (Pérdida / Atenuación)

> **Fuente:** Cap. 3 — _Loss (Attenuation)_ (págs. 87–89, líneas ~5036–5170).

Disminución de la amplitud (potencia). Causas:

- Cable coaxial e impedancia (lado cableado).
- Absorción al atravesar materiales.
- FSPL (ver siguiente sección).
- Multipath destructivo.

---

## 8. Free Space Path Loss (FSPL)

> **Fuente:** Cap. 3 — _Free Space Path Loss_ (págs. 89–91, líneas ~5009–5070).

Aun **sin obstáculos** la señal se atenúa por el ensanchamiento natural del frente de onda (analogía del globo). La pérdida es **logarítmica**, no lineal.

**Fórmulas:**

$$ FSPL = 36.6 + 20\log*{10}(f*{MHz}) + 20\log*{10}(D*{millas}) $$

$$ FSPL = 32.44 + 20\log*{10}(f*{MHz}) + 20\log*{10}(D*{km}) $$

**Regla de los 6 dB:** doblar la distancia → 6 dB de pérdida adicional.

### Tabla 3.2 — Atenuación por FSPL

> **Fuente:** Cap. 3, pág. 90.

| Distancia (m) | 2.4 GHz  | 5 GHz    |
| ------------- | -------- | -------- |
| 1             | 40 dB    | 46.4 dB  |
| 10            | 60 dB    | 66.4 dB  |
| 100           | 80 dB    | 86.4 dB  |
| 1000          | 100.0 dB | 106.4 dB |

**Implicación crítica para Heatmapper:**

- 5 GHz se atenúa más rápido que 2.4 GHz a la misma distancia (~6.4 dB adicionales).
- El modelo log-distance es la base teórica del **algoritmo de interpolación** (RP3) y el **modelo de propagación del optimizador IA** (RP5).
- La señal recibida nunca puede ser mayor que la transmitida (también limita el upfade del multipath).

---

## 9. Multipath

> **Fuente:** Cap. 3 — _Multipath_ (págs. 91–94, líneas ~5072–5140).

Múltiples copias de la misma señal llegan al receptor con diferencias de tiempo (delay spread) por reflexión/dispersión/difracción/refracción. Cuatro resultados posibles según la fase relativa:

| Resultado                 | Diferencia de fase | Efecto                                                                             |
| ------------------------- | ------------------ | ---------------------------------------------------------------------------------- |
| **Upfade**                | 0°–120°            | Aumento de amplitud (constructivo)                                                 |
| **Downfade**              | 121°–179°          | Disminución de amplitud (destructivo)                                              |
| **Nulling**               | 180°               | Cancelación total de la señal                                                      |
| **Data corruption / ISI** | —                  | Bits superpuestos por delay spread → frame corrupto → CRC falla → retransmisión L2 |

**Implicación para Heatmapper:**

- Dos mediciones RSSI tomadas en posiciones muy próximas pueden diferir varios dB por multipath. **Es necesario promediar varias capturas** por punto (mitiga ruido y multipath).
- Entornos con mucho metal (almacenes, hangares) son ambientes de **alto multipath**: el heatmap debe representarse con mayor incertidumbre o suavizado mayor.

---

## 10. Visual Line of Sight vs. RF Line of Sight

> **Fuente:** Cap. 3 — _Visual Line of Sight / RF Line of Sight_ (líneas ~7003–7060).

La línea de vista visual no garantiza línea de vista RF: la zona de Fresnel debe estar despejada. Aplicable principalmente para enlaces outdoor punto-a-punto; mencionado aquí solo como referencia del libro.

---

## Resumen de aplicabilidad al proyecto

- **RP1 (captura):** la métrica RSSI capturada por el sistema operativo Android **ya incluye** los efectos de absorción + FSPL + multipath en ese punto y momento. No hay forma de separarlos a posteriori → el sistema debe **muestrear varias veces** y **promediar**.
- **RP3 (heatmap):** el método de interpolación espacial (IDW, kriging, log-distance fit) debe asumir atenuación logarítmica con obstáculos.
- **RP4 (cobertura):** las zonas muertas pueden ser por **FSPL**, **absorción** (paredes), **difracción** (sombras RF) o **nulling** por multipath — el reporte debe poder **distinguirlas** o, al menos, no confundirlas con falla del AP.
- **RP5 (IA):** los priors del modelo de propagación deben tomar en cuenta los valores de atenuación de la **Tabla 3.1** según el material registrado en el plano.
