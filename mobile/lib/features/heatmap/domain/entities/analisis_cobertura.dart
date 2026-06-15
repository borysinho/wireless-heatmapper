import 'package:equatable/equatable.dart';

import 'ap_detectado.dart';

/// Diagnóstico automático de cobertura. Sprint 4 — PB-06.
class AnalisisCobertura extends Equatable {
  final int id;
  final int mapaCalorId;
  final double pctCobertura;
  final double pctZonasMuertas;
  final int celdasZonasMuertas;
  final int cantidadSolapamientos;
  final int cantidadInterferencias;
  final Map<String, dynamic> hallazgos;
  final String resumen;
  final List<APDetectado> apsDetectados;

  const AnalisisCobertura({
    required this.id,
    required this.mapaCalorId,
    required this.pctCobertura,
    required this.pctZonasMuertas,
    required this.celdasZonasMuertas,
    required this.cantidadSolapamientos,
    required this.cantidadInterferencias,
    required this.hallazgos,
    required this.resumen,
    required this.apsDetectados,
  });

  AnalisisCobertura copyWith({
    List<APDetectado>? apsDetectados,
  }) {
    return AnalisisCobertura(
      id: id,
      mapaCalorId: mapaCalorId,
      pctCobertura: pctCobertura,
      pctZonasMuertas: pctZonasMuertas,
      celdasZonasMuertas: celdasZonasMuertas,
      cantidadSolapamientos: cantidadSolapamientos,
      cantidadInterferencias: cantidadInterferencias,
      hallazgos: hallazgos,
      resumen: resumen,
      apsDetectados: apsDetectados ?? this.apsDetectados,
    );
  }

  @override
  List<Object?> get props => [
        id,
        mapaCalorId,
        pctCobertura,
        pctZonasMuertas,
        celdasZonasMuertas,
        cantidadSolapamientos,
        cantidadInterferencias,
        hallazgos,
        resumen,
        apsDetectados,
      ];
}
