## PostgreSQL como Base de Datos Central

### Justificación de PostgreSQL

**PostgreSQL** (versión 15+) es el sistema de gestión de bases de datos relacionales (SGBDR) seleccionado como única fuente de verdad del Wireless HeatMapper. La selección de PostgreSQL sobre alternativas como MySQL/MariaDB o bases de datos NoSQL se fundamenta en las siguientes características técnicas:

**Cumplimiento ACID completo.** PostgreSQL garantiza las propiedades de Atomicidad, Consistencia, Aislamiento y Durabilidad (ACID) en todas las transacciones. En el contexto del Wireless HeatMapper, esto asegura que una operación que implique insertar un punto de medición, actualizar el contador de mediciones del proyecto y registrar el timestamp de última actividad sea atómica: o se completan los tres pasos o no se completa ninguno. Esto es crítico para mantener la consistencia referencial de los datos de un proyecto (PostgreSQL Global Development Group, 2023).

**Soporte nativo de tipos geoespaciales.** PostgreSQL ofrece soporte nativo para el tipo `FLOAT[]` y, con la extensión **PostGIS**, para tipos geométricos avanzados. En la versión inicial del Wireless HeatMapper, las coordenadas de los puntos de medición se almacenan como columnas `x FLOAT` e `y FLOAT` (coordenadas normalizadas sobre el plano), sin requerir PostGIS. Sin embargo, la arquitectura está diseñada para migrar a tipos geoespaciales PostGIS en versiones futuras, habilitando consultas espaciales nativas (puntos dentro de un polígono, distancias entre puntos).

**JSON y JSONB.** PostgreSQL soporta almacenamiento de documentos JSON con indexación completa mediante el tipo `JSONB`. El Wireless HeatMapper utiliza este tipo para almacenar el array de resultados del análisis de cobertura (hallazgos de zonas muertas, CCI y ACI) como documentos estructurados dentro de la tabla de análisis, evitando la necesidad de tablas adicionales para datos con estructura variable.

**Integridad referencial con CASCADE.** Las relaciones entre entidades del dominio (proyectos → planos → puntos de medición → mediciones WiFi) se implementan con claves foráneas con `ON DELETE CASCADE`, garantizando que al eliminar un proyecto se eliminen automáticamente todos sus planos y datos asociados sin dejar huérfanos en la base de datos.

### Modelo físico: tablas principales

El esquema relacional del Wireless HeatMapper incluye las siguientes tablas principales:

| Tabla                | Descripción                                                                                        |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| `usuario`            | Cuentas de técnicos y administradores con `password_hash` bcrypt y campo `rol` (ADMIN/TECNICO)     |
| `cliente`            | Catálogo de clientes de Bulldog Tech. (nombre único, estado activo/inactivo)                       |
| `proyecto`           | Proyectos de site survey (nombre, estado, técnico asignado, cliente)                               |
| `plano`              | Planos de edificios asociados a proyectos (URL del archivo en storage, factor de escala calibrado) |
| `punto_medicion`     | Puntos marcados sobre el plano (coordenadas x, y en píxeles y métricas)                            |
| `medicion_wifi`      | Muestras de señal WiFi capturadas (RSSI, SSID, BSSID, canal, frecuencia, timestamp)                |
| `analisis_cobertura` | Resultado del análisis automático de un plano (JSONB con hallazgos de cobertura)                   |
| `heatmap`            | Imagen PNG del heatmap generado (URL en storage, parámetros de interpolación)                      |
| `enlace_cliente`     | Tokens UUID para el portal de cliente (token, expiración, contador de accesos)                     |
| `refresh_token`      | Tokens de renovación de sesión (hash, usuario, expiración, revocado)                               |

### Gestión de migraciones con Alembic

Alembic gestiona la evolución del esquema de base de datos mediante archivos de migración versionados. Cada migración es un script Python con dos funciones: `upgrade()` que aplica los cambios y `downgrade()` que los revierte. El historial de migraciones se almacena en la tabla `alembic_version` de la misma base de datos, garantizando que cualquier entorno (desarrollo, staging, producción) pueda llevar el esquema al estado correcto con un solo comando: `alembic upgrade head`.
