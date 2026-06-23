import 'dart:async';
import 'dart:io';
import 'dart:typed_data';

import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/features/planos/data/datasources/plano_remote_datasource.dart';

class _CapturandoAdapter implements HttpClientAdapter {
  RequestOptions? ultimaRequest;

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    ultimaRequest = options;
    return ResponseBody.fromString(
      '''
{
  "id": 1,
  "proyecto_id": 10,
  "nombre": "plano.png",
  "formato": "png",
  "ancho_px": 100,
  "alto_px": 80,
  "tamano_bytes": 68,
  "url_firmada": "/planos/archivo/plano.png?exp=1&sig=a",
  "calibrado": false,
  "cantidad_puntos": 0,
  "escala_m_por_px": null,
  "distancia_real_m": null,
  "calibracion_x1": null,
  "calibracion_y1": null,
  "calibracion_x2": null,
  "calibracion_y2": null,
  "warning": null,
  "created_at": "2026-01-01T12:00:00",
  "updated_at": "2026-01-01T12:00:00"
}
''',
      201,
      headers: {
        Headers.contentTypeHeader: [Headers.jsonContentType],
      },
    );
  }

  @override
  void close({bool force = false}) {}
}

void main() {
  group('PlanoRemoteDatasource.importar', () {
    late Directory tempDir;

    setUp(() async {
      tempDir = await Directory.systemTemp.createTemp('planos_test_');
    });

    tearDown(() async {
      if (await tempDir.exists()) {
        await tempDir.delete(recursive: true);
      }
    });

    test('envía multipart con timeout amplio para producción', () async {
      final archivo = File('${tempDir.path}/plano.png');
      await archivo.writeAsBytes(_pngMinimo);
      final adapter = _CapturandoAdapter();
      final dio = Dio(BaseOptions(baseUrl: 'https://example.test/api'))
        ..httpClientAdapter = adapter;
      final datasource = PlanoRemoteDatasource(dio);

      final plano = await datasource.importar(
        proyectoId: 10,
        rutaArchivo: archivo.path,
      );

      final request = adapter.ultimaRequest!;
      expect(plano.id, 1);
      expect(request.method, 'POST');
      expect(request.path, '/proyectos/10/planos');
      expect(request.data, isA<FormData>());
      expect(
        request.contentType,
        startsWith(Headers.multipartFormDataContentType),
      );
      expect(request.sendTimeout, PlanoRemoteDatasource.kUploadTimeout);
      expect(request.receiveTimeout, PlanoRemoteDatasource.kUploadTimeout);
    });

    test('puede importar desde bytes sin depender de una ruta física',
        () async {
      final adapter = _CapturandoAdapter();
      final dio = Dio(BaseOptions(baseUrl: 'https://example.test/api'))
        ..httpClientAdapter = adapter;
      final datasource = PlanoRemoteDatasource(dio);

      await datasource.importar(
        proyectoId: 10,
        bytesArchivo: _pngMinimo,
        nombre: 'plano.png',
      );

      final request = adapter.ultimaRequest!;
      final formData = request.data as FormData;
      expect(request.path, '/proyectos/10/planos');
      expect(formData.files.single.value.filename, 'plano.png');
    });
  });
}

const _pngMinimo = <int>[
  0x89,
  0x50,
  0x4e,
  0x47,
  0x0d,
  0x0a,
  0x1a,
  0x0a,
  0x00,
  0x00,
  0x00,
  0x0d,
  0x49,
  0x48,
  0x44,
  0x52,
  0x00,
  0x00,
  0x00,
  0x01,
  0x00,
  0x00,
  0x00,
  0x01,
  0x08,
  0x06,
  0x00,
  0x00,
  0x00,
  0x1f,
  0x15,
  0xc4,
  0x89,
  0x00,
  0x00,
  0x00,
  0x0b,
  0x49,
  0x44,
  0x41,
  0x54,
  0x78,
  0x9c,
  0x63,
  0xf8,
  0xff,
  0xff,
  0x3f,
  0x00,
  0x05,
  0xfe,
  0x02,
  0xfe,
  0xdc,
  0xcc,
  0x59,
  0xe7,
  0x00,
  0x00,
  0x00,
  0x00,
  0x49,
  0x45,
  0x4e,
  0x44,
  0xae,
  0x42,
  0x60,
  0x82,
];
