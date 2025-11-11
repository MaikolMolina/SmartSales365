import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import '../models/auth_response.dart';
import 'api.dart';
import 'notification_service.dart';

class AuthService {
  static final AuthService _instance = AuthService._internal();
  factory AuthService() => _instance;
  AuthService._internal();

  /// 🔹 Inicia sesión y guarda el usuario en SharedPreferences
  Future<AuthResponse> login(String username, String password) async {
    final response = await ApiService.post('/auth/login/', {
      'username': username,
      'password': password,
    });

    if (response.statusCode == 200) {
      final authResponse = AuthResponse.fromJson(jsonDecode(response.body));

      // Guardar usuario en SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('user', jsonEncode(authResponse.user.toJson()));
      await prefs.setBool('is_logged_in', true);

      // Enviar token FCM al backend después del login exitoso
      await _sendFcmTokenAfterLogin();

      return authResponse;
    } else {
      throw Exception('Error al iniciar sesión: ${response.statusCode}');
    }
  }

  /// 🔹 Cierra sesión, elimina token FCM y limpia datos locales
  Future<void> logout() async {
    try {
      // Remover token FCM del backend antes de hacer logout
      await _removeFcmTokenBeforeLogout();

      final response = await ApiService.post('/auth/logout/', {});

      // Limpiar SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('user');
      await prefs.remove('is_logged_in');
      await prefs.remove('session_cookie');
      await prefs.remove('fcm_token');

      if (response.statusCode != 200) {
        throw Exception('Error al cerrar sesión');
      }

      print('✅ Logout completado correctamente');
    } catch (e) {
      print('⚠️ Error durante logout: $e');

      // Continuar limpiando incluso si falla la comunicación
      final prefs = await SharedPreferences.getInstance();
      await prefs.clear();
    }
  }

  /// 🔹 Envía el token FCM al backend después de login
  Future<void> _sendFcmTokenAfterLogin() async {
    try {
      final notificationService = NotificationService();
      final token = await notificationService.getCurrentToken();

      if (token != null) {
        await ApiService.post('/auth/save_fcm_token/', {
          'fcm_token': token,
        });

        // Guardar token localmente
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('fcm_token', token);

        print('✅ Token FCM enviado al backend después del login');
      } else {
        print('⚠️ No se encontró token FCM para enviar');
      }
    } catch (e) {
      print('❌ Error enviando token FCM después del login: $e');
    }
  }

  /// 🔹 Informa al backend que el token FCM ya no debe usarse
  Future<void> _removeFcmTokenBeforeLogout() async {
    try {
      await ApiService.post('/auth/remove_fcm_token/', {});
      print('✅ Token FCM removido del backend antes del logout');
    } catch (e) {
      print('❌ Error removiendo token FCM antes del logout: $e');
    }
  }

  /// 🔹 Obtiene el usuario actual almacenado localmente
  Future<User?> getCurrentUser() async {
    final prefs = await SharedPreferences.getInstance();
    final userString = prefs.getString('user');

    if (userString != null) {
      return User.fromJson(jsonDecode(userString));
    }
    return null;
  }

  /// 🔹 Verifica si hay sesión activa
  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('is_logged_in') ?? false;
  }
}
