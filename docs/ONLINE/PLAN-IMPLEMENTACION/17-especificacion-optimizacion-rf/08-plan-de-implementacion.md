# 08 — Plan de Implementación y Decisiones

## 1. Condición de inicio

No implementar hasta que el Product Owner apruebe:

- modelo AP físico/radio/BSSID;
- datos obligatorios y supuestos permitidos;
- métricas y perfiles de optimización;
- tratamiento regulatorio y de 6 GHz;
- criterios de aceptación de este paquete.

## 2. Orden recomendado

### Etapa 1 — Alinear documentación normativa

1. Refinar RP5 en el PAPS Online sin duplicar esta especificación; enlazarla.
2. Refinar PB-07 y PB-12 y sus criterios de aceptación.
3. Actualizar UC08/UC09, modelo de datos y trazabilidad.
4. Corregir la referencia “Tabla 3.1 FSPL”: la tabla corresponde a materiales.

### Etapa 2 — Inventario y captura contextual

1. Migraciones de AP físico, radio, BSSID, antena e instantánea RF.
2. Endpoints y validaciones de inventario.
3. Formularios móviles para ambos escenarios.
4. Asociación asistida BSSID → radio → AP.

### Etapa 3 — Predictor RF

1. Normalización de potencia/EIRP.
2. Modelo log-distance por banda y obstáculos.
3. Patrones de antena y calibración.
4. Predicción por punto y grilla con incertidumbre.

### Etapa 4 — Optimizador

1. Generación de candidatos y restricciones duras.
2. Score multiobjetivo.
3. Acciones para infraestructura existente.
4. Alternativas y explicación.

### Etapa 5 — Comparación y entrega

1. Heatmaps por banda y política combinada.
2. Valores proyectados en puntos.
3. UX de comparación PB-12.
4. Reporte técnico y portal de cliente.

### Etapa 6 — Validación

1. Tests sintéticos y contractuales.
2. Piloto controlado con AP temporal.
3. Survey posterior a instalación.
4. Ajuste de umbrales y confianza.

## 3. Compatibilidad y migración

- Crear primero tablas nuevas sin eliminar columnas vigentes.
- Migrar BSSID detectados como registros provisionales no vinculados.
- Mantener lectura de escenarios antiguos con una versión de esquema.
- No inferir automáticamente que BSSID parecidos pertenecen al mismo AP.
- Mantener mapas históricos sin banda como `LEGACY_NO_ESPECIFICADA` hasta decidir su reclasificación.
- Retirar contratos antiguos solo después de migrar móvil, web y reportes.

## 4. Impacto estimado en artefactos vigentes

| Artefacto                         | Cambio posterior a aprobación                                  |
| --------------------------------- | -------------------------------------------------------------- |
| PAPS Online RP5                   | Configuración por radio, bandas y predicción por punto         |
| PB-20                             | Aclarar conjunto de BSSID observados vs inventario físico      |
| PB-07                             | Entradas, acciones y configuración RF completa                 |
| PB-12                             | Comparación por banda y valores proyectados                    |
| PB-08/PB-17                       | Mostrar configuración, supuestos e incertidumbre               |
| Modelo de contexto UC08/UC09      | Flujos para inventario y escenarios completos                  |
| Modelo de datos                   | Nuevas entidades y compatibilidad                              |
| Matriz de trazabilidad            | Restricciones RF adicionales vinculadas a PB-07/PB-12          |

## 5. Riesgos

| Riesgo                                      | Mitigación                                                         |
| ------------------------------------------- | ------------------------------------------------------------------ |
| Datos manuales incompletos                  | Completitud, supuestos explícitos y bloqueo de alta confianza      |
| Potencia no comparable entre fabricantes    | Normalizar dBm/EIRP y conservar referencia original                |
| Sobreajuste del ML                          | Validación espacial y fallback físico                              |
| Tiempo de búsqueda elevado                  | Candidatos acotados, trabajos asíncronos y presupuesto de cómputo  |
| Predicción confundida con garantía          | Incertidumbre y survey de validación obligatorio                   |
| Complejidad excesiva para el técnico        | Formularios progresivos, catálogo y valores por defecto visibles   |

## 6. Decisiones pendientes del Product Owner

| Id     | Decisión                                                                  | Propuesta inicial                                  |
| ------ | ------------------------------------------------------------------------- | -------------------------------------------------- |
| DR-01  | ¿6 GHz forma parte del producto?                                          | No, limitar esta iteración a 2,4 y 5 GHz           |
| DR-02  | Dominio regulatorio inicial                                               | Bolivia, parametrizable y validado antes de código |
| DR-03  | ¿Catálogo cerrado de APs o ingreso libre?                                 | Catálogo aprobado + opción manual con advertencia  |
| DR-04  | Umbral de precisión para escenario de alta confianza                     | MAE ≤ 6 dB en validación espacial                  |
| DR-05  | ¿Capacidad se optimiza en esta iteración o solo se reporta como riesgo?   | Incluir score básico por densidad                  |
| DR-06  | ¿Se permiten antenas externas en el alcance inicial?                      | Sí, mediante catálogo acotado                      |
| DR-07  | ¿El informe proyectado exige siempre survey de validación para cierre?    | Sí, para marcarlo como validado                    |

**Decisión del Product Owner — 20-jun-2026:** se aprueban las propuestas iniciales DR-01..DR-07 para esta iteración.

## 7. Resultado de la revisión

Paquete aprobado por el Product Owner el 20-jun-2026. La implementación mantiene 6 GHz fuera del alcance, usa Bolivia como dominio inicial parametrizable y exige survey posterior para declarar un escenario validado.
