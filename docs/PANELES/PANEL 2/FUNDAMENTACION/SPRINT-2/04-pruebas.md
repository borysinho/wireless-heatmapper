# Sprint 2 — Pruebas

## S2.4 Pruebas Realizadas

### Pruebas del backend

**Tabla 18.** Casos de prueba del backend (pytest) — Sprint 2

| ID | Caso de prueba | Resultado esperado | Estado |
| -- | -------------- | ------------------ | ------ |
| CA1 | Importación de plano válido | `201 Created` con metadatos y URL firmada | Pasada |
| CA2 | Archivo con tamaño excedido | `413 Payload Too Large` | Pasada |
| CA3 | Formato inválido | `415 Unsupported Media Type` | Pasada |
| CA4 | PDF multipágina | `201 Created` y advertencia de primera página importada | Pasada |
| CA5 | Calibración válida | `200 OK` con factor calculado | Pasada |
| CA6 | Distancia menor a 1 metro | `422 Unprocessable Entity` | Pasada |
| CA7 | Recalibración con puntos existentes | `409 Conflict` | Pasada |

### Pruebas de la app móvil

**Tabla 19.** Casos de prueba de la aplicación móvil — Sprint 2

| ID | Funcionalidad evaluada | Resultado esperado | Estado |
| -- | ---------------------- | ------------------ | ------ |
| FL1 | Importación de plano PNG/JPG/PDF | El archivo se carga y el plano queda visible en pantalla | Pasada |
| FL2 | Zoom y desplazamiento sobre el plano | La navegación mantiene estabilidad y contexto visual | Pasada |
| FL3 | Calibración con dos toques | La línea de referencia se dibuja y permite confirmar distancia | Pasada |
| FL4 | Visualización de distancia con regla | El sistema muestra metros coherentes con la escala persistida | Pasada |

### Resultado de la revisión del sprint

En la Sprint Review del 11 de mayo de 2026 se constató que todos los casos comprometidos fueron superados. El incremento fue aceptado con el criterio de que el plano queda disponible y calibrado para la captura WiFi en línea prevista en el sprint siguiente.

---
