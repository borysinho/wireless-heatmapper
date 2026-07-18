# Anexos

## Anexo A: codigos QR

| Recurso | URL |
| ------- | --- |
| Repositorio GitHub | https://github.com/borysinho/wireless-heatmapper |
| Sitio empresarial Team 24 Software | https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/ |
| Facebook oficial Team 24 Software | https://www.facebook.com/profile.php?id=61591962512748 |
| Panel administrador | https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/admin/login |
| Documentacion Swagger / OpenAPI | https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/docs |
| Manual de usuario | https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/ |
| Releases moviles | https://github.com/borysinho/wireless-heatmapper/releases |

## Anexo B: glosario

| Termino | Definicion |
| ------- | ---------- |
| AP | Punto de acceso inalambrico. |
| BSSID | Identificador MAC de una radio WiFi. |
| Heatmap | Representacion visual de intensidad de senal sobre un plano. |
| RSSI | Indicador de intensidad de senal recibida. |
| SaaS | Software como servicio operado en la nube. |
| Sprint | Iteracion corta de trabajo en Scrum. |
| Token de enlace | Credencial URL para acceso controlado al portal cliente. |

## Anexo C: matriz resumida de trazabilidad

| Requerimiento | Historia/flujo | Modelo | Prueba |
| ------------- | -------------- | ------ | ------ |
| RP1 | Captura WiFi | Contexto, logica | Registro de mediciones y validacion RSSI. |
| RP2 | Plano y puntos | Datos, logica | Carga, calibracion y puntos validos. |
| RP3 | Heatmap | Arquitectura, datos | Generacion con puntos minimos. |
| RP5 | IA | Arquitectura, datos | Conjunto derivado y comparacion. |
| RP7 | Admin | Contexto, datos | Usuarios, clientes y proyectos. |
| RP8 | Persistencia | Arquitectura, datos | Integracion backend + PostgreSQL. |
| RP9 | Portal cliente | Logica, despliegue | Token valido, expirado y revocado. |

## Anexo D: lista de diagramas

| Codigo | Diagrama |
| ------ | -------- |
| D01 | Modelo de contexto. |
| D02 | Arquitectura por paquetes. |
| D03 | Arquitectura de despliegue. |
| D04 | Modelo de datos conceptual. |
| D05 | Logica de captura y heatmap. |
| D06 | Logica de portal cliente. |
| D07 | Estados del proyecto. |
| D08 | Navegabilidad CASE. |
| D09 | Flujo de pruebas del Proceso Unificado. |

## Anexo E: consolidacion a Word

El documento Word se genera mediante el script de consolidacion incluido con esta entrega. Dicho script renderiza diagramas PlantUML, genera codigos QR, une los capitulos y produce el documento consolidado para Microsoft Word.
