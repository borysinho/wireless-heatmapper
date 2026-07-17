# Modelos de desarrollo

El proyecto Wireless HeatMapper utiliza modelos UML 2.5+ como soporte tecnico del proceso Scrum. Estos modelos permiten representar el sistema desde cuatro perspectivas obligatorias: contexto, arquitectura, datos y logica. Cada perspectiva tiene un proposito distinto y se vincula con diagramas PlantUML versionados en `docs/SW2/diagramas/`, de forma que el documento academico, la herramienta CASE y el repositorio mantengan la misma fuente de verdad.

Los modelos se aplican sobre la modalidad 100 % en linea del producto: la aplicacion movil actua como cliente delgado, el backend FastAPI concentra la logica de negocio, PostgreSQL es la unica fuente persistente de datos de dominio y la plataforma web cubre la administracion y el portal de cliente.

## Modelo de contexto

El modelo de contexto delimita la frontera funcional de Wireless HeatMapper y muestra como interactuan los actores humanos y sistemas externos con el producto. Su objetivo es aclarar que responsabilidades pertenecen al sistema y que responsabilidades quedan fuera de el.

En este proyecto, el contexto distingue al tecnico de campo, administrador, cliente, Android WifiManager API y servicio interno de IA. Tambien resume los casos de uso principales relacionados con autenticacion, proyectos, planos, captura WiFi, heatmaps, administracion, propuestas IA y consulta por enlace.

| Diagrama | Tipo UML | Bloque PlantUML |
| -------- | -------- | --------------- |
| Modelo de Contexto - Wireless HeatMapper | Casos de uso | [01-modelo-contexto.puml](../diagramas/01-modelo-contexto.puml) |

## Modelo de arquitectura

El modelo de arquitectura describe la organizacion tecnica del sistema y las responsabilidades de cada componente. Sirve para verificar que la solucion respeta el stack acordado: Flutter/Dart para la app movil, React/TypeScript para la web, FastAPI para el backend, PostgreSQL como base central, Docker Compose y Nginx para despliegue.

La arquitectura se representa con dos vistas complementarias. La vista de paquetes muestra la separacion por capas y modulos de software. La vista de despliegue muestra los nodos de ejecucion, contenedores, artefactos y enlaces de comunicacion entre dispositivo Android, navegador, servidor cloud, backend, web, base de datos y GitHub Actions.

| Diagrama | Tipo UML | Bloque PlantUML |
| -------- | -------- | --------------- |
| Modelo de Arquitectura - Diagrama de Paquetes | Paquetes | [02-arquitectura-paquetes.puml](../diagramas/02-arquitectura-paquetes.puml) |
| Modelo de Arquitectura - Diagrama de Despliegue | Despliegue | [03-arquitectura-despliegue.puml](../diagramas/03-arquitectura-despliegue.puml) |

## Modelo de datos

El modelo de datos representa las entidades de negocio, sus atributos principales y relaciones. Su funcion es asegurar que la persistencia centralizada cubre los datos necesarios para ejecutar los flujos del producto sin almacenamiento local de dominio en la app movil.

El modelo conceptual incluye usuarios, clientes, proyectos, planos, puntos de medicion, lecturas RSSI, conjuntos AP, items de conjuntos, mapas de calor y tokens de enlace cliente. Tambien explicita relaciones de composicion y multiplicidad para reflejar que un proyecto contiene planos, mediciones, heatmaps y enlaces publicados.

| Diagrama | Tipo UML | Bloque PlantUML |
| -------- | -------- | --------------- |
| Modelo de Datos Conceptual - Wireless HeatMapper | Clases | [04-modelo-datos-conceptual.puml](../diagramas/04-modelo-datos-conceptual.puml) |

## Modelo de logica

El modelo de logica describe el comportamiento dinamico del sistema. A diferencia del modelo de datos, que muestra estructura, este modelo muestra secuencias de mensajes, cambios de estado y reglas de ejecucion observables durante los casos de uso principales.

