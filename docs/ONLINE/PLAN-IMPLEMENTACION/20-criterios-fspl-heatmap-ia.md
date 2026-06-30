# 20 — Criterios FSPL, Heatmap e IA

**Estado:** Criterio técnico vigente
**Alcance:** PB-05, PB-07, PB-12; RP3 y RP5
**Modalidad:** 100 % en línea

Este documento aclara la relación entre la generación de mapas de calor observados, el predictor RF basado en FSPL/log-distance y el modelo de IA que recomienda posiciones de APs.

## 1. Separación de responsabilidades

El sistema maneja dos tipos de mapas:

| Tipo de mapa | Fuente principal | Algoritmo apropiado | Propósito |
| ------------ | ---------------- | ------------------- | --------- |
| Heatmap observado | Mediciones reales RSSI capturadas por el técnico | IDW oficial único | Interpolar el comportamiento medido entre puntos de lectura |
| Heatmap proyectado | Posiciones/configuraciones propuestas de APs | FSPL/log-distance calibrable por plano | Simular cobertura antes de instalar, mover o reconfigurar APs |

FSPL/log-distance no reemplaza a IDW para el heatmap observado. IDW responde: "con estas muestras reales, ¿cómo estimo los espacios intermedios?". FSPL/log-distance responde: "si ubico un AP en esta coordenada, con esta banda, potencia y restricciones, ¿qué señal esperaría en cada celda?".

## 2. Por qué el heatmap observado usa IDW

El heatmap actual se genera desde mediciones reales en dBm. Esas mediciones ya incluyen efectos combinados de distancia, absorción, multipath, interferencia, orientación del dispositivo, mobiliario y condiciones del entorno. Por ello, el backend debe interpolar la evidencia observada, no reemplazarla por una simulación física.

IDW queda como algoritmo oficial único porque es determinístico, simple de explicar y suficiente cuando la densidad de puntos es aceptable. No se expone Kriging al usuario final para evitar que el mismo conjunto de mediciones produzca mapas visualmente diferentes y genere una lectura engañosa para el cliente.

La ubicación estimada o confirmada de los APs se usa como referencia de visualización y análisis, no como muestra RSSI sintética para interpolar el heatmap observado.

## 3. Por qué la IA usa FSPL/log-distance

La IA debe evaluar escenarios que todavía no existen en campo: agregar APs, moverlos, cambiar potencia, cambiar banda, canal o modelo. En esas posiciones propuestas no hay mediciones reales, por lo que IDW no tiene muestras nuevas para interpolar.

FSPL/log-distance funciona como baseline físico porque modela la pérdida de señal por distancia y frecuencia. La referencia CWNA local sobre Free Space Path Loss y la regla de 6 dB está en `05-antennas-and-accessories.md`, dentro de la carpeta del libro Markdown. Sobre esa base, el sistema puede sumar penalización por banda, potencia/EIRP, ganancia de antena, pérdida de cable y correcciones calibradas localmente.

La fórmula conceptual usada por el predictor es:

```text
RSSI = EIRP + ganancia_receptor
       - perdida_log_distance(frecuencia, distancia, exponente)
       + ajuste_patron_antena
       + correccion_calibrada
```

## 4. Cómo la IA recomienda posiciones de APs

El flujo del optimizador es:

1. Validar que exista un plano calibrado, un conjunto AP técnico fuente, mediciones RSSI y restricciones de negocio.
2. Construir el inventario AP -> radio -> BSSID asociado al conjunto técnico.
3. Calibrar el predictor por banda cuando las mediciones reales lo permiten.
4. Generar posiciones/configuraciones candidatas dentro del área operativa y las restricciones permitidas.
5. Predecir RSSI por radio y celda para cada candidato usando FSPL/log-distance o calibración local.
6. Calcular cobertura, redundancia, CCI/ACI, costo, cantidad de APs y penalizaciones.
7. Aplicar greedy + búsqueda local para mejorar posiciones en una grilla de pasos.
8. Persistir las mejores alternativas como `conjunto_ap` de origen `ia`, sin modificar el conjunto técnico fuente ni las mediciones reales.

El criterio principal de cobertura es maximizar el área objetivo con RSSI suficiente, usando como referencia el umbral de diseño **RSSI ≥ −70 dBm**. También se penalizan exceso de APs, costo alto, potencia sobredimensionada, interferencia y violación de restricciones.

## 5. Criterios para usar calibración local o baseline FSPL/log-distance

El backend usa degradación controlada:

| Condición | Resultado |
| --------- | --------- |
| Hay al menos 3 muestras válidas para una banda concreta | Se calibra modelo local para esa banda |
| Hay menos de 3 muestras válidas para una banda | Esa banda usa baseline FSPL/log-distance |
| No hay ninguna banda calibrable | El modelo completo reporta `baseline_fspl` |
| Hay una o más bandas calibradas | El modelo reporta `calibracion_local_por_plano` para esas bandas |

Una muestra válida de calibración debe cumplir:

- RSSI en rango operativo: mayor a −120 dBm y menor a 0 dBm.
- Distancia positiva entre el punto de medición y el AP físico.
- BSSID medido asociado a una radio/AP físico del mismo plano.
- Radio habilitada.
- BSSID incluido en el conjunto AP técnico usado como fuente de IA.

