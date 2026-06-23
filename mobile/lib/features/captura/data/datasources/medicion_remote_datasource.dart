import 'package:dio/dio.dart';

import '../../domain/entities/nivel_senal.dart';
import '../../domain/entities/punto_medicion.dart';
import '../../domain/entities/resultado_escaneo.dart';
import '../../domain/repositories/captura_repository.dart';
import '../../../planos/data/models/plano_model.dart';
import '../../../planos/domain/entities/plano.dart';
import '../models/punto_medicion_model.dart';

/// Datasource remoto de captura. Consume la API REST del backend.
/// Sprint 3 — PB-03 (POST /mediciones) y PB-04 (puntos).
class MedicionRemoteDatasource {
  final Dio _dio;

  const MedicionRemoteDatasource(this._dio);

  /// Envía un lote de mediciones al backend. POST /api/mediciones.
  Future<PuntoMedicion> enviarLote({
    required int planoId,
    required double posX,
    required double posY,
    required List<ResultadoEscaneo> escaneos,
  }) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/mediciones',
        data: {
          'plano_id': planoId,
          'pos_x': posX,
          'pos_y': posY,
          'mediciones': escaneos
              .map((e) => {
                    'ssid': e.ssid,
                    'bssid': e.bssid,
                    'rssi': e.rssi,
                    if (e.canal != null) 'canal': e.canal,
                    if (e.frecuenciaMhz != null)
                      'frecuencia_mhz': e.frecuenciaMhz,
                  })
              .toList(),
        },
      );
      final body = response.data!;
      return PuntoMedicionModel(
        id: body['punto_id'] as int,
        planoId: planoId,
        posX: posX,
        posY: posY,
        nivel: NivelSenal.fromString(body['nivel'] as String),
      );
    } on DioException catch (e) {
      throw CapturaApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  /// Lista los puntos de medición de un plano. GET /api/planos/{id}/puntos.
  Future<List<PuntoMedicion>> listarPuntos(int planoId) async {
    try {
      final response = await _dio.get<List<dynamic>>('/planos/$planoId/puntos');
      return (response.data ?? [])
          .map((e) => PuntoMedicionModel.fromJson(e as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      throw CapturaApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  /// Obtiene el polígono operativo guardado en el plano.
  Future<List<PuntoPlano>> obtenerPoligonoInteres(int planoId) async {
    try {
      final response = await _dio.get<Map<String, dynamic>>('/planos/$planoId');
      return PlanoModel.fromJson(response.data!).poligonoInteres;
    } on DioException catch (e) {
      throw CapturaApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  /// Guarda el polígono operativo del plano.
  Future<List<PuntoPlano>> guardarPoligonoInteres({
    required int planoId,
    required List<PuntoPlano> puntos,
  }) async {
    try {
      final response = await _dio.patch<Map<String, dynamic>>(
        '/planos/$planoId/poligono-interes',
        data: {
          'puntos': puntos.map((p) => {'x': p.x, 'y': p.y}).toList(),
        },
      );
      return PlanoModel.fromJson(response.data!).poligonoInteres;
    } on DioException catch (e) {
      throw CapturaApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  /// Detalle de un punto. GET /api/puntos/{id}.
  Future<PuntoMedicion> obtenerPunto(int puntoId) async {
    try {
      final response = await _dio.get<Map<String, dynamic>>('/puntos/$puntoId');
      return PuntoMedicionModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw CapturaApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  /// Agrega mediciones a un punto existente. POST /api/puntos/{id}/mediciones.
  Future<PuntoMedicion> agregarMediciones({
    required int puntoId,
    required List<ResultadoEscaneo> escaneos,
  }) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/puntos/$puntoId/mediciones',
        data: {
          'mediciones': escaneos
              .map((e) => {
                    'ssid': e.ssid,
                    'bssid': e.bssid,
                    'rssi': e.rssi,
                    if (e.canal != null) 'canal': e.canal,
                    if (e.frecuenciaMhz != null)
                      'frecuencia_mhz': e.frecuenciaMhz,
                  })
              .toList(),
        },
      );
      return PuntoMedicionModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw CapturaApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  /// Mueve un punto existente. PATCH /api/puntos/{id}.
  Future<PuntoMedicion> moverPunto({
    required int puntoId,
    required double posX,
    required double posY,
  }) async {
    try {
      final response = await _dio.patch<Map<String, dynamic>>(
        '/puntos/$puntoId',
        data: {
          'pos_x': posX,
          'pos_y': posY,
        },
      );
      return PuntoMedicionModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw CapturaApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  /// Elimina un punto. DELETE /api/puntos/{id}.
  Future<void> eliminarPunto(int puntoId) async {
    try {
      await _dio.delete<void>('/puntos/$puntoId');
    } on DioException catch (e) {
      throw CapturaApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  static String _mensajeDesdeError(DioException e) {
    final status = e.response?.statusCode;
    final path = e.requestOptions.path;
    if ((status == 404 || status == 405) &&
        path.contains('/poligono-interes')) {
      return 'El servidor de producción no tiene habilitado el guardado de polígonos. Actualiza el backend.';
    }
    if (status == 422) {
      final mensaje = _detalleDesdeRespuesta(e.response?.data);
      return mensaje ?? 'Datos inválidos en la solicitud.';
    }
    if (status == 404) return 'Recurso no encontrado.';
    if (status == 401) return 'Sesión expirada.';
    if (status == 403) return 'No tienes permisos para modificar este recurso.';
    if (status != null && status >= 500) {
      return 'El servidor no pudo procesar la solicitud.';
    }
    return 'Error de red. Reintenta.';
  }

  static String? _detalleDesdeRespuesta(dynamic data) {
    if (data is! Map<String, dynamic>) return null;
    final detail = data['detail'];
    if (detail is String && detail.trim().isNotEmpty) return detail;
    if (detail is List && detail.isNotEmpty) {
      final mensajes = detail
          .map((item) {
            if (item is Map<String, dynamic>) {
              return item['msg']?.toString();
            }
            return item.toString();
          })
          .whereType<String>()
          .where((mensaje) => mensaje.trim().isNotEmpty)
          .toList();
      if (mensajes.isNotEmpty) return mensajes.join(' ');
    }
    return null;
  }
}
