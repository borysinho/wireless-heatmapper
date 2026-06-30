---
marp: true
theme: heatmapper
paginate: true
size: 16:9
footer: "Wireless HeatMapper · Panel 3 · UAGRM-FICCT 2026"
---

<!-- _class: portada -->
<!-- _paginate: false -->
<!-- _footer: '' -->

![logo](img/logo.png)

# Wireless HeatMapper

## Panel 3 · Heatmaps, análisis, IA y publicación

<div class="meta">

**Ingeniería de Software II · Grupo 24**
Jhasmany Fernandez Ortega · Herland Borys Quiroga Flores
Cliente: **Bulldog Tech.** · Junio 2026

</div>

---

# 1. Qué se presenta en Panel 3

Panel 3 se centra en la parte técnica que convierte mediciones WiFi en decisiones:

- **Sprint 4:** conjuntos de APs, generación de heatmaps y análisis automático de cobertura.
- **Sprint 5:** recomendaciones IA, comparación de escenarios y reportes PDF.
- **Avance conectado:** publicación controlada hacia portal cliente mediante enlace.

> El contenido fue contrastado con la implementación actual en `backend/`, `mobile/` y `web/`; no se incluye funcionalidad que solo exista como alcance documental.

---

# 2. Flujo implementado de heatmap

<div class="cols2">
<div>

**Entrada real**

- Plano calibrado.
- Polígono de interés obligatorio.
- Puntos de medición persistidos.
- APs agrupados por BSSID.
- Conjunto de APs seleccionado.

</div>
<div>

**Salida del backend**

- Matriz RSSI.
- Imagen PNG firmada.
- Escala CWNA.
- Puntos usados para lectura.
- Advertencias por baja densidad de muestras.

</div>
</div>

El heatmap puede generarse por **AP individual**, **subconjunto** o **conjunto completo**.

---

# 3. Algoritmos y criterios técnicos

| Elemento | Implementación |
| -------- | -------------- |
| Interpolación base | IDW con potencia 2 |
| Alternativa | Kriging ordinario determinístico |
| Escala visual | Rangos RSSI con paleta CWNA |
| Objetivo operativo | RSSI >= −70 dBm |
| Zona muerta | RSSI < −90 dBm |
| Máscara | Solo se evalúa el polígono de interés |

El sistema no dibuja solo una imagen: conserva la **matriz RSSI** para análisis, comparación e IA.

---

# 4. Análisis automático de cobertura

El backend calcula métricas accionables sobre la matriz generada:

- Porcentaje de cobertura adecuada.
- Porcentaje y cantidad de zonas muertas.
- Zonas problemáticas bajo −75 dBm.
- APs detectados con SSID, BSSID, canal, frecuencia y posición estimada.
- Solapamientos de AP con criterio RSSI >= −70 dBm.
- Interferencias **CCI** y **ACI** cuando corresponde por canal.

> Esta salida alimenta el panel inferior móvil, la revisión web y los entregables al cliente.

---

# 5. App móvil: operación del técnico

<div class="cols2">
<div>

**Lo implementado en Flutter**

- Lista APs disponibles del plano.
- Crea y edita conjuntos de APs.
- Persiste ubicación de AP dentro del conjunto.
- Genera heatmaps desde backend.
- Muestra matriz, imagen, leyenda, puntos y análisis.

</div>
<div>

**Regla de arquitectura**

- Cliente móvil delgado.
- Sin BD local de dominio.
- Operación REST en línea.
- Estado técnico persistido en PostgreSQL.
- El cálculo pesado queda en FastAPI.

</div>
</div>

La app móvil se usa para trabajo de campo y validación visual, no para ejecutar IA.

---

# 6. IA y escenarios optimizados

El módulo IA implementado recomienda ubicaciones de AP sobre el plano:

- Usa mediciones reales y mapa actual como línea base.
- Calibra un modelo de propagación por banda cuando hay muestras suficientes.
- Si no hay calibración local, usa baseline físico tipo FSPL/log-distance.
- Evalúa candidatos sobre grilla, zonas críticas y centro del plano.
- Aplica búsqueda greedy y ajuste local.
- Genera alternativas con cobertura proyectada, mejora, APs sugeridos y confianza.

La generación IA está restringida al **panel web admin**.

---

# 7. Espacio RF del proyecto

<div class="cols2">
<div>

**Conjuntos AP**

- Revisión de conjuntos creados desde móvil, web o IA.
- Estados de gobernanza: borrador, revisión, aprobado, publicado o descartado.
- Selección de qué conjunto podrá ver el cliente.
- Base para generar heatmaps por AP individual, subconjunto o conjunto completo.

</div>
<div>

**Escenarios IA**

- Generación de alternativas optimizadas desde un conjunto AP.
- Comparación entre cobertura actual y cobertura proyectada.
- Aprobación interna antes de compartir.
- Publicación de la propuesta final al cliente.

</div>
</div>

El **Espacio RF** concentra el objetivo final del proyecto: pasar del relevamiento técnico a una propuesta compartible y verificable.

---

# 8. Publicación por enlace al cliente

El cierre implementado del flujo RF está en la pestaña **Publicación**:

- El admin selecciona explícitamente **conjuntos AP publicados** y **escenarios IA publicados**.
- Define vigencia del enlace: 1, 7, 30 o 90 días.
- Puede generar solo el enlace o enviarlo al correo de referencia del cliente.
- El sistema mantiene enlaces activos/revocados, fecha de expiración y contador de accesos.
- El portal `/portal/:token` muestra únicamente el contenido autorizado del proyecto.

> Resultado final: Bulldog Tech. entrega al cliente un enlace controlado con heatmaps, análisis y propuesta RF, sin exponer información interna ni contenido no aprobado.
