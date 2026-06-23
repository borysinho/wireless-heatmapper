import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../../core/network/connectivity_monitor.dart';
import '../../../../core/wifi/throttling_manager.dart';
import '../../../../core/wifi/wifi_scanner.dart';
import '../../domain/entities/punto_medicion.dart';
import '../../domain/repositories/captura_repository.dart';
import 'captura_state.dart';

/// Cubit de la sesión de captura WiFi.
/// Sprint 3 — PB-03, PB-04 (Sp3-11).
///
/// Ciclo principal:
///   CapturaInactiva → iniciarSesion → CapturaActiva
///   CapturaActiva  → marcarPunto   → CapturaEnviando → CapturaActiva / CapturaError
///   CapturaActiva  → (throttling)  → CapturaThrottling → CapturaActiva
///   CapturaActiva  → (sin red)     → CapturaPausada → CapturaActiva
///   Cualquier estado → detenerSesion → CapturaInactiva
class CapturaCubit extends Cubit<CapturaState> {
  final CapturaRepository _repo;
  final WifiScanner _scanner;
  final ThrottlingManager _throttling;
  final ConnectivityMonitor _connectivity;

  CapturaCubit({
    required CapturaRepository repo,
    required WifiScanner scanner,
    required ThrottlingManager throttling,
    required ConnectivityMonitor connectivity,
  })  : _repo = repo,
        _scanner = scanner,
        _throttling = throttling,
        _connectivity = connectivity,
        super(const CapturaInactiva());

  List<PuntoMedicion> get _puntosActuales => switch (state) {
        CapturaActiva(:final puntos) => puntos,
        CapturaEnviando(:final puntos) => puntos,
        CapturaThrottling(:final puntos) => puntos,
        CapturaPausada(:final puntos) => puntos,
        CapturaPuntoDetalle(:final puntos) => puntos,
        CapturaError(:final puntos) => puntos,
        _ => const <PuntoMedicion>[],
      };

  int? get _planoIdActual => switch (state) {
        CapturaActiva(:final planoId) => planoId,
        CapturaEnviando(:final planoId) => planoId,
        CapturaThrottling(:final planoId) => planoId,
        CapturaPausada(:final planoId) => planoId,
        CapturaPuntoDetalle(:final planoId) => planoId,
        CapturaError(:final planoId) => planoId,
        _ => null,
      };

  bool get _modoContinuoActual => switch (state) {
        CapturaActiva(:final modosContinuo) => modosContinuo,
        CapturaEnviando(:final modosContinuo) => modosContinuo,
        CapturaThrottling(:final modosContinuo) => modosContinuo,
        CapturaPausada(:final modosContinuo) => modosContinuo,
        CapturaPuntoDetalle(:final modosContinuo) => modosContinuo,
        CapturaError(:final modosContinuo) => modosContinuo,
        _ => false,
      };

  int get _intervaloSegundosActual => switch (state) {
        CapturaActiva(:final intervaloSegundos) => intervaloSegundos,
        CapturaEnviando(:final intervaloSegundos) => intervaloSegundos,
        CapturaThrottling(:final intervaloSegundos) => intervaloSegundos,
        CapturaPausada(:final intervaloSegundos) => intervaloSegundos,
        CapturaPuntoDetalle(:final intervaloSegundos) => intervaloSegundos,
        CapturaError(:final intervaloSegundos) => intervaloSegundos,
        _ => 30,
      };

  // -------------------------------------------------------------------------
  // Ciclo de sesión
  // -------------------------------------------------------------------------

  /// Inicia la sesión de captura para [planoId]. Carga los puntos existentes.
  Future<void> iniciarSesion(int planoId) async {
    emit(const CapturaLoading());
    try {
      final puntos = await _repo.listarPuntos(planoId);
      emit(CapturaActiva(planoId: planoId, puntos: puntos));
    } catch (_) {
      emit(CapturaActiva(planoId: planoId));
    }
  }

  /// Detiene la sesión. El estado vuelve a [CapturaInactiva].
  void detenerSesion() => emit(const CapturaInactiva());

  // -------------------------------------------------------------------------
  // Modo de captura
  // -------------------------------------------------------------------------

  /// Cambia el modo de captura (Puntual ↔ Continuo) y el intervalo.
  void cambiarModo({required bool continuo, int intervaloSegundos = 30}) {
    final id = _planoIdActual;
    if (id == null) return;
    emit(
      CapturaActiva(
        planoId: id,
        puntos: _puntosActuales,
        modosContinuo: continuo,
        intervaloSegundos: intervaloSegundos,
      ),
    );
  }

