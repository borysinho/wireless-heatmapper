/// Configuración central de la app móvil.
///
/// Para producción o cambios de entorno, modificar el valor inyectado con
/// `--dart-define=API_BASE_URL=...` o el archivo `dart-defines/default.json`.
class AppConfig {
  AppConfig._();

  /// Punto único de acceso al backend REST.
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.29.23.250/api',
  );
}
