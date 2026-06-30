# Wireless HeatMapper — Exposición Sprint 2 y Sprint 3

**Proyecto:** Wireless HeatMapper · Ingeniería de Software II — FICCT, UAGRM  
**Cliente:** Bulldog Tech.  
**Modalidad:** 100 % en línea (toda persistencia en PostgreSQL vía backend FastAPI)  
**Fecha de referencia:** mayo 2026

---

## Contexto: ¿dónde estamos parados?

El Sprint 1 entregó la **fundación del sistema**: autenticación JWT, gestión de usuarios y clientes en el panel admin web, y las primeras pantallas de la app móvil para crear y listar proyectos de survey. Con esa base operativa, los Sprints 2 y 3 construyen la **columna vertebral del trabajo de campo**:

```
Sprint 1 (hecho) → Sprint 2 → Sprint 3 → Sprint 4 …
[Autenticación]    [Planos]   [Captura]   [Heatmap]
[Proyectos CRUD]   [Escala]   [WiFi]      [IA]
```

Dicho de otra forma: sin los planos calibrados del Sprint 2 no se puede capturar nada, y sin la captura del Sprint 3 no hay datos para generar el heatmap del Sprint 4.

---

## Sprint 2 — Planos en línea: importar y calibrar

**Período:** 28 abril – 11 mayo 2026 (10 días hábiles)  
**PHU comprometidos:** 16  
**Historias de usuario:** PB-02 (Importar plano) · PB-11 (Calibrar escala)

### Objetivo en una oración

> Al cierre del Sprint 2 un técnico puede subir el plano de un edificio al sistema y trazar sobre él la escala real en metros, dejando el plano listo y calibrado en PostgreSQL para recibir mediciones en campo.

---

### ¿Qué problema resuelve?

El técnico de Bulldog Tech. llega a un edificio con el teléfono. Antes de tomar mediciones WiFi necesita:

1. Tener una imagen del piso o zona como referencia visual.
2. Que el sistema sepa cuántos metros reales corresponden a cada píxel del plano.

Sin ese paso previo, las coordenadas de los puntos de medición son solo píxeles sin significado real, y la IA del Sprint 5 no puede calcular modelos de propagación correctos.

---

### HU PB-02 — Importar Plano de Edificio

#### Descripción

El técnico sube uno o más archivos (PNG, JPG o PDF de una sola página) al backend. El sistema almacena el archivo, genera una URL de acceso firmada y devuelve las dimensiones del plano en píxeles. La app renderiza el plano en un canvas con soporte de zoom y desplazamiento táctil.

**Restricciones técnicas relevantes:**

- Tamaño máximo: **20 MB** por archivo.
- PDF multipágina: solo se procesa y guarda la **primera página** (conversión a PNG mediante PyMuPDF en el backend).
- Formatos aceptados: `PNG`, `JPG`, `PDF`.
- La URL firmada expira en **1 hora**; el cliente la renueva al reabrir la pantalla.
- Un proyecto puede tener **múltiples planos** (uno por piso, locación o zona).
- Un plano **no puede eliminarse** si ya tiene puntos de medición asociados.

#### Ejemplo de uso paso a paso

**Escenario:** El técnico "Carlos Soliz" tiene el proyecto `Edificio Torre Norte` creado en Sprint 1. Ahora quiere subir el plano del piso 3.

```
1. Carlos abre la app → Mis Proyectos → toca "Torre Norte".
2. Toca el botón "+" en la sección "Planos".
3. El explorador de archivos del teléfono se abre.
4. Carlos selecciona "plano_piso3.pdf" (8 MB, 2 páginas).
5. La app envía:
   POST /api/proyectos/42/planos
   Content-Type: multipart/form-data
   [archivo binario]
6. El backend detecta PDF multipágina → convierte página 1 a PNG (PyMuPDF).
7. El backend guarda el archivo como:
   plano_42_a3c7f2d8.png  →  /var/lib/heatmapper/planos/
8. El backend responde:
   HTTP 201 Created
   {
     "id": 17,
     "urlFirmada": "http://backend/planos/plano_42_a3c7f2d8.png?token=...",
     "formato": "PDF",
     "anchoPx": 2480,
     "altoPx": 3508,
     "warning": "Se importó solo la primera página del PDF"
   }
9. La app muestra el plano renderizado. Carlos puede hacer pinch-to-zoom
   y desplazarse con el dedo. El mensaje "Se importó solo la primera página"
   aparece brevemente como snackbar informativo.
```

