import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';
import '../../features/auth/presentation/bloc/auth_cubit.dart';
import '../../features/auth/presentation/bloc/auth_state.dart';
import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/proyectos/presentation/bloc/proyecto_cubit.dart';
import '../../features/proyectos/presentation/pages/proyectos_page.dart';
import '../../features/proyectos/presentation/pages/proyecto_form_page.dart';
import '../../main.dart';

class AppRouter {
  AppRouter._();

  static final GoRouter router = GoRouter(
    initialLocation: '/login',
    redirect: (context, routerState) async {
      // CA-3: si ya hay sesión activa, redirigir a /proyectos desde /login.
      // Se evalúa sólo en AuthAuthenticated para evitar loops.
      final authCubit = sl<AuthCubit>();
      if (authCubit.state is AuthAuthenticated &&
          routerState.matchedLocation == '/login') {
        return '/proyectos';
      }
      return null;
    },
    routes: [
      // Sprint 1: PB-09 — Autenticar Usuario (Sp-05)
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) {
          return BlocProvider<AuthCubit>.value(
            value: sl<AuthCubit>()..checkSesionActiva(),
            child: const LoginPage(),
          );
        },
      ),
      // Sprint 1: PB-01 / PB-10 — Gestionar y Ver Proyectos (Sp-13)
      GoRoute(
        path: '/proyectos',
        name: 'proyectos',
        builder: (context, state) {
          return BlocProvider<ProyectoCubit>(
            create: (_) => sl<ProyectoCubit>(),
            child: const ProyectosPage(),
          );
        },
        routes: [
          // Crear nuevo proyecto (Sp-13)
          GoRoute(
            path: 'nuevo',
            name: 'proyecto-nuevo',
            builder: (context, state) {
              final cubit = state.extra as ProyectoCubit;
              return BlocProvider<ProyectoCubit>.value(
                value: cubit,
                child: const ProyectoFormPage(),
              );
            },
          ),
          // Editar proyecto existente (Sp-13)
          GoRoute(
            path: ':id/editar',
            name: 'proyecto-editar',
            builder: (context, routeState) {
              // extra: Map con 'cubit' y 'proyecto'.
              final extra = routeState.extra as Map<String, dynamic>;
              final cubit = extra['cubit'] as ProyectoCubit;
              return BlocProvider<ProyectoCubit>.value(
                value: cubit,
                child: ProyectoFormPage(
                  proyectoExistente: extra['proyecto'] as dynamic,
                ),
              );
            },
          ),
          // Detalle de proyecto (pendiente PB-02 / PB-10 — Sprint 1)
          GoRoute(
            path: ':id',
            name: 'proyecto-detalle',
            builder: (context, routeState) {
              final id = routeState.pathParameters['id'] ?? '';
              return Scaffold(
                appBar: AppBar(title: Text('Proyecto #$id')),
                body: const Center(
                  child: Text('Detalle de proyecto — pendiente PB-02'),
                ),
              );
            },
          ),
        ],
      ),
    ],
  );
}
