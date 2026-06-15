import '../../domain/entities/mapa_calor.dart';
import 'escala_heatmap_model.dart';

class MapaCalorModel extends MapaCalor {
  const MapaCalorModel({
    required super.id,
    required super.planoId,
    required super.algoritmo,
    required super.resolucion,
    required super.bssid,
    required super.ssid,
    required super.apPosX,
    required super.apPosY,
    required super.urlImagen,
    required super.matriz,
    required super.escala,
    required super.cantidadPuntos,
    required super.rssiMin,
    required super.rssiMax,
    required super.createdAt,
  });

  factory MapaCalorModel.fromJson(Map<String, dynamic> json) {
    return MapaCalorModel(
      id: json['id'] as int,
      planoId: json['plano_id'] as int,
      algoritmo: json['algoritmo'] as String,
      resolucion: json['resolucion'] as int,
      bssid: json['bssid'] as String,
      ssid: json['ssid'] as String,
      apPosX: (json['ap_pos_x'] as num).toDouble(),
      apPosY: (json['ap_pos_y'] as num).toDouble(),
      urlImagen: json['url_imagen'] as String,
      matriz: (json['matriz'] as List<dynamic>)
          .map(
            (fila) => (fila as List<dynamic>)
                .map((v) => (v as num).toDouble())
                .toList(),
          )
          .toList(),
      escala: (json['escala'] as List<dynamic>)
          .map((e) => EscalaHeatmapModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      cantidadPuntos: json['cantidad_puntos'] as int,
      rssiMin: (json['rssi_min'] as num).toDouble(),
      rssiMax: (json['rssi_max'] as num).toDouble(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}
