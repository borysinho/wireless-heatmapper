import 'dart:io';

import 'package:dio/dio.dart';

import '../../domain/repositories/plano_repository.dart';
import '../models/plano_model.dart';

/// Datasource remoto del feature Planos. Consume la API REST del backend.
/// HU PB-02 (importar) y PB-11 (calibrar) — Sprint 2.
class PlanoRemoteDatasource {
  final Dio _dio;

  /// Tamaño máximo permitido — PB-02 CA-3.
  static const int kMaxBytes = 20 * 1024 * 1024;

  /// Tiempo de espera para subir planos en redes móviles o producción.
  static const Duration kUploadTimeout = Duration(minutes: 2);

  /// Extensiones aceptadas — PB-02 CA-2.
  static const Set<String> kFormatosPermitidos = {'png', 'jpg', 'jpeg', 'pdf'};

  const PlanoRemoteDatasource(this._dio);

  /// Lista los planos de un proyecto.
  Future<List<PlanoModel>> listar(int proyectoId) async {
    final response = await _dio.get<List<dynamic>>(
      '/proyectos/$proyectoId/planos',
    );
    return (response.data ?? [])
        .map((e) => PlanoModel.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Importa un plano. Valida tamaño y formato antes de enviar.
  Future<PlanoModel> importar({
    required int proyectoId,
    String? rutaArchivo,
    List<int>? bytesArchivo,
    String? nombre,
  }) async {
    final nombreArchivo =
        _nombreArchivo(nombre: nombre, rutaArchivo: rutaArchivo);
    final ext = _extension(nombreArchivo);
    if (!kFormatosPermitidos.contains(ext)) {
      throw PlanoFormatoNoSoportadoException(ext);
    }

    final tamano = bytesArchivo?.length ?? await _tamanoDesdeRuta(rutaArchivo);
    if (tamano > kMaxBytes) {
      throw PlanoArchivoMuyGrandeException(tamano);
    }

    final formData = FormData.fromMap({
      if (nombre != null && nombre.isNotEmpty) 'nombre': nombre,
      'archivo': bytesArchivo != null
          ? MultipartFile.fromBytes(bytesArchivo, filename: nombreArchivo)
          : await _multipartDesdeRuta(rutaArchivo, nombreArchivo),
    });

    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/proyectos/$proyectoId/planos',
        data: formData,
        options: Options(
          contentType: Headers.multipartFormDataContentType,
          sendTimeout: kUploadTimeout,
          receiveTimeout: kUploadTimeout,
        ),
      );
      return PlanoModel.fromJson(response.data!);
    } on DioException catch (e) {
      _mapearError(e);
      rethrow;
    }
  }

