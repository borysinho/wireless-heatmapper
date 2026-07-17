# Prompts secuenciales para documentacion SW2

## Instrucciones globales

Ejecuta los prompts en el orden indicado. Cada respuesta debe producir o actualizar un archivo Markdown independiente en `docs/SW2/DOCUMENTACION/`, manteniendo lenguaje formal academico en espanol, formato compatible con APA, tablas Markdown estables y diagramas UML 2.5+ en PlantUML cuando corresponda.

Reglas obligatorias para todos los prompts:

- No mencionar rutas internas, nombres de archivos de trabajo ni notas privadas usadas como insumo.
- Mantener el proyecto como modalidad 100 % en linea: cliente movil delgado, backend REST como fuente de verdad y PostgreSQL como persistencia central.
- Usar "Team 24 Software" como empresa de software y "Bulldog Tech." como cliente del caso.
- Preservar los umbrales tecnicos: RSSI < -90 dBm como zona muerta, objetivo de diseno >= -70 dBm, Android >= 8.0 con throttling de 4 escaneos cada 2 minutos.
- Cuando se requieran diagramas, generar PlantUML formal compatible con UML 2.5+.
- Cuando se usen datos legales, costos de cloud, cuentas de tiendas o fuentes externas, citar fuentes oficiales o institucionales.
- Mantener trazabilidad entre requerimientos, historias de usuario, modelos, pruebas y producto entregado.

## Prompt 01 - Portada y control documental

Genera `00-portada.md` con portada academica para Ingenieria de Software II, incluyendo universidad, facultad, materia, grupo, empresa simulada, proyecto, cliente, integrantes, docente, ciudad, gestion 2026, version del documento, control de cambios y declaracion de modalidad 100 % en linea.

## Prompt 02 - Resumen ejecutivo

Genera `01-resumen-ejecutivo.md` con una sintesis formal del problema, solucion, alcance del producto, valor para Bulldog Tech., componentes entregados, modalidad operativa y estructura de los doce puntos documentales solicitados por la materia.

## Prompt 03 - PAPS

Genera `02-paps.md` como version adaptada del Plan Aplicado a Proyecto de Software para SW2. Debe incluir problema, situacion deseada, objetivos, alcance, restricciones, requerimientos principales, stack tecnologico, cronograma por sprints y criterios de aceptacion, sin copiar contenido redundante.

## Prompt 04 - Modelos de desarrollo

Genera `03-modelos-desarrollo.md` con los cuatro modelos obligatorios: contexto, arquitectura, datos y logica. Debe explicar cada modelo, listar sus diagramas y enlazar los bloques PlantUML correspondientes en `docs/SW2/diagramas/`.

## Prompt 05 - Manual de garantia de calidad

Genera `04-manual-calidad.md` como manual institucional de calidad para Team 24 Software. Debe basarse en ISO/IEC 90003 e IEEE 730, orientarse a la empresa de software y no solamente al producto. Debe incluir mision, vision, politica de calidad, roles, procesos, registros, metricas, auditoria, no conformidades y mejora continua.

## Prompt 06 - Herramientas CASE

Genera `05-herramientas-case.md` demostrando uso real de herramientas CASE. Debe explicar navegabilidad entre modelos, trazabilidad entre casos de uso, secuencias, clases, datos y despliegue, y proponer evidencias de demostracion en StarUML/PlantUML.

## Prompt 07 - Aspectos legales

Genera `06-aspectos-legales.md` con los tramites para apertura de una empresa de software en Bolivia: tipo societario recomendado, registro de comercio, NIT, patente municipal, obligaciones tributarias, registro de derecho de autor de software, contratos, datos personales y responsabilidades administrativas.

## Prompt 08 - Infraestructura para produccion

Genera `07-infraestructura-produccion.md` describiendo gestion de proyecto, repositorio, ramas, control de configuracion, CI/CD, Docker, Nginx, base de datos, ambientes, seguridad operativa, monitoreo, backups e IA integrada al desarrollo.

## Prompt 09 - Sitio web de la empresa

Genera `08-sitio-web-empresa.md` describiendo el sitio publico de Team 24 Software, publicado en linea, con secciones de empresa, servicios, producto, descargas, soporte, contacto, chatbot entrenado y politicas de mantenimiento del contenido.

## Prompt 10 - Estudio de mercado

Genera `09-estudio-mercado.md` con cuantificacion del mercado, segmentos, clientes objetivo, competidores, problema economico, propuesta de valor, precios, monetizacion, proyeccion de ingresos, costos y riesgos comerciales. Toda conclusion debe tener base numerica o declararse como supuesto verificable.

## Prompt 11 - Pruebas del software

Genera `10-plan-pruebas.md` aplicando el flujo de trabajo de pruebas del Proceso Unificado, tres niveles de prueba (desarrollador, QA y Product Owner), pruebas de caja blanca por camino basico para al menos cuatro metodos con complejidad ciclomatica >= 3, checklists, rendimiento, seguridad y evidencias de herramientas.

## Prompt 12 - Marketing

Genera `11-marketing.md` con objetivos, publicos, posicionamiento, canales, calendario, piezas promocionales, demo, ferias, redes sociales, metricas y presupuesto inicial para promover Team 24 Software y Wireless HeatMapper.

## Prompt 13 - Puesta en marcha

Genera `12-puesta-marcha.md` con comparacion de AWS, Google Cloud y Azure, proyeccion de costos, decision de plataforma, requisitos de cuentas de Google Play y Apple Developer, licenciamiento SaaS, terminos y condiciones, politica de privacidad y adopcion asistida por IA.

## Prompt 14 - Software como producto

Genera `13-software-producto.md` documentando el producto final: componentes backend, web y movil, funcionalidades, URLs publicas, releases moviles, repositorio, criterios de entrega, soporte, versionado y evidencias de funcionamiento.

## Prompt 15 - Bibliografia

Genera `14-bibliografia.md` con referencias en formato APA 7 de fuentes tecnicas, normativas, legales, herramientas, cloud, tiendas de aplicaciones y referencias WiFi.

## Prompt 16 - Anexos

Genera `15-anexos.md` con tabla de codigos QR, glosario, matriz de trazabilidad resumida, checklists, lista de diagramas, evidencias esperadas y guia de consolidacion a Word.

## Prompt 17 - Validacion final

Revisa todos los documentos generados y verifica que:

- Los doce puntos exigidos esten cubiertos.
- Existan diagramas PlantUML para los modelos y flujos principales.
- Las fuentes externas esten citadas.
- Las URLs publicas esten incluidas con QR.
- El texto no referencie archivos internos como fuente academica.
- El documento pueda consolidarse con `_build_docx.sh`.

