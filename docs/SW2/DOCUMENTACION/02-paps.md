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

