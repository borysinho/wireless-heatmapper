# 04 — Diseño WLAN: cobertura, canales y capacidad

> Extracción del **Capítulo 13 — WLAN Design Concepts** del libro CWNA-107. Es el capítulo **central** para los requisitos RP4 (análisis de cobertura: dead zones, interferencia) y RP5 (sugerencias de IA para reubicación de APs).

**Fuente principal:** [CWNA-107.md](../CWNA-107.md), Cap. 13 — _WLAN Design Concepts_ (págs. 473–525, líneas ~14999–15800).

---

## 1. Calidad de señal recibida — Tabla 13.1

El criterio universal de diseño: garantizar **−70 dBm o mejor** en toda la zona objetivo, bien por encima del piso de ruido.

**Tabla 13.1 — Calidad de señal recibida:**

| Calidad                         | dBm         |
| ------------------------------- | ----------- |
| Muy fuerte                      | −30 dBm     |
| Muy fuerte                      | −40 dBm     |
| Muy fuerte                      | −50 dBm     |
| Muy fuerte                      | −60 dBm     |
| **Fuerte (objetivo de diseño)** | **−70 dBm** |
| Aceptable                       | −80 dBm     |
| Débil                           | −90 dBm     |
| Muy débil (≈ piso ruido)        | −95 dBm     |

> Una señal ≥ −70 dBm **garantiza generalmente** que el cliente use uno de los data rates más altos que soporta. Pero **la cobertura debe validarse desde la perspectiva del cliente**, no del AP, y con distintos tipos de cliente (la sensibilidad RSSI varía entre dispositivos).

**Fuente:** CWNA-107.md, Cap. 13 — _WLAN Coverage Design_, Tabla 13.1 (págs. 473–474, líneas ~15000–15045).

---

## 2. SNR para diseño

Recordatorio del Cap. 4 (ver `02-rssi-y-mediciones.md`):

| SNR mínimo | Aplicación                                |
| ---------- | ----------------------------------------- |
| 20 dB      | Datos generales                           |
| 25 dB      | **Voz (VoWiFi)**                          |
| 29 dB      | 802.11ac con 256-QAM (data rates máximos) |
| 35 dB      | 802.11ax con 1024-QAM (futuro)            |

> Para **voz** el libro recomienda diseñar para **−65 dBm o más fuerte** (no −70 dBm), de modo que aun con noise floor alto (−90 dBm) se mantenga SNR ≥ 25 dB. Recordar regla de 6 dB: −67 dBm tiene **la mitad de la potencia** de −64 dBm aprox.

**Fuente:** CWNA-107.md, Cap. 13 — _Signal-to-Noise Ratio_, Figura 13.2 (págs. 475–476, líneas ~15045–15090).

---

## 3. Dynamic Rate Switching (DRS)

A medida que un cliente se aleja del AP, **negocia data rates más bajos** (modulaciones menos complejas, más robustas). Si la señal cae por debajo de −70 dBm el cliente sigue conectado pero a menor tasa.

Implicaciones:

- Existe **correlación directa señal ↔ distancia ↔ data rate**.
- Las tasas bajas **consumen mucho más airtime** para entregar el mismo payload (efecto colateral negativo en toda la red).
- El AP **también hace DRS** en sentido downlink (no solo el cliente).
- Los thresholds son **propietarios** (vendor-dependent).
- **Estrategia preferida:** mejor diseñar para que el cliente roame a otro AP con buena señal antes que dejarlo bajar a tasas mínimas.

**Fuente:** CWNA-107.md, Cap. 13 — _Dynamic Rate Switching_, Figura 13.3 (págs. 476–478, líneas ~15090–15155).

---

## 4. Transmit Power — anti-patrón "AP a 100 mW"

> "APs at maximum transmit power will result in oversized coverage and not meet your capacity needs."

Best practices:

- **No** desplegar APs indoor a 100 mW, aunque lo soporten.
- Recomendación típica: **1/4 a 1/3 de la potencia máxima**.
- En alta densidad: hasta **1 mW**.
- APs a máxima potencia ↑ probabilidad de **CCI** y **sticky clients** → roaming malo.
- **Mismatch de potencia AP ↔ cliente** (cliente típicamente 15–20 mW vs AP 10 mW) genera CCI desde el cliente. **TPC (Transmit Power Control)** ayuda.

