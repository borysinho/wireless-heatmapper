import 'package:flutter/material.dart';
import 'core/navigation/app_router.dart';

class HeatmapperApp extends StatelessWidget {
  const HeatmapperApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Wireless HeatMapper',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF2980B9)),
        useMaterial3: true,
      ),
      routerConfig: AppRouter.router,
    );
  }
}
