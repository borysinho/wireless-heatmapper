import 'package:dio/dio.dart';

import '../models/analisis_cobertura_model.dart';
import '../models/ap_detectado_model.dart';
import '../models/mapa_calor_model.dart';

class HeatmapRemoteDatasource {
  final Dio _dio;

  const HeatmapRemoteDatasource(this._dio);

  Future<MapaCalorModel> generarHeatmap({
    required int planoId,
    required String algoritmo,
    required int resolucion,
  }) async {
    try {
      final response = await _dio.get<Map<String, dynamic>>(
        '/planos/$planoId/heatmap',
        queryParameters: {
          'algoritmo': algoritmo,
          'resolucion': resolucion,
        },
      );
      return MapaCalorModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<AnalisisCoberturaModel> analizarMapa(int mapaId) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/mapas/$mapaId/analisis',
      );
      return AnalisisCoberturaModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<APDetectadoModel> confirmarAP({
    required int apId,
    required double posX,
    required double posY,
  }) async {
    try {
      final response = await _dio.patch<Map<String, dynamic>>(
        '/aps/$apId',
        data: {'pos_x': posX, 'pos_y': posY, 'confirmado': true},
      );
      return APDetectadoModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  static String _mensajeDesdeError(DioException e) {
    final status = e.response?.statusCode;
    final data = e.response?.data;
    if (status == 422 && data is Map && data['detail'] is String) {
      return data['detail'] as String;
    }
    if (status == 404) return 'Recurso no encontrado.';
    if (status == 401) return 'Sesión expirada.';
    return 'No se pudo procesar el heatmap. Reintenta.';
  }
}

class HeatmapApiException implements Exception {
  final String mensaje;
  final int? statusCode;

  const HeatmapApiException(this.mensaje, {this.statusCode});

  @override
  String toString() => mensaje;
}
