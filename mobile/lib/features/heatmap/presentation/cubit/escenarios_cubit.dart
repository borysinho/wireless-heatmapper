import 'dart:io';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:path_provider/path_provider.dart';

import '../../domain/entities/escenario_optimizado.dart';
import '../../domain/usecases/heatmap_usecases.dart';
import 'escenarios_state.dart';

class EscenariosCubit extends Cubit<EscenariosState> {
  final GenerarEscenariosUseCase _generar;
  final CompararEscenarioUseCase _comparar;
  final CrearReporteUseCase _crearReporte;
  final DescargarReporteUseCase _descargarReporte;

  EscenariosCubit({
    GenerarEscenariosUseCase? generar,
    CompararEscenarioUseCase? comparar,
    CrearReporteUseCase? crearReporte,
    DescargarReporteUseCase? descargarReporte,
  })  : _generar = generar ?? GetIt.I<GenerarEscenariosUseCase>(),
        _comparar = comparar ?? GetIt.I<CompararEscenarioUseCase>(),
        _crearReporte = crearReporte ?? GetIt.I<CrearReporteUseCase>(),
        _descargarReporte =
            descargarReporte ?? GetIt.I<DescargarReporteUseCase>(),
        super(const EscenariosState());

  Future<void> generar({
    required int proyectoId,
    int maxAps = 3,
    double? presupuesto,
    String bandaPreferida = '5',
    String modeloAp = 'AP empresarial de potencia ajustable',
    double costoUnitario = 1,
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

  Future<void> crearYDescargarReporte({
    required int proyectoId,
    int? escenarioId,
  }) async {
    emit(state.copyWith(cargando: true, limpiarError: true));
    try {
      final reporte = await _crearReporte(
        proyectoId: proyectoId,
        escenarioId: escenarioId,
      );
      if (reporte.estado != 'LISTO' || reporte.urlDescarga == null) {
        emit(state.copyWith(cargando: false, reporte: reporte));
        return;
      }
      final dir = await getApplicationDocumentsDirectory();
      final carpeta = Directory('${dir.path}/reportes');
      if (!await carpeta.exists()) {
        await carpeta.create(recursive: true);
      }
      final rutaDestino = '${carpeta.path}/reporte-${reporte.id}.pdf';
      final rutaLocal = await _descargarReporte(
        urlDescarga: reporte.urlDescarga!,
        rutaDestino: rutaDestino,
      );
      emit(
        state.copyWith(
          cargando: false,
          reporte: ReporteTecnico(
            id: reporte.id,
            proyectoId: reporte.proyectoId,
            escenarioId: reporte.escenarioId,
            estado: reporte.estado,
            urlDescarga: reporte.urlDescarga,
            rutaLocal: rutaLocal,
            sha256: reporte.sha256,
            tamanioBytes: reporte.tamanioBytes,
            error: reporte.error,
          ),
        ),
      );
    } catch (e) {
      emit(state.copyWith(cargando: false, error: e.toString()));
    }
  }
}
