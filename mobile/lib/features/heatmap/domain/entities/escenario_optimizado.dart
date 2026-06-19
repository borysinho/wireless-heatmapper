import 'package:equatable/equatable.dart';

import 'mapa_calor.dart';

class RecomendacionAP extends Equatable {
  final int id;
  final int orden;
  final String accion;
  final double coordX;
  final double coordY;
  final String banda;
  final String modeloAp;
  final double costoEstimado;
  final double rssiProyectado;
  final String justificacion;

  const RecomendacionAP({
    required this.id,
    required this.orden,
    required this.accion,
    required this.coordX,
    required this.coordY,
    required this.banda,
    required this.modeloAp,
    required this.costoEstimado,
    required this.rssiProyectado,
    required this.justificacion,
  });

  @override
  List<Object?> get props => [
        id,
        orden,
        accion,
        coordX,
        coordY,
        banda,
        modeloAp,
        costoEstimado,
        rssiProyectado,
        justificacion,
      ];
}

class EscenarioOptimizado extends Equatable {
  final int id;
  final int proyectoId;
  final int planoId;
  final int? mapaActualId;
  final int? mapaProyectadoId;
  final String nombre;
  final String banda;
  final String modeloAp;
  final double pctCoberturaActual;
  final double pctCobertura;
  final double costoEstimado;
  final int cantidadAps;
  final String resumen;
  final Map<String, dynamic> restricciones;
  final Map<String, dynamic> metricas;
  final List<RecomendacionAP> recomendaciones;
  final DateTime createdAt;

  const EscenarioOptimizado({
    required this.id,
    required this.proyectoId,
    required this.planoId,
    required this.mapaActualId,
    required this.mapaProyectadoId,
    required this.nombre,
    required this.banda,
    required this.modeloAp,
    required this.pctCoberturaActual,
    required this.pctCobertura,
    required this.costoEstimado,
    required this.cantidadAps,
    required this.resumen,
    required this.restricciones,
    required this.metricas,
    required this.recomendaciones,
    required this.createdAt,
  });

  @override
  List<Object?> get props => [
        id,
        proyectoId,
        planoId,
        mapaActualId,
        mapaProyectadoId,
        nombre,
        banda,
        modeloAp,
        pctCoberturaActual,
        pctCobertura,
        costoEstimado,
        cantidadAps,
        resumen,
        recomendaciones,
        createdAt,
      ];
}

class ResumenComparacion extends Equatable {
  final double deltaPctCobertura;
  final int deltaZonasMuertas;
  final double costoEstimado;
  final int cantidadCambios;
  final String lectura;

  const ResumenComparacion({
    required this.deltaPctCobertura,
    required this.deltaZonasMuertas,
    required this.costoEstimado,
    required this.cantidadCambios,
    required this.lectura,
  });

  @override
  List<Object?> get props => [
        deltaPctCobertura,
        deltaZonasMuertas,
        costoEstimado,
        cantidadCambios,
        lectura,
      ];
}

class ComparacionEscenario extends Equatable {
  final EscenarioOptimizado escenario;
  final MapaCalor heatmapActual;
  final MapaCalor heatmapProyectado;
  final List<List<double>> matrizDiferencia;
  final ResumenComparacion resumen;

  const ComparacionEscenario({
    required this.escenario,
    required this.heatmapActual,
    required this.heatmapProyectado,
    required this.matrizDiferencia,
    required this.resumen,
  });

  @override
  List<Object?> get props => [
        escenario,
        heatmapActual,
        heatmapProyectado,
        matrizDiferencia,
        resumen,
      ];
}

class ReporteTecnico extends Equatable {
  final int id;
  final int proyectoId;
  final int? escenarioId;
  final String estado;
  final String? urlDescarga;
  final String? sha256;
  final int tamanioBytes;
  final String? error;

  const ReporteTecnico({
    required this.id,
    required this.proyectoId,
    required this.escenarioId,
    required this.estado,
    required this.urlDescarga,
    required this.sha256,
    required this.tamanioBytes,
    required this.error,
  });

  @override
  List<Object?> get props => [
        id,
        proyectoId,
        escenarioId,
        estado,
        urlDescarga,
        sha256,
        tamanioBytes,
        error,
      ];
}
