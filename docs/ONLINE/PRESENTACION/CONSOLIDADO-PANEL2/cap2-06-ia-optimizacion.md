## Inteligencia Artificial para la Optimización del Posicionamiento de Puntos de Acceso

### Formulación del problema

El problema de determinar el número mínimo de puntos de acceso y sus posiciones óptimas en un edificio para garantizar cobertura uniforme ≥ −70 dBm puede formularse como un **problema de optimización combinatoria**: dado el espacio de posiciones candidatas sobre el plano (discretizado en celdas), y dado un modelo de propagación RF que predice el RSSI en cualquier punto del plano desde cualquier posición de AP, encontrar el subconjunto mínimo de posiciones candidatas tal que todo punto habitable del plano tenga al menos un AP con RSSI ≥ −70 dBm.

Este problema es NP-difícil en su formulación general (Sherali & Pendyala, 1992), ya que el número de combinaciones crece exponencialmente con el número de celdas candidatas. En la práctica, se abordan tres categorías de enfoques:

1. **Métodos heurísticos:** algoritmos voracos (_greedy_) que colocan APs secuencialmente en la posición que maximice la cobertura incremental. Rápidos pero no garantizan la solución óptima global.
2. **Metaheurísticas:** algoritmos genéticos, enjambre de partículas (PSO) y recocido simulado (SA) que exploran el espacio de soluciones de forma estocástica. Mejor calidad que los métodos voraces, con mayor costo computacional.
3. **Aprendizaje automático:** modelos que aprenden la relación entre la posición de un AP, el mapa de atenuación del edificio y el campo de cobertura resultante, y que generalizan para nuevas plantas sin necesidad de simular explícitamente la propagación.

### Modelo de predicción de RSSI basado en aprendizaje supervisado

El módulo de IA del Wireless HeatMapper (RP5) adopta un enfoque de **aprendizaje supervisado** para la predicción del campo de RSSI. La idea central es entrenar un modelo que, dado:

- Las coordenadas $(x_{AP}, y_{AP})$ de un AP candidato sobre el plano,
- Las coordenadas $(x, y)$ de un punto de evaluación,
- Un vector de características del entorno en el camino entre AP y punto (materiales de los muros atravesados, distancia real, distancia en línea recta),

prediga el valor de RSSI esperado en el punto de evaluación.

El **conjunto de datos de entrenamiento** se compone de:

- Mediciones reales acumuladas en proyectos anteriores persistidos en la base de datos del Wireless HeatMapper (aprendizaje sobre datos reales del cliente).
- Datasets sintéticos generados por simulación de propagación RF con un modelo de _log-distance path loss_ con factores de atenuación por material:

$$RSSI(d) = RSSI_0 - 10 \cdot n \cdot \log_{10}(d) - \sum_{j} L_j$$

donde $RSSI_0$ es el RSSI de referencia a 1 m, $n$ es el exponente de path loss (típicamente entre 2.5 y 4.5 en entornos interiores), $d$ es la distancia al AP y $L_j$ es la atenuación introducida por el $j$-ésimo muro en el trayecto.

### Arquitectura del modelo

El modelo implementado en scikit-learn es un **regresor de bosque aleatorio** (Random Forest Regressor) por las siguientes razones:

- **Robustez ante valores atípicos:** el RSSI medido en campo puede tener outliers por interferencias momentáneas; el bosque aleatorio es menos sensible que los modelos lineales.
- **Capacidad de capturar relaciones no lineales:** la propagación RF en interiores es altamente no lineal; el bosque aleatorio aproxima bien funciones complejas sin suposiciones sobre la forma de la distribución.
- **Interpretabilidad:** es posible extraer la importancia relativa de cada característica (distancia, número de muros, tipo de material), lo que facilita la validación del modelo por parte de ingenieros de redes.
- **Bajo costo de inferencia:** la predicción de un campo completo de RSSI (grilla de 100 × 100 puntos) tarda milisegundos en el backend Python, compatible con la experiencia interactiva esperada por el usuario.

La optimización del posicionamiento de APs se realiza mediante un **algoritmo de búsqueda voraz** guiado por el modelo: en cada iteración, se evalúa en qué posición candidata la adición de un nuevo AP maximiza la cobertura incremental (porcentaje del área que pasa de RSSI < −70 dBm a RSSI ≥ −70 dBm). El proceso continúa hasta que toda el área habitable alcanza el objetivo de cobertura o hasta alcanzar un número máximo de APs configurado por el usuario.

### Validación del módulo de IA

La validación del módulo de IA se realiza mediante:

1. **Validación cruzada k-fold** sobre el conjunto de datos de entrenamiento para medir el error medio absoluto (MAE) en dBm.
2. **Pruebas de campo:** en instalaciones reales de Bulldog Tech., el técnico puede comparar el heatmap proyectado (generado por la IA antes del despliegue de los APs adicionales) con el heatmap real medido tras la instalación.
3. **Métrica de cobertura:** porcentaje del área del plano con RSSI ≥ −70 dBm antes y después de aplicar el plan de APs recomendado por la IA.

La combinación de aprendizaje supervisado para la predicción de RSSI y búsqueda voraz para la colocación de APs convierte el módulo RP5 en una herramienta práctica que, a diferencia de las soluciones comerciales de diseño predictivo, se retroalimenta con los datos reales de cada nuevo proyecto completado en la plataforma.
