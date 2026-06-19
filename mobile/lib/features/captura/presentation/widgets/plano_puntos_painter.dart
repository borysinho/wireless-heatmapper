import 'package:flutter/material.dart';

import '../../../../core/theme/app_tokens.dart';
import '../../domain/entities/punto_medicion.dart';

/// Painter de Flutter Canvas que dibuja los puntos de medición sobre el plano.
/// Sprint 3 — PB-04 (Sp3-19).
///
/// Los puntos se renderizan como marcadores neutros de ubicación. El nivel de
/// señal se consulta en el detalle del punto o en el heatmap filtrado por AP.
class PlanoPuntosPainter extends CustomPainter {
  final List<PuntoMedicion> puntos;
  final int? puntoSeleccionadoId;
  final Size tamanoPlano;

  const PlanoPuntosPainter({
    required this.puntos,
    required this.tamanoPlano,
    this.puntoSeleccionadoId,
  });

  @override
  void paint(Canvas canvas, Size size) {
    if (tamanoPlano.isEmpty) return;

    final scaleX = size.width / tamanoPlano.width;
    final scaleY = size.height / tamanoPlano.height;

    for (final punto in puntos) {
      final cx = punto.posX * scaleX;
      final cy = punto.posY * scaleY;

      final seleccionado = punto.id == puntoSeleccionadoId;
      final radio = seleccionado ? 14.0 : 10.0;

      // Sombra
      canvas.drawCircle(
        Offset(cx + 1, cy + 1),
        radio + 1,
        Paint()..color = Colors.black26,
      );

      // Relleno
      canvas.drawCircle(
        Offset(cx, cy),
        radio,
        Paint()..color = kSeedColor,
      );

      // Borde blanco
      canvas.drawCircle(
        Offset(cx, cy),
        radio,
        Paint()
          ..color = Colors.white
          ..style = PaintingStyle.stroke
          ..strokeWidth = seleccionado ? 3 : 2,
      );
    }
  }

  @override
  bool shouldRepaint(PlanoPuntosPainter oldDelegate) =>
      oldDelegate.puntos != puntos ||
      oldDelegate.puntoSeleccionadoId != puntoSeleccionadoId ||
      oldDelegate.tamanoPlano != tamanoPlano;

  /// Convierte coordenadas de pantalla en coordenadas del plano.
  /// [tapOffset] es la posición del toque en el widget canvas.
  /// [canvasSize] es el tamaño actual del widget Canvas.
  static Offset pantallaToPlanoCoordenadas({
    required Offset tapOffset,
    required Size canvasSize,
    required Size tamanoPlano,
  }) {
    if (canvasSize.isEmpty || tamanoPlano.isEmpty) return tapOffset;
    final scaleX = tamanoPlano.width / canvasSize.width;
    final scaleY = tamanoPlano.height / canvasSize.height;
    return Offset(
      (tapOffset.dx * scaleX).clamp(0, tamanoPlano.width),
      (tapOffset.dy * scaleY).clamp(0, tamanoPlano.height),
    );
  }

  /// Retorna el [PuntoMedicion] más cercano al toque en coordenadas del plano,
  /// o `null` si ninguno está a menos de [radioTolerancia] píxeles del plano.
  static PuntoMedicion? puntoEnPosicion({
    required Offset posPlano,
    required List<PuntoMedicion> puntos,
    double radioTolerancia = 20,
  }) {
    PuntoMedicion? cercano;
    double minDist = radioTolerancia;
    for (final p in puntos) {
      final dist = (Offset(p.posX, p.posY) - posPlano).distance;
      if (dist < minDist) {
        minDist = dist;
        cercano = p;
      }
    }
    return cercano;
  }

  /// Retorna el punto más cercano al toque midiendo la distancia en pantalla.
  ///
  /// Esto evita que los puntos de planos grandes queden casi imposibles de
  /// tocar cuando el plano se renderiza reducido en el móvil.
  static PuntoMedicion? puntoEnPosicionPantalla({
    required Offset tapOffset,
    required Size canvasSize,
    required Size tamanoPlano,
    required List<PuntoMedicion> puntos,
    double radioToleranciaPantalla = 28,
  }) {
    if (canvasSize.isEmpty || tamanoPlano.isEmpty) return null;

    final scaleX = canvasSize.width / tamanoPlano.width;
    final scaleY = canvasSize.height / tamanoPlano.height;
    PuntoMedicion? cercano;
    var minDist = radioToleranciaPantalla;

    for (final punto in puntos) {
      final centroPantalla = Offset(
        punto.posX * scaleX,
        punto.posY * scaleY,
      );
      final dist = (centroPantalla - tapOffset).distance;
      if (dist < minDist) {
        minDist = dist;
        cercano = punto;
      }
    }
    return cercano;
  }
}
