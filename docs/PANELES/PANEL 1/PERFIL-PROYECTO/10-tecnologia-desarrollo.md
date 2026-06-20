# 10. Tecnología de Desarrollo

## 10.1 Stack Tecnológico

### Backend

**Tabla 11a.** Stack tecnológico — Backend

| Tecnología        | Uso                                           | Justificación                                                                                                                                                    |
| ----------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Python 3.11+**  | Lenguaje principal del backend                | Ecosistema maduro para ciencia de datos e IA; sintaxis clara; amplia disponibilidad de bibliotecas para procesamiento de señales y machine learning.              |
| **FastAPI**       | Framework REST API                            | Alto rendimiento (basado en Starlette/ASGI), validación automática con Pydantic, generación de documentación OpenAPI integrada y soporte nativo para async/await. |
| **PostgreSQL 15+**| Base de datos relacional central              | Motor robusto, open source, soporte de tipos espaciales (PostGIS para coordenadas), transacciones ACID y excelente integración con SQLAlchemy.                    |
| **SQLAlchemy**    | ORM y acceso a datos                          | Permite un control preciso del esquema y las consultas; facilita la migración con Alembic y desacopla el modelo de dominio del motor de BD.                       |
| **Alembic**       | Migraciones de base de datos                  | Control de versiones del esquema de base de datos alineado con el ciclo de desarrollo incremental de Scrum.                                                       |

### Aplicación Móvil

| Tecnología          | Uso                                           | Justificación                                                                                                                                               |
| ------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Flutter / Dart**  | App Android (cliente REST en línea)           | Un solo código base para múltiples plataformas, widgets Material 3, rendimiento nativo. Elimina la necesidad de BD local (modalidad 100% en línea).          |
| **BLoC / Cubit**    | Gestión de estado                             | Patrón declarativo, testeable y predecible; separa presentación de lógica de negocio conforme a la arquitectura por capas del proyecto.                     |
| **Dio**             | Cliente HTTP                                  | Interceptores de autenticación JWT, manejo de errores centralizado y soporte para *multipart* (carga de planos e imágenes).                                  |

### Frontend Web

| Tecnología              | Uso                                           | Justificación                                                                                                                                              |
| ----------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **React 18 + TypeScript** | Panel de administración web                 | Ecosistema maduro, tipado estático que reduce errores en tiempo de desarrollo, componentes reutilizables y amplio soporte de la comunidad.                  |
| **Vite**                | Bundler y servidor de desarrollo              | Compilación rápida en desarrollo, Hot Module Replacement eficiente, configuración mínima.                                                                  |
| **TanStack Query**      | Gestión de estado del servidor                | Caché automática, sincronización con el backend y manejo declarativo de estados de carga y error.                                                          |

### Infraestructura y Despliegue

| Tecnología           | Uso                                           | Justificación                                                                                                                                                  |
| -------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Docker Compose**   | Orquestación de servicios en local/producción | Reproducibilidad del entorno; todos los servicios (backend, BD, frontend, Nginx) se levantan con un único comando.                                             |
| **Nginx**            | Reverse proxy                                 | Gestión centralizada de rutas HTTP/HTTPS; separa el tráfico de la API del frontend estático.                                                                   |
| **GitHub Actions**   | CI/CD                                         | Integrado con el repositorio; automatiza linting, pruebas, construcción de imágenes Docker y despliegue al entorno de producción en cada merge a `main`.       |

### Herramientas CASE y Desarrollo Colaborativo

| Herramienta       | Uso                                                    |
| ----------------- | ------------------------------------------------------ |
| **StarUML**       | Modelado UML 2.5+: casos de uso, clases, secuencia, despliegue, paquetes |
| **PlantUML**      | Diagramas embebidos en documentación Markdown           |
| **GitHub**        | Control de versiones, gestión de issues y pull requests |
| **VS Code**       | IDE principal con extensiones para Flutter, Python y TypeScript |

---

## 10.2 Proceso de Desarrollo

El proyecto adopta **Scrum** como marco de trabajo ágil, combinando su ciclo iterativo e incremental con las cuatro actividades fundamentales de ingeniería de software: análisis, diseño, implementación y pruebas. Estas actividades se ejecutan dentro de cada sprint, lo que permite un desarrollo continuo con entregas verificables al final de cada iteración.

