# Infraestructura para la produccion de software

## Vision general

La infraestructura de Team 24 Software integra herramientas de gestion, desarrollo colaborativo, control de versiones, automatizacion, contenedores, despliegue, seguridad e inteligencia artificial aplicada al ciclo de desarrollo. El objetivo es producir software repetible, verificable y desplegable.

## Gestion del proyecto

El proyecto se gestiona con Scrum. El Product Backlog organiza historias de usuario; el Sprint Backlog descompone tareas; la Sprint Review valida incrementos; y la Retrospective captura mejoras. El tablero debe reflejar el estado real del sprint sin depender de avisos del docente.

Las herramientas aceptables para demostrar la gestion incluyen Jira, Trello, GitHub Projects o Chotrack. Para esta entrega se documenta el flujo Scrum y se conserva evidencia versionada del backlog, sprint, tareas y trazabilidad.

## Desarrollo colaborativo

| Area | Herramienta o practica |
| ---- | ---------------------- |
| Repositorio | GitHub. |
| Versionado | Git con ramas por funcionalidad y rama principal protegida. |
| Revision | Pull requests o revision cruzada antes de integrar. |
| Convenciones | Commits descriptivos, trazabilidad con HU y criterios de aceptacion. |
| Documentacion | Markdown, PlantUML y documentos consolidados. |

## Control de configuracion

Los elementos bajo control incluyen:

- Codigo fuente backend, web y movil.
- Migraciones de base de datos.
- Configuracion Docker.
- Nginx y reglas de reverse proxy.
- Variables de entorno documentadas.
- Diagramas y documentos versionados.
- Releases moviles y artefactos de despliegue.

## Automatizacion CI/CD

El pipeline de integracion continua debe ejecutar:

- Pruebas backend con pytest.
- Analisis estatico backend con ruff.
- Lint y build del frontend.
- Analisis y pruebas de Flutter.
- Construccion de imagenes Docker.
- Publicacion controlada de artefactos.
- Despliegue a servidor productivo cuando el cambio sea aprobado.

## Contenedores y despliegue

El despliegue productivo se organiza con Docker Compose:

- `nginx`: terminacion TLS y reverse proxy.
- `backend`: API FastAPI y modulo IA.
- `web`: bundle React estatico.
- `db`: PostgreSQL con volumen persistente.

Nginx publica la API bajo `/api`, el panel web, el portal de cliente y los recursos estaticos. El backend no expone directamente la base de datos al exterior.

Kubernetes se considera una alternativa de orquestacion para una etapa posterior con multiples microservicios, escalamiento horizontal o alta disponibilidad. No se adopta como tecnologia principal de esta entrega porque el alcance operativo inicial se cubre con Docker Compose, Nginx y una unica base PostgreSQL centralizada.

## Seguridad operativa

| Control | Aplicacion |
| ------- | ---------- |
| TLS | Trafico cifrado entre clientes y servidor. |
| JWT | Autenticacion de usuarios. |
| Roles | Administrador, tecnico y acceso publico controlado por token. |
| Ownership | Validacion de propiedad de proyectos y recursos. |
| Secretos | Variables de entorno y secretos de CI/CD. |
| Backups | Copias periodicas de PostgreSQL y archivos subidos. |
| Auditoria | Registro de accesos relevantes y releases. |

## Inteligencia artificial integrada al desarrollo

El equipo puede utilizar asistentes de IA en IDE para acelerar tareas de analisis, generacion de pruebas, refactorizacion, documentacion y revision. Su uso debe ser responsable: todo resultado generado por IA se revisa, prueba y adapta al criterio del equipo. La IA no reemplaza la validacion tecnica ni la responsabilidad profesional.

Ejemplos de herramientas aplicables son GitHub Copilot, Gemini, Codex u otros asistentes integrados al IDE. Su evidencia debe mostrarse como apoyo al desarrollo y a la especificacion, no como sustituto de pruebas, revisiones o aceptacion del Product Owner.

## Ambientes

| Ambiente | Uso | Reglas |
| -------- | --- | ------ |
| Local | Desarrollo individual | Datos de prueba y secretos locales. |
| Integracion | Validacion de ramas | Tests automatizados y base efimera. |
| Produccion | Acceso real del producto | TLS, backups, monitoreo y cambios aprobados. |
