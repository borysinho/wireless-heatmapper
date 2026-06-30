# CONSOLIDADO-CAPITULOS — Wireless HeatMapper · Segundo Período

Esta carpeta contiene la **reestructuración formal en capítulos** del Perfil de Proyecto del sistema **Wireless HeatMapper**, conforme a la indicación del docente (clase 28-04-2026): el documento pasa de ser un "perfil de proyecto" a organizarse en capítulos numerados con fundamentación teórica y tecnológica.

---

## Estructura de capítulos

| Capítulo                                    | Contenido                                                                                                                                                                               | Fuente de archivos                          |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **Capítulo 1 — Definición del Proyecto**    | Introducción, antecedentes, descripción del problema, objetivos, alcance, tecnología, cronograma, proceso Scrum, Sprint 0 y Sprint 1                                                    | `../CONSOLIDADO/*.md` (reutilizado íntegro) |
| **Capítulo 2 — Fundamentación Teórica**     | Redes IEEE 802.11, propagación RF en interiores, métricas de cobertura (RSSI/SNR/CCI), metodología de site survey, mapas de calor e interpolación espacial, IA para optimización de APs | Archivos `cap2-*.md` de esta carpeta        |
| **Capítulo 3 — Fundamentación Tecnológica** | Arquitectura cliente-servidor REST, Flutter/Dart+BLoC, Python/FastAPI+SQLAlchemy, PostgreSQL, React+TypeScript, Docker Compose+Nginx, JWT, scikit-learn/TensorFlow                      | Archivos `cap3-*.md` de esta carpeta        |
| **Bibliografía**                            | Lista unificada con todas las fuentes académicas, técnicas y de software usadas en los tres capítulos                                                                                   | `bibliografia-actualizada.md`               |
| **Anexos**                                  | Situación actual vs. deseada, carta de aceptación, diapositivas                                                                                                                         | `../CONSOLIDADO/22-anexos.md`               |

---

## Orden de concatenación para generar el .docx final

```
CAPÍTULO 1  →  ../CONSOLIDADO/01-portada.md
               ../CONSOLIDADO/03-introduccion.md
               ../CONSOLIDADO/04-antecedentes.md
               ../CONSOLIDADO/05-descripcion-problema.md
               ../CONSOLIDADO/06-situacion-problematica.md
               ../CONSOLIDADO/07-situacion-deseada.md
               ../CONSOLIDADO/08-objetivos.md
               ../CONSOLIDADO/09-alcance.md
               ../CONSOLIDADO/10-tecnologia.md
               ../CONSOLIDADO/11-cronograma.md
               ../CONSOLIDADO/12-proceso-scrum-definiciones.md
               ../CONSOLIDADO/13-sprint-0-definicion-inicial.md
               ../CONSOLIDADO/14-sprint-1-planning.md
               ../CONSOLIDADO/15-sprint-1-historias-usuario.md
               ../CONSOLIDADO/16-sprint-1-sprint-backlog.md
               ../CONSOLIDADO/17-sprint-1-patron-desarrollo.md
               ../CONSOLIDADO/18-sprint-1-ejecucion.md
               ../CONSOLIDADO/19-sprint-1-review.md
               ../CONSOLIDADO/20-sprint-1-retrospective.md

CAPÍTULO 2  →  cap2-encabezado.md
               cap2-01-fundamentos-wifi.md
               cap2-02-propagacion-rf.md
               cap2-03-metricas-cobertura.md
               cap2-04-site-survey.md
               cap2-05-interpolacion-heatmap.md
               cap2-06-ia-optimizacion.md

CAPÍTULO 3  →  cap3-encabezado.md
               cap3-01-arquitectura-rest.md
               cap3-02-flutter-dart.md
               cap3-03-fastapi-python.md
               cap3-04-postgresql.md
               cap3-05-react-typescript.md
               cap3-06-docker-nginx.md
               cap3-07-jwt-seguridad.md
               cap3-08-scikit-ml.md

CIERRE      →  bibliografia-actualizada.md
               ../CONSOLIDADO/22-anexos.md
```

Ejecutar `_build_docx.sh` para generar automáticamente `WirelessHeatMapper-SegundoPeriodo.docx`.

---

## Requisito del segundo período (clase 28-04-2026)

El docente indicó que el documento debe:

1. Organizarse en capítulos numerados (mínimo dos de fundamentación).
2. **Fundamentación Teórica:** solo teoría del dominio (redes WiFi, propagación RF, site survey, mapas de calor, IA para cobertura) — sin hablar de herramientas de software.
3. **Fundamentación Tecnológica:** solo las tecnologías _específicas_ usadas en el proyecto (no generalidades).
4. Todo con literatura especializada, bibliografía actualizada y citas APA en el cuerpo del texto.
5. Continuar el desarrollo del software (Sprint 2 y siguientes).

---

_Última actualización: 21 de mayo de 2026._
