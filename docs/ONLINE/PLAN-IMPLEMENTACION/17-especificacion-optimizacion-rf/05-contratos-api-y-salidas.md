# 05 — Contratos API y Salidas

Los contratos siguientes son conceptuales. Los nombres finales deberán mantener las convenciones del backend antes de implementar.

Estos contratos se interpretan bajo la gobernanza del documento 18:

- el inventario RF puede ser alimentado desde móvil o web según permisos del usuario;
- la generación IA, comparación de escenarios proyectados y publicación se exponen solo a web admin o procesos backend autorizados;
- el portal cliente consume únicamente contenido publicado explícitamente;
- el móvil no debe invocar endpoints de generación IA ni recibir alternativas IA no aprobadas.

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

Acceso permitido: web admin o proceso backend autorizado. No debe estar disponible para la app móvil.

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
  "requiereCoberturaSecundaria": true,
  "fuenteEntrada": {
    "tipo": "SELECCION_APS_MAPA",
    "apIds": [11, 12, 15],
    "conjuntoId": null
  }
}
```

`fuenteEntrada` puede ser una selección directa de APs del mapa, un conjunto existente opcional, el inventario RF completo o el baseline observado. Un `conjuntoId` no es obligatorio.

Respuesta conceptual mínima:

```json
{
  "trabajoId": 91,
  "estado": "PENDIENTE",
  "origen": "ia",
  "estadoGobernanza": "pendiente_revision"
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

Acceso permitido: web admin o proceso backend autorizado. El portal cliente usa una vista pública filtrada cuando el escenario está publicado. El móvil no consume este detalle para alternativas IA.

Debe incluir:

- origen, estado de gobernanza, fuente de entrada y fechas de generación/aprobación/publicación;
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

Los mapas proyectados de origen IA no se devuelven al móvil. Para el portal cliente, solo se devuelven si el escenario o mapa fue publicado explícitamente.

## 6. Valores proyectados en puntos del escenario

```text
GET /api/escenarios-rf/{id}/puntos-proyectados?banda=5_GHZ
```

Ejemplo:

```json
{
  "puntoMedicionId": null,
  "coordX": 184.5,
  "coordY": 92.0,
  "banda": "5_GHZ",
  "rssiObservadoDbm": null,
  "rssiProyectadoDbm": -66.0,
  "diferenciaDb": null,
  "radioPrimariaId": 301,
  "rssiSecundarioDbm": -70.0,
  "incertidumbreDb": 4.2
}
```

La ausencia de un valor observado se representa con `null`; nunca se inventa un baseline para una instalación nueva. Los puntos generados por IA, sus coordenadas y sus lecturas proyectadas pertenecen al escenario y no modifican puntos ni mediciones reales.

## 7. Comparación PB-12

```text
GET /api/escenarios-rf/{id}/comparacion
```

Acceso permitido: web admin o proceso backend autorizado. El móvil no compara escenarios IA. El portal cliente visualiza únicamente comparaciones publicadas.

La respuesta ofrece, por banda:

- mapa observado cuando exista;
- mapa proyectado;
- mapa de diferencia;
- cambios de cobertura, zonas muertas, redundancia y CCI/ACI;
- puntos con mayor mejora y mayor riesgo;
- advertencia de que proyectado no equivale a medido.

## 8. Gobernanza y publicación

Contratos conceptuales para aprobación/publicación:

```text
PATCH /api/escenarios-rf/{id}/estado
POST  /api/proyectos/{proyecto_id}/publicaciones-cliente
PATCH /api/publicaciones-cliente/{id}
GET   /api/portal/{token}
```

Estados mínimos:

| Estado               | Uso                                                                              |
| -------------------- | -------------------------------------------------------------------------------- |
| `pendiente_revision` | Resultado IA interno; no visible para móvil ni cliente                           |
| `aprobado_interno`   | Validado por Bulldog Tech.; todavía no visible para cliente                      |
| `publicado_cliente`  | Disponible en el portal cliente según el enlace y selección de contenido         |
| `descartado`         | Conservado para auditoría, sin uso como resultado vigente                        |

La publicación selecciona explícitamente conjuntos, heatmaps, análisis, alternativas IA y reportes. No publica el proyecto completo por defecto.

## 9. Errores relevantes

| Código | Caso                                                                  |
| ------ | --------------------------------------------------------------------- |
| 403    | Usuario/canal no autorizado para generar, comparar o publicar IA      |
| 409    | Se intenta optimizar mientras cambió la fuente de entrada, baseline o inventario |
| 422    | Entrada inválida o combinación de banda/canal/modelo no soportada      |
| 424    | Faltan datos obligatorios para producir un escenario defendible       |
| 503    | Predictor requerido no disponible; se informa si existe fallback físico |
