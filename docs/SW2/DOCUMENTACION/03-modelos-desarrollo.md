# Modelos de desarrollo

El proyecto adopta Scrum como marco de gestion y complementa cada incremento con modelos de ingenieria elaborados en UML 2.5+. Los modelos obligatorios son contexto, arquitectura, datos y logica. Su funcion es mantener una vision verificable del alcance, estructura, persistencia y comportamiento dinamico del sistema.

## Modelo de contexto

El modelo de contexto delimita actores, casos de uso y frontera del sistema. Los actores principales son tecnico de campo, administrador, cliente, Android WifiManager API y servicio interno de IA. Su representacion se incorpora como figura UML en el documento consolidado.

## Modelo de arquitectura

El modelo de arquitectura representa los componentes principales: app movil Flutter, plataforma web React, backend FastAPI, modulo IA, PostgreSQL, Nginx y pipeline de despliegue. Se documenta mediante diagrama de paquetes y diagrama de despliegue:

- Diagrama de paquetes.
- Diagrama de despliegue.

## Modelo de datos

El modelo de datos define las entidades de negocio persistidas en PostgreSQL: usuario, cliente, proyecto, plano, punto de medicion, lectura RSSI, conjunto AP, mapa de calor y token de enlace cliente. Su representacion conceptual se incorpora como figura UML en el documento consolidado.

## Modelo de logica

El modelo de logica describe flujos dinamicos relevantes mediante diagramas de secuencia, estados y actividad. Para SW2 se priorizan los flujos que demuestran mayor valor de negocio:

- Captura de mediciones y generacion de heatmap.
- Publicacion y consulta del portal cliente.
- Ciclo de vida de un proyecto.

## Trazabilidad entre modelos

| Elemento | Modelo de contexto | Modelo de arquitectura | Modelo de datos | Modelo de logica |
| -------- | ------------------ | ---------------------- | --------------- | ---------------- |
| Captura WiFi | UC05 | App movil, backend, PostgreSQL | PuntoMedicion, LecturaRSSI | Secuencia captura-heatmap |
| Heatmap | UC06 | Backend, InterpolacionService | MapaCalor, ConjuntoAP | Secuencia captura-heatmap |
| IA | UC08, UC09 | Modulo IA backend | ConjuntoAP, ConjuntoAPItem | Flujo de propuesta |
| Portal cliente | UC15, UC16, UC17 | Web, backend, Nginx | TokenEnlaceCliente | Secuencia portal |
| Administracion | UC13, UC18, UC19 | Web admin, backend | Usuario, Cliente, Proyecto | CRUD administrativo |

## Criterios formales UML

- Los casos de uso separan actores humanos y sistemas externos.
- Los paquetes muestran dependencias dirigidas y responsabilidades por capa.
- El despliegue distingue nodos fisicos/logicos, contenedores y artefactos.
- Las clases expresan atributos, multiplicidades, composicion y asociaciones.
- Las secuencias muestran mensajes sincronos, validaciones y persistencia.
