import 'package:equatable/equatable.dart';

import 'nivel_senal.dart';

/// Lectura RSSI de un BSSID individual, real o estimada por el backend.
class LecturaRSSI extends Equatable {
  final int id;
  final int puntoId;
  final String ssid;
  final String bssid;
  final int rssi;
  final int? canal;
  final int? frecuenciaMhz;
  final NivelSenal nivel;
  final int numeroLectura;
  final String origen;

  const LecturaRSSI({
    required this.id,
    required this.puntoId,
    required this.ssid,
    required this.bssid,
    required this.rssi,
    this.canal,
    this.frecuenciaMhz,
    required this.nivel,
    this.numeroLectura = 1,
    this.origen = 'CAMPO',
  });

  @override
  List<Object?> get props => [
        id,
        puntoId,
        ssid,
        bssid,
        rssi,
        canal,
        frecuenciaMhz,
        nivel,
        numeroLectura,
        origen,
      ];
}
