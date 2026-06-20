# 05 — Site Survey y validación: la metodología WiFi profesional

> Extracción del **Capítulo 14 — Site Survey and Validation** del libro CWNA-107. Este capítulo es **el más importante** para validar la metodología completa del proyecto Heatmapper: lo que la app hace **es exactamente** un site survey híbrido (medición + visualización + reporte), por lo que cada sección de este capítulo aterriza directamente sobre uno o más requisitos RP1–RP6.

**Fuente principal:** [CWNA-107.md](../CWNA-107.md), Cap. 14 — _Site Survey and Validation_ (págs. 537–584, líneas ~16258–17050).

---

## 1. Entrevista de site survey y diseño

> "Setenta y cinco por ciento del trabajo de una buena red inalámbrica está en el pre-engineering."

Antes de cualquier medición, debe ocurrir una **entrevista con los stakeholders** para identificar objetivos, requisitos y metas de la WLAN. Sin esto, el survey produce datos sin contexto.

**Customer Briefing** — explicar: ventajas/limitaciones de Wi-Fi, que el throughput agregado es **≤ 50 % del data rate anunciado**, que es half-duplex compartido, y por qué se necesita un site survey.

### Categorías de preguntas a documentar

| Categoría                       | Preguntas clave                                                                                                                                                             |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Business Requirements**       | ¿Cuál es el propósito de la WLAN? ¿Qué aplicaciones? ¿Quiénes son los usuarios? ¿Qué dispositivos (laptops, handhelds, BYOD, IoT)? ¿Restricciones estéticas o de montaje?   |
| **Capacity and Coverage**       | ¿Dónde se requiere cobertura? (no asumir "everywhere"). Aplicaciones, número de usuarios y devices, picos on/off, capacidades MIMO de los clientes, devices legacy.         |
| **Existing WLAN**               | ¿Cuáles son los problemas actuales? ¿Fuentes conocidas de interferencia RF? ¿Dead zones conocidas? ¿Existe documentación de un survey anterior? ¿Qué equipo está instalado? |
| **Infrastructure Connectivity** | Roaming requerido (capa 2 vs capa 3), wiring closets ≤ 100 m, switches (PoE 802.3af/at, VLANs, port speed), naming convention, RADIUS/LDAP, MDM/BYOD, IPv6.                 |
| **Security Expectations**       | Encriptación, AAA, WIDS/WIPS, regulaciones (HIPAA, PCI, FIPS 140-2, GDPR).                                                                                                  |
| **Guest Access**                | SSID separado, VLAN, firewall, captive portal, self-registration.                                                                                                           |
| **Aesthetics**                  | Indoor APs con antenas internas, encoframientos, APs camuflados.                                                                                                            |
| **Outdoor Surveys**             | Lightning, snow/ice, NEMA enclosures, FCC/FAA si > 200 ft / cerca de aeropuerto.                                                                                            |

**Fuente:** CWNA-107.md, Cap. 14 — _WLAN Site Survey and Design Interview_ (págs. 537–548, líneas ~16258–16455).

---

## 2. Mercados verticales — consideraciones por industria

| Vertical                         | Consideración crítica                                                                                                                                                                                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Government**                   | Seguridad (FIPS 140-2), credenciales, exportación AES restringida en algunos países.                                                                                                                                                                               |
| **Education (K–12 / Higher Ed)** | Programas 1:1 (1 tablet por estudiante) → alta densidad. APs en cada aula puede ser correcto **o incorrecto** según el caso. Materiales densos (cinderblock, brick) atenúan mucho.                                                                                 |
| **Healthcare**                   | **Interferencia biomédica** (cauterizadores, equipos ISM-band). Tarea: reunirse con el departamento biomédico. **Pasillos largos, múltiples pisos, salas de rayos X con plomo, vidrios con malla.** Voz (VoWiFi para enfermería) y RTLS (RFID activo) son comunes. |
| **Retail**                       | Interferencia 2.4 GHz (cordless phones, baby monitors en demo). Inventario en racks → atenuación. Encuestar en temporada alta.                                                                                                                                     |
| **Warehouses / Manufacturing**   | Antenas direccionales por techos altos y racks metálicos. Cercas chain-link bloquean RF. Roaming obligatorio (montacargas, scanners). En manufactura: clean rooms, equipos de seguridad, sindicatos.                                                               |
| **Multi-Tenant Buildings**       | WLANs vecinas mal configuradas (canales no estándar 2/8, bonding 40/80 MHz). Planeación cuidadosa de canal y potencia.                                                                                                                                             |

