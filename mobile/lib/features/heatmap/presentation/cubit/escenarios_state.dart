import 'package:equatable/equatable.dart';

import '../../domain/entities/escenario_optimizado.dart';
import '../../domain/entities/inventario_rf.dart';

class EscenariosState extends Equatable {
  final bool cargando;
  final List<EscenarioOptimizado> escenarios;
  final ComparacionEscenario? comparacion;
  final ReporteTecnico? reporte;
  final InventarioRF? inventario;
  final String? error;

  const EscenariosState({
    this.cargando = false,
    this.escenarios = const [],
    this.comparacion,
    this.reporte,
    this.inventario,
    this.error,
  });

  EscenariosState copyWith({
    bool? cargando,
    List<EscenarioOptimizado>? escenarios,
    ComparacionEscenario? comparacion,
    ReporteTecnico? reporte,
    InventarioRF? inventario,
    String? error,
    bool limpiarError = false,
  }) {
    return EscenariosState(
      cargando: cargando ?? this.cargando,
      escenarios: escenarios ?? this.escenarios,
      comparacion: comparacion ?? this.comparacion,
      reporte: reporte ?? this.reporte,
      inventario: inventario ?? this.inventario,
      error: limpiarError ? null : error ?? this.error,
    );
  }

  @override
  List<Object?> get props => [
        cargando,
        escenarios,
        comparacion,
        reporte,
        inventario,
        error,
      ];
}
