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
        apSeleccionado: ap,
        apPosX: ap.posX,
        apPosY: ap.posY,
      ));
    } on HeatmapApiException catch (e) {
      emit(HeatmapError(e.mensaje));
    } catch (_) {
      emit(const HeatmapError('No se pudieron cargar los APs detectados.'));
    }
  }

  void seleccionarAP(APDisponible ap) {
    final actual = state;
    if (actual is HeatmapSeleccionAP) {
      emit(actual.copyWith(
        apSeleccionado: ap,
        apPosX: ap.posX,
        apPosY: ap.posY,
      ));
    } else if (actual is HeatmapReady) {
      emit(HeatmapSeleccionAP(
        aps: actual.aps,
        apSeleccionado: ap,
        apPosX: ap.posX,
        apPosY: ap.posY,
      ));
    }
  }

  void ubicarAP({required double posX, required double posY}) {
    final actual = state;
    if (actual is HeatmapSeleccionAP) {
      emit(actual.copyWith(
        apPosX: posX,
        apPosY: posY,
        mensaje: 'Ubicación del AP actualizada.',
      ));
    }
  }

  Future<void> generar({
    required int planoId,
    required APDisponible ap,
    required double apPosX,
    required double apPosY,
    String algoritmo = 'IDW',
    int resolucion = 128,
  }) async {
    final aps = switch (state) {
      HeatmapSeleccionAP(:final aps) => aps,
      HeatmapReady(:final aps) => aps,
      _ => <APDisponible>[],
    };
    emit(const HeatmapLoading(mensaje: 'Generando heatmap del AP…'));
    try {
      final mapa = await _generarHeatmap(
        planoId: planoId,
        algoritmo: algoritmo,
        resolucion: resolucion,
        bssid: ap.bssid,
        apPosX: apPosX,
        apPosY: apPosY,
      );
      emit(HeatmapReady(
        mapa: mapa,
        aps: aps,
        apSeleccionado: ap,
        analizando: true,
      ));
      final analisis = await _analizarMapa(mapa.id);
      emit(HeatmapReady(
        mapa: mapa,
        aps: aps,
        apSeleccionado: ap,
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
