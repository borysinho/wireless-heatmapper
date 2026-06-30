# 20 — Criterios FSPL, Heatmap e IA

**Estado:** Criterio técnico vigente
**Alcance:** PB-05, PB-07, PB-12; RP3 y RP5
**Modalidad:** 100 % en línea

Este documento aclara la relación entre la generación de mapas de calor observados, el predictor RF basado en FSPL/log-distance y el módulo IA que recomienda conjuntos AP derivados. La implementación vigente persiste todos los `mapa_calor` con `algoritmo = IDW`; FSPL/log-distance se usa como predictor interno para estimar RSSI de propuestas IA antes de interpolarlas.

## 1. Separación de responsabilidades

El sistema separa tres responsabilidades:

| Responsabilidad | Fuente principal | Algoritmo / modelo implementado | Propósito |
| --------------- | ---------------- | ------------------------------- | --------- |
| Heatmap observado persistido | Mediciones reales RSSI capturadas por el técnico (`lectura_rssi.origen = CAMPO`) | IDW oficial único | Interpolar el comportamiento medido entre puntos de lectura |
| Evaluación IA interna | Posiciones/configuraciones candidatas de APs | FSPL/log-distance con calibración local y corrección espacial por plano | Estimar cobertura futura y puntuar alternativas antes de persistirlas |
| Heatmap proyectado persistido | Lecturas RSSI estimadas por IA (`lectura_rssi.origen = IA_ESTIMADA`) | IDW oficial único | Renderizar la propuesta IA con el mismo formato operativo de mapas |

FSPL/log-distance no reemplaza a IDW para los mapas persistidos. IDW responde: "con estas muestras reales o estimadas, ¿cómo estimo los espacios intermedios?". FSPL/log-distance responde: "si ubico un AP en esta coordenada, con esta banda, potencia y restricciones, ¿qué señal esperaría antes de materializar la propuesta?".

## 2. Por qué el heatmap observado usa IDW

El heatmap actual se genera desde mediciones reales en dBm. Esas mediciones ya incluyen efectos combinados de distancia, absorción, multipath, interferencia, orientación del dispositivo, mobiliario y condiciones del entorno. Por ello, el backend debe interpolar la evidencia observada, no reemplazarla por una simulación física.

IDW queda como algoritmo oficial único porque es determinístico, simple de explicar y suficiente cuando la densidad de puntos es aceptable. No se expone Kriging al usuario final para evitar que el mismo conjunto de mediciones produzca mapas visualmente diferentes y genere una lectura engañosa para el cliente.

La ubicación estimada o confirmada de los APs se usa como referencia de visualización y análisis, no como muestra RSSI sintética para interpolar el heatmap observado.

La escala visual operativa del heatmap debe coincidir con la escala usada durante la captura móvil: `Óptimo` desde −70 dBm, `Aceptable` desde −80 dBm, `Pobre` desde −85 dBm, `Muy pobre` desde −90 dBm y `Zona muerta` por debajo de −90 dBm. Esta decisión evita que una misma lectura real sea verde en captura pero amarilla o naranja al renderizar el mapa.

La paleta usada para esos rangos sigue la convención visual observada en Ekahau para mapas de intensidad de señal: negro/gris para señal muy baja, amarillo en rangos de transición y verde/lima para señal suficiente o fuerte. El negro se reserva exclusivamente para `Zona muerta`, porque representa RSSI menor a −90 dBm o no detección del AP seleccionado.

IDW conserva la lectura directa cuando la celda coincide con una medición real, pero aplica soporte local conservador en celdas intermedias: si una celda queda por encima de un umbral operativo por influencia de un único punto fuerte y los vecinos cercanos no respaldan ese nivel, el valor se degrada al rango inferior inmediato. Esto reduce manchas verdes o amarillas aisladas que no tienen soporte suficiente en las mediciones del entorno, sin ocultar puntos reales buenos capturados por el técnico.

## 3. Por qué la IA usa FSPL/log-distance

La IA debe evaluar escenarios que todavía no existen en campo: agregar APs, moverlos, cambiar potencia, cambiar banda, canal o modelo. En esas posiciones propuestas no hay mediciones reales, por lo que primero necesita un predictor RF para generar valores RSSI estimados.

FSPL/log-distance funciona como baseline físico porque modela la pérdida de señal por distancia y frecuencia. La referencia CWNA local sobre Free Space Path Loss y la regla de 6 dB está en `05-antennas-and-accessories.md`, dentro de la carpeta del libro Markdown. Sobre esa base, el sistema suma penalización por banda, potencia/EIRP cuando existe configuración de radio recomendada, ganancia de antena, pérdida de cable y correcciones calibradas localmente.

La fórmula conceptual usada por el predictor es:

```text
RSSI = EIRP + ganancia_receptor
       - perdida_log_distance(frecuencia, distancia, exponente)
       + ajuste_patron_antena
       + correccion_calibrada
       + correccion_espacial_calibrada(x,y)
```

