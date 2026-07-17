

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


# Manual de garantia de calidad del software

## Identidad institucional

**Empresa:** Team 24 Software  
**Eslogan:** Software medible, verificable y alineado al cliente.  
**Normas guia:** ISO/IEC 90003 e IEEE 730.  

Este manual se orienta a la empresa de software, no solamente a Wireless HeatMapper. Define politicas y procedimientos aplicables a los proyectos de Team 24 Software, usando Wireless HeatMapper como primera aplicacion institucional.

## Mision

Desarrollar soluciones de software confiables, mantenibles y verificables, aplicando practicas de ingenieria, gestion de calidad y mejora continua para resolver necesidades reales de clientes mediante productos funcionales y documentados.

## Vision

Consolidarse como una empresa capaz de entregar productos de software con trazabilidad completa, evidencia de calidad, seguridad operativa y valor de negocio medible.

## Politica de calidad

Team 24 Software se compromete a construir software que satisfaga requisitos acordados con el cliente, cumpla criterios tecnicos verificables y conserve evidencia documental suficiente para demostrar conformidad. La calidad se gestiona desde el inicio del proyecto mediante requisitos claros, diseno trazable, revision tecnica, pruebas por niveles, control de cambios y mejora continua.

## Objetivos de calidad

| Objetivo | Metrica | Meta |
| -------- | ------- | ---- |
| Requisitos verificables | Historias con criterios de aceptacion | 100 % antes de ejecucion |
| Trazabilidad | Requisitos vinculados con diseno y prueba | 100 % de funcionalidades implementadas |
| Defectos criticos | Defectos criticos abiertos al liberar | 0 |
| Calidad de codigo | Cambios revisados o validados | 100 % de incrementos entregables |
| Pruebas | Pruebas definidas ejecutadas | 100 % de pruebas obligatorias por sprint |
| Documentacion | Artefactos afectados actualizados | 100 % antes del cierre |

## Roles de calidad

| Rol | Responsabilidad |
| --- | --------------- |
| Direccion tecnica | Aprobar arquitectura, releases y decisiones de alto impacto. |
| Product Owner | Validar valor de negocio y aceptacion funcional. |
| Scrum Master | Controlar proceso, riesgos, impedimentos y mejora continua. |
| Desarrollador | Implementar y probar su propio codigo antes de entregar. |
| QA rotativo | Intentar quebrar el incremento, revisar seguridad, rendimiento y bordes. |
| Responsable de configuracion | Controlar versiones, ramas, dependencias y artefactos liberados. |

## Procesos de calidad

| Proceso | Entradas | Salidas | Evidencia |
| ------- | -------- | ------- | --------- |
| Gestion de requisitos | Necesidad del cliente | Backlog priorizado | Historias, criterios, trazabilidad |
| Diseno | Historias aceptadas | Modelos UML y decisiones | Diagramas, actas tecnicas |
| Implementacion | Diseno y criterios | Codigo integrado | Commits, revisiones, CI |
| Verificacion | Codigo ejecutable | Resultados de prueba | Reportes pytest, Flutter, web |
| Validacion | Incremento desplegable | Aceptacion o rechazo | Acta de Sprint Review |
| Liberacion | Incremento validado | Version entregable | Release, changelog, evidencia |
| Mejora | Metricas y defectos | Acciones correctivas | Retrospectiva |

## Control documental y configuracion

- Todo documento formal mantiene version, fecha, responsable y estado.
- Todo cambio de alcance se registra con impacto sobre requisitos, historias, modelos y pruebas.
- El codigo fuente se administra con Git y ramas controladas.
- Los secretos no se versionan; se gestionan por variables de entorno o mecanismos seguros.
- Los artefactos liberados se vinculan a una version de repositorio y a evidencias de prueba.

## Auditoria interna

La auditoria de calidad se ejecuta por sprint o antes de una liberacion relevante. Debe revisar:

- Trazabilidad entre requisito, historia, implementacion y prueba.
- Cumplimiento de Definition of Done.
- Resultados de pruebas automatizadas y manuales.
- Riesgos abiertos.
- Defectos bloqueantes.
- Estado de documentacion y evidencias.

## No conformidades

Una no conformidad se registra cuando un entregable no cumple un requisito, criterio de aceptacion, politica de calidad o control obligatorio. El registro minimo incluye descripcion, severidad, responsable, causa probable, accion correctiva, accion preventiva y evidencia de cierre.

## Mejora continua

Cada sprint concluye con retrospectiva. La empresa debe registrar al menos una accion de mejora, asignar responsable y verificar su cierre en el siguiente ciclo. La mejora no se limita al codigo; puede afectar pruebas, comunicacion, infraestructura, documentacion, seguridad o estimacion.



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

## Proposito

El sitio web representa a Team 24 Software como empresa de desarrollo, no solamente al producto Wireless HeatMapper. Debe estar publicado en linea y servir como punto institucional para presentacion corporativa, servicios, soporte, contacto y acceso a soluciones.

## URL publica

La plataforma publicada se accede mediante:

<https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/>

Para la presentacion academica, esta URL se acompana con codigo QR en anexos.

## Contenido minimo del sitio

