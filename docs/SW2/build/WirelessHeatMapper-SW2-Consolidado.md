

---
title: "Documentacion Integral del Proyecto Wireless HeatMapper"
subtitle: "Ingenieria de Software II"
author:
  - "Grupo 24 - Team 24 Software"
date: "Gestion 2026"
lang: es-BO
---

# Documentacion Integral del Proyecto Wireless HeatMapper

**Universidad:** Universidad Autonoma Gabriel Rene Moreno  
**Facultad:** Facultad Integral del Chaco y/o Facultad de Ingenieria en Ciencias de la Computacion y Telecomunicaciones  
**Materia:** Ingenieria de Software II  
**Proyecto:** Sistema Inteligente de Analisis y Optimizacion de Cobertura WiFi mediante Mapas de Calor  
**Empresa de software:** Team 24 Software  
**Cliente del caso:** Bulldog Tech.  
**Grupo:** 24  
**Integrantes:** Jhasmany Jhunnior Fernandez Ortega; Herland Borys Quiroga Flores  
**Ciudad:** Santa Cruz de la Sierra, Bolivia  
**Gestion:** 2026  
**Modalidad del producto:** 100 % en linea  

## Control documental

| Version | Fecha | Responsable | Descripcion |
| ------- | ----- | ----------- | ----------- |
| 1.0 | 17 jul 2026 | Team 24 Software | Emision inicial de la documentacion integral para Ingenieria de Software II. |

## Declaracion de alcance documental

El presente documento consolida los doce puntos exigidos para la materia Ingenieria de Software II. El producto documentado corresponde al mismo sistema desarrollado como proyecto de Taller de Grado I, ajustado a una presentacion academica mas amplia que incorpora empresa de software, calidad, herramientas CASE, aspectos legales, infraestructura, mercado, pruebas, marketing, puesta en marcha y entrega como producto.



# Resumen ejecutivo

Wireless HeatMapper es un sistema integrado para relevar, procesar, analizar y publicar resultados de cobertura WiFi en ambientes interiores mediante mapas de calor. El proyecto se presenta para la materia Ingenieria de Software II como producto de Team 24 Software y toma como cliente del caso a Bulldog Tech., empresa que requiere mejorar la forma en que documenta y justifica sus decisiones tecnicas sobre redes inalambricas.

## Sintesis del problema

El proceso tradicional de site survey usado por Bulldog Tech. depende en gran medida de la experiencia del tecnico, de herramientas aisladas y de consolidacion posterior manual. Las mediciones de intensidad de senal, la ubicacion de cada lectura sobre el plano, la interpretacion de zonas criticas y la entrega de resultados al cliente no quedan integradas en una unica fuente de verdad. Esta situacion genera riesgo de perdida de datos, dificulta la trazabilidad tecnica, aumenta el retrabajo y limita la capacidad de demostrar con evidencia objetiva por que una zona requiere ajuste, reemplazo o reubicacion de puntos de acceso.

El problema no se reduce a capturar valores RSSI. La necesidad real es convertir mediciones de campo en informacion tecnica verificable, visual y compartible. Sin un flujo integrado, Bulldog Tech. no puede mantener historiales consistentes por proyecto, comparar escenarios de cobertura ni entregar al cliente final una visualizacion clara del estado de su red.

## Sintesis de la solucion

La solucion propuesta es un sistema 100 % en linea compuesto por aplicacion movil Android, backend REST, base de datos central, modulo de inteligencia artificial y plataforma web. La aplicacion movil opera como cliente delgado para tecnicos de campo; el backend concentra la logica de negocio, seguridad, persistencia, interpolacion y procesamiento de propuestas; PostgreSQL actua como unica fuente de verdad; y la web cubre la administracion interna y la publicacion segura de resultados al cliente.

El sistema permite registrar proyectos, asociarlos a clientes, importar y calibrar planos, marcar puntos de medicion, capturar redes WiFi cercanas, generar mapas de calor, administrar conjuntos de puntos de acceso, comparar propuestas actuales y derivadas por IA, y publicar resultados mediante un enlace unico. Los criterios tecnicos conservan los umbrales definidos para el producto: RSSI < -90 dBm como zona muerta, objetivo de diseno >= -70 dBm y consideracion del throttling de Android >= 8.0 de 4 escaneos cada 2 minutos.

## Alcance del producto

El alcance funcional vigente cubre ocho dominios principales: autenticacion y administracion de usuarios, gestion de clientes, gestion de proyectos, carga y calibracion de planos, captura de mediciones WiFi en campo, generacion de mapas de calor, optimizacion asistida por IA y portal web para clientes. La operacion se organiza alrededor de proyectos de cobertura, cada uno con sus planos, mediciones, conjuntos de puntos de acceso, heatmaps y publicaciones.

Quedan fuera del alcance vigente la sincronizacion diferida, la persistencia local de dominio en el dispositivo movil, la medicion activa de ancho de banda con herramientas externas, el posicionamiento automatico del tecnico por SLAM o triangulacion inercial, el diagnostico persistido como modulo independiente y la generacion de reportes PDF como flujo principal. La entrega prioriza visualizacion interactiva, trazabilidad en backend y publicacion web controlada.

## Valor para Bulldog Tech.

Para Bulldog Tech., Wireless HeatMapper aporta valor operativo y comercial. En lo operativo, estandariza el trabajo de campo, reduce la dependencia de registros manuales, centraliza evidencias y facilita revisar mediciones historicas de cada proyecto. En lo tecnico, permite interpretar cobertura sobre planos calibrados, identificar zonas de senal degradada y comparar escenarios de puntos de acceso con criterios objetivos. En lo comercial, mejora la presentacion de resultados ante clientes finales mediante un portal visual, accesible por enlace, sin depender de archivos estaticos o explicaciones informales.

El producto tambien fortalece la capacidad de la empresa para escalar servicios de consultoria WiFi. Al convertir cada proyecto en un conjunto de datos trazables, Bulldog Tech. puede justificar recomendaciones de infraestructura, documentar decisiones y ofrecer un servicio mas profesional en sectores como oficinas, instituciones educativas, hoteles, comercios y ambientes industriales.

## Componentes entregados

| Componente | Sintesis de entrega |
| ---------- | ------------------- |
| Aplicacion movil Android | Cliente Flutter para tecnicos de campo, con autenticacion, gestion de proyectos, planos, captura de mediciones y visualizacion de resultados. |
| Backend REST | API FastAPI con reglas de negocio, autenticacion, autorizacion, endpoints de dominio, procesamiento de heatmaps y servicios de IA. |
| Base de datos central | Persistencia PostgreSQL para usuarios, clientes, proyectos, planos, lecturas, mapas de calor, conjuntos de AP y publicaciones. |
| Plataforma web administrativa | Interfaz React para administradores, gestion de usuarios, clientes, proyectos, propuestas, publicaciones y supervision general. |
| Portal de cliente | Vista web por enlace unico para consultar resultados publicados sin instalar la aplicacion movil ni acceder al panel administrativo. |
| Infraestructura de despliegue | Contenedores, reverse proxy, configuracion de ambientes, automatizacion y criterios de operacion en linea. |
| Documentacion academica | PAPS, modelos, manual de calidad, herramientas CASE, aspectos legales, infraestructura, mercado, pruebas, marketing, puesta en marcha y producto final. |

## Modalidad operativa

La modalidad operativa oficial es 100 % en linea. Esto significa que la aplicacion movil no conserva estado de dominio entre sesiones ni implementa base de datos local para proyectos, planos o mediciones. Cada accion relevante se ejecuta contra el backend mediante servicios REST autenticados, y toda informacion persistente queda registrada en PostgreSQL.

Este enfoque simplifica la trazabilidad, evita conflictos de sincronizacion y garantiza que administradores, tecnicos y clientes consulten informacion consistente. Cuando no existe conectividad, la operacion de dominio no se simula como trabajo offline; el sistema debe informar la condicion y reanudar el flujo cuando el backend vuelva a estar disponible.

## Cobertura de los doce puntos

La documentacion integral se estructura alrededor de los doce puntos solicitados por la materia. Cada punto cumple una funcion distinta dentro de la evaluacion: algunos describen el producto, otros formalizan el proceso de desarrollo, la empresa de software, la calidad, la validacion, la comercializacion y la puesta en marcha.

| Punto | Eje documental | Contenido esperado |
| ----- | -------------- | ------------------ |
| 1 | PAPS adaptado a SW2 | Problema, situacion deseada, objetivos, alcance, restricciones, requerimientos, stack, cronograma y criterios de aceptacion. |
| 2 | Modelos de desarrollo | Modelos de contexto, arquitectura, datos y logica, con trazabilidad entre casos de uso, componentes, entidades y flujos. |
| 3 | Manual de garantia de calidad | Politica institucional de calidad, roles, procesos, registros, metricas, auditorias, no conformidades y mejora continua. |
| 4 | Herramientas CASE | Uso de modelado UML, navegabilidad entre diagramas, trazabilidad y evidencias de soporte al diseno. |
| 5 | Aspectos legales | Apertura de empresa de software en Bolivia, obligaciones tributarias, contratos, propiedad intelectual y proteccion de datos. |
| 6 | Infraestructura tecnologica | Gestion de repositorio, ramas, CI/CD, contenedores, Nginx, base de datos, ambientes, seguridad, monitoreo y backups. |
| 7 | Sitio web de la empresa | Presencia publica de Team 24 Software, servicios, producto, descargas, soporte, contacto y mantenimiento de contenido. |
| 8 | Estudio de mercado | Segmentos objetivo, competidores, propuesta de valor, precios, monetizacion, costos, proyeccion y riesgos comerciales. |
| 9 | Plan de pruebas | Estrategia de pruebas por niveles, caja blanca, rendimiento, seguridad, checklists y criterios de aceptacion. |
| 10 | Marketing | Objetivos, publicos, posicionamiento, canales, calendario, piezas promocionales, metricas y presupuesto inicial. |
| 11 | Puesta en marcha | Comparacion cloud, costos, decision de plataforma, licencias, tiendas, terminos, privacidad y adopcion asistida. |
| 12 | Software como producto | Componentes finales, funcionalidades, accesos publicos, releases, versionado, soporte, criterios de entrega y evidencias. |

## Cierre ejecutivo

Wireless HeatMapper integra ingenieria de software, redes inalambricas, visualizacion espacial e inteligencia artificial aplicada en un producto operable en linea. Su valor principal consiste en transformar un proceso tecnico manual en un flujo digital trazable, verificable y presentable para el cliente final. La documentacion de SW2 amplia esa entrega tecnica con una vision institucional completa: empresa productora, calidad, legalidad, mercado, pruebas, marketing, despliegue y sostenibilidad del producto.


# Plan Aplicado a Proyecto de Software

## Identificacion

**Proyecto:** Wireless HeatMapper  
**Empresa de software:** Team 24 Software  
**Cliente:** Bulldog Tech.  
**Tipo de solucion:** Sistema integrado en linea con aplicacion movil, backend REST, modulo de IA y plataforma web.  
**Modalidad:** 100 % en linea.  

## Problema

Bulldog Tech. requiere mejorar el proceso de relevamiento de cobertura WiFi en interiores. El metodo manual actual fragmenta la captura, la ubicacion espacial de mediciones, la generacion de mapas de calor y la comunicacion de resultados al cliente. Esa fragmentacion reduce la confiabilidad tecnica del entregable y eleva el tiempo de consolidacion posterior al trabajo de campo.

## Situacion deseada

El tecnico debe poder ejecutar el ciclo de survey desde una aplicacion movil conectada al backend: crear proyectos, importar planos, calibrarlos, marcar puntos de medicion, capturar redes WiFi y generar mapas de calor. El administrador debe supervisar usuarios, clientes, proyectos y propuestas. El cliente final debe acceder a resultados publicados mediante portal web seguro sin recibir archivos manuales desactualizados.

## Objetivo general

Desarrollar un sistema en linea que permita capturar, procesar, analizar y compartir informacion de cobertura WiFi en interiores mediante mapas de calor, centralizando la informacion en backend y proporcionando visualizacion movil y web.

## Objetivos especificos

- Implementar autenticacion y administracion de usuarios, clientes y proyectos.
- Permitir carga y calibracion de planos.
- Registrar mediciones WiFi georreferenciadas sobre plano.
- Generar mapas de calor con criterios tecnicos de cobertura.
- Incorporar propuestas asistidas por IA para ubicacion o ajuste de puntos de acceso.
- Publicar resultados seleccionados al cliente mediante portal web.
- Mantener trazabilidad entre requerimientos, historias de usuario, modelos, pruebas y entregables.

## Alcance funcional

| Codigo | Requerimiento principal | Cobertura |
| ------ | ---------------------- | --------- |
| RP1 | Captura de senal WiFi en linea | Medicion RSSI, SSID, BSSID, canal y frecuencia desde Android. |
| RP2 | Mapeo sobre plano | Importacion, calibracion y puntos de medicion. |
| RP3 | Generacion de heatmap | Interpolacion backend y visualizacion de mapa. |
| RP5 | Optimizacion asistida por IA | Conjuntos de AP derivados y comparacion contra estado actual. |
| RP7 | Administracion de usuarios | Panel web para administradores. |
| RP8 | Persistencia centralizada | PostgreSQL como fuente de verdad. |
| RP9 | Portal de cliente | Enlace unico para consulta de resultados publicados. |