**Caso de error — archivo demasiado grande:**

```
Carlos intenta subir "plano_full_hd.jpg" (25 MB).
→ HTTP 413 Payload Too Large
→ La app muestra: "El archivo supera el límite de 20 MB. Comprime la imagen e inténtalo de nuevo."
```

**Caso de error — formato no soportado:**

```
Carlos selecciona "plano.dwg" (AutoCAD).
→ HTTP 415 Unsupported Media Type
→ La app muestra: "Formato no soportado. Usa PNG, JPG o PDF."
```

#### Flujo técnico resumido

```
[App Móvil]                    [Backend FastAPI]              [Almacenamiento]
     |                               |                               |
     |── POST /planos (multipart) ──>|                               |
     |                               |── validar tamaño y formato    |
     |                               |── si PDF: PyMuPDF → PNG       |
     |                               |── guardar archivo ───────────>|
     |                               |── INSERT plano en PostgreSQL  |
     |                               |── generar URL firmada         |
     |<──── 201 + urlFirmada ────────|                               |
     |                               |                               |
     |── renderizar en Canvas ──────>|                               |
```

---

### HU PB-11 — Calibrar Escala del Plano

#### Descripción

Una vez que el plano está subido, el técnico dibuja una línea sobre él entre dos puntos conocidos (por ejemplo, el largo de un pasillo) e ingresa la longitud real en metros. El backend calcula y persiste el factor `escala_m_por_px`, que convierte píxeles del plano a metros reales.

**Fórmula:**
$$\text{escala\_m\_por\_px} = \frac{\text{distancia\_real\_m}}{\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}}$$

**Restricciones:**

- Distancia de referencia **mínima: 1 metro** (para evitar errores de precisión).
- Si el plano ya tiene puntos de medición asociados, **no se puede recalibrar** (HTTP 409).
- La calibración es **obligatoria** para habilitar la captura en el Sprint 3.
- El estado de calibración persiste en el backend y es accesible desde cualquier dispositivo.

#### Ejemplo de uso paso a paso

**Escenario:** Carlos ya subió el plano del piso 3. Ahora quiere calibrarlo usando el pasillo central que mide 12 metros.

```
1. Carlos toca "Calibrar escala" en la pantalla del plano.
2. La app entra en modo calibración (borde azul pulsante en el canvas).
3. Carlos toca el inicio del pasillo → punto A (980, 450) en píxeles del plano.
4. Carlos toca el final del pasillo → punto B (1840, 450) en píxeles del plano.
   La app dibuja una línea naranja entre A y B.
5. Aparece un diálogo: "¿Qué longitud real tiene esta línea?"
   Carlos escribe: 12  (metros)  → toca "Confirmar".
6. La app envía:
   PATCH /api/planos/17/calibracion
   {
     "x1": 980, "y1": 450,
     "x2": 1840, "y2": 450,
     "distanciaRealM": 12.0
   }
7. El backend calcula:
   distancia_px = sqrt((1840-980)² + (450-450)²) = 860 px
   escala_m_por_px = 12.0 / 860 ≈ 0.01395 m/px
8. El backend actualiza el registro del plano y responde:
   HTTP 200 OK
   {
     "id": 17,
     "escalaMPorPx": 0.01395,
     "calibrado": true
   }
9. La app muestra una "regla virtual":
   Carlos toca dos puntos cualesquiera del plano y ve la distancia real en metros.
   Ejemplo: toca una sala → la app muestra "≈ 8.4 m × 5.2 m".
10. El botón "Iniciar captura" (Sprint 3) se habilita con ícono verde.
```

**Caso de error — distancia insuficiente:**

```
Carlos dibuja una línea muy corta (0.5 m de referencia).
→ HTTP 422 Unprocessable Entity
→ La app muestra: "La distancia debe ser al menos 1 metro para garantizar precisión."
```

**Caso de error — plano ya tiene puntos:**

```
Carlos intenta recalibrar un plano que ya tiene 15 puntos de medición del Sprint 3.
→ HTTP 409 Conflict
→ La app muestra: "No es posible recalibrar con mediciones registradas. Elimina los puntos primero."
   (El botón "Calibrar" aparece deshabilitado con ese tooltip).
```

---

### Diagrama de relación Sprint 2