**Fuente:** CWNA-107.md, Cap. 14 — _Vertical Market Considerations_ (págs. 548–551, líneas ~16455–16550).

---

## 3. Survey legacy: AP-on-a-stick

Método tradicional: montar temporalmente un AP (con batería, en trípode), medir la zona de cobertura caminando, mover el AP al siguiente lugar, repetir.

> Sigue siendo efectivo, pero es **muy consume tiempo y costoso**. Hoy se prefiere el método híbrido (sección 7).

**Fuente:** CWNA-107.md, Cap. 14 — _Legacy AP-on-a-Stick Survey_ (págs. 551–559, líneas ~16550–16700).

---

## 4. Spectrum Analysis (análisis del espectro)

> "Si el background noise excede −85 dBm en cualquier banda, el rendimiento de la WLAN se degrada severamente."

**Por qué es necesario:**

- Datos corruptos → CRC falla → no ACK → retransmisión.
- Si las retransmisiones layer-2 superan **10 %**, el throughput sufre seriamente.
- Aplicaciones IP de tiempo real requieren pérdida IP ≤ **1 %**, retransmisiones layer-2 ≤ **10 %** (preferible ≤ 5 % para VoIP).
- Un interferer con amplitud fuerte puede hacer que el AP **difiera transmisión indefinidamente** (CCA siempre ocupado).

### Fuentes de interferencia

**2.4 GHz ISM:**

- Microondas (incluso 0.0000001 % de fuga = interferencia)
- Cordless phones DSSS/FHSS 2.4 GHz
- Bombillas fluorescentes
- Cámaras de video 2.4 GHz, baby monitors
- Motores de elevadores
- Cauterizadores médicos, cortadores de plasma
- Bluetooth (mouse, keyboard, headsets)

**5 GHz U-NII:**

- Cordless phones 5 GHz
- Radar
- Sensores de perímetro
- Satélite digital
- WLANs 5 GHz vecinas
- Bridges 5 GHz outdoor
- LTE no licenciado

**Conclusión clave:** un buen survey **siempre** incluye spectrum analysis con un analizador real (ej. MetaGeek Wi-Spy DBx, Ekahau Sidekick), **no** solo con un escáner Wi-Fi.

**Fuente:** CWNA-107.md, Cap. 14 — _Spectrum Analysis_ (págs. 551–555, líneas ~16550–16640).

---

## 5. Coverage Analysis — procedimiento −70 dBm

Procedimiento canónico para encontrar la ubicación óptima de los APs:

### Configuración inicial

- Potencia inicial recomendada: **25 mW** (NO 100 mW).
- Medir con la **radio 5 GHz** (rango menor → es el limitante).
- Threshold: **−70 dBm** (datos generales) o **−65 dBm** (voz).

### Procedimiento

1. Colocar AP en la **esquina del edificio**.
2. Caminar diagonalmente hacia el centro hasta que la señal caiga a **−70 dBm** → ahí va el **primer AP**.
3. Montar temporalmente el AP allí y caminar para encontrar todos los **cell edges** (−70 dBm).
4. Ajustar potencia o reubicar si la celda es muy grande/pequeña.
5. Para el **siguiente AP**: desde el AP1, caminar paralelo al borde del edificio hasta el punto −70 dBm. Desde ese punto seguir caminando hasta el **siguiente** −70 dBm → ahí va el **AP2**.
6. **Daisy-chain** este procedimiento por todo el edificio.

> **Crítica del libro a la regla "15–30 % overlap":** "no hay forma de medir overlap". Lo que importa es que **cada cliente vea siempre ≥ 2 APs ≥ −70 dBm** (primario + secundario, ver Cap. 13 sección 6 en `04-diseno-wlan.md`).

### Mediciones obligatorias en el cell edge

- **RSSI** (dBm) — también llamado RSL (Received Signal Level)
- **Noise level** (dBm)
- **SNR** (dB) — mínimo 20 dB datos, 25 dB voz

### Survey manual: pasivo vs activo

| Tipo        | Característica                                      | Mide                                                                                |
| ----------- | --------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Passive** | Cliente NO asociado al AP                           | Layer 1: RSSI, noise floor, SNR. Información de management/control frames a layer 2 |
| **Active**  | Cliente asociado al AP, ICMP pings, frames de datos | Todo lo del passive **+** packet loss, retransmisión layer-2 %                      |

> Práctica recomendada: hacer **ambos** y mergear los reportes.