**Fuente:** CWNA-107.md, Cap. 13 — _Transmit Power_ (pág. 478, líneas ~15155–15185).

---

## 5. Roaming Design

- **El cliente decide cuándo roam**, no el AP. Lo dispara enviando una _reassociation request frame_.
- Triggers típicos: RSSI debilitándose + escuchar un AP alternativo más fuerte; también SNR, error rate, retransmisiones.
- Los thresholds son **propietarios**. Ejemplo: un VoWiFi phone puede roamear con +5 dB de diferencia hacia el nuevo AP, pero requerir +10 dB para volver al original (anti ping-pong).
- Algunos clientes (Intel) permiten ajustar la **agresividad de roaming**.
- Estándares relevantes: **802.11k** (radio resource measurement, neighbor reports), **802.11r** (fast BSS transition, FT — handoff seguro <150 ms para voz), **802.11v** (capacity-aware roaming). Wi-Fi Alliance: certificación **Voice-Enterprise**.

**Fuente:** CWNA-107.md, Cap. 13 — _Roaming Design_ (págs. 479–481, líneas ~15185–15280).

---

## 6. Cobertura primaria y secundaria — La "regla del 5 dB"

> **Mito desmentido por el libro:** la regla "15–30 % overlap entre celdas" es ambigua y poco útil porque las celdas reales son irregulares (forma de ameba), no círculos perfectos.

**Regla práctica recomendada (Keith Parsons):** desde cualquier punto del área cubierta, el cliente debe escuchar:

- 1 AP primario a ≥ **−65 dBm** (o el target de diseño)
- 1 AP secundario a **≥ −70 dBm** (es decir, dentro de 5 dB del primario)

Esto garantiza redundancia ante fallo de un AP y handoff suave.

**Anti-patrones detectables:**

- **Roaming dead zone:** el cliente no escucha un AP alternativo lo suficientemente fuerte → puede perder conectividad temporal.
- **Sticky clients:** el cliente escucha demasiados APs muy fuertes → no roamea aunque esté bajo otro AP. También causado por demasiada overlap.
- **Layer-3 roaming:** si el roaming cruza subredes IP, **el cliente pierde su IP** salvo que se use Mobile IP / túneles entre controladores.

**Fuente:** CWNA-107.md, Cap. 13 — _Primary and Secondary Coverage_ y _Layer 3 Roaming_ (págs. 481–485, líneas ~15280–15400).

---

## 7. Channel Design — ACI vs CCI

| Tipo                                    | Causa                                                                                         | Severidad                                                 | Solución                                              |
| --------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------- |
| **ACI — Adjacent Channel Interference** | Diseño incorrecto de canales (celdas vecinas en canales con overlap de frecuencia, ej. 1 y 3) | **Grave** — corrupción de tramas, retransmisiones layer-2 | Usar solo canales no solapados (1, 6, 11 en 2.4 GHz)  |
| **CCI — Co-Channel Interference**       | Múltiples APs en el **mismo** canal "se escuchan" → CSMA/CA hace que difieran transmisiones   | Moderado — pérdida de airtime, no corrupción              | Diseñar reuso espacial; en 2.4 GHz es casi inevitable |

> **Hecho clave (frecuentemente olvidado):** en CCI, el **cliente** es la causa principal (no los APs), porque está en posiciones impredecibles. Por eso CCI **siempre cambia con la movilidad**.

CCI también se llama **OBSS (Overlapping Basic Service Set)**.

**Fuente:** CWNA-107.md, Cap. 13 — _Adjacent Channel Interference_, _Co-Channel Interference_, Figuras 13.10–13.17 (págs. 485–491, líneas ~15400–15530).

---

## 8. Reuso 2.4 GHz — Patrón 1/6/11

- En 2.4 GHz **solo 3 canales** son non-overlapping según 802.11-2016 (separación de 25 MHz entre frecuencias centrales): **canales 1, 6 y 11**.
- Patrón típico: panal 1-6-11 reutilizado.
- En Europa el patrón 1-5-9-13 a veces se usa (4 canales, leve overlap), pero clientes norteamericanos no pueden transmitir en canal 13.
- **Pensar en 3D:** en edificios multi-piso, **escalonar los APs** entre pisos. No replicar el mismo patrón "cookie-cutter" piso a piso.

**Fuente:** CWNA-107.md, Cap. 13 — _2.4 GHz Channel Reuse_, Figuras 13.11–13.13 (págs. 486–489, líneas ~15440–15490).

