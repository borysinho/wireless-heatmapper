## 3.8 scikit-learn y TensorFlow para el Módulo de Inteligencia Artificial

### 3.8.1 Selección del framework de machine learning

El módulo de IA del Wireless HeatMapper (RP5) requiere:

1. **Entrenamiento offline** de modelos de regresión con datasets de propagación RF (sintéticos y reales acumulados de proyectos anteriores).
2. **Inferencia en línea** (en tiempo de respuesta HTTP) para predecir el campo de RSSI dado un mapa del edificio y una posición de AP candidata.
3. **Despliegue ligero** dentro del contenedor Docker del backend, sin necesidad de hardware GPU dedicado en el servidor de producción.

Con estos criterios, se seleccionaron dos frameworks complementarios:

- **scikit-learn** para el modelo de predicción de RSSI (Random Forest Regressor) y para las etapas de preprocesamiento y evaluación.
- **TensorFlow Lite / ONNX Runtime** como alternativa para modelos más complejos (redes neuronales) en despliegue de producción con bajo overhead de memoria.

### 3.8.2 scikit-learn — Regresión con Bosque Aleatorio

**scikit-learn** es la librería de machine learning más utilizada en Python para modelos de aprendizaje supervisado y no supervisado clásicos (Pedregosa et al., 2011). Se implementa íntegramente en Python y NumPy, con componentes críticos en Cython/C++ para rendimiento. Su interfaz estandarizada (`fit`, `predict`, `score`) facilita la experimentación y el reemplazo de modelos sin cambiar el código de integración.

El **Random Forest Regressor** implementado en scikit-learn es un conjunto (_ensemble_) de $T$ árboles de decisión entrenados con subconjuntos aleatorios del conjunto de entrenamiento (bagging) y subconjuntos aleatorios de características en cada nodo de cada árbol. La predicción final es el promedio de las predicciones de todos los árboles:

$$\hat{z}_{RF}(x) = \frac{1}{T} \sum_{t=1}^{T} f_t(x)$$

Esta agregación reduce la varianza del modelo individual (propenso a sobreajuste) manteniendo bajo el sesgo, lo que lo hace especialmente adecuado para regresión sobre datos ruidosos como las mediciones de RSSI de campo.

El pipeline de scikit-learn para el Wireless HeatMapper incluye:

```
Datos brutos
    ↓ StandardScaler (normalización de coordenadas y distancias)
    ↓ RandomForestRegressor (n_estimators=200, max_depth=20)
    ↓ Predicción de RSSI en grilla del plano
    ↓ Algoritmo voraz de colocación de APs
    ↓ Heatmap proyectado del escenario optimizado
```

### 3.8.3 Persistencia del modelo con joblib

Los modelos entrenados se serializan con **joblib** (incluido en scikit-learn) a un archivo `.pkl` que se almacena en el sistema de archivos del contenedor. El backend FastAPI carga el modelo al iniciar y lo mantiene en memoria para responder peticiones de inferencia sin releer el disco en cada request.

### 3.8.4 Evaluación y métricas del modelo

El rendimiento del modelo de predicción de RSSI se evalúa con las siguientes métricas estándar de regresión:

| Métrica                           | Descripción                                     | Meta del proyecto |
| --------------------------------- | ----------------------------------------------- | ----------------- |
| MAE (Mean Absolute Error)         | Error medio en dBm entre RSSI predicho y medido | ≤ 5 dBm           |
| RMSE (Root Mean Square Error)     | Penaliza más los errores grandes                | ≤ 8 dBm           |
| R² (coeficiente de determinación) | Proporción de varianza explicada por el modelo  | ≥ 0.80            |

La validación se realiza con k-fold cross-validation (k=5) para garantizar que las métricas reportadas generalizan a datos no vistos durante el entrenamiento.

### 3.8.5 Integración con el backend FastAPI

El módulo de IA se integra en el backend como un servicio Python (`ai/service.py`) que expone dos funciones:

- `generar_heatmap_proyectado(plano_id, posiciones_ap_propuestas) → bytes`: devuelve la imagen PNG del heatmap proyectado.
- `sugerir_posiciones_ap(plano_id, objetivo_rssi=-70) → List[Posicion]`: ejecuta el algoritmo voraz y devuelve la lista de posiciones candidatas recomendadas.

Estas funciones son invocadas por los endpoints REST correspondientes (`POST /api/proyectos/{id}/analisis/ia`) y sus resultados se persisten en PostgreSQL para ser consultados posteriormente desde el portal de cliente sin necesidad de re-ejecutar el modelo.
