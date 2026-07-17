# Resumen ejecutivo

Wireless HeatMapper es un sistema integrado para relevar, analizar y compartir cobertura WiFi en interiores mediante mapas de calor. El problema que atiende es la operacion fragmentada de los tecnicos de Bulldog Tech., quienes tradicionalmente combinan aplicaciones moviles de analisis WiFi, planos impresos, hojas de calculo y procesamiento manual posterior. Esa forma de trabajo eleva el riesgo de error, dificulta la trazabilidad de mediciones y retrasa la entrega de resultados tecnicos al cliente.

La solucion se construyo bajo una modalidad 100 % en linea. La aplicacion movil Android funciona como cliente delgado para el tecnico de campo; el backend REST concentra la logica de negocio, persistencia, interpolacion e inteligencia artificial; y la plataforma web permite administracion organizacional y acceso seguro del cliente final mediante enlace unico. Toda persistencia de dominio reside en PostgreSQL, sin base de datos local ni sincronizacion diferida en el dispositivo movil.

El producto entrega las siguientes capacidades principales:

- Gestion de usuarios, clientes y proyectos.
- Importacion y calibracion de planos.
- Captura de mediciones WiFi con RSSI, SSID, BSSID, canal y frecuencia.
- Generacion de mapas de calor mediante procesamiento backend.
- Gestion de conjuntos de puntos de acceso y propuestas asistidas por IA.
- Comparacion entre configuracion actual y propuesta.
- Portal de cliente con visualizacion interactiva del resultado publicado.
- Repositorio, releases moviles y frontend accesibles en linea.

La documentacion SW2 complementa el producto con el enfoque institucional exigido por la materia. No solo describe el software, sino tambien la empresa simulada que lo produce, su manual de calidad, su infraestructura, su estrategia comercial, sus procedimientos legales, su plan de pruebas y su puesta en marcha como producto real.

## Cobertura de los doce puntos

| Punto | Entregable documental |
| ----- | --------------------- |
| 1 | PAPS adaptado a SW2. |
| 2 | Modelos de contexto, arquitectura, datos y logica. |
| 3 | Manual de garantia de calidad institucional. |
| 4 | Uso de herramientas CASE y navegabilidad entre modelos. |
| 5 | Aspectos legales para apertura de empresa de software en Bolivia. |
| 6 | Infraestructura tecnologica para produccion de software. |
| 7 | Sitio web de la empresa publicado en linea. |
| 8 | Estudio de mercado cuantificado. |
| 9 | Plan integral de pruebas del software. |
| 10 | Plan de marketing. |
| 11 | Puesta en marcha, cloud, licencias, tiendas, terminos y privacidad. |
| 12 | Software como producto final entregable. |