---

## 9. Reuso 5 GHz

- Hasta **25 canales** disponibles según región (U-NII-1, U-NII-2A, U-NII-2C/E, U-NII-3).
- Reglas:
  1. Canales adyacentes (ej. 36 y 40) **sí** tienen leve overlap → dejar al menos un canal de separación.
  2. Distancia espacial entre celdas en mismo canal: al menos **dos celdas** de separación.
  3. **Usar la mayor cantidad posible de canales** → minimiza CCI (incluyendo CCI causada por clientes).
- **DFS channels (5.25–5.35 y 5.47–5.725 GHz):** deben **usarse cuando sea posible**. Razones para no habilitarlas: clientes legacy, o detección frecuente de radar.
- DFS workflow: AP escucha 60 s antes de transmitir; si detecta pulso de radar usa **CSA (Channel Switch Announcement)** para mover clientes. Tras detección debe esperar 30 min para volver al canal. _Zero-wait DFS_ (Broadcom) usa una cadena MIMO para escuchar mientras opera en otra.

**Fuente:** CWNA-107.md, Cap. 13 — _5 GHz Channel Reuse_ y _DFS Channels_ (págs. 492–497, líneas ~15490–15600).

---

## 10. Channel Bonding 40 MHz

- 802.11n introdujo bonding 20 + 20 → 40 MHz (doble bandwidth, doble data rate teórico).
- **Trade-offs:**
  - Menos canales disponibles → más CCI.
  - Noise floor +3 dB (SNR −3 dB) → puede bajar MCS rate.
  - 80 MHz / 160 MHz **no recomendados en enterprise** (no hay frecuencia suficiente).
- Reglas para bonding:
  - Usar 40 MHz **solo si DFS está habilitado** (más canales).
  - AP transmit power ≤ 12 dBm.
  - Paredes densas (concrete/brick atenúan ≥10 dB; drywall solo ~3 dB).
  - En multi-piso, evitar bonding salvo atenuación significativa entre pisos.

**Fuente:** CWNA-107.md, Cap. 13 — _40 MHz Channel Design_, Figuras 13.21–13.23 (págs. 497–499, líneas ~15600–15665).

---

## 11. RRM / Adaptive RF vs Configuración estática

- **RRM (Radio Resource Management):** asignación adaptativa y automática de canal y potencia por los APs basada en costos calculados (proprietary cada vendor).
- Activado por defecto en casi todos los vendors.
- **Pero RRM no reemplaza un diseño WLAN apropiado.** Un site survey predictivo o manual **siempre debe hacerse antes** del despliegue, y un _validation survey_ después.
- En entornos complejos (alta densidad, antenas direccionales), los propios vendors recomiendan usar **canales y potencia estáticos**.

**Fuente:** CWNA-107.md, Cap. 13 — _Static Channels and Transmit Power vs. Adaptive RF_ (págs. 500–501, líneas ~15665–15700).

---

## 12. Single-Channel Architecture (SCA) — alternativa

- Vendors: Fortinet, Allied Telesys, Ubiquiti.
- **Todos los APs en el mismo canal y compartiendo un BSSID virtual.**
- El cliente cree estar conectado a "un único AP" → **zero handoff time** (ideal para VoWiFi + 802.1X/EAP).
- Desventaja: capacidad limitada a un solo canal por "channel blanket".
- Hoy día menos relevante porque MCA + Voice-Enterprise (802.11r) ya da fast roaming.

**Fuente:** CWNA-107.md, Cap. 13 — _Single-Channel Architecture_ (págs. 501–504, líneas ~15700–15770).

---

## 13. Capacity Design — del "diseño por rango" al "diseño por capacidad"

Cambio de paradigma fundamental en Wi-Fi enterprise:

- **Antes:** "¿cuál es el rango del AP?" → poner la potencia al máximo, pocos APs.
- **Hoy:** densidad de clientes domina → **cell sizing** (más APs, cada uno con menor potencia).

### Niveles de densidad

| Categoría                    | Definición                                                                                      | Ejemplo                        |
| ---------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------ |
| **HD (High Density)**        | Default actual de casi cualquier WLAN: usuarios con varios devices, múltiples salas con paredes | Oficinas, hospitales, hoteles  |
| **VHD (Very High Density)**  | Mucha gente en **un único espacio abierto sin paredes**                                         | Auditorio, gimnasio, cafetería |
| **UHD (Ultra High Density)** | Decenas de miles de devices en el mismo espacio                                                 | Estadios, arenas               |

