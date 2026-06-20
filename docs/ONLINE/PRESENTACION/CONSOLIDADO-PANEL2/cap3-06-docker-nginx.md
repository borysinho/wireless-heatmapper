## Docker Compose y Nginx para Infraestructura y Despliegue

### Contenerización con Docker

**Docker** es la plataforma de contenerización que permite empaquetar una aplicación junto con todas sus dependencias en una unidad autocontenida denominada **contenedor**. A diferencia de las máquinas virtuales, los contenedores comparten el kernel del sistema operativo anfitrión, lo que los hace significativamente más ligeros y rápidos de arrancar (Docker Inc., 2023).

La contenerización del Wireless HeatMapper tiene las siguientes implicaciones prácticas:

- **Reproducibilidad del entorno:** el entorno de ejecución del backend (Python 3.12, dependencias exactas del `pyproject.toml`) es idéntico en la laptop del desarrollador, en el servidor de CI/CD y en producción. Se elimina el problema "funciona en mi máquina".
- **Aislamiento:** los cuatro servicios del sistema (base de datos, backend, web, proxy) se ejecutan en contenedores aislados que se comunican a través de una red Docker privada. El servicio de base de datos PostgreSQL no está expuesto directamente a Internet; solo el proxy Nginx es accesible desde el exterior.
- **Gestión de versiones de dependencias:** la imagen Docker del backend queda asociada a un tag de versión en el registro de contenedores, permitiendo rollback inmediato a una versión anterior en caso de un despliegue fallido.

### Docker Compose para orquestación multi-servicio

**Docker Compose** es la herramienta que define y orquesta el conjunto de contenedores que componen el Wireless HeatMapper como un sistema integrado. El archivo `docker-compose.yml` declara cuatro servicios:

| Servicio  | Imagen                         | Función                               |
| --------- | ------------------------------ | ------------------------------------- |
| `db`      | `postgres:15-alpine`           | Base de datos PostgreSQL 15           |
| `backend` | `backend:latest` (build local) | API REST FastAPI en Uvicorn           |
| `web`     | `web:latest` (build local)     | Archivos estáticos del frontend React |
| `nginx`   | `nginx:1.25-alpine`            | Reverse proxy, TLS y enrutamiento     |

Los servicios se conectan a través de una red Docker interna privada. Solo el puerto 80/443 de Nginx está expuesto al exterior. La base de datos no tiene puertos expuestos públicamente.

Las variables de entorno sensibles (contraseñas de la base de datos, `SECRET_KEY` para JWT, etc.) se pasan a los contenedores mediante archivos `.env` que no se versionan en Git (están listados en `.gitignore`). Docker Compose carga automáticamente estos archivos en el startup.

### Nginx como reverse proxy

**Nginx** actúa como punto único de entrada al sistema, enrutando las peticiones HTTP/HTTPS según el prefijo de la URL:

| Prefijo de URL | Destino interno                          |
| -------------- | ---------------------------------------- |
| `/api/`        | `backend:8000` (FastAPI)                 |
| `/admin/`      | `web:80` (panel de administración React) |
| `/c/`          | `web:80` (portal de cliente React)       |
| `/`            | `web:80` (página raíz / landing)         |

Este enrutamiento por prefijo es lo que permite que todos los servicios sean accesibles desde el mismo dominio, evitando problemas de CORS (Cross-Origin Resource Sharing) entre el frontend React y el backend FastAPI. Nginx también gestiona la terminación TLS (HTTPS), la compresión gzip de respuestas estáticas y los encabezados de caché para los assets de React.

### GitHub Actions para CI/CD

El pipeline de integración continua y despliegue continuo (CI/CD) está implementado con **GitHub Actions**. En cada push a la rama principal (`main`), el pipeline ejecuta:

1. Lint y formato del código (ruff, prettier, dart analyze).
2. Suite completa de tests del backend (pytest + pytest-cov).
3. Build de la imagen Docker del backend.
4. Push de la imagen al registro de contenedores (GitHub Container Registry).

Este pipeline garantiza que toda versión desplegada en producción ha pasado los controles de calidad automáticos y que la imagen Docker es reproducible desde el código fuente en cualquier momento.
