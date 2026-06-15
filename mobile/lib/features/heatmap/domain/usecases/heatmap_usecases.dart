import '../entities/analisis_cobertura.dart';
import '../entities/ap_disponible.dart';
import '../entities/ap_detectado.dart';
import '../entities/mapa_calor.dart';
import '../repositories/heatmap_repository.dart';

class ListarAPsDisponiblesUseCase {
  final HeatmapRepository _repo;
  const ListarAPsDisponiblesUseCase(this._repo);

  Future<List<APDisponible>> call(int planoId) {
    return _repo.listarAPsDisponibles(planoId);
  }
}

class GenerarHeatmapUseCase {
  final HeatmapRepository _repo;
  const GenerarHeatmapUseCase(this._repo);

  Future<MapaCalor> call({
    required int planoId,
    required String algoritmo,
    required int resolucion,
    required String bssid,
    required double apPosX,
    required double apPosY,
  }) {
    return _repo.generarHeatmap(
      planoId: planoId,
      algoritmo: algoritmo,
      resolucion: resolucion,
      bssid: bssid,
      apPosX: apPosX,
      apPosY: apPosY,
    );
  }
}

class AnalizarMapaUseCase {
  final HeatmapRepository _repo;
  const AnalizarMapaUseCase(this._repo);

  Future<AnalisisCobertura> call(int mapaId) => _repo.analizarMapa(mapaId);
}

class ConfirmarAPUseCase {
  final HeatmapRepository _repo;
  const ConfirmarAPUseCase(this._repo);

  Future<APDetectado> call({
    required int apId,
    required double posX,
    required double posY,
  }) {
    return _repo.confirmarAP(apId: apId, posX: posX, posY: posY);
  }
}
