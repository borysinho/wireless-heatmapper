# Sprint 3 — Implementación

## S3.3 Avance de Implementación

### Componentes del backend

**Tabla 22.** Componentes implementados en backend para captura WiFi

| Componente | Descripción |
| ---------- | ----------- |
| `POST /api/mediciones` | Inserta un lote completo de mediciones asociado a un nuevo punto |
| `POST /api/puntos/{id}/mediciones` | Agrega lecturas adicionales a un punto existente en modo continuo |
| `GET /api/planos/{id}/puntos` | Lista los puntos persistidos de un plano |
| `GET /api/puntos/{id}` | Devuelve el detalle del punto y sus mediciones |
| `DELETE /api/puntos/{id}` | Elimina el punto y sus mediciones en cascada |
| `MedicionRepository` | Persiste lotes y clasifica el nivel por umbrales de señal |
| Alembic `c3d4e5f6a7b8` | Crea `punto_medicion` y `medicion_wifi` |
| Alembic `d5e6f7a8b9c0` | Añade `numero_lectura` para distinguir ciclos de escaneo |

### Componentes de la aplicación móvil

**Tabla 23.** Componentes implementados en la app móvil para el Sprint 3

| Componente | Descripción |
| ---------- | ----------- |
| `WifiScanner` | Envoltura sobre `wifi_scan` con validación de permisos y normalización de resultados |
| `ThrottlingManager` | Controla el límite de 4 escaneos por 2 minutos y expone contador regresivo |
| `CapturaCubit` | Gestiona ocho estados operativos: Inactiva, Loading, Activa, Enviando, Throttling, Pausada, PuntoDetalle y Error |
| `CapturaPage` | Superficie principal de captura con `InteractiveViewer` y `TransformationController` |
| `PlanoPuntosPainter` | Dibuja puntos sobre el plano con color asociado al nivel de señal |
| `PuntoDetalleSheet` | Presenta lecturas agrupadas por `numero_lectura` mediante `DraggableScrollableSheet` |
| Modo continuo | Ejecuta capturas periódicas con `Timer` configurable en 15, 30 o 60 segundos |

### Funcionalidades añadidas sobre la planificación base

Durante la implementación se incorporaron tres ajustes funcionales que complementan el alcance inicialmente descrito. El primero es el campo `numero_lectura`, necesario para diferenciar ciclos de escaneo sobre un mismo punto en modo continuo. El segundo es el endpoint específico para agregar mediciones a un punto ya existente, lo que evita duplicar marcadores innecesarios en el plano. El tercero es el estado `CapturaPuntoDetalle`, que conserva el contexto del plano mientras se inspecciona o elimina un punto desde la interfaz móvil.

### Resultado técnico del incremento

Al finalizar el Sprint 3, el sistema registra mediciones WiFi en línea, las asocia a puntos georreferenciados sobre el plano calibrado y ofrece retroalimentación visual inmediata sobre el estado de la cobertura observada en campo.

---
