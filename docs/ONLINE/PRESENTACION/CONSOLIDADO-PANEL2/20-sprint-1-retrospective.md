# 10.9 Sprint 1 — Sprint Retrospective (R-5)

**Formato:** F2 — Retrospectiva de Sprint
**Evento:** R-5 Sprint Retrospective
**Proyecto:** Wireless HeatMapper — Sprint 1
**Objetivo de la retrospectiva:** Identificar lo que funcionó bien, lo que no funcionó y las mejoras para el Sprint 2
**Lugar, fecha, hora:** 27 de abril de 2026, 10:00 hrs
**Participantes:** Jhasmany Fernandez (SM) · Herland Borys Quiroga (PO)

| ¿Qué salió bien?                                                 | ¿Qué no salió bien?                                       | ¿Problemas encontrados y cómo se resolvieron?                         | ¿Qué debemos cambiar para mejorar?                              |
| ---------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------- |
| 60/60 tests pytest en verde con 87 % de cobertura                | Widget tests Flutter: 3 con error (5/8 pasan)             | Tests Flutter fallaron por mock de ConnectivityMonitor; pendiente fix | Agregar mocks correctos para ConnectivityMonitor en el Sprint 2 |
| Docker Compose funcional con 4 contenedores desde el día 1       | No se configuró framework de tests web (Vitest)           | Sp1-11 incompleto; se decidió posponer al Sprint 2                    | Configurar Vitest para web al inicio del Sprint 2               |
| Backend con arquitectura limpia en 4 capas (api→svc→repo→models) | Capacidad excedida: 99 hrs estimadas vs 80 disponibles    | Se priorizó funcionalidad core; código ya estaba implementado         | Ser más conservadores en comprometer PHU en Planning Poker      |
| Migraciones Alembic versionadas y reversibles                    | Pruebas de aceptación con PO (6 tareas Sp1-xx) pendientes | Se realizarán en la presentación R-4 del 27 abr                       | Hacer mini-reviews al cierre de cada HU dentro del Sprint       |
| Funcionalidad completa: admin web + auth móvil + CRUD proyectos  | APK no generado por CI/CD                                 | Se construye manualmente; CI build imagen Docker sí funciona          | Configurar step de build APK en GitHub Actions para el Sprint 2 |
