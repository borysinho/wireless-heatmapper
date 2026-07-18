# Herramientas CASE

## Concepto

CASE significa Computer Aided Software Engineering, es decir, ingenieria de software asistida por computador. En este proyecto la herramienta CASE no se utiliza solamente para dibujar, sino para organizar modelos, navegar entre artefactos, mantener consistencia semantica y respaldar decisiones de diseno.

## Herramientas adoptadas

| Herramienta | Uso |
| ----------- | --- |
| StarUML | Organizacion de modelos UML 2.5+, paquetes, clases, casos de uso y diagramas dinamicos. |
| PlantUML | Representacion textual versionable de diagramas UML. |
| Visual Studio Code | Edicion, vista previa, trazabilidad con repositorio y revision Markdown. |
| GitHub | Versionado, control de cambios, revision y publicacion de evidencia. |

## Navegabilidad esperada

La demostracion CASE debe permitir recorrer la arquitectura desde niveles generales hacia detalles tecnicos:

1. Diagrama de paquetes del sistema.
2. Paquete de aplicacion movil, backend o web.
3. Casos de uso asociados al paquete.
4. Diagrama de secuencia del caso de uso.
5. Clases, servicios o repositorios que participan en la secuencia.
6. Entidades de datos persistidas.
7. Pruebas vinculadas al comportamiento esperado.

El recorrido replica la navegabilidad solicitada en clase: desde un diagrama de paquetes se ingresa al caso de uso, luego al diagrama de comunicacion o secuencia, despues a las clases participantes, y los mensajes observados en la interaccion se verifican como metodos u operaciones de esas clases.

La figura UML de navegabilidad CASE representa este recorrido y demuestra la relacion entre modelos, clases, datos y pruebas.

## Evidencia de uso real

| Evidencia | Descripcion |
| --------- | ----------- |
| Modelo de contexto | Actores, casos de uso y frontera del sistema. |
| Modelo de arquitectura | Paquetes y despliegue con componentes reales. |
| Modelo de datos | Clases conceptuales y relaciones de persistencia. |
| Modelo de logica | Secuencias de captura, heatmap y portal cliente. |
| Trazabilidad | Relacion entre requerimientos, casos de uso, entidades y pruebas. |
| Exportacion | Diagramas renderizados a imagen para documento Word. |

## Beneficio para productividad

El enfoque CASE reduce retrabajo porque los diagramas se versionan como texto, se revisan junto con el codigo y pueden regenerarse automaticamente. Tambien facilita explicar el sistema al docente, al Product Owner y al equipo tecnico, manteniendo una relacion clara entre lo solicitado, lo disenado, lo implementado y lo probado.

## Criterios de aceptacion de la demostracion

- Se visualizan al menos los cuatro modelos obligatorios.
- Se demuestra navegabilidad entre caso de uso, secuencia, clase y dato.
- Los diagramas usan notacion UML 2.5+.
- El modelo no contradice la modalidad 100 % en linea.
- Las entidades y componentes corresponden al producto implementado.