  // -------------------------------------------------------------------------
  // Marcar punto (PB-03 + PB-04 CA-1)
  // -------------------------------------------------------------------------

  /// Escanea las redes WiFi y envía el lote al backend para la posición [posX],[posY].
  ///
  /// Flujo:
  ///   1. Verifica conectividad → CapturaPausada si no hay red.
  ///   2. Verifica throttling → CapturaThrottling si se alcanzó el límite.
  ///   3. Realiza el escaneo WiFi.
  ///   4. Registra el escaneo en el ThrottlingManager.
  ///   5. Envía el lote al backend.
  ///   6. Agrega el punto a la lista local y emite CapturaActiva.
  Future<void> marcarPunto({
    required double posX,
    required double posY,
  }) async {
    final planoId = _planoIdActual;
    if (planoId == null) return;

    // Capturar estado antes de operaciones async para preservar modosContinuo
    // e intervaloSegundos al restaurar al finalizar.
    final estadoAntes = state;
    final puntosActuales = _puntosActuales;
    final modoContinuo = _modoContinuoActual;
    final intervaloSegundos = _intervaloSegundosActual;

    // 1. Verificar conectividad
    final conectado = await _connectivity.estaConectado();
    if (!conectado) {
      emit(CapturaPausada(
        planoId: planoId,
        puntos: puntosActuales,
        modosContinuo: modoContinuo,
        intervaloSegundos: intervaloSegundos,
      ));
      return;
    }

    // 2. Verificar throttling
    if (!_throttling.puedeEscanear) {
      emit(CapturaThrottling(
        planoId: planoId,
        puntos: puntosActuales,
        segundosRestantes: _throttling.segundosHastaProximo,
        modosContinuo: modoContinuo,
        intervaloSegundos: intervaloSegundos,
      ));
      return;
    }

    emit(CapturaEnviando(
      planoId: planoId,
      puntos: puntosActuales,
      modosContinuo: modoContinuo,
      intervaloSegundos: intervaloSegundos,
    ));

    try {
      // 3. Escanear
      final escaneos = await _scanner.escanear();
      if (escaneos.isEmpty) {
        emit(CapturaError(
          planoId: planoId,
          puntos: puntosActuales,
          mensaje: 'No se detectaron redes WiFi en el escaneo.',
          modosContinuo: modoContinuo,
          intervaloSegundos: intervaloSegundos,
        ));
        return;
      }

      // 4. Registrar en throttling
      _throttling.registrarEscaneo();

      // 5. Enviar lote al backend
      final punto = await _repo.enviarLote(
        planoId: planoId,
        posX: posX,
        posY: posY,
        escaneos: escaneos,
      );

      // 6. Actualizar lista local preservando el modo (continuo/puntual).
      final nuevaLista = [...puntosActuales, punto];
      _restaurarActivo(estadoAntes, planoId, nuevaLista);
    } on WifiScanException catch (e) {
      emit(CapturaError(
        planoId: planoId,
        puntos: puntosActuales,
        mensaje: e.mensaje,
        modosContinuo: modoContinuo,
        intervaloSegundos: intervaloSegundos,
      ));
    } on CapturaApiException catch (e) {
      emit(CapturaError(
        planoId: planoId,
        puntos: puntosActuales,
        mensaje: e.mensaje,
        modosContinuo: modoContinuo,
        intervaloSegundos: intervaloSegundos,
      ));
    } catch (_) {
      emit(CapturaError(
        planoId: planoId,
        puntos: puntosActuales,
        mensaje: 'No se pudo enviar el lote. Reintenta.',
        modosContinuo: modoContinuo,
        intervaloSegundos: intervaloSegundos,
      ));
    }
  }

  // -------------------------------------------------------------------------
  // Agregar mediciones a punto existente (PB-03 — modo continuo)
  // -------------------------------------------------------------------------

