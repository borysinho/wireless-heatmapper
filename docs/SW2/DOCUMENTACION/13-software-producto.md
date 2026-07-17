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

