import 'package:equatable/equatable.dart';

/// Rango de la leyenda CWNA-107 devuelta por el backend.
class EscalaHeatmap extends Equatable {
  final int desde;
  final int hasta;
  final String colorHex;
  final String etiqueta;

  const EscalaHeatmap({
    required this.desde,
    required this.hasta,
    required this.colorHex,
    required this.etiqueta,
  });

  @override
  List<Object?> get props => [desde, hasta, colorHex, etiqueta];
}
