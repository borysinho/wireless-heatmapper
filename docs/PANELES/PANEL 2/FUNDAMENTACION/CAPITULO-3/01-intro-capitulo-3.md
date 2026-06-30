# 3. Arquitectura y Stack Tecnológico del Sistema

Este capítulo desarrolla los conceptos técnicos que sustentan la arquitectura implementada en Wireless HeatMapper. No se reiteran las razones de selección del stack expuestas previamente, sino que se profundiza en la forma en que cada tecnología participa en el comportamiento del sistema y en la interacción entre sus componentes: backend, persistencia, aplicación móvil, panel web, módulo analítico e infraestructura de despliegue.

La revisión se organiza siguiendo el flujo principal de la solución. Primero se examina la capa de servicios REST del backend con FastAPI y el esquema de autenticación basado en JWT. Después se estudia la persistencia relacional con PostgreSQL, SQLAlchemy y Alembic. La tercera y cuarta secciones explican la arquitectura del cliente móvil en Flutter y del panel web en React con TypeScript, ambos integrados con el backend mediante contratos tipados.

El capítulo concluye con la fundamentación del análisis automatizado de cobertura y con la infraestructura de contenedores, proxy reverso y automatización continua. En conjunto, estas tecnologías hacen posible una solución estrictamente en línea, donde la captura, almacenamiento, análisis y visualización de la cobertura WiFi se ejecutan como un sistema coordinado y verificable.

### Referencias

FastAPI. (2024). *FastAPI — Documentación oficial*. Tiangolo. https://fastapi.tiangolo.com/

PostgreSQL Global Development Group. (2024). *PostgreSQL 15 documentation*. https://www.postgresql.org/docs/15/

---
