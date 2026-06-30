# 18 — Reglas de Gobierno para Conjuntos de APs, Heatmaps e IA

**Estado:** Refinado según decisión de negocio — 27-jun-2026
**Alcance:** PB-20, PB-05, PB-07, PB-12, PB-15, PB-16 y PB-17
**Modalidad:** 100 % en línea

Este documento registra las reglas vigentes para separar responsabilidades entre la app móvil, la plataforma web, el backend y el portal de cliente en torno a conjuntos de APs, heatmaps interactivos y propuestas generadas por IA.

La decisión clave es que ya no existe un flujo de aprobación/publicación por estados en las entidades de RF. La publicación al cliente se resuelve mediante selección explícita de contenido en `token_enlace_cliente`.

---

## 1. Principio rector

El técnico de campo crea conjuntos AP porque esos APs son relevantes para el proyecto. En un mismo plano pueden existir varios conjuntos técnicos, pero todos representan selecciones curadas frente a lecturas externas, hotspots o APs vecinos que no forman parte del alcance del proyecto.

La IA no crea escenarios independientes. La IA crea uno o más conjuntos AP propuestos a partir de un único conjunto AP técnico. Cada conjunto IA conserva trazabilidad hacia su conjunto fuente mediante `conjunto_origen_id`.

---

## 2. Frontera por canal

| Canal                | Responsabilidad principal                                                                                      |
| -------------------- | -------------------------------------------------------------------------------------------------------------- |
| App móvil            | Captura en campo, calibración, medición, creación de conjuntos técnicos y visualización operativa de heatmaps |
| Backend FastAPI      | Persistencia, validación, generación de heatmaps y ejecución de IA                                             |
| Plataforma web admin | Revisión operativa, generación de propuestas IA y creación de enlaces cliente                                  |
| Portal web cliente   | Consulta restringida al contenido incluido explícitamente en el enlace                                         |

---

## 3. Reglas del móvil

1. El móvil puede crear conjuntos AP técnicos asociados a un plano.
2. Cada conjunto creado desde móvil se guarda inmediatamente en backend.
3. El móvil no almacena estado de dominio entre sesiones.
4. El móvil puede generar heatmaps operativos desde AP individual, subconjunto o conjunto completo.
5. El móvil no solicita ni administra generación IA.
6. El móvil no consume entidades de diagnóstico persistido ni reportes PDF.

---

## 4. Reglas de conjuntos AP

1. `conjunto_ap` es la entidad común para conjuntos técnicos y conjuntos propuestos por IA.
2. Un conjunto técnico tiene `origen = manual_movil` o `origen = manual_web`.
3. Un conjunto IA tiene `origen = ia`.
4. Un conjunto IA debe tener `conjunto_origen_id` apuntando a un único conjunto técnico.
5. No se permite generar un conjunto IA a partir de otro conjunto IA.
6. Un conjunto IA puede tener igual, menor o mayor cantidad de APs que su conjunto fuente.
7. Los datos específicos de IA se guardan como metadatos opcionales en `conjunto_ap` y `conjunto_ap_item`.
8. El conjunto fuente no se modifica cuando se generan propuestas IA.

---

## 5. Reglas de heatmap

1. `mapa_calor` representa mapas reales o proyectados.
2. Un heatmap generado desde un conjunto técnico conserva `conjunto_ap_id` hacia ese conjunto.
3. Un heatmap proyectado por IA conserva `conjunto_ap_id` hacia el conjunto IA propuesto.
4. La matriz, escala, BSSID usados y firma de mediciones permanecen en `mapa_calor`.
5. No se persiste diagnóstico de cobertura separado.
6. La generación masiva desde la previsualización web produce solo el mapa global del conjunto y los mapas individuales por AP; no crea combinaciones intermedias.

---

## 6. Reglas de IA

1. La generación IA se solicita desde web o backend autorizado.
2. La entrada obligatoria es un conjunto AP técnico existente.
3. La IA usa mediciones observadas, plano calibrado, restricciones solicitadas e inventario RF disponible.
4. La salida se persiste como uno o más `conjunto_ap` de origen `ia`.
5. Cada propuesta IA registra resumen, métricas, restricciones y versión del motor IA.
6. Cada AP propuesto registra acción recomendada, justificación, posición, banda, modelo, costo estimado y radios cuando corresponda.
7. La IA no modifica mediciones reales ni conjuntos técnicos.

---

## 7. Reglas de portal cliente

1. El portal cliente no accede al proyecto completo.
2. El enlace cliente contiene únicamente `conjunto_ids` y `mapa_ids`.
3. La selección de contenido en el enlace es la única regla de visibilidad para cliente.
4. El cliente puede consultar conjuntos y mapas de calor incluidos explícitamente en el enlace.
5. El cliente no crea, edita ni solicita generación de heatmaps o IA.
6. No existe descarga de reporte PDF desde el portal.

---

## 8. Entidades descartadas

| Elemento eliminado        | Motivo de descarte                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------- |
| `estado_gobernanza`       | La visibilidad se controla por contenido del enlace, no por estado en RF          |
| `analisis_cobertura`      | No se realizará diagnóstico persistido                                             |
| `ap_detectado`            | No se confirmarán APs inferidos desde diagnóstico                                  |
| `escenario_optimizado`    | La propuesta IA se modela como `conjunto_ap` derivado                              |
| `recomendacion_ap`        | Las recomendaciones viven en los items del conjunto IA                             |
| `valor_proyectado_punto`  | El resultado proyectado vive en `mapa_calor` asociado al conjunto IA               |
| `reporte`                 | No se exportarán PDFs desde el sistema                                             |

---

## 9. Trazabilidad HU/RP

| Regla funcional                                      | HU impactadas           | RP asociado |
| ---------------------------------------------------- | ----------------------- | ----------- |
| Conjuntos técnicos creados desde móvil               | PB-20                   | RP3         |
| Heatmaps por AP, subconjunto o conjunto completo     | PB-05                   | RP3, RP4    |
| Generación masiva sin combinaciones intermedias      | PB-05, PB-07, PB-12     | RP3, RP5    |
| IA restringida a backend/web                         | PB-07, PB-12            | RP5         |
| Propuestas IA como conjuntos derivados               | PB-07, PB-12            | RP5         |
| Selección de contenido por enlace cliente            | PB-15, PB-16, PB-17     | RP9         |

Este refinamiento no crea nuevas HU ni renombra RP. Ajusta la solución al modelo de negocio vigente.
