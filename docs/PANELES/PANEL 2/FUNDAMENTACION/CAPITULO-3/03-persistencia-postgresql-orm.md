## 3.2 Persistencia con PostgreSQL, SQLAlchemy y Alembic

PostgreSQL 15 constituye la fuente central de verdad del sistema. Su modelo transaccional ACID garantiza atomicidad, consistencia, aislamiento y durabilidad, propiedades indispensables cuando una misma operación debe registrar un punto de medición y varias lecturas WiFi como un único lote coherente. En este proyecto también resultan relevantes tipos como `NUMERIC` o `FLOAT` para factores de escala, `BYTEA` cuando se requiere almacenar binarios en otros escenarios, y `TIMESTAMP WITH TIME ZONE` para auditar eventos desde diferentes clientes sin perder referencia temporal uniforme.

Sobre el motor relacional se aplica la capa *Object-Relational Mapper* (ORM, mapeador objeto-relacional). El ORM no reemplaza el modelo de dominio, pero reduce fricción entre objetos de aplicación y tablas persistentes. En Wireless HeatMapper el patrón Repository encapsula consultas y reglas de acceso a datos, mientras que la unidad transaccional se conserva en la sesión SQLAlchemy, siguiendo la lógica de una *Unit of Work* (unidad de trabajo) controlada por solicitud.

SQLAlchemy resuelve el mapeo de entidades, relaciones y ciclo de vida de objetos persistidos. La gestión de `Session` delimita cuándo una transacción inicia, confirma o revierte cambios. A su vez, la distinción entre *lazy loading* (carga diferida) y *eager loading* (carga anticipada) permite equilibrar simplicidad y rendimiento según el caso. Relaciones declaradas con `relationship()` enlazan proyectos con planos, planos con puntos y puntos con mediciones, manteniendo integridad de cascada cuando el modelo así lo exige.

Alembic extiende esta arquitectura al versionado del esquema. Cada migración se registra como código reproducible, trazable y reversible. El modo `autogenerate` acelera la detección de cambios estructurales, aunque la revisión manual sigue siendo necesaria para asegurar nombres, tipos y restricciones coherentes. En el proyecto, la migración inicial establece la base del sistema; la migración `a1b2c3d4e5f6` introduce la entidad de planos y sus campos de calibración; y las migraciones `c3d4e5f6a7b8` y `d5e6f7a8b9c0` incorporan el modelo de mediciones y el campo `numero_lectura` para sesiones continuas.

Esta capa tecnológica define la persistencia del backend. Gracias a ella, la lógica de negocio puede operar sobre entidades del dominio sin perder control sobre transacciones, claves foráneas, cascadas de borrado ni evolución incremental del esquema de base de datos.

### Referencias

Alembic. (2024). *Alembic documentation*. SQLAlchemy authors. https://alembic.sqlalchemy.org/

PostgreSQL Global Development Group. (2024). *PostgreSQL 15 documentation*. https://www.postgresql.org/docs/15/

SQLAlchemy. (2024). *SQLAlchemy 2.0 documentation*. https://docs.sqlalchemy.org/

---
