import '../../domain/entities/mapa_calor.dart';
import '../../../planos/domain/entities/plano.dart';
import 'ap_disponible_model.dart';
import 'escala_heatmap_model.dart';

class MapaCalorModel extends MapaCalor {
  const MapaCalorModel({
    required super.id,
    required super.planoId,
    required super.conjuntoApId,
    required super.modoGeneracion,
    required super.algoritmo,
    required super.resolucion,
    required super.bssid,
    required super.ssid,
    required super.apPosX,
    required super.apPosY,
    required super.apsInteres,
    required super.bssidsGeneracion,
    required super.urlImagen,
    required super.matriz,
    required super.escala,
    required super.cantidadPuntos,
    required super.rssiMin,
    required super.rssiMax,
    required super.rssiPromedio,
    required super.puntosLectura,
    required super.poligonoInteres,
    required super.advertencias,
    required super.createdAt,
  });

  factory MapaCalorModel.fromJson(Map<String, dynamic> json) {
    return MapaCalorModel(
      id: json['id'] as int,
      planoId: json['plano_id'] as int,
      conjuntoApId: json['conjunto_ap_id'] as int?,
      modoGeneracion: json['modo_generacion'] as String? ?? 'SUBCONJUNTO',
      algoritmo: json['algoritmo'] as String,
      resolucion: json['resolucion'] as int,
      bssid: json['bssid'] as String,
      ssid: json['ssid'] as String,
      apPosX: (json['ap_pos_x'] as num).toDouble(),
      apPosY: (json['ap_pos_y'] as num).toDouble(),
      apsInteres: _apsInteresDesdeJson(json),
      bssidsGeneracion:
          (json['bssids_generacion'] as List<dynamic>? ?? const [])
              .map((item) => item.toString())
              .toList(),
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
      rssiPromedio: (json['rssi_promedio'] as num?)?.toDouble() ??
          (((json['rssi_min'] as num).toDouble() +
                  (json['rssi_max'] as num).toDouble()) /
              2),
      puntosLectura: _puntosLecturaDesdeJson(json),
      poligonoInteres: _poligonoDesdeJson(json['poligono_interes']),
      advertencias: (json['advertencias'] as List<dynamic>? ?? const [])
          .map((item) => item.toString())
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  static List<PuntoPlano> _poligonoDesdeJson(dynamic json) {
    if (json is! List<dynamic>) return const [];
    return json.map((item) {
      final data = item as Map<String, dynamic>;
      return PuntoPlano(
        x: (data['x'] as num).toDouble(),
        y: (data['y'] as num).toDouble(),
      );
    }).toList();
  }

  static List<PuntoLecturaHeatmap> _puntosLecturaDesdeJson(
    Map<String, dynamic> json,
  ) {
    final puntos = json['puntos_lectura'];
    if (puntos is! List<dynamic>) return const [];
    return puntos.map(
      (item) {
        final data = item as Map<String, dynamic>;
        return PuntoLecturaHeatmap(
          puntoId: data['punto_id'] as int,
          posX: (data['pos_x'] as num).toDouble(),
          posY: (data['pos_y'] as num).toDouble(),
          rssi: (data['rssi'] as num).toDouble(),
        );
      },
    ).toList();
  }

  static List<APDisponibleModel> _apsInteresDesdeJson(
    Map<String, dynamic> json,
  ) {
    final aps = json['aps_interes'];
    if (aps is List<dynamic>) {
      return aps
          .map((e) => APDisponibleModel.fromJson(e as Map<String, dynamic>))
          .toList();
    }
    return [
      APDisponibleModel(
        bssid: json['bssid'] as String,
        ssid: json['ssid'] as String,
        canal: null,
        frecuenciaMhz: null,
        rssiPromedio: 0,
        posX: (json['ap_pos_x'] as num).toDouble(),
        posY: (json['ap_pos_y'] as num).toDouble(),
        cantidadPuntos: json['cantidad_puntos'] as int,
        seleccionado: true,
      ),
    ];
  }
}
