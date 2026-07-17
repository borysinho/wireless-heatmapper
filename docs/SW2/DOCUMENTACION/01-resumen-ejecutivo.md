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
