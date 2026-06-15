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
  final Set<String> bssidsSeleccionados;
  final String bssidActivo;
  final Map<String, double> apPosXPorBssid;
  final Map<String, double> apPosYPorBssid;
  final String? mensaje;

  HeatmapSeleccionAP({
    required this.aps,
    required Set<String> bssidsSeleccionados,
    required this.bssidActivo,
    required Map<String, double> apPosXPorBssid,
    required Map<String, double> apPosYPorBssid,
    this.mensaje,
  })  : bssidsSeleccionados = Set.unmodifiable(bssidsSeleccionados),
        apPosXPorBssid = Map.unmodifiable(apPosXPorBssid),
        apPosYPorBssid = Map.unmodifiable(apPosYPorBssid);

  APDisponible get apActivo => aps.firstWhere(
        (ap) => ap.bssid == bssidActivo,
        orElse: () => aps.first,
      );

  List<APDisponible> get apsSeleccionados =>
      aps.where((ap) => bssidsSeleccionados.contains(ap.bssid)).toList();

  double posXDe(APDisponible ap) => apPosXPorBssid[ap.bssid] ?? ap.posX;

  double posYDe(APDisponible ap) => apPosYPorBssid[ap.bssid] ?? ap.posY;

  HeatmapSeleccionAP copyWith({
    Set<String>? bssidsSeleccionados,
    String? bssidActivo,
    Map<String, double>? apPosXPorBssid,
    Map<String, double>? apPosYPorBssid,
    String? mensaje,
  }) {
    return HeatmapSeleccionAP(
      aps: aps,
      bssidsSeleccionados: bssidsSeleccionados ?? this.bssidsSeleccionados,
      bssidActivo: bssidActivo ?? this.bssidActivo,
      apPosXPorBssid: apPosXPorBssid ?? this.apPosXPorBssid,
      apPosYPorBssid: apPosYPorBssid ?? this.apPosYPorBssid,
      mensaje: mensaje,
    );
  }

  @override
  List<Object?> get props => [
        aps,
        bssidsSeleccionados.toList()..sort(),
        bssidActivo,
        apPosXPorBssid.entries
            .map((entry) => '${entry.key}:${entry.value}')
            .toList()
          ..sort(),
        apPosYPorBssid.entries
            .map((entry) => '${entry.key}:${entry.value}')
            .toList()
          ..sort(),
        mensaje,
      ];
}

class HeatmapReady extends HeatmapState {
  final MapaCalor mapa;
  final List<APDisponible> aps;
  final Set<String> bssidsSeleccionados;
  final String bssidActivo;
  final Map<String, double> apPosXPorBssid;
  final Map<String, double> apPosYPorBssid;
  final AnalisisCobertura? analisis;
  final bool analizando;
  final String? mensaje;

  HeatmapReady({
    required this.mapa,
    required this.aps,
    required Set<String> bssidsSeleccionados,
    required this.bssidActivo,
    required Map<String, double> apPosXPorBssid,
    required Map<String, double> apPosYPorBssid,
    this.analisis,
    this.analizando = false,
    this.mensaje,
  })  : bssidsSeleccionados = Set.unmodifiable(bssidsSeleccionados),
        apPosXPorBssid = Map.unmodifiable(apPosXPorBssid),
        apPosYPorBssid = Map.unmodifiable(apPosYPorBssid);

  HeatmapReady copyWith({
    MapaCalor? mapa,
    List<APDisponible>? aps,
    Set<String>? bssidsSeleccionados,
    String? bssidActivo,
    Map<String, double>? apPosXPorBssid,
    Map<String, double>? apPosYPorBssid,
    AnalisisCobertura? analisis,
    bool? analizando,
    String? mensaje,
  }) {
    return HeatmapReady(
      mapa: mapa ?? this.mapa,
      aps: aps ?? this.aps,
      bssidsSeleccionados: bssidsSeleccionados ?? this.bssidsSeleccionados,
      bssidActivo: bssidActivo ?? this.bssidActivo,
      apPosXPorBssid: apPosXPorBssid ?? this.apPosXPorBssid,
      apPosYPorBssid: apPosYPorBssid ?? this.apPosYPorBssid,
      analisis: analisis ?? this.analisis,
      analizando: analizando ?? this.analizando,
      mensaje: mensaje,
    );
  }

  @override
  List<Object?> get props => [
        mapa,
        aps,
        bssidsSeleccionados.toList()..sort(),
        bssidActivo,
        apPosXPorBssid.entries
            .map((entry) => '${entry.key}:${entry.value}')
            .toList()
          ..sort(),
        apPosYPorBssid.entries
            .map((entry) => '${entry.key}:${entry.value}')
            .toList()
          ..sort(),
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
