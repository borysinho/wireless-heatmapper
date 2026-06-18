/// Configuración central de la app móvil.
///
/// La URL base se inyecta en tiempo de compilación con
/// `--dart-define-from-file=dart-defines/<perfil>.json`.
class AppConfig {
  AppConfig._();

  /// Punto único de acceso al backend REST.
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2/api',
  );
}