RP4 y RP6 se conservan como requerimientos historicos de analisis y reportes, pero su valor se atiende mediante visualizacion interactiva, metricas operativas y portal web, sin diagnostico persistido ni reporte PDF como flujo principal.

## Restricciones

- El cliente movil no implementa base de datos local de dominio.
- No existe sincronizacion diferida; toda operacion de negocio requiere backend.
- La persistencia central es PostgreSQL.
- La seguridad se basa en autenticacion, autorizacion por rol y control de propiedad de datos.
- Los criterios WiFi minimos son: RSSI < -90 dBm como zona muerta, objetivo de diseno >= -70 dBm y consideracion del throttling Android >= 8.0 de 4 escaneos cada 2 minutos.

## Stack tecnologico

| Componente | Tecnologia |
| ---------- | ---------- |
| App movil | Flutter / Dart, BLoC/Cubit, cliente REST. |
| Backend | Python, FastAPI, SQLAlchemy, Alembic. |
| Inteligencia artificial | Servicios Python para propagacion RF y propuesta de AP. |
| Base de datos | PostgreSQL 15+. |
| Web | React, TypeScript, Vite. |
| Infraestructura | Docker Compose, Nginx, TLS, GitHub Actions. |
| Modelado | UML 2.5+ con PlantUML y herramienta CASE. |

## Plan por sprints

| Sprint | Objetivo | Resultado |
| ------ | -------- | --------- |
| 0 | Definicion inicial e infraestructura | Repositorio, contenedores, backend base y CI. |
| 1 | Fundacion CRUD | Usuarios, clientes, proyectos, autenticacion y panel inicial. |
| 2 | Planos | Importacion y calibracion de planos. |
| 3 | Captura | Medicion WiFi en linea y puntos de medicion. |
| 4 | Heatmap | Conjuntos AP y mapas de calor backend. |
| 5 | IA | Propuestas derivadas y comparacion. |
| 6 | Portal cliente | Enlaces seguros y visualizacion externa. |

## Criterios generales de aceptacion

- Cada funcionalidad tiene criterios de aceptacion trazables.
- Cada incremento pasa por pruebas de desarrollador, QA y validacion del Product Owner.
- Cada endpoint protege autenticacion, rol y propiedad de datos.
- Las operaciones de campo persisten en backend sin depender de estado local.
- El producto final dispone de repositorio, frontend publicado y releases moviles.



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


# Manual institucional de calidad del software

## Proposito

El presente manual define el sistema institucional de gestion y aseguramiento de la calidad de Team 24 Software. Su alcance no se limita a un producto especifico: establece politicas, roles, procesos, registros, metricas, auditorias, tratamiento de no conformidades y mejora continua aplicables a todos los proyectos de software desarrollados por la empresa.

Wireless HeatMapper se considera el primer caso formal de aplicacion del manual, pero las reglas aqui descritas son corporativas y deben mantenerse para futuros productos, servicios de desarrollo, mantenimiento, soporte, consultoria e implementaciones para clientes.

## Marco normativo de referencia

El manual toma como referencia dos normas de calidad aplicables al desarrollo de software:

| Norma | Uso institucional en Team 24 Software |
| ----- | ------------------------------------- |
| ISO/IEC 90003 | Guia para aplicar principios de gestion de calidad ISO 9001 en organizaciones que adquieren, desarrollan, operan o mantienen software. Se adopta para organizar procesos, responsabilidades, control documental, gestion de requisitos, diseno, desarrollo, validacion, entrega y mejora. |
| IEEE 730 | Estructura de referencia para el plan de aseguramiento de calidad del software. Se adopta para definir actividades SQA, revisiones, auditorias, registros, metricas, control de no conformidades, gestion de riesgos y evidencia objetiva. |

La adopcion es proporcional al tamano de la empresa y al contexto academico-comercial de Team 24 Software. No implica certificacion formal, sino aplicacion disciplinada de practicas verificables y auditables.

## Identidad institucional

| Elemento | Definicion |
| -------- | ---------- |
| Empresa | Team 24 Software |
| Rubro | Desarrollo, integracion, despliegue y soporte de soluciones de software. |
| Enfoque | Productos web, moviles y backend orientados a procesos tecnicos verificables. |
| Cliente de referencia | Bulldog Tech., para el caso Wireless HeatMapper. |
| Eslogan | Software medible, verificable y alineado al cliente. |

## Mision

Desarrollar soluciones de software confiables, mantenibles, seguras y verificables, aplicando practicas de ingenieria, gestion de calidad y mejora continua para resolver necesidades reales de clientes mediante productos funcionales, documentados y sostenibles.

## Vision

Consolidarse como una empresa de software reconocida por entregar productos con trazabilidad completa, evidencia objetiva de calidad, seguridad operativa, cumplimiento documental y valor de negocio medible para sus clientes.

## Principios de calidad

Team 24 Software adopta los siguientes principios como base de su sistema de calidad:

- Orientacion al cliente y a los usuarios reales del software.
- Liderazgo tecnico con responsabilidades claras.
- Participacion activa del equipo en la prevencion de defectos.
- Enfoque basado en procesos, no en esfuerzos aislados.
- Decisiones sustentadas en datos, metricas y evidencia.
- Gestion preventiva de riesgos tecnicos, operativos y de seguridad.
- Mejora continua del producto, del proceso y de la organizacion.
- Trazabilidad entre requisitos, diseno, implementacion, pruebas y entrega.

## Politica de calidad

Team 24 Software se compromete a desarrollar, mantener y entregar software que satisfaga los requisitos acordados con el cliente, cumpla criterios tecnicos verificables y conserve evidencia documental suficiente para demostrar conformidad.

La calidad se gestiona desde el inicio de cada proyecto mediante requisitos claros, diseno trazable, control de cambios, revisiones tecnicas, pruebas por niveles, auditorias internas, gestion de no conformidades y mejora continua. Cada incremento entregable debe contar con evidencia proporcional a su riesgo, impacto y alcance.

La direccion de Team 24 Software es responsable de comunicar esta politica, revisarla periodicamente y asegurar que el equipo cuente con procedimientos, herramientas y criterios de aceptacion suficientes para cumplirla.

## Objetivos institucionales de calidad

| Objetivo | Metrica | Meta institucional |
| -------- | ------- | ------------------ |
| Asegurar requisitos verificables | Historias o requisitos con criterios de aceptacion definidos | 100 % antes de iniciar desarrollo |
| Mantener trazabilidad | Requisitos vinculados con diseno, codigo, pruebas y evidencias | 100 % de funcionalidades liberadas |
| Prevenir defectos criticos | Defectos criticos abiertos al liberar | 0 |
| Mejorar calidad tecnica | Cambios revisados, probados o validados por CI | 100 % de incrementos entregables |
| Asegurar pruebas suficientes | Pruebas obligatorias ejecutadas segun nivel de riesgo | 100 % antes de aprobacion |
| Controlar documentacion | Artefactos afectados actualizados | 100 % antes de cierre de sprint o release |
| Gestionar riesgos | Riesgos relevantes identificados con respuesta definida | 100 % de riesgos altos |
| Mejorar continuamente | Acciones de mejora registradas y verificadas | Al menos 1 por retrospectiva |

## Alcance del sistema de calidad

El sistema de calidad aplica a:

- Descubrimiento y gestion de necesidades del cliente.
- Definicion de alcance, requerimientos y criterios de aceptacion.
- Diseno funcional, tecnico, de datos, seguridad e infraestructura.
- Desarrollo de software backend, web, movil, integraciones y scripts.
- Pruebas unitarias, integracion, sistema, seguridad, rendimiento y aceptacion.
- Gestion de configuracion, ramas, versiones, dependencias y releases.
- Despliegue, puesta en marcha, soporte y mantenimiento.
- Documentacion tecnica, academica, comercial y operativa.
- Auditoria interna, no conformidades, acciones correctivas y mejora continua.

Quedan fuera del alcance del sistema de calidad las decisiones comerciales, legales o contractuales que no esten relacionadas con el cumplimiento del producto o servicio. Sin embargo, cuando dichas decisiones afecten requisitos, seguridad, datos, costos de operacion o soporte, deben registrarse como riesgos o restricciones del proyecto.

## Estructura organizacional y roles

| Rol | Responsabilidades de calidad |
| --- | ---------------------------- |
| Direccion tecnica | Aprobar arquitectura, releases, tecnologia base, decisiones de alto impacto y politica de calidad. |
| Product Owner | Representar valor de negocio, priorizar backlog, aceptar o rechazar incrementos y validar criterios de aceptacion. |
| Scrum Master | Facilitar el proceso, remover impedimentos, proteger la Definition of Done, registrar retrospectivas y dar seguimiento a mejoras. |
| Responsable de calidad | Mantener este manual, coordinar auditorias internas, revisar registros, controlar no conformidades y reportar metricas. |
| Responsable de configuracion | Administrar repositorio, ramas, versionado, dependencias, ambientes, artefactos liberados y evidencias de build. |
| Desarrollador | Implementar con criterios de calidad, ejecutar pruebas propias, documentar decisiones relevantes y corregir defectos asignados. |
| QA rotativo | Disenar y ejecutar pruebas, intentar quebrar el incremento, revisar bordes, seguridad, rendimiento y evidencia de aceptacion. |
| Responsable de seguridad | Revisar autenticacion, autorizacion, secretos, exposicion de datos, dependencias vulnerables y configuracion de despliegue. |
| Cliente o representante | Revisar entregables, confirmar aceptacion funcional, informar desviaciones y validar que el producto resuelva la necesidad acordada. |

En equipos pequenos, una persona puede asumir mas de un rol, pero las responsabilidades no desaparecen. Cuando exista conflicto entre quien desarrolla y quien valida, se debe registrar la validacion cruzada posible o la limitacion existente.

## Mapa de procesos institucionales

El sistema de calidad se organiza en tres grupos de procesos: direccion, realizacion del software y soporte.

| Grupo | Proceso | Proposito |
| ----- | ------- | --------- |
| Direccion | Planificacion de calidad | Definir objetivos, politicas, alcance, roles, riesgos y criterios de aceptacion. |
| Direccion | Revision de direccion | Evaluar metricas, auditorias, no conformidades, satisfaccion del cliente y acciones de mejora. |
| Realizacion | Gestion de requisitos | Capturar, analizar, priorizar, validar y controlar cambios sobre requisitos. |
| Realizacion | Diseno y arquitectura | Definir estructura del sistema, modelo de datos, integraciones, seguridad y restricciones tecnicas. |
| Realizacion | Desarrollo | Implementar funcionalidades segun estandares, revisiones, pruebas y control de configuracion. |
| Realizacion | Verificacion | Comprobar que el software cumple especificaciones mediante pruebas, revisiones y analisis estatico. |
| Realizacion | Validacion | Confirmar con el cliente o PO que el producto satisface la necesidad de negocio. |
| Realizacion | Liberacion y despliegue | Preparar versiones, migraciones, configuracion, evidencias, changelog y puesta en marcha. |
| Soporte | Gestion de configuracion | Controlar repositorio, ramas, versiones, ambientes, dependencias y artefactos. |
| Soporte | Gestion de riesgos | Identificar, analizar, responder y monitorear riesgos tecnicos, operativos y de negocio. |
| Soporte | Gestion de no conformidades | Registrar desviaciones, analizar causa, corregir, prevenir recurrencia y verificar cierre. |
| Soporte | Mejora continua | Convertir metricas, defectos, auditorias y retrospectivas en acciones de mejora verificables. |

## Procedimientos de calidad por ciclo de vida

### Inicio de proyecto

- Identificar cliente, problema, objetivos, alcance, restricciones y criterios de exito.
- Registrar interesados, roles y responsabilidades.
- Definir riesgos iniciales y supuestos.
- Seleccionar herramientas de gestion, repositorio, comunicacion y documentacion.
- Establecer Definition of Done inicial y estrategia de pruebas.

### Gestion de requisitos

- Cada requisito debe tener origen, descripcion, prioridad, criterio de aceptacion y responsable de validacion.
- Los requisitos funcionales deben conectarse con casos de uso, historias o tareas implementables.
- Los requisitos no funcionales deben expresarse como condiciones verificables.
- Todo cambio de alcance debe evaluar impacto en tiempo, costo, pruebas, documentacion y riesgos.
- Los requisitos eliminados o diferidos deben conservar justificacion para evitar reintroducciones accidentales.

### Diseno y arquitectura

- El diseno debe representar la solucion antes de codificar componentes de alto impacto.
- Los modelos deben conservar consistencia con el alcance aprobado.
- Las decisiones arquitectonicas relevantes deben registrar contexto, alternativas, decision y consecuencia.
- El diseno debe considerar seguridad, mantenibilidad, despliegue, pruebas y operacion.
- Los cambios sobre arquitectura, modelo de datos o integraciones deben pasar por revision tecnica.

