import '../../domain/entities/ap_disponible.dart';
import '../../domain/entities/conjunto_ap.dart';
import '../../domain/entities/mapa_calor.dart';
import '../../domain/repositories/heatmap_repository.dart';
import '../datasources/heatmap_remote_datasource.dart';

class HeatmapRepositoryImpl implements HeatmapRepository {
  final HeatmapRemoteDatasource _datasource;

  const HeatmapRepositoryImpl(this._datasource);

  @override
  Future<List<APDisponible>> listarAPsDisponibles(int planoId) async {
    final aps = await _datasource.listarAPsDisponibles(planoId);
    return List<APDisponible>.of(aps);
  }

  @override
  Future<List<ConjuntoAP>> listarConjuntosAP(int planoId) async {
    final conjuntos = await _datasource.listarConjuntosAP(planoId);
    return List<ConjuntoAP>.of(conjuntos);
  }

  @override
  Future<ConjuntoAP> crearConjuntoAP({
    required int planoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required String bandaObjetivo,
    required List<String> bssids,
    List<Map<String, dynamic>> configuracionesRadio = const [],
  }) {
    return _datasource.crearConjuntoAP(
      planoId: planoId,
      nombre: nombre,
      proposito: proposito,
      descripcion: descripcion,
      bandaObjetivo: bandaObjetivo,
      bssids: bssids,
      configuracionesRadio: configuracionesRadio,
    );
  }

  @override
  Future<ConjuntoAP> actualizarConjuntoAP({
    required int conjuntoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required String bandaObjetivo,
    required List<String> bssids,
    List<Map<String, dynamic>> configuracionesRadio = const [],
  }) {
    return _datasource.actualizarConjuntoAP(
      conjuntoId: conjuntoId,
      nombre: nombre,
      proposito: proposito,
      descripcion: descripcion,
      bandaObjetivo: bandaObjetivo,
      bssids: bssids,
      configuracionesRadio: configuracionesRadio,
    );
  }

  @override
  Future<void> eliminarConjuntoAP(int conjuntoId) {
    return _datasource.eliminarConjuntoAP(conjuntoId);
  }

  @override
  Future<ConjuntoAP> actualizarUbicacionAPConjunto({
    required int conjuntoId,
    required String bssid,
    required double posX,
    required double posY,
  }) {
    return _datasource.actualizarUbicacionAPConjunto(
      conjuntoId: conjuntoId,
      bssid: bssid,
      posX: posX,
      posY: posY,
    );
  }

  @override
  Future<MapaCalor> generarHeatmap({
    required int planoId,
    required String algoritmo,
    required int resolucion,
    required List<String> bssids,
    required List<double> apPosX,
    required List<double> apPosY,
  }) {
    return _datasource.generarHeatmap(
      planoId: planoId,
      algoritmo: algoritmo,
      resolucion: resolucion,
      bssids: bssids,
      apPosX: apPosX,
      apPosY: apPosY,
    );
  }

  @override
  Future<MapaCalor> generarHeatmapDesdeConjunto({
    required int conjuntoId,
    required String modo,
    required String algoritmo,
    required int resolucion,
    List<String>? bssids,
    List<double>? apPosX,
    List<double>? apPosY,
  }) {
    return _datasource.generarHeatmapDesdeConjunto(
      conjuntoId: conjuntoId,
      modo: modo,
      algoritmo: algoritmo,
      resolucion: resolucion,
      bssids: bssids,
      apPosX: apPosX,
      apPosY: apPosY,
    );
  }
}
