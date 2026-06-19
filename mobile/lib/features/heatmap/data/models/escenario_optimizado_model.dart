import '../../domain/entities/escenario_optimizado.dart';
import 'mapa_calor_model.dart';

class RecomendacionAPModel extends RecomendacionAP {
  const RecomendacionAPModel({
    required super.id,
    required super.orden,
    required super.accion,
    required super.coordX,
    required super.coordY,
    required super.banda,
    required super.modeloAp,
    required super.costoEstimado,
    required super.rssiProyectado,
    required super.justificacion,
  });

  factory RecomendacionAPModel.fromJson(Map<String, dynamic> json) {
    return RecomendacionAPModel(
      id: json['id'] as int,
      orden: json['orden'] as int,
      accion: json['accion'] as String,
      coordX: (json['coord_x'] as num).toDouble(),
      coordY: (json['coord_y'] as num).toDouble(),
      banda: json['banda'] as String,
      modeloAp: json['modelo_ap'] as String,
      costoEstimado: (json['costo_estimado'] as num).toDouble(),
      rssiProyectado: (json['rssi_proyectado'] as num).toDouble(),
      justificacion: json['justificacion'] as String,
    );
  }
}

class EscenarioOptimizadoModel extends EscenarioOptimizado {
  const EscenarioOptimizadoModel({
    required super.id,
    required super.proyectoId,
    required super.planoId,
    required super.mapaActualId,
    required super.mapaProyectadoId,
    required super.nombre,
    required super.banda,
    required super.modeloAp,
    required super.pctCoberturaActual,
    required super.pctCobertura,
    required super.costoEstimado,
    required super.cantidadAps,
    required super.resumen,
    required super.restricciones,
    required super.metricas,
    required super.recomendaciones,
    required super.createdAt,
  });

  factory EscenarioOptimizadoModel.fromJson(Map<String, dynamic> json) {
    return EscenarioOptimizadoModel(
      id: json['id'] as int,
      proyectoId: json['proyecto_id'] as int,
      planoId: json['plano_id'] as int,
      mapaActualId: json['mapa_actual_id'] as int?,
      mapaProyectadoId: json['mapa_proyectado_id'] as int?,
      nombre: json['nombre'] as String,
      banda: json['banda'] as String,
      modeloAp: json['modelo_ap'] as String,
      pctCoberturaActual: (json['pct_cobertura_actual'] as num).toDouble(),
      pctCobertura: (json['pct_cobertura'] as num).toDouble(),
      costoEstimado: (json['costo_estimado'] as num).toDouble(),
      cantidadAps: json['cantidad_aps'] as int,
      resumen: json['resumen'] as String,
      restricciones: Map<String, dynamic>.from(json['restricciones'] as Map),
      metricas: Map<String, dynamic>.from(json['metricas'] as Map),
      recomendaciones: (json['recomendaciones'] as List<dynamic>)
          .map((e) => RecomendacionAPModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}

class ResumenComparacionModel extends ResumenComparacion {
  const ResumenComparacionModel({
    required super.deltaPctCobertura,
    required super.deltaZonasMuertas,
    required super.costoEstimado,
    required super.cantidadCambios,
    required super.lectura,
  });

  factory ResumenComparacionModel.fromJson(Map<String, dynamic> json) {
    return ResumenComparacionModel(
      deltaPctCobertura: (json['delta_pct_cobertura'] as num).toDouble(),
      deltaZonasMuertas: json['delta_zonas_muertas'] as int,
      costoEstimado: (json['costo_estimado'] as num).toDouble(),
      cantidadCambios: json['cantidad_cambios'] as int,
      lectura: json['lectura'] as String,
    );
  }
}

class ComparacionEscenarioModel extends ComparacionEscenario {
  const ComparacionEscenarioModel({
    required super.escenario,
    required super.heatmapActual,
    required super.heatmapProyectado,
    required super.matrizDiferencia,
    required super.resumen,
  });

  factory ComparacionEscenarioModel.fromJson(Map<String, dynamic> json) {
    return ComparacionEscenarioModel(
      escenario: EscenarioOptimizadoModel.fromJson(
        json['escenario'] as Map<String, dynamic>,
      ),
      heatmapActual: MapaCalorModel.fromJson(
        json['heatmap_actual'] as Map<String, dynamic>,
      ),
      heatmapProyectado: MapaCalorModel.fromJson(
        json['heatmap_proyectado'] as Map<String, dynamic>,
      ),
      matrizDiferencia: (json['matriz_diferencia'] as List<dynamic>)
          .map(
            (fila) => (fila as List<dynamic>)
                .map((v) => (v as num).toDouble())
                .toList(),
          )
          .toList(),
      resumen: ResumenComparacionModel.fromJson(
        json['resumen'] as Map<String, dynamic>,
      ),
    );
  }
}

class ReporteTecnicoModel extends ReporteTecnico {
  const ReporteTecnicoModel({
    required super.id,
    required super.proyectoId,
    required super.escenarioId,
    required super.estado,
    required super.urlDescarga,
    required super.sha256,
    required super.tamanioBytes,
    required super.error,
  });

  factory ReporteTecnicoModel.fromJson(Map<String, dynamic> json) {
    return ReporteTecnicoModel(
      id: json['id'] as int,
      proyectoId: json['proyecto_id'] as int,
      escenarioId: json['escenario_id'] as int?,
      estado: json['estado'] as String,
      urlDescarga: json['url_descarga'] as String?,
      sha256: json['sha256'] as String?,
      tamanioBytes: json['tamanio_bytes'] as int,
      error: json['error'] as String?,
    );
  }
}