### Desarrollo

- El codigo debe implementarse en ramas o cambios controlados.
- Cada incremento debe compilar, ejecutarse o construirse segun corresponda.
- El desarrollador debe ejecutar pruebas locales razonables antes de solicitar validacion.
- Las reglas de negocio deben permanecer en componentes apropiados, evitando duplicacion innecesaria.
- Los secretos, claves y credenciales no deben versionarse.
- Los errores deben manejarse con mensajes controlados y sin exponer informacion sensible.

### Revision tecnica

- Las revisiones verifican legibilidad, mantenibilidad, seguridad, cobertura de pruebas, consistencia con requisitos y efecto sobre documentacion.
- Para cambios pequenos, la revision puede ser ejecutada por el propio responsable con evidencia de pruebas.
- Para cambios de alto impacto, se requiere revision cruzada o aprobacion de direccion tecnica.
- Todo hallazgo critico debe resolverse antes de integrar o liberar.

### Verificacion y pruebas

- La verificacion confirma que el software fue construido correctamente respecto a sus especificaciones.
- Deben aplicarse pruebas proporcionales al riesgo: unidad, integracion, sistema, seguridad, rendimiento, regresion y pruebas manuales.
- Cada defecto encontrado debe registrarse con severidad, pasos de reproduccion, resultado esperado, resultado obtenido y evidencia.
- La correccion de un defecto debe incluir reejecucion de la prueba afectada y evaluacion de no regresion.

### Validacion con cliente

- La validacion confirma que el software construido resuelve la necesidad del usuario o cliente.
- Debe ejecutarse sobre incrementos demostrables, no solamente sobre documentos.
- La aceptacion puede ser total, parcial o rechazada, pero siempre debe quedar registrada.
- Las observaciones del cliente pueden convertirse en defectos, cambios de alcance, mejoras o riesgos.

### Liberacion y despliegue

- Toda liberacion debe estar asociada a una version identificable del repositorio.
- Deben registrarse cambios incluidos, pruebas ejecutadas, defectos abiertos aceptados y riesgos residuales.
- Las migraciones, variables de entorno, dependencias y pasos de despliegue deben estar documentados.
- La liberacion no debe exponer datos sensibles, credenciales ni configuraciones inseguras.
- El responsable de configuracion conserva evidencia de build, despliegue y rollback posible.

### Operacion y mantenimiento

- Los incidentes reportados por usuarios se registran y clasifican por severidad.
- Las correcciones se priorizan segun impacto operativo, seguridad y compromiso contractual.
- Los cambios correctivos siguen el mismo control de calidad proporcional al riesgo.
- Las metricas de soporte alimentan retrospectivas y revisiones de direccion.

## Registros obligatorios de calidad

| Registro | Responsable | Momento de generacion | Retencion minima |
| -------- | ----------- | --------------------- | ---------------- |
| Backlog o lista de requisitos | Product Owner | Inicio y refinamiento continuo | Vida del proyecto |
| Criterios de aceptacion | Product Owner | Antes de desarrollo | Vida del proyecto |
| Matriz de trazabilidad | Responsable de calidad | Al cerrar incremento o release | Vida del proyecto |
| Decisiones tecnicas | Direccion tecnica | Cuando exista decision relevante | Vida del proyecto |
| Evidencia de pruebas | QA rotativo / desarrollador | Antes de validar o liberar | Vida del proyecto |
| Reporte de defectos | QA rotativo | Al detectar desviacion | Vida del proyecto |
| Registro de no conformidad | Responsable de calidad | Al confirmar incumplimiento | Vida del proyecto |
| Accion correctiva o preventiva | Responsable asignado | Despues de analizar causa | Hasta cierre y revision |
| Acta de Sprint Review o aceptacion | Product Owner | Al validar incremento | Vida del proyecto |
| Retrospectiva | Scrum Master | Al cerrar ciclo | Vida del proyecto |
| Auditoria interna | Responsable de calidad | Por sprint o antes de release | Vida del proyecto |
| Registro de version o release | Responsable de configuracion | Al liberar | Vida util del producto |
| Inventario de riesgos | Scrum Master | Inicio y seguimiento continuo | Vida del proyecto |

Los registros pueden mantenerse como documentos Markdown, issues, tableros, actas, reportes de CI, commits, capturas, releases o evidencias exportadas, siempre que sean localizables, fechados y vinculables al incremento correspondiente.

## Metricas de calidad

Team 24 Software usa metricas para tomar decisiones y no como mecanismo punitivo. La interpretacion debe considerar contexto, complejidad y riesgo.

| Categoria | Metrica | Formula o criterio | Frecuencia |
| --------- | ------- | ------------------ | ---------- |
| Requisitos | Cobertura de aceptacion | Requisitos con criterios / requisitos totales | Por sprint |
| Trazabilidad | Cobertura trazada | Elementos liberados con vinculo a requisito y prueba / elementos liberados | Por release |
| Defectos | Densidad de defectos | Defectos confirmados / incremento o modulo | Por sprint |
| Severidad | Defectos criticos abiertos | Conteo de defectos criticos no cerrados | Antes de release |
| Pruebas | Ejecucion de pruebas obligatorias | Pruebas ejecutadas / pruebas planificadas | Por sprint |
| Automatizacion | Cobertura de pruebas automatizadas | Pruebas automatizadas relevantes / pruebas repetibles | Por release |
| Estabilidad | Tasa de regresion | Defectos reabiertos o inducidos / defectos cerrados | Por sprint |
| Entrega | Cumplimiento de Definition of Done | Items DoD cumplidos / items DoD aplicables | Por incremento |
| Seguridad | Hallazgos de seguridad abiertos | Conteo por severidad | Por release |
| Mantenimiento | Tiempo medio de correccion | Tiempo desde registro hasta cierre de defecto | Mensual o por sprint |
| Satisfaccion | Aceptacion del PO o cliente | Incrementos aceptados / incrementos presentados | Por review |
| Mejora | Acciones cerradas | Acciones de mejora cerradas / acciones comprometidas | Por retrospectiva |

## Auditoria interna de calidad

La auditoria interna verifica de forma independiente que los procesos definidos se cumplen y que existe evidencia objetiva de conformidad. Debe ejecutarse al menos al cierre de cada sprint relevante o antes de una liberacion externa.

### Alcance minimo de auditoria

- Trazabilidad entre requisitos, historias, diseno, implementacion y pruebas.
- Cumplimiento de Definition of Done.
- Estado de pruebas automatizadas y manuales.
- Defectos abiertos y justificacion de riesgos residuales.
- Cumplimiento de controles de seguridad y configuracion.
- Estado de documentacion afectada.
- Evidencia de revision tecnica y aceptacion del PO o cliente.
- Seguimiento de no conformidades y acciones correctivas previas.

### Resultado de auditoria

| Resultado | Criterio |
| --------- | -------- |
| Conforme | El proceso o entregable cumple requisitos y conserva evidencia suficiente. |
| Observacion | Existe una debilidad que no incumple aun, pero puede generar defecto o riesgo. |
| No conformidad menor | Incumplimiento localizado sin impacto critico sobre entrega, seguridad o cliente. |
| No conformidad mayor | Incumplimiento que afecta requisitos, seguridad, trazabilidad, liberacion o confianza del cliente. |

El reporte de auditoria debe incluir fecha, auditor, alcance, hallazgos, evidencias revisadas, severidad, responsables, acciones requeridas y fecha objetivo de cierre.

## Gestion de no conformidades

Una no conformidad ocurre cuando un producto, proceso, registro o entregable incumple un requisito, criterio de aceptacion, politica de calidad, control obligatorio o compromiso aprobado.

### Clasificacion

| Severidad | Descripcion | Ejemplos |
| --------- | ----------- | -------- |
| Critica | Impide liberar, compromete seguridad, datos o cumplimiento contractual. | Exposicion de credenciales, perdida de datos, acceso no autorizado, funcionalidad principal inutilizable. |
| Alta | Afecta funcionalidad importante o genera riesgo operativo serio. | Requisito clave incompleto, prueba obligatoria fallida, migracion inconsistente. |
| Media | Afecta uso normal, mantenibilidad o evidencia, pero tiene alternativa temporal. | Documentacion incompleta, validacion parcial, defecto funcional acotado. |
| Baja | Desviacion menor sin impacto operativo inmediato. | Error de formato, inconsistencia menor, mejora de claridad. |

### Registro minimo

Cada no conformidad debe registrar:

- Identificador unico.
- Fecha de deteccion.
- Proyecto o proceso afectado.
- Descripcion objetiva.
- Requisito, politica o control incumplido.
- Severidad.
- Evidencia.
- Responsable asignado.
- Analisis de causa raiz.
- Accion correctiva.
- Accion preventiva, cuando aplique.
- Fecha objetivo.
- Estado.
- Evidencia de verificacion de cierre.

### Flujo de tratamiento

| Paso | Actividad | Responsable |
| ---- | --------- | ----------- |
| 1 | Detectar desviacion y conservar evidencia | Cualquier integrante |
| 2 | Clasificar severidad e impacto | Responsable de calidad |
| 3 | Asignar responsable y fecha objetivo | Scrum Master / direccion tecnica |
| 4 | Analizar causa raiz | Responsable asignado |
| 5 | Ejecutar accion correctiva | Responsable asignado |
| 6 | Definir accion preventiva si existe riesgo de recurrencia | Responsable de calidad |
| 7 | Verificar cierre con evidencia | QA rotativo o responsable de calidad |
| 8 | Registrar aprendizaje en retrospectiva si corresponde | Scrum Master |

Una no conformidad critica o alta bloquea la liberacion salvo aceptacion explicita de direccion tecnica y Product Owner, con registro del riesgo residual.

## Control de cambios

Todo cambio relevante debe evaluarse antes de incorporarse. El control de cambios aplica a requisitos, diseno, arquitectura, datos, seguridad, infraestructura, alcance, releases y documentacion formal.

| Tipo de cambio | Evaluacion requerida |
| -------------- | -------------------- |
| Requisito funcional | Impacto en backlog, casos de uso, pruebas, estimacion y aceptacion. |
| Requisito no funcional | Impacto en rendimiento, seguridad, disponibilidad, mantenibilidad y operacion. |
| Modelo de datos | Impacto en migraciones, integridad, compatibilidad y respaldo. |
| Arquitectura | Impacto en componentes, despliegue, dependencias, riesgos y costos. |
| Seguridad | Impacto en autenticacion, autorizacion, secretos, datos personales y auditoria. |
| Infraestructura | Impacto en ambientes, despliegue, monitoreo, backups y rollback. |
| Documentacion | Impacto en trazabilidad, manuales, planes, anexos y evidencias. |

Los cambios aprobados deben quedar vinculados al commit, tarea, historia, issue, acta o documento que los justifique.

## Gestion de configuracion

La gestion de configuracion asegura que los elementos del software sean identificables, reproducibles y controlados.

| Elemento | Control esperado |
| -------- | ---------------- |
| Codigo fuente | Versionado en Git, commits claros, ramas controladas y cambios revisables. |
| Dependencias | Versiones declaradas, actualizacion controlada y revision de vulnerabilidades. |
| Configuracion | Variables de entorno documentadas y secretos excluidos del repositorio. |
| Base de datos | Migraciones trazables, respaldos y procedimientos de restauracion. |
| Artefactos | Builds, releases, imagenes o paquetes asociados a version del repositorio. |
| Documentos | Version, fecha, responsable y coherencia con alcance vigente. |
| Diagramas | Fuente editable conservada y salida visual regenerable cuando aplique. |

## Criterios de liberacion

Un incremento o version puede liberarse cuando cumple las siguientes condiciones:

- Requisitos incluidos tienen criterios de aceptacion cumplidos o excepciones aprobadas.
- No existen defectos criticos abiertos.
- Las pruebas obligatorias pasaron o los riesgos residuales fueron aceptados formalmente.
- La documentacion afectada fue actualizada.
- La version del repositorio esta identificada.
- La configuracion de despliegue no expone secretos ni datos sensibles.
- El PO o cliente valido el incremento segun el alcance acordado.
- Las no conformidades mayores relacionadas con la entrega estan cerradas o aceptadas con plan de mitigacion.

## Mejora continua

La mejora continua convierte la experiencia del equipo en acciones verificables. No se limita al codigo: tambien abarca requisitos, comunicacion, estimacion, pruebas, documentacion, seguridad, infraestructura, soporte y relacion con el cliente.

### Fuentes de mejora

- Retrospectivas de sprint.
- Auditorias internas.
- No conformidades y defectos recurrentes.
- Incidentes de operacion.
- Comentarios del cliente o usuarios.
- Metricas de calidad.
- Revisiones tecnicas.
- Riesgos materializados.

### Ciclo de mejora

| Etapa | Actividad |
| ----- | --------- |
| Identificar | Detectar oportunidad a partir de evidencia o experiencia del equipo. |
| Analizar | Determinar causa, impacto, urgencia y alternativa de solucion. |
| Planificar | Definir accion, responsable, fecha objetivo y metrica de verificacion. |
| Ejecutar | Implementar la accion aprobada. |
| Verificar | Comprobar si la accion redujo el problema o mejoro el resultado. |
| Estandarizar | Incorporar el aprendizaje en procesos, plantillas, checklists o Definition of Done. |

