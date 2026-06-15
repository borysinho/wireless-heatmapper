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

# Ejecutar en desarrollo (usa dart-defines/default.json)
flutter run --dart-define-from-file=dart-defines/default.json

# Ejecutar con URL personalizada
flutter run --dart-define=API_BASE_URL=http://<IP_LOCAL>/api
```

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
| `API_BASE_URL` | `http://10.29.23.250/api` | URL base del backend REST |

La app lee este valor desde `AppConfig.apiBaseUrl`. Para cambiar de ambiente,
usar `--dart-define=API_BASE_URL=...` o actualizar `dart-defines/default.json`.
