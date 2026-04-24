import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'app.dart';
import 'core/database/database_helper.dart';

final GetIt sl = GetIt.instance;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await _initDependencias();
  runApp(const HeatmapperApp());
}

Future<void> _initDependencias() async {
  sl.registerSingletonAsync<DatabaseHelper>(
    () async => DatabaseHelper.instance,
  );
  await sl.allReady();
}
