import 'package:equatable/equatable.dart';

/// AP detectado en las mediciones del plano y disponible para generar heatmap.
class APDisponible extends Equatable {
  final String bssid;
  final String ssid;
  final int? canal;
  final int? frecuenciaMhz;
  final double rssiPromedio;
  final double posX;
  final double posY;
  final int cantidadPuntos;
  final bool seleccionado;

  const APDisponible({
    required this.bssid,
    required this.ssid,
    this.canal,
    this.frecuenciaMhz,
    required this.rssiPromedio,
    required this.posX,
    required this.posY,
    required this.cantidadPuntos,
    this.seleccionado = false,
  });

  @override
  List<Object?> get props => [
        bssid,
        ssid,
        canal,
        frecuenciaMhz,
        rssiPromedio,
        posX,
        posY,
        cantidadPuntos,
        seleccionado,
      ];
}
