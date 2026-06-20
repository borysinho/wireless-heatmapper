# 03 — Antenas: patrones de radiación, beamwidth y tipos

> Extracción de conceptos del **Capítulo 5 — Radio Frequency Signal and Antenna Concepts** del libro CWNA-107, complementado con notas de antenas MIMO indoor del Cap. 13. Aplica principalmente a RP4 (interpretación de cobertura) y RP5 (sugerencias de IA para reubicación de APs).

**Fuentes principales:**

- [CWNA-107.md](../CWNA-107.md), Cap. 5 — _Radio Frequency Signal and Antenna Concepts_ (págs. 141–170, líneas ~6500–7100).
- [CWNA-107.md](../CWNA-107.md), Cap. 13 — _WLAN Design Concepts_, sección de antenas (líneas ~16800–17050).

---

## 1. Polar Charts: Azimuth (H-plane) y Elevation (E-plane)

Los fabricantes documentan el patrón de radiación de una antena con **dos gráficos polares**:

- **Azimuth chart (H-plane / vista superior):** patrón visto desde arriba. Indica cobertura horizontal.
- **Elevation chart (E-plane / vista lateral):** patrón visto de lado. Indica cobertura vertical (qué tanto "se cae" la señal hacia pisos superiores/inferiores).

Los gráficos polares son **logarítmicos** por defecto, donde cada anillo concéntrico representa típicamente 5 o 10 dB. Recordar la **regla de los 6 dB**: una caída de 6 dB significa **la mitad de distancia útil**; una caída de 10 dB equivale a **~70 % menos distancia útil**.

> **Implicación para visualizar heatmap:** si se modela una antena en software, los lóbulos secundarios que se ven grandes en el chart logarítmico son en realidad insignificantes en el chart lineal (cobertura real). No sobreestimar la cobertura "lateral" o "trasera" de una antena dirigible.

**Fuente:** CWNA-107.md, Cap. 5 — _Polar Charts_ y Figuras 5.4–5.5 (págs. 145–147, líneas ~6700–6735).

---

## 2. Beamwidth (Ancho de haz)

El **beamwidth** mide qué tan focalizada está la radiación de una antena. Se mide tanto **horizontalmente** como **verticalmente**, en grados, entre los dos puntos donde la señal cae **−3 dB respecto al máximo** (los llamados _half-power points_).

A menor beamwidth → mayor ganancia y mayor distancia, pero menor área cubierta.

**Fuente:** CWNA-107.md, Cap. 5 — _Beamwidth_ y Figuras 5.6–5.7 (págs. 147–148, líneas ~6735–6790).

---

## 3. Tabla 5.1 — Beamwidth típico por tipo de antena

| Tipo de antena        | Beamwidth horizontal (°) | Beamwidth vertical (°) |
| --------------------- | ------------------------ | ---------------------- |
| **Omnidireccional**   | 360                      | 7 a 80                 |
| **Patch / Panel**     | 30 a 180                 | 6 a 90                 |
| **Yagi**              | 30 a 78                  | 14 a 64                |
| **Sectorial**         | 60 a 180                 | 7 a 17                 |
| **Parabólica (dish)** | 4 a 25                   | 4 a 21                 |

**Fuente:** CWNA-107.md, Cap. 5 — Tabla 5.1 (pág. 149, líneas ~6790–6800).

---

## 4. Categorías de antenas

### 4.1 Omnidireccionales

- Radian RF en todas direcciones (analogía: lámpara de techo).
- El ejemplo clásico es la **dipolo de media onda** ("rubber duck"), por defecto en muchos APs, con ganancia ~2.14 dBi.
- A mayor ganancia (5 dBi, 9 dBi…), el patrón se "aplana": **se incrementa la cobertura horizontal pero se reduce la vertical**.
- **Indoor:** uso típico con ganancia baja (~2.14 dBi). Una antena omni de alta ganancia en planta baja **puede dejar sin señal a pisos superiores**.
- Aplicación principal: punto-a-multipunto desde el centro de la cobertura.

