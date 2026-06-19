import 'package:flutter_bloc/flutter_bloc.dart';

import '../../domain/usecases/heatmap_usecases.dart';
import 'escenarios_state.dart';

class EscenariosCubit extends Cubit<EscenariosState> {
  final GenerarEscenariosUseCase _generar;
  final CompararEscenarioUseCase _comparar;
  final CrearReporteUseCase _crearReporte;

  EscenariosCubit({
    required GenerarEscenariosUseCase generar,
    required CompararEscenarioUseCase comparar,
    required CrearReporteUseCase crearReporte,
  })  : _generar = generar,
        _comparar = comparar,
        _crearReporte = crearReporte,
        super(const EscenariosState());

  Future<void> generar({
    required int proyectoId,
    int maxAps = 3,
    double? presupuesto,
    String bandaPreferida = '5',
    String modeloAp = 'AP WiFi 6 Bulldog BT-AX1800',
    double costoUnitario = 120,
  }) async {
    emit(state.copyWith(cargando: true, limpiarError: true));
    try {
      final escenarios = await _generar(
        proyectoId: proyectoId,
        maxAps: maxAps,
        presupuesto: presupuesto,
        bandaPreferida: bandaPreferida,
        modeloAp: modeloAp,
        costoUnitario: costoUnitario,
      );
      emit(state.copyWith(cargando: false, escenarios: escenarios));
    } catch (e) {
      emit(state.copyWith(cargando: false, error: e.toString()));
    }
  }

  Future<void> comparar(int escenarioId) async {
    emit(state.copyWith(cargando: true, limpiarError: true));
    try {
      final comparacion = await _comparar(escenarioId);
      emit(state.copyWith(cargando: false, comparacion: comparacion));
    } catch (e) {
      emit(state.copyWith(cargando: false, error: e.toString()));
    }
  }

  Future<void> crearReporte({
    required int proyectoId,
    int? escenarioId,
  }) async {
    emit(state.copyWith(cargando: true, limpiarError: true));
    try {
      final reporte = await _crearReporte(
        proyectoId: proyectoId,
        escenarioId: escenarioId,
      );
      emit(state.copyWith(cargando: false, reporte: reporte));
    } catch (e) {
      emit(state.copyWith(cargando: false, error: e.toString()));
    }
  }
}
