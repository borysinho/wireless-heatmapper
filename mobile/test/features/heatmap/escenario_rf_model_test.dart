import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/features/heatmap/data/models/escenario_optimizado_model.dart';

void main() {
  test('interpreta escenario dual-band con configuración por radio', () {
    final escenario = EscenarioOptimizadoModel.fromJson({
      'id': 1,
      'proyecto_id': 2,
      'plano_id': 3,
      'mapa_actual_id': 4,
      'mapa_proyectado_id': 5,
      'nombre': 'Alternativa equilibrada',
      'tipo_negocio': 'RED_EXISTENTE',
      'perfil': 'PRIORIZAR_5_GHZ',
      'politica_combinacion': 'PREFERIR_5_GHZ_SI_CUMPLE_UMBRAL',
      'banda': '5',
      'bandas': ['2.4', '5'],
      'modelo_ap': 'AP empresarial',
      'pct_cobertura_actual': 60,
      'pct_cobertura': 90,
      'costo_estimado': 0,
      'cantidad_aps': 1,
      'resumen': 'Escenario proyectado.',
      'restricciones': <String, dynamic>{},
      'metricas': <String, dynamic>{},
      'mapas_por_banda': {
        '2.4': [
          [-60]
        ],
        '5': [
          [-66]
        ],
      },
      'supuestos': ['Antena verificada'],
      'confianza': 'ALTA',
      'version_motor': 'rf-hibrido-1.0',
      'recomendaciones': [
        {
          'id': 10,
          'orden': 1,
          'accion': 'RECONFIGURAR',
          'coord_x': 100,
          'coord_y': 80,
          'altura_m': 2.8,
          'tipo_montaje': 'TECHO',
          'banda': '5',
          'modelo_ap': 'AP empresarial',
          'costo_estimado': 0,
          'rssi_proyectado': -66,
          'radios': [
            {
              'banda': '2.4',
              'canal': 6,
              'ancho_canal_mhz': 20,
              'potencia_dbm': 8,
              'eirp_dbm': 10.14,
              'tipo_antena': 'OMNIDIRECCIONAL',
            },
            {
              'banda': '5',
              'canal': 44,
              'ancho_canal_mhz': 20,
              'potencia_dbm': 14,
              'eirp_dbm': 16.14,
              'tipo_antena': 'OMNIDIRECCIONAL',
            },
          ],
          'justificacion': 'Configuración por banda.',
        }
      ],
      'created_at': '2026-06-20T12:00:00Z',
    });

    expect(escenario.bandas, ['2.4', '5']);
    expect(escenario.confianza, 'ALTA');
    expect(escenario.recomendaciones.single.radios, hasLength(2));
    expect(escenario.recomendaciones.single.radios.last.canal, 44);
  });
}
