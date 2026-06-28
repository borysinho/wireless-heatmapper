import 'package:flutter_bloc/flutter_bloc.dart';

import '../../data/datasources/heatmap_remote_datasource.dart';
import '../../domain/entities/ap_disponible.dart';
import '../../domain/entities/conjunto_ap.dart';
import '../../domain/usecases/heatmap_usecases.dart';
import 'heatmap_state.dart';

class HeatmapCubit extends Cubit<HeatmapState> {
  final ListarAPsDisponiblesUseCase _listarAPs;
  final ListarConjuntosAPUseCase _listarConjuntos;
  final CrearConjuntoAPUseCase _crearConjunto;
  final ActualizarConjuntoAPUseCase _actualizarConjunto;
  final EliminarConjuntoAPUseCase _eliminarConjunto;
  final GenerarHeatmapUseCase _generarHeatmap;
  final GenerarHeatmapDesdeConjuntoUseCase _generarHeatmapDesdeConjunto;
  final ActualizarUbicacionAPConjuntoUseCase _actualizarUbicacionAPConjunto;
  int? _planoId;

  HeatmapCubit({
    required ListarAPsDisponiblesUseCase listarAPs,
    required ListarConjuntosAPUseCase listarConjuntos,
    required CrearConjuntoAPUseCase crearConjunto,
    required ActualizarConjuntoAPUseCase actualizarConjunto,
    required EliminarConjuntoAPUseCase eliminarConjunto,
    required GenerarHeatmapUseCase generarHeatmap,
    required GenerarHeatmapDesdeConjuntoUseCase generarHeatmapDesdeConjunto,
    required ActualizarUbicacionAPConjuntoUseCase actualizarUbicacionAPConjunto,
  })  : _listarAPs = listarAPs,
        _listarConjuntos = listarConjuntos,
        _crearConjunto = crearConjunto,
        _actualizarConjunto = actualizarConjunto,
        _eliminarConjunto = eliminarConjunto,
        _generarHeatmap = generarHeatmap,
        _generarHeatmapDesdeConjunto = generarHeatmapDesdeConjunto,
        _actualizarUbicacionAPConjunto = actualizarUbicacionAPConjunto,
        super(const HeatmapInitial());

  Future<void> iniciar(int planoId) async {
    _planoId = planoId;
    emit(const HeatmapLoading(mensaje: 'Buscando APs y conjuntos…'));
    try {
      final aps = await _listarAPs(planoId);
      if (aps.isEmpty) {
        emit(const HeatmapError(
          'No hay APs detectados. Registra mediciones antes de generar heatmaps.',
        ));
        return;
      }
      final conjuntos = await _listarConjuntos(planoId);
      emit(HeatmapConjuntos(aps: aps, conjuntos: conjuntos));
    } on HeatmapApiException catch (e) {
      emit(HeatmapError(e.mensaje));
    } catch (_) {
      emit(const HeatmapError('No se pudieron cargar los conjuntos de APs.'));
    }
  }

  void abrirConjunto(ConjuntoAP conjunto) {
    final actual = state;
    if (actual is! HeatmapConjuntos) return;
    final apsConjunto = _apsDelConjunto(
      aps: actual.aps,
      conjunto: conjunto,
    );
    if (apsConjunto.isEmpty) {
      emit(HeatmapConjuntos(
        aps: actual.aps,
        conjuntos: actual.conjuntos,
        mensaje: 'El conjunto no tiene APs disponibles en este plano.',
      ));
      return;
    }
    final seleccionados = {for (final ap in apsConjunto) ap.bssid};
    emit(HeatmapSeleccionAP(
      conjunto: conjunto,
      aps: apsConjunto,
      bssidsSeleccionados: seleccionados,
      bssidActivo: null,
      apPosXPorBssid: {for (final item in apsConjunto) item.bssid: item.posX},
      apPosYPorBssid: {for (final item in apsConjunto) item.bssid: item.posY},
    ));
  }

