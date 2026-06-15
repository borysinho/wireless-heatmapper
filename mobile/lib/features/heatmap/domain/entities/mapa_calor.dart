import 'package:equatable/equatable.dart';

import 'ap_disponible.dart';
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
  final List<APDisponible> apsInteres;
  final String urlImagen;
  final List<List<double>> matriz;
  final List<EscalaHeatmap> escala;
  final int cantidadPuntos;
  final double rssiMin;
  final double rssiMax;
  final double rssiPromedio;
  final List<PuntoLecturaHeatmap> puntosLectura;
  final List<String> advertencias;
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
    required this.apsInteres,
    required this.urlImagen,
    required this.matriz,
    required this.escala,
    required this.cantidadPuntos,
    required this.rssiMin,
    required this.rssiMax,
    required this.rssiPromedio,
    required this.puntosLectura,
    required this.advertencias,
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
        apsInteres,
        urlImagen,
        cantidadPuntos,
        rssiMin,
        rssiMax,
        rssiPromedio,
        puntosLectura,
        advertencias,
        createdAt,
      ];
}

class PuntoLecturaHeatmap extends Equatable {
  final int puntoId;
  final double posX;
  final double posY;
  final double rssi;

  const PuntoLecturaHeatmap({
    required this.puntoId,
    required this.posX,
    required this.posY,
    required this.rssi,
  });

  @override
  List<Object?> get props => [puntoId, posX, posY, rssi];
}