| Seccion | Contenido esperado |
| ------- | ------------------ |
| Quienes somos | Identidad de Team 24 Software, mision, vision y equipo. |
| Productos y servicios | Desarrollo de software, sistemas web, aplicaciones moviles, consultoria WiFi y analitica. |
| Producto destacado | Wireless HeatMapper, problema que resuelve, beneficios y componentes. |
| Descargas | Releases de la aplicacion movil, manuales y enlaces a repositorio si corresponde. |
| Soporte | Canal de ayuda, preguntas frecuentes y flujo de atencion. |
| Contacto | Email, WhatsApp, redes sociales y formulario. |
| Politicas | Terminos y condiciones, privacidad y licenciamiento. |
| Chatbot | Asistente propio entrenado con informacion de empresa y producto. |

## Chatbot propio

El chatbot no debe reducirse a un enlace de WhatsApp. Debe responder preguntas frecuentes sobre:

- Servicios de Team 24 Software.
- Uso general de Wireless HeatMapper.
- Diferencia entre tecnico, administrador y cliente.
- Requisitos para levantar un proyecto de site survey.
- Interpretacion basica de RSSI, mapas de calor y zonas muertas.
- Canales de soporte y escalamiento.

### Base de conocimiento propuesta

| Tema | Respuestas esperadas |
| ---- | -------------------- |
| Empresa | Que hace Team 24 Software, a que clientes atiende y como contactarla. |
| Producto | Funcionalidades principales, modalidad en linea y beneficios. |
| Soporte | Como reportar incidentes, que informacion enviar y tiempos estimados. |
| WiFi | Explicacion de RSSI, objetivo >= -70 dBm y zona muerta < -90 dBm. |
| Privacidad | Datos tratados, finalidad y controles de acceso. |

## Criterios de publicacion

- El sitio se accede por HTTPS.
- No depende de localhost ni prototipos.
- Los enlaces publicos funcionan.
- El contenido distingue empresa, producto y cliente.
- El chatbot responde con informacion especifica y no generica.
- Las politicas legales estan enlazadas.

## Mantenimiento

El contenido debe revisarse en cada release mayor. Los enlaces a descargas moviles, repositorio y documentacion publica deben validarse antes de cada entrega academica o demostracion.



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
**Modalidad:** SaaS en linea con app movil, backend y web.  

## URLs y artefactos publicos

| Recurso | URL |
| ------- | --- |
| Repositorio | <https://github.com/borysinho/wireless-heatmapper> |
| Frontend publicado | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/> |
| Releases moviles | <https://github.com/borysinho/wireless-heatmapper/releases> |

## Componentes entregables

| Componente | Descripcion |
| ---------- | ----------- |
| Backend REST | API FastAPI, autenticacion, servicios, IA, almacenamiento y reglas de negocio. |
| Base de datos | PostgreSQL con migraciones y entidades de dominio. |
| Web admin | Gestion de usuarios, clientes, proyectos, propuestas y publicacion. |
| Portal cliente | Acceso por enlace unico a resultados publicados. |
| App movil | Cliente Android Flutter para tecnicos de campo. |
| Infraestructura | Docker Compose, Nginx, CI/CD y despliegue cloud. |
| Documentacion | Manuales, modelos, pruebas, calidad y puesta en marcha. |

## Funcionalidades principales

- Inicio de sesion y control de roles.
- Administracion de usuarios tecnicos.
- Administracion de clientes.
- Creacion y gestion de proyectos.
- Importacion y calibracion de planos.
- Captura de mediciones WiFi.
- Clasificacion de niveles de senal.
- Generacion de mapas de calor.
- Gestion de conjuntos de AP.
- Propuesta IA como conjunto derivado.
- Comparacion entre configuracion actual y propuesta.
- Generacion de enlace cliente.
- Visualizacion web del resultado publicado.

## Criterios de producto terminado

| Criterio | Condicion |
| -------- | --------- |
| Funcional | Flujos principales operan de extremo a extremo. |
| Tecnico | Backend, web, movil y base de datos integrados. |
| Calidad | Pruebas obligatorias ejecutadas sin defectos criticos. |
| Seguridad | Roles, ownership y tokens aplicados. |
| Operacion | Producto accesible en linea y releases moviles disponibles. |
| Documentacion | PAPS, modelos, pruebas, manual de calidad y puesta en marcha completos. |

## Versionado y releases

Cada release debe incluir:

- Numero de version.
- Fecha.
- Cambios principales.
- Correcciones.
- Riesgos conocidos.
- Artefactos moviles.
- Hash o referencia del repositorio.

## Soporte inicial

El soporte se organiza en tres niveles:

| Nivel | Responsable | Alcance |
| ----- | ----------- | ------- |
| N1 | Soporte funcional | Dudas de uso, acceso y flujo basico. |
| N2 | Equipo tecnico | Incidentes reproducibles, errores y configuracion. |
| N3 | Arquitectura/desarrollo | Defectos complejos, seguridad y cambios estructurales. |

## Evidencia de entrega

La entrega final debe presentar:

- Demostracion del frontend publico.
- APK o release movil descargable.
- Repositorio accesible.
- Pruebas ejecutadas.
- Capturas o video de flujos principales.
- Documento consolidado en Word con diagramas y QR.



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

## Releases moviles

<https://github.com/borysinho/wireless-heatmapper/releases>

![QR releases](/home/bquiroga/Documentos/dev/taller/proyecto-final/docs/SW2/assets/qr-releases.png)

