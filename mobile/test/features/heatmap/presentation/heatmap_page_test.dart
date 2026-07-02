import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:heatmapper/features/heatmap/domain/entities/ap_disponible.dart';
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
}
