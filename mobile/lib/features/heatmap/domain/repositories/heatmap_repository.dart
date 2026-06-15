import '../entities/analisis_cobertura.dart';
import '../entities/ap_detectado.dart';
import '../entities/mapa_calor.dart';

abstract class HeatmapRepository {
  Future<MapaCalor> generarHeatmap({
    required int planoId,
    required String algoritmo,
    required int resolucion,
  });

  Future<AnalisisCobertura> analizarMapa(int mapaId);

  Future<APDetectado> confirmarAP({
    required int apId,
    required double posX,
    required double posY,
  });
}
