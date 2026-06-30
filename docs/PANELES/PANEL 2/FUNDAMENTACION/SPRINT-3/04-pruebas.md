# Sprint 3 — Pruebas

## S3.4 Pruebas Realizadas

### Pruebas del backend

**Tabla 24.** Casos de prueba del backend (pytest) — Sprint 3

| Grupo | Verificación | Resultado esperado | Estado |
| ----- | ------------ | ------------------ | ------ |
| BE1 | Latencia p95 con 50 mediciones por lote | `<= 1 s` | Pasada |
| BE2 | Validación de RSSI en rango `-120 a 0` | `422` para valores inválidos | Pasada |
| BE3 | Validación de ownership | Rechazo de acceso a planos y puntos ajenos | Pasada |
| BE4 | Plano no calibrado | `422` con mensaje de calibración obligatoria | Pasada |
| BE5 | 10 pruebas parametrizadas de umbrales CWNA-107 | Clasificación correcta de nivel | Pasada |

### Pruebas unitarias del `CapturaCubit`

**Tabla 25.** Grupos de pruebas unitarias con `bloc_test` y `mocktail`

| Grupo | Alcance | Estado |
| ----- | ------- | ------ |
| CU1 | `iniciarSesion` | Pasada |
| CU2 | `marcarPunto` | Pasada |
| CU3 | `agregarMedicionesAPunto` | Pasada |
| CU4 | `abrirDetallePunto` | Pasada |
| CU5 | `eliminarPunto` | Pasada |

### Prueba de integración

**Tabla 26.** Verificación integrada de captura en campo

| Escenario | Evidencia esperada | Estado |
| --------- | ------------------ | ------ |
| Captura completa en plano calibrado | Registros visibles en `punto_medicion` y `medicion_wifi` después del envío desde la app | Pasada |

### Resultado de la revisión del sprint

La revisión confirmó que el flujo completo de captura, persistencia y consulta de puntos quedó operativo. Todos los grupos de prueba fueron aceptados y el incremento se consideró listo para servir de base al análisis de cobertura y generación del *heatmap* en las iteraciones siguientes.

---
