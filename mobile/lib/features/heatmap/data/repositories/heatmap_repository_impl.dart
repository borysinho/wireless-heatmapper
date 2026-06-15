import '../../domain/entities/analisis_cobertura.dart';
import '../../domain/entities/ap_detectado.dart';
import '../../domain/entities/mapa_calor.dart';
import '../../domain/repositories/heatmap_repository.dart';
import '../datasources/heatmap_remote_datasource.dart';

class HeatmapRepositoryImpl implements HeatmapRepository {
  final HeatmapRemoteDatasource _datasource;

  const HeatmapRepositoryImpl(this._datasource);

  @override
  Future<MapaCalor> generarHeatmap({
    required int planoId,
    required String algoritmo,
    required int resolucion,
  }) {
    return _datasource.generarHeatmap(
      planoId: planoId,
      algoritmo: algoritmo,
      resolucion: resolucion,
    );
  }

  @override
  Future<AnalisisCobertura> analizarMapa(int mapaId) {
    return _datasource.analizarMapa(mapaId);
  }

  @override
  Future<APDetectado> confirmarAP({
    required int apId,
    required double posX,
    required double posY,
  }) {
    return _datasource.confirmarAP(apId: apId, posX: posX, posY: posY);
  }
}
