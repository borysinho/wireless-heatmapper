import '../entities/analisis_cobertura.dart';
import '../entities/ap_disponible.dart';
import '../entities/ap_detectado.dart';
import '../entities/conjunto_ap.dart';
import '../entities/mapa_calor.dart';

abstract class HeatmapRepository {
  Future<List<APDisponible>> listarAPsDisponibles(int planoId);

  Future<List<ConjuntoAP>> listarConjuntosAP(int planoId);

  Future<ConjuntoAP> crearConjuntoAP({
    required int planoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required List<String> bssids,
  });

  Future<ConjuntoAP> actualizarConjuntoAP({
    required int conjuntoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required List<String> bssids,
  });

  Future<void> eliminarConjuntoAP(int conjuntoId);

  Future<ConjuntoAP> actualizarUbicacionAPConjunto({
    required int conjuntoId,
    required String bssid,
    required double posX,
    required double posY,
  });

  Future<MapaCalor> generarHeatmap({
    required int planoId,
    required String algoritmo,
    required int resolucion,
    required List<String> bssids,
    required List<double> apPosX,
    required List<double> apPosY,
  });

  Future<MapaCalor> generarHeatmapDesdeConjunto({
    required int conjuntoId,
    required String modo,
    required String algoritmo,
    required int resolucion,
    List<String>? bssids,
    List<double>? apPosX,
    List<double>? apPosY,
  });

  Future<AnalisisCobertura> analizarMapa(int mapaId);

  Future<APDetectado> confirmarAP({
    required int apId,
    required double posX,
    required double posY,
  });
}
