# 02 — RSSI, Mediciones y Matemáticas RF

> Extracción de conceptos del **Capítulo 4 — Radio Frequency Components, Measurements, and Mathematics** del libro CWNA-107, relevantes para los requisitos del proyecto Heatmapper (especialmente RP1 — captura WiFi, RP3 — interpolación, RP4 — análisis de cobertura).

**Fuente principal:** [CWNA-107.md](../CWNA-107.md), Cap. 4 — _Radio Frequency Components, Measurements, and Mathematics_ (págs. 103–138, líneas ~5430–6800).

---

## 1. Componentes RF (Transmisor, Antena, Receptor, IR, EIRP)

Toda comunicación inalámbrica involucra una cadena de componentes que **introducen ganancia o pérdida** sobre la señal:

- **Transmisor (Transmitter):** genera la señal AC modulada a una frecuencia específica (2.4 GHz, 5 GHz). Define el _power level_ original. Las regulaciones locales (FCC y equivalentes) limitan dicha potencia.
- **Antena:** convierte el AC en ondas RF y enfoca la radiación según su patrón. La emisión se compara contra un _isotropic radiator_ (radiador teórico ideal que emite igual en todas las direcciones).
- **Receptor:** convierte la señal recibida (mucho más débil que la transmitida, por FSPL y multipath) en bits.
- **Intentional Radiator (IR):** es el conjunto de **todo lo que hay desde el transmisor hasta —pero sin incluir— la antena**: cables, conectores, atenuadores, pararrayos. Se mide en el conector que entra a la antena, en mW o dBm.
- **EIRP (Equivalent Isotropically Radiated Power):** es la **mayor amplitud RF que sale de la antena**. Es el producto entre la potencia entregada a la antena y la ganancia de la antena. Las regulaciones limitan tanto el IR como el EIRP.

> **Nota crítica para RP1 (captura WiFi):** el ajuste de "transmit power" en distintos vendors puede representar **IR o EIRP**, en mW, dBm o porcentaje. Esto significa que una misma "potencia configurada" en dos APs distintos no es directamente comparable sin consultar la documentación del fabricante.

**Fuente:** CWNA-107.md, Cap. 4 — _RF Components_ (págs. 104–107, líneas ~5495–5615).

---

## 2. Unidades de potencia (absolutas) y de comparación (relativas)

| Tipo                   | Unidad             | Descripción                                                                             |
| ---------------------- | ------------------ | --------------------------------------------------------------------------------------- |
| Potencia (absoluta)    | **W (watt)**       | Unidad básica de potencia (V × A).                                                      |
| Potencia (absoluta)    | **mW (milliwatt)** | 1/1000 de un watt. Rango típico de equipos 802.11 indoor: 1–100 mW.                     |
| Potencia (absoluta)    | **dBm**            | Decibelios relativos a 1 mW. 0 dBm = 1 mW.                                              |
| Comparación (relativa) | **dB (decibel)**   | Razón entre dos potencias (10 × log10 de la razón).                                     |
| Comparación (relativa) | **dBi**            | Ganancia de antena relativa al isotrópico. Una dipolo de media onda 2.4 GHz = 2.14 dBi. |
| Comparación (relativa) | **dBd**            | Ganancia de antena relativa a una dipolo de media onda. dBi = dBd + 2.14.               |

> Las **unidades de potencia** miden potencia transmitida o recibida; las **unidades de comparación** miden cambios de potencia (ganancia o pérdida) introducidos por componentes (cables, antenas, FSPL).

**Fuente:** CWNA-107.md, Cap. 4 — _Units of Power and Comparison_ (págs. 107–114, líneas ~5630–5970).

---

## 3. Regla de los 10s y 3s

Permite calcular ganancias y pérdidas RF **sin logaritmos**, con suficiente precisión para diseño de red (no para certificación regulatoria).

Las cuatro reglas:

- **+3 dB (ganancia)** → multiplicar la potencia (mW) por **2**
- **−3 dB (pérdida)** → dividir la potencia (mW) entre **2**
- **+10 dB (ganancia)** → multiplicar la potencia (mW) por **10**
- **−10 dB (pérdida)** → dividir la potencia (mW) entre **10**

Combinando ±3 y ±10 se puede expresar cualquier dB entero. Por ejemplo: −6 dB = (−3) + (−3); +7 dB = (+10) + (−3).

**Tabla 4.1 — Combinaciones de 10s y 3s para dB enteros entre −10 y +10:**

| dB  | Combinación |
| --- | ----------- |
| −10 | −10         |
| −7  | −10 + 3     |
| −6  | −3 − 3      |
| −3  | −3          |
| +3  | +3          |
| +6  | +3 + 3      |
| +7  | +10 − 3     |
| +10 | +10         |

**Ejemplo (Ejercicio 4.2 del libro):** un bridge a 100 mW (= +20 dBm), con cable de −3 dB y antena de +10 dBi:

- IR = 100 mW − 3 dB = 50 mW (= +17 dBm)
- EIRP = 50 mW + 10 dBi = 500 mW (= +27 dBm)

**Fuente:** CWNA-107.md, Cap. 4 — _Rule of 10s and 3s_ y Tabla 4.1 (págs. 115–120, líneas ~5980–6280).

---

## 4. Tabla de conversión dBm ↔ mW (Tabla 4.2)

Referencia rápida obligatoria para RP1/RP3 (interpretación de RSSI capturado):

| dBm     | mW             | Nivel                   |
| ------- | -------------- | ----------------------- |
| +36 dBm | 4 000 mW       | 4 W                     |
| +30 dBm | 1 000 mW       | 1 W                     |
| +20 dBm | 100 mW         | 1/10 W                  |
| +10 dBm | 10 mW          | 1/100 W                 |
| 0 dBm   | 1 mW           | 1/1000 W                |
| −10 dBm | 0.1 mW         | 1/10 mW                 |
| −30 dBm | 0.001 mW       | 1/1000 mW               |
| −50 dBm | 0.00001 mW     | —                       |
| −70 dBm | 0.0000001 mW   | —                       |
| −80 dBm | 0.00000001 mW  | —                       |
| −90 dBm | 0.000000001 mW | 1 mil-millonésima de mW |

> Los radios 802.11 típicamente pueden interpretar señales recibidas entre −30 dBm (muy fuerte, casi pegado al AP) y −100 dBm (al límite del piso de ruido). **Trabajar siempre en dBm**, no en mW.

**Fuente:** CWNA-107.md, Cap. 4 — _RF Math Summary_, Tabla 4.2 (pág. 121, líneas ~6310–6360).

---

## 5. Noise Floor (Piso de Ruido)

El **noise floor** es el nivel ambiental/de fondo de energía RF en un canal específico. Incluye:

- Bits modulados de otros radios 802.11 cercanos.
- Energía no modulada de equipos no-802.11 (microondas, Bluetooth, teléfonos inalámbricos, etc.).

Valores típicos:

- **Banda 2.4 GHz (ISM)**, entorno típico: **~ −100 dBm**.
- Entornos ruidosos (planta de manufactura): **~ −90 dBm**.
- Banda **5 GHz**: piso de ruido **casi siempre menor** que en 2.4 GHz, porque el espectro está menos congestionado.

> **Aviso técnico relevante para RP1:** una NIC 802.11 estándar **no es un analizador de espectro** y solo "ve" bits que pasan su filtro de codificación. Por ello el "noise floor" reportado por la NIC es estimado mediante algoritmos propietarios. La medición real del piso de ruido requiere un _spectrum analyzer_. Algunos APs modernos integran chipsets de análisis de espectro (modo "hybrid").

**Fuente:** CWNA-107.md, Cap. 4 — _Noise Floor_ y _Can an 802.11 NIC truly measure the noise floor?_ (págs. 122, 126–127, líneas ~6370–6395 y ~6520–6580).

---

## 6. SNR — Signal-to-Noise Ratio

