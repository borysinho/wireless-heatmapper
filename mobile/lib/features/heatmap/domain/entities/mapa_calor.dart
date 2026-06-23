import 'package:equatable/equatable.dart';

import 'ap_disponible.dart';
import 'escala_heatmap.dart';
import '../../../planos/domain/entities/plano.dart';

/// Mapa de calor generado por el backend. Sprint 4 — PB-05.
class MapaCalor extends Equatable {
  final int id;
  final int planoId;
  final int? conjuntoApId;
  final String modoGeneracion;
  final String algoritmo;
  final int resolucion;
  final String bssid;
  final String ssid;
  final double apPosX;
  final double apPosY;
  final List<APDisponible> apsInteres;
  final List<String> bssidsGeneracion;
  final String urlImagen;
  final List<List<double>> matriz;
  final List<EscalaHeatmap> escala;
  final int cantidadPuntos;
  final double rssiMin;
  final double rssiMax;
  final double rssiPromedio;
  final List<PuntoLecturaHeatmap> puntosLectura;
  final List<PuntoPlano> poligonoInteres;
  final List<String> advertencias;
  final DateTime createdAt;

  const MapaCalor({
    required this.id,
    required this.planoId,
    this.conjuntoApId,
    this.modoGeneracion = 'SUBCONJUNTO',
    required this.algoritmo,
    required this.resolucion,
    required this.bssid,
    required this.ssid,
    required this.apPosX,
    required this.apPosY,
    required this.apsInteres,
    this.bssidsGeneracion = const [],
    required this.urlImagen,
    required this.matriz,
    required this.escala,
    required this.cantidadPuntos,
    required this.rssiMin,
    required this.rssiMax,
    required this.rssiPromedio,
    required this.puntosLectura,
    this.poligonoInteres = const [],
    required this.advertencias,
    required this.createdAt,
  });

  @override
  List<Object?> get props => [
        id,
        planoId,
        conjuntoApId,
        modoGeneracion,
        algoritmo,
        resolucion,
        bssid,
        ssid,
        apPosX,
        apPosY,
        apsInteres,
        bssidsGeneracion,
        urlImagen,
        cantidadPuntos,
        rssiMin,
        rssiMax,
        rssiPromedio,
        puntosLectura,
        poligonoInteres,
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