  void volverAConjuntos() {
    final planoId = _planoId;
    if (planoId != null) iniciar(planoId);
  }

  Future<void> crearConjunto({
    required int planoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required List<String> bssids,
  }) async {
    final actual = state;
    final aps = actual is HeatmapConjuntos ? actual.aps : <APDisponible>[];
    emit(const HeatmapLoading(mensaje: 'Guardando conjunto de APs…'));
    try {
      await _crearConjunto(
        planoId: planoId,
        nombre: nombre,
        proposito: proposito,
        descripcion: descripcion,
        bssids: bssids,
      );
      final conjuntos = await _listarConjuntos(planoId);
      emit(HeatmapConjuntos(
        aps: aps.isEmpty ? await _listarAPs(planoId) : aps,
        conjuntos: conjuntos,
        mensaje: 'Conjunto de APs creado.',
      ));
    } on HeatmapApiException catch (e) {
      emit(HeatmapConjuntos(
        aps: aps,
        conjuntos: actual is HeatmapConjuntos ? actual.conjuntos : const [],
        mensaje: e.mensaje,
      ));
    } catch (_) {
      emit(HeatmapConjuntos(
        aps: aps,
        conjuntos: actual is HeatmapConjuntos ? actual.conjuntos : const [],
        mensaje: 'No se pudo crear el conjunto.',
      ));
    }
  }

  Future<void> actualizarConjunto({
    required int conjuntoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required List<String> bssids,
  }) async {
    final actual = state;
    final planoId = _planoId;
    if (planoId == null) return;
    final aps = actual is HeatmapConjuntos ? actual.aps : <APDisponible>[];
    final conjuntosActuales =
        actual is HeatmapConjuntos ? actual.conjuntos : <ConjuntoAP>[];
    emit(const HeatmapLoading(mensaje: 'Guardando cambios…'));
    try {
      await _actualizarConjunto(
        conjuntoId: conjuntoId,
        nombre: nombre,
        proposito: proposito,
        descripcion: descripcion,
        bssids: bssids,
      );
      final conjuntos = await _listarConjuntos(planoId);
      emit(HeatmapConjuntos(
        aps: aps.isEmpty ? await _listarAPs(planoId) : aps,
        conjuntos: conjuntos,
        mensaje: 'Conjunto de APs actualizado.',
      ));
    } on HeatmapApiException catch (e) {
      emit(HeatmapConjuntos(
        aps: aps,
        conjuntos: conjuntosActuales,
        mensaje: e.mensaje,
      ));
    } catch (_) {
      emit(HeatmapConjuntos(
        aps: aps,
        conjuntos: conjuntosActuales,
        mensaje: 'No se pudo actualizar el conjunto.',
      ));
    }
  }

  Future<void> eliminarConjunto(int conjuntoId) async {
    final actual = state;
    final planoId = _planoId;
    if (planoId == null) return;
    final aps = actual is HeatmapConjuntos ? actual.aps : <APDisponible>[];
    final conjuntosActuales =
        actual is HeatmapConjuntos ? actual.conjuntos : <ConjuntoAP>[];
    emit(const HeatmapLoading(mensaje: 'Eliminando conjunto…'));
    try {
      await _eliminarConjunto(conjuntoId);
      final conjuntos = await _listarConjuntos(planoId);
      emit(HeatmapConjuntos(
        aps: aps.isEmpty ? await _listarAPs(planoId) : aps,
        conjuntos: conjuntos,
        mensaje: 'Conjunto de APs eliminado.',
      ));
    } on HeatmapApiException catch (e) {
      emit(HeatmapConjuntos(
        aps: aps,
        conjuntos: conjuntosActuales,
        mensaje: e.mensaje,
      ));
    } catch (_) {
      emit(HeatmapConjuntos(
        aps: aps,
        conjuntos: conjuntosActuales,
        mensaje: 'No se pudo eliminar el conjunto.',
      ));
    }
  }

