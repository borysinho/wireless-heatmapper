---
marp: true
theme: heatmapper
paginate: true
size: 16:9
footer: "Wireless HeatMapper · Sprint 0 + Sprint 1 · UAGRM-FICCT 2026"
---

<!-- _class: portada -->
<!-- _paginate: false -->
<!-- _footer: '' -->

![logo](img/logo.png)

# Wireless HeatMapper

## Sistema integrado en línea para site survey WiFi con IA

<div class="meta">

**UAGRM · FICCT · Ingeniería de Software II · Grupo 24**
Jhasmany Fernandez Ortega (SM/Dev) · Herland Borys Quiroga Flores (PO/Dev)
Cliente: **Bulldog Tech.** · Sprint Review S0 + S1 — 27 abril 2026

</div>

---

# 1. Problema y contexto

**Bulldog Tech.** realiza site surveys WiFi en interiores con un mosaico de herramientas desconectadas:

- **Fragmentación de herramientas:** apps WiFi gratuitas + planos en papel + Excel; sin georreferenciación, transcripción manual propensa a errores.
- **Recomendaciones empíricas:** la propuesta de mejora (cantidad y posición de APs) depende sólo de la experiencia del técnico, sin criterios verificables contra umbrales **CWNA-107**.
- **Sin centralización:** cada técnico guarda su trabajo localmente; el administrador no tiene visibilidad consolidada de los proyectos.
- **Entregables estáticos:** PDFs por correo; el cliente no explora ni compara escenarios.

> **Oportunidad:** transformar el proceso en uno basado en evidencia medible y compartible en línea.

---

# 2. Solución y objetivo general

Sistema **estrictamente en línea** integrado sobre una única fuente de verdad (PostgreSQL), bajo el marco técnico **CWNA-107**:

<div class="cols2">
<div>

**📱 App móvil — Flutter**
Cliente delgado para captura WiFi en campo (RSSI, SSID, BSSID, canal). Transmite en línea vía REST + JWT. Sin estado de dominio local.

</div>
<div>

**⚙️ Backend REST + IA — FastAPI**
Interpolación espacial (IDW/Kriging), análisis de cobertura y modelo ML que recomienda posicionamiento óptimo de APs (objetivo ≥ −70 dBm).

</div>
<div>

**🖥️ Web — React + TypeScript**
Panel de administración (técnicos, clientes, proyectos) y portal de cliente con heatmap interactivo accesible por enlace único.

</div>
<div>

**🎯 Marco técnico — CWNA-107**
Umbrales operativos: zona muerta < −90 dBm, diseño objetivo ≥ −70 dBm, throttling Android 8+ (4 scans / 2 min).

</div>
</div>

---

# 3. Alcance (RP1–RP9) y stack tecnológico

<div class="cols2">
<div>

**Requerimientos principales**

- **RP1** Captura WiFi en línea
- **RP2** Gestión de proyectos y planos
- **RP3** Generación de heatmap
- **RP4** Análisis automatizado de cobertura
- **RP5** IA — optimización de APs
- **RP6** Reportes PDF
- **RP7** Administración web
- **RP8** Persistencia centralizada
- **RP9** Portal de cliente

</div>
<div>

**Stack tecnológico**

| Capa    | Tecnología                     |
| ------- | ------------------------------ |
| Móvil   | Flutter · BLoC · Dio           |
| Backend | FastAPI · SQLAlchemy · Alembic |
| BD      | PostgreSQL 15                  |
| Web     | React 18 · Vite · TS           |
| Infra   | Docker Compose + Nginx         |
| CI/CD   | GitHub Actions                 |
| IA      | scikit-learn / ONNX            |

</div>
</div>

> **Exclusiones:** sin modo offline · sin SLAM · sin multi-tenant · sin medición activa de ancho de banda.

---

# 4. Proceso Scrum y cronograma

<div class="meta-grid">
<div><span class="lbl">Equipo (2)</span><span class="val">SM Jhasmany · PO Borys · ambos Devs</span></div>
<div><span class="lbl">Eventos Scrum</span><span class="val">R-1 a R-5</span></div>
<div><span class="lbl">Artefactos</span><span class="val">F3 · F4 · F5</span></div>
<div><span class="lbl">Estimación</span><span class="val">Planning Poker (Fibonacci 1–21 PHU)</span></div>

</div>

| Sprint                    | Duración          | Foco                                        |
| ------------------------- | ----------------- | ------------------------------------------- |
| **S0** Definición inicial | 1 sem (13–17 abr) | Monorepo · Docker · CI/CD · UML             |
| **S1** Fundación          | 2 sem (20–26 abr) | Backend · Auth · Admin Web · CRUD Proyectos |
| S2 Planos en línea        | 2 sem             | Importar y calibrar planos                  |
| S3 Captura WiFi           | 2 sem             | Escaneo y transmisión RSSI                  |
| S4 Heatmap + análisis     | 2 sem             | Interpolación + cobertura                   |
| S5 IA + reportes          | 2 sem             | Modelo ML + PDF                             |
| S6 Portal cliente         | 2 sem             | Acceso por enlace único                     |

---

# 5. Entregable Sprint 0 + Sprint 1

<div class="kpi">
<div><span class="num">29</span><span class="lbl">PHU completados</span></div>
<div><span class="num">6/6</span><span class="lbl">HU en estado Done</span></div>
<div><span class="num">4</span><span class="lbl">contenedores Docker</span></div>
</div>

<div class="cols2 balanced">
<div>

**Sprint 1 — HU completadas (29 PHU)**

| HU        | Descripción                      | PHU |
| --------- | -------------------------------- | --: |
| **PB-13** | Gestionar usuarios (web)         |   8 |
| **PB-19** | Gestionar clientes (web)         |   3 |
| **PB-09** | Autenticar usuario (móvil + JWT) |   5 |
| **PB-18** | Ver proyectos de la organización |   5 |
| **PB-01** | Gestionar proyecto (móvil)       |   5 |
| **PB-10** | Ver historial de proyectos       |   3 |

</div>
<div>

**Sprint 0 (R-1) — Fundación técnica**

- Monorepo `backend/` · `mobile/` · `web/`
- Docker Compose (4 contenedores)
- `GET /api/health → 200 OK`
- Migración Alembic inicial
- Pipeline CI en GitHub Actions

**Demo extremo a extremo (R-4)**

1. Admin crea técnico y cliente en el panel web.
2. Técnico inicia sesión en la app móvil (JWT).
3. Técnico crea, edita y archiva proyectos.
4. Admin supervisa con filtros por técnico/estado/fecha.

</div>
</div>

---

<!-- _class: diagram -->

# 6. Arquitectura — Despliegue Sprint 1

![Diagrama de despliegue Sprint 1](img/02-arq-despliegue-sprint-1.png)

<p class="caption">Cuatro contenedores Docker (Nginx · Backend FastAPI · Web React · PostgreSQL).</p>

---

<!-- _class: diagram -->

# 7. Modelo de datos lógico — Sprint 1

![Modelo lógico Sprint 1](img/04-datos-logico-sprint-1.png)

<p class="caption">Esquema relacional: <code>Usuario</code>, <code>RefreshToken</code>, <code>Cliente</code>, <code>Proyecto</code> + ENUM <code>EstadoProyecto</code> y <code>RolUsuario</code></p>