```
[Proyecto (Sprint 1)]
        |
        | 1..*
        ↓
    [Plano]  ←─── POST /api/proyectos/{id}/planos
        |
        | PATCH /api/planos/{id}/calibracion
        ↓
  [Plano calibrado]
   escala_m_por_px ✓
        |
        | (habilita)
        ↓
  [Captura WiFi — Sprint 3]
```

---

### Resultado al cierre del Sprint 2

Al finalizar este sprint, el sistema puede:

| Capacidad                       | Endpoint                             | Estado esperado        |
| ------------------------------- | ------------------------------------ | ---------------------- |
| Subir plano PNG/JPG/PDF         | `POST /api/proyectos/{id}/planos`    | 201 en p95 ≤ 1 s       |
| Listar planos de un proyecto    | `GET /api/proyectos/{id}/planos`     | 200 con lista paginada |
| Obtener URL firmada renovada    | `GET /api/planos/{id}/url-firmada`   | 200 con URL válida     |
| Calibrar escala                 | `PATCH /api/planos/{id}/calibracion` | 200 con factor m/px    |
| Eliminar plano sin puntos       | `DELETE /api/planos/{id}`            | 204                    |
| Rechazar eliminación con puntos | `DELETE /api/planos/{id}`            | 409                    |

**Demo de cierre:** técnico crea proyecto → sube plano PDF → el sistema convierte la primera página → el técnico dibuja línea de referencia sobre el pasillo → ingresa 12 m → el sistema confirma `0.01395 m/px` → la regla virtual mide distancias correctamente.

---

---

## Sprint 3 — Captura WiFi en línea

**Período:** 12 mayo – 25 mayo 2026 (10 días hábiles)  
**PHU comprometidos:** 21  
**Historias de usuario:** PB-03 (Capturar señales WiFi) · PB-04 (Marcar puntos de medición)

### Objetivo en una oración

> Al cierre del Sprint 3 un técnico puede recorrer un edificio, marcar puntos sobre el plano calibrado y capturar mediciones WiFi reales que se persisten en tiempo real en PostgreSQL, sin guardar nada en el dispositivo.

---

### ¿Qué problema resuelve?

El técnico recorre el edificio con el teléfono. En cada posición relevante (centro de sala, pasillo, ascensor, esquina) necesita:

1. Registrar su posición exacta sobre el plano.
2. Escanear todas las redes WiFi visibles en ese punto (SSID, BSSID, RSSI, canal, frecuencia).
3. Enviar esos datos al servidor **inmediatamente**, sin acumularlos en el teléfono.

Al terminar el recorrido, el servidor tiene todos los datos necesarios para generar el heatmap en el Sprint 4.

---

### HU PB-03 — Capturar Señales WiFi (en línea)

#### Descripción

El técnico activa la captura en la `CapturaPage`. La app usa el `WifiManager` de Android para obtener la lista de redes visibles en ese instante. Cada lote (posición + lista de redes) se envía como un solo request POST al backend. El backend valida, clasifica las señales por nivel y persiste en las tablas `punto_medicion` y `medicion_wifi`.

**Restricciones técnicas críticas:**

| Restricción              | Valor                                               | Fuente                                     |
| ------------------------ | --------------------------------------------------- | ------------------------------------------ |
| Throttling Android ≥ 8.0 | Máx. **4 escaneos cada 2 minutos** en background    | CWNA-107 / Android API                     |
| Reintentos del cliente   | Backoff exponencial: **3 intentos**, máx. 4 s total | PB-03 regla de negocio                     |
| Almacenamiento local     | **Prohibido** bajo cualquier circunstancia          | Modalidad 100 % en línea                   |
| Rango válido de RSSI     | Entre **−120 dBm y 0 dBm**                          | Validación backend (422 si fuera de rango) |
| Cobertura objetivo       | ≥ **−70 dBm** (CWNA-107)                            | Umbral de diseño                           |
| Zona muerta              | < **−90 dBm** (CWNA-107)                            | Clasificación `ZONA_MUERTA`                |

#### Clasificación de nivel de señal (backend)

El backend asigna automáticamente el campo `nivel` a cada medición al persistirla:

| RSSI (dBm) | Nivel         | Uso visual                                      |
| ---------- | ------------- | ----------------------------------------------- |
| ≥ −60      | `EXCELENTE`   | Detalle de medición / heatmap por AP            |
| −60 a −70  | `BUENA`       | Detalle de medición / heatmap por AP            |
| −70 a −80  | `ACEPTABLE`   | Detalle de medición / heatmap por AP            |
| −80 a −90  | `DEBIL`       | Detalle de medición / heatmap por AP            |
| < −90      | `ZONA_MUERTA` | Detalle de medición / heatmap por AP            |

#### Estados de la sesión de captura

La `CapturaPage` maneja un `CapturaCubit` (BLoC) con los siguientes estados:

```
[Inactiva]
    │ iniciar captura (plano calibrado ✓)
    ↓
[Activa] ──── marcar punto ──→ [Enviando lote]
    │                                │ 201 OK
    │                                └──────────────→ [Activa]
    │ 4 escaneos / 2 min
    ↓
[Throttling] ─── ventana liberada ──→ [Activa]
    │
    │ red caída
    ↓
[Pausada] ─── red restablecida + confirmación ──→ [Activa]
    │
    │ detener captura
    ↓
[Inactiva]
```

#### Ejemplo de uso paso a paso — Modo Puntual

**Escenario:** Carlos está en el piso 3 con el plano calibrado. Quiere medir la cobertura de la sala de reuniones.

```
1. Carlos abre el proyecto → toca el plano del piso 3.
2. Toca "Iniciar captura" (habilitado porque el plano está calibrado).
3. La app entra en CapturaPage: el plano se muestra con un banner
   "● Captura activa — conectado al servidor".
4. Carlos camina hasta el centro de la sala de reuniones.
5. Toca sobre el plano en la posición donde se encuentra
   → coordenadas (x=1200, y=890) en píxeles del plano.
6. La app dispara WifiScanner:
   → Android WifiManager.startScan()
   → Devuelve 8 redes visibles:
     SSID:"Bulldog-Corp"   BSSID:"AA:BB:CC:DD:EE:01"  RSSI:-55  canal:6   freq:2437
     SSID:"Bulldog-Corp"   BSSID:"AA:BB:CC:DD:EE:02"  RSSI:-72  canal:6   freq:2437
     SSID:"Visitantes"     BSSID:"AA:BB:CC:DD:EE:03"  RSSI:-68  canal:11  freq:2462
     SSID:"Bulldog-5GHz"   BSSID:"AA:BB:CC:DD:EE:04"  RSSI:-61  canal:36  freq:5180
     ... (4 redes más)
7. La app envía el lote al backend:
   POST /api/mediciones
   {
     "planoId": 17,
     "x": 1200,
     "y": 890,
     "mediciones": [
       {"ssid": "Bulldog-Corp",  "bssid": "AA:BB:CC:DD:EE:01", "rssi": -55, "canal": 6,  "frecuencia": 2437},
       {"ssid": "Bulldog-Corp",  "bssid": "AA:BB:CC:DD:EE:02", "rssi": -72, "canal": 6,  "frecuencia": 2437},
       {"ssid": "Visitantes",    "bssid": "AA:BB:CC:DD:EE:03", "rssi": -68, "canal": 11, "frecuencia": 2462},
       {"ssid": "Bulldog-5GHz",  "bssid": "AA:BB:CC:DD:EE:04", "rssi": -61, "canal": 36, "frecuencia": 5180},
       ...
     ]
   }
8. El backend:
   - Valida ownership del plano (el plano pertenece al proyecto del técnico).
   - Valida rango de RSSI (todos entre -120 y 0).
   - Clasifica cada medición:
     -55 dBm → EXCELENTE
     -72 dBm → ACEPTABLE
     -68 dBm → BUENA
     -61 dBm → BUENA
   - Determina el nivel técnico agregado del punto = peor RSSI del lote = ACEPTABLE (-72).
   - Inserta en PostgreSQL:
     punto_medicion (id=301, plano_id=17, x=1200, y=890, nivel="ACEPTABLE")
     medicion_wifi  (id=1001..1008, punto_id=301, ...)
   - Responde: HTTP 201
     { "puntoId": 301, "nivel": "ACEPTABLE", "cantidadMediciones": 8 }
9. La app renderiza un marcador neutro en (1200, 890) sobre el plano.
   El badge muestra "8 redes".
10. Carlos avanza al siguiente punto. El contador de throttling muestra
    "Escaneos restantes: 3 (se renueva en 1:47)".
```

#### Ejemplo de uso — Gestión de conectividad

