# Guía de Ejecución — Wireless HeatMapper

**Cliente:** Bulldog Tech. | **Proyecto:** Ingeniería de Software II — FICCT-UAGRM Grupo 24

---

## Índice

1. [Prerrequisitos](#1-prerrequisitos)
2. [Backend — FastAPI](#2-backend--fastapi)
3. [Web — React + Vite](#3-web--react--vite)
4. [Mobile — Flutter Android](#4-mobile--flutter-android)
5. [Stack completo con Docker Compose](#5-stack-completo-con-docker-compose)
6. [Ejecución en GitHub Actions (CI)](#6-ejecución-en-github-actions-ci)

---

## 1. Prerrequisitos

| Herramienta    | Versión mínima | Verificar con            |
| -------------- | -------------- | ------------------------ |
| Python         | 3.11+          | `python --version`       |
| Node.js        | 22+            | `node --version`         |
| Flutter SDK    | 3.6.0+         | `flutter --version`      |
| Docker         | 24+            | `docker --version`       |
| Docker Compose | 2.20+          | `docker compose version` |
| PostgreSQL     | 15+ (o Docker) | `psql --version`         |

---

## 2. Backend — FastAPI

### 2.1 Desarrollo local

El backend usa un entorno virtual Python ubicado en `backend/.venv/`.

```bash
# 1. Crear entorno virtual (solo la primera vez)
cd backend
python -m venv .venv

# 2. Activar el entorno virtual
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows

# 3. Instalar dependencias (incluye dev: pytest, ruff, httpx)
pip install -e ".[dev]"

# 4. Copiar y configurar variables de entorno
cp ../.env.example .env
# Editar .env con los valores reales (ver sección Variables de entorno)

# 5. Ejecutar migraciones Alembic
alembic upgrade head

# 6. Iniciar el servidor con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor queda disponible en:

- API: `http://localhost:8000`
- Documentación Swagger: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- Health check: `http://localhost:8000/health`

> **Nota:** Para ejecutar pruebas o lint sin activar el entorno, usar la ruta absoluta al binario:
>
> ```bash
> /ruta/al/proyecto/backend/.venv/bin/pytest tests/ -v
> /ruta/al/proyecto/backend/.venv/bin/ruff check .
> ```

### 2.2 Pruebas y lint

```bash
# Con entorno virtual activado:
pytest tests/ -v              # pruebas unitarias
ruff check .                  # lint estático
```

Para la variable `DATABASE_URL` en pruebas se usa SQLite en memoria para no requerir PostgreSQL:

```bash
DATABASE_URL=sqlite:///./test.db pytest tests/ -v
```

### 2.3 Producción

En producción el backend se ejecuta dentro de Docker. No se usa `--reload` ni `DEBUG=true`. El `Dockerfile` en `backend/` tiene dos etapas:

1. **builder** — instala dependencias con pip.
2. **final** — imagen mínima con usuario sin privilegios `appuser`, expone el puerto `8000`.

```bash
# Build manual de la imagen (normalmente lo hace docker compose)
docker build -t heatmapper-backend:latest ./backend

# Verificar el health check
curl http://localhost:8000/health
# → {"status":"ok","version":"0.1.0"}
```

La cadena de conexión usa la red interna de Docker (`db:5432`), no `localhost`.

---

## 3. Web — React + Vite

### 3.1 Desarrollo local

```bash
cd web

# 1. Instalar dependencias (solo la primera vez o al cambiar package.json)
npm install

# 2. Iniciar servidor de desarrollo con hot-reload
npm run dev
```

Queda disponible en `http://localhost:5173`. Las peticiones a `/api/*` se redirigen automáticamente al backend en `http://localhost:8000` gracias al proxy configurado en `vite.config.ts`.

> **Importante:** el backend debe estar corriendo en el puerto `8000` para que el proxy funcione.

### 3.2 Scripts disponibles

| Comando            | Descripción                                    |
| ------------------ | ---------------------------------------------- |
| `npm run dev`      | Servidor de desarrollo con HMR en puerto 5173  |
| `npm run build`    | Compilación TypeScript + bundle Vite para prod |
| `npm run preview`  | Sirve el bundle generado (simula producción)   |
| `npm run lint`     | ESLint sobre todos los archivos `.ts` / `.tsx` |
| `npx tsc --noEmit` | Verificación de tipos sin emitir archivos      |

### 3.3 Producción

El `Dockerfile` en `web/` tiene dos etapas:

1. **builder** — `node:22-alpine`, ejecuta `npm ci` y `npm run build`, genera `dist/`.
2. **final** — `nginx:1.27-alpine`, sirve el contenido estático desde `dist/` con la configuración `nginx-spa.conf` (SPA fallback: todas las rutas apuntan a `index.html`).

El Nginx interno del contenedor `web` escucha en el puerto `80`. El Nginx externo (servicio `nginx`) actúa de reverse proxy y enruta:

- `/api/*` → backend (puerto `8000` interno)
- `/` → web (puerto `80` interno)

Todo el tráfico externo entra por el puerto `80` del host vía el servicio `nginx`.

---

## 4. Mobile — Flutter Android

### 4.1 Desarrollo local

```bash
cd mobile

# 1. Descargar dependencias
flutter pub get

# 2. Verificar que haya un dispositivo/emulador disponible
flutter devices

# 3. Debug en emulador Android (backend local vía 10.0.2.2)
flutter run --dart-define-from-file=dart-defines/debug-emulador.json

# Debug en emulador/dispositivo específico
flutter run -d <device-id> --dart-define-from-file=dart-defines/debug-emulador.json

# Debug en dispositivo físico conectado por cable
adb reverse tcp:8080 tcp:80
flutter run --dart-define-from-file=dart-defines/debug-dispositivo-fisico.json
```

> **Nota:** En el emulador Android, `10.0.2.2` apunta al `localhost` de la máquina anfitriona. En dispositivo físico por cable, `adb reverse tcp:8080 tcp:80` permite que la app use `http://127.0.0.1:8080/api` y llegue al Nginx local del host.

### 4.2 Análisis y pruebas

```bash
flutter analyze --fatal-infos   # análisis estático (0 warnings permitidos)
flutter test                    # pruebas unitarias y de widget
flutter test --coverage         # pruebas + reporte de cobertura en coverage/lcov.info
```

### 4.3 Build de producción

```bash
# APK estándar (para distribución directa)
flutter build apk --release --dart-define-from-file=dart-defines/release.json

# APK split por ABI (menor tamaño, recomendado)
flutter build apk --release --split-per-abi --dart-define-from-file=dart-defines/release.json

# App Bundle para Google Play
flutter build appbundle --release --dart-define-from-file=dart-defines/release.json
```

Los artefactos se generan en `mobile/build/app/outputs/`:

- APK: `flutter-apk/app-release.apk`
- Bundle: `bundle/release/app-release.aab`

> La app móvil se conecta al backend mediante la URL configurada. En producción apunta al dominio real donde esté desplegado el stack Docker.

---

## 5. Stack completo con Docker Compose

### 5.1 Variables de entorno

```bash
# En la raíz del proyecto
cp .env.example .env
```

Editar `.env` con valores reales:

```env
POSTGRES_DB=heatmapper
POSTGRES_USER=heatmapper_user
POSTGRES_PASSWORD=contrasena_segura_aqui

DATABASE_URL=postgresql://heatmapper_user:contrasena_segura_aqui@db:5432/heatmapper
SECRET_KEY=clave_secreta_aleatoria_de_al_menos_32_caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

VITE_API_BASE_URL=http://localhost/api
```

> `SECRET_KEY` puede generarse con: `python -c "import secrets; print(secrets.token_hex(32))"`

### 5.2 Desarrollo (con hot-reload)

Docker Compose aplica automáticamente `docker-compose.override.yml` en modo desarrollo, que:

- Monta `./backend` como volumen → el código se refleja sin rebuild.
- Inicia uvicorn con `--reload`.
- Monta `./web` como volumen → Vite sirve en modo dev con HMR.

```bash
# Levantar todos los servicios en modo desarrollo
docker compose up --build

# En segundo plano
docker compose up --build -d

# Ver logs de un servicio
docker compose logs -f backend
docker compose logs -f web

# Detener
docker compose down

# Detener y eliminar volúmenes (borra la BD)
docker compose down -v
```

Acceso una vez levantado:

| Servicio     | URL                           |
| ------------ | ----------------------------- |
| Web (React)  | `http://localhost`            |
| API REST     | `http://localhost/api`        |
| Swagger UI   | `http://localhost/api/docs`   |
| Health check | `http://localhost/api/health` |

### 5.3 Producción

Para producción se ignora el override file con `-f`:

```bash
# Solo usa docker-compose.yml (sin override de desarrollo)
docker compose -f docker-compose.yml up --build -d

# Ejecutar migraciones de base de datos antes de levantar el backend
docker compose -f docker-compose.yml run --rm backend alembic upgrade head

# Verificar que todos los servicios están saludables
docker compose -f docker-compose.yml ps
```

### 5.4 Diagrama de red interna

```
                     Puerto 80 (host)
                           │
                    ┌──────┴──────┐
                    │    nginx    │ ← reverse proxy
                    └──────┬──────┘
                    /api/  │  /
              ┌────────────┼────────────┐
              ▼            │            ▼
        ┌──────────┐       │      ┌──────────┐
        │ backend  │       │      │   web    │
        │ :8000    │       │      │  :80     │
        └────┬─────┘       │      └──────────┘
             │  heatmapper-net
             ▼
        ┌──────────┐
        │    db    │
        │ :5432    │
        └──────────┘
```

---

## 6. Ejecución en GitHub Actions (CI)

Los tres workflows se ubican en `.github/workflows/` y se disparan automáticamente en cada `push` o `pull_request` que toque archivos del componente correspondiente.

### 6.1 Mobile CI (`mobile-ci.yml`)

**Disparador:** cambios en `mobile/**`

```
Pasos que ejecuta GitHub:
  1. actions/checkout@v4          — clona el repositorio
  2. subosito/flutter-action@v2   — instala Flutter SDK (canal stable, con caché)
  3. flutter pub get              — descarga dependencias
  4. flutter analyze --fatal-infos — análisis estático (falla si hay warnings)
  5. flutter test --coverage       — pruebas unitarias + reporte de cobertura
```

Para dispararlo manualmente desde GitHub:

- Ir a **Actions → Mobile CI → Run workflow** (si se configura `workflow_dispatch`).
- O hacer un `push` que modifique cualquier archivo dentro de `mobile/`.

### 6.2 Backend CI (`backend-ci.yml`)

**Disparador:** cambios en `backend/**`

```
Pasos que ejecuta GitHub:
  1. actions/checkout@v4
  2. actions/setup-python@v5       — Python 3.12 con caché pip
  3. pip install -e ".[dev]"       — instala app + dependencias dev
  4. ruff check .                  — lint estático
  5. pytest tests/ -v              — pruebas unitarias
     (DATABASE_URL=sqlite:///./test.db — sin necesidad de PostgreSQL)
```

> El CI usa SQLite para las pruebas, evitando levantar un contenedor PostgreSQL en cada ejecución.

### 6.3 Web CI (`web-ci.yml`)

**Disparador:** cambios en `web/**`

```
Pasos que ejecuta GitHub:
  1. actions/checkout@v4
  2. actions/setup-node@v4         — Node.js 22 con caché npm
  3. npm ci                        — instalación reproducible de dependencias
  4. npx tsc --noEmit              — verificación de tipos TypeScript (sin emitir)
  5. npm run build                 — build de producción (falla si hay errores TS o Vite)
```

### 6.4 Ver resultados en GitHub

1. Ir al repositorio en GitHub.
2. Clic en la pestaña **Actions**.
3. Seleccionar el workflow: `Mobile CI`, `Backend CI` o `Web CI`.
4. Cada ejecución muestra el log completo de cada paso.
5. Un check verde (✓) indica que lint + pruebas + build pasaron correctamente.

### 6.5 Badge de estado (opcional)

Para mostrar el estado del CI en el README:

```markdown
![Mobile CI](https://github.com/<org>/<repo>/actions/workflows/mobile-ci.yml/badge.svg)
![Backend CI](https://github.com/<org>/<repo>/actions/workflows/backend-ci.yml/badge.svg)
![Web CI](https://github.com/<org>/<repo>/actions/workflows/web-ci.yml/badge.svg)
```

---

## Resumen rápido de comandos

| Componente | Desarrollo                      | Producción                                           |
| ---------- | ------------------------------- | ---------------------------------------------------- |
| Backend    | `uvicorn app.main:app --reload` | `docker compose -f docker-compose.yml up`            |
| Web        | `npm run dev` (puerto 5173)     | `docker compose -f docker-compose.yml up`            |
| Mobile     | Ver §4.1                        | Ver §4.3                                             |
| Stack full | `docker compose up --build`     | `docker compose -f docker-compose.yml up --build -d` |
