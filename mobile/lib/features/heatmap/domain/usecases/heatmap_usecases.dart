import '../entities/ap_disponible.dart';
import '../entities/conjunto_ap.dart';
import '../entities/mapa_calor.dart';
import '../repositories/heatmap_repository.dart';

class ListarAPsDisponiblesUseCase {
  final HeatmapRepository _repo;
  const ListarAPsDisponiblesUseCase(this._repo);

  Future<List<APDisponible>> call(int planoId) {
    return _repo.listarAPsDisponibles(planoId);
  }
}

class ListarConjuntosAPUseCase {
  final HeatmapRepository _repo;
  const ListarConjuntosAPUseCase(this._repo);

  Future<List<ConjuntoAP>> call(int planoId) {
    return _repo.listarConjuntosAP(planoId);
  }
}

class CrearConjuntoAPUseCase {
  final HeatmapRepository _repo;
  const CrearConjuntoAPUseCase(this._repo);

  Future<ConjuntoAP> call({
    required int planoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required List<String> bssids,
  }) {
    return _repo.crearConjuntoAP(
      planoId: planoId,
      nombre: nombre,
      proposito: proposito,
      descripcion: descripcion,
      bssids: bssids,
    );
  }
}

class ActualizarConjuntoAPUseCase {
  final HeatmapRepository _repo;
  const ActualizarConjuntoAPUseCase(this._repo);

  Future<ConjuntoAP> call({
    required int conjuntoId,
    required String nombre,
    required String proposito,
    String? descripcion,
    required List<String> bssids,
  }) {
    return _repo.actualizarConjuntoAP(
      conjuntoId: conjuntoId,
      nombre: nombre,
      proposito: proposito,
      descripcion: descripcion,
      bssids: bssids,
    );
  }
}

class EliminarConjuntoAPUseCase {
  final HeatmapRepository _repo;
  const EliminarConjuntoAPUseCase(this._repo);

  Future<void> call(int conjuntoId) => _repo.eliminarConjuntoAP(conjuntoId);
}

class GenerarHeatmapUseCase {
  final HeatmapRepository _repo;
  const GenerarHeatmapUseCase(this._repo);

  Future<MapaCalor> call({
    required int planoId,
    required String algoritmo,
    required int resolucion,
    required List<String> bssids,
    required List<double> apPosX,
    required List<double> apPosY,
  }) {
    return _repo.generarHeatmap(
      planoId: planoId,
      algoritmo: algoritmo,
      resolucion: resolucion,
      bssids: bssids,
      apPosX: apPosX,
      apPosY: apPosY,
    );
  }
}

class ActualizarUbicacionAPConjuntoUseCase {
  final HeatmapRepository _repo;
  const ActualizarUbicacionAPConjuntoUseCase(this._repo);

  Future<ConjuntoAP> call({
    required int conjuntoId,
    required String bssid,
    required double posX,
    required double posY,
  }) {
    return _repo.actualizarUbicacionAPConjunto(
      conjuntoId: conjuntoId,
      bssid: bssid,
      posX: posX,
      posY: posY,
    );
  }
}

class GenerarHeatmapDesdeConjuntoUseCase {
  final HeatmapRepository _repo;
  const GenerarHeatmapDesdeConjuntoUseCase(this._repo);

  Future<MapaCalor> call({
    required int conjuntoId,
    required String modo,
    required String algoritmo,
    required int resolucion,
    List<String>? bssids,
    List<double>? apPosX,
    List<double>? apPosY,
  }) {
    return _repo.generarHeatmapDesdeConjunto(
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
