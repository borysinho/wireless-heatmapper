---
applyTo: "mobile/**/*.dart"
description: "Reglas para desarrollo Flutter/Dart en la app movil (modalidad 100 % en línea): arquitectura por capas (presentation/domain/data), BLoC/Cubit, cliente Dio, seguridad de sesion y pruebas unitarias."
---

# Convenciones Flutter Mobile

Estas reglas aplican a la app movil de Wireless HeatMapper cuando exista codigo en `mobile/`.

## Alcance y objetivo

- Mantener una arquitectura consistente en Flutter/Dart.
- Alinear implementacion con el stack acordado en [AGENTS.md](../../AGENTS.md) y el [Plan de Implementación Online](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md).
- Reducir deuda tecnica desde el Sprint 1 (PB-13, PB-09, PB-18) según el [Sprint 1](../../docs/ONLINE/PLAN-IMPLEMENTACION/08-sprint-1-fundacion-backend-y-admin.md).

> **Modalidad oficial: 100 % en línea.** La app móvil es un cliente delgado: NO usa base de datos local de dominio, NO implementa sincronización diferida. Toda persistencia de dominio ocurre en el backend (PostgreSQL) vía REST.

## Arquitectura obligatoria

Usar arquitectura por capas y dependencias dirigidas hacia adentro:

- `presentation/`: pantallas, widgets, `Cubit`/`Bloc`, estados y eventos.
- `domain/`: entidades, reglas de negocio y casos de uso.
- `data/`: repositorios, mappers y cliente HTTP (`Dio`) hacia el backend REST.

Reglas:

- `presentation` no realiza llamadas HTTP directamente.
- `data` no conoce widgets ni dependencias de UI.
- Los casos de uso de `domain` exponen contratos claros para `presentation`.
- No introducir capa de persistencia local de dominio (sqflite/drift): la modalidad es 100 % online.

## Gestion de estado

- Priorizar `Cubit` para flujos simples y `Bloc` para flujos complejos.
- Definir estados explicitos (`initial`, `loading`, `success`, `error`) por cada funcionalidad.
- No mezclar logica de negocio dentro de widgets.

## Persistencia y seguridad

- **Sin persistencia local de dominio**: ninguna tabla `sqflite`/`drift` con datos de proyectos, planos, mediciones o análisis.
- Sesion y secretos: `flutter_secure_storage` (sólo para JWT access/refresh y preferencias mínimas de UI).
- Contraseñas: nunca se almacenan en el dispositivo (el backend hashea con bcrypt).
- Nunca hardcodear claves, tokens o credenciales en el codigo.
- Si los retries de un request fallan, NO se persiste el lote: se descarta y se notifica al técnico (ver [Sprint 3 PB-03](../../docs/ONLINE/PLAN-IMPLEMENTACION/10-sprint-3-captura-online.md)).

## Convenciones de codigo Dart

- Archivos: `snake_case.dart`.
- Clases y enums: `PascalCase`.
- Variables, metodos y propiedades: `lowerCamelCase`.
- Evitar archivos "god class"; separar por responsabilidad.

## Pruebas minimas

- Framework base: `flutter_test`.
- Mocks/stubs: `mocktail` (u otra libreria acordada por el equipo).
- Minimo requerido por funcionalidad:
  - 1 prueba unitaria por repositorio (con cliente HTTP mockeado).
  - 1 prueba unitaria por `Cubit`/`Bloc`.
- Incluir casos de error (credenciales invalidas, red caída, timeouts, 4xx/5xx del backend, retries agotados).

## Internacionalizacion y texto

- Idioma por defecto de la app: espanol (es-BO).
- Textos de negocio y mensajes de error en espanol claro.
- Evitar placeholders en ingles en pantallas finales.

## Relacion con artefactos Scrum

- Antes de implementar una funcionalidad, verificar su HU en el Sprint Backlog activo del [Plan de Implementación Online](../../docs/ONLINE/PLAN-IMPLEMENTACION/00-indice.md).
- Referenciar el ID de HU (`PB-NN`) en nombres de branch, commits o PR cuando aplique.
- Si una decision tecnica impacta RP1..RP9, actualizar la [matriz de trazabilidad](../../docs/ONLINE/PLAN-IMPLEMENTACION/14-trazabilidad-rp-hu.md).

## Que evitar

- Introducir patrones o frameworks de estado no acordados sin validacion del PO.
- Saltar la capa `domain` conectando UI directamente al repositorio.
- Mezclar reglas de negocio con widgets de presentacion.
- Subir secretos al repositorio o usar valores sensibles en archivos tracked.
- Reintroducir persistencia local de dominio (sqflite/drift) o lógica de sincronización diferida.
