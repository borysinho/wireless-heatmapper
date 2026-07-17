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
