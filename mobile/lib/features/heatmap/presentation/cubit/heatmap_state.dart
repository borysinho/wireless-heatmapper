import 'package:equatable/equatable.dart';

import '../../domain/entities/analisis_cobertura.dart';
import '../../domain/entities/ap_disponible.dart';
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
  final String mensaje;

  const HeatmapLoading({this.mensaje = 'Cargando heatmap…'});

  @override
  List<Object?> get props => [mensaje];
}

class HeatmapSeleccionAP extends HeatmapState {
  final List<APDisponible> aps;
  final APDisponible apSeleccionado;
  final double apPosX;
  final double apPosY;
  final String? mensaje;

  const HeatmapSeleccionAP({
    required this.aps,
    required this.apSeleccionado,
    required this.apPosX,
    required this.apPosY,
    this.mensaje,
  });

  HeatmapSeleccionAP copyWith({
    APDisponible? apSeleccionado,
    double? apPosX,
    double? apPosY,
    String? mensaje,
  }) {
    return HeatmapSeleccionAP(
      aps: aps,
      apSeleccionado: apSeleccionado ?? this.apSeleccionado,
      apPosX: apPosX ?? this.apPosX,
      apPosY: apPosY ?? this.apPosY,
      mensaje: mensaje,
    );
  }

  @override
  List<Object?> get props => [aps, apSeleccionado, apPosX, apPosY, mensaje];
}

class HeatmapReady extends HeatmapState {
  final MapaCalor mapa;
  final List<APDisponible> aps;
  final APDisponible apSeleccionado;
  final AnalisisCobertura? analisis;
  final bool analizando;
  final String? mensaje;

  const HeatmapReady({
    required this.mapa,
    required this.aps,
    required this.apSeleccionado,
    this.analisis,
    this.analizando = false,
    this.mensaje,
  });

  HeatmapReady copyWith({
    MapaCalor? mapa,
    List<APDisponible>? aps,
    APDisponible? apSeleccionado,
    AnalisisCobertura? analisis,
    bool? analizando,
    String? mensaje,
  }) {
    return HeatmapReady(
      mapa: mapa ?? this.mapa,
      aps: aps ?? this.aps,
      apSeleccionado: apSeleccionado ?? this.apSeleccionado,
      analisis: analisis ?? this.analisis,
      analizando: analizando ?? this.analizando,
      mensaje: mensaje,
    );
  }

  @override
  List<Object?> get props => [
        mapa,
        aps,
        apSeleccionado,
        analisis,
        analizando,
        mensaje,
      ];
}

class HeatmapError extends HeatmapState {
  final String mensaje;

  const HeatmapError(this.mensaje);

  @override
  List<Object?> get props => [mensaje];
}