**Fuente:** CWNA-107.md, Cap. 5 — _Omnidirectional Antennas_ y Figuras 5.8–5.10 (págs. 150–153, líneas ~6800–6925).

### 4.2 Semidireccionales (Patch, Panel, Yagi)

- Dirigen la señal hacia una zona específica.
- **Patch / Panel (planar):** uso indoor en pasillos largos (bibliotecas, almacenes, retail con estanterías altas) montadas alto en pared, apuntando a lo largo del pasillo. Típicamente alternadas en paredes opuestas.
- **Yagi:** point-to-point de corta a media distancia (hasta ~2 millas / 3.2 km).
- Ventaja: pueden montarse altas y **inclinarse hacia abajo** (down-tilt) sin afectar el lado contrario, cosa que no se puede con omni.

**Fuente:** CWNA-107.md, Cap. 5 — _Semidirectional Antennas_ (págs. 153–155, líneas ~6925–6985).

### 4.3 Altamente direccionales (Parabólica, Grid)

- Para enlaces punto a punto de larga distancia (bridging entre edificios).
- Beamwidth muy estrecho (4–25°) y ganancia alta.
- Sensibles a vibración por viento (_wind loading_); en zonas ventosas se prefiere antena tipo **grid** (rejilla) o usar **radome**.

**Fuente:** CWNA-107.md, Cap. 5 — _Highly Directional Antennas_ y Figura 5.14 (págs. 155–157, líneas ~6985–7035).

### 4.4 Sectoriales

- Antenas semidireccionales de alta ganancia (~10 dBi) con patrón "porción de pizza".
- Se montan back-to-back para formar un _sectorized array_ que provee 360° de cobertura, pero con ventajas sobre una omni:
  1. Cada sector puede inclinarse de forma independiente al terreno.
  2. Cada sector usa un transceiver propio → **transmiten en simultáneo** → mayor throughput agregado.
  3. Mayor ganancia que una omni equivalente.
- Uso típico: torres de telefonía celular; en Wi-Fi: stadiums, WISPs, deployments outdoor.

**Fuente:** CWNA-107.md, Cap. 5 — _Sector Antennas_ (págs. 157–158, líneas ~7035–7080).

---

## 5. Antenna Arrays y Beamforming

Tres tipos de beamforming:

- **Static beamforming:** patrón de radiación fijo; se logra agrupando antenas direccionales (sectorized array indoor, ej. APs Riverbed/Xirrus).
- **Dynamic beamforming (beamsteering / smart antennas):** la antena adapta su patrón **frame-por-frame** dirigiendo la energía al cliente activo. Las tramas broadcast (beacons) se mantienen omnidireccionales. **No disponible en el lado cliente.**
- **Transmit Beamforming (TxBF):** definido en 802.11n y formalizado en 802.11ac. No es realmente una técnica de antena, sino **DSP**: se transmite la misma señal en distintas antenas con desfases controlados para que **lleguen en fase** al receptor, emulando una antena unidireccional de mayor ganancia.

**Fuente:** CWNA-107.md, Cap. 5 — _Antenna Arrays_ y _Transmit Beamforming_ (págs. 158–160, líneas ~7080–7130).

---

## 6. MIMO y antenas patch indoor (relevante para alta densidad)

Antes de MIMO (legacy 802.11a/b/g), las antenas patch/panel indoor se usaban para **reducir multipath** (interpretado como dañino).

Con **MIMO** (802.11n/ac), el multipath es **constructivo** (Maximal Ratio Combining) y las antenas patch dejan de ser necesarias para ese propósito. **Pero**:

> Las **antenas patch MIMO** se siguen usando indoor con un objetivo distinto: **proveer cobertura sectorizada en entornos de alta densidad** (gimnasios escolares, salas de conferencia, auditorios). Se montan en techo o pared apuntando hacia abajo, generando "sectores" estrechos de cobertura para servir muchos clientes en poco espacio.