Cada retrospectiva debe producir al menos una accion de mejora. Si una accion no se cierra, debe mantenerse visible hasta ser completada, replanteada o descartada con justificacion.

## Aplicacion inicial en Wireless HeatMapper

Para Wireless HeatMapper, este manual se aplica de la siguiente forma:

| Area | Aplicacion concreta |
| ---- | ------------------- |
| Requisitos | Historias, casos de uso y requerimientos principales deben conservar trazabilidad. |
| Diseno | Modelos de contexto, arquitectura, datos y logica deben mantenerse coherentes con la modalidad 100 % en linea. |
| Desarrollo | Backend FastAPI, web React y app Flutter deben seguir control de configuracion, pruebas y revision tecnica. |
| Pruebas | El plan de pruebas define niveles, tecnicas, rendimiento, seguridad y criterios de cierre. |
| Seguridad | Autenticacion, autorizacion por roles, proteccion de datos y secretos excluidos del repositorio son controles obligatorios. |
| Entrega | Cada release debe vincularse a version, evidencias, cambios incluidos y validacion del PO. |
| Cliente | Bulldog Tech. valida que el producto resuelva el flujo de relevamiento, analisis y publicacion de cobertura WiFi. |

## Revision del manual

Este manual debe revisarse cuando ocurra cualquiera de las siguientes situaciones:

- Inicio de un nuevo proyecto institucional.
- Cambio relevante de metodologia, tecnologia o estructura del equipo.
- Auditoria con no conformidad mayor.
- Incidente de seguridad o perdida de datos.
- Cierre de release principal.
- Solicitud de direccion tecnica, Product Owner o cliente.

La revision debe registrar version, fecha, responsable, motivo del cambio y resumen de modificaciones. El objetivo no es aumentar burocracia, sino mantener un sistema de calidad util, proporcional y verificable.


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


# Aspectos legales para apertura de empresa de software en Bolivia

## Enfoque

Team 24 Software se plantea como una empresa de desarrollo de software que opera en Bolivia y presta servicios tecnologicos a clientes empresariales. Para fines academicos no se ejecuta la apertura real de la empresa, pero se documentan los pasos que deberian cumplirse para constituirla y operar formalmente.

## Tipo de organizacion recomendado

Para una empresa con dos o mas socios se recomienda una Sociedad de Responsabilidad Limitada (S.R.L.), porque separa el patrimonio de la empresa del patrimonio personal de los socios y permite formalizar participaciones. Para un emprendimiento individual podria utilizarse empresa unipersonal, aunque con menor separacion patrimonial.

## Registro de comercio

El registro de comercio en Bolivia es administrado por el Servicio Plurinacional de Registro de Comercio (SEPREC). Aunque en clases se mencione FUNDEMPRESA como referencia historica, la entidad vigente para los tramites de registro comercial es SEPREC.

Pasos generales:

1. Definir razon social, tipo societario, actividad economica y domicilio.
2. Elaborar escritura de constitucion, estatutos y poderes cuando corresponda.
3. Ingresar al portal de tramites de SEPREC.
4. Llenar el formulario virtual de inscripcion.
5. Realizar el pago correspondiente.
6. Atender observaciones si existieran.
7. Obtener la matricula de comercio con codigo de validacion.

Para empresa unipersonal, SEPREC informa que el tramite utiliza formulario virtual, pago en plataforma, analisis legal y emision de Matricula de Comercio, con costo referencial de Bs 130 y plazo de 24 horas desde el siguiente dia habil al pago, sujeto a validacion de la entidad.

## NIT y obligaciones tributarias

El Numero de Identificacion Tributaria identifica a la empresa ante el Servicio de Impuestos Nacionales. Para sociedades registradas en SEPREC, el NIT coincide con la matricula de comercio y la razon social debe coincidir entre SEPREC y SIN.

Obligaciones tributarias principales:

| Concepto | Aplicacion |
| -------- | ---------- |
| IVA | Impuesto al Valor Agregado por operaciones facturadas. |
| IT | Impuesto a las Transacciones. |
| IUE | Impuesto a las Utilidades de las Empresas. |
| Facturacion | Emision de factura segun regimen aplicable. |
| Registros contables | Libros, balances y declaraciones segun normativa tributaria. |

La empresa debe contar con apoyo contable para clasificar actividades, registrar obligaciones periodicas y evitar contingencias por facturacion o impuestos.

## Patente municipal

La actividad economica requiere registro o empadronamiento municipal segun jurisdiccion. En Santa Cruz de la Sierra existen tramites para empadronamiento de patente municipal a la actividad economica para contribuyente natural y juridico. La empresa debe verificar requisitos vigentes del Gobierno Autonomo Municipal correspondiente, domicilio legal, actividad declarada y condiciones de funcionamiento.

## Derechos de autor del software

El software puede registrarse ante el Servicio Nacional de Propiedad Intelectual (SENAPI), en la Direccion de Derecho de Autor y Derechos Conexos. SENAPI reconoce programas de computacion como obras registrables y solicita, entre otros requisitos, carta o memorial, cedulas de identidad, formulario, comprobantes de pago y soporte material del programa. Para aplicaciones web se puede adjuntar video demostrativo y descripcion del programa.

El registro es declarativo y fortalece la seguridad juridica sobre autoria y titularidad, aunque la obra nace protegida desde su creacion.

## Contratos y documentos legales operativos

Team 24 Software debe preparar:

- Contrato de prestacion de servicios o licencia SaaS.
- Acuerdo de niveles de servicio si existe compromiso operativo.
- Terminos y condiciones de uso.
- Politica de privacidad.
- Acuerdos de confidencialidad con clientes.
- Contratos laborales o de prestacion de servicios para colaboradores.
- Politica de propiedad intelectual sobre codigo, documentacion y modelos.

## Equipo administrativo requerido

Una empresa de software no se sostiene solo con desarrolladores. Debe contar con apoyo financiero, contable, tributario y legal para manejar facturacion, impuestos, contratos, propiedad intelectual, costos cloud, licencias y obligaciones laborales.

## Fuentes institucionales consultadas

- Servicio Plurinacional de Registro de Comercio (SEPREC): registro de comercio y tramites empresariales.
- Servicio de Impuestos Nacionales (SIN): NIT y requisitos tributarios.
- Servicio Nacional de Propiedad Intelectual (SENAPI): derecho de autor y registro de programas de computacion.
- Gobierno Autonomo Municipal de Santa Cruz de la Sierra: patente municipal para actividad economica.



# Infraestructura para la produccion de software

## Vision general

La infraestructura de Team 24 Software integra herramientas de gestion, desarrollo colaborativo, control de versiones, automatizacion, contenedores, despliegue, seguridad e inteligencia artificial aplicada al ciclo de desarrollo. El objetivo es producir software repetible, verificable y desplegable.

## Gestion del proyecto

El proyecto se gestiona con Scrum. El Product Backlog organiza historias de usuario; el Sprint Backlog descompone tareas; la Sprint Review valida incrementos; y la Retrospective captura mejoras. El tablero debe reflejar el estado real del sprint sin depender de avisos del docente.

## Desarrollo colaborativo

| Area | Herramienta o practica |
| ---- | ---------------------- |
| Repositorio | GitHub. |
| Versionado | Git con ramas por funcionalidad y rama principal protegida. |
| Revision | Pull requests o revision cruzada antes de integrar. |
| Convenciones | Commits descriptivos, trazabilidad con HU y criterios de aceptacion. |
| Documentacion | Markdown, PlantUML y documentos consolidados. |

## Control de configuracion

Los elementos bajo control incluyen:

- Codigo fuente backend, web y movil.
- Migraciones de base de datos.
- Configuracion Docker.
- Nginx y reglas de reverse proxy.
- Variables de entorno documentadas.
- Diagramas y documentos versionados.
- Releases moviles y artefactos de despliegue.

## Automatizacion CI/CD

El pipeline de integracion continua debe ejecutar:

- Pruebas backend con pytest.
- Analisis estatico backend con ruff.
- Lint y build del frontend.
- Analisis y pruebas de Flutter.
- Construccion de imagenes Docker.
- Publicacion controlada de artefactos.
- Despliegue a servidor productivo cuando el cambio sea aprobado.

## Contenedores y despliegue

El despliegue productivo se organiza con Docker Compose:

- `nginx`: terminacion TLS y reverse proxy.
- `backend`: API FastAPI y modulo IA.
- `web`: bundle React estatico.
- `db`: PostgreSQL con volumen persistente.

Nginx publica la API bajo `/api`, el panel web, el portal de cliente y los recursos estaticos. El backend no expone directamente la base de datos al exterior.

## Seguridad operativa

| Control | Aplicacion |
| ------- | ---------- |
| TLS | Trafico cifrado entre clientes y servidor. |
| JWT | Autenticacion de usuarios. |
| Roles | Administrador, tecnico y acceso publico controlado por token. |
| Ownership | Validacion de propiedad de proyectos y recursos. |
| Secretos | Variables de entorno y secretos de CI/CD. |
| Backups | Copias periodicas de PostgreSQL y archivos subidos. |
| Auditoria | Registro de accesos relevantes y releases. |

## Inteligencia artificial integrada al desarrollo

El equipo puede utilizar asistentes de IA en IDE para acelerar tareas de analisis, generacion de pruebas, refactorizacion, documentacion y revision. Su uso debe ser responsable: todo resultado generado por IA se revisa, prueba y adapta al criterio del equipo. La IA no reemplaza la validacion tecnica ni la responsabilidad profesional.

## Ambientes

| Ambiente | Uso | Reglas |
| -------- | --- | ------ |
| Local | Desarrollo individual | Datos de prueba y secretos locales. |
| Integracion | Validacion de ramas | Tests automatizados y base efimera. |
| Produccion | Acceso real del producto | TLS, backups, monitoreo y cambios aprobados. |



# Sitio web de la empresa

## 1. Proposito

El sitio web publico representa a **Team 24 Software** como empresa de desarrollo de software y servicios tecnologicos. Su funcion no se limita a promocionar Wireless HeatMapper: tambien comunica la identidad institucional, el catalogo de servicios, los canales de soporte, las descargas disponibles, las politicas publicas y el acceso a informacion confiable para clientes, docentes, usuarios tecnicos y visitantes externos.

El sitio se considera parte de la presencia digital de la empresa y debe mantenerse publicado en linea, disponible por HTTPS y alineado con la documentacion oficial del proyecto.

## 2. URL publica

La publicacion en linea del producto y sitio institucional se encuentra en:

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/>

Para presentaciones academicas, entregas documentales y demostraciones, esta URL puede acompanarse con codigo QR en anexos o material promocional. La URL no debe depender de `localhost`, tuneles temporales ni servidores personales apagables durante la evaluacion.

## 3. Objetivos del sitio

| Objetivo | Descripcion |
| -------- | ----------- |
| Presencia institucional | Presentar a Team 24 Software como proveedor responsable de soluciones de software. |
| Difusion comercial | Mostrar servicios ofrecidos, producto principal y beneficios para clientes potenciales. |
| Acceso al producto | Dirigir al usuario hacia Wireless HeatMapper, portal web, manuales y descargas moviles. |
| Soporte operativo | Centralizar preguntas frecuentes, canales de ayuda y reporte de incidentes. |
| Confianza y transparencia | Publicar politicas basicas de privacidad, terminos de uso, mantenimiento y contacto. |
| Atencion asistida | Incorporar un chatbot entrenado con informacion de empresa, producto y soporte. |

## 4. Publico objetivo

| Publico | Necesidad principal dentro del sitio |
| ------- | ------------------------------------ |
| Clientes empresariales | Entender que problema resuelve Wireless HeatMapper y como solicitar una demostracion. |
| Tecnicos de redes | Conocer el flujo de trabajo, descargas moviles, manuales y soporte tecnico. |
| Administradores de organizaciones | Revisar beneficios, seguridad, gestion de usuarios y portal de cliente. |
| Docentes y evaluadores | Ver evidencia de publicacion, alcance del producto y documentacion asociada. |
| Visitantes generales | Identificar a la empresa, servicios ofrecidos y formas de contacto. |

## 5. Mapa de secciones publicas

