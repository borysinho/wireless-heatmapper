import 'package:equatable/equatable.dart';

import 'ap_disponible.dart';

class ConjuntoAP extends Equatable {
  final int id;
  final int planoId;
  final String nombre;
  final String proposito;
  final String? descripcion;
  final bool esPrincipal;
  final int cantidadAps;
  final List<APDisponible> items;
  final DateTime createdAt;
  final DateTime updatedAt;

  const ConjuntoAP({
    required this.id,
    required this.planoId,
    required this.nombre,
    required this.proposito,
    required this.descripcion,
    required this.esPrincipal,
    required this.cantidadAps,
    required this.items,
    required this.createdAt,
    required this.updatedAt,
  });

  @override
  List<Object?> get props => [
        id,
        planoId,
        nombre,
        proposito,
        descripcion,
        esPrincipal,
        cantidadAps,
        items,
        createdAt,
        updatedAt,
      ];
}
