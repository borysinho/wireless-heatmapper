## 3.5 Inteligencia Artificial Aplicada al Análisis de Cobertura WiFi

El análisis automatizado de cobertura puede formularse como un problema de clasificación espacial y de generación de recomendaciones sobre una superficie medida parcialmente. Cada punto capturado entrega una observación discreta de RSSI, canal y frecuencia. A partir de ese conjunto, el sistema debe estimar el comportamiento del espacio completo, identificar patrones anómalos y proponer acciones con sentido técnico. No se trata de una inteligencia artificial genérica, sino de un motor analítico acotado al dominio de propagación y validación WiFi.

El método de interpolación previsto es *Inverse Distance Weighting* (IDW, ponderación por distancia inversa). Su lógica asigna a cada celda de la grilla un valor calculado a partir de mediciones vecinas ponderadas por la distancia elevada a una potencia `p`. Cuando `p` aumenta, las muestras cercanas dominan con más fuerza el resultado. Esta técnica es apropiada para el proyecto porque ofrece una relación favorable entre costo computacional, interpretabilidad y capacidad de ejecución en backend sobre planos de tamaño moderado.

Sobre la superficie interpolada opera una clasificación por umbrales basada en CWNA-107. Cada celda o punto puede etiquetarse como EXCELENTE, BUENA, ACEPTABLE, DEBIL o ZONA_MUERTA según el rango de dBm observado o estimado. Esta clasificación convierte un valor continuo en una señal de decisión utilizable por el técnico y por los módulos de visualización del sistema.

El análisis de interferencias requiere una segunda capa de reglas. Cuando varias muestras del mismo punto revelan APs en el mismo canal con RSSI alto, existe evidencia para investigar solapamiento co-canal. Si la distribución de canales vecinos en 2.4 GHz es inadecuada, también puede inferirse riesgo de interferencia adyacente. Sobre esos hallazgos se construye un árbol de decisiones simple: zonas muertas sugieren incorporación o reubicación de AP; CCI persistente sugiere ajuste de canal; señal marginal en áreas extensas sugiere revisar potencia, densidad o ubicación.

La comparación de escenarios amplía el módulo analítico. Dos matrices de cobertura obtenidas sobre el mismo plano pueden restarse para detectar mejora o deterioro por región. Con ello, el sistema no solo evalúa un levantamiento aislado, sino el efecto de una optimización entre dos estados del despliegue.

En el proyecto, esta fundamentación sostiene el módulo analítico del backend previsto para los Sprint 4 y 5, donde la cobertura deja de ser un dato descriptivo y pasa a convertirse en una interpretación operativa del comportamiento WiFi del edificio.

### Referencias

Li, Y., Ai, B., He, R., Yang, Z., & Zhong, Z. (2020). Machine learning based wireless channel modeling: Challenges and opportunities. *IEEE Communications Magazine, 58*(3), 112–118. https://doi.org/10.1109/MCOM.001.1900487

Shepard, D. (1968). A two-dimensional interpolation function for irregularly-spaced data. *Proceedings of the 1968 ACM National Conference*, 517–524. https://doi.org/10.1145/800186.810616

---
