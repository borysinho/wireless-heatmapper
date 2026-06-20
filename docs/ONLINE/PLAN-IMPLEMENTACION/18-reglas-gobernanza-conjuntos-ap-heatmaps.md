# 18 — Reglas de Gobernanza para Conjuntos de APs, Heatmaps e IA

**Estado:** Aprobado para implementación posterior por el Product Owner — 20-jun-2026
**Alcance:** Refinamiento funcional de PB-20, PB-05, PB-06, PB-07, PB-12, PB-08, PB-15, PB-16 y PB-17
**Modalidad:** 100 % en línea

Este documento registra las reglas de producto para separar responsabilidades entre la app móvil, la plataforma web, el backend y el portal de cliente en torno a conjuntos de APs, heatmaps interactivos, alternativas generadas por IA y publicación por enlace.

El objetivo es conservar el valor operativo del móvil en campo sin exponer recomendaciones estratégicas de IA antes de que Bulldog Tech. decida aprobarlas o publicarlas formalmente al cliente.

---

## 1. Principio rector

El móvil permite capturar datos, crear conjuntos manuales de APs y visualizar heatmaps operativos de campo. La generación de alternativas con IA queda restringida a backend/web. La web administra revisión, aprobación y publicación. El cliente solo accede, mediante enlace, al contenido habilitado explícitamente por Bulldog Tech.

Esta regla no cambia la modalidad oficial del proyecto: toda persistencia de dominio ocurre en el backend y PostgreSQL sigue siendo la única fuente de verdad.

---

## 2. Frontera por canal

| Canal                    | Responsabilidad principal                                                                                      |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- |
| App móvil                | Captura en campo, calibración, medición, creación de conjuntos manuales y visualización operativa de heatmaps |
| Backend FastAPI          | Persistencia, validación, generación de heatmaps, análisis, ejecución de IA y control de estados               |
| Plataforma web admin     | Revisión, comparación, gestión de alternativas IA, aprobación y publicación                                    |
| Portal web cliente       | Consulta restringida de conjuntos, heatmaps, análisis y alternativas publicados mediante enlace                |

---

## 3. Reglas del móvil

1. El móvil puede crear conjuntos de APs manuales asociados a un plano y proyecto.
2. Cada conjunto creado desde el móvil debe guardarse en backend; no se almacena como estado de dominio local entre sesiones.
3. Un conjunto creado desde móvil nace como borrador técnico, preliminar o pendiente de revisión.
4. El móvil puede generar o solicitar heatmaps solo para visualización operativa de campo.
5. El técnico puede usar esos heatmaps para validar cobertura, revisar zonas débiles, decidir si requiere más puntos de medición o explicar una lectura preliminar si el cliente está presente.
6. Los heatmaps vistos en móvil no son entregables oficiales hasta que la web los revise y publique.
7. El móvil no debe permitir solicitar, ejecutar ni administrar generación de alternativas con IA.
8. El móvil no debe exponer alternativas IA no aprobadas, porque podrían revelar al cliente ubicaciones recomendadas o mejoras estratégicas antes del cierre comercial.

---

## 4. Reglas de conjuntos de APs

Un conjunto de APs no representa un único mapa fijo. Es una base de análisis desde la cual se pueden derivar múltiples visualizaciones.

Reglas:

1. Un conjunto contiene APs/BSSID/radios seleccionados con un propósito trazable.
2. Sobre el mismo conjunto se puede interactuar de distintas formas:
   - heatmap de un AP individual;
   - heatmap de algunos APs seleccionados;
   - heatmap del conjunto completo;
   - comparaciones temporales para apoyo de decisión en campo o revisión web.
3. La selección temporal usada para visualizar un heatmap no reemplaza el conjunto original sobre el que trabaja el técnico.
4. El backend debe conservar el origen, autor, fecha, plano, proyecto y estado del conjunto.
5. Cuando cambien las mediciones del plano, el backend debe validar nuevamente que los APs del conjunto sigan siendo utilizables para generar el heatmap.

---

## 5. Tipos de conjuntos

| Tipo de conjunto | Origen        | Uso principal                                                                          | Publicación automática |
| ---------------- | ------------- | -------------------------------------------------------------------------------------- | ---------------------- |
| Manual móvil     | Técnico móvil | Visualización operativa y creación de escenarios de campo                              | No                     |
| Manual web       | Admin web     | Preparación, ajuste o revisión formal de escenarios                                    | No                     |
| IA               | Backend/web   | Alternativas de mejora generadas desde una selección directa de APs del mapa, inventario RF, mediciones observadas o un conjunto existente opcional | No                     |
| Publicado        | Admin web     | Contenido aprobado para cliente y accesible mediante enlace según permisos definidos   | Sí, solo si fue aprobado |

