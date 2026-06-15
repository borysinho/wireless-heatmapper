import 'package:equatable/equatable.dart';

import '../../domain/entities/analisis_cobertura.dart';
import '../../domain/entities/mapa_calor.dart';

sealed class HeatmapState extends Equatable {
  const HeatmapState();

  @override
  List<Object?> get props => [];
}

class HeatmapInitial extends HeatmapState {
  const HeatmapInitial();
}

class HeatmapLoading extends HeatmapState {
  final String algoritmo;
  final int resolucion;

  const HeatmapLoading({
    required this.algoritmo,
    required this.resolucion,
  });

  @override
  List<Object?> get props => [algoritmo, resolucion];
}

class HeatmapReady extends HeatmapState {
  final MapaCalor mapa;
  final AnalisisCobertura? analisis;
  final bool analizando;
  final String? mensaje;

  const HeatmapReady({
    required this.mapa,
    this.analisis,
    this.analizando = false,
    this.mensaje,
  });

  HeatmapReady copyWith({
    MapaCalor? mapa,
    AnalisisCobertura? analisis,
    bool? analizando,
    String? mensaje,
  }) {
    return HeatmapReady(
      mapa: mapa ?? this.mapa,
      analisis: analisis ?? this.analisis,
      analizando: analizando ?? this.analizando,
      mensaje: mensaje,
    );
  }

  @override
  List<Object?> get props => [mapa, analisis, analizando, mensaje];
}

class HeatmapError extends HeatmapState {
  final String mensaje;

  const HeatmapError(this.mensaje);

  @override
  List<Object?> get props => [mensaje];
}
