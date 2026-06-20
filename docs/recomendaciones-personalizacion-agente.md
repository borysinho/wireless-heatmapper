# Recomendaciones de personalizaciones para el agente

Este documento recoge las **personalizaciones adicionales sugeridas** para extender la guía del agente conforme avance el proyecto **Wireless HeatMapper**. Las personalizaciones base ya están en:

- [`AGENTS.md`](../AGENTS.md) — guía global del proyecto.
- [`.github/instructions/scrum-artifacts.instructions.md`](../.github/instructions/scrum-artifacts.instructions.md) — reglas para artefactos Scrum (F3/F4/F5, R-1..R-5).

Las propuestas aquí descritas **aún no están creadas**. Se documentan como backlog de configuración del agente para activarse cuando el equipo lo decida.

---

## 1. Prompts (tareas parametrizadas)

### 1.1 `/nueva-historia-usuario`

- **Tipo:** Prompt (`.github/prompts/nueva-historia-usuario.prompt.md`).
- **Objetivo:** Generar una nueva Historia de Usuario en formato **F4**, con sus 3C (Card, Conversation, Confirmation) y criterios de aceptación `CA1..CAN`, y registrarla automáticamente:
  - En el [Product Backlog F3](SCRUM/F3-product-backlog.md) con el siguiente `PB-NN` libre.
  - En el archivo F5 del Sprint correspondiente (si ya está asignada a un Sprint).
- **Entradas sugeridas:** rol, acción, beneficio, prioridad (Alta/Media/Baja), Sprint destino.
- **Por qué es útil:** evita inconsistencias en el formato F4 y garantiza que la HU quede enlazada en los tres lugares correctos (F3, F4 del Sprint, F5).

### 1.2 `/cerrar-sprint`

- **Tipo:** Prompt (`.github/prompts/cerrar-sprint.prompt.md`).
- **Objetivo:** Generar el esqueleto de los documentos del cierre de un Sprint reutilizando el Sprint Backlog activo:
  - `07-R4-sprint-review.md` con la lista de HU completadas vs. regresadas.
  - `08-R5-sprint-retrospective.md` con las secciones estándar (qué salió bien, qué mejorar, plan de acción).
- **Entradas sugeridas:** número de Sprint, fecha de cierre.
- **Por qué es útil:** estandariza el cierre de cada Sprint y reduce el trabajo manual de copiar plantillas.

### 1.3 `/abrir-sprint`

- **Tipo:** Prompt (`.github/prompts/abrir-sprint.prompt.md`).
- **Objetivo:** A partir de las HU priorizadas en F3 para el siguiente Sprint, generar:
  - El nuevo `F4-historias-de-usuario-sprintN.md` con las HU detalladas.
  - El nuevo `F5-sprint-backlog-sprintN.md` con la tabla de tareas `Sp-NN` (esqueleto vacío para que el equipo complete en Planning Poker).
- **Por qué es útil:** mantiene la nomenclatura `F4-historias-de-usuario-sprintN.md` / `F5-sprint-backlog-sprintN.md` y enlaza desde el [índice SCRUM](SCRUM/00-indice.md).

---

## 2. Instructions (reglas auto-aplicadas por `applyTo`)

Estas se activarán cuando empiece la implementación del código (no antes).

### 2.1 `flutter-mobile.instructions.md`

- **`applyTo`:** `mobile/**/*.dart`
- **Contenido propuesto:**
  - Patrón de capas: `presentation/` (BLoC/Cubit) → `domain/` (entidades + casos de uso) → `data/` (repositorios + sqflite).
  - Convención de naming Dart (`snake_case` para archivos, `PascalCase` para clases, `lowerCamelCase` para miembros).
  - Uso obligatorio de `flutter_secure_storage` para credenciales y tokens.
  - Pruebas con `flutter_test` y `mocktail` (mínimo 1 test unitario por repositorio y por Cubit).
  - Internacionalización siempre en español (es-BO) por defecto.
- **Por qué es útil:** asegura coherencia desde la primera línea de código de la app móvil.

### 2.2 `fastapi-backend.instructions.md`

- **`applyTo`:** `backend/**/*.py`
- **Contenido propuesto:**
  - Estructura modular: `app/api/` (routers), `app/services/`, `app/models/` (SQLAlchemy), `app/schemas/` (Pydantic), `app/ai/` (módulo de IA).
  - Migraciones PostgreSQL con **Alembic**.
  - Autenticación JWT, hasheo `bcrypt`.
  - Endpoints REST en inglés (`/projects`, `/measurements`), pero mensajes y descripciones OpenAPI en español.
  - Tests con `pytest` + `httpx.AsyncClient`.
