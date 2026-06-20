## Redes Inalámbricas de Área Local (WLAN) — Estándar IEEE 802.11

### Definición y origen del estándar

Una **red inalámbrica de área local** (Wireless Local Area Network, WLAN) es un sistema de comunicación de datos que utiliza señales de radiofrecuencia (RF) en lugar de cableado físico para interconectar dispositivos dentro de un área geográfica limitada. El estándar de referencia universal para las WLAN es el **IEEE 802.11**, publicado originalmente por el Instituto de Ingenieros Eléctricos y Electrónicos (IEEE) en 1997 y revisado periódicamente desde entonces (IEEE, 1997). La denominación comercial de las redes conformes al estándar IEEE 802.11 es **Wi-Fi**, término acuñado por la Wi-Fi Alliance para certificar la interoperabilidad entre dispositivos de distintos fabricantes.

El estándar IEEE 802.11 define las capas física (PHY) y de control de acceso al medio (MAC) de las WLAN. La capa PHY especifica las técnicas de modulación, las bandas de frecuencia y los esquemas de codificación empleados; la capa MAC especifica los mecanismos de acceso al medio compartido, la fragmentación de tramas y los procedimientos de asociación, autenticación y roaming (Coleman & Westcott, 2018).

### Variantes relevantes del estándar

A lo largo de su historia, el estándar ha incorporado diversas enmiendas que amplían sus capacidades. Las variantes más relevantes para el contexto del proyecto son:

| Enmienda           | Año  | Bandas          | Velocidad máxima teórica | Característica clave                |
| ------------------ | ---- | --------------- | ------------------------ | ----------------------------------- |
| 802.11b            | 1999 | 2.4 GHz         | 11 Mbps                  | Primera variante de adopción masiva |
| 802.11a            | 1999 | 5 GHz           | 54 Mbps                  | Menos interferencias que 2.4 GHz    |
| 802.11g            | 2003 | 2.4 GHz         | 54 Mbps                  | Retro-compatible con 802.11b        |
| 802.11n (Wi-Fi 4)  | 2009 | 2.4 / 5 GHz     | 600 Mbps                 | MIMO, canales de 40 MHz             |
| 802.11ac (Wi-Fi 5) | 2013 | 5 GHz           | 6.9 Gbps                 | MU-MIMO, canales 80/160 MHz         |
| 802.11ax (Wi-Fi 6) | 2021 | 2.4 / 5 / 6 GHz | 9.6 Gbps                 | OFDMA, BSS Coloring, TWT            |

> Los dispositivos Android modernos soportan mínimamente 802.11n y generalmente 802.11ac. La aplicación móvil del Wireless HeatMapper captura parámetros de señal de cualquier AP que el dispositivo detecte, independientemente de la variante 802.11 que utilice (Coleman & Westcott, 2018).

### Arquitectura básica de una WLAN

Una WLAN en modo infraestructura —el caso aplicable a Bulldog Tech.— está conformada por los siguientes elementos:

- **Punto de Acceso (Access Point, AP):** dispositivo inalámbrico conectado a la red cableada que actúa como concentrador para los clientes Wi-Fi. Cada AP define una célula de cobertura denominada **BSS** (Basic Service Set), identificada por un **BSSID** (dirección MAC del AP).
- **SSID (Service Set Identifier):** nombre lógico de la red Wi-Fi, anunciado en las tramas _beacon_ que el AP transmite periódicamente. Un mismo AP puede anunciar múltiples SSID (red corporativa, red invitados, etc.).
- **Cliente inalámbrico (STA):** cualquier dispositivo que se asocia a un AP para acceder a la red (laptops, smartphones, escáneres de código de barras, etc.).
- **ESS (Extended Service Set):** conjunto de múltiples BSS interconectados por la infraestructura cableada, que comparten el mismo SSID para permitir el roaming transparente de los clientes.

La comprensión de estos elementos es fundamental para interpretar los datos capturados por el Wireless HeatMapper: cada medición RSSI queda asociada al BSSID del AP cuya señal se midió, al SSID de la red correspondiente, al canal y a la frecuencia utilizados.

### Bandas de frecuencia y canales

Las WLAN operan en bandas de frecuencia no licenciadas (libre uso con limitaciones de potencia):

**Banda 2.4 GHz (ISM):** comprende los canales 1 al 14 (según la región). Únicamente los canales 1, 6 y 11 son no solapados entre sí en la región de América del Norte y la mayor parte de América Latina. Tiene mayor penetración en obstáculos pero está más congestionada por la coexistencia con dispositivos Bluetooth, microondas y teléfonos inalámbricos.

**Banda 5 GHz (U-NII):** comprende 25 canales no solapados de 20 MHz. Ofrece menor interferencia, mayor velocidad y menor penetración en obstáculos que la banda 2.4 GHz. Es la banda recomendada por el CWNA-107 para el diseño de redes corporativas de alto rendimiento.

La selección de canal es un parámetro crítico en el diseño de WLAN porque la interferencia co-canal (CCI) —causada por dos APs que utilizan el mismo canal dentro del rango de escucha de un cliente— degrada directamente el rendimiento de la red (Coleman & Westcott, 2018). El módulo de análisis de cobertura del Wireless HeatMapper (RP4) detecta automáticamente los casos de CCI y ACI (interferencia por canal adyacente) a partir de los datos capturados.
