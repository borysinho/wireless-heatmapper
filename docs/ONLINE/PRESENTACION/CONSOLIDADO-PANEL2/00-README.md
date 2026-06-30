# CONSOLIDADO-PANEL2 — Wireless HeatMapper

**Panel 2 · Ingeniería de Software II (FICCT-UAGRM, Grupo 24)**
**Fecha de presentación:** mayo de 2026

---

## Propósito de esta carpeta

Esta carpeta organiza el documento final del **Segundo Período** siguiendo la estructura de capítulos exigida por el docente (Clases 28-04-2026): el perfil del proyecto se convierte en el **Capítulo I**, y se añaden dos capítulos nuevos de fundamentación más el capítulo del proceso Scrum con los sprints desarrollados en este período.

La estructura sigue fielmente el modelo del Grupo 22 (gestión 2025) con los contenidos propios del Wireless HeatMapper.

---

## Estructura del documento final

```
CAPÍTULO I — DEFINICIÓN DEL PROYECTO
  (1)  Introducción
  (2)  Antecedentes
         Revisión Literaria
         Referencias de Aplicaciones
         Caso de Estudio
  (3)  Descripción del Problema
  (4)  Situación Problemática
  (5)  Situación Deseada
  (6)  Objetivos del Proyecto
  (7)  Alcance
  (8)  Tecnología
  (9)  Cronograma  ← actualizado con Sprint 2 y Sprint 3

CAPÍTULO II — FUNDAMENTOS TEÓRICOS DE REDES INALÁMBRICAS IEEE 802.11
  (2.1) Estándares IEEE 802.11 y arquitectura WLAN
  (2.2) Propagación de la señal RF en entornos interiores
  (2.3) Métricas de calidad de cobertura: RSSI y SNR
  (2.4) Metodología de site survey WiFi
  (2.5) Interpolación espacial y mapas de calor
  (2.6) Inteligencia artificial para optimización de puntos de acceso

CAPÍTULO III — ARQUITECTURA TÉCNICA DEL SISTEMA WIRELESS HEATMAPPER
  (3.1) Arquitectura cliente-servidor y principios REST
  (3.2) Flutter y Dart para la aplicación móvil
  (3.3) Python y FastAPI para el backend
  (3.4) PostgreSQL como base de datos central
  (3.5) React y TypeScript para la plataforma web
  (3.6) Docker Compose y Nginx para infraestructura y despliegue
  (3.7) JSON Web Tokens (JWT) para autenticación sin estado
  (3.8) scikit-learn y TensorFlow para el módulo de inteligencia artificial

CAPÍTULO IV — PROCESO DE DESARROLLO SCRUM
  Sprint 2 — Planos en línea (importar y calibrar)
    Sprint Planning
    Historias de Usuario (PB-02, PB-11)
    Sprint Backlog
    Patrón de Desarrollo
    Sprint Review
    Sprint Retrospective
  Sprint 3 — Captura WiFi en línea
    Sprint Planning
    Historias de Usuario (PB-03, PB-04)
    Sprint Backlog
    Patrón de Desarrollo
    Sprint Review
    Sprint Retrospective

Bibliografía

Anexos
  Anexo A — Sprint 0: Definición Inicial
  Anexo B — Sprint 1: Fundación Backend + Admin + Auth Móvil
  Anexo C — Situación Problemática y Situación Deseada (esquemas gráficos)
  Anexo D — Carta de aceptación del caso de estudio (Bulldog Tech.)
  Anexo E — Diapositivas
```

---

## Archivos en esta carpeta

| Archivo                             | Contenido                                                             |
| ----------------------------------- | --------------------------------------------------------------------- |
| `01-portada.md`                     | Portada Panel 2 (mayo 2026)                                           |
| `07-cap1-cronograma-actualizado.md` | Cronograma con Gantt de Sprint 2 y Sprint 3 (reemplaza al de Panel 1) |
| `cap4-sprint2.md`                   | Capítulo IV — Sprint 2 completo (planos en línea)                     |
| `cap4-sprint3.md`                   | Capítulo IV — Sprint 3 completo (captura WiFi en línea)               |
| `_build_docx.sh`                    | Script pandoc que produce `WirelessHeatMapper-Panel2.docx`            |

Los demás capítulos se inyectan desde carpetas hermanas:

- **Capítulo I** (secciones 1-8): `../CONSOLIDADO/03-*.md` a `10-*.md`
- **Capítulo I** (sección 9 cronograma): `./07-cap1-cronograma-actualizado.md`
- **Capítulo II**: `../CONSOLIDADO-CAPITULOS/cap2-*.md`
- **Capítulo III**: `../CONSOLIDADO-CAPITULOS/cap3-*.md`
- **Bibliografía**: `../CONSOLIDADO-CAPITULOS/bibliografia-actualizada.md`
- **Anexos Sprint 0/S1**: `../CONSOLIDADO/13-sprint-0*.md`, `14-*.md` a `20-*.md`

---

## Cómo generar el .docx

```bash
cd docs/ONLINE/PRESENTACION/CONSOLIDADO-PANEL2
bash _build_docx.sh
```

Requiere pandoc ≥ 3.0 instalado (`apt install pandoc` / `brew install pandoc`).

Salida: `WirelessHeatMapper-Panel2.docx`
