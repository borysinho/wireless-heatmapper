import 'package:equatable/equatable.dart';

import 'ap_disponible.dart';

class ConjuntoAP extends Equatable {
  final int id;
  final int planoId;
  final int? conjuntoOrigenId;
  final String nombre;
  final String proposito;
  final String? descripcion;
  final bool esPrincipal;
  final String origen;
  final String estadoGobernanza;
  final int? creadoPorId;
  final int cantidadAps;
  final List<APDisponible> items;
  final DateTime createdAt;
  final DateTime updatedAt;

  const ConjuntoAP({
    required this.id,
    required this.planoId,
    this.conjuntoOrigenId,
    required this.nombre,
    required this.proposito,
    required this.descripcion,
    required this.esPrincipal,
    this.origen = 'manual_movil',
    this.estadoGobernanza = 'borrador_tecnico',
    this.creadoPorId,
    required this.cantidadAps,
    required this.items,
    required this.createdAt,
    required this.updatedAt,
  });

  @override
  List<Object?> get props => [
        id,
        planoId,
        conjuntoOrigenId,
        nombre,
        proposito,
        descripcion,
        esPrincipal,
        origen,
        estadoGobernanza,
        creadoPorId,
        cantidadAps,
        items,
        createdAt,
        updatedAt,
      ];
}