```
Carlos está tomando mediciones. De repente el router de la oficina
se apaga (o Carlos entra a un cuarto sin señal de datos).

→ ConnectivityMonitor detecta red caída.
→ La CapturaPage muestra un banner rojo permanente:
  "⚠ Sin conexión al servidor — captura pausada"
→ El botón "Marcar punto" se deshabilita.
→ El estado del Cubit pasa a [Pausada].

Minutos después, la conexión se restablece.
→ Banner cambia a amarillo: "Conexión restablecida — toca para reanudar"
→ Carlos toca "Reanudar".
→ El estado vuelve a [Activa].
→ No se perdió ningún dato: simplemente no se tomaron mediciones en ese intervalo.
   (No había nada que recuperar porque nada se guardó localmente).
```

#### Ejemplo de uso — Retry exponencial

```
Carlos marca un punto. El backend tarda más de lo esperado.

Intento 1 (inmediato):     timeout → falla
Intento 2 (+ 500 ms):     error 503 → falla
Intento 3 (+ 1 500 ms):   timeout → falla

→ Total: ~2.5 s de espera.
→ La app muestra: "✗ No se pudo enviar el lote. [Reintentar]"
→ El punto NO aparece en el plano (no hay confirmación del servidor).
→ El lote se descarta de la memoria.
→ Carlos puede reintentar manualmente o avanzar al siguiente punto.

IMPORTANTE: En ningún momento se escribió ningún archivo ni base de datos
en el teléfono. Esto cumple con la modalidad 100 % en línea del proyecto.
```

---

### HU PB-04 — Marcar Puntos de Medición

#### Descripción

El técnico interactúa con el canvas del plano en dos modos: **Puntual** (cada toque dispara un escaneo) y **Continuo** (la app escanea automáticamente cada N segundos mientras el técnico se desplaza). Los puntos registrados se muestran sobre el plano como marcadores neutros de ubicación; el color por nivel se reserva para el detalle de mediciones y el heatmap por AP.

**Modos de captura:**

| Modo         | Comportamiento                                       | Cuándo usarlo                   |
| ------------ | ---------------------------------------------------- | ------------------------------- |
| **Puntual**  | Cada toque sobre el plano dispara un escaneo + envío | Medición metódica punto a punto |
| **Continuo** | Escaneo automático cada 15, 30 o 60 s (configurable) | Recorrido libre por pasillos    |

**Reglas clave:**

- El plano **debe estar calibrado** (PB-11). Si no lo está, el botón "Iniciar captura" está deshabilitado con tooltip.
- Las coordenadas del punto se guardan en **píxeles del plano** (no de pantalla), aplicando la transformación inversa del zoom/pan actual.
- El técnico puede **tocar un punto registrado** para ver el detalle de todas las mediciones de ese lote.
- El técnico puede **eliminar un punto** con confirmación (DELETE con cascada sobre las mediciones).

#### Ejemplo de uso — Modo Continuo

**Escenario:** Carlos necesita mapear el pasillo principal que cruza todo el piso 3.

```
1. Carlos activa el modo "Continuo" → selecciona intervalo: 30 segundos.
2. La app muestra: "Modo continuo activo — escaneo cada 30 s"
   Un contador regresivo aparece en pantalla.
3. Carlos empieza a caminar lentamente por el pasillo.
4. A los 30 s, la app escanea automáticamente.
   → Carlos está en (500, 600) → escaneo → POST → marcador en el plano.
5. A los 60 s, escaneo automático.
   → Carlos está en (700, 600) → escaneo → POST → marcador en el plano.
6. A los 90 s, escaneo automático.
   → Carlos está en (950, 600) → escaneo → POST → marcador en el plano.
   Nota: las mediciones del detalle reflejan el cambio de RSSI por AP.
7. A los 120 s, se alcanza el límite de throttling Android (4 escaneos / 2 min).
   → La app pausa el timer automáticamente.
   → Banner: "Límite de escaneos alcanzado — reanuda en 0:47"
   → Carlos espera o continúa caminando sin escanear.
8. Cuando el timer se renueva, la app reanuda automáticamente.
9. Al terminar, Carlos toca "Detener captura".
   El plano muestra la ruta de puntos medidos; la cobertura se interpreta en el heatmap.
```

#### Ejemplo de uso — Detalle de un punto

