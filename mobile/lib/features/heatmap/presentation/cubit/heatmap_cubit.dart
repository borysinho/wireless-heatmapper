import 'package:flutter_bloc/flutter_bloc.dart';

import '../../data/datasources/heatmap_remote_datasource.dart';
import '../../domain/entities/ap_disponible.dart';
import '../../domain/entities/ap_detectado.dart';
import '../../domain/usecases/heatmap_usecases.dart';
import 'heatmap_state.dart';

class HeatmapCubit extends Cubit<HeatmapState> {
  final ListarAPsDisponiblesUseCase _listarAPs;
  final GenerarHeatmapUseCase _generarHeatmap;
  final AnalizarMapaUseCase _analizarMapa;
  final ConfirmarAPUseCase _confirmarAP;

  HeatmapCubit({
    required ListarAPsDisponiblesUseCase listarAPs,
    required GenerarHeatmapUseCase generarHeatmap,
    required AnalizarMapaUseCase analizarMapa,
    required ConfirmarAPUseCase confirmarAP,
  })  : _listarAPs = listarAPs,
        _generarHeatmap = generarHeatmap,
        _analizarMapa = analizarMapa,
        _confirmarAP = confirmarAP,
        super(const HeatmapInitial());

  Future<void> iniciar(int planoId) async {
    emit(const HeatmapLoading(mensaje: 'Buscando APs detectados…'));
    try {
      final aps = await _listarAPs(planoId);
      if (aps.isEmpty) {
        emit(const HeatmapError(
          'No hay APs detectados. Registra mediciones antes de generar heatmaps.',
        ));
        return;
      }
      final ap = aps.first;
      emit(HeatmapSeleccionAP(
        aps: aps,
        bssidsSeleccionados: {ap.bssid},
        bssidActivo: ap.bssid,
        apPosXPorBssid: {for (final item in aps) item.bssid: item.posX},
        apPosYPorBssid: {for (final item in aps) item.bssid: item.posY},
      ));
    } on HeatmapApiException catch (e) {
      emit(HeatmapError(e.mensaje));
    } catch (_) {
      emit(const HeatmapError('No se pudieron cargar los APs detectados.'));
    }
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
      final activo =
          seleccionados.contains(ap.bssid) ? ap.bssid : seleccionados.first;
      emit(actual.copyWith(
        bssidsSeleccionados: seleccionados,
        bssidActivo: activo,
        mensaje: seleccionados.contains(ap.bssid)
            ? 'AP agregado a los APs de interés.'
            : 'AP quitado de los APs de interés.',
      ));
    } else if (actual is HeatmapReady) {
      emit(HeatmapSeleccionAP(
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

  void ubicarAP({String? bssid, required double posX, required double posY}) {
    final actual = state;
    if (actual is HeatmapSeleccionAP) {
      final posXPorBssid = {...actual.apPosXPorBssid};
      final posYPorBssid = {...actual.apPosYPorBssid};
      final bssidObjetivo = bssid ?? actual.bssidActivo;
      posXPorBssid[bssidObjetivo] = posX;
      posYPorBssid[bssidObjetivo] = posY;
      emit(actual.copyWith(
        bssidActivo: bssidObjetivo,
        apPosXPorBssid: posXPorBssid,
        apPosYPorBssid: posYPorBssid,
      ));
    }
  }

  Future<void> generar({
    required int planoId,
    String algoritmo = 'IDW',
    int resolucion = 128,
  }) async {
    final actual = state;
    if (actual is! HeatmapSeleccionAP) return;
    final seleccionados = actual.apsSeleccionados;
    if (seleccionados.isEmpty) {
      emit(actual.copyWith(mensaje: 'Selecciona al menos un AP de interés.'));
      return;
    }
    emit(const HeatmapLoading(mensaje: 'Generando heatmap de APs…'));
    try {
      final mapa = await _generarHeatmap(
        planoId: planoId,
        algoritmo: algoritmo,
        resolucion: resolucion,
        bssids: seleccionados.map((ap) => ap.bssid).toList(),
        apPosX: seleccionados.map(actual.posXDe).toList(),
        apPosY: seleccionados.map(actual.posYDe).toList(),
      );
      emit(HeatmapReady(
        mapa: mapa,
        aps: actual.aps,
        bssidsSeleccionados: actual.bssidsSeleccionados,
        bssidActivo: actual.bssidActivo,
        apPosXPorBssid: actual.apPosXPorBssid,
        apPosYPorBssid: actual.apPosYPorBssid,
        analizando: true,
      ));
      final analisis = await _analizarMapa(mapa.id);
      emit(HeatmapReady(
        mapa: mapa,
        aps: actual.aps,
        bssidsSeleccionados: actual.bssidsSeleccionados,
        bssidActivo: actual.bssidActivo,
        apPosXPorBssid: actual.apPosXPorBssid,
        apPosYPorBssid: actual.apPosYPorBssid,
        analisis: analisis,
      ));
    } on HeatmapApiException catch (e) {
      emit(HeatmapError(e.mensaje));
    } catch (_) {
      emit(const HeatmapError('No se pudo generar el heatmap.'));
    }
  }

  Future<void> regenerarAnalisis() async {
    final actual = state;
    if (actual is! HeatmapReady) return;
    emit(actual.copyWith(analizando: true, mensaje: null));
    try {
      final analisis = await _analizarMapa(actual.mapa.id);
      emit(actual.copyWith(analisis: analisis, analizando: false));
    } on HeatmapApiException catch (e) {
      emit(actual.copyWith(analizando: false, mensaje: e.mensaje));
    } catch (_) {
      emit(actual.copyWith(
        analizando: false,
        mensaje: 'No se pudo actualizar el análisis.',
      ));
    }
  }

  Future<void> confirmarAP(APDetectado ap) async {
    final actual = state;
    if (actual is! HeatmapReady || actual.analisis == null) return;
    try {
      final actualizado = await _confirmarAP(
        apId: ap.id,
        posX: ap.posX,
        posY: ap.posY,
      );
      final aps = actual.analisis!.apsDetectados
          .map((item) => item.id == ap.id ? actualizado : item)
          .toList();
      emit(actual.copyWith(
        analisis: actual.analisis!.copyWith(apsDetectados: aps),
        mensaje: 'Ubicación del AP confirmada.',
      ));
    } on HeatmapApiException catch (e) {
      emit(actual.copyWith(mensaje: e.mensaje));
    } catch (_) {
      emit(actual.copyWith(mensaje: 'No se pudo confirmar el AP.'));
    }
  }
}
