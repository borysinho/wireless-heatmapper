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
| Sitio empresarial Team 24 Software | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/> | Entrada publica institucional, acceso a producto, descargas, soporte y contacto. |
| Panel administrador | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/admin/login> | Acceso para administradores y usuarios autorizados. |
| Portal cliente | `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/portal/{token}` | Acceso por enlace unico generado desde el panel web. |
| API REST | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/> | Base publica de endpoints consumidos por web y movil. |
| Swagger / OpenAPI | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/docs> | Documentacion interactiva de endpoints. |
| Esquema OpenAPI | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api/openapi.json> | Contrato tecnico consumible por herramientas. |
| Manual de usuario | <https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/manual/> | Guia publica de operacion funcional. |
| Releases moviles | <https://github.com/borysinho/wireless-heatmapper/releases> | APK Android generado por GitHub Actions. |

Estas URLs son las referencias publicas para entrega academica, demostracion y continuidad. En anexos se incorporan codigos QR hacia repositorio, sitio empresarial, documentacion OpenAPI, manual de usuario y releases moviles.

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
