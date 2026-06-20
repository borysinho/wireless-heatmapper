# 10.8 Sprint 1 — Sprint Review (R-4)

**Formato:** F1 — Revisión de Sprint
**Evento:** R-4 Sprint Review (presentación conjunta S0+S1)
**Proyecto:** Wireless HeatMapper — Sprint 0 + Sprint 1
**Número de revisión:** 1
**Objetivo de la revisión:** Validar el incremento del Sprint 1 ante el Product Owner y los interesados
**Lugar, fecha, hora:** 27 de abril de 2026, 08:00 hrs

## 10.8.1 Participantes

| Nombre                             | Rol               |
| ---------------------------------- | ----------------- |
| Jhasmany Jhunnior Fernandez Ortega | Scrum Master/Dev  |
| Herland Borys Quiroga Flores       | Product Owner/Dev |

## 10.8.2 Presentación del incremento

| Función presentada                                              | HU           |
| --------------------------------------------------------------- | ------------ |
| Docker Compose: 4 contenedores corriendo + `/api/health` 200 OK | Sprint 0     |
| Admin crea técnico y cliente en el panel web                    | PB-13, PB-19 |
| Técnico inicia sesión en la app móvil con JWT                   | PB-09        |
| Técnico crea, edita, archiva y elimina proyectos en la app      | PB-01        |
| Admin ve todos los proyectos de la organización con filtros     | PB-18        |
| Técnico busca y navega su historial de proyectos                | PB-10        |

## 10.8.3 Flujo de demo (extremo a extremo)

| Paso | Actor               | Acción demostrada                                                         | Resultado verificable                              |
| ---: | ------------------- | ------------------------------------------------------------------------- | -------------------------------------------------- |
|    1 | Administrador (web) | Crea el cliente "Bulldog Tech." y el técnico "Jhasmany"                   | Ambos registros aparecen ACTIVOS en el panel admin |
|    2 | Técnico (app móvil) | Inicia sesión con las credenciales recién creadas                         | Navega a la pantalla "Mis Proyectos" (lista vacía) |
|    3 | Técnico (app móvil) | Crea el proyecto "Edificio Central" seleccionando el cliente del catálogo | El proyecto aparece en la lista del técnico        |
|    4 | Técnico (app móvil) | Edita la descripción del proyecto y luego lo archiva                      | El proyecto pasa a la pestaña "Archivados"         |
|    5 | Administrador (web) | Accede a `/admin/proyectos` y filtra por técnico "Jhasmany"               | Visualiza el proyecto creado en el paso 3          |

## 10.8.4 Retroalimentación

| Pregunta / Comentario                                                                           | Respuesta del equipo                                                                              |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| ¿Los 29 PHU son una velocidad sostenible para un equipo de 2 personas en el primer Sprint real? | SM: sí, es conservadora; se considera 25–30 PHU como rango cómodo para Sprints futuros.           |
| ¿El modelo JWT con refresh de 7 días es adecuado para un sistema de campo en línea?             | PO: es suficiente para el alcance del producto y cubre el requisito RP8 del Plan del Proyecto.    |
| ¿El administrador podría ver el detalle de cada proyecto además del listado general?            | PO: se registra como ítem de mejora para Sprint 2 (extensión de PB-18).                           |
| Los 3 widget tests fallidos en Flutter, ¿representan riesgo para la entrega del Sprint 2?       | SM: riesgo bajo; el código funciona en dispositivo; el fix de mocks está planificado en Sprint 2. |

## 10.8.5 Tareas completadas

| HU        | Estado | PHU        |
| --------- | ------ | ---------- |
| PB-13     | Done   | 8          |
| PB-19     | Done   | 3          |
| PB-09     | Done   | 5          |
| PB-18     | Done   | 5          |
| PB-01     | Done   | 5          |
| PB-10     | Done   | 3          |
| **Total** |        | **29 PHU** |

## 10.8.6 Para lo que viene — Sprint 2

- **PB-02:** Importar plano (PNG/JPG/PDF) al backend asociado a un proyecto.
- **PB-11:** Calibrar escala del plano dibujando línea de referencia.