| Seccion | Contenido esperado | Resultado para el visitante |
| ------- | ------------------ | --------------------------- |
| Inicio | Mensaje principal de Team 24 Software, acceso a Wireless HeatMapper, llamada a demo y accesos rapidos. | Comprende en segundos que ofrece la empresa y donde ingresar. |
| Empresa | Quienes somos, mision, vision, valores, equipo Grupo 24 y enfoque de trabajo. | Reconoce la identidad institucional y responsabilidad del proveedor. |
| Servicios | Desarrollo web, aplicaciones moviles, backend/API, consultoria WiFi, analitica, IA aplicada y mantenimiento. | Identifica servicios contratables mas alla del producto principal. |
| Producto | Presentacion de Wireless HeatMapper, problema, usuarios, arquitectura general, beneficios y flujo de uso. | Entiende el valor del producto y su modalidad 100 % en linea. |
| Descargas | APK Android, manual de usuario, documentacion publica, notas de version y enlaces autorizados. | Obtiene recursos oficiales sin recurrir a archivos sueltos o enlaces informales. |
| Soporte | Preguntas frecuentes, guia para reportar incidentes, horarios de atencion, severidades y tiempos de respuesta. | Sabe como pedir ayuda y que informacion debe enviar. |
| Contacto | Formulario web, correo institucional del proyecto, telefono/WhatsApp autorizado y ubicacion referencial en Santa Cruz de la Sierra. | Puede solicitar informacion, soporte o una demostracion. |
| Chatbot | Asistente conversacional entrenado con informacion aprobada de empresa, producto, soporte y WiFi basico. | Recibe respuestas inmediatas y consistentes antes de escalar a soporte humano. |
| Politicas | Privacidad, terminos de uso, licenciamiento, cookies si aplican y mantenimiento de contenido. | Conoce reglas de uso, tratamiento de datos y alcance del servicio. |

## 6. Seccion Empresa

La seccion de empresa debe diferenciar claramente a **Team 24 Software** del cliente del caso **Bulldog Tech.**. Team 24 Software es la empresa desarrolladora del producto; Bulldog Tech. es el cliente real utilizado para contextualizar el problema de cobertura WiFi.

Contenido minimo:

- Nombre institucional: Team 24 Software.
- Equipo: Grupo 24 de Ingenieria de Software II.
- Ubicacion referencial: Santa Cruz de la Sierra, Bolivia.
- Mision: desarrollar soluciones digitales verificables, mantenibles y orientadas a necesidades reales de clientes.
- Vision: consolidarse como equipo proveedor de software tecnico para redes, analitica y procesos empresariales.
- Valores: calidad, trazabilidad, responsabilidad, seguridad, aprendizaje continuo y comunicacion clara.
- Perfil del equipo: desarrollo web, movil, backend, documentacion, pruebas y despliegue.

## 7. Seccion Servicios

La seccion de servicios presenta capacidades de Team 24 Software de forma comercial y verificable. No debe prometer servicios que no puedan explicarse o demostrarse.

| Servicio | Alcance |
| -------- | ------- |
| Desarrollo de software web | Sistemas administrativos, portales de cliente, dashboards y aplicaciones SPA. |
| Desarrollo movil | Aplicaciones Android con cliente delgado, consumo REST y experiencia orientada a campo. |
| Backend y APIs | APIs REST, autenticacion JWT, persistencia centralizada y documentacion OpenAPI. |
| Consultoria WiFi | Herramientas para relevamiento, interpretacion de RSSI, mapas de calor y evidencia tecnica. |
| Analitica e IA aplicada | Procesamiento de datos, recomendaciones asistidas y automatizacion de decisiones tecnicas. |
| DevOps basico | Contenedores, despliegue con Docker Compose, Nginx, HTTPS y CI/CD. |
| Mantenimiento y soporte | Correcciones, actualizaciones, respaldos, monitoreo y atencion de incidentes. |

Cada servicio debe incluir una descripcion breve, beneficios, ejemplos de entregables y un llamado a contacto.

## 8. Seccion Producto: Wireless HeatMapper

Wireless HeatMapper es el producto destacado del sitio. Debe presentarse como una solucion integrada para relevar, procesar y publicar resultados de cobertura WiFi en interiores mediante mapas de calor.

Contenido minimo:

- Problema que resuelve: mediciones WiFi fragmentadas, uso de planos impresos, transcripcion manual y baja trazabilidad.
- Usuarios principales: administrador, tecnico de campo y cliente final.
- Componentes: app movil Android, backend FastAPI, PostgreSQL, panel web, portal de cliente e IA backend.
- Modalidad: 100 % en linea, sin persistencia local de dominio ni sincronizacion diferida.
- Beneficios: evidencia centralizada, mapas de calor, comparacion de escenarios, portal por enlace y supervision organizacional.
- Criterios tecnicos visibles: objetivo de diseno RSSI >= -70 dBm y zona muerta RSSI < -90 dBm.

La seccion debe incluir enlaces hacia login, portal, manual de usuario, API/documentacion tecnica cuando corresponda y canal de soporte.

## 9. Seccion Descargas

La seccion de descargas debe publicar solamente recursos oficiales, versionados y revisados.

| Recurso | Contenido | Regla de publicacion |
| ------- | --------- | -------------------- |
| APK Android | Instalador de la app movil para tecnicos. | Publicar solo builds generados desde release o entrega aprobada. |
| Manual de usuario | Guia de uso para administrador, tecnico y cliente. | Mantener sincronizado con el incremento desplegado. |
| Notas de version | Cambios principales, correcciones y advertencias. | Una entrada por version liberada. |
| Documentacion publica | Enlaces a documentos aprobados para consulta externa. | No exponer secretos, credenciales ni datos privados. |
| Politicas | Terminos, privacidad, soporte y mantenimiento. | Revisar ante cada cambio de operacion o tratamiento de datos. |

Los enlaces rotos, archivos duplicados o versiones obsoletas deben retirarse o marcarse claramente como historicas.

## 10. Seccion Soporte

La seccion de soporte debe orientar al usuario antes de escalar a contacto humano. Debe contener:

- Preguntas frecuentes sobre acceso, roles, carga de planos, mediciones, heatmaps y portal cliente.
- Guia para reportar incidentes.
- Horario de atencion definido para el contexto academico o productivo.
- Clasificacion de severidad.
- Datos minimos que debe enviar el usuario.
- Flujo de escalamiento desde chatbot hacia soporte humano.

### 10.1. Clasificacion de incidentes

| Severidad | Ejemplo | Tiempo objetivo de primera respuesta |
| --------- | ------- | ------------------------------------ |
| Alta | Sistema publicado inaccesible, login general caido, perdida de acceso al portal. | 4 horas habiles. |
| Media | Error en carga de planos, falla en generacion de heatmap o descarga no disponible. | 1 dia habil. |
| Baja | Consulta funcional, ajuste de texto, duda de uso o solicitud de mejora. | 2 dias habiles. |

### 10.2. Datos requeridos para soporte

- Nombre y rol del usuario.
- Organizacion o cliente relacionado.
- URL o pantalla donde ocurre el problema.
- Pasos para reproducir el incidente.
- Fecha y hora aproximada.
- Captura de pantalla si corresponde.
- Version de APK o navegador utilizado.

## 11. Seccion Contacto

La seccion de contacto debe ofrecer canales claros y evitar informacion ambigua.

| Canal | Uso recomendado |
| ----- | --------------- |
| Formulario web | Solicitudes comerciales, demostraciones, soporte general y mensajes academicos. |
| Correo institucional | Comunicacion formal, seguimiento de incidentes y entrega de evidencias. |
| WhatsApp autorizado | Coordinacion rapida de demostraciones o soporte de baja complejidad. |
| Redes sociales | Difusion institucional, marketing y anuncios publicos. |
| Ubicacion referencial | Identificar la ciudad base de operacion sin publicar domicilios privados. |

El formulario debe pedir solo datos necesarios: nombre, correo, organizacion, motivo, mensaje y consentimiento para tratamiento de datos. No debe solicitar contrasenas, tokens, credenciales ni informacion sensible de redes internas.

## 12. Chatbot entrenado

El sitio debe incluir un chatbot propio o integrado que responda con informacion especifica de Team 24 Software y Wireless HeatMapper. No debe limitarse a redirigir a WhatsApp ni responder con texto generico sin contexto.

### 12.1. Objetivo del chatbot

Atender consultas frecuentes, reducir carga de soporte inicial y guiar al visitante hacia la seccion correcta del sitio. Cuando la consulta supere su alcance, debe escalar al formulario de contacto o al canal de soporte humano.

### 12.2. Base de conocimiento

| Tema | Contenido entrenado o documentado |
| ---- | --------------------------------- |
| Empresa | Identidad de Team 24 Software, equipo, servicios, ubicacion referencial y contacto. |
| Producto | Componentes de Wireless HeatMapper, roles, modalidad online, beneficios y limites. |
| Uso | Inicio de sesion, creacion de proyectos, carga de planos, mediciones, heatmaps y portal cliente. |
| Soporte | Como reportar incidentes, severidades, datos requeridos y tiempos de respuesta. |
| WiFi basico | RSSI, mapas de calor, objetivo >= -70 dBm, zona muerta < -90 dBm e interpretacion general. |
| Privacidad | Datos tratados, finalidad, roles de acceso y recomendaciones de seguridad. |
| Descargas | Donde obtener APK, manuales, notas de version y documentacion autorizada. |

### 12.3. Preguntas que debe responder

- Que es Team 24 Software?
- Que problema resuelve Wireless HeatMapper?
- Como ingreso al sistema publicado?
- Cual es la diferencia entre administrador, tecnico y cliente?
- Como se reporta un problema?
- Donde descargo la app movil?
- Que significa RSSI >= -70 dBm?
- Que significa RSSI < -90 dBm?
- Como se comparte un proyecto con un cliente?
- Que datos trata el sistema?

### 12.4. Limites y seguridad del chatbot

El chatbot debe aplicar las siguientes reglas:

- No inventar precios, contratos, credenciales ni compromisos comerciales no aprobados.
- No solicitar contrasenas, tokens, claves WiFi reales ni secretos de infraestructura.
- No entregar datos privados de clientes, usuarios, planos o proyectos.
- No reemplazar soporte humano en incidentes criticos.
- Indicar cuando una respuesta requiere validacion del equipo.
- Usar lenguaje claro, breve y profesional.
- Basar respuestas en documentacion aprobada, no en suposiciones.

### 12.5. Mantenimiento del entrenamiento

La base del chatbot se actualiza cuando cambian:

- servicios publicados;
- politicas de privacidad o terminos de uso;
- URL productiva;
- flujo de autenticacion;
- version de APK;
- manual de usuario;
- roles o permisos;
- procedimientos de soporte;
- criterios tecnicos visibles para usuarios.

Cada actualizacion debe registrar fecha, responsable, fuente documental usada y alcance del cambio.

## 13. Politicas publicas del sitio

El sitio debe enlazar politicas basicas en lenguaje comprensible:

| Politica | Contenido minimo |
| -------- | ---------------- |
| Privacidad | Datos recolectados, finalidad, responsables, conservacion, seguridad y contacto. |
| Terminos de uso | Reglas de acceso, uso permitido, restricciones, disponibilidad y responsabilidades. |
| Licenciamiento | Titularidad del software, uso de terceros y condiciones de distribucion del APK. |
| Cookies o analitica | Herramientas usadas, finalidad y opciones del usuario, si corresponde. |
| Soporte | Canales, horarios, severidades, tiempos de respuesta y alcance del servicio. |
| Mantenimiento de contenido | Responsables, frecuencia, versionado y criterios para retirar informacion obsoleta. |

Estas politicas deben estar visibles desde el pie de pagina y desde la seccion de soporte o contacto.

## 14. Politicas de mantenimiento del contenido

El contenido del sitio debe tratarse como informacion oficial de la empresa. Cualquier cambio debe ser revisado antes de publicarse, especialmente si afecta producto, soporte, politicas o descargas.

### 14.1. Responsabilidades

| Rol | Responsabilidad |
| --- | --------------- |
| Product Owner | Aprueba contenido de producto, beneficios, alcance y mensajes orientados al cliente. |
| Scrum Master | Coordina revision, evidencia de publicacion y cumplimiento de fechas. |
| Responsable tecnico | Valida URLs, descargas, version de APK, estado del despliegue y enlaces a documentacion. |
| Responsable de calidad | Revisa claridad, consistencia, ortografia, trazabilidad y ausencia de datos sensibles. |

### 14.2. Frecuencia de revision

| Frecuencia | Actividad |
| ---------- | --------- |
| En cada release | Validar enlaces, descargas, notas de version, manuales y capturas visibles. |
| Mensual | Revisar textos institucionales, servicios, contacto, preguntas frecuentes y chatbot. |
| Antes de una demo | Confirmar disponibilidad HTTPS, login, portal, QR, descargas y formulario de contacto. |
| Ante incidente critico | Publicar aviso, actualizar soporte y retirar informacion temporal incorrecta si aplica. |
| Ante cambio legal o de datos | Revisar privacidad, terminos de uso y consentimiento del formulario. |

### 14.3. Flujo de cambio de contenido

1. Identificar necesidad de cambio.
2. Registrar fuente del cambio: release, incidente, feedback de usuario, decision del PO o ajuste legal.
3. Editar contenido en rama o cambio controlado.
4. Revisar ortografia, enlaces, consistencia y datos sensibles.
5. Validar despliegue en ambiente publicado.
6. Registrar fecha, responsable y descripcion breve del cambio.

### 14.4. Criterios de retiro de contenido

Se debe retirar, corregir o marcar como historico cualquier contenido que:

- apunte a descargas no vigentes;
- mencione funcionalidades no disponibles;
- contradiga la modalidad 100 % en linea;
- exponga datos internos, credenciales o informacion de clientes;
- tenga enlaces rotos;
- use capturas desactualizadas;
- prometa tiempos, precios o garantias no aprobadas;
- confunda a Team 24 Software con Bulldog Tech.

