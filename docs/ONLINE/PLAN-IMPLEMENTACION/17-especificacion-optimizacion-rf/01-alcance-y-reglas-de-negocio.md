# 01 — Alcance y Reglas de Negocio

## 1. Objetivo

Refinar RP5 para que el backend y la plataforma web administrada recomienden un escenario técnicamente reproducible compuesto por:

- cantidad y ubicación de APs físicos;
- modelo, montaje y antena de cada AP;
- configuración independiente de sus radios de 2,4 GHz y 5 GHz;
- canal, ancho de canal y potencia por radio;
- heatmaps proyectados por banda;
- valores proyectados sobre puntos observados y/o puntos de predicción propios del escenario IA;
- costo, restricciones respetadas, justificación e incertidumbre.

La propuesta preserva los identificadores PB-07 y PB-12. No se crea una HU paralela ni se renombra RP5.

Este alcance queda gobernado por [18 — Reglas de Gobernanza para Conjuntos de APs, Heatmaps e IA](../18-reglas-gobernanza-conjuntos-ap-heatmaps.md): el móvil captura insumos y visualiza heatmaps operativos, pero la generación de alternativas IA se restringe a backend/web.

## 2. Conceptos de negocio

| Concepto             | Definición                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------- |
| AP físico            | Equipo instalable con posición, modelo, costo, montaje y una o más radios                   |
| Radio                | Transmisor configurable de un AP que opera en una banda concreta                            |
| BSSID                | Identificador de una interfaz/BSS anunciada por una radio; no equivale necesariamente a AP |
| Conjunto de análisis | Selección trazable de BSSID/radios observados para un propósito                             |
| Escenario RF         | Alternativa completa de APs, radios, configuraciones y predicciones                         |
| Medición observada   | RSSI y metadatos obtenidos realmente en campo                                               |
| Punto de predicción IA | Coordenada del mapa usada por el motor para estimar RSSI; puede coincidir o no con un punto medido |
| Valor proyectado     | Estimación del motor para un escenario; nunca reemplaza la medición observada               |

## 3. Gobernanza de acceso y publicación

Reglas:

1. El móvil puede aportar datos detectados, inventario declarado, posiciones y restricciones de campo.
2. El móvil no puede solicitar ni ejecutar generación de alternativas IA.
3. El móvil no puede visualizar recomendaciones IA, mapas proyectados IA ni comparaciones IA no aprobadas.
4. La web admin solicita alternativas IA, revisa resultados, compara escenarios y decide aprobación/publicación.
5. Toda alternativa IA se registra con origen `ia`, fuente de entrada utilizada, estado, autor/proceso solicitante y fecha.
6. Una alternativa IA inicia como `pendiente_revision` o estado equivalente; no queda disponible para el cliente por defecto.
7. El portal cliente solo muestra alternativas, mapas o análisis publicados explícitamente por Bulldog Tech.
8. La alternativa IA puede nacer de una selección directa de APs del mapa, del inventario RF, de un conjunto existente opcional o del baseline observado; no depende obligatoriamente de un conjunto manual creado por el técnico.
9. Los APs propuestos, sus posiciones y las lecturas proyectadas por el modelo pertenecen al escenario IA y no modifican los APs, conjuntos ni mediciones observadas.

## 4. Escenario A — Instalación nueva

La infraestructura definitiva todavía no existe. Bulldog Tech. coloca uno o más APs temporales mediante el procedimiento _AP-on-a-stick_ para caracterizar el sitio.

Reglas:

1. Cada AP temporal debe registrar posición, altura, modelo, antena y configuración de radio usada durante la captura.
2. Las mediciones se vinculan a una instantánea inmutable de esa configuración.
3. Los APs temporales son fuentes de calibración; el optimizador no está obligado a conservar sus posiciones.
4. El resultado contiene APs definitivos nuevos y una lista de materiales preliminar.
5. Si faltan datos de potencia, antena o escala, el sistema no presenta el escenario como recomendación de alta confianza.

## 5. Escenario B — Optimización de red existente

La empresa cliente ya dispone de APs en producción.

Reglas:

1. El técnico registra el inventario físico y relaciona los BSSID detectados con cada AP y radio.
2. Cada AP se clasifica como `MOVIBLE`, `FIJO` o `RETIRABLE`.
3. Cada radio se clasifica como configurable manualmente o administrada mediante RRM/TPC.
4. Las acciones posibles son `MANTENER`, `MOVER`, `RECONFIGURAR`, `CAMBIAR_MODELO`, `RETIRAR` y `AGREGAR`.
5. Un AP fijo puede reconfigurarse si sus restricciones lo permiten, pero no cambiar de coordenadas.
6. La recomendación conserva la correspondencia entre estado actual y propuesto para auditar cada cambio.

## 6. Reglas comunes de optimización

- El área objetivo se define explícitamente; no se asume que todo el plano requiere cobertura.
- El objetivo base se mantiene en RSSI ≥ −70 dBm, salvo que el perfil de servicio aprobado exija −65 dBm.
- Cuando se requiera roaming, cada punto objetivo debe buscar un AP primario y otro secundario con nivel suficiente.
- La optimización considera cobertura, interferencia, capacidad, costo y restricciones físicas; no maximiza únicamente RSSI.
- La banda de 2,4 GHz usa un plan de canales no solapados compatible con la región configurada.
- La banda de 5 GHz evalúa disponibilidad de DFS, ancho de canal y compatibilidad de clientes.
- Las radios de un mismo AP comparten posición física, aunque tengan potencia, canal y ancho diferentes.
- No se mezclan RSSI de bandas distintas sin declarar una política de combinación.
- Los SSID no son una variable primaria de propagación; se conservan para trazabilidad y cálculo de sobrecarga.
- Toda alternativa debe explicar por qué cumple o no cumple cada restricción.
- Toda alternativa queda como resultado interno hasta que un administrador la apruebe o publique.

## 7. Alternativas esperadas

El motor devuelve hasta tres alternativas, cuando sean factibles:

| Perfil                 | Prioridad                                                                 |
| ---------------------- | ------------------------------------------------------------------------- |
| Cobertura equilibrada  | Cumplimiento RF y redundancia con costo moderado                          |
| Prioridad 5 GHz        | Mejor capacidad y reutilización; 2,4 GHz se conserva para legado/alcance |
| Menor costo/cambios    | Reutiliza infraestructura existente y minimiza intervenciones             |

No se fabrican tres alternativas artificiales. Si solo existe una solución factible, se devuelve una con la explicación correspondiente.

## 8. Fuera de alcance inicial

- Configuración automática de controladores o APs del fabricante.
- Garantía de throughput basada únicamente en RSSI.
- Análisis de espectro real mediante la NIC Android.
- Optimización de 6 GHz hasta que el Product Owner la incorpore expresamente.
- Sustitución del survey de validación posterior a la instalación.
- Generación, comparación o visualización de alternativas IA desde la app móvil.
- Regeneración de heatmaps o alternativas desde el portal cliente.
