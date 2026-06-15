import '../entities/analisis_cobertura.dart';
import '../entities/ap_disponible.dart';
import '../entities/ap_detectado.dart';
import '../entities/mapa_calor.dart';

abstract class HeatmapRepository {
  Future<List<APDisponible>> listarAPsDisponibles(int planoId);

  Future<MapaCalor> generarHeatmap({
    required int planoId,
    required String algoritmo,
    required int resolucion,
    required String bssid,
    required double apPosX,
    required double apPosY,
  });

  Future<AnalisisCobertura> analizarMapa(int mapaId);

  Future<APDetectado> confirmarAP({
    required int apId,
    required double posX,
    required double posY,
  });
}