## 15. Criterios de aceptacion del sitio publicado

| Criterio | Verificacion |
| -------- | ------------ |
| Acceso publico | La URL abre por HTTPS desde navegador externo. |
| Identidad clara | Se distingue Team 24 Software, Wireless HeatMapper y Bulldog Tech. |
| Secciones completas | Empresa, servicios, producto, descargas, soporte, contacto, chatbot y politicas estan visibles. |
| Enlaces funcionales | Login, manuales, descargas, politicas y contacto no devuelven error. |
| Chatbot entrenado | Responde preguntas especificas de empresa, producto, soporte y WiFi basico. |
| Seguridad de informacion | No se publican secretos, credenciales, datos privados ni enlaces internos sensibles. |
| Contenido vigente | Textos, descargas y manuales coinciden con la version desplegada. |
| Mantenimiento definido | Existe responsable, frecuencia y flujo de actualizacion documentado. |

## 16. Evidencias recomendadas

Para demostrar que el sitio esta publicado y mantenido, se recomienda conservar:

- captura de la pagina principal con URL visible;
- captura de cada seccion publica;
- captura de una conversacion valida con el chatbot;
- captura de la seccion de descargas;
- captura de politicas enlazadas;
- registro de verificacion de enlaces;
- QR de acceso usado en presentaciones;
- commit o version donde se actualizo el contenido.

## 17. Relacion con otros documentos

Este documento se complementa con:

- `01-resumen-ejecutivo.md`, para la vision general del producto y empresa.
- `04-manual-calidad.md`, para politicas institucionales de calidad.
- `06-aspectos-legales.md`, para obligaciones de empresa de software en Bolivia.
- `07-infraestructura-produccion.md`, para despliegue, ambientes, seguridad y CI/CD.
- `11-marketing.md`, para canales de promocion y posicionamiento.
- `12-puesta-marcha.md`, para operacion del producto desplegado.
- `13-software-producto.md`, para ficha tecnica de Wireless HeatMapper.


# Estudio de mercado

## Objetivo

Evaluar la oportunidad comercial de Wireless HeatMapper para empresas que instalan, diagnostican o mantienen redes WiFi en interiores, con enfasis inicial en Bolivia y posibilidad de expansion regional.

## Mercado objetivo

El producto atiende a organizaciones que necesitan relevar cobertura WiFi y entregar evidencia tecnica:

- Empresas de telecomunicaciones e integradores de redes.
- Consultoras de infraestructura TI.
- Proveedores de servicios administrados.
- Universidades, colegios, clinicas, hoteles y edificios corporativos.
- Empresas con multiples sedes que requieren estandarizar auditorias WiFi.

## Segmentacion

| Segmento | Necesidad | Disposicion probable |
| -------- | --------- | -------------------- |
| Integradores pequenos | Reducir costo frente a herramientas profesionales caras. | Alta si el precio mensual es accesible. |
| Empresas medianas de TI | Estandarizar reportes y supervisar tecnicos. | Alta con portal cliente y control organizacional. |
| Instituciones educativas | Mejorar cobertura en aulas y laboratorios. | Media, depende de presupuesto anual. |
| Hoteles y comercios | Resolver quejas de conectividad. | Media, compra por proyecto. |
| Consultores independientes | Generar entregables mas profesionales. | Alta con plan economico. |

## Competencia y sustitutos

| Alternativa | Fortalezas | Limitaciones para el mercado objetivo |
| ----------- | ---------- | ------------------------------------- |
| Herramientas profesionales de site survey | Alta precision, reportes avanzados, hardware especializado. | Costo elevado, curva de aprendizaje y menor accesibilidad para equipos pequenos. |
| Apps moviles gratuitas | Bajo costo y disponibilidad inmediata. | No integran plano, portal cliente, gestion organizacional ni trazabilidad. |
| Planillas y mapas manuales | No requieren software especializado. | Alto error manual, poco profesional y dificil de auditar. |
| Desarrollo interno | Ajuste exacto a procesos propios. | Costo alto, mantenimiento permanente y riesgo tecnico. |

Como referencia de problema economico, herramientas comerciales de site survey pueden superar USD 3.000 anuales por licencia, lo que crea espacio para una solucion SaaS local o regional de menor costo.

## Supuestos cuantitativos iniciales

Los siguientes numeros son supuestos de planificacion que deben validarse con entrevistas y cotizaciones reales antes de una decision comercial definitiva:

| Variable | Supuesto base |
| -------- | ------------- |
| Clientes potenciales iniciales en Santa Cruz | 30 empresas o consultores TI con actividad en redes. |
| Tasa de conversion primer ano | 10 % del universo inicial. |
| Clientes pagos primer ano | 3 clientes empresariales. |
| Precio SaaS mensual base | USD 49 por organizacion. |
| Precio SaaS profesional | USD 99 por organizacion. |
| Ticket por implementacion/capacitacion | USD 150 por cliente. |
| Churn anual estimado | 15 %. |

## Modelo de monetizacion

Se recomienda modelo SaaS con planes:

| Plan | Precio referencial | Incluye |
| ---- | ------------------ | ------- |
| Base | USD 49/mes | 1 administrador, 2 tecnicos, proyectos limitados. |
| Profesional | USD 99/mes | Mas tecnicos, portal cliente y mayor volumen. |
| Proyecto unico | USD 120 por proyecto | Uso puntual para consultores o auditorias. |
| Servicios | Desde USD 150 | Capacitacion, carga inicial y soporte especializado. |

## Proyeccion simple de ingresos

| Escenario | Clientes promedio | Ingreso mensual SaaS | Ingreso anual SaaS |
| --------- | ----------------- | -------------------- | ------------------ |
| Conservador | 3 clientes a USD 49 | USD 147 | USD 1.764 |
| Base | 5 clientes a USD 99 | USD 495 | USD 5.940 |
| Optimista | 12 clientes a USD 99 | USD 1.188 | USD 14.256 |

Ingresos por capacitacion pueden agregar entre USD 450 y USD 1.800 durante el primer ano, segun cantidad de clientes y servicios contratados.

## Costos comerciales y operativos iniciales

| Concepto | Estimacion mensual |
| -------- | ------------------ |
| Hosting cloud inicial | USD 40 a USD 80 |
| Dominio y certificados | USD 1 a USD 2 prorrateado si se usa dominio propio |
| Marketing digital basico | USD 50 a USD 100 |
| Soporte y operacion | 10 a 20 horas mensuales |
| Herramientas complementarias | USD 0 a USD 30 |

## Indicadores de mercado

- Costo de adquisicion por cliente.
- Tasa de conversion desde demostraciones.
- Tiempo promedio para configurar un proyecto.
- Numero de proyectos por cliente al mes.
- Retencion mensual.
- Satisfaccion de clientes y tecnicos.

## Conclusion comercial

Wireless HeatMapper es viable como producto SaaS especializado si se posiciona en el espacio entre apps gratuitas insuficientes y suites profesionales costosas. El mercado inicial no debe asumirse masivo; debe trabajarse por nicho, con demostraciones tecnicas, pilotos controlados y validacion de disposicion de pago.



# Plan de pruebas del software

## Proposito

El plan de pruebas asegura que Wireless HeatMapper cumpla requisitos funcionales, no funcionales y de negocio antes de su entrega como producto. Integra pruebas de desarrollador, QA y Product Owner, ademas de tecnicas de caja blanca, checklists, rendimiento y seguridad.

## Flujo de trabajo de pruebas del Proceso Unificado

| Actividad | Aplicacion en el proyecto |
| --------- | ------------------------- |
| Planificar pruebas | Definir alcance, riesgos, niveles, herramientas y criterios de aceptacion. |
| Disenar pruebas | Derivar casos desde historias, casos de uso, reglas de negocio y riesgos. |
| Implementar pruebas | Automatizar pruebas unitarias, integracion y fixtures. |
| Ejecutar pruebas | Correr suites backend, web, movil y pruebas manuales. |
| Evaluar resultados | Comparar contra criterios de aceptacion, cobertura y defectos. |
| Registrar defectos | Clasificar severidad, responsable y accion correctiva. |
| Verificar correcciones | Reejecutar pruebas afectadas y validar no regresion. |
| Cerrar pruebas | Emitir reporte y autorizacion de liberacion. |

El flujo se resume en una figura UML de actividad incluida en el consolidado.

## Niveles obligatorios

| Nivel | Responsable | Objetivo | Evidencia |
| ----- | ----------- | -------- | --------- |
| 1. Unidad | Programador | Probar su propio codigo antes de entregar. | pytest, Flutter test, pruebas de servicios. |
| 2. QA | QA rotativo | Intentar quebrar el software, revisar rendimiento y seguridad. | Casos negativos, OWASP, latencia, checklist. |
| 3. Product Owner | PO | Validar valor funcional y cumplimiento de negocio. | Acta de aceptacion o rechazo. |

## Herramientas

| Area | Herramientas |
| ---- | ------------ |
| Backend | pytest, pytest-asyncio, pytest-cov, httpx/TestClient. |
| Web | ESLint, build Vite, pruebas UI planificadas con Vitest. |
| Movil | flutter analyze, flutter test. |
| Rendimiento | pytest-benchmark, Locust o k6. |
| Seguridad | OWASP ZAP, revision de dependencias, validacion de configuracion TLS. |
| Datos | Seed controlado y cargas sinteticas. |

## Tecnica de caja blanca: camino basico

Se seleccionan metodos con complejidad ciclomatica >= 3 por contener decisiones relevantes. Para cada metodo se identifican caminos independientes y pruebas minimas.

### Metodo 1: autenticacion de usuario

**Decision logica:** usuario existente, activo, password valido, token emitido.  
**Complejidad estimada:** 4.

| Camino | Condicion | Resultado esperado |
| ------ | --------- | ------------------ |
| C1 | Email inexistente | Error de credenciales. |
| C2 | Usuario inactivo | Rechazo por estado. |
| C3 | Password invalido | Error de credenciales. |
| C4 | Datos validos | Access token y refresh token emitidos. |

### Metodo 2: carga y validacion de plano

**Decision logica:** formato, tamano, proyecto propio, conversion de archivo.  
**Complejidad estimada:** 5.

| Camino | Condicion | Resultado esperado |
| ------ | --------- | ------------------ |
| C1 | Proyecto ajeno | 403 o rechazo equivalente. |
| C2 | Formato no permitido | Error de validacion. |
| C3 | Archivo excede limite | Error por tamano. |
| C4 | PDF multipagina no permitido | Error controlado. |
| C5 | Archivo valido | Plano almacenado y metadatos registrados. |

### Metodo 3: registro de mediciones WiFi

**Decision logica:** plano calibrado, punto valido, RSSI en rango, lote no vacio, propiedad.  
**Complejidad estimada:** 6.

| Camino | Condicion | Resultado esperado |
| ------ | --------- | ------------------ |
| C1 | Plano no calibrado | Rechazo por precondicion. |
| C2 | Punto fuera del plano | Error de validacion. |
| C3 | RSSI fuera de rango | Error de validacion. |
| C4 | Lote vacio | Error de validacion. |
| C5 | Proyecto ajeno | Rechazo por propiedad. |
| C6 | Lote valido | Lecturas persistidas y clasificadas. |

### Metodo 4: generacion de heatmap

**Decision logica:** puntos minimos, algoritmo soportado, conjunto AP valido, matriz generada, permisos.  
**Complejidad estimada:** 5.

| Camino | Condicion | Resultado esperado |
| ------ | --------- | ------------------ |
| C1 | Menos de 5 puntos | Rechazo por datos insuficientes. |
| C2 | Algoritmo no soportado | Error controlado. |
| C3 | Conjunto AP inexistente | Error de referencia. |
| C4 | Usuario sin permiso | Rechazo por autorizacion. |
| C5 | Datos validos | Mapa de calor generado y persistido. |

## Checklists

### Checklist previo a release

- [ ] Todas las pruebas automatizadas obligatorias pasan.
- [ ] No existen defectos criticos abiertos.
- [ ] Migraciones aplican correctamente.
- [ ] Variables de entorno productivas estan definidas.
- [ ] TLS y reverse proxy estan operativos.
- [ ] Backups estan configurados.
- [ ] Portal cliente no expone proyectos no publicados.
- [ ] Releases moviles incluyen version y changelog.
- [ ] Terminos y politica de privacidad estan disponibles.

### Checklist de seguridad

- [ ] JWT expira y refresh token se invalida al cerrar sesion.
- [ ] Roles impiden acceso cruzado.
- [ ] Validacion de ownership en proyectos, planos, mediciones y heatmaps.
- [ ] Entradas del usuario se validan con schemas.
- [ ] Passwords se almacenan con hash seguro.
- [ ] Secretos no estan versionados.
- [ ] API no expone trazas internas en produccion.

## Pruebas de rendimiento

