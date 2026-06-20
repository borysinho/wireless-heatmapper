# 8. Objetivos

## 8.1 Objetivo General

Desarrollar un sistema integrado de levantamiento y visualización de cobertura Wi-Fi, compuesto por una aplicación móvil Android, un backend REST con módulo de inteligencia artificial y una plataforma web de administración, que permita a Bulldog Tech. diagnosticar, documentar y optimizar la distribución de su red inalámbrica mediante mapas de calor georreferenciados y análisis automatizado.

---

## 8.2 Objetivos Específicos

1. **Diseñar e implementar el backend REST** con FastAPI y PostgreSQL que gestione la autenticación de usuarios, la administración de clientes y proyectos, y el almacenamiento centralizado de mediciones Wi-Fi.
   - *Entregable:* API REST funcional con endpoints documentados y base de datos relacional normalizada.

2. **Desarrollar la aplicación móvil Android** con Flutter que permita al técnico autenticarse, seleccionar un proyecto, y recolectar mediciones de RSSI georreferenciadas sobre el plano de planta de la instalación.
   - *Entregable:* Aplicación Flutter con módulos de autenticación y levantamiento de señal operativos.

3. **Construir el panel web de administración** con React y TypeScript que permita gestionar usuarios, clientes, proyectos y visualizar los mapas de calor generados.
   - *Entregable:* Aplicación web funcional con autenticación, CRUD de entidades principales y visualización de resultados.

4. **Integrar un módulo de inteligencia artificial** en el backend capaz de analizar los datos de cobertura recolectados y generar recomendaciones de optimización de la red.
   - *Entregable:* Módulo de IA con al menos un modelo de análisis validado y endpoint de recomendaciones funcional.

5. **Definir y documentar la arquitectura de despliegue** del sistema mediante Docker Compose y GitHub Actions, garantizando la reproducibilidad del entorno en producción.
   - *Entregable:* Archivo `docker-compose.yml` funcional con todos los servicios orquestados y pipeline de CI/CD configurado.

---
