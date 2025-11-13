import 'user.dart';

class AuthResponse {
  final String message;
  final String token; // 🔹 agregamos token
  final User user;

  AuthResponse({
    required this.message,
    required this.token,
    required this.user,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      message: json['message'],
      token: json['token'], // 🔹 tomamos token del JSON
      user: User.fromJson(json['user']),
    );
  }
}
