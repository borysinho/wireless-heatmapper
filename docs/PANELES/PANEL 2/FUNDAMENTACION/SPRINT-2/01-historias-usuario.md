# Sprint 2 — Historias de Usuario

## S2.1 Historias de Usuario del Sprint 2

**Objetivo del Sprint 2:** Consolidar la gestión de proyectos del técnico y habilitar el trabajo con planos en línea mediante importación, visualización y calibración métrica sobre el backend central.

**Duración:** 2 semanas (28 abr – 11 may 2026)
**Puntos de Historia del Sprint:** 16 PHU

### Cronograma del Sprint 2

![Sprint 2 — Planos en línea: importar + calibrar — 28 abr – 11 may 2026](img/04-sprint-2-detalle.png)

_Figura 25. Diagrama de Gantt — Planificación detallada del Sprint 2 (28 abr – 11 may 2026)._

---

### PB-01 — Gestionar Proyecto

| Campo | Detalle |
| ----- | ------- |
| **ID** | PB-01 |
| **Rol** | Como técnico de campo |
| **Funcionalidad** | quiero crear, editar, archivar y eliminar proyectos de survey |
| **Beneficio** | para organizar las mediciones por edificio, cliente o zona intervenida |
| **PHU** | 5 |

**Conversación / reglas de negocio:**
- El técnico autenticado solo gestiona proyectos asociados a su cuenta.
- Archivar conserva la información histórica y retira el proyecto del listado principal.
- Eliminar requiere confirmación explícita y se bloquea cuando existen reportes exportados.

**Criterios de aceptación:**
- El sistema crea un proyecto válido y lo refleja en el listado activo.
- La edición actualiza nombre, cliente y descripción sin perder historial.
- El archivado modifica el estado y oculta el proyecto del listado por defecto.
- El acceso a proyectos ajenos no está permitido.

---

### PB-10 — Ver Historial de Proyectos

| Campo | Detalle |
| ----- | ------- |
| **ID** | PB-10 |
| **Rol** | Como técnico de campo |
| **Funcionalidad** | quiero consultar mis proyectos con estado y actividad reciente |
| **Beneficio** | para retomar levantamientos sin perder contexto operativo |
| **PHU** | 3 |

**Conversación / reglas de negocio:**
- El listado ordena por última actividad descendente.
- La búsqueda filtra por nombre del proyecto y cliente asociado.
- El listado distingue proyectos activos y archivados.

**Criterios de aceptación:**
- El historial se muestra paginado y con orden consistente.
- El filtro de búsqueda responde sobre nombre y cliente.
- El técnico puede abrir el detalle de cualquier proyecto propio desde el historial.

---

### PB-02 — Importar Plano

| Campo | Detalle |
| ----- | ------- |
| **ID** | PB-02 |
| **Rol** | Como técnico de campo |
| **Funcionalidad** | quiero subir planos en formato PNG, JPG o PDF al proyecto seleccionado |
| **Beneficio** | para disponer de una base visual donde posicionar futuras mediciones WiFi |
| **PHU** | 8 |

**Conversación / reglas de negocio:**
- El backend acepta archivos de hasta 20 MB.
- Si el archivo es PDF y contiene varias páginas, se procesa la primera y se informa advertencia.
- El proyecto puede contener varios planos por locación, piso o zona.

**Criterios de aceptación:**
- Un plano válido retorna `201` con identificador, dimensiones y URL firmada.
- Un archivo que excede el tamaño permitido retorna `413`.
- Un formato no soportado retorna `415`.
- La app renderiza el plano con capacidades de zoom y desplazamiento.

---

### PB-11 — Calibrar Escala

| Campo | Detalle |
| ----- | ------- |
| **ID** | PB-11 |
| **Rol** | Como técnico de campo |
| **Funcionalidad** | quiero marcar dos puntos sobre el plano e ingresar la distancia real |
| **Beneficio** | para obtener una escala fiable en metros por píxel antes de capturar mediciones |
| **PHU** | 8 |

**Conversación / reglas de negocio:**
- La calibración es obligatoria antes de iniciar la captura del Sprint 3.
- La distancia real mínima permitida es 1 metro.
- Un plano con puntos de medición registrados no puede recalibrarse.

**Criterios de aceptación:**
- Dos toques sobre el plano dibujan una línea de referencia.
- Una distancia válida retorna el factor de escala calculado.
- Una distancia menor a 1 metro genera validación `422`.
- La escala persiste al reabrir el proyecto.

---

### Resumen del Sprint Backlog

| HU | Descripción | PHU | Estado |
| -- | ----------- | :-: | ------ |
| PB-01 | Gestionar Proyecto | 5 | Completada |
| PB-10 | Ver Historial de Proyectos | 3 | Completada |
| PB-02 | Importar Plano | 8 | Completada |
| PB-11 | Calibrar Escala | 8 | Completada |
| **Total comprometido** |  | **16** |  |

---
