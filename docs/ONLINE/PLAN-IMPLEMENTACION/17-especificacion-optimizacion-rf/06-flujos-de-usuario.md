# 06 — Flujos de Experiencia de Usuario

## 1. Principios

- La app móvil continúa siendo cliente delgado y persiste inmediatamente sus insumos en el backend.
- El móvil captura datos de campo, inventario preliminar/verificado y conjuntos manuales de APs; no genera ni visualiza alternativas IA.
- La web admin concentra la solicitud de optimización, revisión de escenarios, comparación, aprobación y publicación.
- Todo resultado proyectado lleva la etiqueta **Estimación**, nunca “medición”.
- El portal cliente solo muestra contenido publicado explícitamente por Bulldog Tech.

## 2. Flujo móvil — Captura de insumos RF

1. Importar o abrir plano calibrado.
2. Capturar puntos de medición con BSSID, SSID, canal, frecuencia y RSSI.
3. Crear conjuntos manuales de APs cuando el técnico requiera una vista de campo.
4. Generar heatmaps operativos desde AP individual, subconjunto o conjunto completo.
5. Registrar o completar inventario RF si se conoce el AP físico, radio, potencia, antena y montaje.
6. Revisar completitud y advertencias como guía de captura.
7. Guardar todo en backend para revisión posterior.

El flujo móvil termina en insumos y visualización operativa. No incluye “solicitar alternativas”, “generar recomendación IA”, “comparar escenario IA” ni “compartir PDF IA”.

## 3. Flujo web admin — Instalación nueva

1. Seleccionar “Instalación nueva”.
2. Revisar plano, mediciones, inventario RF, APs del mapa y conjuntos manuales disponibles.
3. Definir áreas objetivo y perfil de servicio.
4. Registrar o validar AP temporal y su configuración por radio.
5. Completar materiales, atenuaciones y restricciones de montaje.
6. Revisar completitud, supuestos y bloqueos.
7. Elegir la fuente de entrada: selección directa de APs del mapa, inventario RF, conjunto existente opcional o baseline observado.
8. Solicitar alternativas IA desde backend.
9. Revisar mapas por banda, configuración, costo, supuestos e incertidumbre.
10. Aprobar internamente, descartar o publicar contenido seleccionado.

## 4. Flujo web admin — Red existente

1. Seleccionar “Optimizar red existente”.
2. Ver BSSID detectados agrupados provisionalmente por banda/SSID.
3. Crear, importar o corregir APs físicos.
4. Asociar cada BSSID a su radio y AP correspondientes.
5. Confirmar posición y configuración actual.
6. Marcar APs fijos, movibles o retirables.
7. Definir áreas, clientes, restricciones y presupuesto.
8. Validar inventario y elegir la fuente de entrada: APs seleccionados del mapa, conjunto existente opcional o inventario completo.
9. Solicitar alternativas IA.
10. Revisar acciones `antes → después` por AP.
11. Aprobar internamente, descartar o publicar contenido seleccionado.

## 5. Pantallas propuestas

| Canal        | Pantalla                   | Contenido principal                                                     |
| ------------ | -------------------------- | ----------------------------------------------------------------------- |
| Móvil        | Conjuntos manuales         | APs detectados, propósito, selección y ubicación operativa              |
| Móvil        | Heatmap operativo          | Visualización por AP individual, subconjunto o conjunto completo        |
| Móvil        | Inventario RF de campo     | APs físicos, radios, BSSID y advertencias de completitud                |
| Web admin    | Requisitos RF              | Áreas objetivo, aplicaciones, densidad, bandas, roaming y presupuesto   |
| Web admin    | Inventario de APs          | APs físicos, estado, posición, radios y completitud                     |
| Web admin    | Editor de radios           | BSSID, banda, canal, ancho, potencia, RRM/DFS y antena                  |
| Web admin    | Caracterización del plano  | Muros, materiales, pérdidas y zonas permitidas                          |
| Web admin    | Revisión de entradas       | Bloqueos, advertencias y supuestos                                      |
| Web admin    | Alternativas IA            | Cobertura, costo, confianza, APs, cambios y fuente de entrada           |
| Web admin    | Detalle del escenario      | Plan sobre plano y configuración por radio                              |
| Web admin    | Comparación                | Observado/proyectado/diferencia por 2,4 GHz y 5 GHz                     |
| Web admin    | Publicación                | Selección de conjuntos, heatmaps, análisis y alternativas para cliente  |
| Portal cliente | Vista publicada          | Contenido aprobado por enlace, sin edición ni regeneración              |

## 6. Visualización por banda

La comparación web contiene pestañas:

- `2,4 GHz`;
- `5 GHz`;
- `Combinado`, solo si existe política;
- `Diferencia`.

Al tocar una celda o punto se muestran RSSI observado cuando exista, RSSI proyectado, delta cuando corresponda, radio primaria, radio secundaria e incertidumbre. Si el punto fue generado por IA, se muestra como punto proyectado sin lectura observada asociada.

## 7. Representación de un AP propuesto

Cada AP muestra una ficha compacta en web admin y, si se publica, en portal cliente:

```text
AP-04 · MOVER · 6,2 m
Modelo: catálogo/modelo aprobado
Montaje: techo, 2,8 m
2,4 GHz: canal 1 · 20 MHz · 8 dBm
5 GHz: canal 44 · 20 MHz · 14 dBm
Impacto: +18 % cobertura 5 GHz
Confianza: media (antena asumida)
```

## 8. Prevención de errores

- Advertir cuando dos BSSID posiblemente pertenecen al mismo AP, sin asociarlos automáticamente como hecho.
- No permitir introducir “50 %” de potencia sin conocer el máximo o conservarlo como valor no normalizado.
- Confirmar dominio regulatorio antes de ofrecer canales/DFS.
- Mostrar que una señal fuerte en 2,4 GHz no demuestra cobertura suficiente en 5 GHz.
- Evitar que la acción “aplicar escenario” sugiera configuración automática; en esta versión genera un plan técnico.
- Bloquear acciones de generación IA desde el móvil aunque la interfaz móvil oculte los botones.
- Mostrar claramente si una alternativa es interna, aprobada o publicada.