La `correccion_espacial_calibrada(x,y)` no modela muros, puertas ni materiales. Es un ajuste empírico derivado de los residuos de mediciones reales del mismo plano: diferencia entre el RSSI real observado y el RSSI que el modelo distancia/banda habría predicho en esa misma coordenada.

## 4. Cómo la IA recomienda posiciones de APs

El flujo del optimizador es:

1. Validar que exista un plano calibrado, polígono de interés, conjunto AP técnico fuente, mediciones RSSI y restricciones de negocio.
2. Leer el conjunto técnico fuente (`conjunto_ap`) y sus items (`conjunto_ap_item`) con snapshots de BSSID, banda, canal, posición y radios opcionales en JSON. Ya no existe inventario físico `ap_fisico` / `radio_ap` / `bssid_radio`.
3. Generar o recuperar el mapa actual del conjunto técnico con IDW sobre lecturas `CAMPO`.
4. Calibrar el predictor por banda cuando las mediciones reales y las posiciones de los items del conjunto lo permiten; luego construir una corrección espacial por residuos cuando hay suficientes muestras por banda.
5. Generar posiciones/configuraciones candidatas dentro del polígono de interés, combinando puntos críticos de señal y grilla del plano.
6. Predecir RSSI por celda para cada candidato usando FSPL/log-distance, calibración local y corrección espacial cuando aplica, y calcular cobertura con umbral objetivo.
7. Aplicar greedy + búsqueda local para mejorar posiciones en una grilla de pasos.
8. Persistir las mejores alternativas como `conjunto_ap` de origen `ia`, sin modificar el conjunto técnico fuente ni las mediciones reales.
9. Materializar lecturas estimadas en `lectura_rssi` con `origen = IA_ESTIMADA`, `conjunto_ap_id` del conjunto IA, `modelo_origen = rf-hibrido-1.2` e `incertidumbre_db = 6.0`.
10. Generar el heatmap proyectado persistido con IDW sobre esas lecturas estimadas y asociarlo al conjunto IA.

El criterio principal de cobertura es maximizar el área objetivo con RSSI suficiente, usando como referencia el umbral de diseño **RSSI ≥ −70 dBm**. La implementación actual calcula cobertura proyectada, mejora porcentual, cantidad de APs evaluada, zonas muertas proyectadas y cobertura por banda; deja CCI/ACI, costo real y restricciones de potencia avanzada como metadatos/supuestos o extensión posterior.

## 5. Criterios para usar calibración local o baseline FSPL/log-distance

El backend usa degradación controlada:

| Condición | Resultado |
| --------- | --------- |
| Hay al menos 3 muestras válidas para una banda concreta | Se calibra modelo local para esa banda |
| Hay menos de 3 muestras válidas para una banda | Esa banda usa baseline FSPL/log-distance |
| No hay ninguna banda calibrable | El modelo completo reporta `baseline_fspl` |
| Hay una o más bandas calibradas, pero sin residuos espaciales suficientes | El modelo reporta `calibracion_local_por_plano` para esas bandas |
| Hay al menos 3 residuos espaciales válidos para una banda | El modelo reporta `calibracion_espacial_por_plano` y aplica corrección por coordenada en esa banda |

Una muestra válida de calibración debe cumplir:

- RSSI en rango operativo: mayor a −120 dBm y menor a 0 dBm.
- Distancia positiva entre el punto de medición y la posición del item del conjunto AP.
- BSSID medido incluido en el conjunto AP técnico usado como fuente de IA.
- Item del conjunto con `pos_x` y `pos_y` definidos.
- Banda tomada de `conjunto_ap_item.banda` o inferida desde frecuencia/canal de la lectura.
- Plano con escala (`escala_m_por_px`) para convertir píxeles a metros.

La calibración se realiza por banda, no globalmente. Por ejemplo, si existen 5 muestras válidas para 5 GHz y solo 2 para 2,4 GHz, el predictor calibra 5 GHz y mantiene baseline FSPL/log-distance para 2,4 GHz. La corrección espacial sigue la misma regla por banda: no mezcla residuos de 2,4 GHz con predicciones de 5 GHz.

Cuando se calibra una banda, el sistema ajusta:

- referencia efectiva a 1 m;
- pérdida por duplicar distancia;
- pérdida de sistema efectiva;
- MAE del ajuste para registrar la calidad de calibración.

El modelo soporta uso de potencia transmitida si recibe al menos 3 muestras con potencia conocida. En el flujo vigente de calibración desde mediciones de campo no se pasa potencia TX, por lo que `usa_potencia_tx` queda normalmente en `false`. En ese caso, las predicciones IA conservan la referencia local aprendida del plano y no reemplazan la calibración por un baseline EIRP genérico; la potencia de las radios recomendadas solo ajusta la referencia cuando la banda no tiene calibración local o cuando la calibración sí incluyó potencia TX.

La app móvil no mide TX Power real desde Android durante el survey. Cuando el técnico conoce la configuración del AP, puede registrar `potencia_tx_dbm` como dato declarado del conjunto AP. Ese dato se guarda en `conjunto_ap_item.radios` junto con `fuente_potencia` y `confianza_potencia`. La IA solo usa esa potencia para calibración si la fuente es `manual` o `controlador` y la confianza es `media` o `alta`; valores `estimada`, `desconocida` o de confianza `baja` quedan como trazabilidad, pero no reemplazan la evidencia RSSI de campo.