**Fuente:** CWNA-107.md, Cap. 14 — _Coverage Analysis_, _Passive Manual Survey_, _Active Manual Survey_, Figs. 14.4–14.7 (págs. 555–560, líneas ~16640–16700).

---

## 6. Survey Híbrido — proceso moderno

> "La mayoría de los profesionales WLAN usan el método híbrido."

**Premisa:** usar **software de análisis predictivo RF** para modelar la cobertura. La precisión del modelo predictivo depende de qué tan bien se caracterice el ambiente. El proceso tiene 4 fases:

### 6.1 Initial Site Visit

- Visitar el sitio con copias del floor plan (laptop/tablet).
- Asegurar acceso a todas las áreas (escolta de seguridad si aplica).
- Para sitios públicos: necesario un segundo asistente (no se puede dejar el equipo).

### 6.2 Spectrum Analysis

Igual que sección 4 anterior — barrer **todo el sitio**.

### 6.3 Attenuation Spot Checks (clave)

En lugar de hacer cobertura full, se **caracteriza la atenuación de cada tipo de pared** en el edificio.

**Procedimiento de medición FSPL ↔ atenuación de pared:**

1. Montar AP temporalmente en una habitación, potencia media, canal 5 GHz, 20 MHz.
2. **Primera medición (FSPL):** medir RSSI a **5 m del AP, 1 m antes de la pared**, sin obstrucciones. Ej: −60 dBm.
3. **Segunda medición:** ir **al otro lado de la misma pared**, a 1 m. Ej: −72 dBm.
4. **Atenuación de la pared = |Medición1| − |Medición2| = 12 dB** en el ejemplo.

Repetir para cada tipo de pared (drywall, concrete, glass, metal). Documentar en el floor plan. **Estos valores alimentan el modelo predictivo.**

### 6.4 Building and Infrastructure Observation

- Observar techo: drop ceiling tiles vs plaster vs beams expuestos.
- Anotar dificultad para correr cable Ethernet.
- ¿APs deben ser ocultados? ¿Restricciones de montaje?
- **Tomar muchas fotos bien documentadas** — sirven para predictive design Y para la validation survey.

**Fuente:** CWNA-107.md, Cap. 14 — _Hybrid Survey_ (págs. 560–563, líneas ~16704–16804).

---

## 7. Predictive Design — herramientas y workflow

Productos comerciales conocidos:

- **Ekahau Site Survey** (líder del mercado)
- **iBwave Wi-Fi Suite**
- **AirMagnet Survey**
- **TamoGraph Site Survey**

### Workflow

1. **Importar floor plan** (.dwg, .dwf vector; o .bmp, .jpg, .tif raster). Escala correcta es **crítica**. Para multi-piso: alinear plantas + especificar atenuación entre pisos.
2. **Dibujar paredes** sobre el plano. La aplicación trae valores predeterminados de atenuación para drywall, concreto, vidrio, etc. Permitir override con valores custom (los del attenuation spot check).
3. **Colocar APs** en el plano. Especificar make/model exacto (cada AP tiene su patrón de antena propio) y potencia.
4. **El motor genera el modelo:**
   - Channel reuse pattern
   - Cell coverage boundaries (heatmap)
   - AP placement
   - AP power settings
   - Número de APs requeridos
   - CCI predicha
5. **Iterar** AP locations / channels / powers hasta cumplir requirements.
6. **Output:** heatmap visual + Bill of Materials (BoM) + lista de antenas externas.

**Fuente:** CWNA-107.md, Cap. 14 — _Predictive Design_, Fig. 14.9 (págs. 563–565, líneas ~16704–16804).

---

## 8. Validation Survey — auditoría post-instalación

> "Una parte que a menudo se omite. Después de instalar, **antes de poner en servicio**, validar que la WLAN cumple los objetivos."

**Procedimiento:** caminar sistemáticamente todo el sitio tomando mediciones RF + de red, registrarlas sobre el floor plan, comparar con el diseño previsto.

**Cuándo se hace:**

- Después de la instalación inicial (validación contra plan).
- Cuando el rendimiento se degrada en producción (diagnóstico).

**Sensibilidad RSSI varía entre dispositivos** → conviene validar con varios tipos de cliente (handheld profesional **+** smartphone consumer).

### Métricas a validar

