# 21 — Auditoría de Implementación vs Plan Scrum

**Fecha de corte:** 29-jun-2026  
**Fuente de verdad:** implementación en `backend/`, `web/`, `mobile/`, migraciones Alembic y tests automatizados.  
**Marco de proceso:** [EnfoqueScrumV3.md](../../EnfoqueScrumV3.md), con R-1 a R-5, F3, F4 y F5.  
**Alcance documental:** plan vigente en `docs/ONLINE/PLAN-IMPLEMENTACION/`. No modifica `docs/SCRUM/`.

---

## 1. Resultado ejecutivo

La implementación real ya cubre el flujo de Sprints 0 a 6 de la modalidad 100 % en línea:

| Área | Evidencia en implementación | Estado documental |
| ---- | --------------------------- | ----------------- |
| Backend REST + IA | `backend/app/api/v1/`, `backend/app/models/`, `backend/app/ai/`, `backend/tests/` | Implementado |
| PostgreSQL como fuente única | migraciones en `backend/alembic/versions/`, modelos SQLAlchemy y ausencia de BD local móvil vigente | Implementado |
| App móvil delgada | `mobile/lib/features/*/data/datasources/*_remote_datasource.dart`, `dio`, `wifi_scan`, `flutter_secure_storage` solo para sesión | Implementado |
| Web admin | rutas `/admin/*` en `web/src/App.tsx`, páginas de usuarios, clientes, proyectos, conjuntos AP, IA y publicación | Implementado |
| Portal cliente | ruta `/portal/:token`, `PortalCliente.tsx`, `shareClient.ts`, endpoints `/api/share/*` | Implementado |

Las brechas eran principalmente documentales:

- Sprint 6 aparecía como planificado aunque el portal y enlaces públicos están implementados.
- `04-modelo-datos.md` conservaba entidades eliminadas (`analisis_cobertura`, `ap_detectado`, `escenario_optimizado`, `recomendacion_ap`, `reporte`).
- `05-product-backlog-online.md`, `06-plan-de-sprints.md`, `12-sprint-5-ia-comparacion-y-reportes.md` y `13-sprint-6-portal-cliente.md` mezclaban alcance inicial con refinamientos posteriores.
- Algunas restricciones técnicas seguían apuntando a notas antiguas en vez de a la carpeta del libro CWNA en Markdown.

---

## 2. Contraste por Sprint

| Sprint | HU planificadas vigentes | Evidencia de implementación | Observación |
| ------ | ------------------------ | --------------------------- | ----------- |
| S0 | Infraestructura | `docker-compose.yml`, `backend/Dockerfile`, `web/Dockerfile`, `nginx/nginx.conf` | Cumple R-1: infraestructura, CI/despliegue y base técnica |
| S1 | PB-13, PB-19, PB-09, PB-18, PB-01, PB-10 | `admin_usuarios.py`, `clientes.py`, `admin_proyectos.py`, `auth.py`, `proyectos.py`, pantallas admin y móvil de proyectos | Implementado |
| S2 | PB-02, PB-11 | `planos.py`, `Plano`, storage local firmado, `PlanoEditorPage`, `PlanosListPage` | Implementado |
| S3 | PB-03, PB-04 | `mediciones.py`, `PuntoMedicion`, `LecturaRSSI`, `WifiScanner`, `ThrottlingManager`, `CapturaPage` | Implementado |
| S4 | PB-20, PB-05 | `heatmaps.py`, `InterpolacionService`, `MapaCalor`, `ConjuntoAP`, `HeatmapPage` | Implementado |
| S5 | PB-07, PB-12 | `escenarios.py`, `OptimizadorAPService`, `ModeloPropagacion`, conjuntos `origen=ia`, comparación por mapas | Implementado con refinamiento: IA como conjuntos AP derivados |
| S6 | PB-15, PB-16, PB-17 | `share.py`, `TokenEnlaceCliente`, `PublicacionClienteProyecto.tsx`, `PortalCliente.tsx` | Implementado; sin descarga PDF por alcance vigente |

---

## 3. Alcance eliminado por refinamiento

