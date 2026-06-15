import '../../domain/entities/escala_heatmap.dart';

class EscalaHeatmapModel extends EscalaHeatmap {
  const EscalaHeatmapModel({
    required super.desde,
    required super.hasta,
    required super.colorHex,
    required super.etiqueta,
  });

  factory EscalaHeatmapModel.fromJson(Map<String, dynamic> json) {
    return EscalaHeatmapModel(
      desde: json['desde'] as int,
      hasta: json['hasta'] as int,
      colorHex: json['color'] as String,
      etiqueta: json['etiqueta'] as String,
    );
  }
}
