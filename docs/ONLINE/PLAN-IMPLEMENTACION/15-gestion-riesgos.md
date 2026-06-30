# 15 — Gestión de Riesgos del Plan de Implementación

> Riesgos identificados a nivel de plan con foco en la modalidad 100 % en línea. Probabilidad (P) e impacto (I) en escala 1–5; severidad = P × I. Mitigaciones operacionalizadas como tareas de sprint o políticas del equipo.

---

## 1. Matriz general de riesgos

| Id   | Riesgo                                                                   |   P |   I | Sev. | Sprint(s) afectados | Categoría     |
| ---- | ------------------------------------------------------------------------ | --: | --: | ---: | ------------------- | ------------- |
| R-01 | Latencia de red en el lugar del survey > umbrales p95                    |   4 |   5 |   20 | S3, S6              | Online        |
| R-02 | Throttling Android ≥ 8.0 limita la productividad de captura              |   5 |   3 |   15 | S3                  | Plataforma    |
| R-03 | Modelo IA no alcanza precisión aceptable con datasets disponibles        |   3 |   5 |   15 | S5                  | Técnico       |
| R-04 | Tiempos de generación de heatmap > 3 s en proyectos grandes              |   3 |   4 |   12 | S4                  | Performance   |
| R-05 | Filtración del enlace de cliente expone datos sensibles                  |   3 |   5 |   15 | S6                  | Seguridad     |
| R-06 | Indisponibilidad del backend bloquea operación de campo (sin offline)    |   3 |   5 |   15 | S3 en adelante      | Online        |
| R-07 | Permisos Android (location, wifi) cambian entre versiones del SO         |   3 |   4 |   12 | S3                  | Plataforma    |
| R-08 | Subestimación de Sprint 5 (IA + comparación)                             |   4 |   4 |   16 | S5                  | Planificación |
| R-09 | Portal cliente con carga lenta al renderizar mapas grandes               |   3 |   3 |    9 | S6                  | Performance   |
| R-10 | OAuth2/JWT mal implementado (token expiration, refresh)                  |   2 |   5 |   10 | S1                  | Seguridad     |
| R-11 | Inyección SQL / IDOR en endpoints del portal público                     |   2 |   5 |   10 | S6                  | Seguridad     |
| R-12 | Alembic con migraciones irreversibles bloquea rollback                   |   2 |   4 |    8 | Todos               | Datos         |
| R-13 | Disponibilidad limitada del equipo (2 personas) ante baja médica         |   3 |   5 |   15 | Todos               | Equipo        |
| R-14 | Cambios de requisitos del cliente (Bulldog Tech.) durante el desarrollo  |   3 |   4 |   12 | S4-S6               | Producto      |
| R-15 | Costo de hosting (PostgreSQL + servidor IA) excede presupuesto académico |   2 |   3 |    6 | S0, S6              | Infra         |
| R-16 | Bibliotecas Konva.js o pdfx con bugs no documentados                     |   2 |   3 |    6 | S2, S6              | Técnico       |
| R-17 | Acceso a un edificio real para survey de validación no se concreta       |   3 |   4 |   12 | S3, S5              | Logístico     |
| R-18 | Tests de IA con datasets sintéticos no representan condiciones reales    |   4 |   3 |   12 | S5                  | Calidad       |

**Total de riesgos identificados:** 18 (severidad media 12.6).

---

## 2. Riesgos críticos (severidad ≥ 15) y mitigación detallada

### R-01 — Latencia de red en el lugar del survey

- **Descripción:** edificios con conectividad celular pobre (sótanos, áreas industriales) hacen que las latencias p95 (scan ≤ 1 s, heatmap ≤ 3 s, login ≤ 2 s) no se cumplan, degradando la UX.
- **Mitigaciones:**
  - Banner permanente de conectividad en `CapturaPage` con medición de latencia (Sp3-11).
  - Reintentos con backoff exponencial en `ApiClient` (Sp3-10).
  - Modo "Pausada (sin red)" con notificación clara al técnico (PB-03 CA3).
  - Documentar en el manual de uso: "Verifique conectividad celular o WiFi del cliente antes de iniciar la captura. La modalidad online requiere red estable."
- **Indicador de éxito:** ≥ 95 % de capturas en pruebas piloto ≤ 1 s p95.
- **Plan B:** si el cliente lo solicita explícitamente y el alcance académico lo permite, evaluar en futuras versiones (post-proyecto) un modo offline opcional.

### R-08 — Subestimación de Sprint 5

- **Descripción:** Sprint 5 concentra IA + comparación (29 PHU en 2 semanas) y es el de mayor incertidumbre técnica.
- **Mitigaciones:**
  - PB-08 fue eliminada; el sprint se concentra en PB-07/PB-12.
  - PB-12 (comparación) puede recortarse a MVP funcional sin pulido visual si PB-07 atrasa.
  - Modelo IA con baseline FSPL/log-distance siempre operativo; si no hay datos suficientes, se reporta degradación controlada.
  - Daily Scrum diario con foco en bloqueos de IA (Sp5-04, Sp5-05, Sp5-06).
- **Indicador de éxito:** burn-down dentro del ±15 % al día 6 de los 10.
- **Plan B:** reducir comparación a vista de métricas y dejar comparación visual avanzada para versión futura.

