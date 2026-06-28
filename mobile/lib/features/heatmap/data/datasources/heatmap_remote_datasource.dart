import 'package:dio/dio.dart';

import '../models/ap_disponible_model.dart';
import '../models/conjunto_ap_model.dart';
import '../models/inventario_rf_model.dart';
import '../models/mapa_calor_model.dart';

class HeatmapRemoteDatasource {
  final Dio _dio;

  const HeatmapRemoteDatasource(this._dio);

  Future<List<APDisponibleModel>> listarAPsDisponibles(int planoId) async {
    try {
      final response = await _dio.get<List<dynamic>>('/planos/$planoId/aps');
      return (response.data ?? [])
          .map((e) => APDisponibleModel.fromJson(e as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<List<ConjuntoAPModel>> listarConjuntosAP(int planoId) async {
    try {
      final response = await _dio.get<List<dynamic>>(
        '/planos/$planoId/conjuntos-ap',
      );
      return (response.data ?? [])
          .map((e) => ConjuntoAPModel.fromJson(e as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<ConjuntoAPModel> crearConjuntoAP({
    required int planoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required List<String> bssids,
  }) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/planos/$planoId/conjuntos-ap',
        data: {
          'nombre': nombre,
          'proposito': proposito,
          'descripcion': descripcion,
          'bssids': bssids,
        },
      );
      return ConjuntoAPModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<ConjuntoAPModel> actualizarConjuntoAP({
    required int conjuntoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required List<String> bssids,
  }) async {
    try {
      final response = await _dio.patch<Map<String, dynamic>>(
        '/conjuntos-ap/$conjuntoId',
        data: {
          'nombre': nombre,
          'proposito': proposito,
          'descripcion': descripcion,
          'bssids': bssids,
        },
      );
      return ConjuntoAPModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<void> eliminarConjuntoAP(int conjuntoId) async {
    try {
      await _dio.delete<void>('/conjuntos-ap/$conjuntoId');
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<ConjuntoAPModel> actualizarUbicacionAPConjunto({
    required int conjuntoId,
    required String bssid,
    required double posX,
    required double posY,
  }) async {
    try {
      final response = await _dio.patch<Map<String, dynamic>>(
        '/conjuntos-ap/$conjuntoId/ubicacion-ap',
        data: {'bssid': bssid, 'pos_x': posX, 'pos_y': posY},
      );
      return ConjuntoAPModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<MapaCalorModel> generarHeatmap({
    required int planoId,
    required String algoritmo,
    required int resolucion,
    required List<String> bssids,
    required List<double> apPosX,
    required List<double> apPosY,
  }) async {
    try {
      final response = await _dio.get<Map<String, dynamic>>(
        '/planos/$planoId/heatmap',
        queryParameters: {
          'algoritmo': algoritmo,
          'resolucion': resolucion,
          'bssid': bssids,
          'ap_pos_x': apPosX,
          'ap_pos_y': apPosY,
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

  Future<MapaCalorModel> generarHeatmapDesdeConjunto({
    required int conjuntoId,
    required String modo,
    required String algoritmo,
    required int resolucion,
    List<String>? bssids,
    List<double>? apPosX,
    List<double>? apPosY,
  }) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/conjuntos-ap/$conjuntoId/heatmaps',
        data: {
          'modo': modo,
          'algoritmo': algoritmo,
          'resolucion': resolucion,
          if (bssids != null) 'bssids': bssids,
          if (apPosX != null) 'ap_pos_x': apPosX,
          if (apPosY != null) 'ap_pos_y': apPosY,
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

  Future<InventarioRFModel> obtenerInventarioRF(int proyectoId) async {
    try {
      final response = await _dio.get<Map<String, dynamic>>(
        '/proyectos/$proyectoId/inventario-rf',
      );
      return InventarioRFModel.fromJson(response.data!);
    } on DioException catch (e) {
      throw HeatmapApiException(
        _mensajeDesdeError(e),
        statusCode: e.response?.statusCode,
      );
    }
  }

  Future<APFisicoRFModel> crearAPFisicoRF({
    required int proyectoId,
    required Map<String, dynamic> datos,
  }) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/proyectos/$proyectoId/inventario-rf/aps',
        data: datos,
      );
      return APFisicoRFModel.fromJson(response.data!);
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
    final detalle = _detalleDesdeRespuesta(data);
    if (detalle != null && detalle.isNotEmpty) {
      return detalle;
    }
    if (status == 404) return 'Recurso no encontrado.';
    if (status == 401) return 'Sesión expirada.';
    if (status != null) {
      return 'No se pudo procesar el heatmap. Código HTTP $status.';
    }
    return 'No se pudo procesar el heatmap. Reintenta.';
  }

  static String? _detalleDesdeRespuesta(Object? data) {
    if (data is Map && data['detail'] is String) {
      return data['detail'] as String;
    }
    if (data is Map && data['detail'] is List) {
      final detalles = data['detail'] as List;
      return detalles.map((item) {
        if (item is Map && item['msg'] is String) return item['msg'];
        return item.toString();
      }).join(' ');
    }
    if (data is Map && data['message'] is String) {
      return data['message'] as String;
    }
    return null;
  }
}

class HeatmapApiException implements Exception {
  final String mensaje;
  final int? statusCode;

  const HeatmapApiException(this.mensaje, {this.statusCode});

  @override
  String toString() => mensaje;
}