El **SNR** es la diferencia (en dB) entre la señal recibida y el piso de ruido:

$$\text{SNR (dB)} = \text{Señal recibida (dBm)} - \text{Noise Floor (dBm)}$$

Ejemplo: señal a −85 dBm con ruido a −100 dBm → SNR = 15 dB.

Umbrales de calidad (consenso de fabricantes):

| SNR     | Calidad   | Recomendación                                                                |
| ------- | --------- | ---------------------------------------------------------------------------- |
| ≥ 25 dB | Excelente | Recomendado para **voz**                                                     |
| ≥ 20 dB | Buena     | Recomendado para **datos**                                                   |
| ≤ 10 dB | Muy mala  | Alta probabilidad de retransmisiones layer-2, baja throughput, alta latencia |

**Fuente:** CWNA-107.md, Cap. 4 — _Signal-to-Noise Ratio_ y Figura 4.2 (pág. 122, líneas ~6395–6420).

---

## 7. SINR — Signal-to-Interference-Plus-Noise Ratio

El **SINR** es la diferencia entre la señal RF primaria y la suma de ruido + interferencia (en dB).

Diferencia clave con SNR:

- **SNR**: indicador a lo largo del tiempo (el ruido tiende a ser estable).
- **SINR**: mejor indicador **instantáneo**, porque la interferencia (otros dispositivos transmitiendo) ocurre con más frecuencia y variabilidad.

> **Aplicabilidad RP4:** SINR es un indicador más útil para **detectar interferencia transitoria** que afecta zonas específicas en momentos concretos. Si el dispositivo Android lo expone, debería capturarse y graficarse adicionalmente al RSSI.

**Fuente:** CWNA-107.md, Cap. 4 — _Signal-to-Interference-Plus-Noise Ratio_ (págs. 122–123, líneas ~6420–6445).

---

## 8. Receive Sensitivity y Tabla 4.3

La **sensibilidad de recepción** es el nivel mínimo de señal que un radio puede decodificar. Es **dependiente de la velocidad (data rate)**: tasas altas (modulaciones complejas como 256-QAM) requieren mayor potencia recibida; tasas bajas usan modulaciones más robustas.

**Tabla 4.3 — Umbrales de sensibilidad de recepción (ejemplo de fabricante, 2.4 GHz):**

| Data Rate          | Señal mínima |
| ------------------ | ------------ |
| MCS7               | −77 dBm      |
| MCS6               | −78 dBm      |
| MCS5               | −80 dBm      |
| MCS4               | −85 dBm      |
| MCS3               | −88 dBm      |
| MCS2 / MCS1 / MCS0 | −90 dBm      |
| 54 Mbps            | −79 dBm      |
| 48 Mbps            | −80 dBm      |
| 36 Mbps            | −85 dBm      |
| 24 Mbps            | −87 dBm      |
| 18 Mbps            | −90 dBm      |
| 12 / 9 / 6 Mbps    | −91 dBm      |

**Fuente:** CWNA-107.md, Cap. 4 — _Received Signal Strength Indicator_, Tabla 4.3 (págs. 123–124, líneas ~6445–6485).

---

## 9. RSSI — Received Signal Strength Indicator (CRÍTICO PARA RP1)

El estándar 802.11-2016 define el **RSSI** como una **métrica relativa** usada por radios 802.11 para representar la fuerza de la señal recibida. **Su valor va de 0 a 255** (entero), y el **mapeo a dBm es definido por cada fabricante** (proprietary).

Cada fabricante define su propio **`RSSI_Max`** (entre 0 y 255) y su propio rango de mapeo a dBm. Por ejemplo:

| Vendor   | RSSI_Max | Rango dBm representado |
| -------- | -------- | ---------------------- |
| Vendor A | 100      | −110 dBm a −10 dBm     |
| Vendor B | 60       | −95 dBm a −35 dBm      |

**Tabla 4.4 — Ejemplo de métricas RSSI de un fabricante:**

