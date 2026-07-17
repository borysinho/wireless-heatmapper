# Manual de garantia de calidad del software

## Identidad institucional

**Empresa:** Team 24 Software  
**Eslogan:** Software medible, verificable y alineado al cliente.  
**Normas guia:** ISO/IEC 90003 e IEEE 730.  

Este manual se orienta a la empresa de software, no solamente a Wireless HeatMapper. Define politicas y procedimientos aplicables a los proyectos de Team 24 Software, usando Wireless HeatMapper como primera aplicacion institucional.

## Mision

Desarrollar soluciones de software confiables, mantenibles y verificables, aplicando practicas de ingenieria, gestion de calidad y mejora continua para resolver necesidades reales de clientes mediante productos funcionales y documentados.

## Vision

Consolidarse como una empresa capaz de entregar productos de software con trazabilidad completa, evidencia de calidad, seguridad operativa y valor de negocio medible.

## Politica de calidad

Team 24 Software se compromete a construir software que satisfaga requisitos acordados con el cliente, cumpla criterios tecnicos verificables y conserve evidencia documental suficiente para demostrar conformidad. La calidad se gestiona desde el inicio del proyecto mediante requisitos claros, diseno trazable, revision tecnica, pruebas por niveles, control de cambios y mejora continua.

## Objetivos de calidad

| Objetivo | Metrica | Meta |
| -------- | ------- | ---- |
| Requisitos verificables | Historias con criterios de aceptacion | 100 % antes de ejecucion |
| Trazabilidad | Requisitos vinculados con diseno y prueba | 100 % de funcionalidades implementadas |
| Defectos criticos | Defectos criticos abiertos al liberar | 0 |
| Calidad de codigo | Cambios revisados o validados | 100 % de incrementos entregables |
| Pruebas | Pruebas definidas ejecutadas | 100 % de pruebas obligatorias por sprint |
| Documentacion | Artefactos afectados actualizados | 100 % antes del cierre |

## Roles de calidad

| Rol | Responsabilidad |
| --- | --------------- |
| Direccion tecnica | Aprobar arquitectura, releases y decisiones de alto impacto. |
| Product Owner | Validar valor de negocio y aceptacion funcional. |
| Scrum Master | Controlar proceso, riesgos, impedimentos y mejora continua. |
| Desarrollador | Implementar y probar su propio codigo antes de entregar. |
| QA rotativo | Intentar quebrar el incremento, revisar seguridad, rendimiento y bordes. |
| Responsable de configuracion | Controlar versiones, ramas, dependencias y artefactos liberados. |

## Procesos de calidad

| Proceso | Entradas | Salidas | Evidencia |
| ------- | -------- | ------- | --------- |
| Gestion de requisitos | Necesidad del cliente | Backlog priorizado | Historias, criterios, trazabilidad |
| Diseno | Historias aceptadas | Modelos UML y decisiones | Diagramas, actas tecnicas |
| Implementacion | Diseno y criterios | Codigo integrado | Commits, revisiones, CI |
| Verificacion | Codigo ejecutable | Resultados de prueba | Reportes pytest, Flutter, web |
| Validacion | Incremento desplegable | Aceptacion o rechazo | Acta de Sprint Review |
| Liberacion | Incremento validado | Version entregable | Release, changelog, evidencia |
| Mejora | Metricas y defectos | Acciones correctivas | Retrospectiva |

## Control documental y configuracion

- Todo documento formal mantiene version, fecha, responsable y estado.
- Todo cambio de alcance se registra con impacto sobre requisitos, historias, modelos y pruebas.
- El codigo fuente se administra con Git y ramas controladas.
- Los secretos no se versionan; se gestionan por variables de entorno o mecanismos seguros.
- Los artefactos liberados se vinculan a una version de repositorio y a evidencias de prueba.

## Auditoria interna

La auditoria de calidad se ejecuta por sprint o antes de una liberacion relevante. Debe revisar:

- Trazabilidad entre requisito, historia, implementacion y prueba.
- Cumplimiento de Definition of Done.
- Resultados de pruebas automatizadas y manuales.
- Riesgos abiertos.
- Defectos bloqueantes.
- Estado de documentacion y evidencias.

## No conformidades

Una no conformidad se registra cuando un entregable no cumple un requisito, criterio de aceptacion, politica de calidad o control obligatorio. El registro minimo incluye descripcion, severidad, responsable, causa probable, accion correctiva, accion preventiva y evidencia de cierre.

## Mejora continua

Cada sprint concluye con retrospectiva. La empresa debe registrar al menos una accion de mejora, asignar responsable y verificar su cierre en el siguiente ciclo. La mejora no se limita al codigo; puede afectar pruebas, comunicacion, infraestructura, documentacion, seguridad o estimacion.