### Tabla 13.2 — Throughput por aplicación

| Aplicación           | Throughput requerido |
| -------------------- | -------------------- |
| Email / web browsing | 0.5 – 1 Mbps         |
| Impresión            | 1 Mbps               |
| Streaming SD         | 1 – 1.5 Mbps         |
| Streaming HD         | 2 – 5 Mbps           |

### Cálculo de capacidad

Heurísticas (Andrew von Nagy):

- AP "saturado" al **80 % de airtime utilization**.
- Devices por radio AP: $80 \div \text{(airtime por device)}$.
- Radios AP necesarios: $(\text{\# devices} \times \text{airtime\%}) \div 80\%$.

Regla práctica: **35–50 devices activos por radio** con uso medio (web/email).

### Tres preguntas clave (capacity planning)

1. **¿Qué aplicaciones?** (impacto directo en throughput requerido).
2. **¿Cuántos usuarios y devices, dónde?** (marcar zonas de alta densidad en el plano).
3. **¿Qué tipo de cliente?** (clientes 1×1:1 consumen mucho más airtime que 2×2:2 o 3×3:3).

**Fuente:** CWNA-107.md, Cap. 13 — _Capacity Design_, _High Density_, Tabla 13.2 (págs. 504–509, líneas ~15770–15920).

---

## 14. Band Steering y Load Balancing

- **Band Steering:** AP responde solo en 5 GHz a un cliente dual-band, "empujándolo" a 5 GHz. Útil porque por defecto los clientes prefieren la señal más fuerte (típicamente 2.4 GHz). Configurable también para balancear: ej. 55 % a 2.4 GHz / 60 % a 5 GHz.
- **Load Balancing entre APs:** AP sobrecargado **difiere la respuesta de asociación** → cliente intenta otro AP. Útil **solo en VHD sin necesidad de roaming** (auditorios). En entornos donde se requiere roaming es **contraproducente** (causa stickiness, bloqueo de reassoc).

**Fuente:** CWNA-107.md, Cap. 13 — _Band Steering_ y _Load Balancing_, Figuras 13.30–13.32 (págs. 510–514, líneas ~15920–16000).

---

## 15. Airtime Consumption — best practices anti-airtime

- **Deshabilitar data rates bajos:** un frame de 1500 bytes a 6 Mbps tarda 1250 µs vs 50 µs a 150 Mbps (**2500 % más airtime**).
- **Configurar basic rate alto:** 5 GHz → **24 Mbps** (12 Mbps mínimo, evitar 18 Mbps por bugs). Reduce 4× el airtime de management/control frames. 2.4 GHz → 24 Mbps si no hay 802.11b legacy (si hay → 11 Mbps).
- **Limitar SSIDs broadcast a 3–4 máximo.** Cada SSID adicional = más beacons + probe responses + overhead enorme.
- Otros tweaks: probe suppression, broadcast suppression, IPv6 suppression, client isolation.

**Fuente:** CWNA-107.md, Cap. 13 — _Airtime Consumption_, Figuras 13.33–13.36 (págs. 514–517, líneas ~16000–16085).

---

## 16. Voice vs Data — Tabla 13.3

| IP Voice                                      | IP Data                      |
| --------------------------------------------- | ---------------------------- |
| Paquetes pequeños y de tamaño uniforme        | Paquetes de tamaño variable  |
| Entrega regular y predecible                  | Entrega "bursty"             |
| Muy afectado por entrega tardía/inconsistente | Mínimamente afectado         |
| **"Better never than late"**                  | **"Better late than never"** |

VoWiFi requiere:

- Retransmisiones layer-2 ≤ 5 % (datos toleran ≤ 10 %).
- Pérdida IP ≤ 2 %.
- Diseño con **−65 dBm** o mejor.
- Recomendación: **deploy voz solo en 5 GHz**.

**Fuente:** CWNA-107.md, Cap. 13 — _Voice vs. Data_, Tabla 13.3 (págs. 517–519, líneas ~16085–16140).

---

## 17. Dual 5 GHz y Software-Defined Radios (SDR)

- En alta densidad es común **deshabilitar 60–75 % de los radios 2.4 GHz** (o convertirlos en _sensor mode_ para detección de rogue APs).
- APs modernos integran **un radio fijo 5 GHz + un SDR** que puede operar como 2.4 o como **otra instancia 5 GHz**.
- Ventaja: ofrecer **2 canales 5 GHz por AP** → más capacidad real.
- Reglas:
  - Solo **20 MHz** (no bonding) en dual-5 GHz.
  - **DFS habilitado** (necesitas más canales).
  - **Separación 60–100 MHz** entre los dos canales del mismo AP (ver Tabla 13.4).
  - Pareo recomendado: AP1 = 36+100, AP2 = 40+104, AP3 = 44+108, …

**Fuente:** CWNA-107.md, Cap. 13 — _Dual 5 GHz and Software-Defined Radios_, Tabla 13.4 (págs. 519–521, líneas ~16140–16210).

---

## Aplicabilidad al proyecto Heatmapper

| Concepto                                  | RP afectado  | Decisión / implicación                                                                                                                                                                     |
| ----------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Tabla 13.1 (calidad −30…−95 dBm)**      | RP3, **RP4** | Usar como leyenda del heatmap. Colores por rango: muy fuerte (verde oscuro), fuerte (verde), aceptable (amarillo), débil (naranja), muy débil (rojo).                                      |
| **Threshold −70 dBm**                     | **RP4**      | Definir como **límite de cobertura "buena"** en la app. Por debajo de −70 dBm marcar como zona de degradación.                                                                             |
| **Threshold −65 dBm para voz**            | RP4          | Modo "VoWiFi": permitir al usuario seleccionar criterio más estricto si la red está pensada para voz.                                                                                      |
| **DRS y data-rate inferido por señal**    | RP3, RP4     | Reportar al usuario un **data rate estimado** por celda interpolada usando Tabla 4.3 (ver `02-rssi-y-mediciones.md`).                                                                      |
| **Regla del 5 dB primario/secundario**    | RP4, RP5     | **Algoritmo de RP4:** para cada punto, identificar el AP más fuerte y verificar que exista al menos otro AP a ≤ 5 dB de diferencia. Si no, marcar "single-coverage" (riesgo de pérdida).   |
| **ACI vs CCI**                            | RP4, **RP5** | RP5 (IA) debe **proponer canales 1/6/11** en 2.4 GHz y reuso espacial en 5 GHz. Detectar APs vecinos en mismo canal o canales adyacentes con overlap → flag "interferencia configuración". |
| **Pensar en 3D (multi-piso)**             | RP2, RP4     | Si Heatmapper soporta múltiples plantas, **no** asumir que la cobertura del piso N es igual a piso N+1. Cada piso necesita su propio site survey y su propio heatmap.                      |
| **Reuso 5 GHz: separar canales**          | RP5          | IA debe respetar mínimo 1 canal de separación entre APs vecinos. Preferir incluir DFS channels en el plan.                                                                                 |
| **AP a max power = anti-pattern**         | RP5          | IA **no** debe aumentar potencia automáticamente para "tapar" zonas muertas; preferir agregar un AP nuevo o reubicar.                                                                      |
| **Cell sizing (más APs, menos potencia)** | RP5          | Modelo de IA: optimizar por número y posición de APs antes que por potencia. Permitir como input el número máximo de APs disponibles.                                                      |
| **Tabla 13.2 throughput por app**         | RP5, RP6     | Permitir al usuario declarar perfil de uso (oficina, streaming, voz) → el reporte (RP6) calcula si la cobertura actual soporta el throughput requerido por punto.                          |
| **Densidad: HD/VHD/UHD**                  | RP5          | Detectar zonas de alta densidad de mediciones o usuarios reportados → recomendar patch antennas MIMO en techo (ver `03-antenas.md`).                                                       |
| **VHD requiere directional antennas**     | RP5          | Anti-recomendación: en auditorios, NO sugerir omni adicional; sugerir patch sectorial.                                                                                                     |
| **Disable basic rate bajos**              | RP5, RP6     | Reporte (RP6) puede incluir recomendación: "Habilitar basic rate 24 Mbps en 5 GHz, ≤ 4 SSIDs".                                                                                             |
| **Layer-3 roaming**                       | —            | Fuera del scope del proyecto (no se mide IP, solo RF).                                                                                                                                     |

---

**Anterior:** [`03-antenas.md`](03-antenas.md) · **Siguiente:** [`05-site-survey.md`](05-site-survey.md)
