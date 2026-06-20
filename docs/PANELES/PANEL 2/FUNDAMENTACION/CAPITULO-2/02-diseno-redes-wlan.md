## 2.1 Diseño y Planificación de Redes WLAN

El diseño de una red *Wireless Local Area Network* (WLAN, red de área local inalámbrica) parte de metas de cobertura medibles. El CWNA-107 diferencia un objetivo primario de aproximadamente −65 dBm para áreas con aplicaciones sensibles a latencia, como voz sobre IP, y un objetivo secundario de −70 dBm para nuevas instalaciones donde se prioriza conectividad estable de datos. Esa distinción evita evaluar la red con un único umbral absoluto. Un edificio puede cumplir conectividad general y, al mismo tiempo, fallar para servicios que requieren márgenes de señal más exigentes.

La cobertura no se analiza solo por intensidad puntual. También importa el solapamiento entre celdas vecinas. En despliegues corporativos se recomienda un traslape de 15 % a 20 % entre áreas útiles de servicio para permitir *roaming* (traspaso de asociación entre puntos de acceso) sin cortes perceptibles. Si el solapamiento es menor, el cliente pierde continuidad durante el desplazamiento. Si es excesivo, aumenta la contención del medio y se degrada la reutilización espectral.

La capacidad por punto de acceso tampoco puede estimarse desde el estándar nominal. En 802.11ac y 802.11ax el ancho de canal, la modulación, la cantidad de flujos espaciales y la densidad de usuarios concurrentes modifican el *throughput* (caudal útil) real disponible para cada cliente. En escenarios empresariales, un AP que anuncia velocidades muy superiores a 1 Gbps rara vez entrega esa cifra como capacidad efectiva por usuario; el presupuesto debe considerar sobrecarga MAC, contención CSMA/CA y degradación por distancia. Por ello, el dimensionamiento de celdas y el análisis de capacidad deben evaluarse de forma conjunta.

El modelo idealizado de celdas hexagonales sirve como abstracción para planificar reutilización y cobertura. Sin embargo, en edificios reales la señal se deforma por muros, mobiliario, ductos, ascensores y vacíos estructurales. La celda observada deja de ser regular y adquiere contornos asimétricos. Wireless HeatMapper toma esa diferencia como criterio operativo: no asume geometrías perfectas, sino que parte de mediciones sobre plano para aproximar la cobertura efectiva de cada zona.

En el proyecto, los umbrales de −65 dBm y −70 dBm alimentan la clasificación visual del *heatmap*, mientras que la lectura del solapamiento entre celdas permite justificar recomendaciones de reubicación o ajuste de potencia de puntos de acceso. El análisis de cobertura, por tanto, no se limita a colorear un plano; interpreta si la distribución espacial satisface el objetivo de diseño esperado para el edificio intervenido.

### Referencias

Coleman, D., Westcott, D. A., Harkins, B., & Jackman, S. (2021). *CWNA: Certified Wireless Network Administrator study guide (Examen CWNA-107)* (5.ª ed.). Sybex.

IEEE. (2021). *IEEE Standard for Information Technology—Telecommunications and information exchange between systems Local and metropolitan area networks—Specific requirements—Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications*. Institute of Electrical and Electronics Engineers.

---