| Operacion | Carga objetivo | Meta |
| --------- | -------------- | ---- |
| Login | 50 usuarios concurrentes | p95 <= 1 s |
| Listado de proyectos | 1.000 proyectos semilla | p95 <= 1 s |
| Registro de mediciones | Lotes de 10 a 50 lecturas | p95 <= 1 s |
| Generacion heatmap | 200 puntos | p95 <= 3 s |
| Portal cliente | 100 accesos concurrentes | p95 <= 2 s |

## Pruebas de vulnerabilidades

Se propone ejecutar OWASP ZAP contra la URL publica y revisar:

- Inyeccion.
- Autenticacion rota.
- Exposicion de datos sensibles.
- Control de acceso roto.
- Configuracion insegura.
- Componentes vulnerables.

## Criterios de cierre

El software se considera apto para entrega cuando las pruebas obligatorias pasan, no existen defectos criticos, los hallazgos medios tienen plan de mitigacion, el Product Owner acepta el alcance y la evidencia queda registrada.


# Plan de marketing

## Objetivo general

Dar a conocer Team 24 Software y posicionar Wireless HeatMapper como una solucion accesible, tecnica y verificable para relevamiento de cobertura WiFi en interiores.

## Publicos objetivo

| Publico | Mensaje principal |
| ------- | ----------------- |
| Integradores de redes | Entregue mapas de calor profesionales sin pagar suites costosas. |
| Empresas con sedes fisicas | Detecte zonas muertas y mejore la experiencia de usuarios WiFi. |
| Consultores TI | Profesionalice sus diagnosticos con evidencia visual e interactiva. |
| Instituciones educativas | Planifique cobertura por aulas, laboratorios y oficinas. |
| Hoteles y comercios | Reduzca quejas por mala senal y documente mejoras. |

## Posicionamiento

Wireless HeatMapper se posiciona como una solucion SaaS local, ligera y especializada para equipos que necesitan mapas de calor WiFi, portal cliente y trazabilidad, pero no justifican el costo de herramientas empresariales de alta gama.

## Canales

| Canal | Uso |
| ----- | --- |
| Sitio web | Presentacion institucional, demo, contacto y soporte. |
| LinkedIn | Publicaciones tecnicas y casos de uso empresariales. |
| Facebook | Alcance local y demostraciones visuales. |
| WhatsApp Business | Contacto comercial y soporte inicial. |
| Ferias tecnologicas | Demostracion presencial con mapas de calor. |
| Convenios academicos | Validacion y difusion en entornos educativos. |
| Repositorio GitHub | Transparencia tecnica y evidencia del producto. |

## Material promocional

- Flyer digital de problema/solucion.
- Video demo de 60 a 90 segundos.
- Caso de uso con plano, mediciones y heatmap.
- Presentacion comercial corta.
- Publicaciones comparativas: app gratuita vs. Wireless HeatMapper.
- QR hacia demo web, repositorio y releases moviles.

## Calendario inicial

| Semana | Actividad |
| ------ | --------- |
| 1 | Publicar landing institucional y demo tecnica. |
| 2 | Publicar video corto de captura y heatmap. |
| 3 | Contactar 10 integradores o consultores TI. |
| 4 | Ejecutar 2 demostraciones guiadas. |
| 5 | Publicar caso de estudio Bulldog Tech. |
| 6 | Ajustar propuesta comercial segun retroalimentacion. |

## Presupuesto referencial

| Concepto | Monto mensual |
| -------- | ------------- |
| Diseno de piezas basicas | USD 30 |
| Publicidad digital local | USD 50 a USD 100 |
| Dominio o correo institucional | USD 1 a USD 5 prorrateado |
| Demo y soporte comercial | 10 horas de equipo |

## Metricas

- Visitantes al sitio.
- Clics en QR o enlaces publicos.
- Contactos recibidos.
- Demos agendadas.
- Pilotos iniciados.
- Conversion a plan pago.
- Costo por lead.
- Retencion posterior al primer mes.



# Aspectos para la puesta en marcha

## Objetivo

Definir las condiciones necesarias para operar Wireless HeatMapper como producto real: infraestructura cloud, costos, licenciamiento, cuentas de publicacion movil, terminos legales, privacidad y adopcion asistida por IA.

## Comparacion cloud

La arquitectura requiere un servidor de aplicacion, base de datos PostgreSQL, reverse proxy, almacenamiento de planos, backups y monitoreo. Para un inicio controlado se compara AWS, Google Cloud y Azure.

| Criterio | AWS | Google Cloud | Azure |
| -------- | --- | ------------ | ----- |
| Computo | EC2 o ECS. | Compute Engine o Cloud Run. | Virtual Machine, App Service o Container Apps. |
| Base de datos | RDS PostgreSQL o PostgreSQL en VM. | Cloud SQL PostgreSQL o PostgreSQL en VM. | Azure Database for PostgreSQL o PostgreSQL en VM. |
| Costeo | AWS Pricing Calculator. | Google Cloud Pricing Calculator. | Azure Pricing Calculator. |
| Ventaja | Ecosistema maduro y amplio. | Buen soporte de analitica y servicios gestionados. | Integracion directa con entorno Microsoft y VM actual del proyecto. |
| Riesgo | Complejidad inicial. | Costos variables si no se controla egress. | Costos de servicios gestionados pueden subir al escalar. |

## Proyeccion de costos iniciales

Los montos son referenciales y deben recalcularse con las calculadoras oficiales antes de compra o despliegue final.

| Escenario | Infraestructura | Costo mensual estimado |
| --------- | --------------- | ---------------------- |
| Economico | Una VM con Docker Compose, PostgreSQL local, backups manuales. | USD 20 a USD 50 |
| Base | VM 2 vCPU/4 GB, disco persistente, backups automatizados. | USD 40 a USD 90 |
| Gestionado | App service/containers + PostgreSQL gestionado + storage. | USD 80 a USD 180 |
| Escalable | Contenedores gestionados, base gestionada, monitoreo y CDN. | USD 180+ |

Para la entrega academica se utiliza Azure por disponibilidad actual del frontend publicado. Para operacion comercial, se recomienda mantener el escenario base hasta validar clientes pagos.

## Cuentas de tiendas moviles

### Google Play

Google Play Console requiere cuenta de Google, aceptacion del Developer Distribution Agreement, verificacion de identidad, seleccion de tipo de cuenta personal u organizacion y pago unico de registro de USD 25. Las cuentas personales nuevas tienen requisitos adicionales de pruebas antes de distribucion publica.

### Apple Developer

Apple Developer Program tiene membresia anual de USD 99 para distribucion en App Store. La inscripcion puede ser individual u organizacion. Las organizaciones deben verificar identidad, contar con D-U-N-S Number y acreditar autoridad para vincular legalmente a la entidad.

## Tipo de licencia

Se recomienda licenciamiento SaaS:

- El cliente paga suscripcion por organizacion.
- Team 24 Software opera backend, web, seguridad y backups.
- La app movil se distribuye como cliente delgado.
- Los datos del cliente se mantienen segregados por organizacion/proyecto.

Tambien puede ofrecerse licencia por proyecto unico para consultores o clientes con baja recurrencia. No se recomienda on-premise en la primera etapa porque incrementa soporte, instalacion y complejidad operativa.

## Terminos y condiciones

Los terminos deben cubrir:

- Descripcion del servicio.
- Roles de usuario.
- Uso permitido y prohibido.
- Responsabilidad sobre datos cargados.
- Disponibilidad y mantenimiento.
- Limitaciones de responsabilidad.
- Propiedad intelectual.
- Suspension de cuentas.
- Soporte y canales oficiales.
- Cambios al servicio.

## Politica de privacidad

La politica debe explicar:

- Datos personales tratados: nombre, email, rol y actividad.
- Datos tecnicos: proyectos, planos, mediciones WiFi, tokens y logs.
- Finalidad: operar el servicio, generar heatmaps, soporte y seguridad.
- Conservacion: mientras exista relacion contractual o necesidad legal.
- Seguridad: autenticacion, control de acceso, cifrado en transito y backups.
- Derechos del usuario: acceso, correccion, eliminacion cuando corresponda.

## Adopcion asistida por IA

Se propone un agente de ayuda integrado que observe contexto de pantalla, rol y flujo actual para responder preguntas sin que el usuario explique desde cero. Ejemplos:

- Si el tecnico esta calibrando plano, explicar como marcar distancia real.
- Si esta capturando WiFi, advertir sobre throttling Android.
- Si el administrador publica enlace, explicar vencimiento y contenido visible.
- Si el cliente consulta portal, explicar interpretacion de colores y RSSI.

## Fuentes oficiales de costos y cuentas

- AWS Pricing Calculator.
- Google Cloud Pricing Calculator.
- Azure Pricing Calculator.
- Google Play Console Help.
- Apple Developer Program.



# Software como producto

## Identificacion del producto

**Nombre:** Wireless HeatMapper  
**Proveedor:** Team 24 Software  
**Cliente inicial:** Bulldog Tech.  
**Modalidad:** SaaS 100 % en linea con app movil Android, backend REST y plataforma web.
**Fuente de verdad:** PostgreSQL central, sin base de datos local de dominio en el dispositivo movil.
**Version movil base:** 1.0.0+1.

Wireless HeatMapper se entrega como un producto integrado para relevamiento, analisis y publicacion de cobertura WiFi. La aplicacion movil funciona como cliente delgado para tecnicos de campo; el backend concentra autenticacion, reglas de negocio, persistencia, generacion de mapas de calor e inteligencia artificial; y la plataforma web permite administracion organizacional, revision tecnica y acceso controlado del cliente final.

## URLs y artefactos publicos

| Recurso | URL | Uso |
| ------- | --- | --- |
| Repositorio GitHub | <https://github.com/borysinho/wireless-heatmapper> | Codigo fuente, documentacion, historial, workflows y trazabilidad tecnica. |
| Frontend publicado | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/> | Entrada publica al panel web y portal de cliente. |
| Panel administrador | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/admin/login> | Acceso para administradores y usuarios autorizados. |
| Portal cliente | `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/portal/{token}` | Acceso por enlace unico generado desde el panel web. |
| API REST | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/> | Base publica de endpoints consumidos por web y movil. |
| Swagger / OpenAPI | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/docs> | Documentacion interactiva de endpoints. |
| Esquema OpenAPI | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/openapi.json> | Contrato tecnico consumible por herramientas. |
| Manual de usuario | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/> | Guia publica de operacion funcional. |
| Releases moviles | <https://github.com/borysinho/wireless-heatmapper/releases> | APK Android generado por GitHub Actions. |

Estas URLs son las referencias publicas para entrega academica, demostracion y continuidad. En anexos se incorporan codigos QR hacia repositorio, frontend publicado, manual de usuario y releases moviles.

## Componentes entregables

| Componente | Descripcion |
| ---------- | ----------- |
| Backend REST + IA | API FastAPI con autenticacion, roles, servicios de dominio, almacenamiento, mapas de calor, propuestas IA y publicacion para cliente. |
| Base de datos | PostgreSQL con migraciones y entidades para usuarios, clientes, proyectos, planos, mediciones, conjuntos AP, mapas de calor y enlaces. |
| Web admin | Plataforma React/TypeScript para gestionar usuarios, clientes, proyectos RF, datos de campo, escenarios IA y publicacion. |
| Portal cliente | Vista web por token para consultar resultados publicados sin cuenta interna. |
| App movil Android | Cliente Flutter para tecnicos de campo: login, proyectos, planos, captura WiFi y consulta de heatmaps. |
| Infraestructura | Docker Compose, Nginx, TLS, GitHub Actions, despliegue cloud y publicacion de APK. |
| Manual y documentacion | Manual de usuario, modelos, pruebas, puesta en marcha, bibliografia y anexos con evidencias. |

## Componentes backend

| Area | Entrega |
| ---- | ------- |
| API | Servicio REST documentado con OpenAPI y healthcheck operativo. |
| Autenticacion | Login, JWT, refresh token, roles y control de acceso por usuario. |
| Administracion | Gestion de usuarios tecnicos, clientes y proyectos organizacionales. |
| Proyectos | CRUD de proyectos, asociacion con cliente y control de ownership. |
| Planos | Carga, almacenamiento, URLs firmadas, consulta y calibracion. |
| Captura WiFi | Persistencia de puntos de medicion y lecturas RSSI enviadas desde Android. |
| Heatmaps | Generacion de mapas de calor desde datos persistidos. |
| Conjuntos AP | Gestion de conjuntos tecnicos, AP disponibles y mapas asociados. |
| IA | Propuestas de optimizacion como conjuntos derivados y trazables. |
| Portal | Generacion y validacion de enlaces unicos para cliente. |
| Notificaciones | Base tecnica para dispositivos push y notificaciones operativas. |

## Componentes web

| Modulo | Entrega |
| ------ | ------- |
| Login administrador | Autenticacion web y carga de sesion. |
| Dashboard | Vista inicial de administracion. |
| Usuarios | Alta, edicion, consulta y administracion de tecnicos. |
| Clientes | Alta, edicion y consulta de clientes organizacionales. |
| Proyectos RF | Listado organizacional y navegacion al detalle tecnico. |
| Datos de campo | Visualizacion de conjuntos AP, mapas e informacion capturada. |
| Escenarios IA | Consulta de propuestas IA y comparacion con datos de campo. |
| Publicacion | Generacion y administracion del enlace unico para cliente. |
| Portal cliente | Visualizacion publica por token de resultados autorizados. |

