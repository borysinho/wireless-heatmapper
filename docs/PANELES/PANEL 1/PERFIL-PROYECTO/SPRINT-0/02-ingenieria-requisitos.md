# Sprint 0 — Ingeniería de Requisitos

## S0.2 Ingeniería de Requisitos Inicial

Durante el Sprint 0 se realizó la sesión inicial de levantamiento de requisitos con el representante de Bulldog Tech. El Product Owner condujo la entrevista siguiendo las 3 C's: documentar las historias (Cards), conversar con el cliente para comprenderlas (Conversación) y confirmar la comprensión mediante ejemplos concretos (Confirmación).

---

### Técnicas utilizadas

- **Entrevista semiestructurada** con el cliente para identificar problemas operativos concretos.
- **Modelo de dominio preliminar** para alinear el vocabulario del negocio con el equipo.
- **Brainstorming interno** para identificar actores, funcionalidades y restricciones.

---

### Requerimientos Principales identificados (RP)

**Tabla 3.** Requerimientos principales del sistema Wireless HeatMapper

| ID    | Requerimiento Principal                                                                      | Prioridad |
| ----- | -------------------------------------------------------------------------------------------- | :-------: |
| RP1   | Gestión de usuarios y autenticación segura (JWT, roles)                                      | Alta      |
| RP2   | Gestión de clientes (organizaciones) por parte del administrador                             | Alta      |
| RP3   | Gestión de proyectos de levantamiento Wi-Fi                                                  | Alta      |
| RP4   | Levantamiento de señal Wi-Fi desde app móvil (recolección de mediciones RSSI)               | Alta      |
| RP5   | Generación de mapa de calor georreferenciado sobre plano de planta                           | Alta      |
| RP6   | Análisis con IA y generación de recomendaciones de optimización                              | Media     |
| RP7   | Panel web de administración y visualización de resultados                                    | Alta      |
| RP8   | Generación y exportación de reportes (PDF/PNG)                                               | Media     |
| RP9   | Gestión de planos de planta (carga y administración)                                         | Media     |

---

### Product Backlog inicial — Historias de Usuario (resumen)

**Tabla 4.** Product Backlog inicial — Historias de usuario priorizadas

| ID     | Historia de Usuario                                                   | PHU | Sprint |
| ------ | --------------------------------------------------------------------- | :-: | :----: |
| PB-01  | Como administrador, quiero gestionar usuarios del sistema             |  3  |   1    |
| PB-09  | Como administrador, quiero gestionar clientes (organizaciones)        |  5  |   1    |
| PB-10  | Como usuario, quiero autenticarme con correo y contraseña             |  3  |   1    |
| PB-13  | Como administrador, quiero gestionar proyectos de levantamiento       |  5  |   1    |
| PB-18  | Como administrador, quiero ver el listado de proyectos por cliente    |  3  |   1    |
| PB-19  | Como técnico, quiero autenticarme desde la app móvil                  |  3  |   1    |
| PB-02  | Como técnico, quiero seleccionar un proyecto y ver su plano           |  5  |   2    |
| PB-03  | Como técnico, quiero marcar puntos de medición sobre el plano         |  8  |   2    |
| PB-04  | Como técnico, quiero que se capture el RSSI automáticamente al marcar |  5  |   2    |
| PB-05  | Como sistema, quiero generar el heatmap a partir de las mediciones    |  8  |   2    |
| PB-06  | Como administrador, quiero ver el heatmap en el panel web             |  5  |   3    |
| PB-07  | Como sistema, quiero analizar la cobertura con IA                     | 13  |   3    |
| PB-08  | Como administrador, quiero exportar reportes en PDF                   |  5  |   3    |
| PB-11  | Como técnico, quiero gestionar planos de planta desde la app          |  5  |   2    |
| PB-12  | Como administrador, quiero gestionar planos desde el panel web        |  3  |   2    |
| PB-15  | Como cliente, quiero ver mis proyectos en el panel web                |  3  |   3    |
| PB-16  | Como sistema, quiero enviar notificaciones de alerta de cobertura     |  5  |   3    |
| PB-17  | Como administrador, quiero gestionar configuración del sistema        |  3  |   3    |

> **Nota:** PB-14 (sincronización offline) fue **eliminada** en la modalidad 100% en línea. Toda la persistencia ocurre en el backend.

---