  /// Renueva la URL firmada (cuando expiró). Devuelve sólo la URL.
  Future<String> renovarUrlFirmada(int planoId) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/planos/$planoId/url-firmada',
    );
    return response.data!['url_firmada'] as String;
  }

  /// Calibra la escala del plano (PB-11 CA-2).
  Future<PlanoModel> calibrar({
    required int planoId,
    required double x1,
    required double y1,
    required double x2,
    required double y2,
    required double distanciaRealM,
  }) async {
    try {
      final response = await _dio.patch<Map<String, dynamic>>(
        '/planos/$planoId/calibracion',
        data: {
          'x1': x1,
          'y1': y1,
          'x2': x2,
          'y2': y2,
          'distancia_real_m': distanciaRealM,
        },
      );
      return PlanoModel.fromJson(response.data!);
    } on DioException catch (e) {
      _mapearError(e, planoId: planoId);
      rethrow;
    }
  }

  /// Elimina un plano.
  Future<void> eliminar(int planoId) async {
    try {
      await _dio.delete<void>('/planos/$planoId');
    } on DioException catch (e) {
      _mapearError(e, planoId: planoId);
      rethrow;
    }
  }

  /// Traduce errores HTTP a excepciones de dominio.
  void _mapearError(DioException e, {int? planoId}) {
    final status = e.response?.statusCode;
    final detail = e.response?.data is Map
        ? (e.response!.data['detail']?.toString() ?? '')
        : '';

    if (status == null) {
      if (e.type == DioExceptionType.connectionTimeout ||
          e.type == DioExceptionType.sendTimeout ||
          e.type == DioExceptionType.receiveTimeout) {
        throw const PlanoStorageException(
          'La conexión tardó demasiado al comunicarse con el servidor.',
        );
      }
      if (e.type == DioExceptionType.connectionError) {
        throw const PlanoStorageException(
          'No se pudo conectar con el servidor de producción.',
        );
      }
    }

    if (status == 404 && planoId != null) {
      throw PlanoNoEncontradoException(planoId);
    }
    if (status == 413) {
      throw PlanoArchivoMuyGrandeException(0);
    }
    if (status == 415) {
      throw PlanoFormatoNoSoportadoException(detail);
    }
    final detailLower = detail.toLowerCase();
    if (status == 409 &&
        detailLower.contains('eliminar') &&
        detailLower.contains('punto')) {
      throw const PlanoEliminacionBloqueadaException();
    }
    if (status == 409 && detailLower.contains('punto')) {
      throw const PlanoRecalibracionBloqueadaException();
    }
    if (status == 422) {
      if (detailLower.contains('distancia')) {
        throw const PlanoDistanciaInvalidaException();
      }
      if (detailLower.contains('punto')) {
        throw const PlanoPuntosInvalidosException();
      }
    }
    if (detail.isNotEmpty) {
      throw PlanoStorageException(detail);
    }
    if (status != null) {
      throw PlanoStorageException('El servidor respondió HTTP $status.');
    }
  }

  /// Devuelve la extensión sin punto y en minúsculas (vacío si no tiene).
  static String _extension(String ruta) {
    final base = _basename(ruta);
    final i = base.lastIndexOf('.');
    if (i < 0 || i == base.length - 1) return '';
    return base.substring(i + 1).toLowerCase();
  }

  /// Devuelve el nombre del archivo (sin path).
  static String _basename(String ruta) {
    final i = ruta.lastIndexOf(RegExp(r'[\\/]'));
    return i < 0 ? ruta : ruta.substring(i + 1);
  }

  static String _nombreArchivo({String? nombre, String? rutaArchivo}) {
    if (nombre != null && nombre.trim().isNotEmpty) {
      return nombre.trim();
    }
    if (rutaArchivo != null && rutaArchivo.trim().isNotEmpty) {
      return _basename(rutaArchivo);
    }
    throw const PlanoStorageException('No se pudo identificar el archivo.');
  }

  static Future<int> _tamanoDesdeRuta(String? rutaArchivo) async {
    if (rutaArchivo == null || rutaArchivo.isEmpty) {
      throw const PlanoStorageException(
          'No se pudo acceder al archivo seleccionado.');
    }
    try {
      final file = File(rutaArchivo);
      if (!await file.exists()) {
        throw const PlanoStorageException(
          'No se pudo acceder al archivo seleccionado.',
        );
      }
      return file.length();
    } on PlanoStorageException {
      rethrow;
    } catch (_) {
      throw const PlanoStorageException(
        'No se pudo leer el archivo seleccionado.',
      );
    }
  }

  static Future<MultipartFile> _multipartDesdeRuta(
    String? rutaArchivo,
    String nombreArchivo,
  ) async {
    if (rutaArchivo == null || rutaArchivo.isEmpty) {
      throw const PlanoStorageException(
          'No se pudo acceder al archivo seleccionado.');
    }
    try {
      return await MultipartFile.fromFile(
        rutaArchivo,
        filename: nombreArchivo,
      );
    } catch (_) {
      throw const PlanoStorageException(
        'No se pudo preparar el archivo seleccionado para subirlo.',
      );
    }
  }
}
