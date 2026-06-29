import '../../domain/entities/lectura_rssi.dart';
import '../../domain/entities/nivel_senal.dart';

class LecturaRSSIModel extends LecturaRSSI {
  const LecturaRSSIModel({
    required super.id,
    required super.puntoId,
    required super.ssid,
    required super.bssid,
    required super.rssi,
    super.canal,
    super.frecuenciaMhz,
    required super.nivel,
    super.numeroLectura = 1,
    super.origen = 'CAMPO',
  });

  factory LecturaRSSIModel.fromJson(Map<String, dynamic> json) {
    return LecturaRSSIModel(
      id: json['id'] as int,
      puntoId: json['punto_id'] as int,
      ssid: json['ssid'] as String,
      bssid: json['bssid'] as String,
      rssi: json['rssi'] as int,
      canal: json['canal'] as int?,
      frecuenciaMhz: json['frecuencia_mhz'] as int?,
      nivel: NivelSenal.fromString(json['nivel'] as String),
      numeroLectura: json['numero_lectura'] as int? ?? 1,
      origen: json['origen'] as String? ?? 'CAMPO',
    );
  }
}