```
Carlos toca el punto en (950, 600) que registró anteriormente.
→ Se abre un bottom sheet (panel inferior) con el detalle:

────────────────────────────────────────────────
  Punto #303 — (950 px, 600 px)
  Posición real: ~13.2 m, ~8.4 m desde esquina NW
  8 redes detectadas:
  ─────────────────────────────────────────────
  1. Bulldog-Corp   AA:BB:CC:01   -55 dBm  EXCELENTE  ch.6
  2. Bulldog-5GHz   AA:BB:CC:04   -61 dBm  BUENA      ch.36
  3. Visitantes     AA:BB:CC:03   -68 dBm  BUENA      ch.11
  4. Bulldog-Corp   AA:BB:CC:02   -79 dBm  ACEPTABLE  ch.6
  5. Vecino-WiFi    DD:EE:FF:01   -84 dBm  DÉBIL      ch.1
  6. IoT-Devices    DD:EE:FF:02   -87 dBm  DÉBIL      ch.11
  7. Backup-AP      DD:EE:FF:03   -91 dBm  ZONA_MUERTA ch.6
  8. Guest-Old      DD:EE:FF:04   -95 dBm  ZONA_MUERTA ch.11
  ─────────────────────────────────────────────
  [Eliminar punto]
────────────────────────────────────────────────
```

#### Ejemplo de uso — Eliminación de punto

```
Carlos se da cuenta de que el punto #302 lo marcó en el lugar equivocado.

1. Toca el punto en el plano.
2. En el bottom sheet toca "Eliminar punto".
3. Aparece diálogo de confirmación:
   "¿Eliminar el punto #302 y sus 8 mediciones? Esta acción no se puede deshacer."
   [Cancelar]  [Eliminar]
4. Carlos toca "Eliminar".
5. La app envía:
   DELETE /api/puntos/302
6. El backend elimina en cascada:
   DELETE FROM medicion_wifi WHERE punto_id = 302  (8 filas)
   DELETE FROM punto_medicion WHERE id = 302       (1 fila)
7. Responde: HTTP 204 No Content
8. El punto desaparece del plano. El bottom sheet se cierra.
```

---

### Conversión de coordenadas — detalle técnico

Este es uno de los aspectos más importantes de la implementación. Las coordenadas que el técnico toca en la pantalla no son iguales a las coordenadas del plano, porque el plano puede estar con zoom o desplazado.

```
Ejemplo:
  El plano tiene 2480 × 3508 px (tamaño real en el servidor).
  La pantalla del teléfono tiene 1080 × 1920 px.
  El usuario aplicó un zoom de 1.8x y desplazó el plano (-200, -400) px.

  El técnico toca (540, 960) en la pantalla (centro).

  Fórmula de conversión (coordenadas de plano):
    x_plano = (x_pantalla - offset_x) / zoom = (540 - (-200)) / 1.8 ≈ 411 px
    y_plano = (y_pantalla - offset_y) / zoom = (960 - (-400)) / 1.8 ≈ 756 px

  El backend recibe (411, 756) como coordenadas del plano.
  Al calibrar: posición real ≈ 411 × 0.01395 m ≈ 5.7 m en X
                               756 × 0.01395 m ≈ 10.5 m en Y
```

Esta conversión ocurre en la app móvil antes de enviar el lote, usando el estado actual de `InteractiveViewer` (Flutter).

---

