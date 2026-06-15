import '../../domain/entities/ap_detectado.dart';

class APDetectadoModel extends APDetectado {
  const APDetectadoModel({
    required super.id,
    required super.bssid,
    required super.ssid,
    super.canal,
    super.frecuenciaMhz,
    required super.rssiPromedio,
    required super.posX,
    required super.posY,
    required super.confirmado,
  });

  factory APDetectadoModel.fromJson(Map<String, dynamic> json) {
    return APDetectadoModel(
      id: json['id'] as int,
      bssid: json['bssid'] as String,
      ssid: json['ssid'] as String,
      canal: json['canal'] as int?,
      frecuenciaMhz: json['frecuencia_mhz'] as int?,
      rssiPromedio: (json['rssi_promedio'] as num).toDouble(),
      posX: (json['pos_x'] as num).toDouble(),
      posY: (json['pos_y'] as num).toDouble(),
      confirmado: json['confirmado'] as bool,
    );
  }
}