| RSSI | dBm      | Strength % | SNR   | Quality % |
| ---- | -------- | ---------- | ----- | --------- |
| 30   | −30 dBm  | 100%       | 70 dB | 100%      |
| 25   | −41 dBm  | 90%        | 60 dB | 100%      |
| 20   | −52 dBm  | 80%        | 43 dB | 90%       |
| 15   | −63 dBm  | 60%        | 33 dB | 50%       |
| 10   | −75 dBm  | 40%        | 25 dB | 35%       |
| 5    | −89 dBm  | 10%        | 10 dB | 5%        |
| 0    | −110 dBm | 0%         | 0 dB  | 0%        |

Conversión genérica a porcentaje:

$$\text{RSSI \%} = \frac{\text{RSSI}}{\text{RSSI\_Max}}$$

> **⚠️ Implicaciones críticas para RP1 (captura WiFi):**
>
> 1. El valor crudo de RSSI que expone Android es **vendor-dependiente**. No tiene sentido comparar RSSI crudos entre dispositivos distintos.
> 2. La app debe almacenar tanto el **RSSI crudo** (entero) como el **valor en dBm** (Android API `WifiManager.calculateSignalLevel()` o usar directamente el campo `level` que ya devuelve dBm desde API 30+).
> 3. Para interpolación (RP3) **siempre debe usarse el valor en dBm**, no el RSSI crudo, para garantizar comparabilidad entre mediciones tomadas con dispositivos distintos.
> 4. Los thresholds de roaming y de DRS (Dynamic Rate Switching) están definidos en función de RSSI, lo cual explica por qué el cliente cambia de AP en ciertos puntos del recorrido — útil para entender el comportamiento observado durante un site survey.
> 5. La **calidad de señal (SQ — Signal Quality)** es otra métrica del estándar relacionada con la correlación de PN-code (afecta BER); muchos fabricantes la agrupan bajo "RSSI metrics".

**Fuente:** CWNA-107.md, Cap. 4 — _Received Signal Strength Indicator_, Tabla 4.4 (págs. 124–126, líneas ~6485–6555).

---

## 10. Link Budget

El **link budget** es la suma algebraica de **todas las ganancias y pérdidas** desde el radio transmisor, a través del medio RF, hasta el radio receptor. Su propósito: **garantizar que la amplitud final recibida quede por encima del umbral de receive sensitivity**.

Componentes a considerar:

- Potencia transmitida original (dBm).
- Pérdidas por cables (dB por cada 100 ft según el rating).
- Pérdidas por conectores (~0.5 dB cada uno, _insertion loss_).
- Pérdidas por pararrayos / atenuadores.
- Ganancia de antena (dBi).
- **Free Space Path Loss (FSPL)** — la mayor pérdida del enlace (ver capítulo 3).
- Ganancia activa de amplificadores RF (si aplica).

**Tabla 4.5 — Ejemplo de link budget (bridge punto a punto 2.4 GHz a 2 km):**

| Componente                 | Ganancia/Pérdida | Señal acumulada   |
| -------------------------- | ---------------- | ----------------- |
| Transmisor                 | —                | +10 dBm           |
| Cable LMR-600 (10 ft)      | −0.44 dB         | +9.56 dBm         |
| Pararrayos                 | −0.1 dB          | +9.46 dBm         |
| Cable LMR-600 (50 ft)      | −2.21 dB         | +7.25 dBm         |
| Antena parabólica          | +25 dBi          | +32.25 dBm (EIRP) |
| FSPL (2 km)                | −106 dB          | −73.75 dBm        |
| Antena parabólica          | +25 dBi          | −48.75 dBm        |
| Cable LMR-600 (50 ft)      | −2.21 dB         | −50.96 dBm        |
| Pararrayos                 | −0.1 dB          | −51.06 dBm        |
| Cable LMR-600 (10 ft)      | −0.44 dB         | −51.5 dBm         |
| **Receptor (señal final)** |                  | **−51.5 dBm**     |

Si el threshold de receive sensitivity es −80 dBm, hay un margen de **28.5 dB** sobre el mínimo requerido → enlace exitoso.

