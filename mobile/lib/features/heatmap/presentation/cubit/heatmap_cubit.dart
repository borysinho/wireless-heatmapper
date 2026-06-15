import 'package:flutter_bloc/flutter_bloc.dart';

import '../../data/datasources/heatmap_remote_datasource.dart';
import '../../domain/entities/ap_detectado.dart';
import '../../domain/usecases/heatmap_usecases.dart';
import 'heatmap_state.dart';

class HeatmapCubit extends Cubit<HeatmapState> {
  final GenerarHeatmapUseCase _generarHeatmap;
  final AnalizarMapaUseCase _analizarMapa;
  final ConfirmarAPUseCase _confirmarAP;

  HeatmapCubit({
    required GenerarHeatmapUseCase generarHeatmap,
    required AnalizarMapaUseCase analizarMapa,
    required ConfirmarAPUseCase confirmarAP,
  })  : _generarHeatmap = generarHeatmap,
        _analizarMapa = analizarMapa,
        _confirmarAP = confirmarAP,
        super(const HeatmapInitial());

  Future<void> cargar({
    required int planoId,
    String algoritmo = 'IDW',
    int resolucion = 128,
  }) async {
    emit(HeatmapLoading(algoritmo: algoritmo, resolucion: resolucion));
    try {
      final mapa = await _generarHeatmap(
        planoId: planoId,
        algoritmo: algoritmo,
        resolucion: resolucion,
      );
      emit(HeatmapReady(mapa: mapa, analizando: true));
      final analisis = await _analizarMapa(mapa.id);
      emit(HeatmapReady(mapa: mapa, analisis: analisis));
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
