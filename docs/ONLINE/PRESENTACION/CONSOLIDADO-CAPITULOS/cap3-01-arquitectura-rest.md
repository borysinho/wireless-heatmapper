## 3.1 Arquitectura del Sistema: Cliente-Servidor y API REST

### 3.1.1 El modelo cliente-servidor

El **modelo cliente-servidor** es una arquitectura de red en la que las responsabilidades de procesamiento se dividen entre dos categorías de participantes: los **clientes**, que solicitan recursos o servicios, y el **servidor**, que los proporciona. Esta separación de responsabilidades ofrece ventajas fundamentales para el Wireless HeatMapper:

- **Centralización de la lógica de negocio:** toda la lógica de análisis (interpolación, detección de zonas muertas, módulo de IA) reside en el servidor, no en los dispositivos cliente. Esto permite actualizarla sin necesidad de actualizar la aplicación móvil.
- **Persistencia centralizada:** existe una única fuente de verdad sobre PostgreSQL, accesible desde la app móvil, el panel web y el portal de cliente. No hay sincronización ni conflictos de datos entre dispositivos.
- **Cliente delgado:** la aplicación móvil Android es un cliente delgado que no almacena estado de dominio entre sesiones. Todo su comportamiento depende de los datos que recibe del servidor en cada sesión.

### 3.1.2 API REST y HTTP

El Wireless HeatMapper adopta el estilo arquitectónico **REST** (Representational State Transfer) para la comunicación entre clientes y servidor. REST es un conjunto de restricciones arquitectónicas aplicadas sobre el protocolo HTTP que produce interfaces predecibles, escalables y desacopladas (Fielding, 2000). Las restricciones REST relevantes para el proyecto son:

- **Interfaz uniforme:** los recursos (proyectos, planos, mediciones, usuarios) se identifican por URLs estables y se manipulan con los verbos estándar de HTTP (GET, POST, PUT, PATCH, DELETE).
- **Sin estado (stateless):** cada petición HTTP contiene toda la información necesaria para procesarla; el servidor no mantiene estado de sesión entre peticiones. La autenticación se delega al token JWT incluido en el encabezado `Authorization` de cada petición.
- **Caché:** las respuestas del servidor pueden indicar si son cacheables, reduciendo la carga del backend para datos que no cambian frecuentemente (por ejemplo, el plano de un proyecto ya cerrado).
- **Sistema en capas:** la presencia de Nginx como reverse proxy entre el cliente y el backend es transparente para el cliente REST; Nginx añade terminación TLS, balanceo de carga y enrutamiento por prefijo de URL sin que los clientes necesiten conocer la topología interna del servidor.

### 3.1.3 OpenAPI y documentación automática

El backend FastAPI genera automáticamente una especificación **OpenAPI 3.0** (anteriormente Swagger) a partir de los tipos y anotaciones del código Python. Esta especificación es el contrato formal entre el backend y los clientes (app móvil y web). El cliente web TypeScript consume la especificación para generar tipos TypeScript automáticos con `openapi-typescript`, garantizando consistencia en tiempo de compilación entre los contratos del backend y el código del frontend.
