import 'dart:async';

import 'package:dio/dio.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

import '../../firebase_options.dart';

@pragma('vm:entry-point')
Future<void> manejarMensajeFirebaseEnSegundoPlano(RemoteMessage mensaje) async {
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
}

/// Integra FCM con la sesión REST del técnico.
///
/// El token identifica al dispositivo, no almacena estado de dominio. El
/// backend lo asocia al usuario autenticado y lo usa al asignarle un proyecto.
class ServicioNotificacionesPush {
  static const _canalId = 'asignaciones_proyecto';
  static const _canalNombre = 'Asignaciones de proyectos';

  final Dio _dio;
  final FirebaseMessaging _mensajeria;
  final FlutterLocalNotificationsPlugin _notificacionesLocales;

  StreamSubscription<String>? _renovacionTokenSub;
  StreamSubscription<RemoteMessage>? _mensajePrimerPlanoSub;
  StreamSubscription<RemoteMessage>? _aperturaMensajeSub;
  void Function(int proyectoId, String? proyectoNombre)? alAbrirProyecto;

  ServicioNotificacionesPush(
    this._dio, {
    FirebaseMessaging? mensajeria,
    FlutterLocalNotificationsPlugin? notificacionesLocales,
  })  : _mensajeria = mensajeria ?? FirebaseMessaging.instance,
        _notificacionesLocales =
            notificacionesLocales ?? FlutterLocalNotificationsPlugin();

  Future<void> inicializar() async {
    FirebaseMessaging.onBackgroundMessage(
      manejarMensajeFirebaseEnSegundoPlano,
    );

    await _notificacionesLocales.initialize(
      settings: const InitializationSettings(
        android: AndroidInitializationSettings('@mipmap/ic_launcher'),
      ),
      onDidReceiveNotificationResponse: (respuesta) {
        final proyectoId = int.tryParse(respuesta.payload ?? '');
        if (proyectoId != null) alAbrirProyecto?.call(proyectoId, null);
      },
    );

    const canal = AndroidNotificationChannel(
      _canalId,
      _canalNombre,
      description: 'Avisos cuando un técnico recibe un proyecto.',
      importance: Importance.high,
    );
    await _notificacionesLocales
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(canal);

    _mensajePrimerPlanoSub ??=
        FirebaseMessaging.onMessage.listen(_mostrarEnPrimerPlano);
    _aperturaMensajeSub ??=
        FirebaseMessaging.onMessageOpenedApp.listen(_abrirDesdeMensaje);

    final inicial = await _mensajeria.getInitialMessage();
    if (inicial != null) {
      // Espera a que GoRouter termine de construirse.
      unawaited(Future<void>.delayed(
        const Duration(milliseconds: 400),
        () => _abrirDesdeMensaje(inicial),
      ));
    }
  }

  Future<void> activarParaSesion() async {
    try {
      final permiso = await _mensajeria.requestPermission(
        alert: true,
        badge: true,
        sound: true,
      );
      if (permiso.authorizationStatus == AuthorizationStatus.denied) return;

      final token = await _mensajeria.getToken();
      if (token != null) await _registrar(token);

      await _renovacionTokenSub?.cancel();
      _renovacionTokenSub = _mensajeria.onTokenRefresh.listen((nuevoToken) {
        unawaited(_registrar(nuevoToken));
      });
    } catch (_) {
      // Las notificaciones no deben impedir que el técnico inicie sesión.
    }
  }

  Future<void> desactivarParaSesion() async {
    await _renovacionTokenSub?.cancel();
    _renovacionTokenSub = null;
    try {
      final token = await _mensajeria.getToken();
      if (token != null) {
        await _dio.delete<void>(
          '/notificaciones/dispositivos',
          data: {'token': token, 'plataforma': 'android'},
        );
      }
    } catch (_) {
      // El cierre de sesión debe continuar aunque no haya red.
    }
  }

  /// Invalida el token cuando la sesión expira y ya no es posible autenticar
  /// la baja contra el backend. FCM rechazará el token anterior y el backend
  /// lo marcará inactivo en el siguiente intento de envío.
  Future<void> invalidarTokenLocal() async {
    await _renovacionTokenSub?.cancel();
    _renovacionTokenSub = null;
    try {
      await _mensajeria.deleteToken();
    } catch (_) {
      // La navegación al login no debe bloquearse por Firebase.
    }
  }

  Future<void> _registrar(String token) async {
    await _dio.post<void>(
      '/notificaciones/dispositivos',
      data: {'token': token, 'plataforma': 'android'},
    );
  }

  Future<void> _mostrarEnPrimerPlano(RemoteMessage mensaje) async {
    final notificacion = mensaje.notification;
    if (notificacion == null) return;
    await _notificacionesLocales.show(
      id: mensaje.messageId.hashCode,
      title: notificacion.title ?? 'Nuevo proyecto asignado',
      body: notificacion.body,
      notificationDetails: const NotificationDetails(
        android: AndroidNotificationDetails(
          _canalId,
          _canalNombre,
          channelDescription: 'Avisos cuando un técnico recibe un proyecto.',
          importance: Importance.high,
          priority: Priority.high,
        ),
      ),
      payload: mensaje.data['proyecto_id'],
    );
  }

  void _abrirDesdeMensaje(RemoteMessage mensaje) {
    final proyectoId = int.tryParse(mensaje.data['proyecto_id'] ?? '');
    if (proyectoId == null) return;
    alAbrirProyecto?.call(proyectoId, mensaje.data['proyecto_nombre']);
  }
}