| Elemento | Estado real | Documento rector |
| -------- | ----------- | ---------------- |
| PB-06 / RP4 como diagnóstico persistido | Eliminado; no hay tablas persistentes de análisis ni AP detectado | [18-reglas-gobernanza-conjuntos-ap-heatmaps.md](18-reglas-gobernanza-conjuntos-ap-heatmaps.md) |
| PB-08 / RP6 como PDF | Eliminado; no existe tabla `reporte` ni endpoint vigente de reportes | [18-reglas-gobernanza-conjuntos-ap-heatmaps.md](18-reglas-gobernanza-conjuntos-ap-heatmaps.md) |
| PB-14 sincronización offline | Eliminado por modalidad online | [05-product-backlog-online.md](05-product-backlog-online.md) |
| Inventario RF físico persistente (`ap_fisico`, `radio_ap`, `bssid_radio`) | Podado; la IA trabaja con conjuntos AP y lecturas reales/estimadas | [19-modelo-base-datos-implementado.md](19-modelo-base-datos-implementado.md) |

---

## 4. Evidencia técnica por capa

### Backend

- Routers activos: `auth`, `admin_usuarios`, `admin_proyectos`, `clientes`, `proyectos`, `notificaciones`, `planos`, `mediciones`, `heatmaps`, `escenarios`, `share`.
- Modelos físicos vigentes: `usuario`, `refresh_token`, `dispositivo_push`, `cliente`, `proyecto`, `plano`, `punto_medicion`, `lectura_rssi`, `conjunto_ap`, `conjunto_ap_item`, `mapa_calor`, `token_enlace_cliente`.
- Servicios clave: interpolación IDW, modelo de propagación FSPL/log-distance, optimizador AP, generación de polígono de interés, notificación push y storage firmado.

### Móvil

- Usa `dio` y datasources remotos para dominio; no mantiene BD local de dominio.
- Persiste sesión con `flutter_secure_storage` y no sincroniza operaciones diferidas.
- Incluye `wifi_scan`, `ThrottlingManager`, captura de puntos, planos, proyectos y heatmaps.
- Los archivos locales de base de datos móvil aparecen eliminados en el estado Git actual, consistente con la modalidad online.

### Web

- Admin: gestión de usuarios, clientes, proyectos organizacionales, revisión RF, generación IA y publicación a cliente.
- Portal: ruta pública por token, carga de contenido seleccionado y visualización de heatmaps/conjuntos permitidos.

---

## 5. Referencias CWNA relevantes

La carpeta oficial de referencia local es:

`docs/Certified Wireless Network Administrator - Official Study Guide Markdown/`

| Tema de implementación | Referencia local | Uso documental |
| ---------------------- | ---------------- | -------------- |
| dB, dBm, ganancia/pérdida y EIRP | `02-rf-fundamentals.md` | Justifica almacenar RSSI en dBm, comparar señales y expresar pérdidas/ganancias |
| Canales 2.4 GHz y solapamiento | `03-spread-spectrum-technology.md` | Justifica tratar canales próximos como interferencia adyacente y privilegiar 1/6/11 |
| FSPL y regla de 6 dB | `05-antennas-and-accessories.md` | Justifica el baseline físico del predictor IA y la relación distancia/pérdida |
| Site survey, señal, ruido, SNR, dead spots e interferencias | `11-site-survey-fundamentals.md` | Justifica la captura en plano, medición en campo, búsqueda de cobertura/dead spots e interferencias |
| Reporte de site survey | `11-site-survey-fundamentals.md` | Justifica que el portal documente metodología, cobertura y brechas aunque el PDF haya sido eliminado |

Nota: el límite de throttling Android 8.0 de 4 escaneos cada 2 minutos no proviene del CWNA; es una restricción de plataforma Android aplicada por `ThrottlingManager`.

---

## 6. Alineación con EnfoqueScrumV3

| Elemento del enfoque | Evidencia documental vigente |
| -------------------- | ---------------------------- |
| R-1 Definición inicial | Sprint 0 documentado con infraestructura, equipo, modelos y criterios |
| R-2 Sprint Planning | Cada documento de sprint declara objetivo, HU incluidas y F5 |
| R-3 Ejecución | Backlogs por tarea y evidencia de implementación por capa |
| R-4 Sprint Review | Estados implementados y criterios de aceptación registrados |
| R-5 Retrospectiva | Riesgos, refinamientos y ajustes de alcance documentados |
| F3 Product Backlog | `05-product-backlog-online.md` |
| F4 Historias de Usuario | Secciones de HU en documentos de Sprint |
| F5 Sprint Backlog | Tablas de tareas por Sprint |

---

## 7. Acciones documentales aplicadas

1. Marcar Sprint 6 como implementado en el índice.
2. Alinear Product Backlog y trazabilidad con 17 HU activas y 142 PHU.
3. Reemplazar el modelo de datos conceptual con las entidades físicas vigentes.
4. Ajustar Sprint 5 y Sprint 6 al refinamiento sin diagnóstico persistido ni PDF.
5. Referenciar directamente la carpeta Markdown del libro CWNA.

