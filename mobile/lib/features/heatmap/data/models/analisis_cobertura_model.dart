import '../../domain/entities/analisis_cobertura.dart';
import 'ap_detectado_model.dart';

class AnalisisCoberturaModel extends AnalisisCobertura {
  const AnalisisCoberturaModel({
    required super.id,
    required super.mapaCalorId,
    required super.pctCobertura,
    required super.pctZonasMuertas,
    required super.celdasZonasMuertas,
    required super.cantidadSolapamientos,
    required super.cantidadInterferencias,
    required super.hallazgos,
    required super.resumen,
    required super.apsDetectados,
  });

  factory AnalisisCoberturaModel.fromJson(Map<String, dynamic> json) {
    return AnalisisCoberturaModel(
      id: json['id'] as int,
      mapaCalorId: json['mapa_calor_id'] as int,
      pctCobertura: (json['pct_cobertura'] as num).toDouble(),
      pctZonasMuertas: (json['pct_zonas_muertas'] as num).toDouble(),
      celdasZonasMuertas: json['celdas_zonas_muertas'] as int,
      cantidadSolapamientos: json['cantidad_solapamientos'] as int,
      cantidadInterferencias: json['cantidad_interferencias'] as int,
      hallazgos: Map<String, dynamic>.from(json['hallazgos'] as Map),
      resumen: json['resumen'] as String,
      apsDetectados: (json['aps_detectados'] as List<dynamic>)
          .map((e) => APDetectadoModel.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }
}
