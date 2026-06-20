---
applyTo: "**/{docker-compose*.yml,Dockerfile,nginx/**}"
description: "Use when creating or modifying Dockerfiles, docker-compose files, Nginx reverse proxy config, environment setup, service networking, or container healthchecks for Wireless HeatMapper."
---

# Convenciones Docker Infra

Reglas para infraestructura y despliegue del proyecto Wireless HeatMapper.

## Objetivo

- Mantener entorno reproducible para desarrollo y despliegue.
- Alinear infraestructura con stack acordado en [AGENTS.md](../../AGENTS.md): FastAPI + PostgreSQL + React + Nginx.
- Evitar configuraciones inseguras o inconsistentes entre servicios.

> Plan de despliegue y diagrama de contenedores en [03-modelo-arquitectura.md](../../docs/ONLINE/PLAN-IMPLEMENTACION/03-modelo-arquitectura.md). Tareas de infra en el [Sprint 0](../../docs/ONLINE/PLAN-IMPLEMENTACION/07-sprint-0-definicion-inicial.md).

## Servicios esperados

En docker-compose definir, como minimo:

- backend: servicio FastAPI.
- db: PostgreSQL 15+.
- web: frontend React compilado y servido por Nginx o contenedor dedicado.
- nginx: reverse proxy para enrutar trafico hacia backend y web.

## Reglas de docker-compose

- Usar nombres de servicio claros y estables (backend, db, web, nginx).
- Declarar networks explicitas (no depender solo de defaults implicitos).
- Definir depends_on para orden basico de arranque cuando aplique.
- Configurar restart policy en servicios criticos.
- Declarar volumes para persistencia de datos de db.

## Variables de entorno y secretos

- Configuracion sensible solo por variables de entorno.
- Usar archivo .env para desarrollo local.
- Nunca commitear secretos reales (tokens, passwords, keys).
- Incluir valores de ejemplo en .env.example cuando aplique.

## Healthchecks y readiness

- Incluir healthcheck obligatorio para db y backend.
- Healthcheck de db debe validar disponibilidad real del motor.
- Healthcheck de backend debe validar endpoint de salud (ej. /health).
- Evitar marcar servicios como listos solo por proceso levantado.

## Nginx reverse proxy

- Nginx debe enrutar:
  - /api -> backend
  - / -> web
- Configurar cabeceras proxy basicas (Host, X-Forwarded-For, X-Forwarded-Proto).
- Definir timeouts razonables para endpoints de API.
- Evitar configuraciones inseguras o excesivamente abiertas por defecto.

## Dockerfile

- Preferir imagenes base oficiales y versiones explicitas.
- Minimizar capas y dependencias innecesarias.
- Usar multi-stage build cuando ayude a reducir tamano final.
- Definir WORKDIR consistente y usuario no-root cuando sea viable.
- No copiar archivos sensibles al contexto de build.

## Networking y puertos

- Exponer solo puertos necesarios al host.
- No publicar puertos internos que no requieren acceso externo.
- Mantener consistencia entre puertos documentados y puertos configurados.

## Calidad operativa minima

- Verificar que compose levante todos los servicios sin errores de configuracion.
- Confirmar conectividad backend <-> db y nginx <-> backend/web.
- Documentar comandos de arranque/parada en README cuando exista.

## Relacion con Scrum y trazabilidad

- Cambios de infraestructura deben referenciar HU o tarea Sp{N}-NN del [Plan de Implementación Online](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md) cuando aplique.
- Si la infraestructura habilita funcionalidades de RP1..RP9, actualizar la [matriz de trazabilidad](../../docs/ONLINE/PLAN-IMPLEMENTACION/14-trazabilidad-rp-hu.md).

## Que evitar

- Hardcodear credenciales en Dockerfile, compose o nginx.
- Crear infraestructura fuera del stack acordado sin aprobacion del PO.
- Omitir healthchecks en servicios criticos.
- Usar imagenes latest sin versionado controlado.
