---
applyTo: "web/**/*.{ts,tsx}"
description: "Use when creating or modifying React + TypeScript web code (admin panel, client portal, auth flows, API integration, routing, state, and UI components) in Wireless HeatMapper."
---

# Convenciones React Web

Reglas para la plataforma web (panel admin + portal de cliente) del proyecto Wireless HeatMapper.

## Objetivo

- Mantener consistencia tecnica en React + TypeScript.
- Alinear implementacion web con RP9 (portal de cliente) y los habilitadores de administración (PB-13, ver [Sprint 1](../../docs/ONLINE/PLAN-IMPLEMENTACION/08-sprint-1-fundacion-backend-y-admin.md) y [Sprint 6](../../docs/ONLINE/PLAN-IMPLEMENTACION/13-sprint-6-portal-cliente.md)).
- Reducir retrabajo por decisiones de arquitectura inconsistentes.

> Stack y convenciones generales en [AGENTS.md](../../AGENTS.md). Plan completo en [docs/ONLINE/PLAN-IMPLEMENTACION/](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md).

## Stack y configuracion

- Build tool: Vite.
- Framework: React.
- Lenguaje: TypeScript con `strict: true`.
- Evitar JavaScript sin tipado en codigo nuevo.

## Estructura recomendada

Organizar por funcionalidades:

- src/features/admin/
- src/features/cliente-portal/
- src/features/auth/

Dentro de cada feature usar carpetas coherentes:

- components/: componentes de UI.
- hooks/: hooks reutilizables.
- api/: cliente HTTP y funciones de acceso a backend.
- pages/ o views/: pantallas de la feature.
- types/: tipos compartidos de la feature.

Reglas:

- No mezclar logica de dominio con componentes de presentacion.
- Evitar componentes gigantes; separar responsabilidades.
- Mantener imports relativos claros o alias definidos de forma consistente.

## Componentes y estado

- Usar componentes funcionales y hooks.
- No usar class components en codigo nuevo.
- Estado de servidor: preferir React Query.
- Estado local/UI: usar Zustand o Context (segun complejidad).
- Evitar duplicar estado del servidor en stores locales sin justificacion.

## Integracion con backend

- Endpoints consumidos desde capa api/ por feature.
- Definir tipos de request/response en TypeScript.
- Mapear errores HTTP a mensajes de UI en espanol.
- No hardcodear URLs de entorno; usar variables de entorno de Vite.

## UX y accesibilidad minima

- Formularios con validacion en cliente y mensajes claros.
- Estados visibles de carga, vacio y error en vistas principales.
- Usar HTML semantico y atributos ARIA cuando corresponda.
- Garantizar navegacion basica por teclado en flujos criticos.

## Estilo de codigo

- Nombres de componentes en PascalCase.
- Hooks custom en formato useXxx.
- Evitar logica compleja inline en JSX; mover a hooks/utilidades.
- Mantener funciones pequenas y enfocadas.

## Pruebas minimas

- Probar componentes y hooks criticos de cada feature.
- Cubrir al menos:
  - render basico,
  - estado loading/error,
  - accion principal del flujo (ej.: login, carga de proyectos, vista de portal).
- Para integracion API, mockear respuestas exitosas y de error.

## Seguridad web

- Nunca exponer secretos en frontend.
- Tratar tokens de autenticacion con cuidado (evitar logs sensibles).
- Escapar/validar contenido dinamico mostrado al usuario.
- No confiar en validaciones solo del cliente; backend sigue siendo fuente de verdad.

## Relacion con Scrum y trazabilidad

- Antes de implementar, verificar HU del Sprint activo en el [Plan de Implementación Online](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md).
- Referenciar PB-NN en branch, commits o PR cuando aplique.
- Si el cambio impacta RP1..RP9, actualizar la [matriz de trazabilidad](../../docs/ONLINE/PLAN-IMPLEMENTACION/14-trazabilidad-rp-hu.md).

## Que evitar

- Introducir framework frontend alternativo sin aprobacion del PO.
- Acoplar componentes a llamadas HTTP directas sin capa api.
- Escribir componentes sin tipado en props/estado.
- Omitir estados de error y carga en vistas de negocio.
