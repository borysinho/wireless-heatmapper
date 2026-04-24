import 'package:go_router/go_router.dart';

class AppRouter {
  AppRouter._();

  static final GoRouter router = GoRouter(
    initialLocation: '/login',
    routes: [
      // Sprint 1: PB-09 — Autenticar Usuario
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) {
          // Implementado en Sp-05 (PB-09)
          throw UnimplementedError('Pantalla de Login — pendiente Sp-05');
        },
      ),
      // Sprint 1: PB-10 — Ver Historial de Proyectos
      GoRoute(
        path: '/proyectos',
        name: 'proyectos',
        builder: (context, state) {
          throw UnimplementedError('Lista de Proyectos — pendiente Sp-17');
        },
      ),
    ],
  );
}