**Fuentes:** CWNA-107.md, Cap. 5 — discusión MIMO patch (pág. 154, líneas ~6960–6975); Cap. 13 — uso indoor de patch MIMO en alta densidad (líneas ~16800–16900).

---

## 7. Visual LoS, RF LoS y Zona de Fresnel (relevante a planos arquitectónicos)

Para enlaces **point-to-point**, no basta con tener línea de vista óptica (Visual LoS): debe mantenerse libre la **zona de Fresnel** (zona elipsoidal alrededor del LoS).

- **Regla práctica:** **no permitir que ningún obstáculo encroach más de 40 %** dentro de la primera zona de Fresnel.
- Recomendación del libro: dejar **60 % de despeje** como mínimo, especialmente en zonas arboladas (los árboles crecen).

> Para Heatmapper esto es relevante si el plano del edificio incluye antenas direccionales hacia el exterior (enlaces inter-edificio). **Para cobertura indoor general, este concepto se aplica de forma indirecta**: paredes y obstáculos dentro del primer "área de Fresnel" entre AP y cliente reducen señal incluso si el LoS visual existe.

**Fuente:** CWNA-107.md, Cap. 5 — _Visual Line of Sight_, _RF Line of Sight_, _Fresnel Zone_ y Figuras 5.16–5.17 (págs. 160–162, líneas ~7140–7250).

---

## Aplicabilidad al proyecto Heatmapper

| Concepto                                                    | RP afectado  | Decisión / implicación                                                                                                                                                                                                                                       |
| ----------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Patrón de antena (azimuth + elevation)**                  | RP4, **RP5** | El modelo de IA para sugerir reubicación de APs (RP5) **debe permitir parametrizar el tipo de antena** del AP (omni 2.14 dBi por defecto, patch, etc.). Modelar la radiación isotrópica como aproximación inicial es aceptable, pero documentar el supuesto. |
| **Beamwidth y half-power points**                           | RP4          | Cuando se estima un radio de cobertura, recordar que **el "alcance" en el plano horizontal depende de la elevación** del AP. Una omni de alta ganancia montada en techo cubre mucho menos directamente debajo que una omni de baja ganancia.                 |
| **Tabla 5.1 (beamwidth por tipo)**                          | RP5          | Catálogo de antenas que la IA puede ofrecer: omni 2.14 dBi (default), patch indoor 60–90°, sectorial outdoor.                                                                                                                                                |
| **Omni montada en planta baja → no cubre pisos superiores** | RP4          | Caso de uso explícito: detectar si la app está siendo usada en un edificio multi-piso con una sola omni en piso 1 → recomendar AP adicional en pisos superiores.                                                                                             |
| **Patch / panel para pasillos largos**                      | RP5          | Si el plano del usuario muestra **pasillos largos con estanterías** (almacén, biblioteca), la IA debería sugerir patch antennas alternadas en paredes en vez de omni en el centro.                                                                           |
| **Patch MIMO para alta densidad indoor**                    | RP5          | Detectar áreas de alta densidad de usuarios (auditorios, aulas grandes) → sugerir patch MIMO en techo apuntando hacia abajo, no omnis adicionales.                                                                                                           |
| **Beamforming dinámico (smart antennas)**                   | RP1, RP4     | El RSSI medido por el cliente puede variar fuertemente entre frames si el AP usa beamsteering. **Promediar varias muestras por punto** durante la captura, no fiarse de una sola lectura instantánea.                                                        |
| **Zona de Fresnel**                                         | RP3, RP4     | Para interpolación, considerar que paredes en la línea AP-cliente atenúan no solo por bloqueo directo sino también por difracción en la zona elipsoidal. La aproximación simple "log-distance + atenuación de paredes" es razonable como modelo inicial.     |
| **Wind loading**                                            | —            | No aplica en deployment indoor del Heatmapper.                                                                                                                                                                                                               |

---

**Anterior:** [`02-rssi-y-mediciones.md`](02-rssi-y-mediciones.md) · **Siguiente:** [`04-diseno-wlan.md`](04-diseno-wlan.md)