### Permisos Android requeridos (Sprint 3)

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
```

> **Nota:** `ACCESS_FINE_LOCATION` es obligatorio en Android 9+ para acceder a resultados de escaneo WiFi. Sin este permiso, `WifiManager.getScanResults()` devuelve una lista vacía.

---

### Resultado al cierre del Sprint 3

Al finalizar este sprint, el sistema puede:

| Capacidad                 | Endpoint / Componente         | Estado esperado                       |
| ------------------------- | ----------------------------- | ------------------------------------- |
| Capturar lote WiFi        | `POST /api/mediciones`        | 201 en p95 ≤ 1 s con 50 mediciones    |
| Listar puntos de un plano | `GET /api/planos/{id}/puntos` | 200 con lista                         |
| Ver detalle de un punto   | `GET /api/puntos/{id}`        | 200 con mediciones ordenadas por RSSI |
| Eliminar punto            | `DELETE /api/puntos/{id}`     | 204 con cascada                       |
| Modo puntual (app)        | `CapturaPage` - toque         | Punto + badge en plano                |
| Modo continuo (app)       | `CapturaPage` - timer         | Escaneo cada N segundos               |
| Throttling visible        | `CapturaPage` - contador      | Deshabilitado al límite               |
| Gestión de red caída      | `ConnectivityMonitor`         | Banner permanente                     |
| No almacenamiento local   | Ausencia de tablas SQLite     | Verificable por auditoría             |

**Demo de cierre:** técnico activa captura → marca 10 puntos en modo puntual → en campo real con router WiFi de prueba → los 10 puntos y sus mediciones aparecen en la BD → verificado con consulta directa a PostgreSQL.

---

---

## Relación entre Sprints 2 y 3

```
                    ┌─────────────────────────────────────────────┐
                    │               SPRINT 2                       │
                    │                                              │
  [Proyecto]────────┤  POST /planos ──► almacena archivo          │
  (Sprint 1)        │  PATCH /calibracion ──► escala_m_por_px     │
                    │                                              │
                    └────────────────────┬────────────────────────┘
                                         │ plano calibrado ✓
                                         ▼
                    ┌─────────────────────────────────────────────┐
                    │               SPRINT 3                       │
                    │                                              │
                    │  POST /mediciones ──► punto_medicion         │
                    │                   ──► medicion_wifi (n)      │
                    │  Canvas ──► coordenadas con escala real      │
                    │                                              │
                    └────────────────────┬────────────────────────┘
                                         │ datos de señal ✓
                                         ▼
                              [SPRINT 4 — Heatmap e IA]
```

**Dependencia estricta:** el Sprint 3 no puede ejecutarse sobre un plano no calibrado. El campo `calibrado: bool` en la tabla `plano` actúa como semáforo: si es `false`, el endpoint `POST /api/mediciones` devuelve `HTTP 422` con mensaje `"El plano no está calibrado. Complete la calibración antes de registrar mediciones."`.

---

## Tabla resumen comparativa

| Aspecto                       | Sprint 2                          | Sprint 3                               |
| ----------------------------- | --------------------------------- | -------------------------------------- |
| **Objetivo central**          | Subir y calibrar plano            | Capturar señales WiFi en campo         |
| **HU**                        | PB-02, PB-11                      | PB-03, PB-04                           |
| **PHU**                       | 16                                | 21                                     |
| **Actor principal**           | Técnico (antes del campo)         | Técnico (en campo)                     |
| **Responsable backend**       | Jhasmany (PB-02) + Borys (PB-11)  | Jhasmany (PB-03) + Borys (PB-04)       |
| **Responsable móvil**         | Jhasmany                          | Jhasmany                               |
| **Tablas nuevas en BD**       | `plano`                           | `punto_medicion`, `medicion_wifi`      |
| **Endpoints nuevos**          | 5                                 | 4                                      |
| **Restricción técnica clave** | PyMuPDF / escala ≥ 1 m            | Throttling Android / sin datos locales |
| **Criterio de done**          | Plano calibrado con regla virtual | 10 puntos reales en BD vía campo       |

---

## Glosario técnico

| Término                 | Definición                                                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **RSSI**                | Received Signal Strength Indicator — potencia de la señal recibida en dBm (negativo; más cercano a 0 = más fuerte) |
| **BSSID**               | Dirección MAC del punto de acceso WiFi (identifica el hardware físico)                                             |
| **SSID**                | Nombre de la red WiFi (puede tener múltiples BSSID)                                                                |
| **Throttling Android**  | Limitación del sistema operativo a 4 escaneos WiFi cada 2 minutos en apps en segundo plano (Android ≥ 8.0)         |
| **Zona muerta**         | Área donde la señal WiFi es < −90 dBm, prácticamente inutilizable (CWNA-107)                                       |
| **Plano calibrado**     | Plano con el factor `escala_m_por_px` calculado y persistido                                                       |
| **Lote de mediciones**  | Conjunto de ScanResults de un solo escaneo, asociados a un punto (x,y)                                             |
| **Backoff exponencial** | Estrategia de reintento donde el tiempo de espera aumenta exponencialmente entre intentos                          |
| **JWT**                 | JSON Web Token — mecanismo de autenticación sin estado usado por el backend FastAPI                                |
| **p95**                 | Percentil 95 de latencia — el 95 % de las solicitudes se resuelven en ese tiempo o menos                           |

---

_Documento generado para exposición académica — Wireless HeatMapper · FICCT-UAGRM · Grupo 24_