La calibración se realiza por banda, no globalmente. Por ejemplo, si existen 5 muestras válidas para 5 GHz y solo 2 para 2,4 GHz, el predictor calibra 5 GHz y mantiene baseline FSPL/log-distance para 2,4 GHz.

Cuando se calibra una banda, el sistema ajusta:

- referencia efectiva a 1 m;
- pérdida por duplicar distancia;
- uso de potencia transmitida si hay al menos 3 muestras con potencia conocida;
- pérdida de sistema efectiva;
- MAE del ajuste para registrar la calidad de calibración.

La pérdida por duplicar distancia queda acotada entre 3 dB y 12 dB para evitar resultados físicamente absurdos. La referencia efectiva a 1 m queda acotada entre −90 dBm y −15 dBm.

## 6. Cómo justificar la decisión registrada en la base de datos

Cada conjunto IA guarda en `metricas_ia.calibracion_modelo` el resumen del predictor usado. La lectura operativa es:

- `tipo = baseline_fspl`: el sistema no encontró suficientes muestras válidas para calibrar ninguna banda del conjunto fuente. La recomendación se generó con el comportamiento físico base: 6 dB por duplicar distancia, penalización de banda y parámetros por defecto.
- `tipo = calibracion_local_por_plano`: el sistema encontró al menos una banda con 3 o más muestras válidas. Esa banda usa parámetros ajustados al plano; las bandas no presentes en `bandas` siguen usando baseline.
- `muestras`: cantidad total de lecturas válidas que efectivamente participaron en la calibración.
- `bandas`: detalle por banda calibrada, incluyendo referencia a 1 m, pérdida por duplicar distancia, MAE y si se pudo usar potencia TX.

La decisión no se toma por cantidad total de mediciones del proyecto, sino por la intersección entre: mediciones del plano, BSSID del conjunto técnico fuente, radios/APs físicos vinculados, radios habilitadas y banda concreta. Un proyecto puede tener muchas mediciones, pero si no están asociadas a APs físicos confirmados o no pertenecen al conjunto fuente, no sirven para calibrar el predictor IA.

En la explicación de un heatmap IA debe indicarse:

1. El conjunto IA y su conjunto técnico origen.
2. El tipo de calibración registrado.
3. Las bandas calibradas y cuántas muestras aportaron.
4. Si una banda no aparece en `bandas`, se interpretó con baseline FSPL/log-distance.
5. El motivo técnico: falta o suficiencia de muestras válidas por banda.

## 7. Relación con IDW

IDW y FSPL/log-distance no compiten en el mismo punto del flujo:

- IDW: reconstruye el mapa actual desde lecturas reales.
- FSPL/log-distance: proyecta mapas futuros de APs propuestos.
- Calibración local: ajusta FSPL/log-distance con evidencia real del plano.

Por eso, la explicación correcta no es "usar FSPL en vez de IDW" para todo el proyecto. La regla vigente es: **IDW como algoritmo único para heatmaps observados; FSPL/log-distance calibrable para predicción IA y heatmaps proyectados**.

## 8. Referencias

- [11 — Sprint 4: Heatmap y análisis](11-sprint-4-heatmap-y-analisis.md)
- [12 — Sprint 5: IA y comparación de propuestas](12-sprint-5-ia-comparacion-y-reportes.md)
- [17.04 — Motor predictivo y optimizador](17-especificacion-optimizacion-rf/04-motor-predictivo-y-optimizador.md)
- [18 — Reglas de Gobierno para Conjuntos de APs, Heatmaps e IA](18-reglas-gobernanza-conjuntos-ap-heatmaps.md)
- [CWNA Markdown — Índice](../../Certified%20Wireless%20Network%20Administrator%20-%20Official%20Study%20Guide%20Markdown/index.md)
- [CWNA Markdown — 02 RF Fundamentals](../../Certified%20Wireless%20Network%20Administrator%20-%20Official%20Study%20Guide%20Markdown/02-rf-fundamentals.md): dB, dBm, ganancia, pérdida y EIRP.
- [CWNA Markdown — 03 Spread Spectrum Technology](../../Certified%20Wireless%20Network%20Administrator%20-%20Official%20Study%20Guide%20Markdown/03-spread-spectrum-technology.md): canales 2,4 GHz, solapamiento y separación 1/6/11.
- [CWNA Markdown — 05 Antennas and Accessories](../../Certified%20Wireless%20Network%20Administrator%20-%20Official%20Study%20Guide%20Markdown/05-antennas-and-accessories.md): FSPL y regla de 6 dB.
- [CWNA Markdown — 11 Site Survey Fundamentals](../../Certified%20Wireless%20Network%20Administrator%20-%20Official%20Study%20Guide%20Markdown/11-site-survey-fundamentals.md): metodología de site survey, mediciones de señal en dBm, dead spots, cobertura e interferencias.

> Nota documental: el límite Android de 4 escaneos cada 2 minutos desde Android 8.0 es una restricción de plataforma usada por la app móvil, no una regla CWNA.