  List<APDisponible> _apsDelConjunto({
    required List<APDisponible> aps,
    required ConjuntoAP conjunto,
  }) {
    final porBssid = {for (final ap in aps) ap.bssid: ap};
    return [
      for (final item in conjunto.items)
        if (porBssid[item.bssid] != null)
          APDisponible(
            bssid: porBssid[item.bssid]!.bssid,
            ssid: porBssid[item.bssid]!.ssid,
            canal: porBssid[item.bssid]!.canal,
            frecuenciaMhz: porBssid[item.bssid]!.frecuenciaMhz,
            rssiPromedio: porBssid[item.bssid]!.rssiPromedio,
            posX: item.posX == 0 ? porBssid[item.bssid]!.posX : item.posX,
            posY: item.posY == 0 ? porBssid[item.bssid]!.posY : item.posY,
            cantidadPuntos: porBssid[item.bssid]!.cantidadPuntos,
            seleccionado: porBssid[item.bssid]!.seleccionado,
          ),
    ];
  }

  void alternarAPInteres(APDisponible ap) {
    final actual = state;
    if (actual is HeatmapSeleccionAP) {
      final seleccionados = {...actual.bssidsSeleccionados};
      if (seleccionados.contains(ap.bssid)) {
        if (seleccionados.length == 1) {
          emit(actual.copyWith(
            bssidActivo: ap.bssid,
            mensaje: 'Debe quedar al menos un AP de interés seleccionado.',
          ));
          return;
        }
        seleccionados.remove(ap.bssid);
      } else {
        seleccionados.add(ap.bssid);
      }
      final activo = seleccionados.contains(actual.bssidActivo)
          ? actual.bssidActivo
          : seleccionados.first;
      emit(actual.copyWith(
        bssidsSeleccionados: seleccionados,
        bssidActivo: activo,
        mensaje:
            '${seleccionados.length} de ${actual.aps.length} APs seleccionados.',
      ));
    } else if (actual is HeatmapReady) {
      emit(HeatmapSeleccionAP(
        conjunto: actual.conjunto,
        aps: actual.aps,
        bssidsSeleccionados: actual.bssidsSeleccionados,
        bssidActivo: ap.bssid,
        apPosXPorBssid: actual.apPosXPorBssid,
        apPosYPorBssid: actual.apPosYPorBssid,
      ));
    }
  }

  void activarAP(APDisponible ap) {
    final actual = state;
    if (actual is HeatmapSeleccionAP) {
      emit(actual.copyWith(bssidActivo: ap.bssid));
    }
  }

  Future<void> alternarFiltroAP({
    required int planoId,
    required APDisponible ap,
    required String algoritmo,
    required int resolucion,
  }) async {
    final actual = state;
    if (actual is! HeatmapReady) return;
    final nuevoBssid = actual.bssidActivo == ap.bssid ? null : ap.bssid;
    emit(actual.copyWith(bssidActivo: nuevoBssid));
    await generar(
      planoId: planoId,
      algoritmo: algoritmo,
      resolucion: resolucion,
    );
  }

  Future<void> limpiarFiltroAP({
    required int planoId,
    required String algoritmo,
    required int resolucion,
  }) async {
    final actual = state;
    if (actual is! HeatmapReady || actual.bssidActivo == null) return;
    emit(actual.copyWith(bssidActivo: null));
    await generar(
      planoId: planoId,
      algoritmo: algoritmo,
      resolucion: resolucion,
    );
  }

  void ubicarAP({
    String? bssid,
    required double posX,
    required double posY,
    bool persistir = true,
  }) {
    final actual = state;
    if (actual is HeatmapSeleccionAP) {
      final posXPorBssid = {...actual.apPosXPorBssid};
      final posYPorBssid = {...actual.apPosYPorBssid};
      final bssidObjetivo =
          bssid ?? actual.bssidActivo ?? actual.apActivo.bssid;
      posXPorBssid[bssidObjetivo] = posX;
      posYPorBssid[bssidObjetivo] = posY;
      emit(actual.copyWith(
        bssidActivo: bssidObjetivo,
        apPosXPorBssid: posXPorBssid,
        apPosYPorBssid: posYPorBssid,
      ));
      final conjunto = actual.conjunto;
      if (conjunto != null && persistir) {
        _persistirUbicacionAPConjunto(
          conjuntoId: conjunto.id,
          bssid: bssidObjetivo,
          posX: posX,
          posY: posY,
        );
      }
    }
  }

