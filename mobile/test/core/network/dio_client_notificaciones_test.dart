import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/core/network/dio_client.dart';

class _AdaptadorSesionExpirada implements HttpClientAdapter {
  final Map<String, int> solicitudesAutorizadas = {};

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    if (options.path == '/auth/refresh') {
      return _json(200, {'access_token': 'access_vigente'});
    }

    // Hace coincidir los 401 para reproducir el arranque de la app: el listado
    // y el registro FCM salen juntos con el access token vencido.
    if (options.headers['Authorization'] != 'Bearer access_vigente') {
      await Future<void>.delayed(const Duration(milliseconds: 20));
      return _json(401, {'detail': 'Token expirado'});
    }

    solicitudesAutorizadas.update(
      '${options.method} ${options.path}',
      (cantidad) => cantidad + 1,
      ifAbsent: () => 1,
    );
    if (options.path == '/notificaciones/dispositivos') {
      return _json(201, {'registrado': true});
    }
    return _json(200, <dynamic>[]);
  }

  ResponseBody _json(int estado, Object cuerpo) => ResponseBody.fromString(
        jsonEncode(cuerpo),
        estado,
        headers: {
          Headers.contentTypeHeader: [Headers.jsonContentType],
        },
      );

  @override
  void close({bool force = false}) {}
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test(
    'reintenta el registro FCM cuando coincide con la renovación de sesión',
    () async {
      FlutterSecureStorage.setMockInitialValues({
        'access_token': 'access_vencido',
        'refresh_token': 'refresh_vigente',
      });
      const almacenamiento = FlutterSecureStorage();
      final cliente = DioClient(almacenamiento);
      final adaptador = _AdaptadorSesionExpirada();
      cliente.dio.httpClientAdapter = adaptador;

      final respuestas = await Future.wait([
        cliente.dio.get<List<dynamic>>('/proyectos'),
        cliente.dio.post<Map<String, dynamic>>(
          '/notificaciones/dispositivos',
          data: {
            'token': 'token-fcm-del-dispositivo',
            'plataforma': 'android',
          },
        ),
      ]);

      expect(respuestas[0].statusCode, 200);
      expect(respuestas[1].statusCode, 201);
      expect(
        adaptador.solicitudesAutorizadas['GET /proyectos'],
        1,
      );
      expect(
        adaptador.solicitudesAutorizadas['POST /notificaciones/dispositivos'],
        1,
      );
      expect(
        await almacenamiento.read(key: 'access_token'),
        'access_vigente',
      );
    },
  );
}
