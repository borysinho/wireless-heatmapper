import '../../../../core/config/app_config.dart';

/// Resuelve una URL firmada relativa a una URL absoluta consumible por el cliente.
/// El backend devuelve la URL relativa (p. ej. `/planos/archivo/...?exp=&sig=`)
/// cuando `PUBLIC_API_URL` no está configurado en el servidor.
/// Sprint 2 — PB-02.
String resolverUrlFirmada(String urlFirmada) {
  if (urlFirmada.startsWith('http://') || urlFirmada.startsWith('https://')) {
    return urlFirmada;
  }
  if (urlFirmada.startsWith('/')) {
    return '${AppConfig.apiBaseUrl}$urlFirmada';
  }
  return '${AppConfig.apiBaseUrl}/$urlFirmada';
}
