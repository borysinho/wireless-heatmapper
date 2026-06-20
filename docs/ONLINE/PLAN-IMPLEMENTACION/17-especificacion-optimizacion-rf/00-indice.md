# 17 — Especificación de Optimización RF por Escenarios

**Estado:** Aprobada para implementación por el Product Owner — 20-jun-2026

**Alcance:** Refinamiento de RP5, PB-07 y PB-12

**Modalidad:** 100 % en línea

Este paquete define cómo evolucionar el módulo de recomendación para que produzca un **plan RF completo**, no solamente coordenadas de APs. La propuesta distingue AP físico, radio y BSSID; contempla instalaciones nuevas y redes existentes; optimiza 2,4 GHz y 5 GHz; y conserva por separado las mediciones reales y las predicciones.

Esta especificación complementa el alcance de Sprint 5 y es la referencia técnica vigente para la evolución de PB-07/PB-12. Los documentos normativos enlazan este paquete para evitar duplicar sus contratos y reglas detalladas.

## Documentos

| #  | Documento                                                        | Propósito                                                                      |
| -- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 01 | [Alcance y reglas de negocio](01-alcance-y-reglas-de-negocio.md) | Escenarios, conceptos, reglas y criterios funcionales                          |
| 02 | [Modelo de dominio y datos](02-modelo-de-dominio-y-datos.md)     | Entidades, relaciones, invariantes y migración conceptual                      |
| 03 | [Entradas y captura](03-entradas-y-captura.md)                   | Datos por AP/radio, ambiente, restricciones y procedencia                      |
| 04 | [Motor predictivo y optimizador](04-motor-predictivo-y-optimizador.md) | Arquitectura híbrida RF + ML + optimización y tratamiento por banda       |
| 05 | [Contratos API y salidas](05-contratos-api-y-salidas.md)         | Endpoints, payloads conceptuales, mapas y valores proyectados                  |
| 06 | [Flujos de experiencia de usuario](06-flujos-de-usuario.md)      | Captura guiada, inventario, generación y comparación de escenarios            |
| 07 | [Validación y criterios de aceptación](07-validacion-y-aceptacion.md) | Pruebas, métricas, incertidumbre y validación posterior a la instalación  |
| 08 | [Plan de implementación y decisiones](08-plan-de-implementacion.md) | Orden de trabajo, impacto documental y decisiones pendientes              |

## Decisiones rectoras

1. Una `MedicionWifi` es evidencia observada y no se modifica al generar una recomendación.
2. Un AP físico contiene una o más radios; una radio puede anunciar uno o más BSSID.
3. La potencia se normaliza a dBm y EIRP, conservando el valor original ingresado.
4. Cada escenario genera resultados separados para 2,4 GHz y 5 GHz.
5. Un mapa combinado solo es válido si declara la política de selección de banda.
6. El resultado incluye configuración por radio y valores proyectados en cada punto original y en una grilla continua.
7. La predicción es una estimación con incertidumbre; debe validarse mediante un survey posterior a la instalación.

## Referencias vigentes

- [PAPS Online](../../Wireless%20Heatmapper%20-%20PAPS%20-%20Modalidad%20Online.md)
- [Modelo de datos vigente](../04-modelo-datos.md)
- [Sprint 4 — Heatmap y análisis](../11-sprint-4-heatmap-y-analisis.md)
- [Sprint 5 — IA, comparación y reportes](../12-sprint-5-ia-comparacion-y-reportes.md)
- [Referencias CWNA-107](../../../cwna-referencia-proyecto/00-indice.md)