- **Por qué es útil:** previene inconsistencias entre el backend y el contrato esperado por la app móvil y la web.

### 2.3 `react-web.instructions.md`

- **`applyTo`:** `web/**/*.{ts,tsx}`
- **Contenido propuesto:**
  - Vite + React + TypeScript estricto (`strict: true`).
  - Estado con React Query (servidor) y Zustand o Context (UI local).
  - Componentes funcionales, hooks, sin `class components`.
  - Estructura: `src/features/<feature>/` (admin, cliente-portal, auth) con `components/`, `hooks/`, `api/`.
- **Por qué es útil:** alinea panel de administración (RP7) y portal de cliente (RP9) bajo un mismo patrón.

### 2.4 `docker-infra.instructions.md`

- **`applyTo`:** `**/{docker-compose*.yml,Dockerfile,nginx/**}`
- **Contenido propuesto:**
  - Servicios definidos: `backend`, `db` (PostgreSQL 15+), `web` (bundle React servido por Nginx), `nginx` (reverse proxy).
  - Variables de entorno por `.env` (nunca commitear secretos).
  - Healthchecks obligatorios para `backend` y `db`.
- **Por qué es útil:** mantiene reproducibilidad del entorno de despliegue acordado.

---

## 3. Skills (workflows on-demand con assets)

### 3.1 `validar-trazabilidad-rp`

- **Tipo:** Skill (`.github/skills/validar-trazabilidad-rp/SKILL.md`).
- **Objetivo:** Recorrer F3, F4 y F5 y verificar que cada **RP1..RP9** del PAPS tenga al menos una HU asociada y que cada HU enlace su(s) RP. Reportar huérfanos.
- **Por qué es útil:** garantiza la trazabilidad requerimientos ↔ historias ↔ tareas exigida por la materia.

### 3.2 `generar-burndown`

- **Tipo:** Skill.
- **Objetivo:** A partir del estado de las tareas `Sp-NN` del Sprint activo, generar el bloque PlantUML del Burndown Chart para insertarlo en `06-R3-daily-scrum.md`.
- **Por qué es útil:** automatiza el seguimiento diario del Sprint sin redibujar el gráfico a mano.

---

## 4. Hooks (acciones deterministas en lifecycle)

### 4.1 `validar-ids-pb-sp.json`

- **Tipo:** Hook `PreToolUse` para escritura en `docs/SCRUM/**`.
- **Objetivo:** Bloquear escrituras que rompan la secuencia `PB-NN` o `Sp-NN` (duplicados o saltos).
- **Por qué es útil:** previene corrupción del Product Backlog por ediciones simultáneas.

---

## 5. Cómo activar una recomendación

Para crear cualquiera de las personalizaciones anteriores, pedir al agente:

```
/create-prompt nueva-historia-usuario
/create-instructions flutter-mobile
/create-skill validar-trazabilidad-rp
/create-hook validar-ids-pb-sp
```

El agente seguirá las convenciones definidas en [`AGENTS.md`](../AGENTS.md) y en [`.github/instructions/scrum-artifacts.instructions.md`](../.github/instructions/scrum-artifacts.instructions.md), y aplicará el flujo descrito en el skill `agent-customization` de VS Code.

---

## 6. Estado actual

| Personalización                    | Estado       | Sprint sugerido para activarla |
| ---------------------------------- | ------------ | ------------------------------ |
| `AGENTS.md`                        | ✅ Creado    | —                              |
| `scrum-artifacts.instructions.md`  | ✅ Creado    | —                              |
| `/nueva-historia-usuario` (prompt) | ⬜ Pendiente | Cualquier momento              |
| `/cerrar-sprint` (prompt)          | ⬜ Pendiente | Antes del cierre del Sprint 1  |
| `/abrir-sprint` (prompt)           | ⬜ Pendiente | Antes del Sprint 2             |
| `flutter-mobile.instructions.md`   | ✅ Creado    | Inicio Sprint 1 (código móvil) |
| `fastapi-backend.instructions.md`  | ✅ Creado    | Sprint 5 (backend + sync)      |
| `react-web.instructions.md`        | ✅ Creado    | Sprint 5 (panel admin)         |
| `docker-infra.instructions.md`     | ✅ Creado    | Sprint 5 (despliegue)          |
| `validar-trazabilidad-rp` (skill)  | ✅ Creado    | Antes de cada Sprint Review    |
| `generar-burndown` (skill)         | ⬜ Pendiente | Sprint 1 (Daily Scrum)         |
| `validar-ids-pb-sp` (hook)         | ⬜ Pendiente | Cuando el F3 supere ~25 HU     |