**Fuente:** CWNA-107.md, Cap. 4 — _Link Budget_, Figura 4.4 y Tabla 4.5 (págs. 127–130, líneas ~6585–6720).

---

## 11. Fade Margin / System Operating Margin (SOM)

- **Fade Margin:** "colchón" de señal por encima del receive sensitivity, planificado durante el diseño para absorber fluctuaciones (interferencia, multipath, clima).
- **SOM (System Operating Margin):** medición real del colchón después de instalado el enlace.

Recomendaciones del libro:

| Escenario                               | Fade Margin recomendado                                                                                      |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Bridge outdoor punto a punto (largo)    | **20–25 dB** (compensa lluvia: ~0.05 dB/km en 2.4/5 GHz, multipath, clima)                                   |
| Indoor con multipath alto o ruido alto  | **5 dB** sobre el umbral del fabricante                                                                      |
| Indoor típico (best practice del libro) | Apuntar a cobertura ≥ **−70 dBm** para data rates altos; en entornos ruidosos **−65 dBm con 5 dB de margen** |

**Fuente:** CWNA-107.md, Cap. 4 — _Fade Margin / System Operating Margin_ y _When are Fade Margin Calculations Needed?_ (págs. 130–132, líneas ~6720–6800).

---

## Aplicabilidad al proyecto Heatmapper

| Concepto                                          | RP afectado       | Decisión / Implicación                                                                                                                                                                   |
| ------------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Componentes RF (IR vs EIRP)**                   | RP4, RP5          | Al modelar APs en planos, distinguir entre potencia configurada (IR/EIRP) y sus efectos. La IA debe permitir parametrizar antena y cableado del AP.                                      |
| **dBm como unidad universal**                     | RP1, RP3, RP4     | Toda la base de datos del proyecto **debe almacenar señales en dBm**. El RSSI crudo se guarda solo como valor auxiliar.                                                                  |
| **Regla de 10s y 3s**                             | RP3, RP5          | Útil para validaciones rápidas y para cálculos en backend de IA (estimar potencia tras atenuación de paredes).                                                                           |
| **Tabla dBm↔mW**                                  | —                 | Referencia para mostrar al usuario en el reporte exportado (RP6).                                                                                                                        |
| **Noise Floor**                                   | RP4               | Si la API expone ruido (Android lo expone parcialmente vía `ScanResult.frequency` + métricas WifiRtt), incluir en heatmap secundario. Reconocer que es estimado, no medido con espectro. |
| **SNR ≥ 25 dB / ≤ 10 dB**                         | RP3, RP4          | Definir capa "calidad SNR" en el heatmap: **verde ≥ 25, amarillo 10–25, rojo ≤ 10**.                                                                                                     |
| **SINR**                                          | RP4               | Si está disponible, capa adicional para visualizar interferencia instantánea.                                                                                                            |
| **Receive Sensitivity por data rate (Tabla 4.3)** | RP4, RP5          | El "área cubierta" depende del data rate objetivo. La IA (RP5) debe permitir configurar el data rate mínimo deseado (ej. 24 Mbps para voz, 6 Mbps para mera asociación).                 |
| **RSSI proprietary 0–255**                        | **RP1 (CRÍTICO)** | Almacenar tanto el `level` (dBm) como el RSSI crudo. Documentar en cada lectura el modelo del dispositivo Android para reproducibilidad.                                                 |
| **Link budget**                                   | RP5               | La IA debe sumar pérdidas por paredes (Tabla 3.1, ver `01-fundamentos-rf.md`) y FSPL para predecir señal en cada celda del plano.                                                        |
| **Fade Margin**                                   | RP4               | Definir **zona muerta = señal < −75 dBm** (umbral con 5 dB de margen sobre −70 dBm de cobertura recomendada). Marcar **alerta = señal entre −70 y −75 dBm**.                             |

---

**Siguiente archivo:** [`03-antenas.md`](03-antenas.md) — Patrones de radiación, beamwidth y selección de antenas (Cap. 5 + Cap. 13).