Los conjuntos o alternativas de tipo IA pueden ser interactivos en web del mismo modo que los manuales: el administrador puede revisar un AP, un subconjunto o la alternativa completa antes de decidir si se publica. No requieren haber nacido de un conjunto manual creado previamente por el técnico.

---

## 6. Reglas de IA

1. La generación de alternativas con IA se solicita desde la web o desde procesos backend autorizados.
2. El móvil queda fuera del flujo de generación IA.
3. Las alternativas IA se generan a partir de datos persistidos en backend: plano, mediciones observadas, inventario RF, APs seleccionados directamente del mapa, conjuntos de APs existentes si se eligen, restricciones y parámetros aprobados.
4. Cada alternativa IA debe registrarse con origen `ia`, fuente de entrada utilizada, fecha de generación, autor o proceso solicitante, métricas, restricciones consideradas y estado.
5. Una alternativa IA inicia en estado interno, por ejemplo `pendiente_revision`.
6. La alternativa IA no debe exponerse al cliente hasta que sea aprobada y publicada por Bulldog Tech.
7. La web puede permitir comparar alternativas IA contra selecciones manuales, conjuntos manuales, mediciones reales y heatmaps actuales, siempre conservando separada la evidencia observada de los valores proyectados.
8. La IA no modifica mediciones reales ni conjuntos manuales usados como referencia. Sus APs propuestos, posiciones proyectadas, puntos simulados y lecturas estimadas se guardan como datos propios del escenario IA.

---

## 7. Reglas de publicación al cliente

1. El portal de cliente solo muestra contenido publicado explícitamente.
2. El enlace de cliente no habilita acceso general al proyecto completo.
3. La web debe permitir seleccionar qué conjuntos, heatmaps, análisis o alternativas IA se incluyen en el enlace.
4. Un conjunto o alternativa puede estar aprobado internamente sin estar publicado al cliente.
5. El cliente no puede crear, editar, regenerar ni recalcular heatmaps o alternativas.
6. El cliente solo visualiza los escenarios autorizados, con la información técnica que Bulldog Tech. considere prudente compartir.

---

## 8. Estados recomendados

| Estado               | Significado                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------- |
| `borrador_tecnico`   | Creado en móvil por técnico para análisis de campo                                        |
| `preliminar`         | Guardado en backend, aún sin revisión formal                                              |
| `pendiente_revision` | Requiere validación por administrador o responsable técnico                               |
| `aprobado_interno`   | Validado por Bulldog Tech., pero no visible para cliente                                  |
| `publicado_cliente`  | Habilitado explícitamente para el enlace de cliente                                       |
| `descartado`         | Conservado para auditoría, pero no usado como resultado vigente                           |

Estos nombres son orientativos para la implementación. La decisión técnica final puede ajustar identificadores, pero debe preservar la semántica de revisión y publicación.

---

## 9. Trazabilidad HU/RP

| Regla funcional                                      | HU impactadas                    | RP asociado |
| ---------------------------------------------------- | -------------------------------- | ----------- |
| Conjuntos manuales creados desde móvil               | PB-20                            | RP3         |
| Heatmaps operativos por AP, subconjunto o conjunto   | PB-05, PB-06                     | RP3, RP4    |
| IA restringida a backend/web                         | PB-07, PB-12                     | RP5         |
| Comparación entre escenario actual y alternativas IA | PB-12                            | RP5         |
| Reportes y resultados oficiales                      | PB-08                            | RP6         |
| Selección de contenido publicado por enlace          | PB-15, PB-16, PB-17              | RP9         |

Este refinamiento no crea nuevas HU ni renombra RP. Aclara reglas de gobernanza para las HU ya planificadas e implementadas o pendientes.

---

## 10. Criterio de aceptación documental

La implementación futura debe considerarse alineada con esta decisión cuando:

1. El móvil permita crear conjuntos manuales y visualizar heatmaps operativos sin acceder a generación IA.
2. Todo conjunto creado desde móvil persista en backend con origen y estado.
3. La web pueda revisar conjuntos manuales, selecciones directas de APs y alternativas IA antes de publicarlos.
4. La IA solo genere alternativas desde backend/web.
5. El portal de cliente muestre únicamente contenido publicado mediante enlace.
6. La trazabilidad de autor, origen, fuente de entrada, estado, proyecto, plano y fecha se conserve para cada conjunto o alternativa.