| Métrica                   | Objetivo / herramienta                                                                                                                                         |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cobertura**             | ≥ −70 dBm, SNR ≥ 20 dB (datos) / 25 dB (voz).                                                                                                                  |
| **Capacity / Throughput** | Test bidireccional cliente↔servidor con **iPerf** (CLI, open-source, integrado en muchos APs) o **TamoSoft Throughput Test** (GUI, free, Win/Mac/iOS/Android). |
| **Roaming**               | Validar handoff transparente, especialmente con 802.1X/EAP (FT). Herramientas handheld traen test de roaming integrado.                                        |
| **Delay (Latency)**       | Crítico para VoIP/streaming.                                                                                                                                   |
| **Jitter**                | Variación del latency. WLAN con retransmisiones altas → jitter alto → audio/video choppy. Target: < 5 % retx (VoIP), idealmente 2 %.                           |
| **Connectivity**          | Wired infra debe soportar la carga, segmentación, routing, PoE.                                                                                                |
| **Aesthetics**            | Verificar montaje limpio, profesional.                                                                                                                         |

**Herramientas validation handheld:** ej. **NetScout AirCheck G2** — ruggedized, identifica APs/clientes, SSIDs, RF, security, traffic.

**Fuente:** CWNA-107.md, Cap. 14 — _Validation Survey_ (págs. 565–569, líneas ~16804–16866).

---

## 9. Site Survey Tools — toolkit indoor

| Herramienta                        | Uso                                                                                      |
| ---------------------------------- | ---------------------------------------------------------------------------------------- |
| **Spectrum analyzer**              | Análisis de espectro 2.4 + 5 GHz                                                         |
| **Blueprints / floor plans**       | Mapear cobertura, marcar mediciones                                                      |
| **Signal strength software**       | Coverage analysis (en laptop, tablet, smartphone, o handheld validation tool)            |
| **WLAN client**                    | Laptop / smartphone / handheld validation (NetScout AirCheck G2)                         |
| **Access Point**                   | Idealmente del **mismo vendor** que se desplegará (cada vendor implementa RSSI distinto) |
| **WLAN Controller**                | Versión "branch office" pequeña (2 lb vs 30 lb del core)                                 |
| **Battery pack**                   | Para alimentar el AP sin extensiones eléctricas                                          |
| **Binoculars**                     | Útiles en warehouses altos y plenum spaces                                               |
| **Flashlight**                     | Esquinas oscuras, plenum                                                                 |
| **Walkie-talkies / cell phones**   | Comunicación entre encuestadores en pisos distintos                                      |
| **Antennas**                       | Indoor omni / direccionales (cada vez menos por antenas integradas)                      |
| **Temporary mounting**             | Bungee cords, ties, duct tape, **tripods/masts** (ej. HiveRadar, hasta 9 ft)             |
| **Digital camera**                 | Documentar ubicación exacta de cada AP, también sirve como "binoculares" con zoom        |
| **Measuring wheel / laser**        | Validar que cada AP esté ≤ 100 m de cable al closet                                      |
| **Markers (cinta de color, dots)** | Marcar dónde se montará el AP final                                                      |
| **Ladder / forklift**              | Para montar APs en techos altos                                                          |

> Regla crítica: **conducir el survey con el mismo hardware AP del vendor que se va a desplegar**. NO sobrevés con vendor X y despliegues con vendor Y.

**Fuente:** CWNA-107.md, Cap. 14 — _Indoor Site Survey Tools_, Fig. 14.12 (págs. 569–572, líneas ~16866–16970).

---

## 10. Site Survey Tools — toolkit outdoor

Para outdoor (mesh, bridging punto-a-punto):

- **Topographic map** (en lugar de blueprint)
- **Link analysis software** (predictive)
- **Calculadoras**: link budget, Fresnel, FSPL, fade margin, atenuación de cable (VSWR)
- **Maximum tree growth data** (la vegetación crece y obstruye el Fresnel)
- **Binoculars** (visual line of sight, no equivale a RF LOS)
- **Walkie-talkies / cell phones** (links de hasta 1 mi+)
- **Signal generator + wattmeter** (testear cables y conectores)
- **Variable-loss attenuator** (simular distintas longitudes de cable)
- **Inclinometer** (altura de obstáculos)
- **GPS** (lat/lon de sitios y obstrucciones)
- **Digital camera** con zoom largo
- **Spectrum analyzer** (RF ambient en sitios de TX)
- **Spotlight 3M-candle / sunlight reflector** (apuntar al sitio remoto distante)

**Fuente:** CWNA-107.md, Cap. 14 — _Outdoor Site Survey Tools_ (págs. 572–574, líneas ~16970–17000).

