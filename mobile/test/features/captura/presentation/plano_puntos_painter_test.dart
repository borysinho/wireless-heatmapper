import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/features/captura/domain/entities/nivel_senal.dart';
import 'package:heatmapper/features/captura/domain/entities/punto_medicion.dart';
import 'package:heatmapper/features/captura/presentation/widgets/plano_puntos_painter.dart';

void main() {
  group('PlanoPuntosPainter', () {
    test('detecta un punto cargado usando distancia en pantalla', () {
      const punto = PuntoMedicion(
        id: 7,
        planoId: 3,
        posX: 1000,
        posY: 500,
        nivel: NivelSenal.verde,
      );

      final seleccionado = PlanoPuntosPainter.puntoEnPosicionPantalla(
        tapOffset: const Offset(102, 52),
        canvasSize: const Size(400, 200),
        tamanoPlano: const Size(4000, 2000),
        puntos: const [punto],
      );

      expect(seleccionado?.id, 7);
    });

    test('ignora taps fuera del radio visible del marcador', () {
      const punto = PuntoMedicion(
        id: 7,
        planoId: 3,
        posX: 1000,
        posY: 500,
        nivel: NivelSenal.verde,
      );

      final seleccionado = PlanoPuntosPainter.puntoEnPosicionPantalla(
        tapOffset: const Offset(180, 120),
        canvasSize: const Size(400, 200),
        tamanoPlano: const Size(4000, 2000),
        puntos: const [punto],
      );

      expect(seleccionado, isNull);
    });
  });
}