### R-06 — Indisponibilidad del backend bloquea operación

- **Descripción:** sin offline, cualquier caída del backend detiene el survey. SLA del proyecto académico realista: 99 % (no 99.9 %).
- **Mitigaciones:**
  - Healthcheck en `docker-compose.yml` para los 4 servicios (db, backend, web, nginx).
  - Política de despliegue: blue/green o reinicio rápido con `docker compose restart` ≤ 30 s.
  - Monitoreo simple con `uptime-kuma` o `healthchecks.io` para alertar al SM.
  - Comunicación con el cliente: ventana de mantenimiento documentada (sábados 02:00–03:00 BOL).
- **Indicador de éxito:** uptime medido ≥ 99 % en pruebas piloto.

### R-03 — Modelo IA no alcanza precisión aceptable

- **Descripción:** el baseline FSPL/log-distance o la calibración local pueden no capturar la complejidad real (paredes, materiales, multipath).
- **Mitigaciones:**
  - Baseline FSPL/log-distance siempre operativo.
  - Calibración local por plano cuando existan muestras suficientes.
  - Registrar en `metricas_ia` si se usó baseline o calibración local.
  - Presentar la propuesta como recomendación orientativa cuando falten datos reales suficientes.
- **Indicador de éxito:** propuesta IA generada con trazabilidad de calibración y sin modificar mediciones reales.

### R-05 — Filtración del enlace de cliente

- **Descripción:** un enlace público (UUID + HMAC) compartido por error filtra heatmap, análisis y plan de APs de un cliente.
- **Mitigaciones:**
  - Tokens UUID v4 (122 bits de entropía) + HMAC firmado (no falsificable).
  - Expiración configurable y revocación en cualquier momento (PB-15).
  - Auditoría: `accesos`, `ultimo_acceso`, `ip_ultimo_acceso` (PB-15 reglas).
  - Endpoint público no expone datos del técnico ni de otros proyectos (PB-17 CA5).
  - Headers de seguridad en Nginx: `Referrer-Policy: no-referrer`, `X-Robots-Tag: noindex`.
  - Comunicación con el cliente: "No publique este enlace en redes sociales ni canales públicos."
- **Indicador de éxito:** revisión de seguridad OWASP Top 10 sin findings críticos.

### R-13 — Disponibilidad limitada del equipo

- **Descripción:** equipo de 2 personas (Borys, Jhasmany). Una baja por enfermedad reduce la capacidad al 50 %.
- **Mitigaciones:**
  - Pair-programming en componentes críticos (auth, IA, portal).
  - Documentación inline obligatoria por DoD (no merge sin docstring).
  - Backlog priorizado: en caso de baja, se mantienen los RP de prioridad Alta y se difieren los Media a un sprint siguiente.
  - Plan de contingencia: extender el sprint afectado en 1 semana antes de aceptar reducción de alcance.
- **Indicador de éxito:** ningún sprint pierde más del 20 % de su alcance por riesgo de equipo.

---

## 3. Riesgos por sprint (resumen)

| Sprint | Riesgos relevantes                 | Acción de monitoreo                            |
| ------ | ---------------------------------- | ---------------------------------------------- |
| S0     | R-15                               | Validar costos de hosting al cierre del setup  |
| S1     | R-10, R-13                         | Code review de auth obligatorio                |
| S2     | R-12, R-13, R-16                   | Verificar reversibilidad de migraciones        |
| S3     | R-01, R-02, R-06, R-07, R-13, R-17 | Pruebas piloto con WiFi de oficina             |
| S4     | R-04, R-13                         | Benchmark p95 con dataset real al día 7        |
| S5     | R-03, R-08, R-13, R-17, R-18       | Daily con foco en IA; review intermedio día 6  |
| S6     | R-05, R-09, R-11, R-13, R-14       | Auditoría de seguridad y rendimiento antes del Sprint Review |

---

## 4. Política de gestión de riesgos

- **Revisión:** al inicio de cada Sprint Planning (R-2) y en cada Sprint Retrospective (R-5) se revisa esta tabla.
- **Owner:** Scrum Master (Jhasmany) mantiene el documento; Product Owner (Borys) aprueba cambios de severidad o alcance.
- **Escalamiento:** un riesgo con severidad ≥ 20 (e.g., R-01) requiere revisión inmediata con el cliente Bulldog Tech.
- **Nuevos riesgos:** se documentan al pie de la tabla §1 manteniendo numeración correlativa (R-19, R-20, ...).

---

## 5. Lecciones para futuras versiones

> Se anticipan estos puntos para la documentación post-proyecto (modalidad híbrida o evolución del producto):

1. La decisión de "100 % online" es válida para el alcance académico pero limita la operación en zonas con mala conectividad. Una v2.0 podría introducir captura local con sincronización diferida (HU PB-14 reactivada).
2. El modelo IA requiere un dataset real para alcanzar precisión profesional. Bulldog Tech. podría aportar 5–10 surveys históricos como gold standard.
3. La generación de entregables exportables queda fuera del alcance vigente; si Bulldog Tech. la solicita en producción, evaluar una cola asíncrona separada.
4. El portal del cliente podría enriquecerse con interactividad adicional (filtros, animación temporal de la captura), fuera del alcance académico actual.