---

## 11. Documents, Forms y Deliverables

### Documentación obtenida del cliente (pre-survey)

- **Blueprints** (digitales preferible, vector format para predictive). Si no existen: arquitecto, city hall, fire department, fire-escape plan a escala, o dibujar a mano.
- **Topographic map** (si es outdoor)
- **Network topology map** (wired + layer 3 boundaries) — puede requerir NDA
- **Security credentials** (badges, escolta)

### Checklists del survey engineer

- **Interview Checklist** — preguntas de la entrevista
- **Installation Checklist** — info de montaje por AP (location, antenna type, orientation, mounting, power)
- **Equipment Checklist** — herramientas

### Deliverables (reporte final al cliente)

> Reportes profesionales de cientos de páginas. Software comercial (Ekahau, iBwave) genera estos PDF con templates.

| Sección                                | Contenido                                                                                                |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Purpose Statement**                  | Requisitos del cliente + business justification                                                          |
| **Spectrum Analysis**                  | Fuentes potenciales de interferencia identificadas                                                       |
| **RF Coverage Analysis**               | Cell boundaries, heatmap                                                                                 |
| **Hardware Placement & Configuration** | AP placement, antenna orientation, channel reuse, power settings, técnicas de instalación, cable routing |
| **Capacity & Performance Analysis**    | Throughput tests (opcional)                                                                              |
| **Pictures**                           | Fotos del survey (ubicación AP, interferers, problemas)                                                  |

### Reportes adicionales

- **Vendor recommendations** (idealmente mismo vendor del survey)
- **Security recommendations**
- **Bill of Materials (BoM)** + **Project schedule**

**Fuente:** CWNA-107.md, Cap. 14 — _Documents and Reports_, _Deliverables_, _Additional Reports_, Figs. 14.13–14.14 (págs. 574–578, líneas ~17000–17050).

---

## Aplicabilidad al proyecto Heatmapper

> **Heatmapper = una herramienta de site survey híbrido para Android.** El Cap. 14 es esencialmente la **especificación funcional implícita** del producto.

