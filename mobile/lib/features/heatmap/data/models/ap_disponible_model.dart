import '../../domain/entities/ap_disponible.dart';

class APDisponibleModel extends APDisponible {
  const APDisponibleModel({
    required super.bssid,
    required super.ssid,
    super.canal,
    super.frecuenciaMhz,
    required super.rssiPromedio,
    required super.posX,
    required super.posY,
    required super.cantidadPuntos,
  });

  factory APDisponibleModel.fromJson(Map<String, dynamic> json) {
    return APDisponibleModel(
      bssid: json['bssid'] as String,
      ssid: json['ssid'] as String,
      canal: json['canal'] as int?,
      frecuenciaMhz: json['frecuencia_mhz'] as int?,
      rssiPromedio: (json['rssi_promedio'] as num).toDouble(),
      posX: (json['pos_x'] as num).toDouble(),
      posY: (json['pos_y'] as num).toDouble(),
      cantidadPuntos: json['cantidad_puntos'] as int,
    );
  }
}
