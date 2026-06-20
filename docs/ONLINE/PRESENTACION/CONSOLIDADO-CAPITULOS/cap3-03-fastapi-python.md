## 3.3 Python y FastAPI para el Backend REST

### 3.3.1 Python como lenguaje de backend

**Python** (versión 3.12 en este proyecto) es el lenguaje seleccionado para el backend por las siguientes razones específicas al contexto del Wireless HeatMapper:

- **Ecosistema científico y de machine learning:** las librerías `numpy`, `scipy`, `scikit-learn` y `tensorflow`/`onnxruntime` —requeridas para el módulo de interpolación espacial (RP3) y el módulo de IA (RP5)— tienen sus implementaciones más maduras y documentadas en Python. Reimplementar estas funciones en otro lenguaje implicaría reinventar soluciones ya probadas en producción.
- **FastAPI** (ver sección siguiente) es nativo de Python y es el framework REST de más alta productividad disponible para ese lenguaje.
- **SQLAlchemy** (ver más abajo) es el ORM más completo del ecosistema Python, con soporte nativo para PostgreSQL avanzado.
- **Type hints nativos:** Python 3.10+ incluye soporte nativo para anotaciones de tipos que FastAPI y Pydantic aprovechan para generar validación automática de datos y documentación OpenAPI.

### 3.3.2 FastAPI como framework REST

**FastAPI** es un framework web moderno para Python, construido sobre Starlette (ASGI) y Pydantic, diseñado específicamente para construir APIs REST de alto rendimiento con mínimo código repetitivo (Ramírez, 2023). Su selección para el Wireless HeatMapper se fundamenta en:

- **Alto rendimiento:** FastAPI está basado en ASGI (Asynchronous Server Gateway Interface) y Uvicorn, lo que le permite manejar cientos de peticiones concurrentes sin bloqueo de hilos. En benchmarks independientes, FastAPI supera en rendimiento a Flask y Django REST Framework, y es comparable a frameworks Node.js como Express.
- **Validación automática con Pydantic v2:** cada endpoint declara sus parámetros de entrada y salida con modelos Pydantic, que validan y serializan automáticamente los datos JSON. Esto elimina código de validación manual y produce errores HTTP 422 descriptivos cuando los datos son inválidos.
- **Generación automática de OpenAPI:** FastAPI genera la especificación OpenAPI 3.0 del API en tiempo de ejecución a partir de los modelos Pydantic y las firmas de las funciones, accesible en `/api/docs` (Swagger UI) y `/api/openapi.json`.
- **Soporte nativo de async/await:** los endpoints FastAPI pueden ser funciones asíncronas (`async def`), lo que permite operaciones de I/O no bloqueantes (lecturas de base de datos, llamadas a servicios externos) sin consumir hilos del sistema operativo.

### 3.3.3 SQLAlchemy 2.x como ORM

**SQLAlchemy** (versión 2.x) es el Object-Relational Mapper (ORM) utilizado para la interacción con la base de datos PostgreSQL. La versión 2.x introduce una API unificada y moderna basada en `select()` declarativo con type annotations, eliminando la ambigüedad entre el estilo _Core_ y el estilo _ORM_ de versiones anteriores (Bayer, 2023).

Las razones para preferir SQLAlchemy sobre SQL directo en el Wireless HeatMapper son:

- **Portabilidad:** si en el futuro se migrara a otra base de datos relacional, solo cambiaría el string de conexión, no el código de acceso a datos.
- **Protección contra inyección SQL:** SQLAlchemy usa parámetros vinculados (`bindparam`) de forma automática, eliminando la clase de vulnerabilidades SQL Injection (OWASP A03:2021) en todos los accesos a datos.
- **Migraciones con Alembic:** la herramienta Alembic, del mismo autor que SQLAlchemy, gestiona las migraciones del esquema de base de datos de forma versionada. Cada migración es un script Python que puede aplicarse (`upgrade`) o revertirse (`downgrade`), garantizando reproducibilidad del esquema en cualquier entorno.

### 3.3.4 Pydantic v2 para validación y serialización

**Pydantic** es la librería de validación de datos integrada en FastAPI. Los esquemas (schemas) Pydantic definen la forma esperada de los cuerpos de petición y respuesta de los endpoints REST. En el Wireless HeatMapper, cada entidad del dominio tiene un conjunto de esquemas Pydantic diferenciados: esquema de creación (campos requeridos al crear), esquema de actualización (campos opcionales) y esquema de respuesta (campos expuestos al cliente, sin `password_hash`). Esta separación explícita es una práctica de seguridad que garantiza que datos sensibles nunca se serialicen en las respuestas.