  Future<void> _persistirUbicacionAPConjunto({
    required int conjuntoId,
    required String bssid,
    required double posX,
    required double posY,
  }) async {
    try {
      await _actualizarUbicacionAPConjunto(
        conjuntoId: conjuntoId,
        bssid: bssid,
        posX: posX,
        posY: posY,
      );
    } catch (_) {
      final actual = state;
      if (actual is HeatmapSeleccionAP) {
        emit(actual.copyWith(
          mensaje: 'No se pudo guardar la ubicación del AP.',
        ));
      }
    }
  }

  Future<void> generar({
    required int planoId,
    String algoritmo = 'IDW',
    int resolucion = 128,
  }) async {
    final actual = state;
    final contexto = switch (actual) {
      HeatmapSeleccionAP() => actual,
      HeatmapReady() => HeatmapSeleccionAP(
          conjunto: actual.conjunto,
          aps: actual.aps,
          bssidsSeleccionados: actual.bssidsSeleccionados,
          bssidActivo: actual.bssidActivo,
          apPosXPorBssid: actual.apPosXPorBssid,
          apPosYPorBssid: actual.apPosYPorBssid,
        ),
      _ => null,
    };
    if (contexto == null) return;
    final bssidFiltro = actual is HeatmapReady ? contexto.bssidActivo : null;
    final seleccionados = bssidFiltro == null
        ? contexto.apsSeleccionados
        : contexto.aps.where((ap) => ap.bssid == bssidFiltro).toList();
    if (seleccionados.isEmpty) {
      emit(contexto.copyWith(mensaje: 'Selecciona al menos un AP de interés.'));
      return;
    }
    emit(const HeatmapLoading(mensaje: 'Generando heatmap de APs…'));
    try {
      final bssids = seleccionados.map((ap) => ap.bssid).toList();
      final conjunto = contexto.conjunto;
      final mapa = conjunto == null
          ? await _generarHeatmap(
              planoId: planoId,
              algoritmo: algoritmo,
              resolucion: resolucion,
              bssids: bssids,
              apPosX: seleccionados.map(contexto.posXDe).toList(),
              apPosY: seleccionados.map(contexto.posYDe).toList(),
            )
          : await _generarHeatmapDesdeConjunto(
              conjuntoId: conjunto.id,
              modo: _modoGeneracion(
                totalConjunto: contexto.aps.length,
                seleccionados: bssids.length,
              ),
              algoritmo: algoritmo,
              resolucion: resolucion,
              bssids: bssids,
              apPosX: seleccionados.map(contexto.posXDe).toList(),
              apPosY: seleccionados.map(contexto.posYDe).toList(),
            );
      emit(HeatmapReady(
        mapa: mapa,
        conjunto: contexto.conjunto,
        aps: contexto.aps,
        bssidsSeleccionados: contexto.bssidsSeleccionados,
        bssidActivo: bssidFiltro,
        apPosXPorBssid: contexto.apPosXPorBssid,
        apPosYPorBssid: contexto.apPosYPorBssid,
      ));
    } on HeatmapApiException catch (e) {
      emit(HeatmapError(e.mensaje));
    } catch (_) {
      emit(const HeatmapError('No se pudo generar el heatmap.'));
    }
  }

  String _modoGeneracion({
    required int totalConjunto,
    required int seleccionados,
  }) {
    if (seleccionados == 1) return 'INDIVIDUAL';
    if (seleccionados == totalConjunto) return 'CONJUNTO_COMPLETO';
    return 'SUBCONJUNTO';
  }

}
