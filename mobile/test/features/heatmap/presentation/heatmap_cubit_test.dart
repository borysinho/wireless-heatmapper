import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/features/heatmap/domain/entities/ap_disponible.dart';
import 'package:heatmapper/features/heatmap/domain/entities/conjunto_ap.dart';
import 'package:heatmapper/features/heatmap/domain/repositories/heatmap_repository.dart';
import 'package:heatmapper/features/heatmap/domain/usecases/heatmap_usecases.dart';
import 'package:heatmapper/features/heatmap/presentation/cubit/heatmap_cubit.dart';
import 'package:heatmapper/features/heatmap/presentation/cubit/heatmap_state.dart';
import 'package:mocktail/mocktail.dart';

class _MockHeatmapRepository extends Mock implements HeatmapRepository {}

const _apPrincipal = APDisponible(
  bssid: '3c:41:0e:a8:70:a0',
  ssid: 'LCM',
  canal: 1,
  frecuenciaMhz: 2412,
  rssiPromedio: -62,
  posX: 100,
  posY: 120,
  cantidadPuntos: 13,
);

const _apSecundario = APDisponible(
  bssid: '3c:41:0e:a8:70:a1',
  ssid: 'LCM',
  canal: 6,
  frecuenciaMhz: 2437,
  rssiPromedio: -68,
  posX: 220,
  posY: 260,
  cantidadPuntos: 10,
);

ConjuntoAP _conjunto({
  double posX = 0,
  double posY = 0,
  int id = 9,
  String nombre = 'LCM 2.4',
  String origen = 'manual_movil',
}) =>
    ConjuntoAP(
      id: id,
      planoId: 37,
      nombre: nombre,
      proposito: 'Lecturas de red LCM 2.4 GHz',
      descripcion: null,
      esPrincipal: false,
      origen: origen,
      cantidadAps: 2,
      items: [
        APDisponible(
          bssid: _apPrincipal.bssid,
          ssid: _apPrincipal.ssid,
          canal: _apPrincipal.canal,
          frecuenciaMhz: _apPrincipal.frecuenciaMhz,
          rssiPromedio: _apPrincipal.rssiPromedio,
          posX: posX,
          posY: posY,
          cantidadPuntos: _apPrincipal.cantidadPuntos,
        ),
        _apSecundario,
      ],
      createdAt: DateTime(2026, 6, 19),
      updatedAt: DateTime(2026, 6, 19),
    );

HeatmapCubit _crearCubit(HeatmapRepository repo) => HeatmapCubit(
      listarAPs: ListarAPsDisponiblesUseCase(repo),
      listarConjuntos: ListarConjuntosAPUseCase(repo),
      crearConjunto: CrearConjuntoAPUseCase(repo),
      actualizarConjunto: ActualizarConjuntoAPUseCase(repo),
      prepararConjuntoIA: PrepararConjuntoIAUseCase(repo),
      eliminarConjunto: EliminarConjuntoAPUseCase(repo),
      generarHeatmap: GenerarHeatmapUseCase(repo),
      generarHeatmapDesdeConjunto: GenerarHeatmapDesdeConjuntoUseCase(repo),
      actualizarUbicacionAPConjunto: ActualizarUbicacionAPConjuntoUseCase(repo),
    );

void main() {
  late _MockHeatmapRepository repo;
  late HeatmapCubit cubit;

  setUp(() {
    repo = _MockHeatmapRepository();
    cubit = _crearCubit(repo);
  });

  tearDown(() => cubit.close());

  test('lista solo conjuntos creados por el técnico de campo', () async {
    final conjuntoCampo = _conjunto();
    final conjuntoIA = _conjunto(id: 10, nombre: 'Propuesta IA', origen: 'ia');
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apPrincipal, _apSecundario]);
    when(() => repo.listarConjuntosAP(37))
        .thenAnswer((_) async => [conjuntoIA, conjuntoCampo]);

    await cubit.iniciar(37);

    final state = cubit.state;
    expect(state, isA<HeatmapConjuntos>());
    expect((state as HeatmapConjuntos).conjuntos, [conjuntoCampo]);
  });

  test('persiste ubicación luego de seleccionar un AP dentro del conjunto',
      () async {
    final conjunto = _conjunto();
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apPrincipal, _apSecundario]);
    when(() => repo.listarConjuntosAP(37)).thenAnswer((_) async => [conjunto]);
    when(
      () => repo.actualizarUbicacionAPConjunto(
        conjuntoId: any(named: 'conjuntoId'),
        bssid: any(named: 'bssid'),
        posX: any(named: 'posX'),
        posY: any(named: 'posY'),
      ),
    ).thenAnswer((_) async => _conjunto(posX: 340, posY: 280));

    await cubit.iniciar(37);
    cubit.abrirConjunto(conjunto);
    cubit.activarAP(_apPrincipal);
    cubit.ubicarAP(bssid: _apPrincipal.bssid, posX: 340, posY: 280);

    await untilCalled(
      () => repo.actualizarUbicacionAPConjunto(
        conjuntoId: 9,
        bssid: _apPrincipal.bssid,
        posX: 340,
        posY: 280,
      ),
    );
    verify(
      () => repo.actualizarUbicacionAPConjunto(
        conjuntoId: 9,
        bssid: _apPrincipal.bssid,
        posX: 340,
        posY: 280,
      ),
    ).called(1);
  });

  test('no persiste movimientos transitorios durante el arrastre', () async {
    final conjunto = _conjunto();
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apPrincipal, _apSecundario]);
    when(() => repo.listarConjuntosAP(37)).thenAnswer((_) async => [conjunto]);

    await cubit.iniciar(37);
    cubit.abrirConjunto(conjunto);
    cubit.activarAP(_apPrincipal);
    cubit.ubicarAP(
      bssid: _apPrincipal.bssid,
      posX: 330,
      posY: 270,
      persistir: false,
    );

    verifyNever(
      () => repo.actualizarUbicacionAPConjunto(
        conjuntoId: any(named: 'conjuntoId'),
        bssid: any(named: 'bssid'),
        posX: any(named: 'posX'),
        posY: any(named: 'posY'),
      ),
    );
  });

  test('prepara IA en segundo plano luego de crear un conjunto', () async {
    final conjunto = _conjunto(id: 12, nombre: 'Conjunto nuevo');
    when(
      () => repo.crearConjuntoAP(
        planoId: any(named: 'planoId'),
        nombre: any(named: 'nombre'),
        proposito: any(named: 'proposito'),
        descripcion: any(named: 'descripcion'),
        bandaObjetivo: any(named: 'bandaObjetivo'),
        bssids: any(named: 'bssids'),
        configuracionesRadio: any(named: 'configuracionesRadio'),
      ),
    ).thenAnswer((_) async => conjunto);
    when(() => repo.prepararConjuntoIA(proyectoId: 5, conjuntoId: 12))
        .thenAnswer((_) async {});
    when(() => repo.listarConjuntosAP(37)).thenAnswer((_) async => [conjunto]);
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apPrincipal, _apSecundario]);

    await cubit.crearConjunto(
      proyectoId: 5,
      planoId: 37,
      nombre: 'Conjunto nuevo',
      proposito: 'Preparar propuestas IA',
      bandaObjetivo: '2.4',
      bssids: [_apPrincipal.bssid],
    );

    await untilCalled(
      () => repo.prepararConjuntoIA(proyectoId: 5, conjuntoId: 12),
    );
    verify(() => repo.prepararConjuntoIA(proyectoId: 5, conjuntoId: 12))
        .called(1);
  });
}
