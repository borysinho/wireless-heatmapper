import 'dart:io';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:path_provider/path_provider.dart';

import '../../domain/entities/escenario_optimizado.dart';
import '../../domain/repositories/heatmap_repository.dart';
import '../../domain/usecases/heatmap_usecases.dart';
import 'escenarios_state.dart';

class EscenariosCubit extends Cubit<EscenariosState> {
  final HeatmapRepository _repositorio;
  final GenerarEscenariosUseCase _generar;
  final CompararEscenarioUseCase _comparar;
  final CrearReporteUseCase _crearReporte;
  final DescargarReporteUseCase? _descargarReporte;

  EscenariosCubit({
    GenerarEscenariosUseCase? generar,
    CompararEscenarioUseCase? comparar,
    CrearReporteUseCase? crearReporte,
    DescargarReporteUseCase? descargarReporte,
    HeatmapRepository? repositorio,
  })  : _repositorio = repositorio ?? GetIt.I<HeatmapRepository>(),
        _generar = generar ?? GetIt.I<GenerarEscenariosUseCase>(),
        _comparar = comparar ?? GetIt.I<CompararEscenarioUseCase>(),
        _crearReporte = crearReporte ?? GetIt.I<CrearReporteUseCase>(),
        _descargarReporte = descargarReporte,
        super(const EscenariosState());

  Future<void> cargarInventario(int proyectoId) async {
    emit(state.copyWith(cargando: true, limpiarError: true));
    try {
      final inventario = await _repositorio.obtenerInventarioRF(proyectoId);
      emit(state.copyWith(cargando: false, inventario: inventario));
    } catch (e) {
      emit(state.copyWith(cargando: false, error: e.toString()));
    }
  }

  Future<void> crearAPFisico({
    required int proyectoId,
    required Map<String, dynamic> datos,
  }) async {
    emit(state.copyWith(cargando: true, limpiarError: true));
    try {
      await _repositorio.crearAPFisicoRF(proyectoId: proyectoId, datos: datos);
      final inventario = await _repositorio.obtenerInventarioRF(proyectoId);
      emit(state.copyWith(cargando: false, inventario: inventario));
    } catch (e) {
      emit(state.copyWith(cargando: false, error: e.toString()));
    }
  }

  Future<void> generar({
    required int proyectoId,
    int maxAps = 3,
    double? presupuesto,
    String bandaPreferida = '5',
    List<String> bandas = const ['2.4', '5'],
    String tipoNegocio = 'INSTALACION_NUEVA',
    String perfil = 'COBERTURA_EQUILIBRADA',
    String politicaCombinacion = 'PREFERIR_5_GHZ_SI_CUMPLE_UMBRAL',
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
        bandas: bandas,
        tipoNegocio: tipoNegocio,
        perfil: perfil,
        politicaCombinacion: politicaCombinacion,
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

  Future<void> crearYCompartirReporte({
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
      final descargarReporte = _resolverDescargaReporte();
      final dir = await getTemporaryDirectory();
      final carpeta = Directory('${dir.path}/reportes-heatmapper');
      if (!await carpeta.exists()) {
        await carpeta.create(recursive: true);
      }
      final rutaDestino =
          '${carpeta.path}/reporte-heatmapper-${reporte.id}.pdf';
      final rutaLocal = await descargarReporte(
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

  DescargarReporteUseCase _resolverDescargaReporte() {
    if (_descargarReporte != null) return _descargarReporte;
    if (GetIt.I.isRegistered<DescargarReporteUseCase>()) {
      return GetIt.I<DescargarReporteUseCase>();
    }
    if (GetIt.I.isRegistered<HeatmapRepository>()) {
      return DescargarReporteUseCase(GetIt.I<HeatmapRepository>());
    }
    throw StateError(
      'No se pudo inicializar la descarga del reporte. '
      'Reinicia la app para cargar las dependencias.',
    );
  }
}
