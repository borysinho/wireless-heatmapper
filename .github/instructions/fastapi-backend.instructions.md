---
applyTo: "backend/**/*.py"
description: "Use when creating or modifying FastAPI backend code, PostgreSQL models, Alembic migrations, authentication, sync endpoints, or IA integration in Wireless HeatMapper."
---

# Convenciones FastAPI Backend

Reglas para el backend REST + IA del proyecto Wireless HeatMapper.

## Objetivo

- Mantener una arquitectura limpia y consistente para FastAPI.
- Alinear el backend con el stack acordado: Python/FastAPI + PostgreSQL.
- Facilitar trazabilidad con HU del Product Backlog del [Plan de Implementación Online](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md).

> **Modalidad oficial: 100 % en línea.** El backend es la única fuente de verdad de dominio (PostgreSQL). El cliente móvil no persiste datos de dominio ni hace sincronización diferida. Ver [PAPS Online](<../../docs/ONLINE/Wireless Heatmapper - PAPS - Modalidad Online.md>) y [AGENTS.md](../../AGENTS.md).

## Estructura recomendada

Organizar el backend con separacion por responsabilidades:

- app/api/: routers y contratos HTTP.
- app/services/: logica de aplicacion.
- app/models/: modelos ORM (SQLAlchemy).
- app/schemas/: DTOs de entrada/salida (Pydantic).
- app/repositories/: acceso a datos.
- app/ai/: inferencia y utilidades del modulo IA.
- app/core/: configuracion, seguridad y utilidades comunes.

Reglas:

- Los routers no contienen logica de negocio compleja.
- La logica de negocio vive en services/use-cases.
- Evitar acceso directo a BD desde routers.

## API y contratos

- Framework obligatorio: FastAPI.
- Endpoints y paths en ingles (ejemplo: /projects, /measurements, /auth/login).
- Mensajes de negocio y documentacion OpenAPI en espanol.
- Usar codigos HTTP consistentes y respuestas tipadas con Pydantic.

## Persistencia y migraciones

- BD central: PostgreSQL 15+.
- ORM: SQLAlchemy.
- Migraciones: Alembic (obligatorio para cambios de esquema).
- Nunca modificar tablas manualmente en entorno compartido sin migracion versionada.

## Seguridad

- Autenticacion basada en JWT.
- Hash de contrasenas con bcrypt (nunca texto plano).
- Secretos y credenciales solo por variables de entorno.
- No hardcodear tokens, passwords o connection strings.
- Aplicar validacion de entrada en todos los endpoints.

## Ingesta en línea desde la app móvil

La modalidad oficial es 100 % online. **No existe HU de sincronización diferida** (PB-14 eliminada). En su lugar:

- Endpoints transaccionales que aceptan lotes pequeños por request (ej. `POST /api/mediciones` con un lote por punto).
- Validar integridad de payload (campos requeridos, tipos, relaciones, ownership por `tecnico_id`).
- Latencias objetivo p95: scan ≤ 1 s, heatmap ≤ 3 s, login ≤ 2 s (ver [01-marco-scrum-online.md](../../docs/ONLINE/PLAN-IMPLEMENTACION/01-marco-scrum-online.md)).
- Registrar trazas de errores sin exponer datos sensibles.
- No diseñar mecanismos de "reconciliación" basados en estado local del cliente: el cliente reintenta y, si falla, se notifica al técnico.

## Modulo de IA

Cuando se implemente RP6/PB-07 (Sprint 5):

- Separar inferencia en app/ai/ para no mezclar con routers.
- Versionar modelo y parametros de inferencia.
- Definir contratos estables de request/response para recomendaciones de AP.
- Incluir validaciones para entradas fuera de rango.

## Pruebas minimas

- Framework de pruebas: pytest.
- Pruebas de API: httpx.AsyncClient (o TestClient cuando aplique).
- Minimos por funcionalidad:
  - 1 prueba de endpoint exitoso.
  - 1 prueba de validacion/error.
  - 1 prueba de servicio principal.
- Para autenticacion: cubrir login valido, invalido y token expirado.

## Observabilidad y calidad

- Registrar logs estructurados por modulo.
- Evitar imprimir secretos en logs.
- Mantener funciones pequenas y enfocadas.
- Aplicar tipado en funciones publicas.

## Relacion con Scrum

- Antes de implementar, verificar que la HU este comprometida en el Sprint activo del [Plan de Implementación Online](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md).
- Referenciar PB-NN en branch, commits o PR cuando corresponda.
- Si un cambio backend impacta RP1..RP9, actualizar la matriz de [trazabilidad RP↔HU](../../docs/ONLINE/PLAN-IMPLEMENTACION/14-trazabilidad-rp-hu.md).

## Que evitar

- Acoplar logica de negocio en routers.
- Mezclar modelos ORM con esquemas de respuesta sin capa de conversion.
- Introducir framework alternativo al stack acordado sin aprobacion del PO.
- Crear endpoints sin validacion o sin pruebas minimas.
