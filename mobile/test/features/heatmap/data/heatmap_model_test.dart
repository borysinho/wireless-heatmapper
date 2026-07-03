import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/features/heatmap/data/models/ap_disponible_model.dart';
import 'package:heatmapper/features/heatmap/data/models/conjunto_ap_model.dart';
import 'package:heatmapper/features/heatmap/data/models/mapa_calor_model.dart';

void main() {
  test('APDisponibleModel preserva ausencia de ubicación confirmada', () {
    final ap = APDisponibleModel.fromJson(const {
      'bssid': '3c:41:0e:a8:70:a0',
      'ssid': 'LCM',
      'canal': 1,
      'frecuencia_mhz': 2412,
      'rssi_promedio': -62,
      'pos_x': null,
      'pos_y': null,
      'cantidad_puntos': 13,
    });

    expect(ap.posX, 0);
    expect(ap.posY, 0);
    expect(ap.ubicacionConfirmada, isFalse);
  });

  test('ConjuntoAPModel no confirma ubicación cuando el item no trae posición',
      () {
    final conjunto = ConjuntoAPModel.fromJson({
      'id': 9,
      'plano_id': 37,
      'conjunto_origen_id': null,
      'nombre': 'LCM 2.4',
      'proposito': 'Lecturas de red LCM 2.4 GHz',
      'descripcion': null,
      'es_principal': false,
      'banda_objetivo': '2.4',
      'origen': 'manual_movil',
      'creado_por_id': 4,
      'resumen_ia': null,
      'metricas_ia': null,
      'restricciones_ia': null,
      'version_motor_ia': null,
      'cantidad_aps': 1,
      'items': const [
        {
          'bssid': '3c:41:0e:a8:70:a0',
          'ssid': 'LCM',
          'canal': 1,
          'frecuencia_mhz': 2412,
          'rssi_promedio': -62,
          'pos_x': null,
          'pos_y': null,
          'cantidad_puntos': 13,
        },
      ],
      'created_at': '2026-06-19T12:00:00',
      'updated_at': '2026-06-19T12:00:00',
    });

    expect(conjunto.items.single.posX, 0);
    expect(conjunto.items.single.posY, 0);
    expect(conjunto.items.single.ubicacionConfirmada, isFalse);
  });

  test('MapaCalorModel mantiene APs de interés sin ubicación confirmada', () {
    final mapa = MapaCalorModel.fromJson({
      'id': 21,
      'plano_id': 37,
      'conjunto_ap_id': 9,
      'modo_generacion': 'CONJUNTO_COMPLETO',
      'algoritmo': 'IDW',
      'resolucion': 128,
      'bssid': 'CONJUNTO_9',
      'ssid': 'LCM 2.4',
      'ap_pos_x': 0,
      'ap_pos_y': 0,
      'aps_interes': const [
        {
          'bssid': '3c:41:0e:a8:70:a0',
          'ssid': 'LCM',
          'canal': 1,
          'frecuencia_mhz': 2412,
          'rssi_promedio': -62,
          'pos_x': null,
          'pos_y': null,
          'cantidad_puntos': 13,
        },
      ],
      'bssids_generacion': const ['3c:41:0e:a8:70:a0'],
      'url_imagen': '',
      'matriz': const [
        [0, 0],
        [0, 0],
      ],
      'escala': const [],
      'cantidad_puntos': 2,
      'rssi_min': -80,
      'rssi_max': -45,
      'rssi_promedio': -62.5,
      'puntos_lectura': const [],
      'poligono_interes': const [],
      'advertencias': const [],
      'created_at': '2026-06-19T12:00:00',
    });

    expect(mapa.apsInteres.single.posX, 0);
    expect(mapa.apsInteres.single.posY, 0);
    expect(mapa.apsInteres.single.ubicacionConfirmada, isFalse);
  });
}
