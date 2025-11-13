import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import '../models/auth_response.dart';
import 'api.dart';

class AuthService {
  static final AuthService _instance = AuthService._internal();
  factory AuthService() => _instance;
  AuthService._internal();

  User? _user;
  String? _token;

  User? get user => _user;
  bool get isAuthenticated => _token != null;

  /// 🔹 Login básico
  Future<AuthResponse> login(String username, String password) async {
    final response = await ApiService.post('/auth/login/', {
      'username': username,
      'password': password,
    });

    if (response.statusCode == 200) {
      final authResponse = AuthResponse.fromJson(jsonDecode(response.body));
      _user = authResponse.user;
      _token = authResponse.token;

      // Guardar localmente
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('user', jsonEncode(_user!.toJson()));
      await prefs.setString('token', _token!);
      await prefs.setBool('is_logged_in', true);

      return authResponse;
    } else {
      throw Exception('Error al iniciar sesión');
    }
  }

  /// 🔹 Logout básico
  Future<void> logout() async {
    _user = null;
    _token = null;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('user');
    await prefs.remove('token');
    await prefs.setBool('is_logged_in', false);
  }

  /// 🔹 Obtener usuario actual
  Future<User?> getCurrentUser() async {
    if (_user != null) return _user;
    final prefs = await SharedPreferences.getInstance();
    final userString = prefs.getString('user');
    if (userString != null) {
      _user = User.fromJson(jsonDecode(userString));
      _token = prefs.getString('token');
      return _user;
    }
    return null;
  }

  /// 🔹 Verificar sesión activa
  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    final loggedIn = prefs.getBool('is_logged_in') ?? false;
    if (loggedIn) await getCurrentUser();
    return loggedIn;
  }
}
