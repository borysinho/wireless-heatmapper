## 2.4 Metodología de Site Survey WiFi

### 2.4.1 Definición y propósito

Un **site survey WiFi** es el proceso sistemático de evaluar las características de un entorno físico para determinar la calidad de la cobertura inalámbrica existente o para planificar el despliegue óptimo de una nueva red. Según el CWNA-107, "el 75 % del trabajo de una buena red inalámbrica está en el pre-engineering" (Coleman & Westcott, 2018, p. 537), subrayando que la medición y el análisis previos al despliegue son tan importantes —o más— que la instalación misma del equipamiento.

El producto central de un site survey es el **mapa de cobertura** (o mapa de calor) del edificio: una representación visual sobre el plano de planta que muestra la distribución espacial de los valores de RSSI, SNR y demás métricas de calidad de señal. Este mapa es el entregable principal del Wireless HeatMapper.

### 2.4.2 Tipos de site survey

El CWNA-107 distingue tres modalidades de site survey según el método de obtención de datos (Coleman & Westcott, 2018):

#### Survey Pasivo (Passive Survey)

El cliente inalámbrico **no se asocia** al AP. Opera en modo escucha pasiva, capturando las tramas _beacon_ y _probe response_ que los APs transmiten. Mide RSSI, nivel de ruido, SNR y metadatos de las tramas de gestión (SSID, BSSID, canal, tipo de cifrado). Es el tipo de survey que ejecuta la aplicación móvil del Wireless HeatMapper durante el recorrido del técnico: el dispositivo Android escanea las redes disponibles en cada punto sin necesidad de autenticarse en ninguna de ellas.

#### Survey Activo (Active Survey)

El cliente se **asocia** a un AP específico y transmite tráfico de prueba (pings ICMP, frames de datos). Además de las métricas del survey pasivo, mide pérdida de paquetes (packet loss) y porcentaje de retransmisiones a nivel de capa 2. Proporciona una imagen más completa del rendimiento real de la red, pero requiere credenciales de acceso al AP bajo análisis.

#### Survey Predictivo (Predictive Survey)

Utiliza **software de modelado RF** para simular la cobertura sin necesidad de visitar físicamente cada punto del edificio. El técnico importa el plano, dibuja los muros con sus valores de atenuación (obtenidos durante una visita de caracterización), coloca los APs virtualmente y el motor de cálculo genera un heatmap simulado. Herramientas comerciales como Ekahau Site Survey, iBwave Wi-Fi Suite y TamoGraph Site Survey implementan esta modalidad (Coleman & Westcott, 2018). El Wireless HeatMapper implementa la fase posterior al survey —generación del heatmap proyectado con IA— como complemento del survey pasivo de campo.

### 2.4.3 Procedimiento canónico de análisis de cobertura (CWNA-107)

El procedimiento recomendado por el CWNA-107 para determinar la ubicación óptima de los APs durante un survey es el siguiente (Coleman & Westcott, 2018):

1. **Configurar el AP de prueba a 25 mW** (no a potencia máxima), midiendo preferentemente con la radio de 5 GHz, cuya menor cobertura es el factor limitante del diseño.
2. **Colocar el AP en una esquina del edificio** y caminar diagonalmente hacia el interior hasta que el RSSI descienda a **−70 dBm**: esa posición es la ubicación del primer AP.
3. **Mapear los bordes de la celda (cell edges)** —los límites donde la señal del AP1 cae a −70 dBm— caminando desde el AP en distintas direcciones.
4. **Encadenar el proceso** (daisy-chain): desde el AP1, caminar paralelo al borde del edificio hasta alcanzar el próximo punto de −70 dBm, y desde allí continuar hasta el siguiente −70 dBm. Esa segunda posición es la ubicación del AP2. Repetir para todos los APs del edificio.
5. **Registrar cobertura primaria y secundaria:** desde cualquier punto cubierto, el cliente debe escuchar al menos un AP a ≥ −65 dBm (primario) y un AP secundario a ≤ 5 dBm por debajo del primario, para garantizar roaming suave.

Este procedimiento es el que inspira la lógica del módulo de IA del Wireless HeatMapper (RP5): dado un conjunto de mediciones reales de campo, el modelo sugiere la cantidad mínima de APs y sus posiciones para que toda la zona relevada cumpla el objetivo de diseño ≥ −70 dBm.

### 2.4.4 Análisis del espectro

El CWNA-107 establece que un site survey profesional siempre debe incluir un **análisis del espectro** en todas las bandas de interés, con un analizador de espectro real (no con la NIC Wi-Fi del cliente). El propósito es identificar fuentes de interferencia no-802.11 —microondas, teléfonos inalámbricos DECT, cámaras de videovigilancia analógica, dispositivos Bluetooth, motores industriales— cuya energía eleva el piso de ruido y degrada el SNR sin que sea posible detectarlos con un escáner Wi-Fi convencional (Coleman & Westcott, 2018).

> "Si el piso de ruido excede −85 dBm en cualquier banda, el rendimiento de la WLAN se degrada severamente" (Coleman & Westcott, 2018, p. 551).

En la versión actual del Wireless HeatMapper, el módulo de captura (RP1) no incluye análisis de espectro —que requiere hardware especializado—, pero el módulo de análisis de cobertura (RP4) registra el nivel de ruido reportado por la NIC Android como indicador aproximado, y el portal de cliente muestra esta información como parte del reporte técnico entregado.

### 2.4.5 Densidad de muestreo

La fidelidad del mapa de calor depende directamente de la densidad espacial de los puntos de medición: a mayor densidad de puntos, menor es el error de interpolación entre ellos. El CWNA-107 recomienda una densidad mínima de puntos por metro cuadrado como función del tamaño del área a relevar y de la heterogeneidad del entorno. En entornos con muchos obstáculos (oficinas abiertas con cubículos, plantas industriales con racks) se requiere mayor densidad que en espacios abiertos.

El Wireless HeatMapper delega al técnico la decisión de densidad de muestreo —quien marca manualmente cada punto sobre el plano— pero el portal de cliente muestra visualmente las zonas del plano con escasez de puntos de medición, incentivando al técnico a completar las áreas con baja densidad antes de generar el reporte final.
