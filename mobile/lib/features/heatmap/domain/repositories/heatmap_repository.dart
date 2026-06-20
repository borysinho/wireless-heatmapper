import '../entities/analisis_cobertura.dart';
import '../entities/ap_disponible.dart';
import '../entities/ap_detectado.dart';
import '../entities/conjunto_ap.dart';
import '../entities/escenario_optimizado.dart';
import '../entities/mapa_calor.dart';
import '../entities/inventario_rf.dart';

abstract class HeatmapRepository {
  Future<InventarioRF> obtenerInventarioRF(int proyectoId);

  Future<APFisicoRF> crearAPFisicoRF({
    required int proyectoId,
    required Map<String, dynamic> datos,
  });

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

  Future<List<EscenarioOptimizado>> generarEscenarios({
    required int proyectoId,
    required int maxAps,
    double? presupuesto,
    required String bandaPreferida,
    required List<String> bandas,
    required String tipoNegocio,
    required String perfil,
    required String politicaCombinacion,
    required String modeloAp,
    required double costoUnitario,
    int resolucion = 64,
  });

  Future<ComparacionEscenario> compararEscenario(int escenarioId);

  Future<ReporteTecnico> crearReporte({
    required int proyectoId,
    int? escenarioId,
  });

  Future<String> descargarReporte({
    required String urlDescarga,
    required String rutaDestino,
  });
}
