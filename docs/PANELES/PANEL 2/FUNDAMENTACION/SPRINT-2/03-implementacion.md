# Sprint 2 — Implementación

## S2.3 Avance de Implementación

### Componentes del backend

**Tabla 16.** Componentes implementados en backend para el Sprint 2

| Componente | Descripción |
| ---------- | ----------- |
| `POST /api/proyectos/{id}/planos` | Recibe archivos `multipart/form-data`, valida formato y tamaño, y persiste el plano asociado al proyecto |
| `GET /api/proyectos/{id}/planos` | Lista los planos registrados para un proyecto |
| `GET /api/planos/{id}/url-firmada` | Renueva la URL temporal para descarga o visualización del plano |
| `PATCH /api/planos/{id}/calibracion` | Registra puntos de referencia y factor `escala_m_por_px` |
| `DELETE /api/planos/{id}` | Elimina un plano si no existen puntos de medición asociados |
| `StorageService` | Abstracción de almacenamiento sobre sistema de archivos con interfaz compatible con futura evolución hacia S3 |
| `PdfService` con PyMuPDF | Renderiza la primera página de PDF a PNG utilizable en la app y el backend |

### Componentes de la aplicación móvil

**Tabla 17.** Componentes implementados en la app móvil para el Sprint 2

| Componente | Descripción |
| ---------- | ----------- |
| `PlanoEditorPage` | Editor visual del plano con superficie interactiva basada en Flutter Canvas |
| `InteractiveViewer` | Habilita zoom y desplazamiento para navegar el plano sin perder precisión táctil |
| `file_picker` | Selecciona archivos PNG, JPG y PDF desde el dispositivo |
| `pdfx` | Previsualiza documentos PDF importados en la capa móvil |
| Modo calibración | Captura dos toques, solicita distancia real y dibuja la línea de referencia |
| Visualización de regla | Permite medir distancias una vez persistida la calibración |

### Infraestructura y persistencia

La capa de datos del backend se amplió con la migración Alembic `a1b2c3d4e5f6_sp2_planos`, que introduce la entidad de planos y sus campos de calibración. De manera complementaria, la infraestructura en contenedores incorpora un volumen persistente destinado al almacenamiento físico de archivos. Esta decisión mantiene separado el repositorio de código del contenido subido por el técnico y deja abierta la posibilidad de migrar el almacenamiento a un servicio compatible con S3 sin cambiar el contrato principal de la aplicación.

### Resultado técnico del incremento

Al cierre del Sprint 2, el sistema permite crear o localizar un proyecto, subir un plano en línea, visualizarlo desde la app móvil y establecer su escala real con persistencia centralizada. Ese incremento deja preparado el escenario para asociar puntos de medición georreferenciados en el Sprint 3.

---
