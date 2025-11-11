import 'user.dart';
class AuthResponse {
  final String message;
  final User user;

  AuthResponse({required this.message, required this.user});

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      message: json['message'],
      user: User.fromJson(json['user']),
    );
  }
}