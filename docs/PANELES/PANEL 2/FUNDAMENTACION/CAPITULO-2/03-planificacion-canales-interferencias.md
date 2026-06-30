## 2.2 Planificación de Canales y Gestión de Interferencias

La planificación de canales determina cuánta eficiencia puede conservar una WLAN cuando múltiples puntos de acceso operan en un mismo espacio físico. En la banda de 2.4 GHz existen 14 canales definidos por el estándar, aunque en la región de las Américas normalmente se utilizan 11. Debido al ancho espectral de 20 MHz y a la cercanía entre frecuencias centrales, solo los canales 1, 6 y 11 pueden considerarse no solapados en condiciones normales de diseño. Esa restricción convierte a 2.4 GHz en una banda útil para compatibilidad, pero limitada para ambientes densos.

La banda de 5 GHz ofrece mayor flexibilidad. Los canales se distribuyen en segmentos *Unlicensed National Information Infrastructure* (UNII, infraestructura nacional no licenciada), comúnmente UNII-1, UNII-2 y UNII-3, con un conjunto amplio de canales no solapados cuando se trabaja en anchos de 20 MHz. En la práctica, el aprovechamiento efectivo depende del país, de la política regulatoria sobre DFS y del perfil de los clientes. Aun así, 5 GHz brinda mejores condiciones para reutilización espectral y diseño de alta densidad.

Un patrón de reutilización de canales busca separar celdas cercanas que emiten en la misma frecuencia. Cuando dos APs comparten canal y se escuchan mutuamente se produce *Co-Channel Interference* (CCI, interferencia co-canal). No siempre implica corrupción de tramas, pero sí más tiempo de espera, menor eficiencia y degradación del *throughput*. En cambio, la *Adjacent Channel Interference* (ACI, interferencia de canal adyacente) sí introduce solapamiento espectral entre celdas en canales vecinos, fenómeno especialmente dañino en 2.4 GHz por el reuso incorrecto de combinaciones como 1, 3 y 5.

Otro problema clásico es el *hidden node problem* (problema del nodo oculto). Ocurre cuando dos clientes no pueden oírse entre sí, aunque ambos sí alcanzan al mismo AP. El resultado son colisiones repetidas en el receptor compartido. El mecanismo RTS/CTS no elimina toda la ineficiencia, pero puede reducirla al coordinar la reserva temporal del medio antes de la transmisión de tramas más sensibles a colisión.

En Wireless HeatMapper estos conceptos se traducen en reglas de análisis. El sistema puede identificar puntos de acceso observados en el levantamiento, reconocer coincidencia de canal y valorar si existe un patrón de solapamiento problemático cuando señales elevadas del mismo canal coexisten en zonas cercanas. Esa lectura resulta esencial para el módulo de interferencias y para la emisión de recomendaciones sobre cambio de canal, redistribución de potencia o segmentación por banda.

### Referencias

Coleman, D., Westcott, D. A., Harkins, B., & Jackman, S. (2021). *CWNA: Certified Wireless Network Administrator study guide (Examen CWNA-107)* (5.ª ed.). Sybex.

IEEE. (2021). *IEEE Standard for Information Technology—Telecommunications and information exchange between systems Local and metropolitan area networks—Specific requirements—Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications*. Institute of Electrical and Electronics Engineers.

---
