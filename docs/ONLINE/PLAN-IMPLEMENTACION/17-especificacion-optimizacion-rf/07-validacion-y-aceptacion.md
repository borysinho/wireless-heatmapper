# 07 — Validación y Criterios de Aceptación

## 1. Estrategia de validación

La validación se realiza en cuatro niveles:

1. fórmulas y reglas RF;
2. calidad predictiva con separación espacial;
3. factibilidad de la optimización;
4. survey real posterior a la instalación.

## 2. Pruebas unitarias RF

- conversión mW ↔ dBm;
- cálculo IR/EIRP con ganancia y pérdidas;
- FSPL y regla de 6 dB al duplicar distancia;
- mayor pérdida de 5 GHz respecto de 2,4 GHz a igual distancia;
- atenuación acumulada de obstáculos;
- patrón de antena y orientación;
- validación de canales/ancho/DFS por región;
- detección CCI/ACI por banda;
- respeto de niveles discretos de potencia del equipo.

## 3. Datasets sintéticos de regresión

| Dataset                     | Resultado esperado                                                        |
| --------------------------- | ------------------------------------------------------------------------- |
| Espacio abierto             | Simetría para omni y decaimiento logarítmico                              |
| Edificio en U               | APs en extremos o solución equivalente factible                           |
| Pasillo largo               | Ventaja de antena direccional correctamente orientada                     |
| Dos pisos                   | Atenuación entre plantas y canales escalonados                            |
| Alta densidad               | Más radios/celdas pequeñas, sin resolver todo con potencia máxima         |
| AP fijo mal ubicado         | Mantener coordenada y proponer reconfiguración/adición                    |
| BSSID dual-band vinculados  | Una posición física con dos configuraciones de radio                      |

## 4. Calidad predictiva

La evaluación usa partición espacial, no muestras aleatorias vecinas. Se reporta por banda:

- MAE y RMSE en dB;
- error percentil 95;
- sesgo medio;
- cobertura del intervalo de incertidumbre;
- comparación baseline físico vs físico + ML.

Meta inicial propuesta para revisión: MAE ≤ 6 dB en puntos de validación del mismo sitio. Si no se cumple, el sistema puede mostrar escenarios exploratorios, pero no declararlos de alta confianza.

## 5. Criterios de aceptación funcionales

### CA-RF-01 — Inventario

Un AP dual-band puede contener radios separadas y varios BSSID sin duplicar el equipo físico.

### CA-RF-02 — Inmutabilidad

Generar, regenerar o eliminar un escenario no modifica `MedicionWifi` ni su instantánea de captura.

### CA-RF-03 — Configuración completa

Cada AP recomendado presenta posición, altura, modelo/montaje y configuración de sus radios habilitadas.

### CA-RF-04 — Separación por banda

Cada alternativa genera mapas y métricas independientes de 2,4 y 5 GHz.

### CA-RF-05 — Combinación explícita

El mapa combinado declara política y nunca se confunde con un mapa de banda.

### CA-RF-06 — Puntos proyectados

Cada punto original devuelve RSSI proyectado, delta cuando exista baseline, radios primaria/secundaria e incertidumbre.

### CA-RF-07 — Restricciones

No se mueve un AP fijo ni se recomienda potencia/canal/ancho fuera de las capacidades o regulación configuradas.

### CA-RF-08 — Escenario nuevo

Los APs temporales calibran el modelo, pero no se convierten automáticamente en APs definitivos.

### CA-RF-09 — Escenario existente

Cada propuesta identifica claramente qué se mantiene, mueve, reconfigura, retira o agrega.

### CA-RF-10 — Fallback

Si ML no mejora el baseline físico, el motor utiliza el baseline y registra la decisión.

## 6. Pruebas de contrato e integración

- autorización y pertenencia del proyecto en todos los endpoints;
- idempotencia de validación y reproducción con la misma versión/semilla;
- conflicto si cambia el baseline durante el cálculo;
- serialización de matrices y puntos por banda;
- compatibilidad temporal con mapas y recomendaciones vigentes;
- reporte PDF con configuración por radio, supuestos e incertidumbre.

## 7. Validación posterior a la instalación

El plan recomendado no se considera confirmado hasta ejecutar un survey de validación:

1. instalar/configurar según escenario aprobado;
2. medir sistemáticamente las mismas áreas;
3. comparar proyectado vs observado por banda;
4. validar cobertura, SNR, roaming y capacidad aplicable;
5. registrar desviaciones y recalibrar el modelo.

El reporte final diferencia “diseño proyectado” de “resultado validado”.

