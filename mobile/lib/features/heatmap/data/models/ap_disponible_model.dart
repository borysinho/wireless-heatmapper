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
    super.seleccionado,
    super.potenciaTxDbm,
    super.fuentePotencia,
    super.confianzaPotencia,
    super.radios,
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
      seleccionado: json['seleccionado'] as bool? ?? false,
      potenciaTxDbm: (json['potencia_tx_dbm'] as num?)?.toDouble(),
      fuentePotencia: json['fuente_potencia'] as String?,
      confianzaPotencia: json['confianza_potencia'] as String?,
      radios: _listaMapas(json['radios']),
    );
  }

  static List<Map<String, dynamic>>? _listaMapas(Object? value) {
    if (value is! List) return null;
    return value
        .whereType<Map>()
        .map((item) => Map<String, dynamic>.from(item))
        .toList(growable: false);
  }
}
