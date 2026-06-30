## 3.1 Arquitectura REST y Framework FastAPI

La arquitectura *Representational State Transfer* (REST, transferencia de estado representacional) organiza la API alrededor de recursos direccionables y operaciones uniformes. En Wireless HeatMapper esto se expresa mediante rutas claras para proyectos, planos, puntos y mediciones, con mensajes autocontenidos y sin estado de sesión persistido en el servidor entre solicitudes. El principio *stateless* (sin estado) simplifica la escalabilidad horizontal y obliga a que cada petición incluya su contexto de autenticación.

La interfaz uniforme se concreta mediante verbos HTTP coherentes con la intención del recurso: `POST` para crear, `GET` para consultar, `PATCH` para actualizar y `DELETE` para remover. El principio de sistema por capas también está presente. El cliente conversa con Nginx, el proxy reenvía al backend y este delega la lógica a routers, esquemas y repositorios. Cuando una respuesta es susceptible de reutilización, como un detalle de recurso, el diseño permite incorporar comportamiento *cacheable* (almacenable en caché) sin alterar el contrato expuesto.

La autenticación se apoya en *JSON Web Token* (JWT, token web JSON). Un JWT contiene tres segmentos: `header`, `payload` y `signature`. El encabezado indica algoritmo y tipo; la carga útil incorpora identidad y reclamos; la firma protege la integridad del token. En el flujo del proyecto, el usuario se autentica una vez, recibe un token de acceso de corta duración y utiliza un mecanismo de renovación para obtener nuevos tokens sin reenviar credenciales en cada operación.

FastAPI aporta dos capacidades decisivas. La primera es la generación automática de contratos OpenAPI 3.0 a partir de tipos Python y modelos declarados. La segunda es su ejecución sobre *Asynchronous Server Gateway Interface* (ASGI, interfaz asíncrona de pasarela para servidores), que permite aprovechar `async` y `await` cuando una operación requiere concurrencia eficiente. Aunque no toda la lógica es asíncrona, el modelo de FastAPI facilita mezclar validación, serialización y enrutamiento con bajo costo ceremonial.

El patrón de inyección de dependencias mediante `Depends()` estructura buena parte del backend. Se utiliza para resolver autenticación, sesiones de base de datos y colaboradores de acceso a datos sin acoplar las funciones de ruta a instancias globales rígidas. Sobre esa base, Pydantic v2 valida esquemas de entrada y salida, convierte tipos, aplica restricciones y serializa respuestas en formatos consistentes.

En la solución implementada, esta fundamentación se observa en la capa de presentación del backend: routers especializados, esquemas para entrada y salida, dependencias para control de acceso y documentación automática de los endpoints que consumen la app móvil y el panel web.

### Referencias

FastAPI. (2024). *FastAPI — Documentación oficial*. Tiangolo. https://fastapi.tiangolo.com/

Fielding, R. T. (2000). *Architectural styles and the design of network-based software architectures* (Doctoral dissertation, University of California, Irvine).

Jones, M., Bradley, J., & Sakimura, N. (2015). *JSON Web Token (JWT)* (RFC 7519). IETF. https://doi.org/10.17487/RFC7519

---
