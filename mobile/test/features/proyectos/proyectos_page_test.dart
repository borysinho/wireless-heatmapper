import 'package:bloc_test/bloc_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:heatmapper/features/auth/presentation/bloc/auth_cubit.dart';
import 'package:heatmapper/features/auth/presentation/bloc/auth_state.dart';
import 'package:heatmapper/features/proyectos/domain/usecases/actualizar_proyecto_usecase.dart';
import 'package:heatmapper/features/proyectos/domain/usecases/archivar_proyecto_usecase.dart';
import 'package:heatmapper/features/proyectos/domain/usecases/crear_proyecto_usecase.dart';
import 'package:heatmapper/features/proyectos/domain/usecases/eliminar_proyecto_usecase.dart';
import 'package:heatmapper/features/proyectos/domain/usecases/obtener_proyectos_activos_usecase.dart';
import 'package:heatmapper/features/proyectos/presentation/bloc/proyecto_cubit.dart';
import 'package:heatmapper/features/proyectos/presentation/pages/proyectos_page.dart';
import 'package:heatmapper/main.dart' as app;
import 'package:mocktail/mocktail.dart';

class MockAuthCubit extends MockCubit<AuthState> implements AuthCubit {}

class MockObtenerProyectosActivosUseCase extends Mock
    implements ObtenerProyectosActivosUseCase {}

class MockCrearProyectoUseCase extends Mock implements CrearProyectoUseCase {}

class MockActualizarProyectoUseCase extends Mock
    implements ActualizarProyectoUseCase {}

class MockArchivarProyectoUseCase extends Mock
    implements ArchivarProyectoUseCase {}

class MockEliminarProyectoUseCase extends Mock
    implements EliminarProyectoUseCase {}

void main() {
  late MockAuthCubit authCubit;
  late MockObtenerProyectosActivosUseCase obtenerProyectos;
  late ProyectoCubit proyectoCubit;

  setUp(() async {
    await app.sl.reset();
    authCubit = MockAuthCubit();
    obtenerProyectos = MockObtenerProyectosActivosUseCase();
    when(() => authCubit.state).thenReturn(const AuthUnauthenticated());
    when(() => obtenerProyectos()).thenThrow(Exception('sin conexión'));
    app.sl.registerLazySingleton<AuthCubit>(() => authCubit);

    proyectoCubit = ProyectoCubit(
      obtenerActivos: obtenerProyectos,
      crear: MockCrearProyectoUseCase(),
      actualizar: MockActualizarProyectoUseCase(),
      archivar: MockArchivarProyectoUseCase(),
      eliminar: MockEliminarProyectoUseCase(),
    );
  });

  tearDown(() async {
    await proyectoCubit.close();
    await authCubit.close();
    await GetIt.instance.reset();
  });

  testWidgets(
    'muestra un solo botón Reintentar y recarga desde ProyectoCubit',
    (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: BlocProvider<ProyectoCubit>.value(
            value: proyectoCubit,
            child: const ProyectosPage(),
          ),
        ),
      );
      await tester.pump();
      await tester.pump();

      expect(
          find.text('No se pudo cargar la lista de proyectos.'), findsWidgets);
      expect(find.text('Reintentar'), findsOneWidget);
      verify(() => obtenerProyectos()).called(1);

      await tester.tap(find.text('Reintentar'));
      await tester.pump();
      await tester.pump();

      verify(() => obtenerProyectos()).called(1);
      expect(find.text('Reintentar'), findsOneWidget);
    },
  );
}