## Componentes moviles

| Modulo | Entrega |
| ------ | ------- |
| Autenticacion | Login de tecnico contra backend y manejo seguro de sesion. |
| Proyectos | Listado, creacion, edicion, archivo y eliminacion logica segun permisos. |
| Clientes | Consulta remota de clientes para asociar proyectos. |
| Planos | Listado, carga, visualizacion, calibracion y renovacion de URL firmada. |
| Captura WiFi | Escaneo WiFi Android, seleccion de punto sobre plano y envio de mediciones. |
| Heatmap | Consulta de AP disponibles, conjuntos AP, escala y mapas generados en backend. |
| Conectividad | Avisos cuando la operacion en linea no esta disponible. |
| Notificaciones | Integracion base con Firebase Messaging y notificaciones locales. |
| Configuracion productiva | APK release apuntando a `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api`. |

La app movil conserva solamente credenciales de sesion y preferencias minimas necesarias. No almacena datos de dominio entre sesiones ni implementa sincronizacion diferida.

## Funcionalidades principales por actor

| Actor | Funcionalidades entregadas |
| ----- | -------------------------- |
| Administrador | Iniciar sesion, gestionar usuarios, gestionar clientes, consultar proyectos organizacionales, revisar datos RF, consultar escenarios IA y publicar resultados por enlace. |
| Tecnico de campo | Iniciar sesion en Android, gestionar sus proyectos, cargar y calibrar planos, capturar mediciones WiFi, consultar heatmaps y operar siempre contra el backend. |
| Cliente final | Abrir enlace unico, visualizar proyecto publicado, revisar datos de campo, heatmaps y resultados seleccionados por el administrador. |
| Sistema backend | Persistir dominio, aplicar reglas de acceso, generar heatmaps, gestionar conjuntos AP, producir propuestas IA trazables y servir contratos API. |
| Operacion DevOps | Validar cambios por CI, desplegar contenedores, publicar APK, mantener variables productivas y verificar salud de servicios. |

## Flujo de valor extremo a extremo

1. El administrador crea clientes, tecnicos y revisa proyectos desde la web.
2. El tecnico ingresa a la app movil y crea o selecciona un proyecto asignado.
3. El tecnico sube el plano al backend y calibra la escala del plano.
4. El tecnico captura lecturas WiFi sobre puntos del plano desde Android.
5. El backend persiste puntos, lecturas y datos de APs en PostgreSQL.
6. El tecnico o administrador genera conjuntos AP y mapas de calor.
7. El backend genera propuestas IA como conjuntos derivados y comparables.
8. El administrador selecciona resultados publicables y genera un enlace de cliente.
9. El cliente abre el portal por token y consulta los resultados publicados.

Este flujo demuestra la modalidad 100 % en linea: todas las operaciones de dominio dependen del backend y de la base central.

## Releases moviles

El release movil Android se administra con GitHub Actions.

| Elemento | Definicion |
| -------- | ---------- |
| Disparador automatico | Push de tags `mobile-v*`. |
| Disparador manual | Ejecucion manual con tag opcional y bandera de pre-release. |
| Validaciones previas | Instalacion de dependencias, analisis estatico y pruebas Flutter. |
| Build | APK Android en modo release con variables productivas. |
| Nombre de APK | `WirelessHeatMapper-{TAG}.apk`. |
| Destino | GitHub Releases del repositorio. |
| Retencion adicional | Artefacto temporal de GitHub Actions por 14 dias. |
| Backend configurado | `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api`. |

Cada release movil debe quedar asociado a un tag, un commit de origen, notas de release y APK descargable. El patron recomendado de tag conserva el formato `mobile-v{version}` o `mobile-v{version}-{run}` cuando se genera desde ejecucion manual.

## Repositorio y trazabilidad tecnica

| Recurso | Criterio de control |
| ------- | ------------------- |
| Rama productiva | `main` representa la version desplegable. |
| Rama de integracion | `develop` concentra integracion antes de promocion. |
| Ramas de trabajo | Ramas cortas por historia, correccion, infraestructura o documentacion. |
| Commits | Mensajes claros, preferentemente Conventional Commits en espanol. |
| Pull requests | Cambios funcionales pasan por validaciones aplicables antes de integrarse. |
| Workflows | CI, despliegue cloud y release movil quedan versionados en GitHub. |
| Evidencia historica | Git, GitHub Actions, GitHub Releases, OpenAPI y capturas de demostracion. |

## Criterios de producto terminado

| Criterio | Condicion |
| -------- | --------- |
| Funcional | Flujos principales de administracion, captura, heatmap, IA y portal cliente operan de extremo a extremo. |
| Modalidad online | La app movil no reintroduce base local de dominio ni sincronizacion diferida. |
| Integracion | Backend, web, movil, PostgreSQL, Nginx y workflows estan integrados segun la arquitectura documentada. |
| Seguridad | Roles, ownership, JWT, refresh token, URLs firmadas y tokens de portal se aplican en puntos criticos. |
| Calidad | Pruebas razonables del release ejecutadas sin defectos criticos abiertos. |
| Operacion | Plataforma web publica, API documentada, manual publicado y APK disponible en releases. |
| Documentacion | PAPS, modelos, pruebas, manual, puesta en marcha, bibliografia y anexos se encuentran completos. |
| Evidencia | Existen capturas, video o demostracion guiada de los flujos principales y enlaces publicos. |

## Soporte inicial

El soporte se organiza por niveles para separar dudas de uso, incidentes reproducibles y cambios estructurales.

| Nivel | Responsable | Alcance | Tiempo objetivo inicial |
| ----- | ----------- | ------- | ----------------------- |
| N1 | Product Owner / soporte funcional | Accesos, dudas de uso, navegacion, datos de demo y acompanamiento al cliente. | 1 dia habil |
| N2 | Equipo tecnico | Errores reproducibles, fallas de integracion, problemas de configuracion y revision de logs. | 2 dias habiles |
| N3 | Arquitectura / desarrollo | Defectos complejos, seguridad, migraciones, infraestructura, IA y cambios de diseno. | 3 a 5 dias habiles |

Canales minimos recomendados:

- Correo de soporte institucional.
- Registro de incidencias en GitHub Issues o tablero equivalente.
- Evidencia obligatoria por incidencia: usuario afectado, fecha, pasos, captura, URL o proyecto relacionado.
- Clasificacion por severidad: critica, alta, media o baja.

## Versionado

| Artefacto | Regla de versionado |
| --------- | ------------------- |
| Codigo fuente | Historial Git con commits atomicos y tags para releases relevantes. |
| Backend | Version expuesta por healthcheck y metadatos de la API. |
| Web | Version asociada al commit desplegado y a la imagen Docker publicada. |
| Movil | Version declarada en Flutter y tag `mobile-v*`. |
| Imagenes Docker | Tags `latest` y `COMMIT_SHA` en el registro de contenedores. |
| Documentacion | Control por Git y actualizacion junto al release. |
| Base de datos | Migraciones versionadas junto al cambio de modelo. |

Cada release debe incluir:

- Numero o tag de version.
- Fecha de publicacion.
- Commit o hash de referencia.
- Cambios principales.
- Correcciones incluidas.
- Riesgos conocidos o limitaciones.
- Artefactos publicados: APK, imagenes Docker, URL productiva o documentacion.
- Evidencias de pruebas ejecutadas.

## Evidencias de funcionamiento

| Evidencia | Forma esperada |
| --------- | -------------- |
| Repositorio accesible | URL publica de GitHub y hash del commit entregado. |
| Pipeline CI | Ejecucion de GitHub Actions sin fallos criticos en backend, web y manual. |
| Despliegue productivo | Plataforma web abierta en el dominio Azure y healthcheck backend operativo. |
| OpenAPI | Swagger disponible en `/api/docs` y esquema en `/api/openapi.json`. |
| APK Android | Archivo publicado en GitHub Releases con notas de release. |
| Login administrador | Captura o video del acceso a `/admin/login`. |
| Gestion de usuarios/clientes | Captura o video de alta, edicion o consulta. |
| Proyecto y plano | Captura o video de creacion de proyecto, carga y calibracion de plano. |
| Captura WiFi movil | Captura o video de punto medido y lectura enviada al backend. |
| Heatmap | Captura o video del mapa de calor generado desde datos persistidos. |
| Escenario IA | Captura o video de propuesta IA como conjunto derivado. |
| Portal cliente | URL con token de demo y captura de resultados publicados. |
| Manual de usuario | Sitio `/manual/` accesible con guia funcional. |
| Consolidado final | Documento academico en Word con diagramas y codigos QR. |

Para la entrega final, las evidencias deben vincularse al mismo commit o release que se presenta. Si una evidencia corresponde a un ambiente de demo, se registra la fecha, usuario de prueba, proyecto usado y limitaciones conocidas.

## Cierre de producto

Wireless HeatMapper queda definido como un producto integrado compuesto por:

- Backend FastAPI con persistencia PostgreSQL, reglas de negocio, generacion de heatmaps e IA.
- Plataforma web React/Vite para administracion, revision RF, escenarios IA y portal cliente.
- App Android Flutter para tecnicos de campo, operando como cliente delgado en linea.
- Infraestructura productiva reproducible con Docker Compose, Nginx, TLS y GitHub Actions.
- Repositorio, releases moviles, documentacion, manual y evidencias suficientes para demostracion y continuidad.

El producto final cumple la orientacion del proyecto: captura, analisis y entrega de resultados WiFi sin persistencia local de dominio en el dispositivo movil y con PostgreSQL como fuente central de verdad.


# Bibliografia

Amazon Web Services. (2026). *AWS Pricing Calculator*. https://aws.amazon.com/aws-cost-management/aws-pricing-calculator/

Apple Inc. (2026). *Apple Developer Program*. https://developer.apple.com/programs/

Apple Inc. (2026). *Identity verification*. https://developer.apple.com/help/account/membership/identity-verification

Coleman, D. D., & Westcott, D. A. (2018). *Certified Wireless Network Administrator Official Study Guide: Exam CWNA-107*. Sybex.

Google. (2026). *Get started with Play Console*. https://support.google.com/googleplay/android-developer/answer/6112435

Google Cloud. (2026). *Google Cloud Pricing Calculator*. https://cloud.google.com/products/calculator

Google Cloud. (2026). *Cloud SQL pricing*. https://cloud.google.com/sql/pricing

International Organization for Standardization. (2014). *ISO/IEC 90003:2014 Software engineering: Guidelines for the application of ISO 9001:2008 to computer software*.

Microsoft. (2026). *Azure Pricing Calculator*. https://azure.microsoft.com/pricing/calculator/

Microsoft. (2026). *Plan and manage costs for Azure App Service*. https://learn.microsoft.com/azure/app-service/overview-manage-costs

Object Management Group. (2017). *Unified Modeling Language specification, version 2.5.1*. https://www.omg.org/spec/UML/

Servicio de Impuestos Nacionales. (2026). *Generacion del Numero de Identificacion Tributaria (NIT)*. https://siatinfo.impuestos.gob.bo/

Servicio Nacional de Propiedad Intelectual. (2026). *Derecho de Autor y Derechos Conexos*. https://www.senapi.gob.bo/derecho-de-autor-y-derechos-conexos

Servicio Plurinacional de Registro de Comercio. (2026). *Tramites del Registro de Comercio*. https://www.seprec.gob.bo/

The Institute of Electrical and Electronics Engineers. (2014). *IEEE Standard for Software Quality Assurance Processes (IEEE Std 730)*.



# Anexos

## Anexo A: codigos QR

| Recurso | URL |
| ------- | --- |
| Repositorio GitHub | https://github.com/borysinho/wireless-heatmapper |
| Frontend publicado | https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/ |
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

\newpage

# Figuras UML renderizadas


## modelo contexto

![modelo contexto](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/01-modelo-contexto.png)


## arquitectura paquetes

![arquitectura paquetes](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/02-arquitectura-paquetes.png)


## arquitectura despliegue

![arquitectura despliegue](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/03-arquitectura-despliegue.png)


## modelo datos conceptual

![modelo datos conceptual](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/04-modelo-datos-conceptual.png)


## logica captura heatmap

![logica captura heatmap](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/05-logica-captura-heatmap.png)


## logica portal cliente

![logica portal cliente](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/06-logica-portal-cliente.png)


## estados proyecto

![estados proyecto](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/07-estados-proyecto.png)


## case navegabilidad

![case navegabilidad](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/08-case-navegabilidad.png)


## flujo pruebas rup

![flujo pruebas rup](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/diagramas/09-flujo-pruebas-rup.png)


\newpage

# Codigos QR

## Repositorio GitHub

<https://github.com/borysinho/wireless-heatmapper>

![QR repositorio](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-repositorio.png)

## Frontend publicado

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/>

![QR frontend](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-frontend.png)

## Manual de usuario

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/>

![QR manual](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-manual.png)

## Releases moviles

<https://github.com/borysinho/wireless-heatmapper/releases>

![QR releases](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-releases.png)

