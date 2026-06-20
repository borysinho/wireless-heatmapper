## 3.6 Infraestructura con Docker Compose, Nginx y CI/CD

Docker encapsula aplicaciones y dependencias dentro de imágenes reproducibles compuestas por capas de sistema de archivos. Cada contenedor aísla procesos, variables y puertos, lo que permite ejecutar servicios heterogéneos con configuración consistente entre desarrollo, pruebas y despliegue. En Wireless HeatMapper este enfoque evita configuraciones manuales divergentes entre backend, base de datos, frontend y proxy.

Docker Compose extiende esa lógica hacia la orquestación local de varios servicios. El archivo de composición del proyecto describe contenedores para `db`, `backend`, `web` y `nginx`, además de volúmenes persistentes para la base de datos y el almacenamiento de planos. Los *healthchecks* (comprobaciones de salud) permiten determinar cuándo un servicio está listo para aceptar conexiones, reduciendo fallos por arranque desordenado entre dependencias.

Nginx actúa como *reverse proxy* (proxy reverso), punto de entrada único para tráfico HTTP y HTTPS. Mediante bloques `upstream` y reglas `proxy_pass`, el servidor separa el tráfico dirigido al backend REST del contenido estático entregado por el frontend. Esta capa también puede centralizar encabezados de seguridad, compresión, límites de carga y terminación TLS cuando el entorno lo exige.

La automatización continua se apoya en GitHub Actions. Un flujo de trabajo en `.github/workflows/ci.yml` puede encadenar validación de código, ejecución de pruebas y construcción de artefactos. En términos de proceso, el pipeline del proyecto sigue la secuencia lógica de `push` a `main`, verificación técnica, construcción de imágenes y preparación para despliegue. Las credenciales sensibles no se fijan en el repositorio; se administran mediante secretos y variables de entorno definidas en el entorno de ejecución.

Esta infraestructura respalda el comportamiento 100 % en línea del sistema. La app móvil, el panel web y el backend no operan como piezas aisladas, sino como servicios coordinados que comparten persistencia, autenticación y un mismo punto de publicación sobre la red.

### Referencias

Docker Inc. (2024). *Docker Compose — Documentación oficial*. https://docs.docker.com/compose/

GitHub. (2024). *GitHub Actions documentation*. https://docs.github.com/actions

Nginx, Inc. (2024). *NGINX admin guide*. https://docs.nginx.com/

---
