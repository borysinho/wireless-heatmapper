import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/features/heatmap/domain/entities/ap_disponible.dart';
import 'package:heatmapper/features/heatmap/domain/entities/conjunto_ap.dart';
import 'package:heatmapper/features/heatmap/domain/entities/mapa_calor.dart';
import 'package:heatmapper/features/heatmap/domain/repositories/heatmap_repository.dart';
import 'package:heatmapper/features/heatmap/domain/usecases/heatmap_usecases.dart';
import 'package:heatmapper/features/heatmap/presentation/cubit/heatmap_cubit.dart';
import 'package:heatmapper/features/heatmap/presentation/pages/heatmap_page.dart';
import 'package:mocktail/mocktail.dart';

class _MockHeatmapRepository extends Mock implements HeatmapRepository {}

const _apDisponible = APDisponible(
  bssid: '3c:41:0e:a8:70:a0',
  ssid: 'LCM 5G',
  canal: 36,
  frecuenciaMhz: 5180,
  rssiPromedio: -61,
  posX: 100,
  posY: 120,
  cantidadPuntos: 8,
);

const _apSinUbicacion = APDisponible(
  bssid: '3c:41:0e:a8:70:a0',
  ssid: 'LCM 5G',
  canal: 36,
  frecuenciaMhz: 5180,
  rssiPromedio: -61,
  posX: 0,
  posY: 0,
  cantidadPuntos: 8,
  ubicacionConfirmada: false,
);

ConjuntoAP _conjuntoSinUbicacion() => ConjuntoAP(
      id: 9,
      planoId: 37,
      nombre: 'LCM 5G',
      proposito: 'Lecturas de red LCM 5 GHz',
      descripcion: null,
      esPrincipal: false,
      bandaObjetivo: '5',
      origen: 'manual_movil',
      cantidadAps: 1,
      items: const [_apSinUbicacion],
      createdAt: DateTime(2026, 6, 19),
      updatedAt: DateTime(2026, 6, 19),
    );

MapaCalor _mapaSinUbicacion(ConjuntoAP conjunto) => MapaCalor(
      id: 21,
      planoId: 37,
      conjuntoApId: conjunto.id,
      modoGeneracion: 'CONJUNTO_COMPLETO',
      algoritmo: 'IDW',
      resolucion: 128,
      bssid: 'CONJUNTO_9',
      ssid: conjunto.nombre,
      apPosX: 0,
      apPosY: 0,
      apsInteres: conjunto.items,
      bssidsGeneracion: [_apSinUbicacion.bssid],
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
    when(() => repo.listarAPsDisponibles(37))
        .thenAnswer((_) async => const [_apDisponible]);
    when(() => repo.listarConjuntosAP(37)).thenAnswer((_) async => const []);
    cubit = _crearCubit(repo);
  });

  tearDown(() => cubit.close());

  Future<void> abrirFormulario(WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<HeatmapCubit>.value(
          value: cubit,
          child: const HeatmapPage(
            proyectoId: 5,
            planoId: 37,
            imagenUrl: 'https://example.com/plano.png',
            anchoPlanoPx: 800,
            altoPlanoPx: 600,
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.byTooltip('Crear conjunto'));
    await tester.pumpAndSettle();
  }

  Future<void> guardarFormulario(WidgetTester tester) async {
    final botonGuardar = find.text('Guardar conjunto', skipOffstage: false);
    await tester.ensureVisible(botonGuardar);
    await tester.pumpAndSettle();
    await tester.tap(botonGuardar);
    await tester.pumpAndSettle();
  }

  testWidgets('muestra mensaje cuando falta el nombre del conjunto',
      (tester) async {
    await abrirFormulario(tester);

    await guardarFormulario(tester);

    expect(find.text('El nombre es obligatorio.'), findsWidgets);
    verifyNever(
      () => repo.crearConjuntoAP(
        planoId: any(named: 'planoId'),
        nombre: any(named: 'nombre'),
        proposito: any(named: 'proposito'),
        descripcion: any(named: 'descripcion'),
        bandaObjetivo: any(named: 'bandaObjetivo'),
        bssids: any(named: 'bssids'),
        configuracionesRadio: any(named: 'configuracionesRadio'),
      ),
    );
  });

  testWidgets('muestra mensaje cuando no hay AP seleccionado', (tester) async {
    await abrirFormulario(tester);

    await tester.enterText(find.byType(TextField).first, 'Conjunto 5 GHz');
    await tester.tap(find.text('Desmarcar todos'));
    await tester.pumpAndSettle();
    await guardarFormulario(tester);

    expect(find.text('Selecciona al menos un AP.'), findsWidgets);
    verifyNever(
      () => repo.crearConjuntoAP(
        planoId: any(named: 'planoId'),
        nombre: any(named: 'nombre'),
        proposito: any(named: 'proposito'),
        descripcion: any(named: 'descripcion'),
        bandaObjetivo: any(named: 'bandaObjetivo'),
        bssids: any(named: 'bssids'),
        configuracionesRadio: any(named: 'configuracionesRadio'),
      ),
    );
  });

  testWidgets('no dibuja marcador de AP sin ubicación en heatmap generado',
      (tester) async {
    final conjunto = _conjuntoSinUbicacion();
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
    ).thenAnswer((_) async => _mapaSinUbicacion(conjunto));

    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<HeatmapCubit>.value(
          value: cubit,
          child: const HeatmapPage(
            proyectoId: 5,
            planoId: 37,
            imagenUrl: 'https://example.com/plano.png',
            anchoPlanoPx: 800,
            altoPlanoPx: 600,
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    cubit.abrirConjunto(conjunto);
    await tester.pumpAndSettle();
    await cubit.generar(planoId: 37);
    await tester.pumpAndSettle();

    expect(find.byIcon(Icons.router), findsNothing);
  });
}
