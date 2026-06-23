# Wireless HeatMapper — App Móvil (Flutter)

Cliente móvil Android para relevamiento y análisis de cobertura WiFi.  
**Modalidad: 100 % en línea** — sin base de datos local de dominio, todo persiste en el backend REST.

## Requisitos

- Flutter SDK ≥ 3.6 estable
- Android SDK / emulador (API 26+)
- Backend levantado (ver [README raiz](../README.md))

## Configuración rápida

```bash
# Instalar dependencias
flutter pub get

# Analizar código
flutter analyze

# Ejecutar pruebas unitarias
flutter test

# Debug en emulador Android (backend local vía 10.0.2.2)
flutter run --dart-define-from-file=dart-defines/debug-emulador.json

# Debug en dispositivo físico por cable (backend local vía adb reverse)
adb reverse tcp:8080 tcp:80
flutter run --dart-define-from-file=dart-defines/debug-dispositivo-fisico.json

# Debug apuntando a una IP específica de la red
flutter run --dart-define-from-file=dart-defines/debug-ip.json

# Debug apuntando a producción
flutter run --dart-define-from-file=dart-defines/debug-produccion.json

# Build release (usa la URL de dart-defines/release.json)
flutter build apk --release --dart-define-from-file=dart-defines/release.json
```

## Publicación en GitHub Releases

La app móvil no se despliega en servidor. El APK de producción se publica como
asset en GitHub Releases mediante el workflow **Mobile Release**.

Formas de publicar:

```bash
# Opción recomendada: crear un tag móvil y subirlo
git tag mobile-v1.0.0
git push origin mobile-v1.0.0
```

También se puede ejecutar manualmente desde GitHub Actions → **Mobile Release**,
indicando un `release_tag` como `mobile-v1.0.0`.

El workflow compila con:

```bash
flutter build apk --release --dart-define-from-file=dart-defines/release.json
```

El archivo publicado queda con el nombre `WirelessHeatMapper-<tag>.apk`.

### Secret requerido para Firebase

El archivo `mobile/android/app/google-services.json` no se versiona porque está
ignorado por Git. Para que GitHub Actions pueda construir el APK, crear este
secret del repositorio:

| Secret                                  | Valor recomendado                                      |
| --------------------------------------- | ------------------------------------------------------ |
| `MOBILE_GOOGLE_SERVICES_JSON_BASE64`    | Contenido base64 de `mobile/android/app/google-services.json` |

Generar el valor con:

```bash
base64 -w 0 mobile/android/app/google-services.json
```

Como alternativa, se puede crear `MOBILE_GOOGLE_SERVICES_JSON` con el JSON
crudo completo.

## Arquitectura

```
lib/
  core/
    network/       # DioClient (cliente HTTP REST centralizado)
    navigation/    # AppRouter (go_router)
    security/      # (vacío — el backend maneja bcrypt)
  features/
    auth/          # PB-09: Autenticación (BLoC + datasource remoto)
    proyectos/     # PB-01: Gestión de proyectos (BLoC + datasource remoto)
    planos/        # PB-02: Planos (Sprint 2+)
```

Estructura por capas: `presentation` → `domain` → `data` (Dio → backend REST).

## Variables de entorno

| Variable       | Por defecto           | Descripción               |
| -------------- | --------------------- | ------------------------- |
| `API_BASE_URL` | `http://10.0.2.2/api` | URL base del backend REST |

La app lee este valor desde `AppConfig.apiBaseUrl`. Para cambiar de ambiente,
usar `--dart-define-from-file` con uno de estos perfiles:

| Archivo                                      | Uso                                             |
| -------------------------------------------- | ----------------------------------------------- |
| `dart-defines/debug-emulador.json`           | Debug en emulador Android contra backend local  |
| `dart-defines/debug-dispositivo-fisico.json` | Debug en teléfono por cable con `adb reverse`   |
| `dart-defines/debug-ip.json`                 | Debug contra una IP específica de la red        |
| `dart-defines/debug-produccion.json`         | Debug contra producción                         |
| `dart-defines/release.json`                  | Build release contra producción                 |

Para cambiar la IP de debug por red, modificar solamente `dart-defines/debug-ip.json`.
Para cambiar el dominio de release, modificar solamente `dart-defines/release.json`.
