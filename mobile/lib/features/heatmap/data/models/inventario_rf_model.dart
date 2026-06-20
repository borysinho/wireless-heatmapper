import '../../domain/entities/inventario_rf.dart';

class RadioInventarioRFModel extends RadioInventarioRF {
  const RadioInventarioRFModel({
    required super.id,
    required super.banda,
    required super.canal,
    required super.anchoCanalMhz,
    required super.potenciaDbm,
    required super.potenciaMaxDbm,
    required super.eirpDbm,
  });

  factory RadioInventarioRFModel.fromJson(Map<String, dynamic> json) {
    return RadioInventarioRFModel(
      id: json['id'] as int,
      banda: json['banda'] as String,
      canal: json['canal'] as int,
      anchoCanalMhz: json['ancho_canal_mhz'] as int,
      potenciaDbm: (json['potencia_dbm'] as num).toDouble(),
      potenciaMaxDbm: (json['potencia_max_dbm'] as num).toDouble(),
      eirpDbm: (json['eirp_dbm'] as num).toDouble(),
    );
  }
}

class APFisicoRFModel extends APFisicoRF {
  const APFisicoRFModel({
    required super.id,
    required super.nombre,
    required super.fabricante,
    required super.modelo,
    required super.rol,
    required super.restriccionMovimiento,
    required super.coordX,
    required super.coordY,
    required super.alturaM,
    required super.verificado,
    required super.radios,
  });

  factory APFisicoRFModel.fromJson(Map<String, dynamic> json) {
    return APFisicoRFModel(
      id: json['id'] as int,
      nombre: json['nombre'] as String,
      fabricante: json['fabricante'] as String,
      modelo: json['modelo'] as String,
      rol: json['rol'] as String,
      restriccionMovimiento: json['restriccion_movimiento'] as String,
      coordX: (json['coord_x'] as num).toDouble(),
      coordY: (json['coord_y'] as num).toDouble(),
      alturaM: (json['altura_m'] as num).toDouble(),
      verificado: json['verificado'] as bool,
      radios: (json['radios'] as List<dynamic>)
          .map(
              (e) => RadioInventarioRFModel.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }
}

class InventarioRFModel extends InventarioRF {
  const InventarioRFModel({
    required super.planoId,
    required super.aps,
    required super.porcentajeCompletitud,
    required super.nivelCompletitud,
    required super.bloqueos,
    required super.advertencias,
  });

  factory InventarioRFModel.fromJson(Map<String, dynamic> json) {
    return InventarioRFModel(
      planoId: json['plano_id'] as int,
      aps: (json['aps'] as List<dynamic>)
          .map((e) => APFisicoRFModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      porcentajeCompletitud: (json['porcentaje_completitud'] as num).toDouble(),
      nivelCompletitud: json['nivel_completitud'] as String,
      bloqueos: (json['bloqueos'] as List<dynamic>).cast<String>(),
      advertencias: (json['advertencias'] as List<dynamic>).cast<String>(),
    );
  }
}