  /// Escanea y agrega mediciones a un punto ya creado [puntoId].
  ///
  /// A diferencia de [marcarPunto], no crea un punto nuevo.
  /// Si el escaneo devuelve 0 redes o hay throttling, el ciclo se omite
  /// silenciosamente para no interrumpir el modo continuo.
  Future<void> agregarMedicionesAPunto({required int puntoId}) async {
    final planoId = _planoIdActual;
    if (planoId == null) return;

    final puntosActuales = _puntosActuales;
    final estadoActual = state;
    final modoContinuo = _modoContinuoActual;
    final intervaloSegundos = _intervaloSegundosActual;

    // 1. Verificar conectividad
    final conectado = await _connectivity.estaConectado();
    if (!conectado) {
      emit(CapturaPausada(
        planoId: planoId,
        puntos: puntosActuales,
        modosContinuo: modoContinuo,
        intervaloSegundos: intervaloSegundos,
      ));
      return;
    }

    // 2. Throttling: saltar ciclo silenciosamente (no bloquear modo continuo)
    if (!_throttling.puedeEscanear) return;

    emit(CapturaEnviando(
      planoId: planoId,
      puntos: puntosActuales,
      modosContinuo: modoContinuo,
      intervaloSegundos: intervaloSegundos,
    ));

    try {
      // 3. Escanear
      final escaneos = await _scanner.escanear();
      if (escaneos.isEmpty) {
        _restaurarActivo(estadoActual, planoId, puntosActuales);
        return;
      }

      // 4. Registrar en throttling
      _throttling.registrarEscaneo();

      // 5. Agregar mediciones al punto existente
      final puntoActualizado = await _repo.agregarMediciones(
        puntoId: puntoId,
        escaneos: escaneos,
      );

      // 6. Actualizar el punto en la lista local
      final nuevaLista = puntosActuales
          .map((p) => p.id == puntoId ? puntoActualizado : p)
          .toList();
      _restaurarActivo(estadoActual, planoId, nuevaLista);
    } on WifiScanException {
      _restaurarActivo(estadoActual, planoId, puntosActuales);
    } on CapturaApiException catch (e) {
      emit(CapturaError(
        planoId: planoId,
        puntos: puntosActuales,
        mensaje: e.mensaje,
        modosContinuo: modoContinuo,
        intervaloSegundos: intervaloSegundos,
      ));
    } catch (_) {
      _restaurarActivo(estadoActual, planoId, puntosActuales);
    }
  }

  /// Restaura el estado [CapturaActiva] preservando modosContinuo e intervalo.
  /// Si el estado anterior era [CapturaPuntoDetalle], re-emite el detalle con
  /// el punto actualizado en lugar de volver a [CapturaActiva].
  void _restaurarActivo(
    CapturaState estadoAntes,
    int planoId,
    List<PuntoMedicion> puntos,
  ) {
    if (estadoAntes is CapturaActiva) {
      emit(estadoAntes.copyWith(puntos: puntos));
    } else if (estadoAntes is CapturaPuntoDetalle) {
      // Actualizar el punto seleccionado con sus nuevas mediciones
      final puntoActualizado = puntos.firstWhere(
        (p) => p.id == estadoAntes.puntoSeleccionado.id,
        orElse: () => estadoAntes.puntoSeleccionado,
      );
      emit(CapturaPuntoDetalle(
        planoId: planoId,
        puntos: puntos,
        puntoSeleccionado: puntoActualizado,
        modosContinuo: estadoAntes.modosContinuo,
        intervaloSegundos: estadoAntes.intervaloSegundos,
      ));
    } else {
      emit(CapturaActiva(
        planoId: planoId,
        puntos: puntos,
        modosContinuo: _modoContinuoActual,
        intervaloSegundos: _intervaloSegundosActual,
      ));
    }
  }

  PuntoMedicion _puntoConPosicion(
    PuntoMedicion punto, {
    required double posX,
    required double posY,
  }) {
    return PuntoMedicion(
      id: punto.id,
      planoId: punto.planoId,
      posX: posX,
      posY: posY,
      nivel: punto.nivel,
      mediciones: punto.mediciones,
    );
  }

  List<PuntoMedicion> _actualizarPuntoEnLista(
    List<PuntoMedicion> puntos,
    PuntoMedicion actualizado,
  ) {
    return puntos
        .map((punto) => punto.id == actualizado.id ? actualizado : punto)
        .toList();
  }

  /// Reubica el punto localmente para dar retroalimentación inmediata al arrastrar.
  void reubicarPuntoLocal({
    required int puntoId,
    required double posX,
    required double posY,
  }) {
    final planoId = _planoIdActual;
    if (planoId == null) return;
    final estadoAntes = state;
    PuntoMedicion? actual = estadoAntes is CapturaPuntoDetalle &&
            estadoAntes.puntoSeleccionado.id == puntoId
        ? estadoAntes.puntoSeleccionado
        : null;
    for (final punto in _puntosActuales) {
      if (actual != null) break;
      if (punto.id == puntoId) {
        actual = punto;
        break;
      }
    }
    if (actual == null) return;
    final actualizado = _puntoConPosicion(actual, posX: posX, posY: posY);
    final nuevaLista = _actualizarPuntoEnLista(_puntosActuales, actualizado);
    _restaurarActivo(estadoAntes, planoId, nuevaLista);
  }

