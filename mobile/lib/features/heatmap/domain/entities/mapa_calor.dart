import 'package:equatable/equatable.dart';

import 'escala_heatmap.dart';

/// Mapa de calor generado por el backend. Sprint 4 — PB-05.
class MapaCalor extends Equatable {
  final int id;
  final int planoId;
  final String algoritmo;
  final int resolucion;
  final String bssid;
  final String ssid;
  final double apPosX;
  final double apPosY;
  final String urlImagen;
  final List<List<double>> matriz;
  final List<EscalaHeatmap> escala;
  final int cantidadPuntos;
  final double rssiMin;
  final double rssiMax;
  final DateTime createdAt;

  const MapaCalor({
    required this.id,
    required this.planoId,
    required this.algoritmo,
    required this.resolucion,
    required this.bssid,
    required this.ssid,
    required this.apPosX,
    required this.apPosY,
    required this.urlImagen,
    required this.matriz,
    required this.escala,
    required this.cantidadPuntos,
    required this.rssiMin,
    required this.rssiMax,
    required this.createdAt,
  });

  @override
  List<Object?> get props => [
        id,
        planoId,
        algoritmo,
        resolucion,
        bssid,
        ssid,
        apPosX,
        apPosY,
        urlImagen,
        cantidadPuntos,
        rssiMin,
        rssiMax,
        createdAt,
      ];
}
