# Diagramas Mermaid de los Paneles

El presente directorio consolida la conversión de diagramas PlantUML a Mermaid para su reutilización, revisión técnica e importación en StarUML 7.0. Cada archivo `.mmd` contiene únicamente código Mermaid puro y preserva, en lo posible, la semántica UML 2.5 del diagrama de origen.

## Panel 1

| Archivo | Tipo UML 2.5 | Fuente PlantUML original | Descripción breve |
| ------- | ------------ | ------------------------ | ----------------- |
| `panel1/p1-01-ishikawa-causa-efecto.mmd` | Mapa mental | `05-descripcion-problema.md`, línea 21 | Diagrama de causa-efecto sobre la deficiente gestión de cobertura Wi-Fi en Bulldog Tech. |
| `panel1/p1-02-modelo-dominio.mmd` | Diagrama de clases | `05-descripcion-problema.md`, línea 66 | Modelo de dominio general del sistema Wireless HeatMapper. |
| `panel1/p1-12-situacion-actual-deseada.mmd` | Diagrama de actividad aproximado en `flowchart LR` | `12-anexos.md`, línea 7 | Contraste entre la situación operativa actual y la situación deseada. |
| `panel1/sprint0/p1-s0-01-casos-uso.mmd` | Diagrama de casos de uso aproximado en `flowchart LR` | `SPRINT-0/03-modelos-iniciales.md`, línea 11 | Contexto funcional inicial del Sprint 0. |
| `panel1/sprint0/p1-s0-02-paquetes.mmd` | Diagrama de paquetes aproximado en `flowchart TB` | `SPRINT-0/03-modelos-iniciales.md`, línea 68 | Arquitectura por paquetes propuesta para móvil, backend, web y base de datos. |
| `panel1/sprint0/p1-s0-03-despliegue.mmd` | Diagrama de despliegue aproximado en `flowchart TB` | `SPRINT-0/03-modelos-iniciales.md`, línea 143 | Distribución de artefactos y contenedores para el Sprint 0. |
| `panel1/sprint0/p1-s0-04-datos-conceptual.mmd` | Diagrama de clases | `SPRINT-0/03-modelos-iniciales.md`, línea 182 | Modelo de datos conceptual inicial del producto. |
| `panel1/sprint1/p1-s1-01-casos-uso.mmd` | Diagrama de casos de uso aproximado en `flowchart LR` | `SPRINT-1/02-modelos.md`, línea 11 | Alcance funcional del Sprint 1 para autenticación y administración. |
| `panel1/sprint1/p1-s1-02-paquetes.mmd` | Diagrama de paquetes aproximado en `flowchart TB` | `SPRINT-1/02-modelos.md`, línea 49 | Estructura lógica por componentes del Sprint 1. |
| `panel1/sprint1/p1-s1-03-despliegue.mmd` | Diagrama de despliegue aproximado en `flowchart TB` | `SPRINT-1/02-modelos.md`, línea 130 | Topología de despliegue para clientes, proxy, backend y base de datos. |
| `panel1/sprint1/p1-s1-04-datos-conceptual.mmd` | Diagrama de clases | `SPRINT-1/02-modelos.md`, línea 173 | Entidades principales del Sprint 1 con tipos de datos básicos. |
| `panel1/sprint1/p1-s1-05-secuencia-autenticacion.mmd` | Diagrama de secuencia | `SPRINT-1/02-modelos.md`, línea 265 | Flujo de autenticación entre frontend, API, servicio de autenticación y base de datos. |

## Panel 2

| Archivo | Tipo UML 2.5 | Fuente PlantUML original | Descripción breve |
| ------- | ------------ | ------------------------ | ----------------- |
| `panel2/sprint2/p2-s2-01-casos-uso.mmd` | Diagrama de casos de uso aproximado en `flowchart LR` | `PANEL 2/SPRINT-2/02-modelos.md`, línea 7 | Casos de uso del Sprint 2 para importación y calibración de planos. |
| `panel2/sprint2/p2-s2-02-clases.mmd` | Diagrama de clases | `PANEL 2/SPRINT-2/02-modelos.md`, línea 43 | Relación conceptual entre proyecto y plano durante el Sprint 2. |
| `panel2/sprint2/p2-s2-03-secuencia-subida.mmd` | Diagrama de secuencia | `PANEL 2/SPRINT-2/02-modelos.md`, línea 82 | Flujo de subida de un plano desde la app móvil al backend. |
| `panel2/sprint2/p2-s2-04-secuencia-calibracion.mmd` | Diagrama de secuencia | `PANEL 2/SPRINT-2/02-modelos.md`, línea 113 | Proceso de calibración de escala del plano importado. |
| `panel2/sprint3/p2-s3-01-casos-uso.mmd` | Diagrama de casos de uso aproximado en `flowchart LR` | `PANEL 2/SPRINT-3/02-modelos.md`, línea 7 | Contexto funcional del Sprint 3 para captura y marcado de mediciones. |
| `panel2/sprint3/p2-s3-02-secuencia-captura.mmd` | Diagrama de secuencia | `PANEL 2/SPRINT-3/02-modelos.md`, línea 38 | Secuencia de captura y persistencia de señales Wi-Fi. |
| `panel2/sprint3/p2-s3-03-estados-captura.mmd` | Diagrama de estados | `PANEL 2/SPRINT-3/02-modelos.md`, línea 71 | Máquina de estados de la sesión de captura. |

## Plan de sprints

| Archivo | Tipo UML 2.5 | Fuente PlantUML original | Descripción breve |
| ------- | ------------ | ------------------------ | ----------------- |
| `plan-sprints/pert-dependencias.mmd` | Diagrama de actividad aproximado en `flowchart TD` | `plan-de-sprints.md`, línea 52 | Dependencias secuenciales y ruta crítica del plan de sprints. |
| `plan-sprints/velocidad-sprints.mmd` | Diagrama temporal convertido a `xychart-beta` | `plan-de-sprints.md`, línea 116 | Velocidad esperada por sprint medida en PHU planificados. |

## Nota de conversión

Los bloques `@startgantt` se excluyeron de manera deliberada por solicitud explícita. La conversión se limitó a los diagramas PlantUML solicitados y a un diagrama temporal conciso trasladado a `xychart-beta`.

---
