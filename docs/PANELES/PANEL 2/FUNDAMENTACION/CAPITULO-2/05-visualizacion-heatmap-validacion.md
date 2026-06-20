## 2.4 Visualización de Datos RF mediante Mapas de Calor y Validación de Cobertura

Un *heatmap* (mapa de calor) representa una superficie continua de intensidad derivada de un conjunto discreto de muestras. En el contexto de radiofrecuencia, cada medición de señal se asocia a una posición sobre el plano y luego se interpola para estimar valores en áreas no muestreadas de manera puntual. El resultado no sustituye la observación original; la amplifica espacialmente para facilitar la lectura de patrones, transiciones y vacíos de cobertura.

La convención cromática cumple una función semántica. Verde suele indicar cobertura excelente, amarillo una condición buena o aceptable, naranja una degradación ya perceptible, rojo una señal débil y negro o gris una zona muerta. En redes WiFi empresariales, estos rangos se interpretan a partir de umbrales como los descritos en la Tabla 13.1 del CWNA-107. Un color, por sí solo, carece de valor técnico si no está ligado a una escala explícita de dBm y a un criterio de uso previsto.

La validación posterior a la instalación compara el diseño previsto con la medición real. No basta con comprobar que existe conectividad. Se debe cuantificar qué porcentaje del área útil conserva niveles iguales o superiores a −70 dBm, cuánta superficie cae por debajo de −90 dBm y dónde se concentran las discontinuidades. Estas métricas convierten la inspección visual en una evaluación repetible, útil para aceptar o corregir un despliegue.

También resulta relevante la comparación entre escenarios. Un mismo plano puede levantarse antes y después de una optimización de potencia, de un cambio de canal o de la reubicación de un punto de acceso. Al contrastar dos superficies de cobertura se identifican mejoras, degradaciones y desplazamientos del patrón de señal. Esa capacidad es valiosa para Bulldog Tech., porque permite demostrar con evidencia espacial si una intervención produjo el efecto esperado.

Wireless HeatMapper adopta esta lógica como base para el módulo de *heatmap* del Sprint 4 y para la comparación de escenarios prevista en el Sprint 5. La utilidad del sistema no radica solo en visualizar colores sobre un plano, sino en vincular cada zona con umbrales de aceptación, métricas de cobertura y recomendaciones operativas derivadas del comportamiento real de la WLAN.

**Tabla 14.** Métricas de validación de cobertura para entornos empresariales basadas en CWNA-107

| Métrica | Umbral de referencia | Interpretación operativa |
| ------- | -------------------- | ------------------------ |
| Área con señal ≥ −70 dBm | Meta principal de diseño | Cobertura adecuada para datos empresariales y continuidad de servicio |
| Área con señal ≥ −65 dBm | Meta reforzada | Cobertura apta para aplicaciones sensibles a latencia |
| Área con señal < −90 dBm | Debe tender a 0 % | Zona muerta o de conectividad marginal |
| Comparación entre escenarios | Diferencia por celda o por área agregada | Permite verificar mejora o deterioro después de una intervención |

### Referencias

Coleman, D., Westcott, D. A., Harkins, B., & Jackman, S. (2021). *CWNA: Certified Wireless Network Administrator study guide (Examen CWNA-107)* (5.ª ed.). Sybex.

Longley, P. A., Goodchild, M. F., Maguire, D. J., & Rhind, D. W. (2015). *Geographic information science and systems* (4.ª ed.). Wiley.

---