### Estructura del proceso

```
Sprint 0 (Inicio)
├── Organización del equipo (roles Scrum)
├── Ingeniería de Requisitos inicial (conversación con el cliente)
└── Modelos iniciales: contexto, arquitectura, datos → Product Backlog

Sprint N (1, 2, 3...)
├── Planificación del Sprint
│   ├── Selección de HU del Product Backlog
│   ├── Análisis: Las 3 C's (Cards, Conversación, Confirmación)
│   └── Sprint Backlog (tareas de granularidad mínima)
│
├── Ejecución del Sprint
│   ├── Diseño: arquitectura, datos, lógica, interfaces
│   ├── Implementación: código con estándar y refactoring
│   └── Pruebas: unitarias (dev), calidad (QA), aceptación (PO)
│
└── Revisión del Sprint
    ├── Demostración del incremento operativo al cliente
    └── Actualización del Product Backlog
```

### Roles del equipo

| Rol              | Integrante                         | Responsabilidad principal                                   |
| ---------------- | ---------------------------------- | ----------------------------------------------------------- |
| Scrum Master     | Fernandez Ortega Jhasmany Jhunnior | Facilitar el proceso Scrum; remover impedimentos             |
| Product Owner    | Quiroga Flores Herland Borys       | Gestionar el Product Backlog; representar al cliente         |
| Desarrolladores  | Ambos integrantes                  | Diseño, implementación y pruebas (equipo multifuncional)    |

### Duración de sprints

| Sprint          | Duración          | Fechas                        |
| --------------- | ----------------- | ----------------------------- |
| Sprint 0        | 1 semana (5 días) | 13 abr 2026 → 17 abr 2026    |
| Sprint 1        | 1 semana (5 días) | 20 abr 2026 → 24 abr 2026    |
| Sprint 2 al 6   | 2 semanas (14 días) | A partir del 27 abr 2026    |
| Cierre          | 1 semana (5 días) | Al finalizar Sprint 6         |

> **M0 — Presentación conjunta Sprint 0 + Sprint 1:** 27 de abril de 2026.

### Incremento

Cada sprint debe generar una **versión operativa de software** que aporte valor real al cliente. Las historias de usuario se consideran completas únicamente cuando pasan los tres filtros de prueba: unitarias (desarrollador), calidad (QA) y aceptación (Product Owner).

### Plan de Sprints — Gantt

![Plan general de Sprints — Wireless HeatMapper (modalidad 100 % en línea)](img/01-plan-general-sprints.png)

_Figura 15. Diagrama de Gantt — Cronograma de sprints del proyecto Wireless HeatMapper (abril–julio 2026)._

### Objetivos por Sprint

**Tabla 12.** Objetivos e hitos verificables por sprint

| Sprint   | Objetivo                                                                                                    | Hito verificable                                                |
| -------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Sprint 0 | Backend "hello world" con Docker Compose, PostgreSQL, CI/CD y modelos UML aprobados                        | `curl /api/health` → 200 OK                                     |
| Sprint 1 | Admin crea técnicos y clientes en panel web; técnico inicia sesión en app y gestiona proyectos             | Crear usuario/cliente en web → login en app → CRUD proyectos    |
| Sprint 2 | Técnico sube plano PNG/PDF y lo calibra sobre un proyecto; persiste en PostgreSQL                           | Recorrido completo plano + calibración                          |
| Sprint 3 | Técnico marca puntos sobre el plano y captura mediciones Wi-Fi persistidas en línea                        | Demo en vivo captura → BD muestra registros                     |
| Sprint 4 | Técnico solicita heatmap al backend y ve análisis automático (zonas muertas, CCI/ACI); el sistema aplica los umbrales CWNA-107 (−70 dBm objetivo, −90 dBm zona muerta) para clasificar las zonas | Heatmap renderizado + panel de análisis con clasificación por zonas                         |
| Sprint 5 | Técnico recibe recomendaciones de IA, compara escenarios y exporta reporte PDF                              | Recomendaciones IA + comparación + PDF descargable              |
| Sprint 6 | Técnico genera enlace; cliente lo abre en navegador y ve heatmap, análisis y plan AP                       | Portal de cliente con token real funcionando                    |


---
