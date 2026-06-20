# Sprint 3 — Historias de Usuario

## S3.1 Historias de Usuario del Sprint 3

**Objetivo del Sprint 3:** Implementar la captura WiFi en línea con asociación inmediata de mediciones a puntos georreferenciados sobre el plano calibrado.

**Duración:** 2 semanas (12 may – 25 may 2026)
**Puntos de Historia del Sprint:** 21 PHU

**Restricciones CWNA-107:** throttling Android 4 scans/2 min y clasificación de cobertura basada en umbrales de señal.

### Cronograma del Sprint 3

![Sprint 3 — Captura WiFi en línea — 12 may – 25 may 2026](img/05-sprint-3-detalle.png)

_Figura 26. Diagrama de Gantt — Planificación detallada del Sprint 3 (12–25 may 2026)._

---

### PB-03 — Capturar Señales WiFi

| Campo | Detalle |
| ----- | ------- |
| **ID** | PB-03 |
| **Rol** | Como técnico de campo |
| **Funcionalidad** | quiero escanear redes WiFi y enviar cada lote de resultados al backend en línea |
| **Beneficio** | para registrar mediciones sin persistencia local y disponer de datos inmediatos en el servidor |
| **PHU** | 13 |

**Conversación / reglas de negocio:**
- Cada lote incluye la posición del punto y una colección de mediciones con SSID, BSSID, RSSI, canal y frecuencia.
- El plano debe estar calibrado antes de permitir la captura.
- El backend clasifica la señal según rangos de dBm alineados con CWNA-107.
- Android limita el escaneo a 4 lecturas por cada 2 minutos bajo las condiciones definidas por la plataforma.

**Criterios de aceptación:**
- Un lote válido se registra en línea con respuesta `201`.
- RSSI fuera del rango operativo retorna `422`.
- Si no hay conectividad disponible, la aplicación no guarda lotes localmente y notifica la incidencia.
- La clasificación de cobertura se aplica desde el backend al persistir el lote.

---

### PB-04 — Marcar Puntos de Medición

| Campo | Detalle |
| ----- | ------- |
| **ID** | PB-04 |
| **Rol** | Como técnico de campo |
| **Funcionalidad** | quiero marcar puntos sobre el plano y consultar o eliminar sus lecturas asociadas |
| **Beneficio** | para vincular cada escaneo con una ubicación verificable del edificio |
| **PHU** | 8 |

**Conversación / reglas de negocio:**
- El modo puntual crea un punto por toque sobre el plano.
- El modo continuo agrega lecturas periódicas a un punto existente con `numero_lectura` incremental.
- Cada punto se dibuja con un color asociado al nivel agregado de señal.
- El detalle del punto agrupa mediciones por ciclo de lectura.

**Criterios de aceptación:**
- Cada toque en modo puntual genera punto, escaneo y persistencia.
- El modo continuo respeta el intervalo configurado y el límite de throttling.
- El detalle del punto se consulta desde el backend y se presenta ordenado.
- Eliminar un punto remueve también sus mediciones asociadas.

---

### Resumen del Sprint Backlog

| HU | Descripción | PHU | Estado |
| -- | ----------- | :-: | ------ |
| PB-03 | Capturar Señales WiFi | 13 | Completada |
| PB-04 | Marcar Puntos de Medición | 8 | Completada |
| **Total comprometido** |  | **21** |  |

---