La pérdida por duplicar distancia queda acotada entre 3 dB y 12 dB para evitar resultados físicamente absurdos. La referencia efectiva a 1 m queda acotada entre −90 dBm y −15 dBm.

### 5.1 Calibración espacial más fuerte implementada

La calibración espacial más fuerte agrega una segunda capa sobre la calibración distancia/banda:

1. El backend calibra primero el modelo log-distance con las lecturas reales válidas.
2. Para cada lectura válida calcula el residual: `RSSI_real - RSSI_predicho_sin_correccion_espacial`.
3. Cada residual se guarda en memoria de la corrida con su coordenada `(x,y)` del punto de medición y su banda.
4. Los residuos se acotan entre −18 dB y +12 dB para evitar que una medición atípica domine toda la proyección.
5. Si una banda tiene al menos 3 residuos, el predictor interpola una corrección por IDW espacial interno al momento de estimar cada celda o punto.
6. Si la predicción no recibe coordenadas, o la banda no tiene 3 residuos, la corrección espacial es 0 dB y el modelo vuelve a la calibración local/baseline.

Este mecanismo usa únicamente datos ya existentes: `lectura_rssi`, `punto_medicion`, escala del plano y posiciones `pos_x`/`pos_y` de `conjunto_ap_item`. No requiere geometría de muros, materiales ni cambios en el modelo de base de datos.

## 6. Cómo justificar la decisión registrada en la base de datos

Cada conjunto IA guarda en `metricas_ia.calibracion_modelo` el resumen del predictor usado. La lectura operativa es:

- `tipo = baseline_fspl`: el sistema no encontró suficientes muestras válidas para calibrar ninguna banda del conjunto fuente. La recomendación se generó con el comportamiento físico base: 6 dB por duplicar distancia, penalización de banda y parámetros por defecto.
- `tipo = calibracion_local_por_plano`: el sistema encontró al menos una banda con 3 o más muestras válidas. Esa banda usa parámetros ajustados al plano; las bandas no presentes en `bandas` siguen usando baseline.
- `tipo = calibracion_espacial_por_plano`: además de la calibración local, el sistema encontró al menos una banda con 3 o más residuos espaciales válidos y aplica corrección por coordenada al optimizar y materializar lecturas IA.
- `muestras`: cantidad total de lecturas válidas que efectivamente participaron en la calibración.
- `bandas`: detalle por banda calibrada, incluyendo referencia a 1 m, pérdida por duplicar distancia, MAE y si se pudo usar potencia TX.
- `correccion_espacial`: detalle por banda con cantidad de residuos, corrección promedio, mínima y máxima aplicada como campo residual.

Además, el conjunto IA guarda métricas de cobertura (`pct_cobertura_actual`, `pct_cobertura_proyectada`, `mejora_pct`, `zonas_muertas_proyectadas`, `pct_cobertura_por_banda`), supuestos, confianza, `mapas_por_banda` y lecturas estimadas/simuladas. La fuente canónica para renderizar mapas proyectados es `lectura_rssi` con `origen = IA_ESTIMADA`; las copias en `metricas_ia` son trazabilidad de la corrida IA.

La decisión no se toma por cantidad total de mediciones del proyecto, sino por la intersección entre: mediciones del plano, BSSID del conjunto técnico fuente, items del conjunto con posición conocida y banda concreta. Un proyecto puede tener muchas mediciones, pero si no pertenecen al conjunto fuente o no tienen posición de AP en `conjunto_ap_item`, no sirven para calibrar el predictor IA.

En la explicación de un heatmap IA debe indicarse:

1. El conjunto IA y su conjunto técnico origen.
2. El tipo de calibración registrado.
3. Las bandas calibradas y cuántas muestras aportaron.
4. Si una banda no aparece en `bandas`, se interpretó con baseline FSPL/log-distance.
5. Si existe `correccion_espacial`, cuántos residuos por banda se usaron y si el ajuste fue positivo o negativo en promedio.
6. El motivo técnico: falta o suficiencia de muestras válidas por banda.

## 7. Relación con IDW

IDW y FSPL/log-distance no compiten en el mismo punto del flujo:

- IDW: reconstruye mapas persistidos desde lecturas reales (`CAMPO`) o estimadas (`IA_ESTIMADA`).
- FSPL/log-distance: estima RSSI futuro de APs propuestos y alimenta las lecturas IA.
- Calibración local: ajusta FSPL/log-distance con evidencia real del plano.
- Corrección espacial: ajusta la predicción por coordenada usando residuos reales del plano, sin modelar muros/materiales.

Por eso, la explicación correcta no es "usar FSPL en vez de IDW" para todo el proyecto. La regla vigente implementada es: **IDW como algoritmo único para `mapa_calor`; FSPL/log-distance calibrable como predictor IA para generar lecturas estimadas y evaluar propuestas**.

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