  /// Persiste la nueva posición del punto en backend.
  Future<void> moverPunto({
    required int puntoId,
    required double posX,
    required double posY,
  }) async {
    final planoId = _planoIdActual;
    if (planoId == null) return;
    final estadoAntes = state;
    final anteriores = _puntosActuales;
    try {
      final actualizado = await _repo.moverPunto(
        puntoId: puntoId,
        posX: posX,
        posY: posY,
      );
      final nuevaLista = _actualizarPuntoEnLista(_puntosActuales, actualizado);
      _restaurarActivo(estadoAntes, planoId, nuevaLista);
    } on CapturaApiException catch (e) {
      emit(CapturaError(
        planoId: planoId,
        puntos: anteriores,
        mensaje: e.mensaje,
        modosContinuo: _modoContinuoActual,
        intervaloSegundos: _intervaloSegundosActual,
      ));
    } catch (_) {
      emit(CapturaError(
        planoId: planoId,
        puntos: anteriores,
        mensaje: 'No se pudo mover el punto.',
        modosContinuo: _modoContinuoActual,
        intervaloSegundos: _intervaloSegundosActual,
      ));
    }
  }

  // -------------------------------------------------------------------------
  // Restablecimiento tras pausa / throttling
  // -------------------------------------------------------------------------

  /// Vuelve a CapturaActiva tras resolver el problema de red o throttling.
  void reanudar() {
    final id = _planoIdActual;
    if (id == null) return;
    emit(CapturaActiva(
      planoId: id,
      puntos: _puntosActuales,
      modosContinuo: _modoContinuoActual,
      intervaloSegundos: _intervaloSegundosActual,
    ));
  }

  // -------------------------------------------------------------------------
  // Detalle de punto (PB-04 CA-4)
  // -------------------------------------------------------------------------

  /// Carga el detalle de un punto y emite [CapturaPuntoDetalle].
  Future<void> abrirDetallePunto(int puntoId) async {
    final id = _planoIdActual;
    if (id == null) return;
    // Preservar modosContinuo e intervalo para restaurarlos al cerrar el detalle
    final bool modoCont;
    final int intervalo;
    if (state
        case CapturaActiva(:final modosContinuo, :final intervaloSegundos)) {
      modoCont = modosContinuo;
      intervalo = intervaloSegundos;
    } else if (state
        case CapturaPuntoDetalle(
          :final modosContinuo,
          :final intervaloSegundos,
        )) {
      modoCont = modosContinuo;
      intervalo = intervaloSegundos;
    } else {
      modoCont = _modoContinuoActual;
      intervalo = _intervaloSegundosActual;
    }
    try {
      final punto = await _repo.obtenerPunto(puntoId);
      emit(CapturaPuntoDetalle(
        planoId: id,
        puntos: _puntosActuales,
        puntoSeleccionado: punto,
        modosContinuo: modoCont,
        intervaloSegundos: intervalo,
      ));
    } catch (_) {
      emit(CapturaError(
        planoId: id,
        puntos: _puntosActuales,
        mensaje: 'No se pudo cargar el detalle del punto.',
        modosContinuo: modoCont,
        intervaloSegundos: intervalo,
      ));
    }
  }

  /// Cierra el detalle y vuelve a [CapturaActiva], preservando el modo.
  void cerrarDetalle() {
    final id = _planoIdActual;
    if (id == null) return;
    final bool modoCont;
    final int intervalo;
    if (state
        case CapturaPuntoDetalle(
          :final modosContinuo,
          :final intervaloSegundos,
        )) {
      modoCont = modosContinuo;
      intervalo = intervaloSegundos;
    } else {
      modoCont = _modoContinuoActual;
      intervalo = _intervaloSegundosActual;
    }
    emit(CapturaActiva(
      planoId: id,
      puntos: _puntosActuales,
      modosContinuo: modoCont,
      intervaloSegundos: intervalo,
    ));
  }

  // -------------------------------------------------------------------------
  // Eliminar punto (PB-04 CA-5)
  // -------------------------------------------------------------------------

  /// Elimina un punto (con confirmación previa en la UI). PB-04 CA-5.
  Future<void> eliminarPunto(int puntoId) async {
    final id = _planoIdActual;
    if (id == null) return;
    final actuales = _puntosActuales;
    try {
      await _repo.eliminarPunto(puntoId);
      final nuevaLista = actuales.where((p) => p.id != puntoId).toList();
      emit(CapturaActiva(planoId: id, puntos: nuevaLista));
    } on CapturaApiException catch (e) {
      emit(CapturaError(
        planoId: id,
        puntos: actuales,
        mensaje: e.mensaje,
        modosContinuo: _modoContinuoActual,
        intervaloSegundos: _intervaloSegundosActual,
      ));
    }
  }
}
