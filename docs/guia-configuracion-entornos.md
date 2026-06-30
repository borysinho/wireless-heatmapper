# Guía de configuración de entornos — Web y Mobile

Describe cómo apuntar el servidor de desarrollo Vite y la app Flutter hacia distintos hosts
del backend sin modificar el código fuente.

---

## Web (Vite dev server)

El proxy del servidor de desarrollo lee la variable `VITE_PROXY_TARGET` desde el archivo
`web/.env.local` (ignorado por git). Si la variable no existe, el fallback en
`web/vite.config.ts` es `http://localhost:8000`.

### Entorno por defecto (Docker local / emulador)

Eliminar o no crear `web/.env.local`. El proxy apuntará a `http://localhost:8000`.

### Entorno de pruebas (host remoto)

Crear `web/.env.local` con el target deseado:

```env
VITE_PROXY_TARGET=http://10.138.57.250:8000
```

> El backend expone el puerto 8000 directamente en el host cuando se levanta con
> `docker-compose.override.yml` (modo desarrollo).

---

## Mobile (Flutter)

La URL base de la API se inyecta en tiempo de compilación mediante `--dart-define-from-file`.
Los archivos de configuración están versionados en `mobile/dart-defines/`.

| Archivo                                      | `API_BASE_URL`                                                        | Cuándo usar                                      |
| -------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------ |
| `dart-defines/debug-emulador.json`           | `http://10.0.2.2/api`                                                 | Debug en emulador Android (localhost del host)   |
| `dart-defines/debug-dispositivo-fisico.json` | `http://127.0.0.1:8080/api`                                           | Debug en teléfono por cable con `adb reverse`    |
| `dart-defines/debug-ip.json`                 | Configurado en el archivo                                             | Debug contra una IP específica de la red         |
| `dart-defines/debug-produccion.json`         | `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api`      | Debug contra producción                          |
| `dart-defines/release.json`                  | `https://wireless-heatmapper-g24.eastus2.cloudapp.azure.com/api`      | Build release / producción                       |

`dart-defines/default.json` se conserva como alias del perfil de emulador para
compatibilidad con comandos antiguos.

### Comandos de ejecución

```bash
# Debug en emulador Android
flutter run --dart-define-from-file=dart-defines/debug-emulador.json

# Debug en dispositivo físico conectado por cable
adb reverse tcp:8080 tcp:80
flutter run --dart-define-from-file=dart-defines/debug-dispositivo-fisico.json

# Debug apuntando a una IP específica
flutter run --dart-define-from-file=dart-defines/debug-ip.json

# Debug apuntando a producción
flutter run --dart-define-from-file=dart-defines/debug-produccion.json

# Release
flutter build apk --release --dart-define-from-file=dart-defines/release.json
```

### Desde VS Code

El archivo `.vscode/launch.json` en la raíz del proyecto define configuraciones
seleccionables desde el panel **Run & Debug**:

- **Flutter — debug emulador** → `dart-defines/debug-emulador.json`
- **Flutter — debug dispositivo físico** → `dart-defines/debug-dispositivo-fisico.json` + task `adb reverse tcp:8080 tcp:80`
- **Flutter — debug IP específica** → `dart-defines/debug-ip.json`
- **Flutter — debug producción** → `dart-defines/debug-produccion.json`
- **Flutter — release** → `dart-defines/release.json` + `--release`

Para cambiar el dominio del entorno release, modificar solamente
`mobile/dart-defines/release.json`. Para debug en dispositivo físico por cable no
se modifica ninguna IP: el teléfono accede a `127.0.0.1:8080` y ADB redirige ese
puerto hacia el Nginx local del host (`localhost:80`).

---

## Agregar un nuevo entorno

1. Crear `mobile/dart-defines/<nombre>.json` con la `API_BASE_URL` correspondiente.
2. Crear (o actualizar) `web/.env.local` con el `VITE_PROXY_TARGET` del nuevo host.
3. Agregar la configuración en `.vscode/launch.json` si se desea acceso rápido desde el IDE.

No modificar `web/vite.config.ts` ni `mobile/lib/core/network/dio_client.dart`; esos
archivos solo definen los valores por defecto y la lógica de carga.
