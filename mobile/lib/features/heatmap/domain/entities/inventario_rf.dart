import 'package:equatable/equatable.dart';

class RadioInventarioRF extends Equatable {
  final int id;
  final String banda;
  final int canal;
  final int anchoCanalMhz;
  final double potenciaDbm;
  final double potenciaMaxDbm;
  final double eirpDbm;

  const RadioInventarioRF({
    required this.id,
    required this.banda,
    required this.canal,
    required this.anchoCanalMhz,
    required this.potenciaDbm,
    required this.potenciaMaxDbm,
    required this.eirpDbm,
  });

  @override
  List<Object?> get props => [
        id,
        banda,
        canal,
        anchoCanalMhz,
        potenciaDbm,
        potenciaMaxDbm,
        eirpDbm,
      ];
}

class APFisicoRF extends Equatable {
  final int id;
  final String nombre;
  final String fabricante;
  final String modelo;
  final String rol;
  final String restriccionMovimiento;
  final double coordX;
  final double coordY;
  final double alturaM;
  final bool verificado;
  final List<RadioInventarioRF> radios;

  const APFisicoRF({
    required this.id,
    required this.nombre,
    required this.fabricante,
    required this.modelo,
    required this.rol,
    required this.restriccionMovimiento,
    required this.coordX,
    required this.coordY,
    required this.alturaM,
    required this.verificado,
    required this.radios,
  });

  @override
  List<Object?> get props => [id, nombre, fabricante, modelo, radios];
}

class InventarioRF extends Equatable {
  final int planoId;
  final List<APFisicoRF> aps;
  final double porcentajeCompletitud;
  final String nivelCompletitud;
  final List<String> bloqueos;
  final List<String> advertencias;

  const InventarioRF({
    required this.planoId,
    required this.aps,
    required this.porcentajeCompletitud,
    required this.nivelCompletitud,
    required this.bloqueos,
    required this.advertencias,
  });

  @override
  List<Object?> get props =>
      [planoId, aps, porcentajeCompletitud, nivelCompletitud];
}
