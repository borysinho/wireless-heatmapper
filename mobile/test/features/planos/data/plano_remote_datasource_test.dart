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
  "descripcion": "Área frontal",
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
        nombreArchivo: 'plano.png',
        nombre: 'Planta baja',
        descripcion: 'Área frontal',
      );

      final request = adapter.ultimaRequest!;
      final formData = request.data as FormData;
      expect(request.path, '/proyectos/10/planos');
      expect(
        formData.fields.any(
          (field) =>
              field.key == 'descripcion' && field.value == 'Área frontal',
        ),
        isTrue,
      );
      expect(
        formData.fields.any(
          (field) => field.key == 'nombre' && field.value == 'Planta baja',
        ),
        isTrue,
      );
      expect(formData.files.single.value.filename, 'plano.png');
    });

    test('valida el formato con el archivo original y no con el nombre visible',
        () async {
      final adapter = _CapturandoAdapter();
      final dio = Dio(BaseOptions(baseUrl: 'https://example.test/api'))
        ..httpClientAdapter = adapter;
      final datasource = PlanoRemoteDatasource(dio);

      await datasource.importar(
        proyectoId: 10,
        bytesArchivo: _pngMinimo,
        nombreArchivo: 'plano.png',
        nombre: 'Planta baja',
      );

      final formData = adapter.ultimaRequest!.data as FormData;
      expect(formData.files.single.value.filename, 'plano.png');
      expect(
        formData.fields.any(
          (field) => field.key == 'nombre' && field.value == 'Planta baja',
        ),
        isTrue,
      );
      expect(
        formData.fields.any((field) => field.key == 'descripcion'),
        isFalse,
      );
    });

    test('acepta JPG cuando Android entrega el nombre sin extensión', () async {
      final adapter = _CapturandoAdapter();
      final dio = Dio(BaseOptions(baseUrl: 'https://example.test/api'))
        ..httpClientAdapter = adapter;
      final datasource = PlanoRemoteDatasource(dio);

      await datasource.importar(
        proyectoId: 10,
        bytesArchivo: _jpgMinimo,
        nombreArchivo: 'imagen_sin_extension',
        extensionArchivo: 'jpg',
        nombre: 'Planta alta',
      );

      final formData = adapter.ultimaRequest!.data as FormData;
      expect(formData.files.single.value.filename, 'imagen_sin_extension.jpg');
      expect(
        formData.fields.any(
          (field) => field.key == 'nombre' && field.value == 'Planta alta',
        ),
        isTrue,
      );
    });

    test('infiere JPG por contenido si no hay extensión informada', () async {
      final adapter = _CapturandoAdapter();
      final dio = Dio(BaseOptions(baseUrl: 'https://example.test/api'))
        ..httpClientAdapter = adapter;
      final datasource = PlanoRemoteDatasource(dio);

      await datasource.importar(
        proyectoId: 10,
        bytesArchivo: _jpgMinimo,
        nombreArchivo: 'imagen_sin_extension',
        nombre: 'Planta alta',
      );

      final formData = adapter.ultimaRequest!.data as FormData;
      expect(formData.files.single.value.filename, 'imagen_sin_extension.jpg');
    });
  });
}

const _jpgMinimo = <int>[
  0xff,
  0xd8,
  0xff,
  0xe0,
  0x00,
  0x10,
  0x4a,
  0x46,
  0x49,
  0x46,
  0x00,
  0xff,
  0xd9,
];

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
