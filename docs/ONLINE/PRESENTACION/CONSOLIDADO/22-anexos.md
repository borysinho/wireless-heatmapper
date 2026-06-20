# 12. Anexos

## Anexo A — Gráficos comparativos: situación actual vs. situación deseada

| Dimensión                            | Situación actual (sin Wireless HeatMapper)                                | Situación deseada (con Wireless HeatMapper)                                                 |
| ------------------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Captura de mediciones                | Apps WiFi analyzer + planilla Excel + transcripción manual                | App móvil delgada con envío en línea por punto al backend                                   |
| Georreferenciación sobre plano       | Marcas a mano sobre plano impreso                                         | Marcado interactivo sobre plano digital calibrado, persistido en backend                    |
| Generación del mapa de calor         | Edición manual posterior en software de imagen                            | Interpolación espacial automática (IDW/Kriging) ejecutada en el backend                     |
| Análisis de cobertura                | Criterio subjetivo del técnico                                            | Detección automática de zonas muertas (< −90 dBm) y CCI/ACI                                 |
| Recomendación de posicionamiento APs | Experiencia individual del técnico, sin justificación cuantitativa        | Recomendaciones generadas por módulo de IA con objetivo ≥ −70 dBm                           |
| Centralización organizacional        | Cada técnico mantiene sus propios archivos locales                        | Backend único (PostgreSQL) — el admin ve todos los proyectos de la organización             |
| Entrega al cliente                   | PDF estático armado a mano, enviado por correo                            | Portal web con enlace único + token + expiración configurable                               |
| Trazabilidad                         | Inexistente — no se puede reconstruir cuándo ni cómo se tomó una medición | End-to-end: cada medición tiene timestamp, técnico, plano, escala y coordenadas almacenadas |

## Anexo B — Carta de aceptación del cliente (Bulldog Tech.)

Documento institucional de Bulldog Tech. en el que la empresa acepta participar como cliente real del proyecto Wireless HeatMapper, recibir presentaciones de los incrementos al cierre de cada Sprint y validar funcionalmente los entregables. La carta original firmada se incluye como adjunto en la entrega física del Plan del Proyecto.

## Anexo C — Diapositivas de la presentación

Material de soporte usado durante la presentación oral de la revisión conjunta del Sprint 0 + Sprint 1. Contiene la línea narrativa del proyecto: introducción al problema, situación actual y deseada, alcance, marco Scrum, resumen del Sprint 0 y demo del Sprint 1. Las diapositivas se entregan en formato PDF como adjunto al Plan del Proyecto.

---

# 13. Apéndices

## Apéndice A — Stack tecnológico implementado

| Componente       | Tecnología                                          | Estado Sprint 1 |
| ---------------- | --------------------------------------------------- | --------------- |
| App móvil        | Flutter / Dart · BLoC/Cubit · Dio · go_router       | Operativo       |
| Backend REST     | Python 3.12 / FastAPI · SQLAlchemy · Alembic · JWT  | Operativo       |
| Base de datos    | PostgreSQL 15 (Docker)                              | Operativo       |
| Web (admin)      | React + TypeScript + Vite + TanStack Query          | Operativo       |
| Infraestructura  | Docker Compose + Nginx (reverse proxy)              | Operativo       |
| CI/CD            | GitHub Actions (lint + tests + build imagen Docker) | Operativo       |
| Pre-commit hooks | ruff · ruff-format · prettier · eslint              | Operativo       |

## Apéndice B — Definition of Done (acordada en Sprint 0)

| Criterio                               | Verificación                                                     |
| -------------------------------------- | ---------------------------------------------------------------- |
| Sí Código implementado en backend      | Endpoints REST documentados con OpenAPI/Swagger                  |
| Sí Código implementado en cliente      | Móvil (Flutter) y/o web (React) consumiendo los endpoints        |
| Sí Migraciones Alembic aplicadas       | Esquema PostgreSQL versionado y reversible                       |
| Sí Pruebas unitarias                   | Cobertura ≥ 70 % en módulos nuevos del backend                   |
| Sí Pruebas de integración              | Tests de endpoints contra BD efímera (pytest + httpx)            |
| Sí Criterios de aceptación validados   | El PO ejecuta cada CA contra el incremento desplegado            |
| Sí Code review aprobado                | Pull Request revisado por el otro miembro del equipo             |
| Sí Mergeado a `main`                   | Squash-merge desde rama `feature/PB-XX-slug`                     |
| Sí Despliegue automático               | Pipeline GitHub Actions construye imagen Docker                  |
| Sí Sin almacenamiento local de dominio | El cliente móvil no persiste entidades de dominio entre sesiones |

## Apéndice C — Trazabilidad HU ↔ RP (Sprint 1)

| HU    | Nombre                               | RP  | UC   |
| ----- | ------------------------------------ | --- | ---- |
| PB-13 | Gestionar usuarios (admin web)       | RP7 | UC13 |
| PB-19 | Gestionar clientes (admin web)       | RP7 | UC19 |
| PB-09 | Autenticar usuario (móvil)           | RP8 | UC11 |
| PB-18 | Ver proyectos de la organización     | RP7 | UC18 |
| PB-01 | Gestionar proyecto de survey (móvil) | RP8 | UC01 |
| PB-10 | Ver historial de proyectos           | RP8 | UC12 |

**RP7:** Gestión de acceso y pre-aprovisionamiento de técnicos por el administrador.
**RP8:** Operaciones CRUD del técnico autenticado contra el backend (sin persistencia local).

---

_Documento generado conforme al marco de trabajo Scrum adoptado por el equipo del proyecto._
_Última actualización: 27 de abril de 2026._
