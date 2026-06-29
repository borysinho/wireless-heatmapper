import '../../domain/entities/conjunto_ap.dart';
import 'ap_disponible_model.dart';

class ConjuntoAPModel extends ConjuntoAP {
  const ConjuntoAPModel({
    required super.id,
    required super.planoId,
    super.conjuntoOrigenId,
    required super.nombre,
    required super.proposito,
    required super.descripcion,
    required super.esPrincipal,
    super.bandaObjetivo,
    super.origen,
    super.creadoPorId,
    super.resumenIa,
    super.metricasIa,
    super.restriccionesIa,
    super.versionMotorIa,
    required super.cantidadAps,
    required super.items,
    required super.createdAt,
    required super.updatedAt,
  });

  factory ConjuntoAPModel.fromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List<dynamic>? ?? const [])
        .map((item) {
          final data = item as Map<String, dynamic>;
          return APDisponibleModel(
            bssid: data['bssid'] as String,
            ssid: data['ssid'] as String? ?? '',
            canal: data['canal'] as int?,
            frecuenciaMhz: data['frecuencia_mhz'] as int?,
            rssiPromedio: (data['rssi_promedio'] as num?)?.toDouble() ?? 0,
            posX: (data['pos_x'] as num?)?.toDouble() ?? 0,
            posY: (data['pos_y'] as num?)?.toDouble() ?? 0,
            cantidadPuntos: data['cantidad_puntos'] as int? ?? 0,
            seleccionado: false,
          );
        })
        .cast<APDisponibleModel>()
        .toList();
    return ConjuntoAPModel(
      id: json['id'] as int,
      planoId: json['plano_id'] as int,
      conjuntoOrigenId: json['conjunto_origen_id'] as int?,
      nombre: json['nombre'] as String,
      proposito: json['proposito'] as String,
      descripcion: json['descripcion'] as String?,
      esPrincipal: json['es_principal'] as bool? ?? false,
      bandaObjetivo: json['banda_objetivo'] as String? ?? '5',
      origen: json['origen'] as String? ?? 'manual_movil',
      creadoPorId: json['creado_por_id'] as int?,
      resumenIa: json['resumen_ia'] as String?,
      metricasIa: _mapaOpcional(json['metricas_ia']),
      restriccionesIa: _mapaOpcional(json['restricciones_ia']),
      versionMotorIa: json['version_motor_ia'] as String?,
      cantidadAps: json['cantidad_aps'] as int? ?? items.length,
      items: items,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  static Map<String, dynamic>? _mapaOpcional(Object? value) {
    if (value is Map<String, dynamic>) return value;
    if (value is Map) return Map<String, dynamic>.from(value);
    return null;
  }
}
