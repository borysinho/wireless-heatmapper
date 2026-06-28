import '../../domain/entities/punto_medicion.dart';
import '../../domain/entities/resultado_escaneo.dart';
import '../../domain/repositories/captura_repository.dart';
import '../../../planos/domain/entities/plano.dart';
import '../datasources/medicion_remote_datasource.dart';

/// Implementación concreta del repositorio de captura.
/// Delega en el datasource remoto.
class CapturaRepositoryImpl implements CapturaRepository {
  final MedicionRemoteDatasource _datasource;

  const CapturaRepositoryImpl(this._datasource);

  @override
  Future<PuntoMedicion> enviarLote({
    required int planoId,
    required double posX,
    required double posY,
    required List<ResultadoEscaneo> escaneos,
  }) =>
      _datasource.enviarLote(
        planoId: planoId,
        posX: posX,
        posY: posY,
        escaneos: escaneos,
      );

  @override
  Future<List<PuntoMedicion>> listarPuntos(int planoId) =>
      _datasource.listarPuntos(planoId);

  @override
  Future<List<PuntoPlano>> obtenerPoligonoInteres(int planoId) =>
      _datasource.obtenerPoligonoInteres(planoId);

  @override
  Future<List<PuntoPlano>> guardarPoligonoInteres({
    required int planoId,
    required List<PuntoPlano> puntos,
  }) =>
      _datasource.guardarPoligonoInteres(planoId: planoId, puntos: puntos);

  @override
  Future<List<PuntoPlano>> eliminarPoligonoInteres(int planoId) =>
      _datasource.eliminarPoligonoInteres(planoId);

  @override
  Future<List<PuntoPlano>> generarPoligonoInteresIA(int planoId) =>
      _datasource.generarPoligonoInteresIA(planoId);

  @override
  Future<PuntoMedicion> obtenerPunto(int puntoId) =>
      _datasource.obtenerPunto(puntoId);

  @override
  Future<PuntoMedicion> agregarMediciones({
    required int puntoId,
    required List<ResultadoEscaneo> escaneos,
  }) =>
      _datasource.agregarMediciones(puntoId: puntoId, escaneos: escaneos);

  @override
  Future<PuntoMedicion> moverPunto({
    required int puntoId,
    required double posX,
    required double posY,
  }) =>
      _datasource.moverPunto(puntoId: puntoId, posX: posX, posY: posY);

  @override
  Future<void> eliminarPunto(int puntoId) => _datasource.eliminarPunto(puntoId);
}
