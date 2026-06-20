# 05 — Contratos API y Salidas

Los contratos siguientes son conceptuales. Los nombres finales deberán mantener las convenciones del backend antes de implementar.

## 1. Inventario RF

```text
GET    /api/planos/{plano_id}/inventario-rf
POST   /api/planos/{plano_id}/aps
PATCH  /api/aps/{ap_id}
POST   /api/aps/{ap_id}/radios
PATCH  /api/radios/{radio_id}
POST   /api/radios/{radio_id}/bssids
POST   /api/mediciones/{medicion_id}/vincular-configuracion
```

El endpoint de lectura devuelve APs físicos, radios, BSSID asociados, procedencia y completitud.

## 2. Validación de entradas

```text
POST /api/proyectos/{proyecto_id}/optimizacion/validar
```

Respuesta resumida:

```json
{
  "nivelCompletitud": "MEDIO",
  "porcentaje": 82,
  "bloqueos": [],
  "advertencias": [
    "La antena de AP-03 se asumirá omnidireccional de 2,14 dBi"
  ],
  "bandasDisponibles": ["2_4_GHZ", "5_GHZ"]
}
```

## 3. Generación de escenarios

```text
POST /api/proyectos/{proyecto_id}/escenarios-rf
```

Solicitud conceptual:

```json
{
  "tipoNegocio": "RED_EXISTENTE",
  "perfil": "PRIORIZAR_5_GHZ",
  "planoIds": [42],
  "areaObjetivoIds": [7, 8],
  "bandas": ["2_4_GHZ", "5_GHZ"],
  "politicaCombinacion": "PREFERIR_5_GHZ_SI_CUMPLE_UMBRAL",
  "maximoAps": 8,
  "presupuesto": 9500,
  "moneda": "BOB",
  "requiereCoberturaSecundaria": true
}
```

La generación puede ser asíncrona:

```text
202 Accepted
{ "trabajoId": 91, "estado": "PENDIENTE" }

GET /api/trabajos-optimizacion/{trabajo_id}
```

## 4. Detalle de escenario

```text
GET /api/escenarios-rf/{escenario_id}
```

Debe incluir:

- factibilidad, perfil, versión del predictor y confianza;
- APs propuestos y relación con APs existentes;
- radios propuestas con banda, canal, ancho, potencia/EIRP y antena;
- restricciones y supuestos;
- métricas globales y por banda;
- costo y lista de materiales;
- justificación por acción.

## 5. Mapas proyectados

```text
GET /api/escenarios-rf/{id}/mapas?banda=2_4_GHZ
GET /api/escenarios-rf/{id}/mapas?banda=5_GHZ
GET /api/escenarios-rf/{id}/mapas?tipo=COMBINADO
GET /api/escenarios-rf/{id}/mapas?tipo=DIFERENCIA&banda=5_GHZ
```

Cada respuesta declara banda, política, resolución, escala, matriz RSSI, incertidumbre y radios dominantes.

## 6. Valores proyectados en puntos reales

```text
GET /api/escenarios-rf/{id}/puntos-proyectados?banda=5_GHZ
```

Ejemplo:

```json
{
  "puntoMedicionId": 501,
  "banda": "5_GHZ",
  "rssiObservadoDbm": -78.0,
  "rssiProyectadoDbm": -66.0,
  "diferenciaDb": 12.0,
  "radioPrimariaId": 301,
  "rssiSecundarioDbm": -70.0,
  "incertidumbreDb": 4.2
}
```

La ausencia de un valor observado se representa con `null`; nunca se inventa un baseline para una instalación nueva.

## 7. Comparación PB-12

```text
GET /api/escenarios-rf/{id}/comparacion
```

La respuesta ofrece, por banda:

- mapa observado cuando exista;
- mapa proyectado;
- mapa de diferencia;
- cambios de cobertura, zonas muertas, redundancia y CCI/ACI;
- puntos con mayor mejora y mayor riesgo;
- advertencia de que proyectado no equivale a medido.

## 8. Errores relevantes

| Código | Caso                                                                  |
| ------ | --------------------------------------------------------------------- |
| 409    | Se intenta optimizar mientras cambió el baseline/inventario           |
| 422    | Entrada inválida o combinación de banda/canal/modelo no soportada      |
| 424    | Faltan datos obligatorios para producir un escenario defendible       |
| 503    | Predictor requerido no disponible; se informa si existe fallback físico |

