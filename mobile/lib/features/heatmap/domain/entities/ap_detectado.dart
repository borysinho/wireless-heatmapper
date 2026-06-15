import 'package:equatable/equatable.dart';

/// Access point detectado en el análisis. Sprint 4 — PB-06.
class APDetectado extends Equatable {
  final int id;
  final String bssid;
  final String ssid;
  final int? canal;
  final int? frecuenciaMhz;
  final double rssiPromedio;
  final double posX;
  final double posY;
  final bool confirmado;

  const APDetectado({
    required this.id,
    required this.bssid,
    required this.ssid,
    this.canal,
    this.frecuenciaMhz,
    required this.rssiPromedio,
    required this.posX,
    required this.posY,
    required this.confirmado,
  });

  APDetectado copyWith({
    double? posX,
    double? posY,
    bool? confirmado,
  }) {
    return APDetectado(
      id: id,
      bssid: bssid,
      ssid: ssid,
      canal: canal,
      frecuenciaMhz: frecuenciaMhz,
      rssiPromedio: rssiPromedio,
      posX: posX ?? this.posX,
      posY: posY ?? this.posY,
      confirmado: confirmado ?? this.confirmado,
    );
  }

  @override
  List<Object?> get props => [
        id,
        bssid,
        ssid,
        canal,
        frecuenciaMhz,
        rssiPromedio,
        posX,
        posY,
        confirmado,
      ];
}
