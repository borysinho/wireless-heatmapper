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
