import 'dart:typed_data';
import 'package:pointycastle/export.dart';
import 'dart:convert';

class PasswordHelper {
  PasswordHelper._();

  /// Genera un hash SHA-256 de la contraseña concatenada con un salt fijo.
  /// Para Sprint 1: implementación mínima. En producción usar bcrypt/Argon2.
  static String hashPassword(String password) {
    final digest = SHA256Digest();
    final input = utf8.encode('heatmapper_salt_$password');
    final hash = digest.process(Uint8List.fromList(input));
    return base64Encode(hash);
  }

  static bool verifyPassword(String password, String storedHash) {
    return hashPassword(password) == storedHash;
  }
}
