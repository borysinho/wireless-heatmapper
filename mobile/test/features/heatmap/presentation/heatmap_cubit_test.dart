import 'dart:async';

import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/features/heatmap/domain/entities/ap_disponible.dart';
import 'package:heatmapper/features/heatmap/domain/entities/conjunto_ap.dart';
import 'package:heatmapper/features/heatmap/domain/entities/mapa_calor.dart';
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
  double posXSecundario = 220,
  double posYSecundario = 260,
  bool ubicacionConfirmada = true,
  bool ubicacionSecundariaConfirmada = true,
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
          ubicacionConfirmada: ubicacionConfirmada,
        ),
        APDisponible(
          bssid: _apSecundario.bssid,
          ssid: _apSecundario.ssid,
          canal: _apSecundario.canal,
          frecuenciaMhz: _apSecundario.frecuenciaMhz,
          rssiPromedio: _apSecundario.rssiPromedio,
          posX: posXSecundario,
          posY: posYSecundario,
          cantidadPuntos: _apSecundario.cantidadPuntos,
          ubicacionConfirmada: ubicacionSecundariaConfirmada,
        ),
      ],
      createdAt: DateTime(2026, 6, 19),
      updatedAt: DateTime(2026, 6, 19),
    );

MapaCalor _mapaConjunto(ConjuntoAP conjunto) => MapaCalor(
      id: 21,
      planoId: conjunto.planoId,
      conjuntoApId: conjunto.id,
      modoGeneracion: 'CONJUNTO_COMPLETO',
      algoritmo: 'IDW',
      resolucion: 128,
      bssid: 'CONJUNTO_${conjunto.id}',
      ssid: conjunto.nombre,
      apPosX: 0,
      apPosY: 0,
      apsInteres: conjunto.items,
      bssidsGeneracion: conjunto.items.map((ap) => ap.bssid).toList(),
      urlImagen: '',
      matriz: const [
        [0, 0],
        [0, 0],
      ],
      escala: const [],
      cantidadPuntos: 2,
      rssiMin: -80,
      rssiMax: -45,
      rssiPromedio: -62.5,
      puntosLectura: const [],
      advertencias: const [],
      createdAt: DateTime(2026, 6, 19),
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

  test('no reutiliza posiciones detectadas al abrir conjunto sin ubicación',
      () async {
    final conjunto = _conjunto(
      ubicacionConfirmada: false,
      ubicacionSecundariaConfirmada: false,
    );
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apPrincipal, _apSecundario]);
    when(() => repo.listarConjuntosAP(37)).thenAnswer((_) async => [conjunto]);

    await cubit.iniciar(37);
    cubit.abrirConjunto(conjunto);

    final state = cubit.state;
    expect(state, isA<HeatmapSeleccionAP>());
    final seleccion = state as HeatmapSeleccionAP;
    expect(seleccion.apPosXPorBssid, isEmpty);
    expect(seleccion.apPosYPorBssid, isEmpty);
    expect(seleccion.aps.first.posX, 0);
    expect(seleccion.aps.first.ubicacionConfirmada, isFalse);
  });

  test('no envía coordenadas estimadas al generar desde conjunto sin ubicación',
      () async {
    final conjunto = _conjunto(
      ubicacionConfirmada: false,
      ubicacionSecundariaConfirmada: false,
    );
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apPrincipal, _apSecundario]);
    when(() => repo.listarConjuntosAP(37)).thenAnswer((_) async => [conjunto]);
    when(
      () => repo.generarHeatmapDesdeConjunto(
        conjuntoId: 9,
        modo: any(named: 'modo'),
        algoritmo: any(named: 'algoritmo'),
        resolucion: any(named: 'resolucion'),
        bssids: any(named: 'bssids'),
        apPosX: null,
        apPosY: null,
      ),
    ).thenAnswer((_) async => _mapaConjunto(conjunto));

    await cubit.iniciar(37);
    cubit.abrirConjunto(conjunto);
    await cubit.generar(planoId: 37);

    verify(
      () => repo.generarHeatmapDesdeConjunto(
        conjuntoId: 9,
        modo: 'CONJUNTO_COMPLETO',
        algoritmo: 'IDW',
        resolucion: 128,
        bssids: any(named: 'bssids'),
        apPosX: null,
        apPosY: null,
      ),
    ).called(1);
    expect(cubit.state, isA<HeatmapReady>());
    final listo = cubit.state as HeatmapReady;
    expect(listo.apPosXPorBssid, isEmpty);
    expect(listo.apPosYPorBssid, isEmpty);
  });

  test('envía coordenadas confirmadas al generar desde conjunto ubicado',
      () async {
    final conjunto = _conjunto(
      posX: 340,
      posY: 280,
      posXSecundario: 410,
      posYSecundario: 300,
    );
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apPrincipal, _apSecundario]);
    when(() => repo.listarConjuntosAP(37)).thenAnswer((_) async => [conjunto]);
    when(
      () => repo.generarHeatmapDesdeConjunto(
        conjuntoId: 9,
        modo: any(named: 'modo'),
        algoritmo: any(named: 'algoritmo'),
        resolucion: any(named: 'resolucion'),
        bssids: any(named: 'bssids'),
        apPosX: any<List<double>?>(named: 'apPosX'),
        apPosY: any<List<double>?>(named: 'apPosY'),
      ),
    ).thenAnswer((_) async => _mapaConjunto(conjunto));

    await cubit.iniciar(37);
    cubit.abrirConjunto(conjunto);
    await cubit.generar(planoId: 37);

    final llamada = verify(
      () => repo.generarHeatmapDesdeConjunto(
        conjuntoId: 9,
        modo: 'INDIVIDUAL',
        algoritmo: 'IDW',
        resolucion: 128,
        bssids: any(named: 'bssids'),
        apPosX: captureAny<List<double>?>(named: 'apPosX'),
        apPosY: captureAny<List<double>?>(named: 'apPosY'),
      ),
    ).captured;
    expect(llamada[0], [340, 410]);
    expect(llamada[1], [280, 300]);
  });

  test('espera guardado de ubicación antes de generar desde conjunto',
      () async {
    final conjunto = _conjunto(
      ubicacionConfirmada: false,
      ubicacionSecundariaConfirmada: false,
    );
    final guardado = Completer<ConjuntoAP>();
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apPrincipal, _apSecundario]);
    when(() => repo.listarConjuntosAP(37)).thenAnswer((_) async => [conjunto]);
    when(
      () => repo.actualizarUbicacionAPConjunto(
        conjuntoId: 9,
        bssid: _apPrincipal.bssid,
        posX: 340,
        posY: 280,
      ),
    ).thenAnswer((_) => guardado.future);
    when(
      () => repo.generarHeatmapDesdeConjunto(
        conjuntoId: 9,
        modo: any(named: 'modo'),
        algoritmo: any(named: 'algoritmo'),
        resolucion: any(named: 'resolucion'),
        bssids: any(named: 'bssids'),
        apPosX: any<List<double>?>(named: 'apPosX'),
        apPosY: any<List<double>?>(named: 'apPosY'),
      ),
    ).thenAnswer((_) async => _mapaConjunto(_conjunto(posX: 340, posY: 280)));

    await cubit.iniciar(37);
    cubit.abrirConjunto(conjunto);
    cubit.alternarAPInteres(_apSecundario);
    cubit.ubicarAP(bssid: _apPrincipal.bssid, posX: 340, posY: 280);
    final generacion = cubit.generar(planoId: 37);
    await Future<void>.delayed(Duration.zero);

    verifyNever(
      () => repo.generarHeatmapDesdeConjunto(
        conjuntoId: any(named: 'conjuntoId'),
        modo: any(named: 'modo'),
        algoritmo: any(named: 'algoritmo'),
        resolucion: any(named: 'resolucion'),
        bssids: any(named: 'bssids'),
        apPosX: any<List<double>?>(named: 'apPosX'),
        apPosY: any<List<double>?>(named: 'apPosY'),
      ),
    );

    guardado.complete(_conjunto(posX: 340, posY: 280));
    await generacion;

    verify(
      () => repo.generarHeatmapDesdeConjunto(
        conjuntoId: 9,
        modo: 'CONJUNTO_COMPLETO',
        algoritmo: 'IDW',
        resolucion: 128,
        bssids: any(named: 'bssids'),
        apPosX: any<List<double>?>(named: 'apPosX'),
        apPosY: any<List<double>?>(named: 'apPosY'),
      ),
    ).called(1);
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
