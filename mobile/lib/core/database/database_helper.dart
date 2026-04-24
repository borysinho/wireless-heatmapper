import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  DatabaseHelper._();
  static final DatabaseHelper instance = DatabaseHelper._();

  static const String _dbName = 'heatmapper.db';
  static const int _dbVersion = 1;

  Database? _db;

  Future<Database> get database async {
    _db ??= await _initDatabase();
    return _db!;
  }

  Future<Database> _initDatabase() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, _dbName);
    return openDatabase(
      path,
      version: _dbVersion,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    // Sprint 1: PB-09 — tabla usuario (Sp-01)
    await db.execute('''
      CREATE TABLE usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
      )
    ''');

    // Sprint 1: PB-01 — tabla proyecto (Sp-09)
    await db.execute('''
      CREATE TABLE proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cliente TEXT NOT NULL,
        descripcion TEXT,
        estado TEXT NOT NULL DEFAULT 'activo',
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        updated_at TEXT NOT NULL DEFAULT (datetime('now'))
      )
    ''');

    // Sprint 1: PB-02 — tabla plano (Sp-22)
    await db.execute('''
      CREATE TABLE plano (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proyecto_id INTEGER NOT NULL,
        ruta_archivo TEXT NOT NULL,
        nombre_original TEXT NOT NULL,
        tipo TEXT NOT NULL,
        escala_pixels_por_metro REAL,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (proyecto_id) REFERENCES proyecto (id) ON DELETE CASCADE
      )
    ''');
  }
}