Para SW2 se priorizan tres diagramas. El primero cubre la captura WiFi en linea y generacion de heatmap. El segundo cubre la publicacion de resultados y acceso del cliente mediante token. El tercero resume el ciclo de vida de un proyecto desde su creacion hasta archivo o reactivacion.

| Diagrama | Tipo UML | Bloque PlantUML |
| -------- | -------- | --------------- |
| Modelo de Logica - Captura WiFi y Generacion de Heatmap | Secuencia | [05-logica-captura-heatmap.puml](../diagramas/05-logica-captura-heatmap.puml) |
| Modelo de Logica - Publicacion y Portal Cliente | Secuencia | [06-logica-portal-cliente.puml](../diagramas/06-logica-portal-cliente.puml) |
| Modelo de Logica - Estados del Proyecto | Estados | [07-estados-proyecto.puml](../diagramas/07-estados-proyecto.puml) |

## Diagramas complementarios

Ademas de los cuatro modelos obligatorios, el paquete documental incluye diagramas de apoyo para demostrar trazabilidad con herramientas CASE y planificacion de pruebas. No reemplazan los modelos principales; sirven como evidencia academica de navegabilidad, validacion y control de calidad.

| Diagrama | Proposito | Bloque PlantUML |
| -------- | --------- | --------------- |
| Herramientas CASE - Navegabilidad entre modelos | Evidenciar trazas entre casos de uso, secuencias, clases, datos y pruebas. | [08-case-navegabilidad.puml](../diagramas/08-case-navegabilidad.puml) |
| Flujo de Trabajo de Pruebas - Proceso Unificado | Representar el flujo general de planificacion, ejecucion, correccion y validacion de pruebas. | [09-flujo-pruebas-rup.puml](../diagramas/09-flujo-pruebas-rup.puml) |

## Trazabilidad entre modelos

| Elemento funcional | Modelo de contexto | Modelo de arquitectura | Modelo de datos | Modelo de logica |
| ------------------ | ------------------ | ---------------------- | --------------- | ---------------- |
| Captura WiFi | UC05 Capturar senales WiFi | App movil, WifiScanner, backend, PostgreSQL | PuntoMedicion, LecturaRSSI | Secuencia captura WiFi y heatmap |
| Gestion de proyectos | UC01 Gestionar proyecto | App movil, web admin, backend | Proyecto, Usuario, Cliente | Estados del proyecto |
| Planos | UC02 Importar plano, UC03 Calibrar plano | App movil, backend, repositorios | Plano, PuntoMedicion | Secuencia captura WiFi y heatmap |
| Heatmaps | UC06 Generar mapa de calor | InterpolacionService, backend, PostgreSQL | MapaCalor, ConjuntoAP | Secuencia captura WiFi y heatmap |
| IA | UC08 Generar propuesta IA, UC09 Comparar propuesta | Modulo IA backend, OptimizadorAPService | ConjuntoAP, ConjuntoAPItem, MapaCalor | Comparacion derivada desde conjuntos AP |
| Portal cliente | UC15 Generar enlace cliente, UC16 Consultar heatmap, UC17 Ver conjuntos AP | Web portal, Nginx, backend share | TokenEnlaceCliente, MapaCalor, ConjuntoAP | Secuencia publicacion y portal cliente |
| Administracion | UC13 Gestionar usuarios, UC18 Ver proyectos organizacion, UC19 Gestionar clientes | Web admin, backend, PostgreSQL | Usuario, Cliente, Proyecto | Flujos CRUD administrativos |

## Criterios formales UML

- Los casos de uso separan actores humanos, sistemas externos y frontera del sistema.
- Los paquetes muestran responsabilidades por capa y dependencias dirigidas.
- El despliegue distingue nodos, contenedores, artefactos y canales de comunicacion.
- Las clases expresan atributos, multiplicidades, composicion y asociaciones relevantes.
- Las secuencias muestran participantes, mensajes sincronos, validaciones y persistencia.
- El diagrama de estados mantiene transiciones compatibles con los estados del proyecto.
- Todos los diagramas se mantienen como PlantUML para facilitar regeneracion, revision y uso en herramientas CASE.
