## Tecnología

### Estrategia

El proyecto adopta el **marco de trabajo Scrum**. Scrum se selecciona porque es un marco iterativo e incremental que se adapta a proyectos de cuatro a seis meses, permite entregar valor de forma temprana al cliente real (Bulldog Tech.) y está diseñado para equipos pequeños multifuncionales y autogestionados (en este caso, dos personas que cubren los roles de Scrum Master, Product Owner y Developer simultáneamente). La estrategia Scrum se complementa con las cuatro actividades obligatorias de la ingeniería de software (análisis, diseño, implementación y pruebas) y se materializa en cinco eventos —**R-1** Definición Inicial, **R-2** Sprint Planning, **R-3** Ejecución (con Daily Scrum), **R-4** Sprint Review y **R-5** Sprint Retrospective— y tres artefactos —**F3** Product Backlog, **F4** Historias de Usuario y **F5** Sprint Backlog—.

### Métodos

- **Lenguaje de modelado:** UML 2.5+ con la herramienta **StarUML** y diagramas embebidos en formato **PlantUML** dentro de los documentos Markdown, para garantizar diagramas versionables en Git y renderizables tanto en VS Code como en la cadena de generación del Word final.
- **Modelado de Casos de Uso (UC01–UC19):** diagrama de Contexto del sistema, conforme al estándar UML.
- **Modelado de Arquitectura:** diagrama de Paquetes en cuatro capas y diagrama de Despliegue de los contenedores Docker.
- **Modelado de Datos:** diagrama de Clases conceptual, esquema lógico relacional y diseño físico PostgreSQL.
- **Modelado de Lógica:** diagramas de Secuencia y de Estados para las HU con flujo de negocio complejo.
- **Estimación de tamaño y esfuerzo:** Métricas de Pressman (KLDC, Puntos de Función), modelo COCOMO II y Ecuación del Software de Putnam–Myers; estimación de PHU mediante **Planning Poker** con escala de Fibonacci (1, 2, 3, 5, 8, 13, 21).
- **Algoritmos de IA y procesamiento de señal:** interpolación espacial (Inverse Distance Weighting / Kriging) en el backend, y modelo de aprendizaje supervisado para recomendación de posicionamiento de APs (entrenamiento con datasets sintéticos y reales de propagación de señal).
- **Fundamento técnico WiFi:** marco de referencia **CWNA-107**, con umbrales operativos RSSI ≥ −70 dBm para diseño objetivo y < −90 dBm para zona muerta.

### Herramientas

#### Herramientas de Software

| Categoría                   | Herramienta                                                                   |
| --------------------------- | ----------------------------------------------------------------------------- |
| Control de versiones        | Git, GitHub                                                                   |
| Gestión del Product Backlog | Notion (sincronizado con scripts Python), GitHub Projects                     |
| Modelado UML                | StarUML 6, PlantUML (embebido en Markdown)                                    |
| Diseño UI/UX                | Figma (prototipos), Material 3 Design Kit                                     |
| Lenguaje móvil              | Dart                                                                          |
| Framework móvil             | Flutter SDK 3.x · BLoC/Cubit · Dio · go_router · flutter_secure_storage       |
| Lenguaje backend            | Python 3.12                                                                   |
| Framework backend           | FastAPI · SQLAlchemy 2.x · Alembic · python-jose (JWT) · bcrypt               |
| Lenguaje web                | TypeScript 5.x                                                                |
| Framework web               | React 18 + Vite + TanStack Query + axios + react-router-dom + react-hook-form |
| Estilo web                  | CSS Modules + tokens de color/tipografía (Poppins, Inter)                     |
| Base de datos               | PostgreSQL 15+                                                                |
| Contenerización             | Docker · Docker Compose                                                       |
| Reverse proxy / TLS         | Nginx (`/api → backend`, `/admin → web`, `/ → portal cliente`)                |
| Calidad de código (backend) | ruff, ruff-format, pytest, pytest-cov                                         |
| Calidad de código (web)     | ESLint, Prettier, Vitest                                                      |
| Calidad de código (móvil)   | dart analyze, dart format, flutter test                                       |
| Pre-commit hooks            | pre-commit (ruff, prettier, eslint, dart format)                              |
| CI/CD                       | GitHub Actions (lint + tests + build de imagen Docker + push)                 |
| Editor / IDE                | Visual Studio Code · Android Studio · DataGrip                                |
| Documentación               | Markdown · Pandoc (generación del .docx final) · LaTeX (opcional)             |
| Modelo de IA                | scikit-learn · TensorFlow / ONNX Runtime (despliegue en backend)              |
| Servidor cloud              | VPS Linux (Render, Fly.io o equivalente)                                      |

#### Herramientas de Hardware

- **Computadoras portátiles de desarrollo (×2):** equipos de los autores con Linux/macOS, mínimo 16 GB de RAM, para ejecutar Docker Compose, Android emulator y entornos de desarrollo simultáneos.
- **Smartphones Android (×2)** con API ≥ 26 (Android 8.0 Oreo) para pruebas en dispositivo físico (siempre en línea).
- **Enrutadores WiFi de prueba (×2)** para construir entornos controlados de validación del algoritmo de interpolación y del módulo de análisis de cobertura.
- **Impresora** para impresión de planos durante pruebas de campo en instalaciones reales de Bulldog Tech.