| Concepto del Cap. 14                                          | RP afectado       | Decisión / implicación para Heatmapper                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Entrevista pre-survey + purpose statement**                 | RP6               | El reporte exportable (RP6) debe iniciar con un _purpose statement_ configurable: nombre del sitio, propósito (datos / voz / VoWiFi), threshold seleccionado (−70 / −65 dBm), aplicaciones objetivo.                                                                                                                                                     |
| **Vertical markets (educación, hospital, retail, warehouse)** | RP4, RP5          | La IA (RP5) puede ofrecer _perfiles preset_ por vertical: "Aula 1:1", "Hospital VoWiFi", "Warehouse handhelds", cada uno ajustando thresholds y tipo de antena recomendado.                                                                                                                                                                              |
| **AP-on-a-stick (legacy)**                                    | —                 | Heatmapper NO implementa este método (es manual y costoso). El usuario despliega APs reales y mide.                                                                                                                                                                                                                                                      |
| **Spectrum analysis**                                         | **RP4**           | **Limitación honesta del proyecto:** Android no expone un spectrum analyzer real (solo lista APs Wi-Fi). El reporte (RP6) debe **declarar esta limitación explícitamente** y recomendar un Wi-Spy / Sidekick para verificar non-Wi-Fi interferers (microondas, baby monitors). Heatmapper sí puede detectar OBSS/CCI a partir de los beacons capturados. |
| **Threshold −70 dBm + diagonal walk + −70 dBm contour**       | **RP1, RP3, RP4** | Esta es **la metodología canónica que la app implementa**. RP1 captura RSSI por punto; RP3 interpola la grilla; RP4 dibuja el contorno de **−70 dBm** y marca todo lo que esté por debajo como "fuera de cobertura óptima".                                                                                                                              |
| **Mediciones obligatorias: RSSI + noise + SNR**               | **RP1**           | Android expone RSSI vía `ScanResult.level` (dBm). **NO expone noise floor** directamente → la app debe estimar SNR usando un piso de ruido típico (−95 dBm) o permitir al usuario configurarlo. Documentar este caveat en el reporte.                                                                                                                    |
| **Passive vs Active manual survey**                           | **RP1**           | RP1 actual es **passive** (escanea beacons). Considerar añadir modo **active** opcional: medir throughput (iPerf-like) cuando el usuario está asociado al AP bajo prueba.                                                                                                                                                                                |
| **Hybrid Survey (premisa entera)**                            | **TODOS**         | Heatmapper es **literalmente** un híbrido: el usuario carga floor plan (RP2), camina midiendo (RP1), la app interpola (RP3) y predice cobertura (RP4). Equivale a "Ekahau de bolsillo" para usuarios que no pueden pagar Ekahau.                                                                                                                         |
| **Initial site visit + acceso a todo**                        | RP4               | UX: la app debe permitir guardar **múltiples sesiones** por sitio (varios pisos, varios edificios) y reanudar.                                                                                                                                                                                                                                           |
| **Attenuation spot checks (FSPL + cross-wall)**               | RP2, **RP5**      | **Funcionalidad sugerida (opcional V2):** modo "calibrar pared" — el usuario marca dos puntos en el plano (uno a 5 m del AP libre, otro al otro lado de una pared) y la app calcula automáticamente la atenuación de esa pared en dB. La IA (RP5) usaría estos valores para refinar el modelo predictivo.                                                |
| **Building observation: techos, cableado**                    | RP6               | Permitir adjuntar **fotos georeferenciadas** al reporte (la cámara del Android es perfecta para esto).                                                                                                                                                                                                                                                   |
| **Predictive design (Ekahau workflow)**                       | **RP2, RP3, RP5** | La fortaleza diferencial de Heatmapper. Importar floor plan (RP2), simular AP placement con FSPL + atenuación (RP3), y RP5 propone reubicaciones/canales óptimos. Es esencialmente lo que hacen Ekahau / iBwave / AirMagnet / TamoGraph en escritorio, pero con captura _real-time_ sobre el plano.                                                      |
| **Validation Survey (post-deploy)**                           | **RP4, RP6**      | Caso de uso #2 de Heatmapper: validar instalación existente. La app **es** una herramienta de validation survey. El reporte (RP6) debe permitir comparar **cobertura medida vs target**.                                                                                                                                                                 |
| **Capacity testing (iPerf, TamoSoft)**                        | RP6               | Out-of-scope inicial; mencionar como recomendación en el reporte.                                                                                                                                                                                                                                                                                        |
| **Roaming validation, delay, jitter**                         | —                 | Out-of-scope para V1. Documentar como future work.                                                                                                                                                                                                                                                                                                       |
| **Aesthetics, mounting**                                      | RP6               | Permitir foto + nota libre por cada AP marcado en el plano.                                                                                                                                                                                                                                                                                              |
| **Toolkit indoor (cámara, blueprints, mediciones)**           | RP1, RP6          | Android es un **toolkit todo-en-uno**: ya integra cámara, GPS, sensor inercial (para tracking de movimiento), Wi-Fi scanner. Heatmapper aprovecha eso.                                                                                                                                                                                                   |
| **Toolkit outdoor (GPS, topo map, Fresnel)**                  | —                 | Out-of-scope (Heatmapper es indoor).                                                                                                                                                                                                                                                                                                                     |
| **Mismo vendor de AP en survey y deploy**                     | RP1, RP4          | **Caveat de honestidad** en el reporte: las mediciones RSSI son del **chipset del Android del usuario**. Cualquier dispositivo cliente real puede ver RSSI distinto (±5–10 dB). Considerar añadir factor de calibración por modelo.                                                                                                                      |
| **Deliverables: 5 secciones del reporte final**               | **RP6**           | Plantilla concreta para el reporte exportable de RP6: (1) Purpose Statement, (2) Spectrum/Interference Analysis (con caveat Android), (3) RF Coverage Analysis (heatmap PDF), (4) Hardware Placement (mapa con APs y propuestas IA de RP5), (5) Capacity & Performance (opcional).                                                                       |
| **Pictures embebidas en el reporte**                          | RP6               | El reporte exportado debe incluir las fotos georeferenciadas que el usuario tomó durante el survey.                                                                                                                                                                                                                                                      |
| **Vendor recommendations (additional report)**                | RP5, RP6          | RP5 puede sugerir "agregar AP modelo XYZ aquí" como recomendación textual en el reporte, no solo coordenadas.                                                                                                                                                                                                                                            |
| **Bill of Materials + Project Schedule**                      | RP6               | Si RP5 sugiere N APs nuevos, RP6 puede generar un BoM básico con los modelos sugeridos.                                                                                                                                                                                                                                                                  |

---

**Anterior:** [`04-diseno-wlan.md`](04-diseno-wlan.md) · **Volver al índice:** [`00-indice.md`](00-indice.md)
